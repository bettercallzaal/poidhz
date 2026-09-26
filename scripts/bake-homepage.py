#!/usr/bin/env python3
"""Render the live round state INTO index.html, so the HTML carries it before any JavaScript.

WHY, AND IT WAS MEASURED BEFORE IT WAS BUILT. On 2026-09-24 `curl https://poidhz.com/` returned
17,546 bytes containing **zero** occurrences of `1412`, `1410`, `1409`, `pascaline`,
`leoxcrane` or `0.005`, while a control search for `poidhz` in the same bytes returned 10. The
instrument was fine; the data genuinely was not there. Everything a visitor came for arrived
only after a second request for a 5,766-byte JSON feed.

That matters for this site more than for most, because **the whole point of poidhz.com is to
be the link in a bounty post.** Research doc `infrastructure/2548-poidhz-site-improvements`
has the full argument. The short version:

  - A reader whose second request fails, stalls, or is blocked gets "loading...". GOV.UK
    measured 0.9% of their visits arriving with no JavaScript available and no choice in it.
    At our scale the percentage is not the argument; the single point of failure is.
  - The `og:description` in the share card is a fixed sentence. It cannot say "three rounds,
    nineteen entries" because nothing regenerates it. The card is the most-seen surface this
    programme has and it has been saying the same thing since week one.

WHAT THIS DOES NOT DO. It does not remove the JavaScript. The script still fetches the feed and
overwrites what this bakes in, which is what keeps the page fresh between builds - this is
progressive enhancement, not a replacement. The baked copy is the floor, not the ceiling.

WHERE IT WRITES. Only between explicit sentinel comments. It never regex-replaces page
structure, because a build step that rewrites HTML it does not fully parse is how a site
silently loses a section.

    python3 scripts/bake-homepage.py
    python3 scripts/bake-homepage.py --check     # non-zero if the page is stale vs the feed
    python3 scripts/bake-homepage.py --selftest
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGE = REPO_ROOT / "index.html"
FEED = REPO_ROOT / "data" / "rounds-live.json"

ROWS_OPEN, ROWS_CLOSE = "<!--BAKED-ROWS-->", "<!--/BAKED-ROWS-->"
LD_OPEN, LD_CLOSE = "<!--BAKED-JSONLD-->", "<!--/BAKED-JSONLD-->"
STATS_OPEN, STATS_CLOSE = "<!--BAKED-STATS-->", "<!--/BAKED-STATS-->"
OGD = re.compile(r'(<meta property="og:description" content=")([^"]*)(">)')
PILL = {"OPEN": "p-open", "VOTING": "p-vote", "WINNER SET": "p-done", "CLOSED": "p-done",
        "CANCELED": "p-dead", "DRAFT": "p-done", "UNKNOWN": "p-dead"}


def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def eth(n) -> str:
    """Mirrors the page's own eth(). A different rounding here would make the baked table and
    the JavaScript table disagree with each other in front of the reader."""
    if n is None:
        return "-"
    s = f"{float(n):.4f}".rstrip("0").rstrip(".")
    return f"{s} ETH"


def shut(r: dict, now: dt.datetime) -> bool:
    c = r.get("closes_at")
    if not c:
        return False
    try:
        return dt.datetime.fromisoformat(c) <= now
    except ValueError:
        return False


def cast_rounds(feed: dict) -> list[dict]:
    return [r for r in (feed.get("rounds") or []) if r.get("bounty_id")]


def winner_cell(r: dict) -> str:
    w = r.get("winner")
    if w:
        h = w.get("handle") or (w.get("wallet") or "")[:8]
        return "@" + esc(h)
    if r.get("offchain"):
        return '<span style="color:var(--text-muted)">credited off-chain</span>'
    return '<span style="color:var(--text-dim)">-</span>'


def render_rows(feed: dict, now: dt.datetime) -> str:
    out = []
    for r in cast_rounds(feed):
        url = r.get("url") or f"https://poidh.xyz/base/bounty/{r['bounty_id']}"
        st = "CLOSED" if (r.get("status") == "OPEN" and shut(r, now)) else (r.get("status") or "UNKNOWN")
        pill = f'<span class="pill {PILL.get(st, "p-done")}">{esc(st.lower())}</span>'
        claims = r.get("claims")
        out.append(
            f'<tr><td><a href="{esc(url)}" target="_blank" rel="noopener">'
            f'{esc(r.get("label") or ("R" + str(r.get("round"))))}</a></td>'
            f'<td>{pill}</td><td>{claims if claims is not None else "-"}</td>'
            f'<td>{eth(r.get("amount_native"))}</td><td>{winner_cell(r)}</td></tr>')
    return "".join(out)


def totals(feed: dict) -> dict:
    cast = cast_rounds(feed)
    return {
        "rounds": len(cast),
        "entries": sum(r.get("claims") or 0 for r in cast),
        "pot": sum(r.get("amount_native") or 0 for r in cast),
        "paid": len([r for r in cast if r.get("winner")]),
    }


def render_stats(feed: dict) -> str:
    t = totals(feed)
    return ("".join(
        f'<div class="stat"><b>{v}</b><span>{lbl}</span></div>'
        for v, lbl in ((t["rounds"], "rounds run"), (t["entries"], "entries"),
                       (eth(t["pot"]), "in pots"), (t["paid"], "winners paid"))))


def render_og(feed: dict, now: dt.datetime) -> str:
    """The share card sentence. It leads with whatever is LIVE, because that is the only part
    a reader can act on, and falls back to the record when nothing is open."""
    t = totals(feed)
    live = [r for r in cast_rounds(feed) if r.get("status") == "OPEN" and not shut(r, now)]
    voting = [r for r in cast_rounds(feed) if r.get("status") == "VOTING"]
    if len(live) > 1:
        # TWO ROUNDS CAN RUN AT ONCE AND THIS SENTENCE COULD NOT SAY SO. From 2026-09-25 the
        # ad round (1418) and the code round (1421) overlap on purpose - one closes Sunday,
        # the other the Monday after the festival. `live[0]` would have described one of them
        # and silently hidden the other, on the share card, which is the surface most people
        # see before they see the site.
        n = sum(r.get("claims") or 0 for r in live)
        head = (f"{len(live)} bounties are open right now, with {n} "
                f"{'entry' if n == 1 else 'entries'} between them.")
    elif live:
        n = live[0].get("claims") or 0
        head = (f"A bounty is open now with {n} "
                f"{'entry' if n == 1 else 'entries'} in it.")
    elif voting:
        head = "A pick is in its contributor vote right now."
    else:
        head = "Nothing is open at this moment."
    # NO APOSTROPHES IN THIS SENTENCE. It goes into an HTML attribute, so html.escape turns
    # one into &#x27;, and a crawler that does not decode entities prints that literally in
    # the share card. Cheaper to write around it than to rely on every unfurler being correct.
    return (f"{head} {t['rounds']} rounds run, {t['entries']} entries, "
            f"{eth(t['pot'])} in pots, {t['paid']} winners paid. "
            f"Every entrant gets public notes.")


def render_jsonld(feed: dict, now: dt.datetime) -> str:
    """An ItemList of the rounds. Machine-readable state, which the page had none of.

    DELIBERATELY NOT AN `Event` FOR ZAOSTOCK. zaostock.com/program already publishes Event
    JSON-LD with the real start and end times - that is where this session read "2026-10-03
    12:00 to 18:00" and the Black Moon evening from. Publishing a second copy here creates two
    sources for one fact, and the moment they drift the wrong one is the one somebody quotes.
    This page links to zaostock.com; it does not restate it.
    """
    items = []
    for i, r in enumerate(cast_rounds(feed), 1):
        url = r.get("url") or f"https://poidh.xyz/base/bounty/{r['bounty_id']}"
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": r.get("label") or f"R{r.get('round')}",
            "url": url,
        })
    blob = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "ZAO bounties on poidh",
        "description": "Every bounty The ZAO has issued on poidh, with its live state.",
        "url": "https://poidhz.com/",
        "numberOfItems": len(items),
        "itemListElement": items,
    }
    return ('<script type="application/ld+json">'
            + json.dumps(blob, separators=(",", ":")) + "</script>")


def splice(page: str, open_m: str, close_m: str, body: str) -> str:
    i, j = page.find(open_m), page.find(close_m)
    if i == -1 or j == -1 or j < i:
        raise SystemExit(f"FAIL: index.html is missing the {open_m} / {close_m} sentinels. "
                         f"Nothing was written - this script refuses to guess where the "
                         f"content goes.")
    return page[:i + len(open_m)] + body + page[j:]


def bake(page: str, feed: dict, now: dt.datetime) -> str:
    page = splice(page, ROWS_OPEN, ROWS_CLOSE, render_rows(feed, now))
    page = splice(page, STATS_OPEN, STATS_CLOSE, render_stats(feed))
    page = splice(page, LD_OPEN, LD_CLOSE, render_jsonld(feed, now))
    og = render_og(feed, now)
    if not OGD.search(page):
        raise SystemExit("FAIL: no og:description meta in index.html. Nothing was written.")
    return OGD.sub(lambda m: m.group(1) + esc(og) + m.group(3), page, count=1)


def load_feed() -> dict:
    if not FEED.exists():
        raise SystemExit(f"FAIL: {FEED} does not exist. Run scripts/refresh-rounds.py first. "
                         f"Baking nothing is not the same as baking an empty table.")
    feed = json.loads(FEED.read_text())
    if not cast_rounds(feed):
        raise SystemExit("FAIL: the feed has no rounds with a bounty_id. Refusing to bake an "
                         "empty table over a good one - an empty page reads as 'this "
                         "programme has done nothing'.")
    return feed


def _selftest() -> bool:
    passed = True

    def c(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    now = dt.datetime.fromisoformat("2026-09-24T06:00:00-04:00")
    feed = {"rounds": [
        {"bounty_id": 1409, "label": "Daily 1", "status": "WINNER SET", "claims": 6,
         "amount_native": 0.0061, "winner": {"handle": "leoxcrane"},
         "closes_at": "2026-09-21T16:00:00-04:00"},
        {"bounty_id": 1410, "label": "Daily 2", "status": "VOTING", "claims": 8,
         "amount_native": 0.005, "closes_at": "2026-09-22T17:00:00-04:00"},
        {"bounty_id": 1412, "label": "Daily 3", "status": "OPEN", "claims": 5,
         "amount_native": 0.005, "closes_at": "2026-09-23T17:00:00-04:00"},
        {"round": 9},  # planned, no bounty_id - must be skipped everywhere
    ]}

    c("eth() matches the page's own rounding", eth(0.0061) == "0.0061 ETH" and eth(0.005) == "0.005 ETH")
    c("eth(None) is a dash, never 0", eth(None) == "-")
    c("a round with no bounty_id is not counted", totals(feed)["rounds"] == 3)
    c("entries add up across cast rounds only", totals(feed)["entries"] == 19)

    rows = render_rows(feed, now)
    c("every cast round has a row", rows.count("<tr>") == 3)
    c("the row carries the real bounty id a crawler can read", "1412" in rows)
    c("the winner's handle is in the HTML", "@leoxcrane" in rows)
    # The bug this exists to prevent: a round still marked OPEN whose stated close has passed.
    c("an OPEN round past its stated close renders as closed, not open",
      'p-open' not in rows and rows.count("closed") >= 1)

    og_after = render_og(feed, now)
    # A round in its contributor vote IS live state and outranks the record, even though
    # nothing is enterable. The totals still ride along behind it.
    c("og description leads with the VOTE when a vote is running and nothing is enterable",
      og_after.startswith("A pick is in its contributor vote")
      and "3 rounds run" in og_after and "19 entries" in og_after)

    quiet = {"rounds": [r for r in feed["rounds"] if r.get("status") not in ("OPEN", "VOTING")]}
    og_quiet = render_og(quiet, now)
    c("og description falls back to the record when nothing at all is live",
      og_quiet.startswith("Nothing is open at this moment.") and "1 winners paid" in og_quiet)

    live_feed = {"rounds": [dict(feed["rounds"][2], closes_at="2026-12-31T17:00:00-05:00")]}
    og_live = render_og(live_feed, now)
    c("og description leads with the OPEN bounty when one is enterable",
      og_live.startswith("A bounty is open now with 5 entries"))

    # TWO OPEN AT ONCE, which is the real state from 2026-09-25 and was unrepresentable.
    two = {"rounds": [
        dict(feed["rounds"][2], bounty_id=1418, claims=2, closes_at="2026-12-31T17:00:00-05:00"),
        dict(feed["rounds"][2], bounty_id=1421, claims=0, closes_at="2026-12-31T17:00:00-05:00"),
    ]}
    og_two = render_og(two, now)
    c("og description counts BOTH open bounties rather than describing one",
      og_two.startswith("2 bounties are open right now, with 2 entries between them."))
    three = {"rounds": [dict(feed["rounds"][2], bounty_id=i, claims=1,
                             closes_at="2026-12-31T17:00:00-05:00") for i in (1, 2, 3)]}
    c("and it scales past two", render_og(three, now).startswith("3 bounties are open right now, with 3 entries"))
    c("one open bounty still reads in the singular form",
      render_og({"rounds": [dict(feed["rounds"][2], claims=2,
                                 closes_at="2026-12-31T17:00:00-05:00")]}, now)
      .startswith("A bounty is open now with 2 entries"))

    one = {"rounds": [dict(feed["rounds"][2], claims=1, closes_at="2026-12-31T17:00:00-05:00")]}
    c("one entry is singular", "with 1 entry in it" in render_og(one, now))
    # An apostrophe here becomes &#x27; in the attribute and some unfurlers print it raw.
    c("the share sentence contains no apostrophe to be mangled",
      "'" not in og_after and "'" not in render_og(one, now))

    ld = json.loads(render_jsonld(feed, now).split(">", 1)[1].rsplit("<", 1)[0])
    c("the JSON-LD parses and counts only cast rounds",
      ld["@type"] == "ItemList" and ld["numberOfItems"] == 3 and len(ld["itemListElement"]) == 3)
    c("it does NOT restate ZAOstock's own Event data", "Event" not in json.dumps(ld))

    page = (f'<meta property="og:description" content="old fixed sentence">'
            f'{LD_OPEN}{LD_CLOSE}'
            f'<div class="stats">{STATS_OPEN}{STATS_CLOSE}</div>'
            f'<tbody>{ROWS_OPEN}<tr><td>stale</td></tr>{ROWS_CLOSE}</tbody>')
    out = bake(page, feed, now)
    c("baking replaces what was between the sentinels", "stale" not in out)
    c("baking keeps the sentinels so it can run again", ROWS_OPEN in out and ROWS_CLOSE in out)
    c("baking is idempotent", bake(out, feed, now) == out)
    c("the og:description is rewritten", "old fixed sentence" not in out and "19 entries" in out)

    try:
        splice("<html>no sentinels here</html>", ROWS_OPEN, ROWS_CLOSE, "x")
        c("a page with no sentinels is REFUSED rather than guessed at", False)
    except SystemExit:
        c("a page with no sentinels is REFUSED rather than guessed at", True)

    # The real page must actually carry the sentinels, or this whole script is decorative.
    if PAGE.exists():
        real = PAGE.read_text()
        c("the REAL index.html carries every sentinel pair",
          all(m in real for m in (ROWS_OPEN, ROWS_CLOSE, STATS_OPEN, STATS_CLOSE,
                                  LD_OPEN, LD_CLOSE)))
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if index.html does not match the feed")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        print("bake-homepage selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    feed = load_feed()
    now = dt.datetime.now().astimezone()
    page = PAGE.read_text()
    baked = bake(page, feed, now)

    if a.check:
        if baked == page:
            t = totals(feed)
            print(f"  PASS: index.html matches the feed - {t['rounds']} rounds, "
                  f"{t['entries']} entries baked into the HTML")
            return 0
        print("  FAIL: index.html is stale against data/rounds-live.json. "
              "Run scripts/bake-homepage.py.")
        return 1

    if baked == page:
        print("  no change - index.html already matches the feed")
        return 0
    PAGE.write_text(baked)
    t = totals(feed)
    print(f"  baked into index.html: {t['rounds']} rounds, {t['entries']} entries, "
          f"{eth(t['pot'])} in pots, {t['paid']} winners paid")
    print(f"  og:description now reads: {render_og(feed, now)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
