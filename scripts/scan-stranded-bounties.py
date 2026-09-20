#!/usr/bin/env python3
"""The bounties poidh cannot show you, and the call that unsticks each one.

WHAT THIS IS. poidh's app reads one contract per chain. Funded, open bounties on the
PRE-V3 contracts are invisible to it: not in the UI, not in `bounties.fetchAll`. Reported
upstream as poidh-app issue #1459 on 2026-08-28, still open with no replies as of
2026-09-20. This reads those contracts directly and writes what it finds.

WHY IT MATTERS MORE THAN THE MONEY. Measured 2026-09-20 on Base: of 201 stranded bounties,
96 already carry submitted work - 492 claims from 306 distinct wallets. 90% of the locked
value sits on bounties where somebody already did the job. It is not abandoned money, it is
unpaid work, and neither side can see the other.

AND IT IS RECOVERABLE. The contract's own escape hatches all worked in production before it
went quiet on 2026-04-21: `acceptClaim` pays a claimant, `cancelOpenBounty` refunds the
issuer. Both are direct calls. So this tool exists to end the situation, not to catalogue
it - which is why every row carries the call that resolves it.

THE TENSION THIS DATA CREATES, STATED ON PURPOSE. Cancelling refunds the issuer and leaves
the claimants with nothing, which is exactly the outcome 306 people are already living
with. Any surface built on this file should show an issuer their claimants BEFORE it shows
them the refund button.

PRIVACY. Zaal's call, 2026-09-20: aggregate figures are public, per-wallet detail is
lookup-only. This file carries addresses because it has to for a lookup to work; a page
built on it must not render a public roster of people with unpaid work. That is theirs to
disclose, not ours.

    python3 scripts/scan-stranded-bounties.py           # writes data/stranded.json
    python3 scripts/scan-stranded-bounties.py --selftest # offline
"""
from __future__ import annotations

import argparse
import json
from decimal import Decimal
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (zpoidh-stranded-scan)"

# Selectors, from `cast sig`. bounties(uint256) returns
# (id, issuer, name, description, amount, claimer, createdAt) - claimer zero means open,
# amount nonzero means funded, and createdAt IS on chain here even though the v3 API
# returns it empty on every live bounty.
SEL_BOUNTY = "0xdc2f8744"   # bounties(uint256)
SEL_CLAIMS = "0x3e1d5cc8"   # getClaimsByBountyId(uint256)
SEL_LENGTH = "getBountiesLength()"

# Only the chains whose contracts can actually be read. Degen is deliberately absent:
# on 2026-09-20 six public endpoints across five providers could not execute a call
# (rpc.degen.tips gave Cloudflare 1016; thirdweb answered eth_chainId from static config
# and then failed eth_call, eth_blockNumber and eth_getBalance alike). Its 225 bounties and
# 10,044 DEGEN are UNREAD, not absent - and a scanner that silently omitted them would
# publish a total that looks complete.
CONTRACTS = [
    {"chain": "base", "chain_id": 8453, "n": 990,
     "address": "0xb502c5856f7244dccdd0264a541cc25675353d39",
     "rpcs": ["https://base-rpc.publicnode.com", "https://mainnet.base.org"]},
    {"chain": "arbitrum", "chain_id": 42161, "n": 180,
     "address": "0x0Aa50ce0d724cc28f8F7aF4630c32377B4d5c27d",
     "rpcs": ["https://arb1.arbitrum.io/rpc", "https://arbitrum-one-rpc.publicnode.com"]},
]

UNREAD_CHAINS = [
    {"chain": "degen", "chain_id": 666666666, "contracts": 4,
     "reason": "six public endpoints across five providers could not execute eth_call on "
               "2026-09-20; see ZAOOS research doc business/2522-poidh-live-bounty-market"},
]


