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
# A claim may name its pull request in WORDS rather than as a link, and one did: claim 8329
# on bounty 1421 is titled "ZAOstock PR 334: skip autoplay hero video on mobile" and carries
# no URL at all. The URL-only matcher above read that as "no claim cites #334" while a claim
# plainly did, which is the entry classification getting the answer backwards.
#
# Deliberately narrow. It wants the literal token PR or "pull request" immediately before the
# number, so a bare figure in prose - a price, a byte count, a year - cannot become an entry.
# \b before PR stops APR and EXPR matching.
PR_WORD_RE = re.compile(r"(?i)\b(?:pr|pull\s+request)\s*#?\s*(\d{1,6})\b")
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


def closes_at_by_bounty() -> dict[int, str]:
    """bounty id -> the round's STATED close, from data/rounds-live.json.

    Not from the chain: poidh returns deadline null for an open bounty and only sets it when a
    vote starts, so a round's advertised close exists in its cast text and in this feed and
    nowhere else. That is exactly why it needs recording - nothing on chain marks the moment.
    """
    p = REPO_ROOT / "data" / "rounds-live.json"
    try:
        feed = json.loads(p.read_text())
    except Exception:
        return {}
    out: dict[int, str] = {}
    for r in feed.get("rounds", []):
        bid, ca = r.get("bounty_id"), r.get("closes_at")
        if isinstance(bid, int) and ca:
            out[bid] = ca
    return out


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


def pr_links_with_claims(bounty: dict) -> list[tuple[str, str, str]]:
    """(url, pr number, claim id) for every github PR link inside a claim on this bounty.

    This is what decides whether a pull request is an ENTRY. A PR nobody claimed is repo
    traffic: the pot pays claims, not pull requests.
    """
    out: list[tuple[str | None, str, str]] = []
    seen: set[tuple[str, str]] = set()
    for c in bounty.get("claims") or []:
        cid = str(c.get("claimId"))
        hay = f"{c.get('title') or ''} {c.get('description') or ''} {c.get('url') or ''}"
        numbered: set[str] = set()
        for m in PR_LINK_RE.finditer(hay):
            url = f"https://github.com/{m.group(1)}/{m.group(2)}/pull/{m.group(3)}"
            key = (url, cid)
            if key in seen:
                continue
            seen.add(key)
            numbered.add(m.group(3))
            out.append((url, m.group(3), cid))
        # A bare "PR 334" makes it an ENTRY but gives nothing to health-check, so its url is
        # None. A number already found as a link is not added twice.
        for m in PR_WORD_RE.finditer(hay):
            num = m.group(1)
            if num in numbered:
                continue
            numbered.add(num)
            out.append((None, num, cid))
    return out


