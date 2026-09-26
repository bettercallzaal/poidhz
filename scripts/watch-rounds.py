#!/usr/bin/env python3
"""Watch the live rounds and print ONE LINE PER CHANGE. Silence means nothing changed.

Built 2026-09-26 because the first `/loop reviewing PRs` was stopped after four empty
ticks. It had no definition of "something happened", so every tick re-read everything and
re-decided by eye whether it was new. This script makes that mechanical: it snapshots the
things a round actually turns on, diffs the snapshot against the last one, and prints only
the differences. A quiet tick costs one line of nothing.

WHAT IT WATCHES, and why each one is a thing that changes what Zaal does:

  1. Bounty status      OPEN -> VOTING -> WINNER SET. VOTING is when resolveVote unlocks.
  2. Vote unlock        the moment resolveVote(<onChainId>) becomes callable. Nobody on a
                        round is paid until that call is fired, and only Zaal can fire it.
  3. New claims         a new entry to read, and on a code round a new PR to review.
  4. Open PRs           on the code repo: new entries, and merges that break a tie.
  5. Claim link health  every github PR link in a claim, HEADed. Round five has an entrant
                        whose claim points at a PR that 404s, so they cannot be judged.

WHAT IT REFUSES TO DO, because each of these is a real bug this repo has shipped:

  - It never reads acceptance from /data. That endpoint carries no isAccepted, and reading
    it there reported the wrong winner four times on 2026-09-26. Status comes from
    query_bounty.status_of, which is imported rather than copied - two copies of the
    precedence rule is two answers to "is it settled".
  - A fetch that FAILS never becomes an event. It warns on stderr and leaves that key's
    state untouched, so the next good tick diffs against the last known-good reading. A
    watcher that reports "all five claims vanished" because the API blinked is worse than
    one that says nothing.
  - It never reports a status going BACKWARDS as fact. Acceptance only moves forward, so
    WINNER SET -> VOTING means the claims endpoint half-failed, not that a winner was
    unset. That prints WATCH-SUSPECT and does not overwrite the state.
  - After 3 consecutive failed sweeps it emits WATCH-DEGRADED on stdout. Silence has to
    mean "nothing changed", never "I stopped being able to look".

    python3 scripts/watch-rounds.py                    # one sweep, print changes, exit
    python3 scripts/watch-rounds.py --watch            # sweep forever, for Monitor
    python3 scripts/watch-rounds.py --interval 120 --watch
    python3 scripts/watch-rounds.py --first-run-summary # print the baseline, not just changes
    python3 scripts/watch-rounds.py --selftest         # no network
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

_qb = import_module("query-bounty")
fetch_bounty_merged = _qb.fetch_bounty_merged
status_of = _qb.status_of

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE = Path(os.environ.get("POIDHZ_WATCH_STATE", Path.home() / ".zao" / "poidhz-watch-state.json"))
PR_LINK_RE = re.compile(r"https?://github\.com/([\w.-]+)/([\w.-]+)/pull/(\d+)")
# Forward-only. A status may advance along this order or jump to CANCELED; going back up it
# means the read was half-broken, not that the chain moved backwards.
STATUS_ORDER = ["CLOSED", "OPEN", "VOTING", "WINNER SET"]
DEGRADED_AFTER = 3


def load_config() -> dict:
    path = REPO_ROOT / "org.config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def watched_bounties(cfg: dict) -> list[int]:
    """Every bounty that can still change: an open round, or one in VOTING awaiting a
    resolveVote. Reads org.config.json's rounds so adding a round to the config is enough."""
    ids: list[int] = []
    rounds = cfg.get("rounds") or {}
    for meta in rounds.values() if isinstance(rounds, dict) else []:
        bid = (meta or {}).get("bounty_id") if isinstance(meta, dict) else None
        if isinstance(bid, int):
            ids.append(bid)
    for bid in cfg.get("default_bounty_ids") or []:
        if isinstance(bid, int) and bid not in ids:
            ids.append(bid)
    return ids


def http_status(url: str, timeout: int = 15) -> int | None:
    """Status code for a URL, or None when the request itself could not be made. None is
    NOT 404 - a DNS failure must never read as "the entrant deleted their PR"."""
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "curl/8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def pr_links_in(bounty: dict) -> list[str]:
    out: list[str] = []
    for c in bounty.get("claims") or []:
        hay = f"{c.get('title') or ''} {c.get('description') or ''} {c.get('url') or ''}"
        for m in PR_LINK_RE.finditer(hay):
            url = f"https://github.com/{m.group(1)}/{m.group(2)}/pull/{m.group(3)}"
            if url not in out:
                out.append(url)
    return out


