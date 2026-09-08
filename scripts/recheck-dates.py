#!/usr/bin/env python3
"""
Which time-bound claims in this repo have gone unverified? Repo-wide, on cron.

The estate hit this five separate times in one day: a programme recorded as live that had
gone inactive, an application drafted against an old cycle, a VPS recorded as down opening
a file 16 days after it came back, doc summaries contradicting their own updated bodies,
and superseded clipboard pages with nothing marking them. Every one was a record that
stayed loud after it stopped being true.

The rule that came out of it is that anything time-bound carries a re-check date written
next to the claim. That rule is only worth having if something reads the dates - otherwise
it is a comment nobody revisits, which is the same defect one level up.

    python3 scripts/recheck-dates.py            # every re-check date, flag the passed ones
    python3 scripts/recheck-dates.py --days 3   # also warn on ones expiring soon
    python3 scripts/recheck-dates.py --selftest

Exit 1 if any date has passed, so a cron step goes loud. It does NOT re-verify anything -
it cannot know whether a figure is still right. It tells you which claims are now
unverified, which is a different and honest thing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_PARTS = {".git", "node_modules", ".handoffs", "data"}

# "re-check by 2026-10-08", "RE-CHECK BY 2026-09-13", "Re-check the figures on this page
# by 2026-10-08". Deliberately loose on what sits between the verb and the date, because
# the phrasing that reads naturally next to a claim varies and a rule people cannot write
# naturally is a rule they stop writing.
RECHECK_RE = re.compile(
    r"re-?check(?:ed)?\b[^\n.]{0,60}?\bby\s+(\d{4}-\d{2}-\d{2})", re.I)


def find_dates(root: Path) -> list[tuple[Path, int, dt.date, str]]:
    out = []
    for p in sorted(root.rglob("*.md")):
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        try:
            lines = p.read_text().splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            for m in RECHECK_RE.finditer(line):
                try:
                    d = dt.date.fromisoformat(m.group(1))
                except ValueError:
                    continue
                out.append((p, i, d, line.strip()[:96]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=0,
                    help="also warn on dates falling within this many days")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        print("recheck-dates selftest")
        passed = True

        def check(label: str, cond: bool) -> None:
            nonlocal passed
            print(f"  {'ok  ' if cond else 'FAIL'} {label}")
            passed = passed and cond

        f = RECHECK_RE.findall
        check("plain form", f("Re-check by 2026-09-09.") == ["2026-09-09"])
        check("shouted form", f("RE-CHECK BY 2026-09-13 and before any cast") == ["2026-09-13"])
        check("words between verb and date",
              f("Re-check the figures on this page by 2026-10-08.") == ["2026-10-08"])
        check("hyphenless spelling", f("recheck by 2026-01-01") == ["2026-01-01"])
        check("ignores a date with no re-check verb", f("Measured 2026-09-07.") == [])
        check("does not run across a sentence boundary",
              f("Re-check this. Something unrelated by 2026-09-09.") == [])
        check("finds the repo's real dates", len(find_dates(REPO_ROOT)) >= 3)
        print("selftest:", "passed" if passed else "FAILED")
        return 0 if passed else 1

    today = dt.date.today()
    rows = find_dates(REPO_ROOT)
    if not rows:
        print("No re-check dates found. Anything time-bound should carry one.")
        return 0

    passed_rows = [r for r in rows if r[2] < today]
    soon = [r for r in rows if today <= r[2] <= today + dt.timedelta(days=a.days)] if a.days else []
    fine = [r for r in rows if r not in passed_rows and r not in soon]

    print(f"Re-check sweep - {len(rows)} time-bound claim(s), today is {today}\n")
    for p, ln, d, text in passed_rows:
        print(f"  PASSED   {p.relative_to(REPO_ROOT)}:{ln}  due {d} "
              f"({(today - d).days}d ago)")
        print(f"           {text}")
    for p, ln, d, text in soon:
        print(f"  SOON     {p.relative_to(REPO_ROOT)}:{ln}  due {d} "
              f"(in {(d - today).days}d)")
    for p, ln, d, _ in fine:
        print(f"  ok       {p.relative_to(REPO_ROOT)}:{ln}  due {d}")

    print()
    if passed_rows:
        print(f"{len(passed_rows)} claim(s) are now UNVERIFIED. That is not the same as wrong - "
              f"re-measure,")
        print("then move the date. Correct it at the top of the file, where it is read.")
        return 1
    print("Nothing has gone unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