def pr_links_in(bounty: dict) -> list[str]:
    """Only the real URLs - a PR named in words has nothing to fetch."""
    return [u for u, _, _ in pr_links_with_claims(bounty) if u]


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
    closes = closes_at_by_bounty()

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
            "closes_at": closes.get(bid),
            "claims": sorted(str(c.get("claimId")) for c in b.get("claims") or []),
            "title": b.get("title"),
        }
        for url, prnum, cid in pr_links_with_claims(b):
            snap.setdefault("entry_prs", {})[prnum] = f"bounty {bid} claim {cid}"
            if url is None:
                continue
            if check_links:
                code = http_status(url)
                if code is None:
                    failures.append(f"link {url}: unreachable")
                else:
                    snap["links"][url] = code

    # Measured-and-empty is not the same as unmeasured. If any bounty was read, the entry
    # set was established even when it turns out nothing cites a PR, so record the {}.
    if snap["bounties"]:
        snap.setdefault("entry_prs", {})
    # WHEN this sweep happened, so a later sweep can answer "were we watching before that
    # close?" - without it, a close that passed before the watcher existed is indistinguishable
    # from one it actually observed.
    snap["swept_at"] = time.time()

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

        # THE CLOSE IS A MOMENT AND NOTHING ON CHAIN MARKS IT. Round three has a claim whose
        # in-or-out status is permanently UNKNOWN because the field was never counted at the
        # boundary - poidh exposes no claim timestamp, so once the moment passes it cannot be
        # reconstructed. This records it while it is still recordable, and once only.
        ca = cur.get("closes_at")
        if ca and not prev.get("close_recorded"):
            try:
                when = dt.datetime.fromisoformat(ca).timestamp()
            except Exception:
                when = None
            # THE FIRST VERSION REPORTED TODAY'S FIELD AS THE FIELD AT A CLOSE DAYS PAST.
            # On its first live sweep it fired for 1409, 1410 and 1412 - closed 21, 22 and 23
            # September - printing CURRENT claim counts under "FIELD AT THE CLOSE". For 1412
            # that asserted five claims at the boundary, when the known fact about that round
            # is that claim 8153 landed ACROSS it and whether it was inside is UNKNOWN. The
            # feature invented the exact false certainty it exists to prevent.
            #
            # A close is now only reported when this watcher was watching before it: the
            # previous sweep must predate the close. Anything older is reported as NOT
            # OBSERVED, which is the true statement.
            # AND BEING ALIVE BEFORE THE CLOSE IS NOT ENOUGH EITHER. The previous version
            # certified whenever the watcher had swept at ANY point before the close, without
            # asking how late the CURRENT reading is. Last sweep at close minus three hours, a
            # claim landing three minutes after the close, this sweep seven minutes after: it
            # printed that claim as part of "the field at the close". Same false certainty, one
            # layer down, found by an independent reviewer driving diff() with a fixed clock.
            #
            # The fix needs no time threshold, because the snapshots already carry the answer.
            # Claims present in the PREVIOUS snapshot were seen at prev_sweep, which is before
            # the close, so they were definitely in. Claims that are new in THIS snapshot
            # appeared somewhere in (prev_sweep, now], a window containing the close, so their
            # side is unknowable - which is exactly round three's claim 8153. So the report
            # states both sets and the width of the window rather than picking a cutoff and
            # calling everything inside it certain.
            prev_sweep = old.get("swept_at")
            if when is not None and now >= when:
                if prev_sweep is not None and prev_sweep < when:
                    confirmed = [c for c in cur["claims"] if c in prev["claims"]]
                    ambiguous = [c for c in cur["claims"] if c not in prev["claims"]]
                    gap = (now - prev_sweep) / 60.0
                    msg = (f"ROUND-CLOSED bounty {bid} reached its stated close ({ca}). "
                           f"CONFIRMED IN: {len(confirmed)} claim(s) seen before the close - "
                           f"{', '.join(confirmed) or 'none'}.")
                    if ambiguous:
                        msg += (f" AMBIGUOUS: {len(ambiguous)} claim(s) first seen on this sweep "
                                f"- {', '.join(ambiguous)} - which appeared somewhere in the "
                                f"{gap:.1f} minutes spanning the close, so whether they beat it "
                                f"is UNKNOWN from here. poidh exposes no claim timestamp.")
                    else:
                        msg += (f" Nothing new appeared in the {gap:.1f} minutes spanning the "
                                f"close, so the field at the close is exactly those "
                                f"{len(confirmed)}.")
                    events.append(msg)
                else:
                    events.append(
                        f"CLOSE-NOT-OBSERVED bounty {bid} closed at {ca}, before this watcher "
                        f"was recording. The field at that moment is UNKNOWN from here and "
                        f"cannot be reconstructed - poidh exposes no claim timestamp. It has "
                        f"{len(cur['claims'])} claim(s) NOW, which is a different statement."
                    )
                cur = {**cur, "close_recorded": True}
        elif prev.get("close_recorded"):
            cur = {**cur, "close_recorded": True}

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

    # An ENTRY is a pull request some claim points at. Everything else on that repo is the
    # maintainer's own traffic. Measured 2026-09-26: the first six PR events this watcher
    # produced were all housekeeping PRs by the repo's own owner, and every one of them was
    # labelled a judging fact. A watcher that calls everything important is read as noise, and
    # the one line that mattered would have been skipped with the rest.
    entry_prs = new.get("entry_prs", old.get("entry_prs") or {})
    merged["entry_prs"] = entry_prs
    if "prs" in new:
        prev_prs = old.get("prs") or {}
        for num, label in new["prs"].items():
            if num not in prev_prs and not first_run:
                if num in entry_prs:
                    events.append(f"ENTRY-NEW #{num} {label} - cited by {entry_prs[num]}")
                else:
                    events.append(f"PR-NEW #{num} {label} - no claim cites it, so not an entry yet")
        for num, label in prev_prs.items():
            if num not in new["prs"]:
                if num in entry_prs:
                    events.append(f"ENTRY-MERGED #{num} {label} - cited by {entry_prs[num]}. "
                                  "Merged wins ties, so this is a judging fact.")
                else:
                    events.append(f"PR-GONE #{num} {label} - merged or closed, no claim cited it")
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
        entries = snap.get("entry_prs") or {}
        cited_open = sorted(n for n in snap["prs"] if n in entries)
        uncited = sorted(n for n in snap["prs"] if n not in entries)
        lines.append(f"  open PRs on the code repo: {len(snap['prs'])}"
                     f" - {len(cited_open)} cited by a claim ({', '.join('#' + n for n in cited_open) or 'none'}),"
                     f" {len(uncited)} not an entry ({', '.join('#' + n for n in uncited) or 'none'})")
        orphan = sorted(n for n in entries if n not in snap["prs"])
        if orphan:
            lines.append(f"  claimed PRs that are NOT open: {', '.join('#' + n for n in orphan)}"
                         " - merged, closed, or never existed")
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

    # THE CLOSE BOUNDARY, both directions. This is the one measurement that cannot be taken
    # late: poidh exposes no claim timestamp, so a field counted at 17:07 cannot be separated
    # from the field at 17:00.
    _close = "2026-09-27T17:00:00-04:00"
    _at = dt.datetime.fromisoformat(_close).timestamp()
    closing = {"bounties": {"1418": {"onchain": 432, "status": "OPEN", "deadline": None,
                                     "closes_at": _close, "claims": ["1", "2", "3"], "title": "R4"}},
               "links": {}, "prs": {}, "swept_at": _at - 600}
    ev, st = diff(closing, json.loads(json.dumps(closing)), _at - 1)
    checks.append(("a minute before the close, nothing is recorded",
                   not any(e.startswith("ROUND-CLOSED") for e in ev)))
    ev, st = diff(closing, json.loads(json.dumps(closing)), _at)
    checks.append(("at the stated close the field is recorded",
                   any(e.startswith("ROUND-CLOSED bounty 1418") for e in ev)))
    checks.append(("and it names the count and the claim ids",
                   any("3 claim(s)" in e and "1, 2, 3" in e for e in ev)))

    # THE REVIEWER'S SCENARIO, which the first fix still got wrong: alive before the close is
    # not the same as having looked recently. Last sweep three hours before, this sweep seven
    # minutes after, a claim that appeared somewhere in between.
    late_prev = {"bounties": {"1418": {"onchain": 432, "status": "OPEN", "deadline": None,
                                       "closes_at": _close, "claims": ["1", "2", "3"], "title": "R4"}},
                 "links": {}, "prs": {}, "swept_at": _at - 3 * 3600}
    late_now = json.loads(json.dumps(late_prev))
    late_now["bounties"]["1418"]["claims"] = ["1", "2", "3", "4"]
    ev, _ = diff(late_prev, late_now, _at + 7 * 60)
    closed = [e for e in ev if e.startswith("ROUND-CLOSED")]
    checks.append(("a claim first seen after the close is NOT counted as in the field",
                   bool(closed) and "CONFIRMED IN: 3 claim(s)" in closed[0]))
    checks.append(("it is named as ambiguous instead",
                   bool(closed) and "AMBIGUOUS: 1 claim(s)" in closed[0] and "- 4 -" in closed[0]))
    checks.append(("and the width of the unobserved window is stated",
                   bool(closed) and "187.0 minutes" in closed[0]))
    checks.append(("the ambiguous case says UNKNOWN rather than implying certainty",
                   bool(closed) and "UNKNOWN" in closed[0]))

    # And when nothing new arrived in that window, the field IS exactly what was confirmed.
    quiet_now = json.loads(json.dumps(late_prev))
    ev, _ = diff(late_prev, quiet_now, _at + 7 * 60)
    closed = [e for e in ev if e.startswith("ROUND-CLOSED")]
    checks.append(("with nothing new in the window, the field is stated exactly",
                   bool(closed) and "is exactly those 3" in closed[0]
                   and "AMBIGUOUS" not in closed[0]))

    # THE BUG THE FIRST LIVE SWEEP FOUND. A close that passed before this watcher existed must
    # NOT be reported as an observed field - it fired for three settled rounds and printed
    # today's counts under "FIELD AT THE CLOSE".
    never_watched = {k: v for k, v in closing.items() if k != "swept_at"}
    ev, st2 = diff(never_watched, json.loads(json.dumps(never_watched)), _at + 86400)
    checks.append(("a close that passed before this watcher ran is NOT reported as observed",
                   not any(e.startswith("ROUND-CLOSED") for e in ev)))
    checks.append(("it is reported as NOT OBSERVED instead, which is the true statement",
                   any(e.startswith("CLOSE-NOT-OBSERVED bounty 1418") for e in ev)))
    checks.append(("and that message says the field then is UNKNOWN",
                   any("UNKNOWN" in e for e in ev if e.startswith("CLOSE-NOT-OBSERVED"))))
    checks.append(("the not-observed notice also fires only once",
                   not any(e.startswith("CLOSE-NOT-OBSERVED")
                           for e in diff(st2, json.loads(json.dumps(never_watched)), _at + 90000)[0])))
    stale = {**json.loads(json.dumps(closing)), "swept_at": _at + 10}
    ev, _ = diff(stale, json.loads(json.dumps(stale)), _at + 86400)
    checks.append(("a sweep that only started AFTER the close does not claim to have seen it",
                   not any(e.startswith("ROUND-CLOSED") for e in ev)))
    ev2, _ = diff(st, json.loads(json.dumps(closing)), _at + 3600)
    checks.append(("it is recorded once, not on every later sweep",
                   not any(e.startswith("ROUND-CLOSED") for e in ev2)))
    no_ca = json.loads(json.dumps(closing))
    del no_ca["bounties"]["1418"]["closes_at"]
    ev, _ = diff(no_ca, json.loads(json.dumps(no_ca)), _at + 3600)
    checks.append(("a round with no stated close records nothing rather than guessing",
                   not any(e.startswith("ROUND-CLOSED") for e in ev)))
    bad = json.loads(json.dumps(closing))
    bad["bounties"]["1418"]["closes_at"] = "not a date"
    ev, _ = diff(bad, json.loads(json.dumps(bad)), _at + 3600)
    checks.append(("an unparseable close does not raise and records nothing",
                   not any(e.startswith("ROUND-CLOSED") for e in ev)))

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
    checks.append(("a new PR is an event", any("#322" in e for e in ev)))
    gone = json.loads(json.dumps(base))
    gone["prs"] = {}
    ev, _ = diff(base, gone, now)
    checks.append(("a merged PR is an event", any("#316" in e for e in ev)))

    # An entry is a PR a claim cites. Everything else is the maintainer's own traffic, and
    # calling that a judging fact is how the one line that matters gets skipped. Both
    # directions, because a label that fires on everything carries no information.
    cited = {"bounties": base["bounties"], "links": {}, "prs": {"316": "alice one"},
             "entry_prs": {"316": "bounty 1421 claim 8304"}}
    ev, _ = diff(cited, {**cited, "prs": {}}, now)
    checks.append(("a CLAIMED pr merging is a judging fact",
                   any(e.startswith("ENTRY-MERGED #316") and "judging fact" in e for e in ev)))
    uncited = {"bounties": base["bounties"], "links": {}, "prs": {"327": "owner housekeeping"},
               "entry_prs": {"316": "bounty 1421 claim 8304"}}
    ev, _ = diff(uncited, {**uncited, "prs": {}}, now)
    checks.append(("an UNCLAIMED pr merging is NOT called a judging fact",
                   any(e.startswith("PR-GONE #327") for e in ev) and not any("judging fact" in e for e in ev)))
    ev, _ = diff(uncited, {**uncited, "prs": {"327": "owner housekeeping", "330": "someone new"}}, now)
    checks.append(("a new pr no claim cites says so", any("not an entry yet" in e for e in ev)))
    entry_new = {**cited, "entry_prs": {"316": "bounty 1421 claim 8304", "318": "bounty 1421 claim 8305"}}
    ev, _ = diff(cited, {**entry_new, "prs": {"316": "alice one", "318": "alice two"}}, now)
    checks.append(("a new pr a claim DOES cite is an ENTRY-NEW",
                   any(e.startswith("ENTRY-NEW #318") and "claim 8305" in e for e in ev)))

    # The entry set must survive a sweep that could not read the bounties, like every other key.
    _, st = diff(cited, {"prs": {"316": "alice one"}}, now)
    checks.append(("an unmeasured sweep keeps the entry set", st.get("entry_prs") == {"316": "bounty 1421 claim 8304"}))

    # SWEEP ITSELF MUST STAMP THE TIME, and nothing tested that. Every check above builds a
    # snapshot by hand, so deleting the line that writes swept_at left the suite green while
    # silently disabling close reporting entirely - a mutation found exactly that. This calls
    # the real sweep() with the network stubbed out.
    import builtins as _b
    _real_fetch, _real_prs = globals()["fetch_bounty_merged"], globals()["open_prs"]
    try:
        globals()["fetch_bounty_merged"] = lambda bid, chain: {
            "onChainId": 1, "isCanceled": False, "inProgress": True, "isVoting": False,
            "deadline": None, "title": "T", "claims": [{"claimId": 1, "isAccepted": False}],
        }
        globals()["open_prs"] = lambda repo: {}
        snap, fails = sweep([1418], "o/r", 8453, check_links=False)
        checks.append(("sweep stamps swept_at, so a close can be judged against it",
                       isinstance(snap.get("swept_at"), (int, float))))
        checks.append(("and that stamp is a real clock reading, not a placeholder",
                       abs(snap.get("swept_at", 0) - time.time()) < 60))
        checks.append(("sweep records the bounty it was given", "1418" in snap.get("bounties", {})))
    finally:
        globals()["fetch_bounty_merged"], globals()["open_prs"] = _real_fetch, _real_prs

    # pr_links_with_claims ties a PR number to the claim that cites it, not just to a url.
    trip = pr_links_with_claims({"claims": [{"claimId": 8304, "title": "https://github.com/o/r/pull/316"}]})
    checks.append(("a PR link carries its claim id", trip == [("https://github.com/o/r/pull/316", "316", "8304")]))

    # THE REAL CLAIM THAT THE URL-ONLY MATCHER MISSED, verbatim. Claim 8329 on bounty 1421
    # names its pull request in words and carries no link, and the watcher reported
    # "PR-NEW #334 ... no claim cites it" while this claim cited it.
    real = pr_links_with_claims({"claims": [
        {"claimId": 8329, "title": "ZAOstock PR 334: skip autoplay hero video on mobile",
         "description": "https://poidhz.com/api/claim-meta"}]})
    # Indexed through a guard, not real[0]: when this regresses the list is EMPTY, and
    # real[0] would raise IndexError and hide every check after it. A crash tells you less
    # than a FAIL, which this suite learned the hard way on 2026-09-26.
    checks.append(("a PR named in words is found", [n for _, n, _ in real] == ["334"]))
    checks.append(("a PR named in words has no url to health-check",
                   bool(real) and real[0][0] is None))
    checks.append(("and it still carries its claim id", bool(real) and real[0][2] == "8329"))
    checks.append(("pr_links_in skips it, because there is nothing to fetch",
                   pr_links_in({"claims": [{"claimId": 8329, "title": "ZAOstock PR 334: x"}]}) == []))

    for text in ("PR #334", "pr 334", "Pull Request 334", "pull request #334"):
        got = [n for _, n, _ in pr_links_with_claims({"claims": [{"claimId": 1, "title": text}]})]
        checks.append((f"{text!r} is read as PR 334", got == ["334"]))

    # FALSE POSITIVES ARE THE WHOLE RISK OF WIDENING THIS. A bare number in prose must not
    # make some unrelated pull request an entry.
    for text in ("the pot is 334 dollars", "1,334 bytes saved", "in 2026 we shipped",
                 "APR 334", "EXPR 334", "PRs are welcome"):
        got = [n for _, n, _ in pr_links_with_claims({"claims": [{"claimId": 1, "title": text}]})]
        checks.append((f"{text!r} is NOT read as a PR reference", got == []))

    # A claim that gives both the link and the words counts the PR once.
    both = pr_links_with_claims({"claims": [
        {"claimId": 7, "title": "PR 316", "description": "https://github.com/o/r/pull/316"}]})
    checks.append(("a PR given as both a link and words is counted once", len(both) == 1))
    checks.append(("and the link form wins, so it can still be health-checked", both[0][0] is not None))

    # Two claims citing the same PR each keep their own row.
    two_claims = pr_links_with_claims({"claims": [
        {"claimId": 1, "title": "https://github.com/o/r/pull/316"},
        {"claimId": 2, "title": "https://github.com/o/r/pull/316"}]})
    checks.append(("two claims citing one PR keep both claim ids",
                   sorted(c for _, _, c in two_claims) == ["1", "2"]))

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
