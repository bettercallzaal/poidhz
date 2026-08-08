#!/usr/bin/env python3
"""
Verify Empire Builder's LIVE leaderboard actually matches what zpoidh generates - the
integration between refresh-poidh-leaderboard.py and Empire Builder is a pull, not a
push (EB fetches from a configured `api_endpoint` URL on its own schedule), which means
a wrong or stale `api_endpoint` on EB's side can silently drift for weeks with zpoidh's
own generated data looking perfectly correct the whole time. This script catches that
class of bug by comparing EB's live leaderboard against zpoidh's own freshly-generated
data/leaderboard.json, not just trusting the two are in sync.

Real bug this script would have caught (found 2026-08-08, still unfixed as of writing):
Empire Builder's "POIDH Submitters" leaderboard has `api_endpoint` set to
bettercallzaal.com/poidh-leaderboard.json - a stale, pre-zpoidh URL, not this repo's own
zpoidh.vercel.app/leaderboard. Live diff: EB has 16 entries, zpoidh generates 22 - missing
6 real submitters entirely, including the actual R3 winner (femmie), whose wallet isn't
in EB's feed at all. Three more wallets have understated scores. This is NOT fixable by
this script or any code change here - EB's own leaderboard admin dashboard needs the
api_endpoint field corrected by someone with access (per Empire Builder's own docs, that's
a manual dashboard action, not an API call). This script's job is to make that drift loud
and re-detectable, not to fix it.

    python3 scripts/check-eb-sync.py                 # compare EB live vs data/leaderboard.json on disk
    python3 scripts/check-eb-sync.py --regenerate     # also re-run refresh-poidh-leaderboard.py first
    python3 scripts/check-eb-sync.py --selftest       # no network

Exit code 0 = in sync (or no real drift beyond score-ordering). Exit code 1 = real drift
found (missing addresses, score mismatches, or a misconfigured api_endpoint) - meant to be
CI/cron-friendly so a scheduled run can alert rather than assume the sync is healthy.
"""

import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_org_config() -> dict:
    """Read org.config.json if present - forking zpoidh for your own org? Edit that
    file's "site_url"/"empire_leaderboard_uuid" instead of this script."""
    path = REPO_ROOT / "org.config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


_CFG = load_org_config()
SITE_URL = _CFG.get("site_url", "https://zpoidh.vercel.app")
LEADERBOARD_UUID = _CFG.get("empire_leaderboard_uuid", "7b8e8dfa-529d-48ad-8c9b-bdb45cc35187")
EB_API_BASE = "https://www.empirebuilder.world/api"

UA = "Mozilla/5.0 (zpoidh-eb-sync-check)"


def http_get(url: str, timeout: int = 15) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def fetch_eb_leaderboard_meta() -> dict:
    return http_get(f"{EB_API_BASE}/leaderboards/{LEADERBOARD_UUID}")


def load_local_feed() -> list[dict]:
    path = REPO_ROOT / "data" / "leaderboard.json"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found - run scripts/refresh-poidh-leaderboard.py first, "
            "or pass --regenerate to this script"
        )
    return json.loads(path.read_text())


def compare(local_feed: list[dict], eb_entries: list[dict]) -> dict:
    """Real comparison logic, pure function so it's covered by --selftest without
    any network calls."""
    local_by_addr = {e["address"].lower(): e["score"] for e in local_feed}
    eb_by_addr = {e["address"].lower(): e.get("score") for e in eb_entries}

    missing_from_eb = sorted(set(local_by_addr) - set(eb_by_addr))
    extra_in_eb = sorted(set(eb_by_addr) - set(local_by_addr))
    score_mismatches = [
        {"address": a, "local_score": local_by_addr[a], "eb_score": eb_by_addr[a]}
        for a in sorted(set(local_by_addr) & set(eb_by_addr))
        if local_by_addr[a] != eb_by_addr[a]
    ]

    return {
        "local_count": len(local_by_addr),
        "eb_count": len(eb_by_addr),
        "missing_from_eb": missing_from_eb,
        "extra_in_eb": extra_in_eb,
        "score_mismatches": score_mismatches,
        "in_sync": not missing_from_eb and not extra_in_eb and not score_mismatches,
    }


def check_endpoint_config(eb_meta: dict) -> dict:
    """Confirm EB's own leaderboard config actually points at THIS org's hosted
    feed, not a stale or unrelated URL. This is the root-cause check - a script can
    regenerate a perfect feed forever and it will never reach EB if this is wrong."""
    configured = ((eb_meta.get("leaderboard") or {}).get("api_endpoint") or "").rstrip("/")
    expected = f"{SITE_URL.rstrip('/')}/leaderboard"
    return {
        "configured_endpoint": configured,
        "expected_endpoint": expected,
        "matches": configured == expected,
    }