def open_prs(repo: str) -> dict[str, str] | None:
    """{pr number: "author title"} for open PRs, or None when gh could not answer."""
    try:
        p = subprocess.run(
            ["gh", "pr", "list", "--repo", repo, "--state", "open", "--limit", "100",
             "--json", "number,author,title"],
            capture_output=True, text=True, timeout=60,
        )
        if p.returncode != 0:
            return None
        rows = json.loads(p.stdout or "[]")
    except Exception:
        return None
    return {str(r["number"]): f"{(r.get('author') or {}).get('login', '?')} {r.get('title', '')}" for r in rows}


def sweep(bounty_ids: list[int], repo: str, chain: int, check_links: bool = True) -> tuple[dict, list[str]]:
    """Read the world. Returns (snapshot, failures). A key absent from the snapshot was
    NOT measured this sweep, which is different from measured-as-empty."""
    snap: dict = {"bounties": {}, "links": {}}
    failures: list[str] = []

    for bid in bounty_ids:
        try:
            b = fetch_bounty_merged(bid, chain)
        except Exception as e:
            failures.append(f"bounty {bid}: {e}")
            continue
        if not b:
            failures.append(f"bounty {bid}: not found on chain {chain}")
            continue
        snap["bounties"][str(bid)] = {
            "onchain": b.get("onChainId"),
            "status": status_of(b),
            "deadline": b.get("deadline"),
            "claims": sorted(str(c.get("claimId")) for c in b.get("claims") or []),
            "title": b.get("title"),
        }
        if check_links:
            for url in pr_links_in(b):
                code = http_status(url)
                if code is None:
                    failures.append(f"link {url}: unreachable")
                else:
                    snap["links"][url] = code

    prs = open_prs(repo)
    if prs is None:
        failures.append(f"gh pr list {repo}: failed")
    else:
        snap["prs"] = prs

    return snap, failures


def ts(epoch: float | int | None) -> str:
    if not epoch:
        return "unknown"
    return dt.datetime.fromtimestamp(epoch).strftime("%a %Y-%m-%d %H:%M:%S")


def diff(old: dict, new: dict, now: float) -> tuple[list[str], dict]:
    """Events worth waking someone for, and the state to persist.

    Anything in `new` that was not measured stays at its `old` value: a missing key is an
    unmeasured key, never a changed one.
    """
    events: list[str] = []
    merged = json.loads(json.dumps(old)) if old else {"bounties": {}, "links": {}, "prs": {}}
    merged.setdefault("bounties", {})
    merged.setdefault("links", {})
    merged.setdefault("prs", {})
    first_run = not (old.get("bounties") or old.get("prs"))

    for bid, cur in (new.get("bounties") or {}).items():
        prev = (old.get("bounties") or {}).get(bid)
        if prev is None:
            merged["bounties"][bid] = cur
            continue

        if cur["status"] != prev["status"]:
            back = (cur["status"] in STATUS_ORDER and prev["status"] in STATUS_ORDER
                    and STATUS_ORDER.index(cur["status"]) < STATUS_ORDER.index(prev["status"]))
            if back:
                events.append(
                    f"WATCH-SUSPECT bounty {bid} read as {cur['status']} after {prev['status']} - "
                    "status does not move backwards, so the claims read was half-broken. State kept."
                )
                cur = {**cur, "status": prev["status"]}
            else:
                events.append(f"STATUS bounty {bid} {prev['status']} -> {cur['status']} ({cur.get('title') or ''})")

        added = [c for c in cur["claims"] if c not in prev["claims"]]
        if added:
            events.append(f"CLAIM bounty {bid} new claim(s) {', '.join(added)} - now {len(cur['claims'])} total")

        # The unlock is a crossing, not a state: emit once, when it happens.
        dl = cur.get("deadline")
        if cur["status"] == "VOTING" and dl:
            was_locked = not prev.get("unlock_emitted") and (prev.get("deadline") or 0) > 0
            if now >= dl and was_locked:
                events.append(
                    f"VOTE-UNLOCK bounty {bid} - resolveVote({cur.get('onchain')}) is callable NOW "
                    f"(vote closed {ts(dl)}). Nobody on this round is paid until Zaal fires it."
                )
                cur = {**cur, "unlock_emitted": True}
            elif prev.get("unlock_emitted"):
                cur = {**cur, "unlock_emitted": True}
        merged["bounties"][bid] = cur

    for url, code in (new.get("links") or {}).items():
        prev_code = (old.get("links") or {}).get(url)
        if prev_code is not None and prev_code != code:
            fixed = prev_code >= 400 and code < 400
            events.append(
                f"{'LINK-FIXED' if fixed else 'LINK-BROKE'} {url} {prev_code} -> {code}"
                + (" - this claim can be judged now." if fixed else " - the work behind this claim is gone.")
            )
        elif prev_code is None and code >= 400 and not first_run:
            events.append(f"LINK-DEAD {url} -> {code} - a new claim points at nothing readable.")
        merged["links"][url] = code

    if "prs" in new:
        prev_prs = old.get("prs") or {}
        for num, label in new["prs"].items():
            if num not in prev_prs and not first_run:
                events.append(f"PR-NEW #{num} {label}")
        for num, label in prev_prs.items():
            if num not in new["prs"]:
                events.append(f"PR-GONE #{num} {label} - merged or closed. Merged wins ties, so this is a judging fact.")
        merged["prs"] = new["prs"]

    return events, merged


