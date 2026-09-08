#!/usr/bin/env python3
"""
Pre-cast readiness check for a bounty round. Run this before funding or casting.

Why this exists: R6's pre-cast audit on 2026-09-06 was done by hand and found that
the issuer wallet held 0.002154 ETH against a 0.0128 ETH round - a hard blocker that
nobody had checked, because checking it was nobody's job and lived in no script. It
also found that R5's stated deadline and its on-chain deadline were six days apart,
and that R5 had never been added to org.config.json's default_bounty_ids, so its nine
claims scored zero on the leaderboard. All three are the same class of failure: a
precondition everyone assumed and no tool measured.

Checks, in the order they matter:

  1. WALLET      - can the issuer EOA actually fund this round (prize + gas headroom)?
  2. DEADLINE    - does the date written in description.md still leave a sane window,
                   given you are casting today?
  3. CONFIG      - is the previous round wired into org.config.json, so its entrants
                   are actually scored?
  4. DESCRIPTION - does it pass validate-bounty-description.py, and is it free of
                   unfilled <PLACEHOLDER> markers?
  5. DATA        - is the committed dashboard data fresh enough to trust?

    python3 scripts/precast-check.py --round 6 --prize 0.0128
    python3 scripts/precast-check.py --round 6 --prize 0.0128 --cast-date 2026-09-11
    python3 scripts/precast-check.py --selftest        # no network

Exit code is 0 when nothing BLOCKING was found, 1 otherwise. WARN never fails the run:
a warning is something to look at, a blocker is something that makes casting impossible.
"""
from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (zpoidh-precast-check)"

# Public Base RPCs. Two of them, because a single endpoint disagreeing with reality is
# exactly the kind of thing that turns "we checked" into "we thought we checked".
BASE_RPCS = (
    "https://mainnet.base.org",
    "https://base-rpc.publicnode.com",
)

# poidh's on-chain floor, confirmed by eth_call on the Base contract (research doc 2202).
MIN_BOUNTY_ETH = 0.001

# Gas headroom on top of the prize. Base is cheap; this is deliberately generous so a
# PASS here does not become a failed transaction.
GAS_HEADROOM_ETH = 0.0007

BLOCKING: list[str] = []
WARNINGS: list[str] = []
NOTES: list[str] = []


def blocking(msg: str) -> None:
    BLOCKING.append(msg)
    print(f"  BLOCK  {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  WARN   {msg}")


def ok(msg: str) -> None:
    NOTES.append(msg)
    print(f"  ok     {msg}")


def load_org_config() -> dict:
    path = REPO_ROOT / "org.config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def eth_balance(address: str) -> float | None:
    """Balance in ETH, agreed by at least two RPCs. None if they disagree or all fail."""
    seen: dict[int, list[str]] = {}
    for rpc in BASE_RPCS:
        payload = json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": "eth_getBalance",
             "params": [address, "latest"]}
        ).encode()
        req = urllib.request.Request(
            rpc, data=payload,
            headers={"Content-Type": "application/json", "User-Agent": UA},
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                wei = int(json.loads(r.read())["result"], 16)
        except Exception as e:
            warn(f"RPC {rpc} did not answer ({type(e).__name__})")
            continue
        seen.setdefault(wei, []).append(rpc)

    if not seen:
        return None
    if len(seen) > 1:
        warn(f"Base RPCs disagree on the balance: {seen}. Check manually before funding.")
        return None
    return next(iter(seen)) / 1e18


def eth_usd() -> float | None:
    try:
        req = urllib.request.Request(
            "https://api.coinbase.com/v2/prices/ETH-USD/spot",
            headers={"User-Agent": UA},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return float(json.loads(r.read())["data"]["amount"])
    except Exception:
        return None


def check_wallet(cfg: dict, prize_eth: float) -> None:
    print("\n[1/5] WALLET")
    addr = cfg.get("treasury_wallet")
    if not addr:
        blocking("org.config.json has no treasury_wallet - cannot check funding")
        return

    need = prize_eth + GAS_HEADROOM_ETH
    have = eth_balance(addr)
    if have is None:
        warn(f"could not read {addr} balance - verify by hand before casting")
        return

    usd = eth_usd()

    def money(e: float) -> str:
        return f"{e:.6f} ETH" + (f" (${e * usd:,.2f})" if usd else "")

    print(f"         issuer {addr}")
    print(f"         have {money(have)} / need {money(need)}  (prize {prize_eth} + gas {GAS_HEADROOM_ETH})")

    if have < need:
        short = need - have
        blocking(f"issuer wallet is SHORT {money(short)}. Fund it before anything else.")
        if prize_eth > MIN_BOUNTY_ETH:
            print(f"         (poidh's on-chain minimum is {MIN_BOUNTY_ETH} ETH, so a smaller round would")
            print( "          cast - but shrinking a locked prize to fit the balance is a silent")
            print( "          downgrade, not a decision. Fund the wallet instead.)")
    else:
        ok(f"issuer wallet can fund this round, {money(have - need)} to spare")


DATE_RE = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(\d{1,2}),\s*(\d{4})",
    re.I,
)
MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}


