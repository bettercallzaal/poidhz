#!/usr/bin/env python3
"""
Did we actually close this round out? The companion to precast-check.py.

precast-check answers "can this round cast". Nothing answered "did we do what the
bounty text said we would after it closed", and the answer turned out to be no for four
rounds running. From docs/PROMISE-AUDIT.md, 2026-09-07:

  R1  promised only the pot. Paid. Clean.
  R2  promised a winner announcement by a named date. Never drafted, never posted.
  R3  promised a winner cast by a named date and a pinned promo. Neither happened.
  R4  promised an equal ETH split. Bounty was canceled by accident; substitute paid.
  R5  promised the clip would run on @wavewarz with credit. Unsent.

Every winner got paid every time. What rots is the promises that cost nothing and have
no deadline enforcing them - a post, a pin, a credit.

This script reads the LIVE on-chain description, because that is the text entrants
actually agreed to and it cannot be edited after the fact. It then:

  1. confirms the money side from chain      - automatic
  2. confirms the round is wired for scoring  - automatic
  3. confirms announcement copy exists        - automatic
  4. lists every promise-shaped sentence      - FOR A HUMAN TO SIGN OFF

Step 4 is deliberately not automated. Whether a clip was actually posted on @wavewarz is
not knowable from a terminal, and a script that guessed would recreate the exact failure
this exists to catch: a confident "done" that nobody checked.

    python3 scripts/postclose-check.py --bounty 1330 --round 5
    python3 scripts/postclose-check.py --bounty 1180 --round 3
    python3 scripts/postclose-check.py --selftest        # offline
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (zpoidh-postclose-check)"
POIDH_SITE = "https://poidh.xyz"
CHAIN_SLUGS = {1: "mainnet", 8453: "base", 42161: "arbitrum", 666666666: "degen"}

# Sentences that commit us to do something AFTER the round closes. Tuned against the real
# text of R1-R5: these patterns catch every promise the hand audit found, and R1 - the one
# clean round - correctly produces only its payout line.
PROMISE_PATTERNS = [
    (r"(?i)\bpinned?\b", "a pin, which no round has ever actually delivered"),
    (r"(?i)winner (?:cast|announced|announcement)", "a winner announcement"),
    (r"(?i)\bannounce", "an announcement"),
    (r"(?i)goes up on|will be reused|we run it|runs your|repost", "publishing the winning work"),
    (r"(?i)credit(?:ed|s)?\b|with your name on it", "crediting the entrant"),
    (r"(?i)airdrop|\$?ZABAL|leaderboard", "a token or leaderboard drop"),
    (r"(?i)split (?:equally|the pot|this pot)|equal slices?", "a pot split"),
    (r"(?i)paid (?:here )?within|winner paid|takes? the (?:full )?pot", "the prize payout"),
]

BLOCKING: list[str] = []
WARNINGS: list[str] = []


def blocking(m: str) -> None:
    BLOCKING.append(m)
    print(f"  BLOCK  {m}")


def warn(m: str) -> None:
    WARNINGS.append(m)
    print(f"  WARN   {m}")


def ok(m: str) -> None:
    print(f"  ok     {m}")


# poidh's /data returns spurious 404s and 504s for bounties that certainly exist - the
# leaderboard cron died on one on 2026-09-08, and bounty 1180 reproduced it by hand the
# same morning, 404 once then 200 on every retry. A genuinely absent bounty 404s every
# time, so retrying costs only seconds on a real absence. --all runs on cron, so an
# unretried blip here would report a healthy round as unreadable.
RETRY_STATUSES = frozenset({404, 429, 500, 502, 503, 504})
RETRY_BACKOFF = (1, 2, 4)


def http_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last: Exception | None = None
    for pause in (*RETRY_BACKOFF, None):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in RETRY_STATUSES:
                raise
            last = e
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
        if pause is None:
            break
        time.sleep(pause)
    raise last  # type: ignore[misc]


def load_org_config() -> dict:
    p = REPO_ROOT / "org.config.json"
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except Exception:
        return {}


def find_promises(description: str) -> list[tuple[str, list[str]]]:
    """Return (sentence, what-it-commits-us-to) per promise-shaped sentence.

    A sentence carrying several promises gets ALL of them, in one entry. R5's text is
    exactly that case - "Winner paid here within 48 hours, and the clip goes up on
    @wavewarz with your name on it" promises a payout AND a publication AND a credit.
    Labelling it only "the prize payout" hid the promise that was actually broken; listing
    it three separate times buried it in noise. The money is never the one that rots."""
    out: list[tuple[str, list[str]]] = []
    seen: set[str] = set()
    chunks = re.split(r"(?<=[.!?])\s+|\n+", description)
    for raw in chunks:
        s = raw.strip()
        if len(s) < 15:
            continue
        labels = [label for pat, label in PROMISE_PATTERNS if re.search(pat, s)]
        if not labels:
            continue
        key = s[:80]
        if key in seen:
            continue
        seen.add(key)
        out.append((s, labels))
    return out


def fetch_accepted_ids(bounty_id: int, chain: int) -> set[int] | None:
    """/data does NOT carry isAccepted. That field only exists on
    claims.fetchBountyClaims, which is exactly why query-bounty.py merges the two.
    Reading /data alone made this script report a PAID round as unpaid - caught
    2026-09-07 against R5, which has been settled since 2026-09-05.
    Returns None if the call fails, so 'unknown' is never rendered as 'unpaid'."""
    import urllib.parse
    inp = urllib.parse.quote(json.dumps(
        {"0": {"json": {"bountyId": bounty_id, "chainId": chain, "limit": 100}}}))
    try:
        r = http_get(f"{POIDH_SITE}/api/trpc/claims.fetchBountyClaims?batch=1&input={inp}")
        payload = r[0]["result"]["data"]["json"]
        # Shape is {"items": [...], "nextCursor": ...} - NOT a bare list. Assuming a list
        # made this return nothing, which surfaced as "payout UNKNOWN" on a round that has
        # been settled since 2026-09-05. Each item's "id" is the same number /data calls
        # "claimId". limit=100 covers every round this repo has run; if a round ever
        # exceeds it, nextCursor needs following.
        rows = payload.get("items", []) if isinstance(payload, dict) else payload
        return {c["id"] for c in rows if c.get("isAccepted")}
    except Exception:
        return None


def check_money(data: dict, bounty_id: int, chain: int) -> dict | None:
    print("\n[1/4] THE MONEY - from chain, automatic")
    claims = data.get("claims") or []
    accepted_ids = fetch_accepted_ids(bounty_id, chain)
    if accepted_ids is None:
        warn("could not read isAccepted from claims.fetchBountyClaims - the payout state is "
             "UNKNOWN, not unpaid. Re-run, or check with query-bounty.py.")
        return None
    accepted = [c for c in claims if c.get("claimId") in accepted_ids]
    amt = int(data.get("amount") or 0) / 1e18

    if data.get("isCanceled"):
        blocking("bounty is CANCELED on chain - the payout path was closed. "
                 "Whatever was promised, a substitute was owed. Check the round's CLOSEOUT.")
        return None
    if not accepted:
        blocking(f"no accepted claim - {amt} ETH has not been awarded")
        return None

    w = accepted[0]
    handle = w.get("farcasterHandle") or w.get("twitterHandle")
    ok(f"paid: {amt} ETH, claim {w.get('claimId')}, "
       f"{'@' + handle if handle else 'wallet ' + str(w.get('issuerAddress'))[:12] + '...'}")
    if not handle:
        warn("the winning wallet resolves to NO linked handle. You cannot credit by name "
             "from chain data alone - confirm who it is before announcing.")
    return w


def check_scoring(cfg: dict, bounty_id: int) -> None:
    print("\n[2/4] SCORING - is this round actually counted, automatic")
    ids = cfg.get("default_bounty_ids") or []
    if bounty_id in ids:
        ok(f"bounty {bounty_id} is in default_bounty_ids, so its claimants score")
    else:
        blocking(f"bounty {bounty_id} is NOT in default_bounty_ids - every entrant in this "
                 f"round scores ZERO on the leaderboard. This is exactly what happened to "
                 f"R5 until 2026-09-06.")


def check_copy(round_dir: Path) -> None:
    print("\n[3/4] ANNOUNCEMENT COPY - does it even exist, automatic")
    if not round_dir.is_dir():
        warn(f"{round_dir.name}/ does not exist - cannot check for copy")
        return
    cands = list(round_dir.glob("*winner-announce*")) + \
        list((round_dir / "cast-templates").glob("*winner-announce*")) if (round_dir / "cast-templates").is_dir() \
        else list(round_dir.glob("*winner-announce*"))
    if cands:
        ok(f"copy exists: {', '.join(str(c.relative_to(round_dir)) for c in cands)}")
        print("         (existing is not sent. R3's has been READY TO SEND since June.)")
    else:
        blocking(f"no winner-announce copy anywhere in {round_dir.name}/ - "
                 f"R2 had none either, and R2's winner was never announced")


def check_promises(description: str) -> None:
    print("\n[4/4] PROMISES - NOT AUTOMATED, a human signs these off")
    promises = find_promises(description)
    if not promises:
        ok("no promise-shaped sentences found beyond the payout")
        return
    print(f"         {len(promises)} sentence(s) in the live bounty text commit us to something.")
    print("         Tick each one off by hand. A terminal cannot see a pin or a post.\n")
    for i, (s, labels) in enumerate(promises, 1):
        s = s if len(s) <= 150 else s[:147] + "..."
        print(f"         [ ] {i}. {'; '.join(labels)}")
        print(f"                \"{s}\"")
    warn(f"{len(promises)} promise(s) need human sign-off - this script cannot close them")


def _selftest() -> bool:
    passed = True

    def check(label: str, cond: bool) -> None:
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and cond

    r5 = ("One winner, chosen using poidh consensus. Winner paid here within 48 hours, "
          "and the clip goes up on @wavewarz with your name on it.")
    p = find_promises(r5)
    labels = [l for _, ls in p for l in ls]
    check("R5's one sentence yields payout AND publish AND credit",
          len(p) == 1 and len(labels) >= 3)
    check("catches 'goes up on @wavewarz'", any("goes up on" in s for s, _ in p))
    check("the broken promise is not hidden behind the payout label",
          any("publishing" in l for l in labels))

    r3 = "Winner clip becomes ZABAL Gamez's pinned promo across @bettercallzaal channels."
    check("catches a pin promise",
          any("pin" in l for _, ls in find_promises(r3) for l in ls))

    r1 = ("The reward: One winner takes the full pot - and the pot grows in real time as "
          "others contribute. Track it live on poidh.")
    p1 = find_promises(r1)
    check("R1, the clean round, yields only its payout line", len(p1) == 1)

    check("ignores fragments too short to be a promise", find_promises("Pinned.") == [])

    dup = "The winner gets credited. The winner gets credited."
    check("does not report the same sentence twice", len(find_promises(dup)) == 1)
    return passed


def sweep_all(chain: int) -> int:
    """Every cast round, automatic checks only. Built for the 6h cron.

    This exists because a checker nobody runs is a checker that does not exist.
    scripts/check-eb-sync.py sat uninvoked from 2026-08-08 to 2026-09-07 while the drift
    it detects stayed open the whole time. The specific thing this catches is R5's
    failure: bounty 1330 closed, was paid, and was never added to default_bounty_ids, so
    nine claimants scored zero on the leaderboard for weeks and nothing said so.

    Deliberately does NOT check promises - those need a human, and a cron that asked a
    human something every six hours would be ignored inside a day."""
    cfg = load_org_config()
    rounds = sorted(cfg.get("rounds") or [], key=lambda r: r.get("round", 0))
    ids = set(cfg.get("default_bounty_ids") or [])
    problems = 0

    print(f"Post-close sweep - {len(rounds)} cast round(s)\n")
    for r in rounds:
        n, bid = r.get("round"), r.get("bounty_id")
        if not bid:
            continue
        label = f"R{n} ({bid})"
        if r.get("offchain"):
            print(f"  skip   {label} - offchain by design: {str(r.get('offchain_note',''))[:60]}...")
            continue
        try:
            d = http_get(f"{POIDH_SITE}/{CHAIN_SLUGS.get(chain,'base')}/bounty/{bid}/data")
        except Exception as e:
            print(f"  ?      {label} - could not read ({type(e).__name__}). UNKNOWN, not broken.")
            continue

        if bid not in ids:
            print(f"  BROKEN {label} - not in default_bounty_ids, its claimants score ZERO")
            problems += 1
            continue

        acc = fetch_accepted_ids(bid, chain)
        if acc is None:
            print(f"  ?      {label} - payout state UNKNOWN, could not read isAccepted")
        elif not acc and not d.get("isCanceled"):
            print(f"  BROKEN {label} - closed and scored, but nothing accepted yet")
            problems += 1
        else:
            print(f"  ok     {label} - wired for scoring, payout settled")

    print()
    if problems:
        print(f"{problems} round(s) need attention. This is the check that would have caught")
        print("R5's nine claimants scoring zero, weeks before anyone noticed by hand.")
        return 1
    print("Every cast round is wired for scoring and settled.")
    print("Promises are NOT checked here - run --bounty <id> --round <n> for those.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bounty", type=int)
    ap.add_argument("--round", type=int)
    ap.add_argument("--chain", type=int, default=8453)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--all", action="store_true",
                    help="sweep every cast round in org.config.json - the automatic checks "
                         "only, for cron. Exits non-zero if any round is unwired or unpaid.")
    a = ap.parse_args()

    if a.selftest:
        print("postclose-check selftest")
        good = _selftest()
        print("selftest:", "passed" if good else "FAILED")
        return 0 if good else 1

    if a.all:
        return sweep_all(a.chain)

    if a.bounty is None:
        ap.error("--bounty is required (or use --selftest or --all)")

    slug = CHAIN_SLUGS.get(a.chain, "base")
    try:
        data = http_get(f"{POIDH_SITE}/{slug}/bounty/{a.bounty}/data")
    except urllib.error.HTTPError as e:
        print(f"ERROR: bounty {a.bounty} on chain {a.chain}: HTTP {e.code}")
        return 1

    print(f"Post-close check - bounty {a.bounty}"
          + (f", R{a.round}" if a.round else "")
          + f"\n  {data.get('title')}")

    check_money(data, a.bounty, a.chain)
    check_scoring(load_org_config(), a.bounty)
    if a.round:
        check_copy(REPO_ROOT / "rounds" / f"r{a.round}")
    check_promises(data.get("description") or "")

    print("\n" + "=" * 62)
    if BLOCKING:
        print(f"NOT CLOSED OUT - {len(BLOCKING)} blocking, {len(WARNINGS)} warning(s)")
        for b in BLOCKING:
            print(f"  BLOCK  {b}")
        return 1
    print(f"Money and wiring are clean. {len(WARNINGS)} thing(s) still need a human.")
    print("\nThis script cannot tell you a post went out. It can only tell you what you")
    print("said you would do. Four rounds have been paid and left owing something.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
