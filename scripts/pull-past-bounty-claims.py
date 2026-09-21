#!/usr/bin/env python3
"""Pull completed poidh bounties on Base with a real claim count for each.

The measurement behind docs/how-bounties-got-shared-2026-09-21.md.

TWO THINGS THIS FILE DOES THAT A NAIVE PULL DOES NOT, BOTH LEARNED THE HARD WAY:

  1. It POSITIVE-CONTROLS the claim counter before trusting a single number. It counts R1
     (bounty 1151) and R5 (bounty 1330), whose claim counts we know independently (11 and
     9), and exits 2 if either is wrong. `bounties.fetchAll` returns only a `hasClaims`
     boolean, and `bounties.fetchByAlbum` returns EMPTY claims arrays - taken at face value
     it once read as "We Them Media got zero claims across 15 bounties". A counter that has
     never been seen returning a known answer is not a counter.

  2. It says what population it measured. `status: past` means COMPLETED bounties, so every
     one of them had claims - 600 of 600 in the 2026-09-21 pull. That is the sample's
     definition, not a finding, and any result drawn from it is about survivors.

    python3 scripts/pull-past-bounty-claims.py            # network; writes data/past-bounties-raw.json
    python3 scripts/pull-past-bounty-claims.py --selftest # offline
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request

OUT = "data/past-bounties-raw.json"   # the committed slim copy is data/past-bounties-2026-09-21.json
CHAIN = 8453
PAGES = 12                            # x 50 = the most recent 600. A cap, and it binds - say so.
CONTROLS = {1151: 11, 1330: 9}        # R1 and R5, known independently


def trpc(proc: str, inp: dict, tries: int = 4):
    url = f"https://poidh.xyz/api/trpc/{proc}?input=" + urllib.parse.quote(json.dumps({"json": inp}))
    err = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
            return json.load(urllib.request.urlopen(req, timeout=30))["result"]["data"]["json"]
        except Exception as e:  # noqa: BLE001 - retried, then re-raised
            err = e
            time.sleep(1.5 * (i + 1))
    raise err


def items_of(payload) -> list:
    """fetchBountyClaims answers either {items: [...]} or a bare list."""
    if isinstance(payload, dict):
        return payload.get("items") or []
    return payload or []


def n_claims(bounty_id: int) -> int:
    return len(items_of(trpc("claims.fetchBountyClaims",
                             {"bountyId": bounty_id, "chainId": CHAIN, "limit": 100})))


def _selftest() -> bool:
    passed = True

    def check(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    check("reads an {items: [...]} payload", len(items_of({"items": [1, 2, 3]})) == 3)
    check("reads a bare-list payload", len(items_of([1, 2])) == 2)
    check("an empty payload is zero, not a crash", items_of(None) == [] and items_of({}) == [])
    check("the controls are the two rounds we know independently",
          CONTROLS == {1151: 11, 1330: 9})
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        print("pull-past-bounty-claims selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    got = {b: n_claims(b) for b in CONTROLS}
    print("CONTROL", got, "expected", CONTROLS, "OK" if got == CONTROLS else "MISMATCH")
    if got != CONTROLS:
        print("Refusing: the claim counter does not return known answers. Nothing it "
              "produced would be trustworthy.")
        return 2

    items, cur = [], None
    for _ in range(PAGES):
        inp = {"chainId": CHAIN, "status": "past", "limit": 50}
        if cur:
            inp["cursor"] = cur
        page = trpc("bounties.fetchAll", inp)
        items += page["items"]
        cur = page.get("nextCursor")
        if not cur:
            break
    print(f"past bounties pulled: {len(items)}"
          + (" - HIT THE PAGE CAP, so this is the most recent slice, not all of them" if cur else ""))
    for b in items:
        if b.get("hasClaims"):
            b["n_claims"] = n_claims(b["id"])
            time.sleep(0.15)
    with open(OUT, "w") as f:
        json.dump(items, f)
    print("saved", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
