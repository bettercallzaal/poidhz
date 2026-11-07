#!/usr/bin/env python3
"""
Log Zaal's place on poidh's own leaderboard (poidh.xyz/leaderboard), so it is possible to
see which of his actions move it.

    python3 scripts/poidh-rank-snapshot.py              # fetch, append if due, write
    python3 scripts/poidh-rank-snapshot.py --dry-run    # fetch and print, write nothing
    python3 scripts/poidh-rank-snapshot.py --selftest   # offline tests, no network

Step 1 of docs/poidh-leaderboard-plan.md. Zaal, 6 Nov 2026: "lowkey wanna get higher on
poidh leaderboard". Measured that day at 17:03 EST: rank 47 of 100, score 223.

WHY A LOG. poidh does not publish its score formula. Casting and funding bounty 1536 on
6 Nov left his score at 223, so funding an open bounty does not count, at least not at
once. The only way to learn what does count is a before-and-after reading around each
thing he does. This is that reading.

SOURCE. The tRPC call behind poidh.xyz/leaderboard, found in its page chunk on 6 Nov:
    leaderboard.fetch  {userAddress, page, limit}
    -> {leaderboard: [[address, {base, degen, arbitrum, mainnet, total}], ...],
        userData: {rank, data: [address, {...same scores...}]},
        pagination: {totalUsers, ...}}

WRITES data/poidh-rank.json, a list of rows. A row is appended when the reading differs
from the last row, or when the last row is from an earlier UTC day. So the file holds at
least one row per day the job runs, and every change.

NEVER A ZERO. If the call fails, or userData is missing or malformed, this prints UNKNOWN,
writes nothing, and exits 2. The last good row stays as it is. It also refuses to write if
the file on disk cannot be read, since replacing it would drop the history.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "data" / "poidh-rank.json"

# Zaal's wallet, read as the issuer of his Singapore bounty 1536 (Base) on 6 Nov 2026.
ADDRESS = "0x7234c36a71ec237c2ae7698e8916e0735001e9af"
API = "https://poidh.xyz/api/trpc/leaderboard.fetch"
UA = "Mozilla/5.0 (poidh-rank-snapshot)"
CHAINS = ("base", "degen", "arbitrum", "mainnet")


def build_url(address: str) -> str:
    payload = {"0": {"json": {"userAddress": address, "page": 1, "limit": 10}}}
    return f"{API}?batch=1&input={urllib.parse.quote(json.dumps(payload))}"


def fetch(address: str, timeout: int = 20):
    req = urllib.request.Request(build_url(address), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 0


def parse(payload, address: str) -> dict | None:
    """The reading for `address`, or None if the payload does not hold a usable one.
    None is UNKNOWN. It is never turned into a zero."""
    try:
        data = payload[0]["result"]["data"]["json"]
        user = data["userData"]
        rank = user["rank"]
        who, scores = user["data"]
    except (KeyError, IndexError, TypeError, ValueError):
        return None
    if not isinstance(who, str) or who.lower() != address.lower():
        return None
    if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
        return None
    if not isinstance(scores, dict) or not _num(scores.get("total")):
        return None
    row = {"rank": rank, "total": scores["total"]}
    for c in CHAINS:
        v = scores.get(c, 0)
        if not _num(v):
            return None
        row[c] = v
    board = (data.get("pagination") or {}).get("totalUsers")
    row["board_size"] = board if isinstance(board, int) and board > 0 else None
    return row


def due(rows: list, reading: dict, today: str) -> bool:
    """Append when there is no last row, the last row is from an earlier day, or any value
    changed."""
    if not rows:
        return True
    last = rows[-1]
    if str(last.get("at", ""))[:10] != today:
        return True
    return any(last.get(k) != v for k, v in reading.items())


def load_rows(path: Path) -> list:
    """Rows on disk. A missing file is an empty log; an unreadable one raises, because
    replacing it would drop the history."""
    if not path.exists():
        return []
    rows = json.loads(path.read_text())
    if not isinstance(rows, list):
        raise ValueError(f"{path} is not a list")
    return rows


def run(address: str, dry_run: bool, path: Path = OUT, fetcher=fetch, now=None) -> int:
    now = now or datetime.now(timezone.utc)
    try:
        payload = fetcher(address)
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
        print(f"UNKNOWN: leaderboard.fetch failed for {address} ({e}). Nothing written.")
        return 2
    reading = parse(payload, address)
    if reading is None:
        print(f"UNKNOWN: no usable userData for {address} in the leaderboard.fetch reply. "
              f"Nothing written.")
        return 2
    print(f"{address}: rank {reading['rank']}, total {reading['total']} "
          + ", ".join(f"{c} {reading[c]}" for c in CHAINS)
          + f", board {reading['board_size']}")

    try:
        rows = load_rows(path)
    except (ValueError, OSError) as e:
        print(f"REFUSED: cannot read {path} ({e}). Not overwriting the history.")
        return 2
    today = now.strftime("%Y-%m-%d")
    if not due(rows, reading, today):
        print("No change since the last row today. Nothing written.")
        return 0
    # Append-only by construction: the old rows are carried over untouched.
    new = rows + [{"at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "address": address.lower(), **reading}]
    if dry_run:
        print("dry run: would append this row.")
        return 0
    path.write_text(json.dumps(new, indent=2) + "\n")
    print(f"appended row {len(new)} to {path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path}")
    return 0


def selftest() -> int:
    import tempfile

    addr = ADDRESS
    scores = {"base": 179, "degen": 0, "arbitrum": 0, "mainnet": 44, "total": 223}

    def reply(user=..., total_users=100):
        u = {"rank": 47, "data": [addr.upper().replace("0X", "0x"), dict(scores)]} if user is ... else user
        return [{"result": {"data": {"json": {"leaderboard": [], "userData": u,
                                              "pagination": {"totalUsers": total_users}}}}}]

    fails = 0

    def check(name, cond):
        nonlocal fails
        print(("ok   " if cond else "FAIL ") + name)
        fails += 0 if cond else 1

    good = parse(reply(), addr)
    check("parses the 6 Nov reading", good == {"rank": 47, "total": 223, "base": 179, "degen": 0,
                                                "arbitrum": 0, "mainnet": 44, "board_size": 100})
    check("null userData is UNKNOWN", parse(reply(user=None), addr) is None)
    check("missing rank is UNKNOWN", parse(reply(user={"data": [addr, scores]}), addr) is None)
    check("rank 0 is UNKNOWN", parse(reply(user={"rank": 0, "data": [addr, scores]}), addr) is None)
    check("another address is UNKNOWN",
          parse(reply(user={"rank": 1, "data": ["0x" + "1" * 40, scores]}), addr) is None)
    check("negative chain score is UNKNOWN",
          parse(reply(user={"rank": 47, "data": [addr, {**scores, "base": -1}]}), addr) is None)
    check("an error reply is UNKNOWN",
          parse([{"error": {"json": {"message": "bad"}}}], addr) is None)
    check("bad board size is kept as None", parse(reply(total_users=0), addr)["board_size"] is None)

    check("first row is due", due([], good, "2026-11-06"))
    same_day = [{"at": "2026-11-06T22:00:00Z", "address": addr, **good}]
    check("same reading same day is not due", not due(same_day, good, "2026-11-06"))
    check("same reading next day is due", due(same_day, good, "2026-11-07"))
    check("changed total same day is due", due(same_day, {**good, "total": 230}, "2026-11-06"))

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "poidh-rank.json"
        t1 = datetime(2026, 11, 6, 22, 3, tzinfo=timezone.utc)
        rc = run(addr, False, p, fetcher=lambda a: reply(), now=t1)
        check("writes the first row", rc == 0 and len(json.loads(p.read_text())) == 1)
        rc = run(addr, False, p, fetcher=lambda a: reply(), now=t1)
        check("no duplicate on an unchanged rerun", rc == 0 and len(json.loads(p.read_text())) == 1)
        before = p.read_text()
        rc = run(addr, False, p, fetcher=lambda a: reply(user=None), now=t1)
        check("UNKNOWN exits 2 and leaves the file", rc == 2 and p.read_text() == before)

        def boom(a):
            raise urllib.error.URLError("unreachable")
        rc = run(addr, False, p, fetcher=boom, now=t1)
        check("network failure exits 2 and leaves the file", rc == 2 and p.read_text() == before)
        p.write_text("{not json")
        rc = run(addr, False, p, fetcher=lambda a: reply(), now=t1)
        check("unreadable history is refused, not replaced", rc == 2 and p.read_text() == "{not json")

    print(f"---\n{'all passed' if not fails else f'{fails} failed'}")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--address", default=ADDRESS)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true", help="offline tests, no network")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    return run(a.address, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
