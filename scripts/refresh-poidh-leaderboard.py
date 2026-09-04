#!/usr/bin/env python3
"""
Refresh poidh-leaderboard.json + poidh-claims.json by aggregating data
across one or more BCZ-issued POIDH bounties + the live $ZABAL Empire
POIDH Submitters leaderboard.

    python3 scripts/refresh-poidh-leaderboard.py
    python3 scripts/refresh-poidh-leaderboard.py --bounty 1151 --bounty 1166

Writes three files into data/:

    data/leaderboard.json  - Empire Builder API-Sourced feed [{address, score}]
                             (the strict schema EB pulls; served at /leaderboard)
    data/claims.json       - Rich data for the hub: bounties + claims + live EB
                             leaderboard with handles + rewards + web3.bio
                             profile supplements (avatar, X handle). Sorted by
                             rank = the ranked leaderboard the hub renders.
    data/audit.json        - Full claim trail for verification

Score = 1 per unique submitter wallet across the whole bounty set. Issuer
wallets are excluded (PoidhV3 enforces issuer != claimant on-chain).

Nothing is written unless the whole run is healthy. Every source below can fail
in a way that produces a smaller, emptier, still-valid-looking set of files, so
the run is compared against the files already on disk and refused if anything
that should only grow went backwards. See guard_publishable().

Data sources (all free, no API keys):
    - poidh.xyz /data: GET /<chain>/bounty/<id>/data - full bounty + every claim
      in one call, Farcaster/X handles already resolved (doc 2202: found via
      Kenny; replaces the tRPC-scrape + web3.bio-handle-lookup pattern)
    - poidh.xyz tRPC: claims.fetchBountyClaims, kept ONLY to recover per-claim
      isAccepted/onChainId, which /data does not expose (verified 2026-08-20);
      degrades to WARN + accepted=false if it goes away
    - empirebuilder.world API: GET /api/leaderboards/<uuid> (handles + rewards)
    - api.web3.bio: GET /profile/<address> (avatar, fid, follower - enrichment
      only; handles come from /data first)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_org_config() -> dict:
    """Read org.config.json if present. Forking zpoidh for your own org? Edit
    that file - every script reads from it instead of BCZ's hardcoded values.
    Missing file or missing key = falls back to BCZ's original defaults below,
    so this is purely additive and never breaks existing behavior."""
    path = REPO_ROOT / "org.config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


_CFG = load_org_config()
DEFAULT_BOUNTY_IDS = _CFG.get("default_bounty_ids", [1151, 1166, 1180, 1249])
DEFAULT_CHAIN_ID = _CFG.get("default_chain_id", 8453)
ZABAL_EMPIRE_ID = _CFG.get("empire_token_address", "0xbB48f19B0494Ff7C1fE5Dc2032aeEE14312f0b07")
POIDH_LEADERBOARD_UUID = _CFG.get("empire_leaderboard_uuid", "7b8e8dfa-529d-48ad-8c9b-bdb45cc35187")

POIDH_BASE = "https://poidh.xyz/api/trpc"
POIDH_SITE = "https://poidh.xyz"
EB_BASE = "https://www.empirebuilder.world/api"
WEB3_BIO_BASE = "https://api.web3.bio"

# poidh.xyz URL slugs per chain id (the /data endpoint is path-addressed)
CHAIN_SLUGS = {8453: "base", 42161: "arbitrum", 1: "ethereum", 666666666: "degen"}

UA = "Mozilla/5.0 (poidh-leaderboard-refresh)"

# Every path in this script that used to print a WARN and carry on appends here
# instead. A non-empty list at write time means this run assembled worse data
# than the files already on disk, which is never worth publishing - see
# guard_publishable() for why that matters and what it refuses.
DEGRADATIONS: list[str] = []


def http_get(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def trpc(proc: str, payload: dict) -> dict:
    inp = urllib.parse.quote(json.dumps({"0": {"json": payload}}))
    return http_get(f"{POIDH_BASE}/{proc}?batch=1&input={inp}")[0]["result"]["data"]["json"]


def fetch_bounty_data(bid: int, chain: int) -> dict:
    """One GET against poidh's /data endpoint: the full bounty object plus
    EVERY claim (no pagination), with farcasterHandle/twitterHandle already
    resolved per claim. Shape verified live against bounty 1180, 2026-08-20:
    claims carry claimId, imageUrl, issuerAddress, issuerName, farcasterHandle,
    twitterHandle, title, description - and do NOT carry isAccepted/onChainId
    (see fetch_accepted_map)."""
    slug = CHAIN_SLUGS.get(chain)
    if slug is None:
        raise SystemExit(f"unknown chain id {chain} - add it to CHAIN_SLUGS")
    return http_get(f"{POIDH_SITE}/{slug}/bounty/{bid}/data")


def fetch_accepted_map(bid: int, chain: int) -> dict[int, dict]:
    """Map claimId -> {accepted, on_chain_id} via the one tRPC call that /data
    cannot replace yet. Best-effort: if tRPC breaks, the refresh still runs and
    the accepted flag degrades to false with a loud WARN (never silently)."""
    out: dict[int, dict] = {}
    try:
        resp = trpc("claims.fetchBountyClaims", {"bountyId": bid, "chainId": chain, "limit": 100})
        items = resp.get("items", [])
        cursor = resp.get("nextCursor")
        for _ in range(49):
            if not cursor:
                break
            resp = trpc("claims.fetchBountyClaims",
                        {"bountyId": bid, "chainId": chain, "limit": 100, "cursor": cursor})
            items.extend(resp.get("items", []))
            cursor = resp.get("nextCursor")
            time.sleep(0.2)  # courtesy delay on someone else's public API
        for c in items:
            out[c["id"]] = {"accepted": bool(c.get("isAccepted")), "on_chain_id": c.get("onChainId")}
    except Exception as e:
        print(f"  WARN: tRPC accepted-flag fetch failed for bounty {bid}: {e} - "
              f"claims will carry accepted=false, on_chain_id=null this run")
        DEGRADATIONS.append(f"bounty {bid}: tRPC accepted-flag fetch failed ({e}), "
                            f"every claim would publish as accepted=false")
    return out


def fetch_eb_leaderboard() -> dict:
    try:
        return http_get(f"{EB_BASE}/leaderboards/{POIDH_LEADERBOARD_UUID}", timeout=15)
    except Exception as e:
        print(f"  WARN: EB leaderboard fetch failed: {e}")
        DEGRADATIONS.append(f"Empire Builder leaderboard fetch failed ({e}), so every rank, "
                            f"boost and totalRewards would publish as null")
        return {"success": False, "leaderboard": None, "entries": []}


def fetch_web3_bio(address: str) -> dict | None:
    try:
        d = http_get(f"{WEB3_BIO_BASE}/profile/{address}", timeout=10)
        if isinstance(d, list) and d:
            for row in d:
                if row.get("platform") == "farcaster":
                    return row
            return d[0]
        return None
    except Exception:
        return None


def load_offchain_credits() -> list[dict]:
    """Off-chain round credits from org.config.json's offchain_credits - rounds where
    the normal on-chain claim path broke (e.g. R4's bounty got canceled instead of
    withdrawn) and participants were credited directly via a wallet,score CSV instead.
    Each entry names a CSV of wallets to flat-credit + a note explaining why."""
    credits = []
    for entry in _CFG.get("offchain_credits", []):
        csv_path = REPO_ROOT / entry["wallets_csv"]
        if not csv_path.exists():
            print(f"  WARN: offchain_credits round {entry.get('round')} references missing file {csv_path}")
            DEGRADATIONS.append(f"offchain_credits round {entry.get('round')} references missing "
                                f"file {entry['wallets_csv']}, so those wallets would silently "
                                f"lose their credit")
            continue
        wallets = []
        with open(csv_path) as f:
            for row in csv.DictReader(f):
                wallets.append(row["address"].lower())
        credits.append({
            "round": entry.get("round"),
            "score": entry.get("score", 1),
            "note": entry.get("note", ""),
            "wallets": wallets,
        })
    return credits


def validate_claim_address(addr: str) -> bool:
    """Check if address is a valid Ethereum address (0x + 40 hex chars)."""
    if not isinstance(addr, str):
        return False
    if not addr.startswith("0x"):
        return False
    if len(addr) != 42:  # 0x + 40 hex chars
        return False
    try:
        int(addr, 16)
        return True
    except ValueError:
        return False


def summarize(feed: list[dict], enriched: list[dict], claims: list[dict], eb_entries: list[dict]) -> dict:
    """The four numbers that decide whether a run is publishable. Kept as a plain
    dict so guard_publishable() can be tested without touching the network or disk."""
    return {
        "submitters": len(feed),
        "accepted_claims": sum(1 for c in claims if c.get("accepted")),
        "ranked": sum(1 for e in enriched if e.get("rank") is not None),
        "zabal": round(sum(e.get("totalRewards", 0) or 0 for e in eb_entries), 4),
    }


def summarize_on_disk(feed_path: Path, claims_path: Path, audit_path: Path) -> dict | None:
    """The same four numbers read back off the files this run is about to replace.
    Returns None on a first-ever run (nothing to compare against), which is the one
    case where every shrink check has to be skipped rather than failed."""
    try:
        feed = json.loads(feed_path.read_text())
        claims_doc = json.loads(claims_path.read_text())
        audit_doc = json.loads(audit_path.read_text())
    except Exception:
        return None
    return {
        "submitters": len(feed) if isinstance(feed, list) else 0,
        "accepted_claims": sum(1 for c in audit_doc.get("claims") or [] if c.get("accepted")),
        "ranked": sum(1 for e in claims_doc.get("leaderboard") or [] if e.get("rank") is not None),
        "zabal": (claims_doc.get("totals") or {}).get("total_zabal_distributed") or 0,
    }


def guard_publishable(new: dict, existing: dict | None, degradations: list[str],
                      allow_shrink: bool = False) -> list[str]:
    """Return the reasons this run must not be written, empty list if it is safe.

    Written after 2026-08-23, when build-bounty-dashboard.py committed
    total_bounties: 0 over 100 live listings because a transient upstream failure
    was indistinguishable from a real empty answer. This script has the same
    shape in four more places, and one thing that incident taught is that an
    exception is not the only way a fetch fails: an upstream that answers 200
    with an empty body degrades data without raising anything at all.

    So there are two families of check here. The degradation list catches the
    paths that threw and were swallowed. The comparisons against what is already
    on disk catch the paths that returned successfully and returned nothing,
    which no amount of exception handling would ever see.

    Every quantity below only ever grows in normal operation. Submitters are
    append-only, an accepted claim is finalised on-chain and cannot un-accept,
    and Empire Builder rank and reward totals are cumulative. A decrease is
    therefore a broken run, not news - except when a human is deliberately
    correcting the set, which is what --allow-shrink is for."""
    blocking: list[str] = []

    for d in degradations:
        blocking.append(d)

    if new["submitters"] == 0:
        blocking.append("assembled 0 submitters; empty is never a real answer here, "
                        "wallets that have already scored cannot un-score")

    if existing is None:
        return blocking

    if not allow_shrink:
        if new["submitters"] < existing["submitters"]:
            blocking.append(f"submitters fell {existing['submitters']} -> {new['submitters']}; "
                            f"the leaderboard is append-only, pass --allow-shrink if this "
                            f"removal is deliberate")
        if new["accepted_claims"] < existing["accepted_claims"]:
            blocking.append(f"accepted claims fell {existing['accepted_claims']} -> "
                            f"{new['accepted_claims']}; an accepted claim is finalised "
                            f"on-chain and cannot un-accept")

    # These two are the 200-with-an-empty-body case: no exception was raised, so
    # nothing is in the degradation list, but the enrichment silently vanished.
    if existing["ranked"] > 0 and new["ranked"] == 0:
        blocking.append(f"every Empire Builder rank disappeared ({existing['ranked']} -> 0) "
                        f"without the fetch failing; treating the feed as degraded, not as "
                        f"everyone having been unranked at once")
    if existing["zabal"] > 0 and new["zabal"] == 0:
        blocking.append(f"total $ZABAL distributed fell {existing['zabal']} -> 0 without the "
                        f"fetch failing; rewards already paid cannot unpay")

    return blocking


def _selftest_offchain() -> bool:
    """Network-free proof that load_offchain_credits reads a wallets CSV via
    org.config.json's offchain_credits, and that the result correctly
    additively merges into addr_score (the R4 fix)."""
    import tempfile

    global _CFG
    original_cfg = _CFG
    with tempfile.TemporaryDirectory() as tmp:
        csv_path = REPO_ROOT / f"_selftest_offchain_{Path(tmp).name}.csv"
        csv_path.write_text("address,score\n" + "0x" + "a" * 40 + ",1\n" + "0x" + "b" * 40 + ",1\n")
        _CFG = {"offchain_credits": [{"round": 4, "score": 1, "wallets_csv": csv_path.name, "note": "test"}]}
        try:
            wallets = load_offchain_credits()
            ok_read = len(wallets) == 1 and wallets[0]["wallets"] == ["0x" + "a" * 40, "0x" + "b" * 40]
        finally:
            _CFG = original_cfg
            csv_path.unlink(missing_ok=True)

    # addr_score merge behavior, tested directly against the same formula used in main()
    bounties_by_addr = {"0x" + "a" * 40: {1151}}  # on-chain: 1 bounty
    offchain_score_by_addr = {"0x" + "a" * 40: 1, "0x" + "c" * 40: 1}  # offchain: +1 each

    def addr_score(addr: str) -> int:
        return (len(bounties_by_addr.get(addr, set())) + offchain_score_by_addr.get(addr, 0)) or 1

    a_score = addr_score("0x" + "a" * 40)  # on-chain 1 + offchain 1 = 2
    c_score = addr_score("0x" + "c" * 40)  # on-chain 0 + offchain 1 = 1 (offchain-only wallet)
    ok_merge = a_score == 2 and c_score == 1
    ok = ok_read and ok_merge
    print(f"  {'ok  ' if ok else 'FAIL'} offchain CSV read + score merge (combined={a_score}, offchain-only={c_score})")
    return ok


def _selftest_guard() -> bool:
    """Network-free, disk-free proof that guard_publishable() blocks each way this
    refresh can quietly publish worse data than it found, and that a healthy run
    still sails through. The numbers are the real ones from 2026-08-24:
    34 submitters, 3 accepted claims, 16 ranked, 32.2585 $ZABAL."""
    live = {"submitters": 34, "accepted_claims": 3, "ranked": 16, "zabal": 32.2585}
    cases = [
        ("healthy run publishes",
         dict(new=live, existing=live, degradations=[]), True),
        ("growth publishes",
         dict(new={**live, "submitters": 35}, existing=live, degradations=[]), True),
        ("first ever run publishes with nothing to compare",
         dict(new=live, existing=None, degradations=[]), True),
        ("zero submitters blocked",
         dict(new={**live, "submitters": 0}, existing=live, degradations=[]), False),
        ("a swallowed fetch exception blocks",
         dict(new=live, existing=live, degradations=["EB fetch failed"]), False),
        ("submitters shrinking blocks",
         dict(new={**live, "submitters": 19}, existing=live, degradations=[]), False),
        ("accepted claims un-accepting blocks",
         dict(new={**live, "accepted_claims": 0}, existing=live, degradations=[]), False),
        ("ranks vanishing with no exception blocks",
         dict(new={**live, "ranked": 0}, existing=live, degradations=[]), False),
        ("rewards zeroing with no exception blocks",
         dict(new={**live, "zabal": 0}, existing=live, degradations=[]), False),
        ("--allow-shrink permits a deliberate removal",
         dict(new={**live, "submitters": 33}, existing=live, degradations=[], allow_shrink=True), True),
        ("--allow-shrink does NOT permit an upstream outage",
         dict(new={**live, "ranked": 0}, existing=live, degradations=[], allow_shrink=True), False),
    ]
    ok = True
    for label, kwargs, should_publish in cases:
        blocking = guard_publishable(**kwargs)
        passed = (not blocking) == should_publish
        ok = ok and passed
        print(f"  {'ok  ' if passed else 'FAIL'} {label}"
              + (f" ({blocking[0]})" if blocking and not passed else ""))
    return ok


def _selftest() -> int:
    """Network-free proof that fetch_accepted_map follows the tRPC cursor,
    merges pages, and degrades to {} (not a crash) when tRPC fails; that the
    chain-slug guard rejects unknown chains; and that offchain round credits
    merge additively into addr_score.
    Run: python3 scripts/refresh-poidh-leaderboard.py --selftest"""
    global trpc
    pages = [
        {"items": [{"id": 1, "isAccepted": False, "onChainId": 10},
                   {"id": 2, "isAccepted": True, "onChainId": 11}], "nextCursor": "c1"},
        {"items": [{"id": 3, "isAccepted": False, "onChainId": 12}], "nextCursor": None},
    ]
    calls = {"n": 0}

    def fake_trpc(proc: str, payload: dict) -> dict:
        i = calls["n"]
        calls["n"] += 1
        if i == 0:
            assert "cursor" not in payload, "page 1 must not send a cursor"
        else:
            assert payload.get("cursor") == "c1", "page 2 must thread the returned cursor"
        return pages[i]

    original = trpc
    trpc = fake_trpc
    try:
        amap = fetch_accepted_map(1, DEFAULT_CHAIN_ID)
    finally:
        trpc = original
    ok_map = (calls["n"] == 2 and sorted(amap) == [1, 2, 3]
              and amap[2] == {"accepted": True, "on_chain_id": 11}
              and amap[1]["accepted"] is False)
    print(f"  {'ok  ' if ok_map else 'FAIL'} accepted map paginated: {len(amap)} claims in {calls['n']} calls, winner flagged")

    def broken_trpc(proc: str, payload: dict) -> dict:
        raise RuntimeError("tRPC gone")

    trpc = broken_trpc
    try:
        degraded = fetch_accepted_map(1, DEFAULT_CHAIN_ID)
    finally:
        trpc = original
    ok_degrade = degraded == {}
    print(f"  {'ok  ' if ok_degrade else 'FAIL'} tRPC failure degrades to empty map (accepted=false), not a crash")

    try:
        fetch_bounty_data(1, chain=999999)
        ok_slug = False
    except SystemExit:
        ok_slug = True
    print(f"  {'ok  ' if ok_slug else 'FAIL'} unknown chain id rejected before any network call")

    ok_offchain = _selftest_offchain()
    ok_guard = _selftest_guard()

    ok = ok_map and ok_degrade and ok_slug and ok_offchain and ok_guard
    print(f"selftest: {'passed' if ok else 'FAILED'}")
    return 0 if ok else 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true", help="run the pagination self-test (no network) and exit")
    p.add_argument("--bounty", type=int, action="append", default=None)
    p.add_argument("--chain", type=int, default=DEFAULT_CHAIN_ID)
    p.add_argument("--skip-web3bio", action="store_true", help="Skip web3.bio profile fetches (faster but no avatars/X)")
    p.add_argument("--allow-shrink", action="store_true",
                   help="Permit this run to publish fewer submitters or fewer accepted claims "
                        "than the files on disk. Only for deliberate corrections; the guard "
                        "exists because a shrink is otherwise always a broken upstream.")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    bounty_ids = args.bounty if args.bounty else DEFAULT_BOUNTY_IDS

    issuers: set[str] = set()
    seen: set[str] = set()
    unique_order: list[str] = []
    bounty_meta: list[dict] = []
    all_claims: list[dict] = []
    total_eth = 0.0
    total_claims = 0
    rejected_claims: list[dict] = []
    # Track which bounties each address submitted to (for score = bounty count)
    bounties_by_addr: dict[str, set[int]] = {}
    # Track unique (bounty_id, issuer) pairs to detect & reject duplicates
    seen_submissions: set[tuple[int, str]] = set()

    # farcaster/twitter handles the /data endpoint resolves per claim, keyed by
    # wallet - used to seed profiles so web3.bio is enrichment, not the source
    data_handles_by_addr: dict[str, dict] = {}

    for bid in bounty_ids:
        b = fetch_bounty_data(bid, args.chain)
        issuer = b["issuer"].lower()
        issuers.add(issuer)
        amount_eth = int(b.get("amount", "0") or 0) / 1e18
        total_eth += amount_eth

        items = b.get("claims") or []
        total_claims += len(items)
        accepted_map = fetch_accepted_map(bid, args.chain)

        print(f"Bounty {bid}: '{b['title'][:60]}' - {len(items)} claims, {amount_eth:.4f} ETH")

        for c in items:
            claim_id = c.get("claimId")
            claim_issuer = c.get("issuerAddress")

            # Validation: issuer field must exist and be a valid address
            if not claim_issuer:
                rejected_claims.append({
                    "claim_id": claim_id,
                    "bounty_id": bid,
                    "reason": "missing issuer field",
                })
                continue

            addr = claim_issuer.lower()

            # Validation: issuer must be a valid Ethereum address
            if not validate_claim_address(addr):
                rejected_claims.append({
                    "claim_id": claim_id,
                    "bounty_id": bid,
                    "reason": f"invalid issuer address format: {addr}",
                    "issuer": addr,
                })
                continue

            # Validation: reject if issuer is the bounty issuer (PoidhV3 enforces this on-chain)
            if addr == issuer:
                rejected_claims.append({
                    "claim_id": claim_id,
                    "bounty_id": bid,
                    "issuer": addr,
                    "reason": "issuer cannot claim their own bounty",
                })
                continue

            # Deduplication: reject if this (bounty, issuer) pair already submitted
            submission_key = (bid, addr)
            if submission_key in seen_submissions:
                rejected_claims.append({
                    "claim_id": claim_id,
                    "bounty_id": bid,
                    "issuer": addr,
                    "reason": "duplicate submission to same bounty",
                })
                continue

            # Claim passed all validation; include it
            seen_submissions.add(submission_key)
            bounties_by_addr.setdefault(addr, set()).add(bid)
            if addr not in seen:
                seen.add(addr)
                unique_order.append(addr)
            if c.get("farcasterHandle") or c.get("twitterHandle"):
                data_handles_by_addr.setdefault(addr, {
                    "farcaster": c.get("farcasterHandle"),
                    "twitter": c.get("twitterHandle"),
                })
            acc = accepted_map.get(claim_id, {})
            all_claims.append({
                "bounty_id": bid,
                "claim_id": claim_id,
                "issuer": addr,
                "title": (c.get("title") or ""),
                "description": (c.get("description") or ""),
                "image_url": c.get("imageUrl") or "",
                "accepted": bool(acc.get("accepted")),
                "on_chain_id": acc.get("on_chain_id"),
            })

        bounty_meta.append({
            "id": bid,
            "chainId": args.chain,
            "title": b["title"],
            "description": (b.get("description") or "")[:500],
            "issuer": issuer,
            "album": b.get("extra", {}).get("album"),
            "amount_eth": amount_eth,
            "in_progress": bool(b.get("inProgress")),
            "is_voting": bool(b.get("isVoting")),
            "is_canceled": bool(b.get("isCanceled")),
            "claims_count": sum(1 for c in all_claims if c["bounty_id"] == bid),
        })

    offchain_credits = load_offchain_credits()
    offchain_score_by_addr: dict[str, int] = {}
    offchain_notes_by_addr: dict[str, list[str]] = {}
    for credit in offchain_credits:
        print(f"Offchain credit round {credit['round']}: {len(credit['wallets'])} wallets, +{credit['score']} each")
        for addr in credit["wallets"]:
            offchain_score_by_addr[addr] = offchain_score_by_addr.get(addr, 0) + credit["score"]
            offchain_notes_by_addr.setdefault(addr, []).append(credit["note"])
            if addr not in seen:
                seen.add(addr)
                unique_order.append(addr)

    # Score = number of distinct BCZ bounties this wallet submitted to on-chain
    # (capped at len(bounty_ids), so e.g. submitting twice to one bounty still = 1
    # but submitting to both R1 + R2 = 2), per Zaal 2026-05-27 - PLUS any offchain
    # round credit (e.g. R4's flat +1, since its bounty got canceled and the
    # on-chain claim path never happened for those wallets).
    def addr_score(addr: str) -> int:
        return (len(bounties_by_addr.get(addr, set())) + offchain_score_by_addr.get(addr, 0)) or 1

    leaderboard_feed = [{"address": a, "score": addr_score(a)} for a in unique_order]

    print(f"\nFetching live EB leaderboard...")
    eb = fetch_eb_leaderboard()
    eb_entries = eb.get("entries") or []
    eb_by_addr = {e["address"].lower(): e for e in eb_entries}
    print(f"  EB entries: {len(eb_entries)}, total ZABAL distributed so far: "
          f"{sum(e.get('totalRewards', 0) for e in eb_entries):.2f}")

    print(f"\nResolving submitter profiles via web3.bio...")
    profiles: dict[str, dict] = {}
    web3bio_misses = 0
    if not args.skip_web3bio:
        for addr in unique_order:
            row = fetch_web3_bio(addr)
            if row:
                profiles[addr] = {
                    "handle": row.get("identity"),
                    "displayName": row.get("displayName"),
                    "avatar": row.get("avatar"),
                    "description": row.get("description"),
                    "fid": (row.get("social") or {}).get("uid"),
                    "follower": (row.get("social") or {}).get("follower"),
                    "farcaster_url": (row.get("links", {}).get("farcaster") or {}).get("link"),
                    "twitter_handle": (row.get("links", {}).get("twitter") or {}).get("handle"),
                    "twitter_url": (row.get("links", {}).get("twitter") or {}).get("link"),
                }
                print(f"  {addr[:10]}... -> @{profiles[addr]['handle']}")
            else:
                profiles[addr] = {}
                web3bio_misses += 1
            time.sleep(0.15)
        # A single miss is normal - plenty of wallets have no profile anywhere.
        # Every single one missing is web3.bio being down, and publishing that
        # blanks every avatar and display name on the hub at once.
        if unique_order and web3bio_misses == len(unique_order):
            DEGRADATIONS.append(f"web3.bio returned nothing for all {len(unique_order)} wallets, "
                                f"so every avatar and display name would publish as null")

    enriched_leaderboard: list[dict] = []
    for addr in unique_order:
        eb_e = eb_by_addr.get(addr, {})
        prof = profiles.get(addr, {})
        dh = data_handles_by_addr.get(addr, {})
        enriched_leaderboard.append({
            "address": addr,
            "score": addr_score(addr),
            "rank": eb_e.get("rank"),
            "farcaster_username": eb_e.get("farcaster_username") or dh.get("farcaster") or prof.get("handle"),
            "displayName": prof.get("displayName"),
            "avatar": prof.get("avatar"),
            "twitter_handle": dh.get("twitter") or prof.get("twitter_handle"),
            "twitter_url": prof.get("twitter_url"),
            "fid": prof.get("fid"),
            "boost": eb_e.get("boost"),
            "totalRewards": eb_e.get("totalRewards"),
            "follower": prof.get("follower"),
            "offchain_credit": offchain_score_by_addr.get(addr) or None,
            "offchain_note": " / ".join(offchain_notes_by_addr.get(addr, [])) or None,
        })
    enriched_leaderboard.sort(key=lambda e: (e.get("rank") or 999, e["address"]))

    data_dir = REPO_ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    feed_path = data_dir / "leaderboard.json"
    claims_path = data_dir / "claims.json"
    audit_path = data_dir / "audit.json"

    # Nothing above this line has touched disk, which is the point: all three
    # files are written together or none of them are, so a refused run leaves a
    # consistent last-good set rather than a half-updated one.
    new_summary = summarize(leaderboard_feed, enriched_leaderboard, all_claims, eb_entries)
    existing_summary = summarize_on_disk(feed_path, claims_path, audit_path)
    blocking = guard_publishable(new_summary, existing_summary, DEGRADATIONS,
                                 allow_shrink=args.allow_shrink)
    if blocking:
        print(f"\nERROR: refusing to publish this run over the files in "
              f"{data_dir.relative_to(REPO_ROOT)}/.", file=sys.stderr)
        for reason in blocking:
            print(f"  - {reason}", file=sys.stderr)
        if existing_summary:
            print(f"  on disk now: {existing_summary}", file=sys.stderr)
        print(f"  this run:    {new_summary}", file=sys.stderr)
        print("The last good data stays on main. Re-run when upstream recovers.", file=sys.stderr)
        return 1

    feed_path.write_text(json.dumps(leaderboard_feed, indent=2) + "\n")

    claims_path.write_text(json.dumps({
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "empire": {
            "token_address": ZABAL_EMPIRE_ID,
            "leaderboard_uuid": POIDH_LEADERBOARD_UUID,
            "leaderboard_name": (eb.get("leaderboard") or {}).get("name"),
            "leaderboard_url": f"https://empirebuilder.world/empire/{ZABAL_EMPIRE_ID}",
            "last_eb_refresh": (eb.get("leaderboard") or {}).get("last_refreshed_at"),
            "apply_boosters": (eb.get("leaderboard") or {}).get("apply_boosters", False),
            "apply_reputation_boosters": (eb.get("leaderboard") or {}).get("apply_reputation_boosters", False),
            "apply_staking_boosters": (eb.get("leaderboard") or {}).get("apply_staking_boosters", False),
        },
        "totals": {
            "bounties": len(bounty_meta),
            "claims": total_claims,
            "unique_submitters": len(enriched_leaderboard),
            "total_eth_escrow": round(total_eth, 6),
            "total_zabal_distributed": round(sum(e.get("totalRewards", 0) or 0 for e in eb_entries), 4),
        },
        "bounties": bounty_meta,
        "offchain_credits": [
            {
                "round": c["round"],
                "score": c["score"],
                "wallet_count": len(c["wallets"]),
                "note": c["note"],
            }
            for c in offchain_credits
        ],
        "leaderboard": enriched_leaderboard,
        "claims": all_claims,
    }, indent=2) + "\n")

    audit_path.write_text(json.dumps({
        "bounty_ids": bounty_ids,
        "chainId": args.chain,
        "issuers": sorted(issuers),
        "total_claims_received": total_claims,
        "total_claims_accepted": len(all_claims),
        "total_claims_rejected": len(rejected_claims),
        "submitter_count": len(enriched_leaderboard),
        "total_eth_escrow": round(total_eth, 6),
        "bounties": bounty_meta,
        "claims": all_claims,
        "rejected_claims": rejected_claims,
    }, indent=2) + "\n")

    print(f"\nWrote {feed_path.relative_to(REPO_ROOT)} (EB feed): {len(leaderboard_feed)} entries")
    print(f"Wrote {claims_path.relative_to(REPO_ROOT)} (rich page data): {len(enriched_leaderboard)} submitters, {len(all_claims)} accepted claims")
    print(f"Wrote {audit_path.relative_to(REPO_ROOT)} (audit trail: {len(all_claims)} accepted, {len(rejected_claims)} rejected)")
    if rejected_claims:
        print(f"\nRejected claims ({len(rejected_claims)}):")
        for r in rejected_claims:
            print(f"  Claim {r.get('claim_id')}: {r['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
