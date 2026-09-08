#!/usr/bin/env python3
"""
Turn the advisory cron checks into a committed artifact, so their findings cannot go quiet.

Three checks now run on the 6h workflow as continue-on-error - the closeout sweep, the
Empire Builder drift check, and the re-check-date sweep. That was the right call: a red
build every six hours over something only a human can action trains everyone to ignore red.

But it creates the opposite failure. A check whose only output is a log line nobody opens
is an inverted alarm: it goes quiet exactly when it has something to say. This repo spent
the week on the mirror of that - records that stay loud after they stop being true - and
the two are the same bug from opposite ends.

So the findings go into data/health.json, which the workflow already commits. Then:
  - drift shows up in a git diff, on a branch someone reviews
  - the numbers are queryable, CORS-open, like the rest of data/
  - "seven broken promises" is a value in a file rather than a line in a log

    python3 scripts/health-report.py                 # write data/health.json
    python3 scripts/health-report.py --print         # write and show it
    python3 scripts/health-report.py --selftest      # offline

Always exits 0. This reports; it does not judge. The checks it summarises keep their own
exit codes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "data" / "health.json"


def promises() -> dict:
    """Per-round promise state, read straight from the ledgers."""
    rounds, totals = {}, {"kept": 0, "broken": 0, "na": 0, "unrecorded": 0}
    for p in sorted(REPO_ROOT.glob("rounds/r*/closeout.json")):
        try:
            rows = json.loads(p.read_text()).get("promises", [])
        except Exception:
            continue
        counts = {}
        for r in rows:
            s = r.get("status", "unrecorded")
            counts[s] = counts.get(s, 0) + 1
            if s in totals:
                totals[s] += 1
        rounds[p.parent.name] = counts
    return {"by_round": rounds, "totals": totals,
            "still_owed": totals["broken"] + totals["unrecorded"]}


def recheck() -> dict:
    """Time-bound claims and whether any have gone unverified."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "rc", REPO_ROOT / "scripts" / "recheck-dates.py")
    if spec is None or spec.loader is None:
        return {"error": "recheck-dates.py not importable"}
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    today = dt.date.today()
    rows = m.find_dates(REPO_ROOT)
    return {
        "total": len(rows),
        "passed": [{"file": str(p.relative_to(REPO_ROOT)), "line": ln, "due": str(d)}
                   for p, ln, d, _ in rows if d < today],
        "upcoming": [{"file": str(p.relative_to(REPO_ROOT)), "line": ln, "due": str(d)}
                     for p, ln, d, _ in rows if d >= today],
    }


def gates() -> dict:
    """Which drafts are currently unsendable, and why."""
    r = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "send-gate.py"), "--all"],
                       capture_output=True, text=True, cwd=REPO_ROOT)
    blocked = [ln.split()[1] for ln in r.stdout.splitlines()
               if ln.strip().startswith("BLOCKED")]
    open_ = [ln.split()[1] for ln in r.stdout.splitlines()
             if ln.strip().startswith("OPEN")]
    return {"blocked": blocked, "open": open_}


def build() -> dict:
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "note": ("Findings from the advisory cron checks. They run continue-on-error so a "
                 "human-only problem does not red-build every six hours - which means their "
                 "output would otherwise live only in logs nobody opens. This file is the "
                 "half that stays visible."),
        "promises": promises(),
        "recheck_dates": recheck(),
        "send_gates": gates(),
    }


def _summary(d: dict) -> None:
    p = d["promises"]
    print(f"  promises: {p['totals']['broken']} broken, "
          f"{p['totals']['unrecorded']} unrecorded, {p['still_owed']} still owed")
    print(f"  re-check dates: {len(d['recheck_dates']['passed'])} passed, "
          f"{d['recheck_dates']['total']} total")
    print(f"  send gates: {len(d['send_gates']['blocked'])} blocked, "
          f"{len(d['send_gates']['open'])} open")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--print", action="store_true", dest="show")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        print("health-report selftest")
        passed = True

        def check(label: str, cond: bool) -> None:
            nonlocal passed
            print(f"  {'ok  ' if cond else 'FAIL'} {label}")
            passed = passed and cond

        d = build()
        check("has all three sections",
              {"promises", "recheck_dates", "send_gates"} <= set(d))
        check("promise totals are counted",
              sum(d["promises"]["totals"].values()) > 0)
        check("still_owed is broken plus unrecorded",
              d["promises"]["still_owed"] ==
              d["promises"]["totals"]["broken"] + d["promises"]["totals"]["unrecorded"])
        check("re-check dates were found", d["recheck_dates"]["total"] >= 3)
        check("send gates were evaluated",
              isinstance(d["send_gates"]["blocked"], list))
        check("serialises to JSON", isinstance(json.dumps(d), str))
        print("selftest:", "passed" if passed else "FAILED")
        return 0 if passed else 1

    d = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # Only write when something SUBSTANTIVE changed. generated_at moves on every run, so
    # writing unconditionally would commit this file four times a day whether or not
    # anything happened - and a file that changes constantly is one nobody looks at, which
    # is the failure this artifact exists to prevent, rebuilt one level up.
    def substance(x: dict) -> str:
        return json.dumps({k: v for k, v in x.items() if k != "generated_at"}, sort_keys=True)

    if OUT.exists():
        try:
            if substance(json.loads(OUT.read_text())) == substance(d):
                print(f"{OUT.relative_to(REPO_ROOT)} unchanged - nothing to commit")
                _summary(d)
                return 0
        except Exception:
            pass

    OUT.write_text(json.dumps(d, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")
    _summary(d)
    if a.show:
        print()
        print(json.dumps(d, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