def _selftest() -> int:
    """No network. Proves the comparison logic catches missing addresses and score
    mismatches - the exact real-world drift this script exists to detect."""
    local_feed = [
        {"address": "0xAAA", "score": 2},
        {"address": "0xBBB", "score": 1},
        {"address": "0xCCC", "score": 1},  # this one is the "R3 winner" case - missing from EB entirely
    ]
    eb_entries = [
        {"address": "0xaaa", "score": 1},  # score understated on EB's side (case-insensitive match)
        {"address": "0xbbb", "score": 1},  # matches
        {"address": "0xddd", "score": 1},  # present on EB but not in the local feed
    ]
    result = compare(local_feed, eb_entries)

    checks = [
        ("detects the address entirely missing from EB", "0xccc" in result["missing_from_eb"]),
        ("detects the score mismatch (2 local vs 1 on EB)", any(m["address"] == "0xaaa" and m["local_score"] == 2 and m["eb_score"] == 1 for m in result["score_mismatches"])),
        ("detects the extra EB-only address", "0xddd" in result["extra_in_eb"]),
        ("correctly reports NOT in sync when real drift exists", result["in_sync"] is False),
        ("address comparison is case-insensitive", len(result["missing_from_eb"]) == 1),
    ]

    endpoint_check_bad = check_endpoint_config({"leaderboard": {"api_endpoint": "https://bettercallzaal.com/poidh-leaderboard.json"}})
    endpoint_check_good = check_endpoint_config({"leaderboard": {"api_endpoint": f"{SITE_URL}/leaderboard"}})
    checks.append(("flags a stale/wrong api_endpoint", endpoint_check_bad["matches"] is False))
    checks.append(("accepts the correct api_endpoint", endpoint_check_good["matches"] is True))

    fails = 0
    for label, ok in checks:
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    print(f"selftest: {len(checks) - fails}/{len(checks)} passed")
    return 1 if fails else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--regenerate", action="store_true", help="run refresh-poidh-leaderboard.py first")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    if args.regenerate:
        print("Regenerating local feed via refresh-poidh-leaderboard.py...")
        r = subprocess.run(["python3", str(REPO_ROOT / "scripts" / "refresh-poidh-leaderboard.py"), "--skip-web3bio"], cwd=REPO_ROOT)
        if r.returncode != 0:
            print("ERROR: refresh-poidh-leaderboard.py failed, cannot verify against stale/missing data")
            return 1

    try:
        local_feed = load_local_feed()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1

    print("Fetching Empire Builder's live leaderboard...")
    try:
        eb_meta = fetch_eb_leaderboard_meta()
    except Exception as e:
        print(f"ERROR: could not reach Empire Builder API: {e}")
        return 1

    if not eb_meta.get("success"):
        print("ERROR: Empire Builder API returned success=false")
        return 1

    eb_entries = ((eb_meta.get("leaderboard") or {}) and eb_meta.get("entries")) or []

    endpoint = check_endpoint_config(eb_meta)
    result = compare(local_feed, eb_entries)

    print(f"\nEmpire Builder api_endpoint check:")
    print(f"  Configured: {endpoint['configured_endpoint']}")
    print(f"  Expected:   {endpoint['expected_endpoint']}")
    print(f"  {'OK - matches' if endpoint['matches'] else 'MISMATCH - EB is not pulling from this repo at all'}")

    print(f"\nLeaderboard comparison ({result['local_count']} local vs {result['eb_count']} on EB):")
    if result["missing_from_eb"]:
        print(f"  MISSING FROM EB ({len(result['missing_from_eb'])} addresses present locally, absent on EB):")
        for a in result["missing_from_eb"]:
            print(f"    {a}")
    if result["extra_in_eb"]:
        print(f"  EXTRA ON EB ({len(result['extra_in_eb'])} addresses on EB not in the local feed - may be from a different bounty set):")
        for a in result["extra_in_eb"]:
            print(f"    {a}")
    if result["score_mismatches"]:
        print(f"  SCORE MISMATCHES ({len(result['score_mismatches'])}):")
        for m in result["score_mismatches"]:
            print(f"    {m['address']}: local={m['local_score']} eb={m['eb_score']}")

    real_drift = not result["in_sync"] or not endpoint["matches"]
    if not real_drift:
        print("\nIn sync - Empire Builder's live leaderboard matches this repo's generated feed.")
    else:
        print("\nNOT IN SYNC. If the api_endpoint mismatch above is the cause, this needs a manual")
        print("fix in Empire Builder's own leaderboard admin dashboard (not a code change here) -")
        print("point api_endpoint at the 'Expected' URL above.")

    return 1 if real_drift else 0


if __name__ == "__main__":
    sys.exit(main())
