#!/usr/bin/env python3
"""Refresh data/rounds-live.json: the live on-chain state of every round in
org.config.json, via the same merged lookup query-bounty.py uses.

Why: round status used to live in hand-edited HTML and README tables, which is
how bounty 1249 sat marked "LIVE" for six weeks after it was canceled. This
file is regenerated on the 6h workflow and /about renders from it.

    python3 scripts/refresh-rounds.py          # writes data/rounds-live.json
"""
from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# query-bounty.py has a hyphen, so import it by path.
_spec = importlib.util.spec_from_file_location("query_bounty", ROOT / "scripts" / "query-bounty.py")
qb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(qb)


def status_of(b: dict) -> str:
    winner = next((c for c in b["claims"] if c.get("isAccepted")), None)
    if b["isCanceled"]:
        return "CANCELED"
    if winner:
        return "WINNER SET"
    if b["isVoting"]:
        return "VOTING"
    if b["inProgress"]:
        return "OPEN"
    return "CLOSED"


def main() -> int:
    cfg = json.loads((ROOT / "org.config.json").read_text())
    chain = cfg.get("default_chain_id", 8453)
    out = []
    for r in cfg.get("rounds", []):
        b = qb.fetch_bounty_merged(r["bounty_id"], chain)
        if not b:
            out.append({"round": r["round"], "bounty_id": r["bounty_id"], "title": r["title"], "status": "UNKNOWN", "error": "fetch failed"})
            print(f"  R{r['round']} ({r['bounty_id']}): fetch failed")
            continue
        winner = next((c for c in b["claims"] if c.get("isAccepted")), None)
        entry = {
            "round": r["round"],
            "bounty_id": r["bounty_id"],
            "title": r["title"],
            "bounty_title": b["title"],
            "url": b["url"],
            "status": status_of(b),
            "amount_native": int(b["amount_wei"] or 0) / 1e18,
            "amount_usd": b.get("priceUsd"),
            "claims": len(b["claims"]),
            "winner": {
                "claim_id": winner["claimId"],
                "handle": winner.get("farcasterHandle") or winner.get("twitterHandle"),
                "wallet": winner.get("issuerAddress"),
            } if winner else None,
            "offchain": bool(r.get("offchain")),
            "offchain_note": r.get("offchain_note"),
        }
        out.append(entry)
        print(f"  R{r['round']} ({r['bounty_id']}): {entry['status']}, {entry['claims']} claims" + (f", winner @{entry['winner']['handle']}" if winner else ""))
    for r in cfg.get("planned_rounds", []):
        out.append({"round": r["round"], "title": r["title"], "status": "DRAFT", "folder": r.get("folder")})
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "chain_id": chain,
        "note": "Live on-chain state per round, from poidh's /data endpoint merged with claims.fetchBountyClaims (see scripts/query-bounty.py). Regenerated every 6h.",
        "rounds": out,
    }
    dest = ROOT / "data" / "rounds-live.json"
    dest.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Wrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
