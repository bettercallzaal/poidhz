"""Shared free-text deadline parser for poidh bounty descriptions.

poidh has a structured `deadline` field that, in practice, nobody sets (0 of
94 open bounties on 2026-08-20). The only place a deadline exists is the
description text, written by hand in whatever shape the issuer felt like.
This module turns that text into an ISO date, or returns None.

Rule: a date only counts as a deadline when it sits within ~300 chars AFTER
a deadline-signalling keyword (deadline / closes / due / ends / through /
until / ...). Grabbing any date anywhere produced false positives (an event
kickoff date reported as the deadline). No keyword, no deadline.

Shapes handled (all seen live on poidh.xyz):
  August 24, 2026            Aug 24, 2026          Sunday, August 30 at 11:59 PM PT
  5 September, 23:59 UTC     20th August, 2026     July 31rst, 2026
  Deadline August 31         2026-02-09T18:49:04Z  2026-08-30
Missing year -> inferred from the bounty's creation date: the first occurrence
of that month/day on or after creation (a January deadline on a December
bounty rolls into the next year).

Usage:
    from deadline_parser import extract_deadline
    iso, raw = extract_deadline(description, created_at=epoch_seconds_or_None)
Run the self-test:  python3 scripts/deadline_parser.py --selftest
"""
from __future__ import annotations

import re
import sys
from datetime import date, datetime, timezone

_MONTH_NAMES = [
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
]
_MONTH_LOOKUP = {m: i + 1 for i, m in enumerate(_MONTH_NAMES)}
_MONTH_LOOKUP.update({m[:3]: i + 1 for i, m in enumerate(_MONTH_NAMES)})
_MONTH_LOOKUP["sept"] = 9

_MONTH = r"(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?"
_DAY = r"(?P<day>\d{1,2})(?:st|nd|rd|th|rst)?"
_YEAR = r"(?:,?\s*(?P<year>20\d{2}))?"

# Month-first: "August 31", "Aug 31, 2026", "Sunday, August 30 at ..."
_MDY_RE = re.compile(rf"\b{_MONTH}\s+{_DAY}\b{_YEAR}", re.IGNORECASE)
# Day-first: "5 September", "20th August, 2026", "31rst July 2026"
_DMY_RE = re.compile(rf"\b{_DAY}\s+(?:of\s+)?{_MONTH}\b{_YEAR}", re.IGNORECASE)
# ISO: 2026-02-09 or 2026-02-09T18:49:04.000Z
_ISO_RE = re.compile(r"\b(?P<year>20\d{2})-(?P<mon>0[1-9]|1[0-2])-(?P<day>0[1-9]|[12]\d|3[01])(?!\d)")

DEADLINE_RE = re.compile(
    r"\b(?:deadline|closes?|closing|due|ends?|ending|submit\s+by|until|through|before|expires?|cutoff|cut-off|last\s+day)\b",
    re.IGNORECASE,
)

_WINDOW = 300


def _infer_year(month: int, day: int, created: date | None) -> int:
    base = created or datetime.now(timezone.utc).date()
    try:
        candidate = date(base.year, month, day)
    except ValueError:
        return base.year
    return base.year if candidate >= base else base.year + 1


def _to_date(year: int, month: int, day: int) -> str | None:
    try:
        return date(year, month, day).isoformat()
    except ValueError:
        return None


def _first_date_in(text: str, created: date | None) -> tuple[str | None, str | None]:
    """Return the earliest-positioned date expression in `text` as (iso, raw)."""
    candidates: list[tuple[int, str | None, str]] = []
    for m in _ISO_RE.finditer(text):
        candidates.append((m.start(), _to_date(int(m["year"]), int(m["mon"]), int(m["day"])), m.group(0)))
    for rx in (_MDY_RE, _DMY_RE):
        for m in rx.finditer(text):
            month = _MONTH_LOOKUP.get(m["month"].lower().rstrip("."))
            if not month:
                continue
            day = int(m["day"])
            if not 1 <= day <= 31:
                continue
            year = int(m["year"]) if m["year"] else _infer_year(month, day, created)
            candidates.append((m.start(), _to_date(year, month, day), m.group(0)))
    candidates = [c for c in candidates if c[1]]
    if not candidates:
        return None, None
    candidates.sort(key=lambda c: c[0])
    _, iso, raw = candidates[0]
    return iso, raw


def extract_deadline(description: str, created_at: int | float | None = None) -> tuple[str | None, str | None]:
    """Return (iso_date, raw_text) for the stated deadline, or (None, None).

    created_at: unix seconds the bounty was created, used only to infer a
    missing year. None -> today's year.
    """
    if not description:
        return None, None
    created = None
    if created_at:
        try:
            created = datetime.fromtimestamp(float(created_at), tz=timezone.utc).date()
        except (ValueError, OSError, OverflowError):
            created = None
    for hit in DEADLINE_RE.finditer(description):
        iso, raw = _first_date_in(description[hit.start(): hit.start() + _WINDOW], created)
        if iso:
            return iso, raw
    return None, None


def selftest() -> int:
    created = datetime(2026, 8, 10, tzinfo=timezone.utc).timestamp()
    cases = [
        # original guards
        ("Build a game. Event kickoff on August 5, 2026. No deadline stated.", None),
        ("Submissions close on July 5, 2026. Prizes paid after.", "2026-07-05"),
        ("Deadline: submissions due August 12, 2026.", "2026-08-12"),
        ("This bounty ends September 1, 2026 at midnight.", "2026-09-01"),
        ("Submit by October 3, 2026 to qualify.", "2026-10-03"),
        ("Prize pool. Judging happens live, winners announced later.", None),
        ("Launched June 2024, still open.", None),
        # shapes that were missed live on 2026-08-20
        ("Pure randomness.  Deadline: 5 September, 23:59 UTC", "2026-09-05"),
        ("## Rules  - **Claim deadline:** Sunday, August 30 at 11:59 PM PT", "2026-08-30"),
        ("Deadline is July 31rst, 2026", "2026-07-31"),
        ("The bounty is open through August 31, 2026 to test the timing.", "2026-08-31"),
        ("Deadline August 31", "2026-08-31"),
        ("Deadline: 20th August, 2026.", "2026-08-20"),
        ("Mode: First Valid Submission Wins. Deadline: 2026-02-09T18:49:04.000Z", "2026-02-09"),
        ("Submissions close on Sept 14", "2026-09-14"),
        ("closes Aug. 29th", "2026-08-29"),
        # year rollover: created Aug 2026, deadline "January 3" -> 2027
        ("Ends January 3.", "2027-01-03"),
        # keyword present but no parseable date
        ("Deadline: [2-3 weeks from posting]", None),
        ("The residue ends up in the produce aisle on the 5th floor.", None),
    ]
    fails = 0
    for desc, want in cases:
        got, _ = extract_deadline(desc, created_at=created)
        ok = got == want
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} want={want!r:>14} got={got!r:>14}  <- {desc[:60]}")
    print(f"selftest: {len(cases) - fails}/{len(cases)} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
