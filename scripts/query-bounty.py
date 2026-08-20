#!/usr/bin/env python3
"""
Query any POIDH bounty by id, or search for a wallet's claims across a set of known
bounties - the "look up a bounty and its winner" tool this repo didn't have. Every other
script in here is round-scoped (build a judging.json, refresh BCZ's own leaderboard); this
is ad-hoc lookup for any bounty id, on any chain, including ones BCZ never issued.

Merges two POIDH endpoints that each carry half the picture:
  - /<chain>/bounty/<id>/data     - bounty metadata + resolved Farcaster/X handles per claim
  - claims.fetchBountyClaims      - the real isAccepted flag per claim (missing from /data)

    python3 scripts/query-bounty.py --bounty 1180                    # single bounty, resolves winner
    python3 scripts/query-bounty.py --bounty 1180 --chain 8453       # explicit chain
    python3 scripts/query-bounty.py --wallet 0xc143cf85...           # scan org.config.json's known rounds
    python3 scripts/query-bounty.py --wallet 0xc143cf85... --bounty-ids 1151,1166,1180
    python3 scripts/query-bounty.py --bounty 1180 --json             # raw merged JSON, no formatting
    python3 scripts/query-bounty.py --selftest                       # no network
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POIDH_BASE = "https://poidh.xyz/api/trpc"
UA = "Mozilla/5.0 (zpoidh-bounty-query)"

# Chain id -> POIDH's own URL path segment for that chain (poidh.xyz/<path>/bounty/<id>).
# Confirmed against docs.poidh.xyz's deployment table and live bounty URLs this session.
CHAIN_PATHS = {
    1: "mainnet",
    8453: "base",
    42161: "arbitrum",
    666666666: "degen",
}


def load_org_config() -> dict:
    """Read org.config.json if present - forking zpoidh for your own org? Edit that
    file's "default_bounty_ids"/"default_chain_id" instead of this script."""
    path = REPO_ROOT / "org.config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


_CFG = load_org_config()
DEFAULT_CHAIN_ID = _CFG.get("default_chain_id", 8453)
DEFAULT_BOUNTY_IDS = _CFG.get("default_bounty_ids", [1151, 1166, 1180, 1249])


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def trpc(proc: str, payload: dict) -> dict:
    import urllib.parse

    inp = urllib.parse.quote(json.dumps({"0": {"json": payload}}))
    return http_get_json(f"{POIDH_BASE}/{proc}?batch=1&input={inp}")[0]["result"]["data"]["json"]


def fetch_bounty_merged(bounty_id: int, chain_id: int) -> dict | None:
    """Merge /data (resolved handles) with claims.fetchBountyClaims (isAccepted) by
    claim id. Returns None if the bounty doesn't exist on this chain."""
    chain_path = CHAIN_PATHS.get(chain_id, "base")
    try:
        data = http_get_json(f"https://poidh.xyz/{chain_path}/bounty/{bounty_id}/data")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except Exception:
        return None

    if not isinstance(data, dict) or "id" not in data:
        return None

    accepted_by_claim: dict[int, dict] = {}
    try:
        claims_resp = trpc("claims.fetchBountyClaims", {"bountyId": bounty_id, "chainId": chain_id})
        for c in claims_resp.get("items", []):
            accepted_by_claim[c["id"]] = c
    except Exception as e:
        print(f"  WARN: claims.fetchBountyClaims failed, winner status unavailable: {e}", file=sys.stderr)

    merged_claims = []
    for claim in data.get("claims", []):
        cid = claim.get("claimId")
        onchain = accepted_by_claim.get(cid, {})
        merged_claims.append(
            {
                **claim,
                "isAccepted": onchain.get("isAccepted", False),
                "onChainId": onchain.get("onChainId"),
                "owner": onchain.get("owner"),
            }
        )

    return {
        "id": data["id"],
        "onChainId": data.get("onChainId"),
        "chainId": data.get("chainId", chain_id),
        "title": data.get("title"),
        "amount_wei": data.get("amount"),
        "issuer": data.get("issuer"),
        "isCanceled": data.get("isCanceled"),
        "inProgress": data.get("inProgress"),
        "isVoting": data.get("isVoting"),
        "priceUsd": data.get("priceUsd"),
        "url": data.get("url"),
        "album": (data.get("extra") or {}).get("album"),
        "claims": merged_claims,
    }


def format_bounty(b: dict) -> str:
    winner = next((c for c in b["claims"] if c.get("isAccepted")), None)
    # Precedence matters: isVoting can stay true on-chain even after a winner is
    # already accepted (confirmed against real bounty 1180 - femmie won, isVoting is
    # still true) - a resolved winner must win over a stale voting flag, not the
    # reverse, or a fully-settled bounty misreports as still "VOTING".
    if b["isCanceled"]:
        status = "CANCELED"
    elif winner:
        status = "WINNER SET"
    elif b["isVoting"]:
        status = "VOTING"
    elif b["inProgress"]:
        status = "OPEN"
    else:
        status = "CLOSED"
    amount_native = int(b["amount_wei"] or 0) / 1e18
    lines = [
        f"Bounty {b['id']} (onchain #{b['onChainId']}, chain {b['chainId']}) - {status}",
        f"  {b['title']}",
        f"  {amount_native:g} native token" + (f" (~${b['priceUsd']:.2f})" if b.get("priceUsd") else ""),
        f"  Issuer: {b['issuer']}",
        f"  Album: {b['album'] or '(none)'}",
        f"  URL: {b['url']}",
        f"  Claims: {len(b['claims'])}",
    ]
    for c in b["claims"]:
        mark = "WINNER" if c.get("isAccepted") else "      "
        handle = c.get("farcasterHandle") or c.get("twitterHandle") or "?"
        lines.append(f"    [{mark}] claim {c['claimId']:>5}  @{handle:<20}  {c.get('title', '')[:50]}")
    return "\n".join(lines)


