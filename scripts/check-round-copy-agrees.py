#!/usr/bin/env python3
"""Refuse a round whose announcement copy states a different deadline than the bounty.

WHY THIS EXISTS, MEASURED. On 2026-09-20 bounty one's close was moved from 6pm Eastern to
4pm, because Zaal picks the winner live on stream at 5pm and a bounty that closes after its
own decision is decided on an incomplete field. The description was retimed in commit
b570446. `rounds/daily/d01/DISTRIBUTION.md` was not, and **six separate announcement blocks
still said 6pm** - the /poidh cast, the reply to past submitters, the Maine-local post, the X
post, the top-up post and the two-hours-before reminder. It was caught by reading the files
before casting, not by any check.

WHY IT IS THE WORST VERSION OF THIS BUG. A poidh description is IMMUTABLE once cast. The
announcement is not. So when they disagree, only the announcement can be corrected - and by
then every person who read it has been told a deadline two hours after the bounty actually
closed. They submit late, to a closed bounty, and we look like we moved the goalposts.

WHY A SCRIPT AND NOT A NOTE. This is the defect family this repo keeps hitting: a number
separated from the thing that makes it true. The estate measures honor-system rules at 3-40%
compliance and enforced ones at ~100%. Thirteen days of this run each get their own copy.

    python3 scripts/check-round-copy-agrees.py rounds/daily/d01
    python3 scripts/check-round-copy-agrees.py --all
    python3 scripts/check-round-copy-agrees.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PASTE_START = "<!-- PASTE BELOW THIS LINE -->"
PASTE_END = "<!-- PASTE ABOVE THIS LINE -->"

# A clock time with a meridiem: "4pm", "4:00pm", "11:59 PM". The meridiem is required, so a
# bare "13 days out" or a date is never mistaken for a deadline.
CLOCK = re.compile(r"(?i)\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b")


def paste_body(text: str) -> str:
    """The text that actually gets cast, when the file marks it; the whole file otherwise."""
    if PASTE_START in text and PASTE_END in text:
        return text.split(PASTE_START, 1)[1].split(PASTE_END, 1)[0].strip() + "\n"
    return text


def times_in(text: str) -> set[str]:
    """Normalised clock times, so 4pm and 4:00pm are the same time and not two."""
    out = set()
    for h, m, ap in CLOCK.findall(text):
        out.add(f"{int(h)}:{m or '00'}{ap.lower()}")
    return out


def check_round(round_dir: Path) -> tuple[bool, list[str]]:
    """The deadline the description commits to must appear in every copy file.

    The copy may name OTHER times as well - "picked live at 5", "post the reminder at 2pm" -
    so this does not demand the sets match. It demands the committed deadline is IN the copy,
    which is the direction that can mislead an entrant."""
    findings = []
    desc = round_dir / "description.md"
    if not desc.exists():
        return False, [f"FAIL: {round_dir} has no description.md"]

    body = paste_body(desc.read_text())
    m = re.search(r"(?im)^\s*Submissions close\s+(.+?)[,.]", body)
    if not m:
        return False, [f"FAIL: {desc} - no 'Submissions close ...' line in the cast text, so "
                       f"there is no deadline to check the copy against"]
    deadline_line = m.group(1).strip()
    committed = times_in(deadline_line)
    if not committed:
        return False, [f"FAIL: {desc} - 'Submissions close {deadline_line}' names no clock time"]
    findings.append(f"     description commits to: {sorted(committed)} ({deadline_line})")

    copy_files = sorted(p for p in round_dir.glob("*.md")
                        if p.name not in {"description.md", "README.md"})
    if not copy_files:
        # An empty set is not a pass. Say so rather than printing a clean bill of health.
        return False, findings + [
            f"FAIL: {round_dir} has no announcement copy to check (only description.md and "
            f"README.md). If this round genuinely has no copy, that is the finding."]

    ok = True
    for cf in copy_files:
        found = times_in(cf.read_text())
        if committed & found:
            findings.append(f"PASS: {cf.name} states the committed deadline")
        else:
            ok = False
            findings.append(
                f"FAIL: {cf.name} never states the committed deadline {sorted(committed)}. "
                f"It says {sorted(found) or 'no time at all'}. The description is IMMUTABLE "
                f"once cast - fix the copy, not the bounty.")
    return ok, findings


def _selftest() -> bool:
    import tempfile
    passed = True

    def check(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    check("4pm and 4:00pm are the same time", times_in("4pm") == times_in("4:00pm"))
    check("a meridiem is required", times_in("13 days out, October 3, 2026") == set())
    check("two different times are two", len(times_in("closes 4pm, picked at 5pm")) == 2)

    with tempfile.TemporaryDirectory() as d:
        r = Path(d) / "d01"
        r.mkdir()
        desc = (f"header noise, closes 9pm maybe\n{PASTE_START}\n"
                f"DEADLINE\n\nSubmissions close 4:00pm Eastern, Monday September 21, 2026.\n"
                f"Winner picked live on stream at 5:00pm Eastern the same day.\n{PASTE_END}\n")
        r.joinpath("description.md").write_text(desc)

        # The real 2026-09-20 defect: copy left on the old time.
        r.joinpath("DISTRIBUTION.md").write_text("Closes 6pm Eastern Monday. <BOUNTY-URL>\n")
        ok, f = check_round(r)
        check("catches copy left on the OLD deadline", not ok and any("never states" in x for x in f))

        r.joinpath("DISTRIBUTION.md").write_text(
            "Closes 4pm Eastern Monday, picked live at 5. <BOUNTY-URL>\n")
        ok, _ = check_round(r)
        check("passes when the copy agrees", ok)

        # The header above the sentinels must not be read as the deadline.
        r.joinpath("DISTRIBUTION.md").write_text("Closes 9pm.\n")
        ok, _ = check_round(r)
        check("the operator header's time is NOT treated as the deadline", not ok)

        r.joinpath("DISTRIBUTION.md").unlink()
        ok, f = check_round(r)
        check("a round with NO copy fails rather than passing vacuously",
              not ok and any("no announcement copy" in x for x in f))

        r.joinpath("description.md").write_text(f"{PASTE_START}\nno deadline here\n{PASTE_END}\n")
        r.joinpath("DISTRIBUTION.md").write_text("Closes 4pm.\n")
        ok, f = check_round(r)
        check("a description with no close line fails, it does not silently pass",
              not ok and any("no 'Submissions close" in x for x in f))
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("round_dir", nargs="?", help="e.g. rounds/daily/d01")
    ap.add_argument("--all", action="store_true", help="every round dir that has a description")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("check-round-copy-agrees selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    if args.all:
        targets = sorted(p.parent for p in (REPO_ROOT / "rounds").glob("*/description.md"))
        targets += sorted(p.parent for p in (REPO_ROOT / "rounds").glob("*/*/description.md"))
        if not targets:
            print("Refusing: found no round directories. The layout changed, or the glob is "
                  "wrong. An empty set is not a pass.")
            return 1
    elif args.round_dir:
        targets = [Path(args.round_dir) if Path(args.round_dir).is_absolute()
                   else REPO_ROOT / args.round_dir]
    else:
        ap.error("give a round directory, or --all, or --selftest")

    worst = 0
    for t in targets:
        ok, findings = check_round(t)
        print(f"\n{t.relative_to(REPO_ROOT) if t.is_relative_to(REPO_ROOT) else t}")
        for f in findings:
            print(f"  {f}")
        if not ok:
            worst = 1
    print(f"\nChecked {len(targets)} round(s).",
          "All copy agrees with its bounty." if worst == 0 else "FIX THE COPY BEFORE POSTING.")
    return worst


if __name__ == "__main__":
    sys.exit(main())
