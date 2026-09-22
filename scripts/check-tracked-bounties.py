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


def check_cast_rounds_are_live(cfg: dict, cast: dict[int, list[str]]) -> list[str]:
    """A round whose folder holds a cast bounty must be in `rounds`, not `planned_rounds`.

    WHY, MEASURED 2026-09-22. `refresh-rounds.py` walks `rounds` and asks poidh for live state.
    It walks `planned_rounds` separately and writes status DRAFT with no bounty_id, because a
    planned round has nothing to look up. Bounty one was cast on 2026-09-20 and its config
    entry was never moved, so the feed carried a daily-01 row with every field null, and
    /about rendered "No round is open right now" FOR TWO DAYS while a bounty was open and
    another was in its contributor vote.

    That is the worst shape of this bug: the page was not stale, it was faithfully rendering a
    feed that did not know the round existed, so every check of the page and of the feed agreed
    with each other and all of them were wrong.

    The stale row also carried a note reading "$25, ... closes Mon 2026-09-21 6pm Eastern,
    decided in Discord". The pot was about $9.84, it closed at 4pm, and it was decided on
    Twitch. Three wrong facts nobody re-read, because a DRAFT row is not something anyone
    thinks to check.

    Eleven more daily rounds are coming, so this is a mechanism rather than a note."""
    findings = []
    planned = {str(r.get("round")): r for r in (cfg.get("planned_rounds") or [])}
    live_folders = {r.get("folder") for r in (cfg.get("rounds") or []) if r.get("folder")}
    # A bounty already owned by a live round is not evidence that some OTHER folder cast it.
    # Caught by this guard failing on its first real run: rounds/r7 mentions bounty 1330
    # because its files discuss R5's winner and a retainer offer to them, and 1330 is R5's.
    # Without this, every folder that merely DISCUSSES another round gets flagged, which is a
    # guard that cries wolf - and a guard that cries wolf gets switched off.
    owned = {r.get("bounty_id") for r in (cfg.get("rounds") or []) if r.get("bounty_id")}

    for bid, files in sorted(cast.items()):
        if bid in owned:
            continue
        folders = {str(Path(f).parent) for f in files}
        for folder in folders:
            if folder in live_folders:
                continue
            hit = next((k for k, r in planned.items() if r.get("folder") == folder), None)
            if hit:
                findings.append(
                    f"FAIL: {folder} has cast bounty {bid}, but config still lists it under "
                    f"planned_rounds as '{hit}'. refresh-rounds.py writes DRAFT with no "
                    f"bounty_id for a planned round, so /about will say no round is open while "
                    f"this one is. Move it to `rounds` with its bounty_id and a label.")
    return findings


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
    stale = check_cast_rounds_are_live(cfg, cast)
    findings.extend(stale)

    if not missing and not stale:
        findings.append("PASS: every bounty this repo has cast is tracked, and every cast "
                        "round is in `rounds` rather than `planned_rounds`")
    return (not missing and not stale), findings


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

        # --- the planned-vs-cast guard, added 2026-09-22 ---
        # This is the EXACT shape the config was in while /about said no round was open.
        prefix = {"default_bounty_ids": [1151, 1409],
                  "rounds": [{"round": 1, "bounty_id": 1151, "folder": "rounds/r1"}],
                  "planned_rounds": [{"round": "daily-01", "folder": "rounds/daily/d01"}]}
        (root / "org.config.json").write_text(json.dumps(prefix))
        ok, f = check(root)
        c("catches a CAST round still sitting in planned_rounds",
          not ok and any("still lists it under planned_rounds" in x for x in f))
        c("and the finding names the bounty and the folder",
          any("1409" in x and "rounds/daily/d01" in x for x in f))

        fixed = {"default_bounty_ids": [1151, 1409],
                 "rounds": [{"round": 1, "bounty_id": 1151, "folder": "rounds/r1"},
                            {"round": "daily-01", "bounty_id": 1409,
                             "folder": "rounds/daily/d01"}],
                 "planned_rounds": []}
        (root / "org.config.json").write_text(json.dumps(fixed))
        ok, f = check(root)
        c("passes once the cast round is moved into `rounds`", ok)

        # The real false positive this guard produced on its first run: a folder that merely
        # DISCUSSES another round's bounty must not be treated as having cast it.
        discuss = {"default_bounty_ids": [1151, 1409],
                   "rounds": [{"round": 1, "bounty_id": 1151, "folder": "rounds/r1"},
                              {"round": "daily-01", "bounty_id": 1409,
                               "folder": "rounds/daily/d01"}],
                   "planned_rounds": [{"round": 7, "folder": "rounds/r7"}]}
        (root / "rounds" / "r7").mkdir(parents=True, exist_ok=True)
        (root / "rounds" / "r7" / "outreach.md").write_text(
            "offer the R1 winner (https://poidh.xyz/base/bounty/1151) a retainer\n")
        (root / "org.config.json").write_text(json.dumps(discuss))
        ok, f = check(root)
        c("a folder that merely DISCUSSES another round's bounty is not flagged",
          ok and not any("rounds/r7" in x for x in f))
        import shutil as _sh
        _sh.rmtree(root / "rounds" / "r7")

        # A round that is genuinely planned and has cast nothing must NOT be flagged.
        planned_only = dict(fixed)
        planned_only["planned_rounds"] = [{"round": 9, "folder": "rounds/r9"}]
        (root / "org.config.json").write_text(json.dumps(planned_only))
        ok, _ = check(root)
        c("a genuinely planned round with no cast bounty is left alone", ok)

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