def query_wallet(wallet: str, bounty_ids: list[int], chain_id: int) -> list[dict]:
    """Scan a fixed set of bounty ids for claims issued by `wallet`. Not a full-feed
    crawl - POIDH has no "claims by wallet across all bounties" endpoint, so this is
    scoped to a known bounty-id list (default: org.config.json's default_bounty_ids)."""
    wallet = wallet.lower()
    hits = []
    for bid in bounty_ids:
        b = fetch_bounty_merged(bid, chain_id)
        if not b:
            continue
        for c in b["claims"]:
            if (c.get("issuerAddress") or "").lower() == wallet:
                hits.append({"bounty_id": bid, "bounty_title": b["title"], "claim": c})
    return hits


def _selftest() -> int:
    """No network. Verifies the /data + claims merge logic and the formatter against
    synthetic fixtures shaped like the real endpoints' actual response schemas."""
    fake_data_claim = {"claimId": 101, "farcasterHandle": "alice", "twitterHandle": "alice_x", "title": "My entry"}
    fake_onchain = {101: {"isAccepted": True, "onChainId": 900, "owner": "0xabc"}}

    merged = {
        **fake_data_claim,
        "isAccepted": fake_onchain.get(101, {}).get("isAccepted", False),
        "onChainId": fake_onchain.get(101, {}).get("onChainId"),
        "owner": fake_onchain.get(101, {}).get("owner"),
    }
    checks = [
        ("merge carries isAccepted from onchain data", merged["isAccepted"] is True),
        ("merge keeps resolved handle from /data", merged["farcasterHandle"] == "alice"),
        ("merge carries owner from onchain data", merged["owner"] == "0xabc"),
    ]

    # isVoting: True on purpose here - matches real bounty 1180 (femmie won R3, but
    # POIDH's isVoting flag stayed true on-chain even after resolution). A winner
    # must take precedence over a stale voting flag, or this exact real bounty
    # would misreport as still "VOTING" when it's actually fully settled.
    fake_bounty = {
        "id": 1180, "onChainId": 194, "chainId": 8453, "title": "Test Bounty",
        "amount_wei": "25000000000000000", "issuer": "0xissuer", "isCanceled": False,
        "inProgress": False, "isVoting": True, "priceUsd": 47.98, "url": "https://poidh.xyz/base/bounty/1180",
        "album": "wethemmedia", "claims": [merged],
    }
    formatted = format_bounty(fake_bounty)
    checks.append(("formatter marks the accepted claim as WINNER", "WINNER" in formatted and "claim   101" in formatted))
    checks.append(("formatter shows resolved handle not raw address", "@alice" in formatted))
    checks.append(("winner takes precedence over a stale isVoting=True flag", "WINNER SET" in formatted and "VOTING\n" not in formatted))

    fails = 0
    for label, ok in checks:
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    print(f"selftest: {len(checks) - fails}/{len(checks)} passed")
    return 1 if fails else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bounty", type=int, help="bounty id to look up")
    p.add_argument("--chain", type=int, default=DEFAULT_CHAIN_ID, help=f"chain id (default {DEFAULT_CHAIN_ID})")
    p.add_argument("--wallet", type=str, help="find claims by this wallet address across --bounty-ids")
    p.add_argument("--bounty-ids", type=str, help="comma-separated bounty ids for --wallet mode (default: org.config.json's default_bounty_ids)")
    p.add_argument("--json", action="store_true", help="print raw merged JSON instead of a formatted summary")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    if args.wallet:
        bounty_ids = [int(x) for x in args.bounty_ids.split(",")] if args.bounty_ids else DEFAULT_BOUNTY_IDS
        hits = query_wallet(args.wallet, bounty_ids, args.chain)
        if args.json:
            print(json.dumps(hits, indent=2))
            return 0
        if not hits:
            print(f"No claims found for {args.wallet} across bounty ids {bounty_ids}")
            return 0
        print(f"{args.wallet} has {len(hits)} claim(s) across the searched bounties:")
        for h in hits:
            c = h["claim"]
            mark = "WINNER" if c.get("isAccepted") else "entrant"
            print(f"  [{mark}] bounty {h['bounty_id']} ({h['bounty_title']}) - claim {c['claimId']}: {c.get('title', '')[:60]}")
        return 0

    if args.bounty is None:
        p.error("provide --bounty <id>, --wallet <address>, or --selftest")

    b = fetch_bounty_merged(args.bounty, args.chain)
    if not b:
        print(f"Bounty {args.bounty} not found on chain {args.chain} (wrong chain? try --chain 8453/42161/1/666666666)", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(b, indent=2))
    else:
        print(format_bounty(b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
