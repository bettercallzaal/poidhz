#!/usr/bin/env python3
"""Print every claim on a bounty, in the shape a write-up needs, with its read timestamp.

Built 2026-09-21 for the Day 264 edition, which became a REVIEW of what people submitted to
bounty one rather than an announcement of it.

WHAT IT CAN AND CANNOT TELL YOU, because a report that blurs the two is how an invented
detail gets published:

  - handle: merged from the bounty's /data endpoint, which resolves wallets to Farcaster or X
    handles. `claims.fetchBountyClaims` does NOT carry one. A wallet with no resolved handle
    prints UNRESOLVED, never a guess.
  - title, description, media url, accepted: straight from the claim record.
  - media type (poster, clip, meme, pitch): INFERRED from the words in the title and
    description, and printed with a `?` so nobody quotes it as fact. poidh stores no type
    field. When it cannot tell, it says UNKNOWN rather than picking the likeliest.
  - the entrant's own public post: only when the claim itself carries a link to one. It is
    often in the title, because poidh's own flow tells entrants to submit their live URL.

    python3 scripts/claim-report.py --bounty 1409
    python3 scripts/claim-report.py --bounty 1409 --json
    python3 scripts/claim-report.py --selftest
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request

CHAIN = 8453
# Ordered: the first match wins, so the more specific words come first.
TYPE_WORDS = [
    ("pitch to camera", "pitch"), ("to camera", "pitch"),
    ("flyer", "flyer"), ("poster", "poster"), ("meme", "meme"),
    ("reel", "clip"), ("video", "clip"), ("clip", "clip"), ("edit", "clip"),
    ("story", "story"), ("carousel", "carousel"), ("graphic", "graphic"),
]


def trpc(proc: str, inp: dict):
    url = f"https://poidh.xyz/api/trpc/{proc}?input=" + urllib.parse.quote(json.dumps({"json": inp}))
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    return json.load(urllib.request.urlopen(req, timeout=30))["result"]["data"]["json"]


def items_of(payload) -> list:
    if isinstance(payload, dict):
        return payload.get("items") or []
    return payload or []


def guess_type(title: str, description: str) -> str:
    """INFERRED, never authoritative. poidh stores no media type."""
    hay = f"{title} {description}".lower()
    for word, label in TYPE_WORDS:
        if word in hay:
            return label
    return "UNKNOWN"


def public_post(claim: dict) -> str | None:
    """The entrant's own public post, if the claim carries a link to one.

    Not the IPFS media url, which is poidh's copy of the file and not a post anyone can see
    in a feed."""
    for field in ("title", "description"):
        m = re.search(r"https?://(?!beige-impossible-dragon)[^\s)]+", claim.get(field) or "")
        if m:
            return m.group(0)
    return None


def handles_for(bounty_id: int, chain: int) -> dict:
    """wallet -> handle, from the bounty page's own data endpoint. Missing is UNRESOLVED."""
    out = {}
    try:
        req = urllib.request.Request(
            f"https://poidh.xyz/{'base' if chain == 8453 else chain}/bounty/{bounty_id}/data",
            headers={"User-Agent": "curl/8"})
        data = json.load(urllib.request.urlopen(req, timeout=30))
    except Exception as e:  # noqa: BLE001 - reported, not swallowed
        print(f"  (handle lookup FAILED: {e}. Every handle will read UNRESOLVED.)")
        return out
    for c in (data.get("claims") or []):
        addr = (c.get("issuerAddress") or c.get("issuer") or "").lower()
        # THE FIELD NAMES MATTER AND THEY ARE NOT THE OBVIOUS ONES. /data calls these
        # farcasterHandle and twitterHandle - the same keys query-bounty.py reads. An earlier
        # version of this file guessed issuerName/farcasterUsername/handle and printed
        # UNRESOLVED for a claimant whose handle query-bounty.py had already resolved.
        name = (c.get("farcasterHandle") or c.get("twitterHandle")
                or c.get("issuerName") or c.get("farcasterUsername") or c.get("handle"))
        if addr and name:
            out[addr] = name if str(name).startswith("@") else f"@{name}"
        # Fall back to keying by claim id, since /data and fetchBountyClaims share those.
        if c.get("claimId") is not None and name:
            out[f"claim:{c['claimId']}"] = name if str(name).startswith("@") else f"@{name}"
    return out


def _selftest() -> bool:
    passed = True

    def check(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    check("reads {items:[...]}", len(items_of({"items": [1]})) == 1)
    check("an empty payload is empty, not a crash", items_of(None) == [])
    check("a flyer is a flyer", guess_type("ZAOstock Oct 3 flyer", "") == "flyer")
    check("more specific words win", guess_type("", "a 15 second pitch to camera") == "pitch")
    check("UNKNOWN rather than a likeliest guess",
          guess_type("my entry", "here is my submission") == "UNKNOWN")
    check("the IPFS media url is NOT treated as a public post",
          public_post({"title": "x", "description":
                       "https://beige-impossible-dragon-883.mypinata.cloud/ipfs/Qm"}) is None)
    check("a real post link IS found",
          public_post({"title": "https://farcaster.xyz/leoxcrane/0xccd0",
                       "description": ""}) == "https://farcaster.xyz/leoxcrane/0xccd0")
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bounty", type=int)
    ap.add_argument("--chain", type=int, default=CHAIN)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("claim-report selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1
    if not args.bounty:
        ap.error("--bounty is required (or use --selftest)")

    stamp = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    claims = items_of(trpc("claims.fetchBountyClaims",
                           {"bountyId": args.bounty, "chainId": args.chain, "limit": 100}))
    handles = handles_for(args.bounty, args.chain)

    rows = []
    for c in claims:
        addr = (c.get("issuer") or "").lower()
        rows.append({
            "claim_id": c.get("id"),
            "handle": handles.get(addr) or handles.get(f"claim:{c.get('id')}")
                      or handles.get(f"claim:{int(c['id'])}" if str(c.get('id','')).isdigit() else "")
                      or "UNRESOLVED",
            "wallet": addr,
            "title": c.get("title"),
            "description": c.get("description"),
            "media_type_INFERRED": guess_type(c.get("title") or "", c.get("description") or ""),
            "public_post": public_post(c),
            "media_url": c.get("url"),
            "is_accepted": c.get("isAccepted"),
        })

    if args.json:
        print(json.dumps({"bounty": args.bounty, "chain": args.chain, "read_at": stamp,
                          "count": len(rows), "claims": rows}, indent=1))
        return 0

    print(f"Bounty {args.bounty} on chain {args.chain} - {len(rows)} claim(s), read {stamp}")
    print("media type is INFERRED from wording; poidh stores no type field\n")
    for r in rows:
        print(f"claim {r['claim_id']}  {r['handle']}  ({r['wallet'][:10]}...)  "
              f"accepted={r['is_accepted']}")
        print(f"   title:  {r['title']}")
        print(f"   desc:   {(r['description'] or '')[:160]}")
        print(f"   type?:  {r['media_type_INFERRED']}")
        print(f"   post:   {r['public_post'] or 'none carried in the claim'}")
        print(f"   media:  {r['media_url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