def check_deadline(round_dir: Path, cast_date: dt.date) -> None:
    """The date in description.md is plain hardcoded text. It does not move when the
    cast slips, which is how a '14-day window' quietly becomes a 7-day one."""
    print("\n[2/5] DEADLINE")
    desc = round_dir / "description.md"
    if not desc.exists():
        blocking(f"{desc.relative_to(REPO_ROOT)} does not exist")
        return

    text = desc.read_text()
    matches = DATE_RE.findall(text)
    if not matches:
        warn("no 'Month D, YYYY' deadline found in description.md - check it by hand")
        return

    month, day, year = matches[-1]
    try:
        deadline = dt.date(int(year), MONTHS[month.lower()], int(day))
    except ValueError:
        warn(f"could not parse deadline '{month} {day}, {year}'")
        return

    window = (deadline - cast_date).days
    print(f"         description says {deadline:%A, %B %-d, %Y}; casting {cast_date:%A, %B %-d}")
    print(f"         that is a {window}-day window")

    weekday = f"{deadline:%A}"
    if weekday.lower() not in text.lower():
        warn(f"description.md does not name the weekday, or names the wrong one - "
             f"{deadline:%B %-d, %Y} is a {weekday}")

    if window < 0:
        blocking(f"the stated deadline is {abs(window)} days in the PAST")
    elif window == 0:
        blocking("the stated deadline is today")
    elif window <= 5:
        blocking(f"a {window}-day window is shorter than any round this repo has run")
    elif window <= 9:
        warn(f"a {window}-day window is shorter than intended. Either re-date "
             f"description.md or accept the shorter round on purpose.")
    else:
        ok(f"{window}-day window")

    if window < 8:
        print("         (the Twitch archive self-deletes after 7 days, so a window this")
        print("          short means entrants who arrive late have almost nothing to clip)")


def check_config(cfg: dict, round_num: int) -> None:
    """Every previous round must be in default_bounty_ids or its entrants score zero.
    R5 sat outside it after closing, so nine claims earned nobody anything."""
    print("\n[3/5] CONFIG")
    ids = cfg.get("default_bounty_ids") or []
    rounds = {r.get("round"): r for r in cfg.get("rounds") or []}

    missing = []
    for n, r in sorted(rounds.items()):
        if n >= round_num:
            continue
        bid = r.get("bounty_id")
        if r.get("offchain"):
            continue  # deliberately excluded, e.g. R4's canceled bounty
        if bid and bid not in ids:
            missing.append((n, bid))

    if missing:
        for n, bid in missing:
            blocking(f"R{n} (bounty {bid}) is NOT in default_bounty_ids - its claimants "
                     f"score nothing on the leaderboard")
    else:
        ok(f"every prior scored round is in default_bounty_ids ({len(ids)} bounties)")

    planned = {r.get("round") for r in cfg.get("planned_rounds") or []}
    if round_num in rounds:
        warn(f"R{round_num} is already in `rounds` - is this round already cast?")
    elif round_num not in planned:
        warn(f"R{round_num} is in neither `rounds` nor `planned_rounds` in org.config.json")
    else:
        ok(f"R{round_num} is listed in planned_rounds")


PLACEHOLDER_RE = re.compile(r"<[A-Z][A-Z0-9_-]{2,}>")

