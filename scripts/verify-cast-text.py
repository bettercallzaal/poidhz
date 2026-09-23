#!/usr/bin/env python3
"""Prove that what this repo says was cast IS what is cast, by diffing against the chain.

WHY. A poidh description is immutable, and this repo's round files claim to hold the text
"as cast" - `rounds/daily/d03/description.md` even states a character count. Those claims are
load-bearing: the announcement copy quotes the bounty, other seats quote our copy, and every
promise audit reads the description to decide what was promised. **Nothing checked them.**

The claim is checkable and it was being made by hand. On 2026-09-23 a header line in d03 said
the winner would be "named live on Twitch" while the cast body said the opposite in the same
file. Nothing public was wrong that time. The next time it might be the paste body itself, and
a wrong paste body means we announce a promise nobody made or miss one we did.

Two ways a repo file drifts from a cast bounty, and this catches both:

  - somebody edits the paste body after casting, to tidy it. The bounty cannot change, so the
    file is now lying about what people agreed to.
  - somebody casts a different draft than the one in the file, and the file keeps the draft.

WHAT IT DOES NOT DO. It does not tell you the description is GOOD. `validate-bounty-description`
and `check-render-safe` do that before a cast. This runs after, and only answers "is the thing
we wrote down the thing that is on chain".

THE MARKER PAIR IS PART OF THE FILE, NOT THE CAST TEXT. Round files wrap the paste body in
`<!-- PASTE BELOW THIS LINE -->` and `<!-- PASTE ABOVE THIS LINE -->`. Forgetting to strip the
closing one is a 31-character difference that looks like real drift; it cost a confusing
measurement the day this was written.

    python3 scripts/verify-cast-text.py --round rounds/daily/d03 --bounty 1412
    python3 scripts/verify-cast-text.py --all
    python3 scripts/verify-cast-text.py --selftest
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

OPEN_MARKER = "<!-- PASTE BELOW THIS LINE -->"
CLOSE_MARKER = "<!-- PASTE ABOVE THIS LINE -->"


def paste_body(text: str) -> str | None:
    """The cast text a round file holds, or None when the file has no paste block.

    None and "" are different answers and the caller must not conflate them: no marker means
    this file does not claim to hold cast text, and an empty block means it claims to and the
    claim is empty, which is a failure.
    """
    if OPEN_MARKER not in text:
        return None
    body = text.split(OPEN_MARKER, 1)[1]
    if CLOSE_MARKER in body:
        body = body.split(CLOSE_MARKER, 1)[0]
    return body.strip()


def live_description(bounty_id: int) -> str | None:
    """The description poidh actually serves for this bounty, or None if it cannot be read.

    None on failure, never "" - an empty string would compare as total drift and turn a
    network blip into a false alarm about immutable text.
    """
    url = f"https://poidh.xyz/base/bounty/{bounty_id}/data"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
        payload = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
    except Exception:
        return None
    for pat in (r'\\"description\\":\\"(.*?)\\",\\"amount\\"',
                r'"description":"(.*?)","amount"'):
        m = re.search(pat, payload, re.S)
        if m:
            try:
                return m.group(1).encode().decode("unicode_escape")
            except Exception:
                return m.group(1)
    return None


def compare(round_dir: Path, bounty_id: int) -> tuple[bool, list[str]]:
    out = []
    f = round_dir / "description.md"
    if not f.exists():
        return False, [f"FAIL: {f} does not exist. A round with no description file cannot "
                       f"have its cast text verified, and that is not a pass."]

    local = paste_body(f.read_text())
    if local is None:
        return True, [f"     SKIP {round_dir.name}: no paste markers, so this file makes no "
                      f"claim about cast text"]
    if not local:
        return False, [f"FAIL: {f} has paste markers with nothing between them."]

    live = live_description(bounty_id)
    if live is None:
        return False, [f"     UNKNOWN {round_dir.name}: could not read bounty {bounty_id}'s "
                       f"live description. Nothing was compared. This is UNKNOWN, not a pass."]

    if live.strip() == local:
        out.append(f"  PASS: {round_dir.name} matches bounty {bounty_id} on chain, "
                   f"{len(local):,} characters")
        return True, out

    a, b = live.strip().splitlines(), local.splitlines()
    out.append(f"FAIL: {round_dir.name} DIFFERS from bounty {bounty_id}. "
               f"live {len(live.strip()):,} chars / {len(a)} lines, "
               f"file {len(local):,} chars / {len(b)} lines. "
               f"**The bounty cannot change, so the file is what is wrong.**")
    for line in list(difflib.unified_diff(a, b, "on-chain", "repo", lineterm=""))[:24]:
        out.append(f"       {line[:160]}")
    return False, out


def cast_rounds() -> list[tuple[Path, int]]:
    cfg = json.loads((REPO_ROOT / "org.config.json").read_text())
    found = []
    for r in cfg.get("rounds", []):
        bid = r.get("bounty_id")
        folder = r.get("folder")
        if not bid:
            continue
        d = REPO_ROOT / folder if folder else REPO_ROOT / "rounds" / f"r{r.get('round')}"
        if d.is_dir():
            found.append((d, int(bid)))
    return found


def _selftest() -> bool:
    passed = True

    def c(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    body = "ANYTHING BUT A POSTER.\n\nSecond line."
    c("extracts the body between the markers",
      paste_body(f"notes\n{OPEN_MARKER}\n{body}\n{CLOSE_MARKER}\n") == body)
    c("the CLOSING marker is stripped - forgetting it is a 31-char phantom diff",
      CLOSE_MARKER not in (paste_body(f"x\n{OPEN_MARKER}\n{body}\n{CLOSE_MARKER}") or ""))
    c("a file with no markers returns None, not empty string",
      paste_body("just notes, no paste block") is None)
    c("None and empty are distinguishable",
      paste_body("no markers") is None
      and paste_body(f"{OPEN_MARKER}\n\n{CLOSE_MARKER}") == "")

    import tempfile
    with tempfile.TemporaryDirectory() as d:
        r = Path(d) / "d99"
        r.mkdir()

        ok, out = compare(r, 1412)
        c("a round with NO description.md fails rather than passing vacuously",
          not ok and any("does not exist" in x for x in out))

        (r / "description.md").write_text(f"notes\n{OPEN_MARKER}\n\n{CLOSE_MARKER}\n")
        ok, out = compare(r, 1412)
        c("empty markers fail", not ok and any("nothing between them" in x for x in out))

        (r / "description.md").write_text("a file that makes no claim")
        ok, out = compare(r, 1412)
        c("no markers is a SKIP and a pass, because it claims nothing",
          ok and any("SKIP" in x for x in out))

    # The network half, against the real bounty this was written for.
    live = live_description(1412)
    if live is None:
        print("  ---- could not reach poidh; the on-chain half of the selftest did not run")
        print("       That is UNKNOWN, not a pass, and it is why this line prints.")
    else:
        c("reads bounty 1412's real description", len(live) > 5000)
        c("a control bounty's description DIFFERS from 1412's",
          (live_description(1410) or "") != live)
        real = REPO_ROOT / "rounds" / "daily" / "d03"
        if real.is_dir():
            ok, out = compare(real, 1412)
            c("the real d03 file matches the real bounty", ok)
            ok2, _ = compare(real, 1410)
            c("comparing d03 against the WRONG bounty fails, so it is really comparing",
              not ok2)
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--round")
    ap.add_argument("--bounty", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("verify-cast-text selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    if args.all:
        targets = cast_rounds()
        if not targets:
            print("FAIL: no cast rounds found in org.config.json. An empty sweep is not a "
                  "clean result.")
            return 1
    elif args.round and args.bounty:
        targets = [(Path(args.round), args.bounty)]
    else:
        ap.error("give --round and --bounty, or --all")

    bad = 0
    for d, bid in targets:
        ok, out = compare(d, bid)
        for line in out:
            print(line)
        bad += not ok
    print(f"\nChecked {len(targets)} cast round(s), {bad} that do not match the chain.")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
