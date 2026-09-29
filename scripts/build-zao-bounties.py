#!/usr/bin/env python3
"""Every ZAO bounty on poidh, plus the bounties other people made about ZAOstock.

WHY. The board listed only rounds typed into org.config.json, so a bounty cast this week did not
exist on poidhz.com until someone edited that file, and round six (1446, cast by @presdency.eth)
never appeared at all. This scans poidh's full feed - open, in progress and past - and writes
data/zao-bounties.json:

  ours       issuer is in web/sources.json `issuers`, or the id is in `bounty_ids`
  community  not ours, but the title or text names ZAOstock / ZAO Festivals / The ZAO

EXIT CODES: 0 written, 2 the scan could not run (an empty feed is a failed read, never "no bounties").
"""
import argparse, json, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "web" / "sources.json"
OUT = ROOT / "data" / "zao-bounties.json"
UA = {"User-Agent": "poidhz.com (+https://poidhz.com)"}


def trpc(proc, payload):
    inp = urllib.parse.quote(json.dumps({"0": {"json": payload}}))
    req = urllib.request.Request(f"https://poidh.xyz/api/trpc/{proc}?batch=1&input={inp}", headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())[0]["result"]["data"]["json"]


def status_of(b, feed_status):
    if b.get("isCanceled"):
        return "canceled"
    # poidh leaves isVoting set on finished bounties, so the feed a bounty came from decides first.
    if feed_status == "past":
        return "closed"
    if b.get("isVoting"):
        return "voting"
    return "open"


def classify(b, issuers, extra_ids, keywords):
    """'ours', 'community' or None."""
    if str(b.get("issuer", "")).lower() in issuers or int(b.get("id", -1)) in extra_ids:
        return "ours"
    text = f"{b.get('title') or ''} {b.get('description') or ''}".lower()
    if any(k in text for k in keywords):
        return "community"
    return None


def row(b, feed_status, chain):
    amount = b.get("amount")
    try:
        eth = int(str(amount)) / 1e18
    except (TypeError, ValueError):
        eth = None
    created = b.get("createdAt")
    return {
        "id": int(b["id"]), "title": b.get("title") or "", "issuer": str(b.get("issuer", "")).lower(),
        "amount_eth": eth, "created_at": datetime.fromtimestamp(created, timezone.utc).isoformat() if created else None,
        "status": status_of(b, feed_status), "has_claims": bool(b.get("hasClaims")), "multiplayer": bool(b.get("isMultiplayer")),
        "url": f"https://poidh.xyz/{'base' if chain == 8453 else chain}/bounty/{b['id']}",
    }


def scan(chain, fetch=trpc, max_pages=40):
    seen = {}
    for feed_status in ("open", "progress", "past"):
        cursor, pages = None, 0
        while pages < max_pages:
            payload = {"chainId": chain, "status": feed_status, "sortType": "date", "limit": 100}
            if cursor:
                payload["cursor"] = cursor
            d = fetch("bounties.fetchAll", payload)
            for b in d.get("items", []):
                seen.setdefault(int(b["id"]), (b, feed_status))
            cursor, pages = d.get("nextCursor"), pages + 1
            if not cursor or not d.get("items"):
                break
    return seen


def build(seen, src, chain):
    issuers = {a.lower() for a in src.get("issuers", [])}
    extra = set(src.get("bounty_ids", []))
    kws = [k.lower() for k in src.get("community_keywords", [])]
    ours, community = [], []
    for b, st in seen.values():
        kind = classify(b, issuers, extra, kws)
        if kind == "ours":
            ours.append(row(b, st, chain))
        elif kind == "community":
            community.append(row(b, st, chain))
    key = lambda r: r["created_at"] or ""
    return {"generated_at": datetime.now(timezone.utc).isoformat(), "chain_id": chain, "scanned": len(seen),
            "ours": sorted(ours, key=key, reverse=True), "community": sorted(community, key=key, reverse=True)}


def selftest():
    fails = 0
    def ok(name, cond):
        nonlocal fails
        print(("ok   " if cond else "FAIL ") + name); fails += 0 if cond else 1
    iss, ids, kws = {"0xaaa"}, {1446}, ["zaostock", "the zao"]
    ok("our issuer is ours", classify({"id": 1, "issuer": "0xAAA"}, iss, ids, kws) == "ours")
    ok("listed id is ours whoever cast it", classify({"id": 1446, "issuer": "0xbbb"}, iss, ids, kws) == "ours")
    ok("stranger naming ZAOstock is community", classify({"id": 2, "issuer": "0xccc", "title": "Film ZAOstock"}, iss, ids, kws) == "community")
    ok("unrelated stranger is neither", classify({"id": 3, "issuer": "0xccc", "title": "a bounty for assay"}, iss, ids, kws) is None)
    ok("canceled beats everything", status_of({"isCanceled": True, "isVoting": True}, "open") == "canceled")
    ok("past feed is closed", status_of({}, "past") == "closed")
    ok("voting is voting", status_of({"isVoting": True}, "progress") == "voting")
    ok("a past bounty is closed even with isVoting left set", status_of({"isVoting": True}, "past") == "closed")
    ok("amount as string wei", row({"id": 5, "amount": "5000000000000000", "createdAt": 1790000000}, "open", 8453)["amount_eth"] == 0.005)
    pages = [{"items": [{"id": 1, "issuer": "0xaaa", "createdAt": 1}], "nextCursor": "c"}, {"items": [{"id": 1, "issuer": "0xaaa", "createdAt": 1}], "nextCursor": None}]
    calls = iter(pages + [{"items": [], "nextCursor": None}] * 4)
    ok("paging dedupes across pages and statuses", len(scan(8453, fetch=lambda p, x: next(calls))) == 1)
    print(f"{10 - fails} of 10 passed"); return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chain", type=int, default=8453)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    src = json.loads(SOURCES.read_text())
    try:
        seen = scan(a.chain)
    except Exception as e:
        print(f"UNKNOWN: poidh feed could not be read: {e}"); return 2
    if not seen:
        print("UNKNOWN: poidh feed returned no bounties at all; refusing to write an empty list"); return 2
    out = build(seen, src, a.chain)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(f"scanned {out['scanned']}: {len(out['ours'])} ours, {len(out['community'])} community -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
