#!/usr/bin/env python3
"""Refuse a bounty this repo has cast that org.config.json does not track.

WHY, MEASURED TWICE. `refresh-poidh-leaderboard.py` aggregates only the bounties in
`org.config.json`'s `default_bounty_ids`. A claim on any other bounty is invisible to it, so
its entrants score nothing and receive no $ZABAL.

  - 2026-09-07: R5's NINE claimants were scoring nothing because bounty 1330 was never added.
    Fixed by adding 1330.
  - 2026-09-21: bounty ONE (1409) had the same problem, found the first time a new round was
    cast after that fix. @predaking and @leoxcrane were on no leaderboard at all.

The fix both times was an entry in a list, which is not a fix - it is the same repair applied
twice. THE SYMPTOM IS INVISIBLE: a refresh that reads the wrong set still exits 0, still
writes valid files, and still prints a healthy-looking count. "38 entries" after a round
closed looks exactly like "38 entries" before it.

So this reads the bounty ids the REPO ITSELF publishes - every poidh bounty URL written in a
round's own markdown - and refuses any that `default_bounty_ids` omits. The repo already knows
what it cast; it just never told the config.

    python3 scripts/check-tracked-bounties.py
    python3 scripts/check-tracked-bounties.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BOUNTY_URL = re.compile(r"poidh\.xyz/(?:base|degen|arbitrum|\d+)/bounty/(\d+)")

# A URL in one of these is a reference to someone else's bounty or to a historical example,
# not a claim that WE cast it. Everything else under rounds/ is ours.
NOT_OURS = ("RATING.md", "IDEAS.md", "_template", "variants", "generated", "drafts")


def cast_bounty_ids(root: Path = REPO_ROOT) -> dict[int, list[str]]:
    """Every poidh bounty id this repo's own round files point at, with where each was found."""
    found: dict[int, list[str]] = {}
    rounds = root / "rounds"
    if not rounds.is_dir():
        return found
    for p in sorted(rounds.rglob("*.md")):
        rel = str(p.relative_to(root))
        if any(skip in rel for skip in NOT_OURS):
            continue
        for m in BOUNTY_URL.finditer(p.read_text()):
            found.setdefault(int(m.group(1)), []).append(rel)
    return found


def check(root: Path = REPO_ROOT) -> tuple[bool, list[str]]:
    cfg_path = root / "org.config.json"
    if not cfg_path.exists():
        return False, [f"FAIL: {cfg_path} is missing, so nothing could be checked"]
    cfg = json.loads(cfg_path.read_text())
    tracked = set(cfg.get("default_bounty_ids") or [])
    # A cast bounty may be deliberately excluded, but the reason has to be WRITTEN DOWN.
    # R4 (1249) is the real case: it was accidentally canceled, so its on-chain claim path is
    # closed and its builders were credited offchain instead. Aggregating it would credit
    # nobody. An exclusion with no reason is indistinguishable from the bug this file exists
    # to catch, so an empty or missing reason does not count as excluded.
    excluded = {int(k): v for k, v in (cfg.get("excluded_bounty_ids") or {}).items()
                if str(v).strip()}
    cast = cast_bounty_ids(root)

    if not cast:
        # An empty set is not a pass. Say which way it failed.
        return False, ["FAIL: found no bounty URLs under rounds/ at all. Either the layout "
                       "changed or the pattern is wrong. An empty search is not a clean bill "
                       "of health."]

    findings = [f"     {len(cast)} bounty id(s) referenced by round files; "
                f"{len(tracked)} tracked in org.config.json"]
    missing = sorted(set(cast) - tracked - set(excluded))
    for b in sorted(set(cast) & set(excluded)):
        findings.append(f"     bounty {b} excluded on purpose: {excluded[b][:90]}")
    for b in missing:
        where = ", ".join(sorted(set(cast[b]))[:3])
        findings.append(
            f"FAIL: bounty {b} is cast and written into {where}, but is NOT in "
            f"default_bounty_ids. Its entrants score nothing and receive no $ZABAL, and the "
            f"leaderboard refresh will still exit 0 while ignoring them.")
    if not missing:
        findings.append("PASS: every bounty this repo has cast is tracked")
    return not missing, findings


def _selftest() -> bool:
    import tempfile
    passed = True

    def c(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "rounds" / "r1").mkdir(parents=True)
        (root / "rounds" / "r1" / "README.md").write_text(
            "live at https://poidh.xyz/base/bounty/1151\n")
        (root / "org.config.json").write_text(json.dumps({"default_bounty_ids": [1151]}))
        ok, f = check(root)
        c("passes when the cast bounty is tracked", ok and any("PASS" in x for x in f))

        # The real 2026-09-21 defect.
        (root / "rounds" / "daily").mkdir()
        (root / "rounds" / "daily" / "d01").mkdir()
        (root / "rounds" / "daily" / "d01" / "README.md").write_text(
            "Live: https://poidh.xyz/base/bounty/1409\n")
        ok, f = check(root)
        c("catches a cast bounty that is NOT tracked",
          not ok and any("bounty 1409" in x and "NOT in" in x for x in f))
        c("the finding names the file it was found in",
          any("rounds/daily/d01/README.md" in x for x in f))

        # A template or a variant is not evidence that we cast anything.
        (root / "rounds" / "daily" / "_template").mkdir()
        (root / "rounds" / "daily" / "_template" / "description.md").write_text(
            "see https://poidh.xyz/base/bounty/9999\n")
        ok, f = check(root)
        c("a _template reference is NOT treated as cast",
          not any("bounty 9999" in x for x in f))

        # A DECLARED exclusion passes; an undeclared or reasonless one does not.
        (root / "org.config.json").write_text(json.dumps(
            {"default_bounty_ids": [1151], "excluded_bounty_ids": {"1409": "canceled, credited offchain"}}))
        ok, f = check(root)
        c("a declared exclusion with a reason passes", ok)
        c("and it is reported, not silent", any("excluded on purpose" in x for x in f))
        (root / "org.config.json").write_text(json.dumps(
            {"default_bounty_ids": [1151], "excluded_bounty_ids": {"1409": "  "}}))
        ok, _ = check(root)
        c("an exclusion with a BLANK reason still fails", not ok)

        # An empty search must fail rather than pass silently.
        import shutil
        shutil.rmtree(root / "rounds")
        (root / "rounds").mkdir()
        ok, f = check(root)
        c("an empty search FAILS rather than reporting clean",
          not ok and any("empty search" in x for x in f))
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        print("check-tracked-bounties selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    ok, findings = check()
    for f in findings:
        print(f"  {f}")
    if not ok:
        print("\nAdd the missing id(s) to default_bounty_ids in org.config.json and re-run\n"
              "scripts/refresh-poidh-leaderboard.py, or those entrants stay unpaid.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