def summarize(snap: dict, now: float) -> list[str]:
    lines = []
    for bid, b in sorted((snap.get("bounties") or {}).items()):
        extra = ""
        if b["status"] == "VOTING" and b.get("deadline"):
            left = (b["deadline"] - now) / 3600.0
            extra = (f"  resolveVote({b.get('onchain')}) callable NOW" if left <= 0
                     else f"  resolveVote({b.get('onchain')}) unlocks {ts(b['deadline'])}, in {left:.2f}h")
        lines.append(f"  bounty {bid} {b['status']}, {len(b['claims'])} claim(s){extra}")
    dead = [f"{u} ({c})" for u, c in sorted((snap.get("links") or {}).items()) if c >= 400]
    lines.append(f"  claim PR links: {len(snap.get('links') or {})} checked, {len(dead)} dead"
                 + (f" - {', '.join(dead)}" if dead else ""))
    if "prs" in snap:
        lines.append(f"  open PRs on the code repo: {len(snap['prs'])}")
    return lines


def _selftest() -> int:
    checks: list[tuple[str, bool]] = []
    now = 1_000_000.0
    base = {
        "bounties": {"1412": {"onchain": 426, "status": "VOTING", "deadline": now + 3600,
                              "claims": ["1", "2"], "title": "R3"}},
        "links": {"https://github.com/o/r/pull/320": 404},
        "prs": {"316": "alice one"},
    }

    # A change must be seen.
    moved = json.loads(json.dumps(base))
    moved["bounties"]["1412"]["status"] = "WINNER SET"
    ev, _ = diff(base, moved, now)
    checks.append(("status advance is an event", any(e.startswith("STATUS") for e in ev)))

    # An identical snapshot must be silent. The control the first loop lacked.
    ev, _ = diff(base, json.loads(json.dumps(base)), now)
    checks.append(("an unchanged sweep prints nothing", ev == []))

    # A vanished key is unmeasured, not a change.
    ev, st = diff(base, {"bounties": {}, "links": {}}, now)
    checks.append(("an unmeasured sweep prints nothing", ev == []))
    # .get, not [], on purpose: if the carry-over breaks, this must report FAIL rather than
    # raise KeyError. A suite that crashes instead of failing tells you less, and a crash in
    # one check hides every check after it.
    checks.append(("an unmeasured sweep keeps the last good reading",
                   st.get("bounties", {}).get("1412", {}).get("status") == "VOTING"))
    checks.append(("an unmeasured sweep keeps the PR set", st.get("prs") == {"316": "alice one"}))

    # Backwards status is suspect, not fact, and must not overwrite.
    settled = json.loads(json.dumps(base))
    settled["bounties"]["1412"]["status"] = "WINNER SET"
    ev, st = diff(settled, base, now)
    checks.append(("a backwards status is WATCH-SUSPECT", any(e.startswith("WATCH-SUSPECT") for e in ev)))
    checks.append(("a backwards status does not overwrite state", st["bounties"]["1412"]["status"] == "WINNER SET"))

    # The unlock fires once, on the crossing.
    ev, st = diff(base, json.loads(json.dumps(base)), now + 3601)
    checks.append(("the vote unlock is an event when it crosses", any(e.startswith("VOTE-UNLOCK") for e in ev)))
    checks.append(("the unlock names the on-chain id, not the poidh id", any("resolveVote(426)" in e for e in ev)))
    ev2, _ = diff(st, json.loads(json.dumps(base)), now + 7200)
    checks.append(("the vote unlock does not repeat every tick", not any(e.startswith("VOTE-UNLOCK") for e in ev2)))
    ev3, _ = diff(base, json.loads(json.dumps(base)), now)
    checks.append(("the vote unlock stays quiet before it crosses", not any(e.startswith("VOTE-UNLOCK") for e in ev3)))

    # Claims, links, PRs.
    more = json.loads(json.dumps(base))
    more["bounties"]["1412"]["claims"] = ["1", "2", "3"]
    ev, _ = diff(base, more, now)
    checks.append(("a new claim is an event", any(e.startswith("CLAIM") and " 3" in e for e in ev)))

    fixed = json.loads(json.dumps(base))
    fixed["links"]["https://github.com/o/r/pull/320"] = 200
    ev, _ = diff(base, fixed, now)
    checks.append(("a dead link coming back is LINK-FIXED", any(e.startswith("LINK-FIXED") for e in ev)))
    broke = json.loads(json.dumps(base))
    broke["links"]["https://github.com/o/r/pull/316"] = 404
    ev, _ = diff(base, broke, now)
    checks.append(("a newly dead link is LINK-DEAD", any(e.startswith("LINK-DEAD") for e in ev)))

    prs = json.loads(json.dumps(base))
    prs["prs"] = {"316": "alice one", "322": "ghost two"}
    ev, _ = diff(base, prs, now)
    checks.append(("a new PR is an event", any(e.startswith("PR-NEW #322") for e in ev)))
    gone = json.loads(json.dumps(base))
    gone["prs"] = {}
    ev, _ = diff(base, gone, now)
    checks.append(("a merged PR is an event", any(e.startswith("PR-GONE #316") for e in ev)))

    # First run must not shout the whole world as news.
    ev, _ = diff({}, base, now)
    checks.append(("the first sweep is a baseline, not 5 events", ev == []))

    # Link extraction, both ways.
    b = {"claims": [{"title": "see https://github.com/ZAODEVZ/ZAOstock/pull/320 please",
                     "description": "and https://github.com/ZAODEVZ/ZAOstock/pull/320 again"},
                    {"title": "no link here"}]}
    links = pr_links_in(b)
    checks.append(("a PR link is found in claim text", links == ["https://github.com/ZAODEVZ/ZAOstock/pull/320"]))
    checks.append(("a claim with no link adds nothing", pr_links_in({"claims": [{"title": "x"}]}) == []))
    checks.append(("a non-PR github link is ignored",
                   pr_links_in({"claims": [{"title": "https://github.com/o/r/issues/9"}]}) == []))

    fails = 0
    for label, ok in checks:
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    print(f"selftest: {len(checks) - fails}/{len(checks)} passed")
    return 1 if fails else 0


