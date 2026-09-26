#!/usr/bin/env python3
"""Render /gallery - every submission this programme has ever received, credited.

WHY THIS EXISTS. poidhz.com could tell you how many people had entered, who they were and what
notes they got, and it could not show you a single thing anybody made. Fifty-one claims across
eight bounties existed only on poidh's own bounty pages, one page per round, with no way to see
the body of work or to find a person's pieces together.

That is a community problem, not a design one. Zaal, 2026-09-25: "how else can we improve our
poidhz website and build a community around the people who have submitted". People come back to
a place that shows their work and credits them by name. A leaderboard row is not that.

WHAT IT REFUSES TO DO.

  - It never invites anyone into a round that is closed. Round state comes from
    data/rounds-live.json, which is regenerated from chain, and a closed round's card says
    CLOSED. check-site-claims.py enforces the same rule across the whole site.
  - It never ranks entrants. The feedback pages carry that rule for the same reason
    (rounds/daily/d01/FEEDBACK.md): telling somebody their piece was the best one that did not
    win says either that the pick was wrong or that the words are empty. Winners are marked
    because that is a fact on chain; nothing else is ordered by quality.
  - It never shows a piece without crediting whoever made it. An unresolved wallet is shown as
    a shortened address, never as "anonymous" - the person is not anonymous, our resolver just
    failed, and those are different claims.

    python3 scripts/build-gallery.py
    python3 scripts/build-gallery.py --check     # CI: fail if the file on disk is stale
    python3 scripts/build-gallery.py --selftest  # offline logic tests
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RICH = REPO_ROOT / "data" / "claims.json"
LIVE = REPO_ROOT / "data" / "rounds-live.json"
FEEDBACK = REPO_ROOT / "feedback"
OUT = REPO_ROOT / "gallery.html"

# A round is open to new work in exactly these states, the same set check-site-claims.py uses.
CAN_SUBMIT = frozenset({"OPEN", "VOTING"})


def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def load() -> dict:
    if not RICH.exists():
        raise SystemExit(f"FAIL: {RICH} does not exist. Run refresh-poidh-leaderboard.py.")
    d = json.loads(RICH.read_text())
    if not d.get("claims"):
        raise SystemExit("FAIL: claims.json holds no claims. An empty gallery would say this "
                         "programme has produced nothing, which is a measurement failure and "
                         "not a fact.")
    return d


def round_state() -> dict[int, dict]:
    """bounty_id -> {status, title, label}. Empty when the feed is missing, and the caller
    then says UNKNOWN rather than guessing a round is open."""
    if not LIVE.exists():
        return {}
    feed = json.loads(LIVE.read_text())
    return {r["bounty_id"]: r for r in feed.get("rounds", []) if r.get("bounty_id")}


def handle_for(addr: str, lb: dict) -> tuple[str, bool]:
    """(display handle, whether it really resolved). A wallet we could not resolve is shown
    as a short address - it is a person we failed to name, not an anonymous one."""
    row = lb.get(addr.lower(), {})
    h = row.get("farcaster_username") or row.get("twitter_handle") or row.get("displayName")
    if h:
        return str(h).lstrip("@"), True
    return addr[:6] + "…" + addr[-4:], False


def feedback_url(bounty_id: int, handle: str, row: dict | None = None) -> str | None:
    """Only ever link a notes page that exists on disk. The programme's one kept promise is
    that every entrant gets notes; a link to a 404 would break it more loudly than silence.

    A PERSON CAN BE FILED UNDER A NAME THAT IS NOT THE ONE THEIR CLAIM RESOLVES TO. Found
    2026-09-25: bounty 1412's claim resolves the wallet to `defifa`, and their notes were
    written to `feedback/1412/kmacb.eth.html` because that is the handle in the claim text.
    Looking up one name only, their own notes were unreachable from their own entry. So every
    name we hold for a wallet is tried, and the first page that exists wins.
    """
    names = [handle]
    if row:
        for k in ("farcaster_username", "twitter_handle", "displayName"):
            v = row.get(k)
            if v:
                names.append(str(v).lstrip("@"))
    seen = set()
    for n in names:
        if n in seen:
            continue
        seen.add(n)
        if (FEEDBACK / str(bounty_id) / f"{n}.html").exists():
            return f"/feedback/{bounty_id}/{n}"
    return None


def is_video(url: str) -> bool:
    return url.lower().split("?")[0].endswith((".mp4", ".mov", ".webm", ".m4v"))


def build(d: dict, states: dict) -> list[dict]:
    """One group per bounty, newest first, each carrying its claims in claim order."""
    lb = {r["address"].lower(): r for r in d.get("leaderboard", [])}
    titles = {b["id"]: b.get("title") for b in d.get("bounties", [])}

    by = defaultdict(list)
    for c in d["claims"]:
        by[c["bounty_id"]].append(c)

    groups = []
    for bid in sorted(by, reverse=True):
        st = states.get(bid, {})
        entries = []
        for c in sorted(by[bid], key=lambda c: -int(c.get("claim_id") or 0)):
            h, resolved = handle_for(c.get("issuer") or "", lb)
            entries.append({
                "claim_id": c.get("claim_id"),
                "title": c.get("title") or "Untitled",
                "handle": h,
                "resolved": resolved,
                "media": c.get("image_url"),
                "video": is_video(c.get("image_url") or ""),
                "won": bool(c.get("accepted")),
                "notes": (feedback_url(bid, h, lb.get((c.get("issuer") or "").lower()))
                          if resolved else None),
            })
        groups.append({
            "bounty_id": bid,
            "title": st.get("title") or titles.get(bid) or f"Bounty {bid}",
            "label": st.get("label") or "",
            "status": st.get("status", "UNKNOWN"),
            "open": st.get("status") in CAN_SUBMIT,
            "entries": entries,
        })
    return groups


def nav() -> str:
    """The nav comes from sync-site-nav.py, which OWNS it across all 29 pages.

    Rendering my own would make two scripts writers of one file: sync-site-nav rewrites the
    block after this runs, and then `--check` here reports the page stale forever. Importing
    the real builder means both produce the same bytes and the check means something.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_nav", Path(__file__).resolve().parent / "sync-site-nav.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.nav_html("/gallery")