def rpc_batch(rpcs: list[str], addr: str, sel: str, ids: list[int], tries: int = 6) -> list[dict]:
    """Batched eth_call. Raises rather than returning short - a partial read that looks
    complete is the failure this whole file exists to document."""
    reqs = [{"jsonrpc": "2.0", "id": i, "method": "eth_call",
             "params": [{"to": addr, "data": sel + format(i, "064x")}, "latest"]} for i in ids]
    body = json.dumps(reqs).encode()
    last = ""
    for a in range(tries):
        rpc = rpcs[a % len(rpcs)]
        try:
            req = urllib.request.Request(
                rpc, body, {"Content-Type": "application/json", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as f:
                out = json.loads(f.read())
            if isinstance(out, list) and len(out) == len(ids):
                return out
            last = f"{rpc} returned {type(out).__name__} of {len(out) if hasattr(out,'__len__') else '?'}"
        except Exception as e:
            last = f"{rpc}: {type(e).__name__}"
        time.sleep(1.5 * (a + 1))
    raise RuntimeError(f"RPC batch failed after {tries} tries ({last})")


def words(hexstr: str) -> list[str]:
    raw = hexstr[2:]
    return [raw[i:i + 64] for i in range(0, len(raw), 64)]


def parse_bounty(res: str) -> dict | None:
    w = words(res)
    if len(w) < 7:
        return None
    return {"amount": int(w[4], 16), "claimer": int(w[5], 16),
            "issuer": "0x" + w[1][-40:], "created_at": int(w[6], 16)}


def parse_claims(res: str) -> list[str]:
    """Claimant addresses. Element layout confirmed against word 2, which carries the
    bounty id and matched the queried bounty on every element read on 2026-09-20."""
    w = words(res)
    if len(w) < 2:
        return []
    n = int(w[1], 16)
    out = []
    for e in range(n):
        try:
            start = 2 + int(w[2 + e], 16) // 32
            out.append("0x" + w[start + 1][-40:])
        except (IndexError, ValueError):
            continue
    return out


def recovery_call(has_claims: bool) -> dict:
    """What the issuer can actually do about it today. Claimants first, on purpose."""
    if has_claims:
        return {
            "primary": "acceptClaim(bountyId, claimId)",
            "primary_effect": "pays the person who did the work",
            "secondary": "cancelOpenBounty(bountyId)",
            "secondary_effect": "refunds you and leaves every claimant with nothing",
        }
    return {
        "primary": "cancelOpenBounty(bountyId)",
        "primary_effect": "refunds you; nobody has entered this one",
        "secondary": None, "secondary_effect": None,
    }


def scan() -> dict:
    chains = []
    for c in CONTRACTS:
        stranded = {}
        ids = list(range(c["n"]))
        for s in range(0, len(ids), 60):
            for it in rpc_batch(c["rpcs"], c["address"], SEL_BOUNTY, ids[s:s + 60]):
                res = it.get("result")
                if not res:
                    continue
                b = parse_bounty(res)
                if b and b["claimer"] == 0 and b["amount"] > 0:
                    stranded[it["id"]] = b
            time.sleep(0.25)

        claims = {}
        sids = list(stranded)
        for s in range(0, len(sids), 25):
            for it in rpc_batch(c["rpcs"], c["address"], SEL_CLAIMS, sids[s:s + 25]):
                res = it.get("result")
                if not res:
                    continue
                cl = parse_claims(res)
                if cl:
                    claims[it["id"]] = cl
            time.sleep(0.25)

        rows = []
        for bid, b in sorted(stranded.items()):
            cl = claims.get(bid, [])
            rows.append({
                "bounty_id": bid, "chain": c["chain"], "chain_id": c["chain_id"],
                "contract": c["address"], "amount_wei": str(b["amount"]),
                "amount_eth": str(Decimal(b["amount"]).scaleb(-18)),
                "issuer": b["issuer"],
                "created_at": datetime.fromtimestamp(b["created_at"], timezone.utc).date().isoformat()
                if b["created_at"] else None,
                "claim_count": len(cl), "claimants": cl,
                "recovery": recovery_call(bool(cl)),
            })
        chains.append({
            "chain": c["chain"], "chain_id": c["chain_id"], "contract": c["address"],
            "ids_read": len(ids), "stranded": len(rows), "bounties": rows,
        })
    return {"chains": chains, "unread": UNREAD_CHAINS}


def totals(data: dict) -> dict:
    rows = [b for c in data["chains"] for b in c["bounties"]]
    wei = sum(int(b["amount_wei"]) for b in rows)
    withwork = [b for b in rows if b["claim_count"]]
    people = {a for b in rows for a in b["claimants"]}
    return {
        "stranded_bounties": len(rows),
        "with_work_submitted": len(withwork),
        "total_claims": sum(b["claim_count"] for b in rows),
        "distinct_claimants": len(people),
        "distinct_issuers": len({b["issuer"] for b in rows}),
        "eth_stranded": str(Decimal(wei).scaleb(-18)),
        "eth_on_bounties_with_work":
            str(Decimal(sum(int(b["amount_wei"]) for b in withwork)).scaleb(-18)),
        "chains_unread": [u["chain"] for u in data["unread"]],
    }


def _selftest() -> bool:
    passed = True

    def check(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    # A real payload shape: offset, length 2, then two element offsets.
    body = ("0x" + format(32, "064x") + format(2, "064x")
            + format(64 + 0, "064x") + format(64 + 6 * 32, "064x")
            + "".join([format(5271, "064x"), format(int("ff83b00e1a8707d4831305524cdc13ff12ddf1b2", 16), "064x"),
                       format(975, "064x"), format(0, "064x"), format(256, "064x"), format(320, "064x")])
            + "".join([format(5274, "064x"), format(int("8dbab1f53609b3f40241557ad0bf3d76275db485", 16), "064x"),
                       format(975, "064x"), format(0, "064x"), format(256, "064x"), format(352, "064x")]))
    got = parse_claims(body)
    check("parses two claimants out of a real-shaped payload", len(got) == 2)
    check("claimant is word 1, not the claim id",
          got and got[0].endswith("ff83b00e1a8707d4831305524cdc13ff12ddf1b2"))
    check("an empty array yields no claimants",
          parse_claims("0x" + format(32, "064x") + format(0, "064x")) == [])
    check("a truncated payload yields nothing rather than guessing", parse_claims("0x00") == [])

    b = parse_bounty("0x" + "".join([format(1, "064x"), format(2, "064x"), format(0, "064x"),
                                     format(0, "064x"), format(1500, "064x"),
                                     format(0, "064x"), format(1717357263, "064x")]))
    check("open and funded is claimer==0 and amount>0", b["claimer"] == 0 and b["amount"] == 1500)
    check("createdAt is read from word 6", b["created_at"] == 1717357263)

    check("a bounty with work offers acceptClaim FIRST",
          recovery_call(True)["primary"].startswith("acceptClaim"))
    check("and names what cancelling costs the claimants",
          "nothing" in recovery_call(True)["secondary_effect"])
    check("a bounty with no work offers only the refund",
          recovery_call(False)["secondary"] is None)

    fake = {"chains": [{"bounties": [
        {"amount_wei": "1000000000000000000", "claim_count": 2, "claimants": ["0xa", "0xb"], "issuer": "0xi"},
        {"amount_wei": "0", "claim_count": 0, "claimants": [], "issuer": "0xi"}]}],
        "unread": [{"chain": "degen"}]}
    t = totals(fake)
    check("totals count distinct people, not claims",
          t["distinct_claimants"] == 2 and t["total_claims"] == 2)
    check("totals count distinct issuers", t["distinct_issuers"] == 1)
    check("unread chains are carried into the totals, not dropped",
          t["chains_unread"] == ["degen"])
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("scan-stranded-bounties selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    data = scan()
    t = totals(data)
    if t["stranded_bounties"] == 0:
        print("Refusing to write: zero stranded bounties found across every readable "
              "contract. That is either a fixed platform or a broken scan, and this tool "
              "cannot tell which. Check the contracts by hand before believing it.")
        return 1

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": ("Funded, open bounties on poidh's pre-v3 contracts, which poidh's own app "
                 "does not read. Upstream: poidh-app issue #1459. Per-wallet detail is for "
                 "lookup by the wallet's owner, not for public listing."),
        "totals": t,
        "unread_chains": data["unread"],
        "chains": data["chains"],
    }
    path = REPO_ROOT / "data" / "stranded.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"{t['stranded_bounties']} stranded bounties, {t['with_work_submitted']} with work "
          f"already submitted")
    print(f"{t['total_claims']} claims from {t['distinct_claimants']} people, across "
          f"{t['distinct_issuers']} issuers")
    print(f"{t['eth_stranded']} ETH stranded, {t['eth_on_bounties_with_work']} of it on "
          f"bounties where the work is done")
    print(f"UNREAD: {', '.join(t['chains_unread']) or 'none'}")
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
