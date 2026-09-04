#!/usr/bin/env python3
"""
Platform-wide POID bounty dashboard builder (loop-night follow-up to
scan-poidh-deadlines.py / build-bounty-calendar.py, per Zaal's ask for "a good UI
calendar that reads if any have submissions and has a bounty with a timer... and
also like /10 ease of getting right away, difficulty, date, money, and other
interesting parameters").

Scans the live platform-wide POID bounty feed (bounties.fetchAll, open + in-progress)
and, for each bounty, computes:

  - has_submissions: straight from POID's own `hasClaims` field (no extra API calls)
  - deadline: same free-text extraction as scan-poidh-deadlines.py (POID has no
    structured deadline field in practice - see that script's docstring)
  - money: bounty amount in ETH + a live-converted USD estimate
  - ease (1-10) / difficulty (1-10): a documented HEURISTIC, not ground truth -
    see score_bounty() below for the exact rule. Flagged as "estimated" in the
    output and in the UI - these are keyword/format-based guesses, not judged by
    a human or an LLM reading the actual submission bar.

Writes data/bounty-dashboard.json for docs/bounty-dashboard.html to render.

    python3 scripts/build-bounty-dashboard.py [--pages 6] [--limit 25]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deadline_parser import extract_deadline  # shared free-text deadline parser

REPO_ROOT = Path(__file__).resolve().parent.parent
POIDH_BASE = "https://poidh.xyz/api/trpc"
UA = "Mozilla/5.0 (zpoidh-bounty-dashboard-builder)"


def load_org_config() -> dict:
    """Read org.config.json if present - forking zpoidh for your own org? Edit
    that file's "default_chain_id" instead of this script. Missing file/key
    falls back to Base mainnet (8453), the original hardcoded default."""
    path = REPO_ROOT / "org.config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


_CFG = load_org_config()


# Keyword buckets for the ease/difficulty heuristic. Order matters - checked
# in this order, first match wins the task-type classification.
TASK_TYPES = [
    # (label, keywords, ease, difficulty)
    ("code", ["pull request", " pr ", "github.com", "repo", "bug fix", "fix a bug",
               "codebase", "smart contract", "deploy", " api ", "typescript", "python"],
     3, 8),
    ("build", ["build a", "app", "mini app", "miniapp", "frame", "prototype", "tool"],
     4, 7),
    ("writing", ["thread", "write-up", "writeup", "essay", "article", "blog post"],
     5, 5),
    ("clip", ["clip", "video", "highlight", "edit", "reel", "60 second", "30-60",
               "30–60"],
     7, 4),
    ("photo", ["photo", "screenshot", "picture", "selfie"],
     9, 2),
    ("social", ["cast", "post", "tag", "share", "repost", "recast"],
     8, 2),
]
DEFAULT_EASE, DEFAULT_DIFFICULTY = 6, 5


def trpc(proc: str, payload: dict) -> dict:
    inp = urllib.parse.quote(json.dumps({"0": {"json": payload}}))
    req = urllib.request.Request(
        f"{POIDH_BASE}/{proc}?batch=1&input={inp}", headers={"User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())[0]["result"]["data"]["json"]


# POID's `amount` field is denominated in the NATIVE token of whatever chain the
# bounty lives on - Base/Arbitrum/Mainnet pay in ETH, Degen Chain pays in DEGEN.
# Treating every amount as ETH (an earlier version of this script did) produced a
# nonsense "13,014 ETH" reading on a real bounty that was actually 13,014 DEGEN
# (~$16). Chain IDs per docs.poidh.xyz.
CHAIN_TOKENS = {
    8453: ("ETH", "ethereum"),
    42161: ("ETH", "ethereum"),
    1: ("ETH", "ethereum"),
    666666666: ("DEGEN", "degen-base"),
}


def fetch_token_prices() -> dict:
    ids = ",".join(sorted({cg_id for _, cg_id in CHAIN_TOKENS.values()}))
    try:
        req = urllib.request.Request(
            f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd",
            headers={"User-Agent": UA},
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
        return {cg_id: data.get(cg_id, {}).get("usd") for _, cg_id in CHAIN_TOKENS.values()}
    except Exception as e:
        print(f"  WARN: token price fetch failed, USD estimates will be null: {e}")
        return {}




def score_bounty(title: str, description: str) -> dict:
    """HEURISTIC ease/difficulty score - keyword + task-type based, not a human
    or LLM judgment call. Documented here so it's auditable, not a black box:

    1. Classify task type by the first keyword bucket that matches (title+desc,
       case-insensitive). Each bucket has a hand-set (ease, difficulty) pair
       reflecting "how easy is it to just go do this right now" vs "how much
       skill/effort does doing it WELL take."
    2. No match -> default middle score (6 ease / 5 difficulty), flagged as
       "unclassified" so the UI can show it distinctly from a real classification.
    """
    text = f"{title} {description}".lower()
    for label, keywords, ease, difficulty in TASK_TYPES:
        if any(kw in text for kw in keywords):
            return {"task_type": label, "ease": ease, "difficulty": difficulty, "classified": True}
    return {"task_type": "unclassified", "ease": DEFAULT_EASE, "difficulty": DEFAULT_DIFFICULTY, "classified": False}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pages", type=int, default=6, help="pages per status to scan")
    p.add_argument("--limit", type=int, default=25, help="bounties per page")
    p.add_argument("--chain", type=int, default=_CFG.get("default_chain_id", 8453))
    args = p.parse_args()

    token_prices = fetch_token_prices()
    now_iso = datetime.now(timezone.utc).isoformat()
    bounties = []
    fetch_errors: list[str] = []

    for status in ("open", "progress"):
        cursor = None
        for page in range(args.pages):
            payload = {"chainId": args.chain, "status": status, "limit": args.limit}
            if cursor is not None:
                payload["cursor"] = cursor
            try:
                d = trpc("bounties.fetchAll", payload)
            except Exception as e:
                print(f"  WARN: {status} page {page} fetch failed: {e}")
                fetch_errors.append(f"{status} page {page}: {e}")
                break

            items = d.get("items", [])
            if not items:
                break
            cursor = d.get("nextCursor")

            for b in items:
                if b.get("isCanceled"):
                    continue
                desc = b.get("description", "") or ""
                deadline_iso, deadline_raw = extract_deadline(desc, created_at=b.get("createdAt"))
                chain_id = b.get("chainId")
                symbol, cg_id = CHAIN_TOKENS.get(chain_id, ("ETH", "ethereum"))
                amount_native = int(b.get("amount", "0") or 0) / 1e18
                price = token_prices.get(cg_id)
                score = score_bounty(b.get("title", ""), desc)

                bounties.append(
                    {
                        "bounty_id": b["id"],
                        "chain_id": chain_id,
                        "title": (b.get("title") or "")[:140],
                        "issuer": b.get("issuer"),
                        "created_at": b.get("createdAt"),
                        "status": status,
                        "is_multiplayer": bool(b.get("isMultiplayer")),
                        "is_voting": bool(b.get("isVoting")),
                        "has_submissions": bool(b.get("hasClaims")),
                        "has_participants": bool(b.get("hasParticipants")),
                        "amount_native": round(amount_native, 5),
                        "amount_token_symbol": symbol,
                        "amount_usd": round(amount_native * price, 2) if price else None,
                        "deadline_iso": deadline_iso,
                        "deadline_raw_text": deadline_raw,
                        "url": f"https://poidh.xyz/base/bounty/{b['id']}",
                        **score,
                    }
                )

            if cursor is None:
                break
            time.sleep(0.25)

    # de-dupe (a bounty could theoretically span "open" and "progress" scans if it
    # transitioned mid-run) - keep the later-seen (progress) entry
    by_id = {}
    for b in bounties:
        by_id[b["bounty_id"]] = b
    bounties = list(by_id.values())

    # Sort: has a deadline first (soonest first), then no-deadline ones after.
    # Rank by USD (not native amount) so a DEGEN bounty and an ETH bounty compare
    # on the same axis instead of DEGEN's larger native numbers always sorting first.
    bounties.sort(key=lambda b: (b["deadline_iso"] is None, b["deadline_iso"] or "", -(b["amount_usd"] or 0)))

    out = {
        "generated_at": now_iso,
        "token_usd_prices": token_prices,
        "token_usd_prices_source": "coingecko.com (live at build time)" if token_prices else None,
        "scoring_methodology": (
            "ease and difficulty are a KEYWORD-BASED HEURISTIC estimate (see "
            "score_bounty() in scripts/build-bounty-dashboard.py), not a human or "
            "LLM judgment reading the actual bounty bar. Treat as a rough sort "
            "signal, not ground truth. 'unclassified' bounties got a flat "
            f"default ({DEFAULT_EASE}/10 ease, {DEFAULT_DIFFICULTY}/10 difficulty) because no "
            "keyword bucket matched their title/description."
        ),
        "total_bounties": len(bounties),
        "with_deadline": sum(1 for b in bounties if b["deadline_iso"]),
        "with_submissions_already": sum(1 for b in bounties if b["has_submissions"]),
        "bounties": bounties,
    }

    out_path = REPO_ROOT / "data" / "bounty-dashboard.json"

    # A transient upstream failure used to look exactly like "the platform has no
    # bounties": the fetch raised, we broke out of the page loop, wrote an empty
    # list, and returned 0. The refresh workflow then saw a substantive diff and
    # committed the wipe. That is what happened at 07:09Z on 2026-08-23, when
    # 431f7ea replaced 100 live listings with total_bounties: 0, and it self-healed
    # six hours later only because the next scheduled run happened to succeed.
    #
    # Empty is never a real answer here, so treat it as the failure it is and
    # leave the last good file untouched.
    if not bounties:
        print("ERROR: scanned 0 bounties, refusing to overwrite "
              f"{out_path.relative_to(REPO_ROOT)}.", file=sys.stderr)
        for err in fetch_errors:
            print(f"  fetch error: {err}", file=sys.stderr)
        if not fetch_errors:
            print("  no fetch errors recorded, so the upstream feed itself "
                  "returned an empty page set.", file=sys.stderr)
        return 1

    # A partial fetch is not safe to publish either. If some pages failed we hold
    # a truncated list, which reads as bounties having disappeared rather than as
    # a broken run.
    if fetch_errors:
        print(f"ERROR: {len(fetch_errors)} page fetch(es) failed, so the "
              f"{len(bounties)} bounties collected are an incomplete set. "
              f"Refusing to overwrite {out_path.relative_to(REPO_ROOT)}.",
              file=sys.stderr)
        for err in fetch_errors:
            print(f"  fetch error: {err}", file=sys.stderr)
        return 1

    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Scanned {len(bounties)} live bounties ({out['with_deadline']} with a parseable deadline, "
          f"{out['with_submissions_already']} already have submissions).")
    print(f"Token prices: {token_prices if token_prices else 'unavailable'}")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
