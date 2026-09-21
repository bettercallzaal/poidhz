#!/usr/bin/env python3
"""Generate one day's ZAOstock bounty from the ladder, ready to paste.

WHY THIS EXISTS. The twelve-day ladder in `rounds/daily/ZAOSTOCK-12.md` is 24 bounties at
two a day. Hand-writing 24 descriptions is how a ladder stops on T-7, and a ladder that
stops reads as abandonment to everyone who entered the day before. The operational risk was
always bigger than the money: the spec says the real dependency is "who casts it at the same
time every day, and what happens on the day nobody does". This is the half of that answer a
script can hold.

WHAT IT GUARANTEES, because these are the things that go wrong by hand:

  - the weekday matches the date. Writing R9 by hand I typed "Monday September 29" and
    "Wednesday October 1"; they are a Tuesday and a Thursday. A poidh description is
    immutable once cast, so a wrong weekday is permanent.
  - the days-out count is computed from the event, never typed.
  - the prize is read from the ladder table rather than remembered.
  - every generated file still has to pass validate-bounty-description.py before it is cast.

IT READS THE LADDER AS THE SOURCE OF TRUTH. Editing the markdown table changes what this
generates. Two copies of a schedule is one more than can stay true.

    python3 scripts/build-daily-bounty.py --day T-12
    python3 scripts/build-daily-bounty.py --all        # writes all twelve
    python3 scripts/build-daily-bounty.py --selftest
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LADDER = REPO_ROOT / "rounds" / "daily" / "ZAOSTOCK-12.md"
TEMPLATE = REPO_ROOT / "rounds" / "daily" / "_template" / "description.md"
OUT_DIR = REPO_ROOT / "rounds" / "daily" / "generated"

EVENT = dt.date(2026, 10, 3)
MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
          "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

# The ladder rows look like:
# | T-12 | Mon 21 Sep | **Make one poster...** rest | photo | 3 |
ROW = re.compile(
    r"^\|\s*(T-\d+)\s*\|\s*(\w{3})\s+(\d{1,2})\s+(\w{3})\s*\|\s*(.+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*$",
    re.M)


def parse_ladder(text: str) -> list[dict]:
    rows = []
    for m in ROW.finditer(text):
        tag, wd, day, mon, ask, fmt, usd = m.groups()
        if mon not in MONTHS:
            continue
        date = dt.date(2026, MONTHS[mon], int(day))
        rows.append({"tag": tag, "date": date, "stated_weekday": wd,
                     "ask": ask, "format": fmt.strip(), "usd": int(usd)})
    return rows


def check_weekdays(rows: list[dict]) -> list[str]:
    """The ladder's own weekday labels, against the calendar. A wrong one here would be
    copied into an immutable description."""
    return [f"{r['tag']}: ladder says {r['stated_weekday']}, {r['date']} is "
            f"{r['date'].strftime('%a')}"
            for r in rows if r["date"].strftime("%a") != r["stated_weekday"]]


def clean_ask(ask: str) -> str:
    """Markdown bold out, sentence in. The ladder writes the headline in ** **."""
    return re.sub(r"\*\*(.+?)\*\*", r"\1", ask).strip()


def eth_for(usd: int, eth_price: Decimal) -> str:
    """Prize in ETH at a stated price. Never a float divide - this repo has published a
    float-rounded wei figure once already."""
    return str((Decimal(usd) / eth_price).quantize(Decimal("0.0001")))


def render(row: dict, template: str, eth_price: Decimal) -> str:
    days_out = (EVENT - row["date"]).days
    close = row["date"]
    return (template
            .replace("{{ASK}}", clean_ask(row["ask"]))
            .replace("{{DAYS_OUT}}", str(days_out))
            .replace("{{PRIZE_ETH}}", eth_for(row["usd"], eth_price))
            .replace("{{PRIZE_USD}}", f"{row['usd']} dollars")
            .replace("{{CLOSE_DAY}}", close.strftime("%A"))
            .replace("{{CLOSE_DATE}}", f"{close.strftime('%B')} {close.day}, {close.year}"))


def _selftest() -> bool:
    passed = True

    def check(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    sample = ("| T-12 | Mon 21 Sep | **Make one poster from the kit.** Any style | photo | 3 |\n"
              "| T-1 | Fri 2 Oct | **\"I am going tomorrow.\"** Bring one person | clip/irl | 3 |\n")
    rows = parse_ladder(sample)
    check("parses both ladder rows", len(rows) == 2)
    check("reads the date, not the label", rows[0]["date"] == dt.date(2026, 9, 21))
    check("reads the prize from the table", rows[0]["usd"] == 3)
    check("crosses the month boundary", rows[1]["date"] == dt.date(2026, 10, 2))
    check("ladder weekdays agree with the calendar", check_weekdays(rows) == [])

    wrong = parse_ladder("| T-12 | Tue 21 Sep | **x** y | photo | 3 |\n")
    check("a WRONG weekday in the ladder is caught", len(check_weekdays(wrong)) == 1)

    check("bold is stripped from the ask",
          clean_ask("**Make one poster.** Any style") == "Make one poster. Any style")
    check("prize converts without a float divide",
          eth_for(3, Decimal("2633.31")) == "0.0011")

    out = render(rows[0], "{{ASK}}|{{DAYS_OUT}}|{{CLOSE_DAY}}|{{CLOSE_DATE}}|{{PRIZE_USD}}",
                 Decimal("2633.31"))
    check("days-out is computed from the event", "|12|" in out)
    check("close weekday is computed, never typed", "Monday" in out)
    check("close date is spelled out", "September 21, 2026" in out)
    check("no placeholder survives rendering", "{{" not in out)
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--day", help="ladder tag, e.g. T-12")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--eth-price", default="2633.31",
                    help="USD per ETH; re-measure before casting, do not trust the default")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("build-daily-bounty selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    if not LADDER.exists() or not TEMPLATE.exists():
        print(f"Refusing: missing {LADDER if not LADDER.exists() else TEMPLATE}")
        return 1

    rows = parse_ladder(LADDER.read_text())
    if len(rows) < 10:
        print(f"Refusing: parsed only {len(rows)} ladder rows. The table shape changed, or "
              f"the regex no longer matches it. A partial ladder is worse than none.")
        return 1

    bad = check_weekdays(rows)
    if bad:
        print("Refusing: the ladder's own weekdays do not match the calendar.")
        for b in bad:
            print("  " + b)
        print("A poidh description is immutable once cast. Fix the ladder first.")
        return 1

    template = TEMPLATE.read_text()
    price = Decimal(args.eth_price)
    targets = rows if args.all else [r for r in rows if r["tag"] == args.day]
    if not targets:
        print(f"No ladder row for {args.day!r}. Tags: {', '.join(r['tag'] for r in rows)}")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for r in targets:
        body = render(r, template, price)
        path = OUT_DIR / f"{r['tag'].lower()}-{r['date'].isoformat()}.md"
        path.write_text(body)
        print(f"  {r['tag']:<5} {r['date']} {r['date'].strftime('%a')}  ${r['usd']}  "
              f"{clean_ask(r['ask'])[:44]}")
    print(f"\nWrote {len(targets)} file(s) to {OUT_DIR.relative_to(REPO_ROOT)}")
    print("Each one still has to pass validate-bounty-description.py before it is cast.")
    print(f"ETH price used: ${price}. Re-measure before casting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
