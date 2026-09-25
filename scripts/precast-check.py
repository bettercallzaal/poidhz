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
import importlib.util
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


def check_deadline(round_dir: Path, cast_date: dt.date, kind: str = "media",
                   after_event_reason: str = "") -> None:
    """The date in description.md is plain hardcoded text. It does not move when the
    cast slips, which is how a '14-day window' quietly becomes a 7-day one.

    `kind` exists because the festival deadline is not universal. Every promo round is worth
    nothing after October 3, so closing later is a hard block. A CODE round is not promo: round
    five asks for pull requests against the repo, which outlives the event, and it closes on
    October 4 on purpose. Before this argument existed the check blocked that round with a
    sentence about promo - a true rule applied to a round it was never written for.
    """
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

    # THESE THRESHOLDS WERE WRITTEN FOR THE WEEKLY ROUNDS AND WENT STALE, AND THE STALE
    # VERSION MADE A FALSE CLAIM. It blocked a 3-day window with "shorter than any round this
    # repo has run" on 2026-09-24 - while daily-01, daily-02 and daily-03 had each run for a
    # SINGLE day and all three filled. It also printed a note about the Twitch archive
    # self-deleting after 7 days, which has nothing to do with a ZAOstock promo round and was
    # printed under every short window regardless of what the round asked for.
    #
    # A short window is now a WARNING that states the real trade-off, not a block. The thing
    # that actually makes a window too short is the EVENT, and that is checked separately
    # below.
    if window < 0:
        blocking(f"the stated deadline is {abs(window)} days in the PAST")
    elif window == 0:
        blocking("the stated deadline is today")
    elif window <= 2:
        warn(f"a {window}-day window is very short. The daily rounds ran one day each and "
             f"filled, so this is possible - but it leaves no room for a draft checkpoint "
             f"and no room for anyone who sees the post late.")
    elif window <= 9:
        ok(f"{window}-day window - in line with this run, whose rounds have been 1 to 3 days")
    else:
        ok(f"{window}-day window")

    # The only deadline that cannot move. A promo round that closes after the thing it
    # promotes is worth nothing, and this repo has an event with a fixed date.
    event = dt.date(2026, 10, 3)
    if deadline > event and kind == "code":
        reason = after_event_reason or ("a code round is not promo - the repository outlives "
                                       "the festival")
        ok(f"closes {(deadline - event).days} day(s) AFTER ZAOstock, and for a code round that "
           f"is deliberate: {reason}")
    elif deadline > event:
        blocking(f"the stated deadline is AFTER ZAOstock ({event:%B %-d}). Promo that lands "
                 f"after the festival is worth nothing. If this round is not promo, record "
                 f"its kind in org.config.json (e.g. \"kind\": \"code\") rather than "
                 f"silencing the check.")
    elif deadline == event:
        warn("the round closes ON the day of the festival - there is no time to use the work")
    else:
        ok(f"closes {(event - deadline).days} days before ZAOstock, leaving time to use it")


def round_sort_key(n) -> tuple:
    """Order round ids that are NOT all the same type.

    THIS FUNCTION EXISTS BECAUSE THIS FILE CRASHED. `org.config.json` carries integer rounds
    (1..5) and string rounds ("daily-01".."daily-04") since the ZAOstock ladder started, and
    `sorted(rounds.items())` raised

        TypeError: '<' not supported between instances of 'str' and 'int'

    which took the whole pre-cast gate down with it - measured 2026-09-24 while checking the
    round-four draft. A gate that crashes does not gate anything, and it crashed at step 3 of
    5, so the two checks after it never ran either.
    """
    return (0, n, "") if isinstance(n, int) else (1, 0, str(n))


def coerce_round(v):
    """"6" becomes 6; "daily-04" stays a string. Keeps integer rounds comparing as numbers."""
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return v


def precedes(n, round_num) -> bool:
    """Whether round `n` comes before the one being cast, across both id styles.

    Integers compare to integers. A "daily-NN" string compares to another "daily-NN". Comparing
    one to the other is meaningless - daily-02 is not "before" R5 in any sense that matters to
    the leaderboard - so it returns False rather than guessing, which is the behaviour the old
    `n >= round_num` had by accident for ints and by crashing for strings.
    """
    if isinstance(n, int) and isinstance(round_num, int):
        return n < round_num
    if isinstance(n, str) and isinstance(round_num, str):
        return n < round_num
    return False