# Figures that must never reach a bounty description. A poidh description is IMMUTABLE once
# cast, so a wrong number in one is permanent and public - R5 shipped "13.9 SOL as of Aug 20"
# and it cannot be fixed, only apologised for.
#
# This list is the enforced half of the do-not-carry table in
# rounds/_template/description.md. That table is prose in a file nobody is required to read;
# this runs before every cast and blocks. Keep the two in step - if you add a row there, add
# a pattern here, or it is advice rather than a rule.
KNOWN_BAD = [
    (r"\b458(\.\d+)?\s*SOL", "458 SOL volume is a superseded May figure and "
     "wavewarz/743 itself says not to use it. Current: 878.316 SOL (wavewarz/974, 2026-07-23)."),
    (r"\b13\.9\b(?!\d)", "13.9 SOL to artists was dated ~2 weeks before the total reached "
     "it. Use the all-legs form with its date, or regenerate from tools/artist-earnings.py."),
    (r"\b1[,.]419\b", "1,419 battles conflicts with the site's own current count and nobody "
     "has settled what counts as a battle. Do not quote a battle count."),
    (r"1\.0+%\s*(artist|share)", "the artist share is 1.005%, not 1.00%."),
    (r"trade fee (is |of )?1\.005", "1.005% is the artist's SHARE of the fee. The trade fee "
     "is 1.500%, split 67/33."),
    (r"\b2\.28\s*%", "2.28% is platform revenue over volume, which FALLS as volume rises. "
     "It is not a fee rate."),
    (r"\b1\.53\s*%", "1.53% folds in settlement bonuses, which are not per-trade."),
]

RECHECK_RE = re.compile(r"[Rr]e-check(?:ed)?\s+(?:the\s+\w+\s+)?by\s+(\d{4}-\d{2}-\d{2})")


def check_known_bad(round_dir: Path) -> None:
    """Block on any figure from the do-not-carry list. Immutable once cast."""
    desc = round_dir / "description.md"
    if not desc.exists():
        return
    body = desc.read_text()
    # only the part that actually gets pasted, if the sentinels are present
    if "<!-- PASTE BELOW THIS LINE -->" in body:
        body = body.split("<!-- PASTE BELOW THIS LINE -->", 1)[1]
        body = body.split("<!-- PASTE ABOVE THIS LINE -->", 1)[0]
    hits = [(re.search(pat, body), why) for pat, why in KNOWN_BAD]
    hits = [(m, why) for m, why in hits if m]
    if not hits:
        ok("no known-bad figures in the pasted description")
        return
    for m, why in hits:
        blocking(f'description contains "{m.group(0).strip()}" - {why}')


def check_recheck_dates(round_dir: Path, today: dt.date) -> None:
    """A re-check date that has passed means the claim beside it is unverified."""
    stale = []
    for f in sorted(round_dir.glob("*.md")):
        for m in RECHECK_RE.finditer(f.read_text()):
            try:
                d = dt.date.fromisoformat(m.group(1))
            except ValueError:
                continue
            if d < today:
                stale.append((f.name, d))
    if not stale:
        return
    for name, d in stale:
        warn(f"{name} carries a re-check date of {d} which has passed - "
             f"re-verify the claim beside it before casting, then move the date")


def check_description(round_dir: Path) -> None:
    print("\n[4/5] DESCRIPTION")
    desc = round_dir / "description.md"
    if not desc.exists():
        return  # already reported by check_deadline

    left = sorted(set(PLACEHOLDER_RE.findall(desc.read_text())))
    if left:
        blocking(f"description.md still has unfilled placeholders: {', '.join(left)}")
    else:
        ok("no unfilled placeholders in description.md")

    validator = REPO_ROOT / "scripts" / "validate-bounty-description.py"
    if not validator.exists():
        warn("validate-bounty-description.py not found, skipped")
        return

    r = subprocess.run(
        [sys.executable, str(validator), "--description", str(desc)],
        capture_output=True, text=True,
    )
    verdict = [ln for ln in r.stdout.splitlines() if "VERDICT" in ln]
    if any("PASS" in v for v in verdict):
        ok("validate-bounty-description.py PASSes")
        print("         (that check matches section HEADERS only and reads nothing inside")
        print("          them - it cannot tell you a REWARD section promises something the")
        print("          round does not actually offer. Read the description yourself too.)")
    else:
        for ln in r.stdout.splitlines():
            if ln.strip().startswith("FAIL"):
                print(f"         {ln.strip()}")
        blocking("validate-bounty-description.py does not pass")


