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

# Columns, in order. Split on the pipe rather than matching a shape.
#
# THE FIRST VERSION OF THIS WAS A REGEX AND IT FAILED SILENTLY. When the ladder gained a
# second ask per day, going from five columns to six, the non-greedy pattern backtracked and
# swallowed BOTH asks into one field - so the generated description read "Make one poster
# from the kit. Any style, must carry date and street | Caption it. One line that makes the
# poster work", pipe and all, and it passed every check. The row-count guard counted twelve
# rows and said fine, because it checked QUANTITY and the defect was SHAPE. That text was one
# paste away from an immutable on-chain description.
COLS = ["tag", "date", "ask_a", "ask_b", "format", "usd"]
TAG = re.compile(r"^T-\d+$")


def parse_ladder(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("| T-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != len(COLS):
            raise ValueError(
                f"ladder row has {len(cells)} columns, expected {len(COLS)}: {line[:70]}")
        r = dict(zip(COLS, cells))
        if not TAG.match(r["tag"]):
            continue
        wd, day, mon = r["date"].split()
        if mon not in MONTHS:
            continue
        for k in ("ask_a", "ask_b"):
            if "|" in r[k]:
                raise ValueError(f"{r['tag']} {k} contains a pipe: {r[k][:50]}")
        rows.append({"tag": r["tag"], "date": dt.date(2026, MONTHS[mon], int(day)),
                     "stated_weekday": wd, "ask_a": r["ask_a"], "ask_b": r["ask_b"],
                     "format": r["format"], "usd": int(r["usd"])})
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


def render(row: dict, template: str, eth_price: Decimal, slot: str = "a") -> str:
    """slot 'a' is the day's make, slot 'b' is the day's move. Two bounties, one day.

    THE PRIZE IS NOT RENDERED INTO THE DESCRIPTION, DELIBERATELY. It used to be, as
    {{PRIZE_ETH}} and {{PRIZE_USD}}. Kenny pointed out on 2026-09-20 that an OPEN bounty's
    pot grows the moment anyone contributes, so a number typed into the description is wrong
    from the first contribution onward - and the description is immutable, so it is wrong
    forever. The prize still goes in the poidh form's reward field, which renders it live,
    and `eth_for` below still computes it for that field and for the CLI summary."""
    days_out = (EVENT - row["date"]).days
    close = row["date"]
    return (template
            .replace("{{ASK}}", clean_ask(row["ask_a" if slot == "a" else "ask_b"]))
            .replace("{{DAYS_OUT}}", str(days_out))
            .replace("{{CLOSE_DAY}}", close.strftime("%A"))
            .replace("{{CLOSE_DATE}}", f"{close.strftime('%B')} {close.day}, {close.year}"))


# THE SHAPE EVERY DAY OF THE RUN HAS ALREADY PROMISED, IN TEXT THAT CANNOT BE EDITED.
#
# Bounty one (poidh 1409, cast 2026-09-20) says in its immutable description: "This is day one
# of thirteen, one bounty a day until ZAOstock itself. Same shape every day: opens, closes at
# 4pm Eastern, decided live at 5pm." That sentence is now a public commitment for days 2-13.
#
# The template it was generated from still said "Submissions close 11:59pm PT" and "Winner by
# contributor vote the following day" - a different deadline, a different time zone, and a vote
# length that is wrong on its face: poidh's open-bounty vote runs TWO days (read from the Base
# contract by the Zorca lane on 2026-09-21, and in our own runbook since R1). Day 2 would have
# cast contradicting day 1, and both would have been permanent.
#
# So every rendered day must carry these, or the generator refuses to write it.
RUN_SHAPE = {
    "Submissions close 4:00pm Eastern": "the 4pm Eastern close day one committed to",
    "live on stream at 5": "the 5pm live pick day one committed to",
    "two days to vote": "the real length of poidh's open-bounty vote",
}
RUN_SHAPE_FORBIDDEN = {
    "11:59pm PT": "the pre-run deadline, in the wrong time zone",
    "the following day": "a one-day vote, which poidh does not run",
}


def check_run_shape(body: str) -> list[str]:
    """What a rendered day is missing from, or contradicts in, the promised shape."""
    problems = [f"missing {why} ({needle!r})" for needle, why in RUN_SHAPE.items()
                if needle not in body]
    problems += [f"contradicts the run: {why} ({needle!r})"
                 for needle, why in RUN_SHAPE_FORBIDDEN.items() if needle in body]
    return problems


def _selftest() -> bool:
    passed = True

    def check(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    sample = ("| T-12 | Mon 21 Sep | **Make one poster.** Any style | **Caption it.** One line | photo | 3 |\n"
              "| T-1 | Fri 2 Oct | **\"I am going tomorrow.\"** Bring one | **Set-up shot.** Anything | clip/irl | 3 |\n")
    rows = parse_ladder(sample)
    check("parses both ladder rows", len(rows) == 2)
    check("reads the date, not the label", rows[0]["date"] == dt.date(2026, 9, 21))
    check("reads the prize from the table", rows[0]["usd"] == 3)
    check("crosses the month boundary", rows[1]["date"] == dt.date(2026, 10, 2))
    check("ladder weekdays agree with the calendar", check_weekdays(rows) == [])

    check("reads BOTH asks, not one merged field",
          rows[0]["ask_a"].startswith("**Make one poster") and rows[0]["ask_b"].startswith("**Caption"))

    wrong = parse_ladder("| T-12 | Tue 21 Sep | **x** y | **z** w | photo | 3 |\n")
    check("a WRONG weekday in the ladder is caught", len(check_weekdays(wrong)) == 1)

    # The defect this parser replaced: a five-column row silently merging two asks.
    try:
        parse_ladder("| T-12 | Mon 21 Sep | **only one ask** | photo | 3 |\n")
        merged = False
    except ValueError:
        merged = True
    check("a row with the WRONG COLUMN COUNT is refused, not guessed at", merged)
    try:
        parse_ladder("| T-12 | Mon 21 Sep | a | b " + chr(124) + " c | photo | 3 |\n")
        piped = False
    except ValueError:
        piped = True
    check("an ask containing a pipe is refused", piped)

    check("bold is stripped from the ask",
          clean_ask("**Make one poster.** Any style") == "Make one poster. Any style")
    check("prize converts without a float divide",
          eth_for(3, Decimal("2633.31")) == "0.0011")

    out = render(rows[0], "{{ASK}}|{{DAYS_OUT}}|{{CLOSE_DAY}}|{{CLOSE_DATE}}",
                 Decimal("2633.31"))
    # The prize must NOT reach the description. If someone re-adds the placeholder to the
    # template, it survives rendering as a literal - and this is what catches that.
    leaked = render(rows[0], "{{PRIZE_ETH}} ETH, about {{PRIZE_USD}}", Decimal("2633.31"))
    check("the prize is NOT rendered into the description",
          leaked == "{{PRIZE_ETH}} ETH, about {{PRIZE_USD}}")
    outb = render(rows[0], "{{ASK}}", Decimal("2633.31"), slot="b")
    check("slot b renders the day's SECOND ask", outb.strip() == "Caption it. One line")
    check("days-out is computed from the event", "|12|" in out)
    check("close weekday is computed, never typed", "Monday" in out)
    check("close date is spelled out", "September 21, 2026" in out)
    check("no placeholder survives rendering", "{{" not in out)

    # The 2026-09-21 defect: the template promised a different shape than day one had.
    stale = ("Submissions close 11:59pm PT, Monday September 21, 2026.\n"
             "Winner by contributor vote the following day.\n")
    probs = check_run_shape(stale)
    check("the OLD template's deadline is refused",
          any("11:59pm PT" in p for p in probs))
    check("a one-day vote is refused", any("the following day" in p for p in probs))
    check("a missing 4pm close is reported", any("4pm Eastern close" in p for p in probs))
    good = ("Zaal names his pick live on stream at 5pm Eastern. Everyone who added to the pot "
            "then has two days to vote on the pick.\n"
            "Submissions close 4:00pm Eastern, Monday September 21, 2026.\n")
    check("a day carrying the promised shape passes", check_run_shape(good) == [])
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

    # Check the TEMPLATE once, before rendering anything, so a drifted template fails loudly
    # rather than producing 24 files that each have to be caught on their own.
    probs = check_run_shape(template)
    if probs:
        print("Refusing: the template does not match the shape bounty one already promised for "
              "all thirteen days, in text that cannot be edited.")
        for p in probs:
            print("  " + p)
        return 1

    price = Decimal(args.eth_price)
    targets = rows if args.all else [r for r in rows if r["tag"] == args.day]
    if not targets:
        print(f"No ladder row for {args.day!r}. Tags: {', '.join(r['tag'] for r in rows)}")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for r in targets:
        for slot in ("a", "b"):
            body = render(r, template, price, slot)
            path = OUT_DIR / f"{r['tag'].lower()}-{r['date'].isoformat()}-{slot}.md"
            path.write_text(body)
            written += 1
            print(f"  {r['tag']:<5}{slot}  {r['date']} {r['date'].strftime('%a')}  ${r['usd']}  "
                  f"{clean_ask(r['ask_a' if slot == 'a' else 'ask_b'])[:42]}")
    print(f"\nWrote {written} file(s) to {OUT_DIR.relative_to(REPO_ROOT)}")
    print("Each one still has to pass validate-bounty-description.py before it is cast.")
    print(f"ETH price used: ${price}. Re-measure before casting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
