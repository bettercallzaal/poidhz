#!/usr/bin/env python3
"""
Generalized POID bounty deadline scanner (zpoidh issue #6, the follow-up beyond BCZ's
own rounds). scripts/build-bounty-calendar.py proved the free-text parsing approach
against 4 known BCZ bounties; this scans the live, platform-wide POID bounty feed
(bounties.fetchAll) so the calendar isn't limited to bounties we already know about.

Confirms Kenny's exact point from the 2026-07-08 fireside: POID's own `deadline` field
on a bounty object is essentially unused - it comes back `null` on real bounties even
when the description explicitly states one ("Submissions close on July 5, 2026").
There genuinely is no structured deadline; the only source of truth is free text.

    python3 scripts/scan-poidh-deadlines.py [--pages 4] [--limit 25] [--status open]

Writes data/poidh-deadlines-global.json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deadline_parser import extract_deadline  # shared free-text deadline parser

REPO_ROOT = Path(__file__).resolve().parent.parent
POIDH_BASE = "https://poidh.xyz/api/trpc"
UA = "Mozilla/5.0 (zpoidh-bounty-deadline-scanner)"


def load_org_config() -> dict:
    """Read org.config.json if present - forking zpoidh for your own org? Edit
    that file's "default_chain_id" instead of this script. Missing file/key
    falls back to Base mainnet (8453), the original hardcoded default."""
    path = REPO_ROOT / "org.config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


_CFG = load_org_config()



def trpc(proc: str, payload: dict) -> dict:
    inp = urllib.parse.quote(json.dumps({"0": {"json": payload}}))
    req = urllib.request.Request(
        f"{POIDH_BASE}/{proc}?batch=1&input={inp}", headers={"User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())[0]["result"]["data"]["json"]




def selftest() -> int:
    from deadline_parser import selftest as _st
    return _st()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true", help="run the deadline-parser self-test and exit")
    p.add_argument("--pages", type=int, default=4, help="how many pages of the live feed to scan")
    p.add_argument("--limit", type=int, default=25, help="bounties per page")
    p.add_argument("--status", default="open", choices=["open", "progress", "past"])
    p.add_argument("--chain", type=int, default=_CFG.get("default_chain_id", 8453))
    args = p.parse_args()

    if args.selftest:
        return selftest()

    now = datetime.now(timezone.utc).date()
    scanned = []
    native_deadline_field_ever_set = 0
    cursor = None

    for page in range(args.pages):
        payload = {"chainId": args.chain, "status": args.status, "limit": args.limit}
        if cursor is not None:
            payload["cursor"] = cursor
        try:
            d = trpc("bounties.fetchAll", payload)
        except Exception as e:
            print(f"  WARN: page {page} fetch failed: {e}")
            break

        items = d.get("items", [])
        if not items:
            break
        cursor = d.get("nextCursor")

        for b in items:
            if b.get("deadline") is not None:
                native_deadline_field_ever_set += 1

            deadline_iso, raw = extract_deadline(b.get("description", ""), created_at=b.get("createdAt"))
            if not deadline_iso:
                continue  # per Kenny's own framing: no stated deadline -> just don't show it

            scanned.append(
                {
                    "bounty_id": b["id"],
                    "title": b.get("title", "")[:120],
                    "issuer": b.get("issuer"),
                    "amount_eth": int(b.get("amount", "0") or 0) / 1e18,
                    "deadline_iso": deadline_iso,
                    "deadline_raw_text": raw,
                    "status": "closed" if deadline_iso < now.isoformat() else "upcoming",
                    "url": f"https://poidh.xyz/base/bounty/{b['id']}",
                }
            )

        if cursor is None:
            break  # fetchAll's nextCursor is absent on the last page - end of feed

        time.sleep(0.3)  # courtesy delay - this is someone else's public API

    scanned.sort(key=lambda e: e["deadline_iso"])

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scan_status": args.status,
        "pages_scanned": args.pages,
        "note": (
            "Generalized scan beyond BCZ's own rounds (see build-bounty-calendar.py for "
            "the BCZ-specific proof of concept). Confirms POID's on-chain/API `deadline` "
            f"field is essentially unused in practice - only {native_deadline_field_ever_set} "
            f"of the bounties scanned had it set at all, even though many describe a clear "
            "deadline in free text. That gap is exactly why this tool exists."
        ),
        "bounties_with_deadline_found": scanned,
    }

    out_path = REPO_ROOT / "data" / "poidh-deadlines-global.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Scanned {args.pages} page(s) of '{args.status}' bounties, found {len(scanned)} with a parseable deadline.")
    print(f"Native 'deadline' field was set on {native_deadline_field_ever_set} bounties out of the scan.")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