def check_data_freshness(max_age_hours: int = 12) -> None:
    print("\n[5/5] DATA")
    path = REPO_ROOT / "data" / "bounty-dashboard.json"
    if not path.exists():
        warn("data/bounty-dashboard.json missing")
        return
    try:
        gen = json.loads(path.read_text())["generated_at"]
        when = dt.datetime.fromisoformat(gen)
    except Exception as e:
        warn(f"could not read generated_at ({e})")
        return

    if when.tzinfo is None:
        when = when.replace(tzinfo=dt.timezone.utc)
    age = (dt.datetime.now(dt.timezone.utc) - when).total_seconds() / 3600
    if age > max_age_hours:
        warn(f"dashboard data is {age:.1f}h old (cron runs every 6h) - is the workflow green?")
    else:
        ok(f"dashboard data is {age:.1f}h old")


DO_NOT_CARRY_TABLE = REPO_ROOT / "rounds" / "_template" / "description.md"


def table_rows() -> list[str]:
    """The quoted figure from each row of the do-not-carry table in _template.

    The published table and KNOWN_BAD have to say the same thing. A comment asking the
    next person to keep them in step is honor-system, and honor-system rules in this
    estate run at 3-40% while enforced ones run at ~100%. So it is checked, not asked."""
    if not DO_NOT_CARRY_TABLE.exists():
        return []
    rows = []
    for line in DO_NOT_CARRY_TABLE.read_text().splitlines():
        m = re.match(r'\s*\|\s*"([^"]+)"\s*\|', line)
        if m:
            rows.append(m.group(1))
    return rows


def check_no_drift() -> list[str]:
    """Published rows with no enforcing pattern. Empty list means the two are in step."""
    return [r for r in table_rows()
            if not any(re.search(pat, r) for pat, _ in KNOWN_BAD)]