def read_state(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True))


def one_sweep(args, state_path: Path, consecutive_failures: int) -> tuple[int, int]:
    """Prints events. Returns (events printed, consecutive all-failed sweeps)."""
    cfg = load_config()
    ids = [int(x) for x in args.bounty.split(",")] if args.bounty else watched_bounties(cfg)
    snap, failures = sweep(ids, args.repo, args.chain, check_links=not args.no_links)
    for f in failures:
        print(f"  WARN could not measure {f}", file=sys.stderr)

    measured_anything = bool(snap.get("bounties")) or "prs" in snap
    if not measured_anything:
        consecutive_failures += 1
        if consecutive_failures >= DEGRADED_AFTER:
            print(f"WATCH-DEGRADED {consecutive_failures} sweeps in a row measured nothing. "
                  "Silence below is not 'no change', it is 'cannot look'.", flush=True)
        return 0, consecutive_failures
    consecutive_failures = 0

    old = read_state(state_path)
    events, new_state = diff(old, snap, time.time())
    for e in events:
        print(e, flush=True)
    new_state["read_at"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_state(state_path, new_state)

    if args.first_run_summary and not events:
        for line in summarize(new_state, time.time()):
            print(line, flush=True)
    return len(events), consecutive_failures


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bounty", help="comma-separated bounty ids (default: org.config.json's rounds)")
    p.add_argument("--repo", default="ZAODEVZ/ZAOstock", help="code repo whose open PRs are entries")
    p.add_argument("--chain", type=int, default=8453)
    p.add_argument("--state", default=str(DEFAULT_STATE), help=f"state file (default {DEFAULT_STATE})")
    p.add_argument("--watch", action="store_true", help="sweep forever, one line per change (for Monitor)")
    p.add_argument("--interval", type=int, default=120, help="seconds between sweeps under --watch")
    p.add_argument("--no-links", action="store_true", help="skip the claim PR link checks")
    p.add_argument("--first-run-summary", action="store_true", help="print the baseline when there are no changes")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    state_path = Path(args.state).expanduser()
    if not args.watch:
        n, _ = one_sweep(args, state_path, 0)
        return 0 if n >= 0 else 1

    fails = 0
    while True:
        try:
            _, fails = one_sweep(args, state_path, fails)
        except KeyboardInterrupt:
            return 0
        except Exception as e:  # a crashed watcher must say so on stdout, not go quiet
            print(f"WATCH-DEGRADED sweep raised {type(e).__name__}: {e}", flush=True)
        time.sleep(max(15, args.interval))


if __name__ == "__main__":
    sys.exit(main())