def render(groups: list[dict]) -> str:
    total = sum(len(g["entries"]) for g in groups)
    people = len({e["handle"] for g in groups for e in g["entries"]})
    rounds = len(groups)
    winners = sum(1 for g in groups for e in g["entries"] if e["won"])

    cards = []
    for g in groups:
        tag = ("OPEN NOW" if g["open"] else g["status"].replace("_", " "))
        tag_class = "open" if g["open"] else "shut"
        items = []
        for e in g["entries"]:
            media = ""
            if e["media"] and e["video"]:
                media = (f'<video class="m" src="{esc(e["media"])}" controls preload="none" '
                         f'playsinline aria-label="{esc(e["title"])}"></video>')
            elif e["media"]:
                media = (f'<img class="m" src="{esc(e["media"])}" loading="lazy" decoding="async" '
                         f'alt="{esc(e["title"])}, by {esc(e["handle"])}">')
            else:
                media = '<div class="m none">no media on this claim</div>'
            links = [f'<a href="https://poidh.xyz/base/bounty/{g["bounty_id"]}">on poidh</a>']
            if e["notes"]:
                links.append(f'<a href="{esc(e["notes"])}">their notes</a>')
            items.append(
                f'<figure class="e{" won" if e["won"] else ""}">'
                f'{media}'
                f'<figcaption>'
                f'{"<b class=w>WON</b>" if e["won"] else ""}'
                f'<span class="t">{esc(e["title"])}</span>'
                f'<span class="h">{esc(e["handle"])}'
                f'{"" if e["resolved"] else " <i>wallet, handle unresolved</i>"}</span>'
                f'<span class="l">{" ".join(links)}</span>'
                f'</figcaption></figure>')
        cards.append(
            f'<section class="round">'
            f'<h2>{esc(g["label"] or g["title"])}'
            f'<span class="tag {tag_class}">{esc(tag)}</span></h2>'
            f'<p class="sub">{esc(g["title"])} - {len(g["entries"])} '
            f'entr{"y" if len(g["entries"]) == 1 else "ies"}</p>'
            f'<div class="grid">{"".join(items)}</div>'
            f'</section>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The work - poidhz</title>
<meta name="description" content="Every submission this programme has received: {total} entries from {people} people across {rounds} rounds, each credited and linked to its notes.">
<meta property="og:title" content="The work - poidhz">
<meta property="og:description" content="{total} entries from {people} people across {rounds} rounds. Everyone credited, every entrant's notes linked.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#070709;--surface:#111115;--surface-2:#16161c;--orange:#ff6b35;--cyan:#00e5ff;
--gold:#f5c842;--pink:#ff3d6e;--zabal:#a78bfa;--green:#4ade80;--text:#e4e2dd;
--text-muted:#8a8895;--text-dim:#4e4c57;--border:#1f1e26;--radius:10px}}
body{{background:var(--bg);color:var(--text);font-family:'Outfit',sans-serif;line-height:1.6;
-webkit-font-smoothing:antialiased;min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;pointer-events:none;z-index:-1;
background:radial-gradient(ellipse 800px 600px at 15% -10%,rgba(167,139,250,.12),transparent 60%),
radial-gradient(ellipse 700px 500px at 90% 10%,rgba(0,229,255,.10),transparent 60%)}}
a{{color:var(--cyan);text-decoration:none}}
a:hover{{text-decoration:underline}}
main{{max-width:1100px;margin:0 auto;padding:2.5rem 1.5rem 5rem}}
.kicker{{font-family:'JetBrains Mono',monospace;font-size:.7rem;text-transform:uppercase;
letter-spacing:.18em;color:var(--cyan)}}
h1{{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(1.9rem,6vw,2.8rem);
line-height:1.1;margin:.4rem 0 .6rem}}
.lede{{color:var(--text-muted);max-width:60ch}}
.stats{{display:flex;gap:2rem;flex-wrap:wrap;margin:1.6rem 0 .5rem;padding:1rem 0;
border-top:1px solid var(--border);border-bottom:1px solid var(--border)}}
.stat b{{display:block;font-family:'Syne',sans-serif;font-size:1.6rem;color:var(--text)}}
.stat span{{font-family:'JetBrains Mono',monospace;font-size:.66rem;text-transform:uppercase;
letter-spacing:.1em;color:var(--text-dim)}}
.round{{margin:3rem 0 0}}
h2{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.3rem;display:flex;
align-items:center;gap:.7rem;flex-wrap:wrap}}
.tag{{font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.12em;
padding:.2rem .5rem;border-radius:4px;border:1px solid var(--border);color:var(--text-dim)}}
.tag.open{{color:#06060a;background:var(--green);border-color:var(--green);font-weight:600}}
.sub{{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--text-dim);
margin:.2rem 0 1rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1rem}}
.e{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
overflow:hidden;display:flex;flex-direction:column}}
.e.won{{border-color:var(--gold)}}
.m{{width:100%;aspect-ratio:1/1;object-fit:cover;background:var(--surface-2);display:block}}
.m.none{{display:grid;place-items:center;font-family:'JetBrains Mono',monospace;
font-size:.68rem;color:var(--text-dim)}}
figcaption{{padding:.7rem .8rem .8rem;display:flex;flex-direction:column;gap:.25rem}}
.w{{font-family:'JetBrains Mono',monospace;font-size:.6rem;letter-spacing:.14em;
color:var(--gold)}}
.t{{font-size:.9rem;line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;
-webkit-box-orient:vertical;overflow:hidden}}
.h{{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:var(--zabal)}}
.h i{{color:var(--text-dim);font-style:normal}}
.l{{font-family:'JetBrains Mono',monospace;font-size:.68rem;display:flex;gap:.7rem;
margin-top:.15rem}}
footer{{border-top:1px solid var(--border);margin-top:3.5rem;padding-top:1.2rem;
font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--text-dim);max-width:70ch}}
@media(max-width:640px){{main{{padding:1.75rem 1rem 4rem}}
.grid{{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.7rem}}}}
</style>
</head>
<body>
{nav()}
<main>
<p class="kicker">the work</p>
<h1>Everything anybody has made for this programme</h1>
<p class="lede">Every claim across every round, credited to whoever made it, linked to their
notes. The pieces lived on eight separate bounty pages and nowhere together until now.</p>