def _selftest() -> bool:
    """No network. Exercises the pure logic - date parsing and the config check."""
    passed = True

    def check(label: str, cond: bool) -> None:
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and cond

    m = DATE_RE.findall("Submissions close 11:59 pm PT, Sunday, September 20, 2026.")
    check("parses a 'Month D, YYYY' deadline", m == [("September", "20", "2026")])
    check("September 20 2026 really is a Sunday",
          dt.date(2026, 9, 20).strftime("%A") == "Sunday")

    check("placeholder regex catches <BOUNTY-ID>",
          PLACEHOLDER_RE.findall("see <BOUNTY-ID> now") == ["<BOUNTY-ID>"])
    check("placeholder regex ignores prose in angle brackets",
          PLACEHOLDER_RE.findall("a <b> tag and <Ok> word") == [])

    global BLOCKING, WARNINGS, NOTES
    BLOCKING, WARNINGS, NOTES = [], [], []
    check_config(
        {"default_bounty_ids": [1151], "rounds": [
            {"round": 1, "bounty_id": 1151},
            {"round": 2, "bounty_id": 1166},
        ], "planned_rounds": [{"round": 3}]},
        round_num=3,
    )
    check("flags a prior round missing from default_bounty_ids",
          any("R2" in b for b in BLOCKING))

    BLOCKING, WARNINGS, NOTES = [], [], []
    check_config(
        {"default_bounty_ids": [1151], "rounds": [
            {"round": 1, "bounty_id": 1151},
            {"round": 2, "bounty_id": 1249, "offchain": True},
        ], "planned_rounds": [{"round": 3}]},
        round_num=3,
    )
    check("does NOT flag a deliberately offchain round",
          not any("R2" in b for b in BLOCKING))

    BLOCKING, WARNINGS, NOTES = [], [], []
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        rd = pathlib.Path(d)
        (rd / "description.md").write_text(
            "<!-- PASTE BELOW THIS LINE -->\n"
            "WaveWarZ has done 458 SOL of volume and paid 13.9 SOL to artists.\n"
            "<!-- PASTE ABOVE THIS LINE -->\n")
        check_known_bad(rd)
    check("blocks a description carrying 458 SOL", any("458" in b for b in BLOCKING))
    check("blocks a description carrying 13.9", any("13.9" in b for b in BLOCKING))

    BLOCKING, WARNINGS, NOTES = [], [], []
    with tempfile.TemporaryDirectory() as d:
        rd = pathlib.Path(d)
        (rd / "description.md").write_text(
            "<!-- PASTE BELOW THIS LINE -->\nA clean description with 60 seconds and 0.0125 ETH.\n"
            "<!-- PASTE ABOVE THIS LINE -->\n")
        check_known_bad(rd)
    check("passes a clean description", not BLOCKING)

    BLOCKING, WARNINGS, NOTES = [], [], []
    with tempfile.TemporaryDirectory() as d:
        rd = pathlib.Path(d)
        # the banned figures live OUTSIDE the paste sentinels - must not block
        (rd / "description.md").write_text(
            "Do not use 458 SOL or 13.9 here.\n"
            "<!-- PASTE BELOW THIS LINE -->\nClean body.\n<!-- PASTE ABOVE THIS LINE -->\n")
        check_known_bad(rd)
    check("ignores banned figures outside the pasted body", not BLOCKING)

    BLOCKING, WARNINGS, NOTES = [], [], []
    with tempfile.TemporaryDirectory() as d:
        rd = pathlib.Path(d)
        (rd / "notes.md").write_text("Re-check by 2020-01-01.\n")
        check_recheck_dates(rd, dt.date(2026, 9, 8))
    check("warns on a passed re-check date", any("2020-01-01" in w for w in WARNINGS))

    BLOCKING, WARNINGS, NOTES = [], [], []
    with tempfile.TemporaryDirectory() as d:
        rd = pathlib.Path(d)
        (rd / "notes.md").write_text("Re-check by 2099-01-01.\n")
        check_recheck_dates(rd, dt.date(2026, 9, 8))
    check("silent on a future re-check date", not WARNINGS)

    BLOCKING, WARNINGS, NOTES = [], [], []
    rows = table_rows()
    check("reads the do-not-carry table out of _template", len(rows) >= 5)
    missed = check_no_drift()
    for r in missed:
        print(f"       UNENFORCED ROW: {r}")
    check("every published do-not-carry row has an enforcing pattern", not missed)

    BLOCKING, WARNINGS, NOTES = [], [], []
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--round", type=int, help="round number, e.g. 6")
    ap.add_argument("--prize", type=float, default=0.0128,
                    help="ETH to fund, fee-adjusted (default 0.0128)")
    ap.add_argument("--cast-date", help="YYYY-MM-DD you intend to cast (default: today)")
    ap.add_argument("--selftest", action="store_true", help="offline logic tests")
    args = ap.parse_args()

    if args.selftest:
        print("precast-check selftest")
        good = _selftest()
        print("selftest:", "passed" if good else "FAILED")
        return 0 if good else 1

    if args.round is None:
        ap.error("--round is required (or use --selftest)")

    cast_date = (dt.date.fromisoformat(args.cast_date) if args.cast_date
                 else dt.date.today())
    round_dir = REPO_ROOT / "rounds" / f"r{args.round}"
    if not round_dir.is_dir():
        print(f"ERROR: {round_dir.relative_to(REPO_ROOT)} does not exist")
        return 1

    cfg = load_org_config()
    print(f"Pre-cast check - R{args.round}, prize {args.prize} ETH, casting {cast_date}")

    check_wallet(cfg, args.prize)
    check_deadline(round_dir, cast_date)
    check_config(cfg, args.round)
    check_description(round_dir)
    check_known_bad(round_dir)
    check_recheck_dates(round_dir, cast_date)
    check_data_freshness()

    print("\n" + "=" * 62)
    if BLOCKING:
        print(f"NOT READY TO CAST - {len(BLOCKING)} blocking, {len(WARNINGS)} warning(s)")
        for b in BLOCKING:
            print(f"  BLOCK  {b}")
        return 1

    if WARNINGS:
        print(f"READY, with {len(WARNINGS)} warning(s) to look at first")
        for w in WARNINGS:
            print(f"  WARN   {w}")
    else:
        print("READY TO CAST - nothing blocking, no warnings")

    print("\nThis script checks preconditions, not judgement. It cannot tell you whether")
    print("the ask is any good, whether the previous round's promises were kept, or")
    print("whether the people who should hear about this round will actually see it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