def resolve_round_id(cfg: dict, round_arg):
    """The config's own id for a round, given any spelling a human types on the CLI.

    `--round d04` is the folder's name and reads naturally, but the config key is `daily-04`.
    Before this existed the two halves of the check disagreed: `round_folder` found
    rounds/daily/d04 through its fallback, while `check_config` compared the literal string
    "d04" against the config keys, missed, and printed "Rd04 is in neither `rounds` nor
    `planned_rounds`" - about a round that was sitting in `planned_rounds` the whole time.
    Measured 2026-09-25 on d04. A warning that is false trains you to skip warnings.

    Returns the config's id (coerced), or the argument unchanged when nothing matches - a
    round genuinely absent from the config must still reach `check_config` and warn.
    """
    for r in cfg.get("rounds", []) + (cfg.get("planned_rounds") or []):
        names = {str(r.get("round"))}
        folder = r.get("folder")
        if folder:
            names.add(Path(folder).name)
        if str(round_arg) in names:
            return coerce_round(r.get("round"))
    return coerce_round(round_arg)


def round_meta(cfg: dict, round_id) -> dict:
    """The config entry for a round, from either list. Empty dict when it has none."""
    for r in cfg.get("rounds", []) + (cfg.get("planned_rounds") or []):
        if str(r.get("round")) == str(round_id):
            return r
    return {}


def round_kind(cfg: dict, round_id) -> str:
    """"media" unless the config says otherwise. The default is the strict one on purpose:
    an unlabelled round gets the promo rules, including the hard October 3 deadline."""
    return str(round_meta(cfg, round_id).get("kind") or "media")


def round_folder(cfg: dict, round_arg) -> Path:
    """The directory that really holds this round, from org.config.json.

    Accepts either style of round id: `--round 6` for rounds/r6, or `--round daily-04` for
    whatever `folder` the config records. Falls back to rounds/r<arg> only when the config has
    nothing, and that fallback is visible in the output rather than silent.
    """
    round_arg = resolve_round_id(cfg, round_arg)
    for r in cfg.get("rounds", []) + (cfg.get("planned_rounds") or []):
        if str(r.get("round")) == str(round_arg) and r.get("folder"):
            return REPO_ROOT / r["folder"]
    guess = REPO_ROOT / "rounds" / f"r{round_arg}"
    if not guess.is_dir():
        for cand in (REPO_ROOT / "rounds" / "daily" / f"d{str(round_arg).zfill(2)}",
                     REPO_ROOT / "rounds" / "daily" / str(round_arg).replace("daily-", "d")):
            if cand.is_dir():
                return cand
    return guess


def check_config(cfg: dict, round_num) -> None:
    """Every previous round must be in default_bounty_ids or its entrants score zero.
    R5 sat outside it after closing, so nine claims earned nobody anything."""
    print("\n[3/5] CONFIG")
    ids = cfg.get("default_bounty_ids") or []
    rounds = {r.get("round"): r for r in cfg.get("rounds") or []}

    missing = []
    for n, r in sorted(rounds.items(), key=lambda kv: round_sort_key(kv[0])):
        if not precedes(n, round_num):
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

# What validate-bounty-description.py actually checks, printed next to its PASS so a green
# line is not read as more assurance than it is. This used to say the validator "matches
# section HEADERS only and reads nothing inside them". That stopped being true when the
# validator gained SECTION_MUST_CONTAIN, and it went on printing for days - understating a
# check is the same defect as overstating one, and it survived because prose about code has
# nothing holding it to the code. The selftest now pins it: every section the validator
# inspects has to be named here, so adding a fifth fails until this text is updated.
VALIDATOR_CAVEAT = (
    "(it reads four section BODIES, not just headers: THE BAR needs a\n"
    " numbered or bulleted rule, THE REWARD a prize amount with its token,\n"
    " DEADLINE a real date or time, THE ASSET KIT a usable link. It still\n"
    " cannot tell you THE REWARD promises something this round does not\n"
    " actually offer. Read the description yourself too.)"
)

