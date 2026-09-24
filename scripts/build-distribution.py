#!/usr/bin/env python3
"""Build a $ZABAL distribution list from the leaderboard, and reconcile it against what was
already paid.

WHY THIS EXISTS. On 2026-09-23 this programme kept a $ZABAL promise for the first time in its
history - 43 recipients, 111,012,370.81 $ZABAL, one transaction. **The method lived nowhere.**
It was reconstructed on 2026-09-24 by decoding the receipt:

    total / sum(scores) = per-point rate, and every address got score x rate

    111,012,370.81 / 60 points = 1,850,206.1802 per point
    43 of 43 addresses matched exactly, 0 on the feed unpaid, 0 mismatches

A method that has to be re-derived from chain data every time is a method that will eventually
be applied slightly differently and nobody will notice. This file is that method, written down
and checkable.

TWO MODES, AND THE DIFFERENCE MATTERS TO WHOEVER IS RECEIVING.

  --full   Everyone on the feed is paid score x rate. Use when starting a fresh cycle. Running
           this twice pays people twice for the same points, which may be exactly what you
           want - a recurring drop - but it is a decision, not a default.

  --topup  Only the points gained SINCE a previous distribution are paid, at the same
           per-point rate that distribution used. Someone whose score did not move gets
           nothing and is left out of the list entirely rather than sent a zero.

TOP-UP READS THE PREVIOUS PAYMENT FROM CHAIN, NOT FROM A FILE. A local record of what was paid
can drift from what was actually sent; the receipt cannot. Pass --against-tx and it decodes
that transaction's Transfer logs and diffs against them.

NOTHING HERE SENDS ANYTHING. It writes a list. Zaal fires every transaction.

    python3 scripts/build-distribution.py --full 118413195.52
    python3 scripts/build-distribution.py --topup --against-tx 0x4b79...
    python3 scripts/build-distribution.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FEED = REPO_ROOT / "data" / "leaderboard.json"
RICH = REPO_ROOT / "data" / "claims.json"
BASE_RPC = "https://mainnet.base.org"
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


def load_feed() -> dict[str, int]:
    """address -> score. Refuses an empty feed rather than producing an empty payout list."""
    if not FEED.exists():
        raise SystemExit(f"FAIL: {FEED} does not exist. Run refresh-poidh-leaderboard.py.")
    rows = json.loads(FEED.read_text())
    out = {r["address"].lower(): int(r["score"]) for r in rows if r.get("address")}
    if not out:
        raise SystemExit("FAIL: the leaderboard feed has no addresses. An empty distribution "
                         "is not a distribution - it is a missing measurement.")
    if sum(out.values()) <= 0:
        raise SystemExit("FAIL: every score is zero. Refusing to divide by zero and refusing "
                         "to pay a flat split that nobody chose.")
    return out


def handles() -> dict[str, str]:
    """address -> a name a human can check. Missing is UNRESOLVED, never blank."""
    if not RICH.exists():
        return {}
    try:
        rows = json.loads(RICH.read_text()).get("leaderboard") or []
    except Exception:
        return {}
    out = {}
    for r in rows:
        a = (r.get("address") or "").lower()
        if a:
            out[a] = (r.get("farcaster_username") or r.get("twitter_handle")
                      or r.get("displayName") or "UNRESOLVED")
    return out


def paid_in_tx(tx_hash: str) -> dict[str, float]:
    """address -> tokens received in that transaction, decoded from its Transfer logs.

    Returns {} only when the transaction genuinely moved no tokens; a failed lookup raises,
    because a silent empty dict here would make a top-up pay everybody in full."""
    payload = json.dumps({"jsonrpc": "2.0", "id": 1,
                          "method": "eth_getTransactionReceipt", "params": [tx_hash]}).encode()
    req = urllib.request.Request(BASE_RPC, data=payload,
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "zpoidh-distribution"})
    with urllib.request.urlopen(req, timeout=40) as r:
        res = json.loads(r.read()).get("result")
    if not res:
        raise SystemExit(f"FAIL: no receipt for {tx_hash}. Nothing was diffed.")
    if res.get("status") != "0x1":
        raise SystemExit(f"FAIL: {tx_hash} did not succeed (status {res.get('status')}). "
                         f"Refusing to treat a failed transaction as money paid.")
    out: dict[str, float] = {}
    for log in res.get("logs", []):
        if log["topics"][0] != TRANSFER_TOPIC or len(log["topics"]) < 3:
            continue
        to = ("0x" + log["topics"][2][-40:]).lower()
        out[to] = out.get(to, 0.0) + int(log["data"], 16) / 1e18
    return out


def rate_from(paid: dict[str, float], scores: dict[str, int]) -> float:
    """The per-point rate a previous distribution used, derived from what it actually sent.

    Uses the MEDIAN of amount/score across addresses present in both, so one odd row cannot
    move it. Raises rather than guessing when nothing overlaps.
    """
    per = sorted(paid[a] / scores[a] for a in paid if scores.get(a))
    if not per:
        raise SystemExit("FAIL: none of the paid addresses are on the current feed, so the "
                         "per-point rate cannot be derived. Nothing was written.")
    mid = len(per) // 2
    return per[mid] if len(per) % 2 else (per[mid - 1] + per[mid]) / 2


def full(scores: dict[str, int], total: float) -> list[tuple[str, int, float]]:
    pts = sum(scores.values())
    rate = total / pts
    return [(a, s, s * rate) for a, s in sorted(scores.items(), key=lambda kv: -kv[1])]


def topup(scores: dict[str, int], paid: dict[str, float], rate: float
          ) -> list[tuple[str, int, float]]:
    """Only the unpaid points, at the previous rate. Zero rows are dropped, not sent."""
    rows = []
    for a, s in sorted(scores.items(), key=lambda kv: -kv[1]):
        already = paid.get(a, 0.0)
        owed = s * rate - already
        if owed > rate * 0.01:      # a hair above zero, to absorb rounding
            rows.append((a, s, owed))
    return rows


def _selftest() -> bool:
    passed = True

    def c(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    # The REAL 2026-09-23 shape: 34 ones, 6 twos, 1 four, 2 fives = 60 points.
    scores = {}
    for i in range(34): scores[f"0x{i:040x}"] = 1
    for i in range(34, 40): scores[f"0x{i:040x}"] = 2
    scores[f"0x{40:040x}"] = 4
    for i in range(41, 43): scores[f"0x{i:040x}"] = 5
    c("the fixture reproduces the real 60-point board",
      len(scores) == 43 and sum(scores.values()) == 60)

    TOTAL = 111012370.81
    rows = full(scores, TOTAL)
    c("full pays every address", len(rows) == 43)
    c("full sums to the total", abs(sum(v for _, _, v in rows) - TOTAL) < 0.01)
    unit = TOTAL / 60
    c("the per-point unit matches the real distribution",
      abs(unit - 1850206.1802) < 0.001)
    c("a score-5 address gets 5 units, as two really did",
      any(abs(v - 5 * unit) < 0.01 for _, s, v in rows if s == 5))
    c("exactly four distinct amounts came out, as on chain",
      len({round(v, 2) for _, _, v in rows}) == 4)

    paid = {a: s * unit for a, s in scores.items()}
    c("rate is recovered from what was paid", abs(rate_from(paid, scores) - unit) < 0.01)

    # Now round three lands: three addresses gain a point and one new address appears.
    after = dict(scores)
    after[f"0x{0:040x}"] += 1
    after[f"0x{34:040x}"] += 1
    after[f"0x{41:040x}"] += 1
    after["0x" + "f" * 40] = 1
    c("the new board is 64 points over 44 addresses",
      sum(after.values()) == 64 and len(after) == 44)

    t = topup(after, paid, unit)
    c("top-up pays only the four who moved", len(t) == 4)
    c("top-up pays one point each", all(abs(v - unit) < 0.01 for _, _, v in t))
    c("top-up total is exactly four points", abs(sum(v for _, _, v in t) - 4 * unit) < 0.01)
    c("nobody who stood still is in the list",
      f"0x{1:040x}" not in {a for a, _, _ in t})
    c("the brand-new address IS in the list", "0x" + "f" * 40 in {a for a, _, _ in t})

    c("re-running a top-up against an up-to-date payment pays nobody",
      topup(after, {a: s * unit for a, s in after.items()}, unit) == [])

    try:
        rate_from({"0xdead": 100.0}, {"0xbeef": 1})
        c("a rate derived from no overlap is REFUSED", False)
    except SystemExit:
        c("a rate derived from no overlap is REFUSED", True)
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", type=float, metavar="TOTAL",
                    help="pay everyone score x (TOTAL / total points)")
    ap.add_argument("--topup", action="store_true",
                    help="pay only points gained since --against-tx")
    ap.add_argument("--against-tx", help="a previous distribution transaction hash")
    ap.add_argument("--out", default="/tmp/zabal-distribution.csv")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        print("build-distribution selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    scores = load_feed()
    names = handles()
    pts = sum(scores.values())
    print(f"feed: {len(scores)} addresses, {pts} points total")

    if a.topup:
        if not a.against_tx:
            ap.error("--topup needs --against-tx")
        paid = paid_in_tx(a.against_tx)
        print(f"previous tx paid {len(paid)} addresses, "
              f"{sum(paid.values()):,.2f} tokens")
        rate = rate_from(paid, scores)
        print(f"per-point rate recovered from that transaction: {rate:,.4f}")
        rows = topup(scores, paid, rate)
        if not rows:
            print("\n  NOBODY IS OWED ANYTHING. Every address on the feed has already been "
                  "paid for every point it holds.")
            return 0
    elif a.full is not None:
        rows = full(scores, a.full)
        print(f"per-point rate: {a.full / pts:,.4f}")
    else:
        ap.error("give --full TOTAL or --topup --against-tx HASH")

    print()
    for addr, score, amt in rows:
        print(f"  {addr}  {score:>2} pts  {amt:>18,.2f}  @{names.get(addr, 'UNRESOLVED')}")
    print(f"\n  {len(rows)} recipients, {sum(v for _, _, v in rows):,.2f} tokens total")

    out = Path(a.out)
    out.write_text("address,amount\n" + "".join(f"{ad},{v:.2f}\n" for ad, _, v in rows))
    print(f"  wrote {out} - address,amount, ready for a disperse tool")
    print("  NOTHING HAS BEEN SENT. Zaal fires the transaction.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
