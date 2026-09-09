#!/usr/bin/env python3
"""Does the public site still say things that stopped being true?

Two rules, both entrant-facing, both found live on 2026-09-08:

  1. NO INVITATION TO A CLOSED ROUND. poidhz.com/hub carried "Round 2 - Live now",
     "Closes Fri May 22" and a "Submit on POIDH" button for bounty 1166, which closed
     2026-05-22. It had been inviting submissions to a closed bounty for 15 weeks. The
     ZABAL Gamez brand kit - a CC-BY page other people mirror - said "Active bounty ...
     closes Sun Jun 14" for bounty 1180 for nearly three months.

  2. NO DEAD INTERNAL LINK. That same card linked /poidh-round2-judging.html and
     /poidh-bounty-best-practices.html, both pre-migration paths, both 404 in production,
     verified with curl the same day.

Why a script rather than a fix: each one was fixed by hand, and a hand fix is only as
durable as the next person's memory. The repo has measured that enforced rules run at
about 100% and honor-system rules at 3-40%.

Round state comes from data/rounds-live.json, which refresh-rounds.py regenerates from
chain every 6h - so this cannot disagree with poidh unless poidh does. That file exists
because bounty 1249 sat marked LIVE for six weeks after it was canceled.

    python3 scripts/check-site-claims.py
    python3 scripts/check-site-claims.py --selftest    # offline, no network
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# A round can honestly ask for a submission in exactly these two states. Anything else -
# WINNER SET, CLOSED, CANCELED, UNKNOWN - must not sit next to an invitation.
CAN_SUBMIT = frozenset({"OPEN", "VOTING"})

# Phrases that ask the reader to act on a round NOW. "View the bounty" and "See the
# submissions" are deliberately absent: linking to a closed round is fine, inviting
# someone into it is not.
INVITATION = re.compile(
    r"(?i)\bsubmit (?:your|on|it|here)\b|\bbe the first\b|\benter now\b|\blive now\b"
    r"|\bclos(?:es|ing)\b\s+(?:on\s+)?(?:mon|tue|wed|thu|fri|sat|sun)"
    r"|\bactive bounty\b|\bopen now\b"
)

# How far either side of a bounty link to look for an invitation. Wide enough to catch a
# CTA in the same card, narrow enough not to reach the next section.
WINDOW = 320


def load_round_status() -> dict[int, str]:
    p = REPO_ROOT / "data" / "rounds-live.json"
    feed = json.loads(p.read_text())
    return {r["bounty_id"]: r.get("status", "UNKNOWN")
            for r in feed.get("rounds", []) if r.get("bounty_id")}


def strip_comments(html: str) -> str:
    """HTML comments explain the fix and quote the old wording, so they trip every rule
    they document. The comment on the hub card contains the literal string this checker
    bans, which made the checker fail on the very change that fixed the bug."""
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    # Same for a JS line comment, for the same reason: the comment explaining why "Be the
    # first" was removed contains "Be the first", and the checker flagged its own fix.
    # Only a line that STARTS with // is dropped, so "https://..." inside code survives.
    return re.sub(r"(?m)^[ \t]*//.*$", " ", html)


def stale_invitations(html: str, status: dict[int, str]) -> list[str]:
    text = strip_comments(html)
    out = []
    for m in re.finditer(r"poidh\.xyz/\w+/bounty/(\d+)", text):
        bid = int(m.group(1))
        st = status.get(bid)
        if st is None or st in CAN_SUBMIT:
            continue
        seg = text[max(0, m.start() - WINDOW):m.end() + WINDOW]
        hit = INVITATION.search(seg)
        if hit:
            out.append(f"bounty {bid} is {st} but the page says {hit.group(0)!r} beside it")
    return sorted(set(out))


# Claims that a round is running right now. Checked against the feed rather than against a
# nearby link, because the worst instance had no link at all: /about's meta description and
# og:description said "Currently R5 active ... through Sun Aug 30, 2026" - the text search
# results and link previews show, cached by other people's systems, with nothing on the page
# to reveal it had gone stale.
#
# "live leaderboard", "live from poidh" and "read live" are ordinary and must not match, so
# every pattern here ties the word to a ROUND or a bounty, never to data.
LIVE_CLAIMS = [
    r"(?i)\bcurrently R\d+\b",
    r"(?i)\bR\d+\b[^.]{0,40}\b(?:is live|active|live through)\b",
    r"(?i)\blive now\b",
    r"(?i)\bactive bounty\b",
    r"(?i)\bbounty\b[^.]{0,30}\blive through\b",
]


def unsupported_live_claims(html: str, any_open: bool) -> list[str]:
    """Liveness claims on a site with no open round. Silent when one is genuinely open -
    this rule is about a claim outliving its round, not about the wording."""
    if any_open:
        return []
    text = strip_comments(html)
    out = []
    for pat in LIVE_CLAIMS:
        m = re.search(pat, text)
        if m:
            out.append(f"says {m.group(0).strip()!r} but no round is OPEN or VOTING")
    return sorted(set(out))


def rewrite_matchers(vercel: dict) -> list[re.Pattern]:
    """vercel.json rewrite sources as regexes, with :params standing for one segment."""
    pats = []
    for rw in vercel.get("rewrites", []):
        src = rw.get("source", "")
        pats.append(re.compile("^" + re.sub(r":\w+", r"[^/]+", re.escape(src)
                                            .replace(r"\:", ":")) + "$"))
    return pats


def resolves(path: str, matchers: list[re.Pattern], exists) -> bool:
    """cleanUrls is on, so /docs/about is served from docs/about.html."""
    if any(p.match(path) for p in matchers):
        return True
    rel = path.lstrip("/")
    return any(exists(c) for c in (rel, rel + ".html", rel + "/index.html", rel + ".md"))


def dead_links(html: str, matchers: list[re.Pattern], exists) -> list[str]:
    text = strip_comments(html)
    out = []
    ids = set(re.findall(r'id="([^"]+)"', text))
    # src too, not just href. The ZABAL Gamez brand kit renders its own logo from
    # /assets/zabal-games-brand/logo.png, a pre-migration path that 404s in production -
    # a broken image on a page whose entire job is handing out that image, and an
    # href-only check walked straight past it.
    for href in set(re.findall(r'(?:href|src)="([^"]+)"', text)):
        if href.startswith("#"):
            if href[1:] and href[1:] not in ids:
                out.append(f"in-page anchor {href} has no matching id")
        elif href.startswith("/") and not href.startswith("//"):
            clean = href.split("#")[0].split("?")[0]
            if clean and not resolves(clean, matchers, exists):
                out.append(f"internal link {href} resolves to nothing")
    return sorted(set(out))


def _selftest() -> bool:
    passed = True

    def check(label: str, cond) -> None:
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    st = {1166: "WINNER SET", 9999: "OPEN"}
    closed_card = ('<a href="https://poidh.xyz/base/bounty/1166">Submit on POIDH</a>')
    check("an invitation beside a settled bounty is caught",
          stale_invitations(closed_card, st))
    check("the same invitation beside an OPEN bounty is fine",
          not stale_invitations(closed_card.replace("1166", "9999"), st))
    check("linking to a closed bounty without inviting is fine",
          not stale_invitations(
              '<a href="https://poidh.xyz/base/bounty/1166">View the bounty</a>', st))
    check("'Live now' counts as an invitation",
          stale_invitations('<div>Round 2 - Live now</div>'
                            '<a href="https://poidh.xyz/base/bounty/1166">x</a>', st))
    # The comment on the real fix quotes the banned wording. Without strip_comments the
    # checker fails on the commit that fixes the bug, which is the fastest way to get a
    # checker deleted.
    check("wording quoted inside an HTML comment is not a hit",
          not stale_invitations(
              '<!-- this used to say Submit on POIDH -->'
              '<a href="https://poidh.xyz/base/bounty/1166">View the bounty</a>', st))
    check("an unknown bounty id is not guessed at",
          not stale_invitations(
              '<a href="https://poidh.xyz/base/bounty/4242">Submit on POIDH</a>', st))

    matchers = rewrite_matchers({"rewrites": [
        {"source": "/round/:n/judging"}, {"source": "/best-practices"}]})
    have = {"docs/about.html", "index.html"}
    ex = lambda c: c in have
    check("a rewrite source resolves", resolves("/round/2/judging", matchers, ex))
    check("cleanUrls finds docs/about.html", resolves("/docs/about", matchers, ex))
    check("a pre-migration path is caught",
          not resolves("/poidh-round2-judging.html", matchers, ex))
    check("a dangling in-page anchor is caught",
          dead_links('<a href="#leaderboard">x</a><div id="lb-table"></div>', matchers, ex))
    check("an anchor that exists is fine",
          not dead_links('<a href="#lb-table">x</a><div id="lb-table"></div>', matchers, ex))
    check("an external link is not checked",
          not dead_links('<a href="https://example.com/nope">x</a>', matchers, ex))
    check("a broken image src is caught, not just a href",
          dead_links('<img src="/assets/zabal-games-brand/logo.png">', matchers, ex))

    meta = '<meta name="description" content="Currently R5 active: best clip, through Sun Aug 30.">'
    check("a stale liveness claim in metadata is caught",
          unsupported_live_claims(meta, any_open=False))
    check("the same claim is fine while a round is genuinely open",
          not unsupported_live_claims(meta, any_open=True))
    check("'live leaderboard' is not a liveness claim about a round",
          not unsupported_live_claims('<h2>Live leaderboard</h2><p>read live from poidh</p>',
                                      any_open=False))
    check("'Live now' is caught with no open round",
          unsupported_live_claims('<h2>Live now</h2>', any_open=False))
    check("wording quoted in a JS line comment is not a hit",
          not stale_invitations(
              '<script>\n  // "Be the first" invited submissions to a closed round\n'
              '  var u = "https://poidh.xyz/base/bounty/1166";\n</script>', st))
    check("a URL inside code is not mistaken for a comment",
          dead_links('<script>\n  var x = 1; // note\n</script>'
                     '<a href="/poidh-round2-judging.html">x</a>', matchers, ex))
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("check-site-claims selftest")
        okd = _selftest()
        print("selftest:", "passed" if okd else "FAILED")
        return 0 if okd else 1

    status = load_round_status()
    vercel = json.loads((REPO_ROOT / "vercel.json").read_text())
    matchers = rewrite_matchers(vercel)
    exists = lambda rel: (REPO_ROOT / rel).exists()

    pages = sorted(p for p in REPO_ROOT.glob("**/*.html")
                   if ".git" not in p.parts and "node_modules" not in p.parts)
    if not pages:
        print("FAIL no HTML pages found - this check would pass on an empty repo")
        return 1

    any_open = any(s in CAN_SUBMIT for s in status.values())
    problems = 0
    print(f"Site claim sweep - {len(pages)} page(s), "
          f"{len(status)} round(s) with a known on-chain state, "
          f"{'a round is OPEN' if any_open else 'none open'}\n")
    for p in pages:
        html = p.read_text()
        rel = p.relative_to(REPO_ROOT)
        for msg in stale_invitations(html, status):
            print(f"  STALE  {rel}: {msg}")
            problems += 1
        for msg in unsupported_live_claims(html, any_open):
            print(f"  CLAIM  {rel}: {msg}")
            problems += 1
        for msg in dead_links(html, matchers, exists):
            print(f"  DEAD   {rel}: {msg}")
            problems += 1

    print()
    if problems:
        print(f"{problems} problem(s). Every one of these is what an entrant sees.")
        return 1
    print("No page invites anyone into a closed round, and no internal link is dead.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