# A code round's skeleton is WHY / THE REPO / WHAT COUNTS / THE REWARD / DEADLINE, and only two
# of those five have a body rule - the other three are matched by their header alone. Saying so
# is the point: the media caveat above would otherwise be printed under a code round and name
# sections that round does not have.
CODE_VALIDATOR_CAVEAT = (
    "(code skeleton: WHY, THE REPO, WHAT COUNTS, THE REWARD, DEADLINE. Only\n"
    " THE REWARD and DEADLINE have their BODIES read - a pointer to the live\n"
    " pot, and a real date or time. WHY, THE REPO and WHAT COUNTS are matched\n"
    " by their headers alone, so a PASS does not mean the repo link resolves\n"
    " or that WHAT COUNTS says anything. Read the description yourself too.)"
)


def validator_sections() -> list[str]:
    """The section ids validate-bounty-description.py inspects the body of.

    Imported from the validator rather than restated, so the two cannot disagree."""
    spec = importlib.util.spec_from_file_location(
        "_vbd", pathlib.Path(__file__).resolve().parent / "validate-bounty-description.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return sorted(mod.SECTION_MUST_CONTAIN)


def paste_body(text: str) -> tuple[str, str]:
    """The part of a description.md that actually gets pasted into poidh, and how we knew.

    Rounds have used three conventions and nothing standardised them: R6 and R7 use sentinel
    comments, R5 fences its TITLE (not its description), R1-R3 have no marker at all.

    Only the sentinels are trusted. Guessing was tried and was worse than not guessing: a
    "longest fenced block" heuristic extracted R5's 8-word title as its description, which
    would have scanned almost none of the real text while looking like it had worked.

    Without sentinels the whole file is scanned and the caller warns. Over-scanning can
    cause a false block, which is visible and correctable in one edit. Under-scanning
    silently passes a banned figure into text that is immutable once cast. Those failures
    are not symmetrical, so the fallback is the loud one."""
    if "<!-- PASTE BELOW THIS LINE -->" in text:
        b = text.split("<!-- PASTE BELOW THIS LINE -->", 1)[1]
        return b.split("<!-- PASTE ABOVE THIS LINE -->", 1)[0], "sentinel comments"
    return text, "whole file (no marker)"


def check_known_bad(round_dir: Path) -> None:
    """Block on any figure from the do-not-carry list. Immutable once cast."""
    desc = round_dir / "description.md"
    if not desc.exists():
        return
    body, how = paste_body(desc.read_text())
    if how == "whole file (no marker)":
        warn("description.md has no paste marker, so the whole file is being scanned - "
             "instructional prose can trip a false block. Add the "
             "<!-- PASTE BELOW THIS LINE --> sentinels from rounds/_template.")
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


def check_description(round_dir: Path, kind: str = "media") -> None:
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

    # A code round has its own skeleton. Running the media validator against it reports FAIL on
    # sections a code bounty is not supposed to have, which is how round five looked broken
    # while being correct. The kind comes from org.config.json, so the two checks cannot drift.
    cmd = [sys.executable, str(validator), "--description", str(desc)]
    if kind == "code":
        cmd += ["--kind", "code"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    verdict = [ln for ln in r.stdout.splitlines() if "VERDICT" in ln]
    if any("PASS" in v for v in verdict):
        ok(f"validate-bounty-description.py PASSes"
           f"{' (--kind code)' if kind == 'code' else ''}")
        caveat = CODE_VALIDATOR_CAVEAT if kind == "code" else VALIDATOR_CAVEAT
        for line in caveat.splitlines():
            print(f"         {line}")
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
        warn(f"dashboard data is {age:.1f}h old (cron runs hourly) - is the workflow green?")
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

    # The alias bug, captured. `--round d04` is the folder name; `daily-04` is the config key.
    alias_cfg = {"default_bounty_ids": [], "rounds": [],
                 "planned_rounds": [{"round": "daily-04", "folder": "rounds/daily/d04"}]}
    check("folder-style d04 resolves to the config key daily-04",
          resolve_round_id(alias_cfg, "d04") == "daily-04")
    check("the config key itself still resolves to itself",
          resolve_round_id(alias_cfg, "daily-04") == "daily-04")
    check("an integer round is unchanged and stays an int",
          resolve_round_id(alias_cfg, "6") == 6)
    check("a round absent from the config is returned unchanged, so it can still warn",
          resolve_round_id(alias_cfg, "d09") == "d09")

    BLOCKING, WARNINGS, NOTES = [], [], []
    check_config(alias_cfg, resolve_round_id(alias_cfg, "d04"))
    check("d04 no longer warns that it is missing from the config",
          not any("neither" in w for w in WARNINGS))

    # kind: the default must stay strict, and a code round must not be blocked by the promo rule
    kind_cfg = {"rounds": [{"round": "daily-04", "folder": "rounds/daily/d04"}],
                "planned_rounds": [{"round": "daily-05", "folder": "rounds/daily/d05",
                                    "kind": "code"}]}
    check("a round with no kind is treated as media", round_kind(kind_cfg, "daily-04") == "media")
    check("a code round reports its kind", round_kind(kind_cfg, "daily-05") == "code")
    check("a round absent from the config is still media",
          round_kind(kind_cfg, "daily-99") == "media")

    import tempfile as _tf
    def _deadline(kind: str, closes: str) -> tuple[list, list]:
        global BLOCKING, WARNINGS, NOTES
        BLOCKING, WARNINGS, NOTES = [], [], []
        with _tf.TemporaryDirectory() as d:
            rd = pathlib.Path(d)
            (rd / "description.md").write_text(f"Submissions close 5:00pm Eastern, {closes}.\n")
            check_deadline(rd, dt.date(2026, 9, 25), kind)
        return BLOCKING, WARNINGS

    b, _ = _deadline("media", "Sunday, October 4, 2026")
    check("a MEDIA round closing after the festival is still blocked",
          any("AFTER ZAOstock" in x for x in b))
    b, _ = _deadline("code", "Sunday, October 4, 2026")
    check("a CODE round closing after the festival is not blocked", not b)
    b, _ = _deadline("code", "Thursday, September 3, 2026")
    check("a CODE round with a deadline in the past is still blocked",
          any("PAST" in x for x in b))

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

    b, how = paste_body("head\n<!-- PASTE BELOW THIS LINE -->\nBODY\n<!-- PASTE ABOVE THIS LINE -->\ntail")
    check("sentinel style extracts only the body",
          b.strip() == "BODY" and how == "sentinel comments")
    _, how = paste_body("a description with no marker at all, several words long")
    check("no marker scans the whole file and says so", how == "whole file (no marker)")
    b, _ = paste_body("notes\n\n```\nshort title\n```\n\nthe real description follows here\n")
    check("a fenced title is NOT mistaken for the body", "real description" in b)

    secs = validator_sections()
    unnamed = [s for s in secs if s.replace("_", " ").upper() not in VALIDATOR_CAVEAT.upper()]
    for s in unnamed:
        print(f"       CAVEAT DOES NOT MENTION: {s}")
    check("the printed caveat names every section the validator inspects",
          secs and not unnamed)

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
    # NOT type=int. org.config.json has carried string round ids ("daily-01") since the
    # ZAOstock ladder started, and argparse rejected them before any check could run.
    ap.add_argument("--round", help="round id: 6, or daily-04")
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
    # THE FOLDER COMES FROM THE CONFIG, NOT FROM f"r{round}". Passing --round 4 used to read
    # rounds/r4 - the ZABAL Gamez open pot from July, whose stated deadline is 2026-07-31 - and
    # then BLOCK with "the stated deadline is 55 days in the PAST", which is a true statement
    # about a completely different round. The same shape was fixed in postclose-check.py on
    # 2026-09-23. A check that reads the wrong directory and answers confidently is worse than
    # no check.
    round_dir = round_folder(load_org_config(), args.round)
    if not round_dir.is_dir():
        print(f"ERROR: {round_dir.relative_to(REPO_ROOT)} does not exist")
        return 1

    cfg = load_org_config()
    round_id = resolve_round_id(cfg, args.round)
    kind = round_kind(cfg, round_id)
    typed = f" (you typed {args.round})" if str(round_id) != str(args.round) else ""
    print(f"Pre-cast check - R{round_id}{typed}, kind {kind}, "
          f"prize {args.prize} ETH, casting {cast_date}")

    check_wallet(cfg, args.prize)
    check_deadline(round_dir, cast_date, kind,
                   round_meta(cfg, round_id).get("closes_after_event_on_purpose", ""))
    check_config(cfg, round_id)
    check_description(round_dir, kind)
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