<div class="stats">
<div class="stat"><b>{total}</b><span>entries</span></div>
<div class="stat"><b>{people}</b><span>people</span></div>
<div class="stat"><b>{rounds}</b><span>rounds</span></div>
<div class="stat"><b>{winners}</b><span>paid winners</span></div>
</div>

{"".join(cards)}

<footer>
No ranking is published here and none is implied by the order - rounds run newest first, and
inside a round the newest claim is first. A piece marked WON is the claim accepted on chain,
which is a fact rather than an opinion. Everything else is simply the work.
<br><br>
A handle shown as a shortened wallet is somebody our resolver could not name, not somebody
anonymous. If that is you, say so and it gets fixed.
<br><br>
Built from data/claims.json, which is regenerated from chain. <a href="/people">The people</a>
- <a href="/feedback">everyone's notes</a> - <a href="/about">what this has and has not
delivered</a>.
</footer>
</main>
</body>
</html>
"""


def _selftest() -> bool:
    ok = True

    def c(label, cond):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + label)
        ok = ok and cond

    lb = [{"address": "0xAAA", "farcaster_username": "pascaline"}]
    d = {
        "leaderboard": lb,
        "bounties": [{"id": 1409, "title": "Daily 01"}],
        "claims": [
            {"bounty_id": 1409, "claim_id": 1, "issuer": "0xaaa", "title": "A",
             "image_url": "https://x/1.jpg", "accepted": True},
            {"bounty_id": 1409, "claim_id": 2, "issuer": "0xBBB", "title": "B",
             "image_url": "https://x/2.mp4", "accepted": False},
        ],
    }
    states = {1409: {"status": "WINNER SET", "title": "Daily 01", "label": "Daily 1"}}
    g = build(d, states)
    c("one group per bounty", len(g) == 1 and g[0]["bounty_id"] == 1409)
    c("newest claim first", [e["claim_id"] for e in g[0]["entries"]] == [2, 1])
    c("a resolved wallet shows its handle", g[0]["entries"][1]["handle"] == "pascaline")
    c("an unresolved wallet shows a short address, never 'anonymous'",
      g[0]["entries"][0]["handle"].startswith("0xBBB"[:6]) and
      "anon" not in g[0]["entries"][0]["handle"].lower())
    c("an mp4 is treated as video", g[0]["entries"][0]["video"] is True)
    c("a jpg is not", g[0]["entries"][1]["video"] is False)
    c("the accepted claim is marked won", g[0]["entries"][1]["won"] is True)
    c("a settled round is not marked open", g[0]["open"] is False)

    g_open = build(d, {1409: {"status": "OPEN"}})
    c("an OPEN round is marked open", g_open[0]["open"] is True)
    g_vote = build(d, {1409: {"status": "VOTING"}})
    c("a VOTING round still accepts work, so it is open", g_vote[0]["open"] is True)
    g_none = build(d, {})
    c("a round missing from the feed is UNKNOWN and NOT open",
      g_none[0]["status"] == "UNKNOWN" and g_none[0]["open"] is False)

    page = render(g)
    c("the page renders the handle", "pascaline" in page)
    c("markup in a title cannot break out",
      "&lt;script&gt;" in render(build(
          {"leaderboard": lb, "bounties": [],
           "claims": [{"bounty_id": 1, "claim_id": 1, "issuer": "0xaaa",
                       "title": "<script>alert(1)</script>", "image_url": "https://x/1.jpg"}]},
          {})))
    c("a settled round shows no OPEN NOW tag", "OPEN NOW" not in page)
    c("an open round does show it", "OPEN NOW" in render(g_open))
    c("images are lazy so fifty of them do not land at once", 'loading="lazy"' in page)
    c("video does not autoplay or preload", 'preload="none"' in page and "autoplay" not in page)
    c("the footer says no ranking is published", "No ranking is published" in page)

    print("selftest:", "passed" if ok else "FAILED")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if gallery.html on disk is not what this would write")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return 0 if _selftest() else 1

    groups = build(load(), round_state())
    page = render(groups)
    total = sum(len(g["entries"]) for g in groups)

    if a.check:
        if not OUT.exists():
            print("FAIL: gallery.html does not exist. Run without --check.")
            return 1
        if OUT.read_text() != page:
            print("FAIL: gallery.html is stale. Run scripts/build-gallery.py.")
            return 1
        print(f"  ok   gallery.html is current ({total} entries)")
        return 0

    if OUT.exists() and OUT.read_text() == page:
        print(f"  no change - gallery.html already shows {total} entries")
        return 0
    OUT.write_text(page)
    people = len({e["handle"] for g in groups for e in g["entries"]})
    print(f"  wrote gallery.html - {total} entries, {people} people, {len(groups)} rounds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
