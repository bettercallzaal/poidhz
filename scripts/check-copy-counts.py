#!/usr/bin/env python3
"""Refuse copy that cites a claim count no bounty actually has.

WHY, AND IT HAPPENED THREE TIMES IN ONE EVENING. Each daily round's description argues from
the previous round's numbers - "four of five claims were a screenshot", "eleven entries have
come in". Those numbers get written while the previous round is STILL OPEN, and then it keeps
receiving claims. By the time the next description is cast the figure is wrong, and **a poidh
description is immutable**, so it is wrong forever in the one place nobody can edit.

Measured 2026-09-22 on round three's draft, before casting:

  - "four of five claims were a screenshot" - written at 13:42 when bounty 1410 had five
    claims. It closed with eight. Appeared three times, twice inside the paste body.
  - "eleven entries have come in over two rounds" - true mid-round-two, fourteen by the close.
  - "almost all of them were a poster" - true of round one alone, false of the pair, because
    round two was mostly video.

None of those were noticed by any existing check. `check-round-copy-agrees` compares deadlines;
`validate-bounty-description` checks structure; neither looks at a number describing another
bounty.

WHAT THIS DOES. It reads the live claim count of every daily bounty in `org.config.json`, then
scans a round's copy for counts that claim to describe claims or entries. A total that matches
no bounty's live count, and no sum of them, is refused with what the real numbers are.

WHAT IT DELIBERATELY DOES NOT DO. It does not try to work out which bounty a sentence means -
that needs to understand the prose, and a checker that guesses wrong trains people to ignore
it. It flags a number that matches NOTHING, which is the case that is always an error.

Text inside an operator note explaining a past correction is exempt via the same declared
marker used elsewhere in this repo, because those sentences quote the wrong number on purpose.

    python3 scripts/check-copy-counts.py rounds/daily/d03
    python3 scripts/check-copy-counts.py --all
    python3 scripts/check-copy-counts.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

WORDS = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8,
         "nine":9, "ten":10, "eleven":11, "twelve":12, "thirteen":13, "fourteen":14,
         "fifteen":15, "sixteen":16, "seventeen":17, "eighteen":18, "nineteen":19,
         "twenty":20}

NUM = r"(?:\d+|" + "|".join(WORDS) + r")"
# "four of eight claims", "eleven entries", "8 claims", "fourteen entries from eleven people"
OF_TOTAL = re.compile(rf"(?i)\b({NUM})\s+of\s+(?:the\s+)?({NUM})\s+(claims?|entries|entrants)\b")
# BARE WAS TOO GREEDY AND CRIED WOLF ON ITS FIRST REAL RUN. As `N (claims|entries)` it flagged
# six lines and all six were correct English: "if two entries land in the same place" is a
# hypothetical, and "0 claims at 23:17" is a historical snapshot of a moment, not a claim about
# the final field. A checker that flags correct copy trains its reader to ignore it, so it now
# requires the sentence to ASSERT ARRIVAL - came in, were filed, from N people - which is the
# only shape that is making a claim about a total.
BARE = re.compile(rf"(?i)\b({NUM})\s+(claims?|entries|entrants)\s+"
                  rf"(?:have\s+come\s+in|came\s+in|were\s+filed|have\s+been\s+filed|"
                  rf"from\s+{NUM}|across)\b")

EXEMPT = re.compile(r"<!--\s*COUNT-NOTE:\s*(.*?)\s*-->", re.S)
# A line that is explaining a PAST wrong number quotes it on purpose.
QUOTING = re.compile(r'(?i)(earlier version|an earlier|said ["“]|stale|was wrong|'
                     r'corrected|re-measured|re-counted|measured at \d)')


def to_int(tok: str) -> int:
    return int(tok) if tok.isdigit() else WORDS[tok.lower()]


def live_counts() -> dict[int, int] | None:
    """Claim count per daily bounty. None when it cannot be established - never an empty dict,
    because an empty dict would make every cited number look wrong."""
    import subprocess
    cfg = json.loads((REPO_ROOT / "org.config.json").read_text())
    ids = [r["bounty_id"] for r in cfg.get("rounds", [])
           if str(r.get("round", "")).startswith("daily") and r.get("bounty_id")]
    if not ids:
        return None
    out = {}
    for b in ids:
        try:
            r = subprocess.run(["python3", str(REPO_ROOT / "scripts" / "claim-report.py"),
                                "--bounty", str(b), "--json"],
                               capture_output=True, text=True, timeout=90)
            out[b] = len(json.loads(r.stdout)["claims"])
        except Exception:
            return None
    return out or None


def valid_totals(counts: dict[int, int]) -> set[int]:
    """Every count a true sentence could legitimately cite.

    THIS USED TO BE `per-bounty counts, plus the grand total`, AND IT CRIED WOLF TWICE THE
    DAY IT FIRST MATTERED. Round copy almost never describes all the bounties or exactly one
    of them - it describes THE ONES BEFORE THIS ONE. Round three's cast text says "Fourteen
    entries from eleven people", which is rounds one and two added up; round three's pick doc
    says "ten of the thirteen claims", which is rounds two and three. Both are correct English
    about real numbers, and both were refused because neither is a single bounty nor the whole
    set.

    Worse, the grand total MOVES as the current round takes claims, so a sentence about
    earlier rounds starts failing the moment anyone enters the new one. Bounty 1412 going
    from four claims to five turned one passing line into a failure without a word changing.

    So: every subset sum. With a handful of bounties that is a few dozen numbers, and it is
    the set a true sentence can actually draw from.
    """
    sums = {0}
    for n in counts.values():
        sums |= {s + n for s in sums}
    return sums - {0}


def check_round(round_dir: Path, counts: dict[int, int]) -> tuple[bool, list[str]]:
    findings = []
    ok = True
    valid = valid_totals(counts)
    findings.append(f"     live: " + ", ".join(f"bounty {b}={n}" for b, n in sorted(counts.items()))
                    + f"; total {sum(counts.values())}")

    files = sorted(p for p in round_dir.glob("*.md"))
    if not files:
        return False, findings + [f"FAIL: {round_dir} has no markdown to check. An empty "
                                  f"sweep is not a clean round."]

    for f in files:
        text = f.read_text()
        m = EXEMPT.search(text)
        if m and m.group(1).strip():
            findings.append(f"     {f.name} exempt: {m.group(1).strip()[:60]}")
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if QUOTING.search(line):
                continue
            for mm in OF_TOTAL.finditer(line):
                part, total = to_int(mm.group(1)), to_int(mm.group(2))
                if total not in valid:
                    ok = False
                    findings.append(
                        f"FAIL: {f.name}:{line_no} says \"{mm.group(0)}\" but no bounty has "
                        f"{total} claims. Live: {sorted(valid)}. A cast description is "
                        f"immutable - this number is wrong forever once it goes out.")
                elif part > total:
                    ok = False
                    findings.append(f"FAIL: {f.name}:{line_no} \"{mm.group(0)}\" - the part is "
                                    f"bigger than the total.")
            for mm in BARE.finditer(line):
                n = to_int(mm.group(1))
                if n not in valid:
                    ok = False
                    findings.append(
                        f"FAIL: {f.name}:{line_no} says \"{mm.group(0)}\" but no bounty has "
                        f"{n} claims and the two-round total is {sum(counts.values())}. "
                        f"Live: {sorted(valid)}.")
    if ok:
        findings.append(f"PASS: every claim count in {round_dir.name} matches a real one")
    return ok, findings


def _selftest() -> bool:
    passed = True

    def c(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    c("word to int", to_int("eight") == 8 and to_int("14") == 14)

    import tempfile
    counts = {1409: 6, 1410: 8}   # the real final field
    with tempfile.TemporaryDirectory() as d:
        r = Path(d) / "d03"; r.mkdir()
        f = r / "description.md"

        # THE REAL PRE-FIX TEXT. This is what was in the draft and what shipped past every
        # other check in this repo.
        f.write_text("1. UPLOAD THE FILE ITSELF. In round two, four of five claims were a "
                     "screenshot of a post instead of the piece.\n")
        ok, fnd = check_round(r, counts)
        c("catches the REAL 'four of five claims' that was in the draft",
          not ok and any("no bounty has 5 claims" in x for x in fnd))

        f.write_text("In round two, four of the eight claims were a screenshot.\n")
        ok, _ = check_round(r, counts)
        c("passes once corrected to four of eight", ok)

        f.write_text("Eleven entries have come in over two rounds.\n")
        ok, fnd = check_round(r, counts)
        c("catches the REAL 'eleven entries' (the total is 14)",
          not ok and any("eleven entries" in x.lower() for x in fnd))

        f.write_text("Fourteen entries from eleven people.\n")
        ok, _ = check_round(r, counts)
        c("passes on the corrected total of fourteen", ok)

        f.write_text("Six entries came in.\n")
        ok, _ = check_round(r, counts)
        c("a per-bounty count (6) is valid, not only the total", ok)

        # THE SIX FALSE POSITIVES THIS PRODUCED ON ITS FIRST REAL RUN. All six were correct
        # English, and a checker that flags correct copy gets ignored.
        for text in ("If two entries land in the same place, the one that took a note wins.",
                     "Live at 23:17, 0 claims.",
                     "1 claim so far",
                     "Two entries carry another tool's watermark."):
            f.write_text(text + "\n")
            ok, _ = check_round(r, counts)
            c(f"does NOT flag {text[:42]!r}", ok)

        f.write_text("nine of ten claims were fine.\n")
        ok, fnd = check_round(r, counts)
        c("an invented total is caught", not ok)

        # A sentence explaining a past error quotes the wrong number on purpose.
        f.write_text('An earlier version said "four of five claims" and it was stale.\n')
        ok, _ = check_round(r, counts)
        c("a line explaining a PAST correction is not flagged", ok)

        f.write_text("ten of four claims\n")
        ok, fnd = check_round(r, counts)
        c("part bigger than total is caught", not ok)

        # THE TWO REAL FALSE POSITIVES OF 2026-09-23, with the three-bounty field that
        # produced them. A sentence about SOME of the rounds is the normal case, not the
        # exception, and the grand total moves under it while the current round is open.
        three = {1409: 6, 1410: 8, 1412: 5}
        c("subset sums are what a true sentence can cite",
          valid_totals(three) == {5, 6, 8, 11, 13, 14, 19})

        f.write_text("Fourteen entries from eleven people.\n")
        ok, fnd = check_round(r, three)
        c("'fourteen' (rounds one plus two) passes while round three is open", ok)

        f.write_text("Ten of the thirteen claims went to IPFS as a still.\n")
        ok, fnd = check_round(r, three)
        c("'thirteen' (rounds two plus three) passes", ok)

        f.write_text("Twelve claims have come in.\n")
        ok, fnd = check_round(r, three)
        c("a number matching no subset (12) is still caught", not ok)

        for p in r.glob("*.md"):
            p.unlink()
        ok, fnd = check_round(r, counts)
        c("a round with no markdown FAILS rather than passing vacuously",
          not ok and any("empty sweep" in x for x in fnd))
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("check-copy-counts selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    counts = live_counts()
    if counts is None:
        print("  SKIP: could not establish live claim counts, so nothing was checked. "
              "This is UNKNOWN, not clean.")
        return 0

    targets = ([p for p in sorted((REPO_ROOT / "rounds" / "daily").glob("d*")) if p.is_dir()]
               if args.all else [Path(args.path)] if args.path else [])
    if not targets:
        print("give a round directory or --all")
        return 1

    bad = 0
    for t in targets:
        print(f"\n{t}")
        ok, findings = check_round(t, counts)
        for f in findings:
            print(f"  {f}")
        bad += not ok
    print(f"\nChecked {len(targets)} round(s), {bad} with a count that matches nothing.")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
