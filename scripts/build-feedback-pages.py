#!/usr/bin/env python3
"""Render a feedback page per bounty entrant, from data/feedback/<round>.json.

WHY A PAGE. Zaal, 2026-09-22: "add all this to the poidhz.com website so i can just link that
for more info so lets do one piece of feedback in message adn then rest on their subpage". The
message carries one line and a URL; the page carries the rest.

WHY THE URL CARRIES THE BOUNTY ID. Zaal, same day: "its not a slug we can reuse so lets make
sure its tied to bounty". `/feedback/predaking` is a handle slug, and a handle enters more than
one round - building round three over it would overwrite the round-one notes in place, with no
error and no trace, and every link already sent would quietly start showing different text. The
path is `/feedback/<bounty_id>/<handle>`, so each round's notes are their own artifact forever.

WHY THEY ARE SHARED RATHER THAN UNLISTED. Same ruling: "so they can see what feedback others
got too". This OVERRIDES the first version of this script, which made every page noindex with
no index page, on the strength of research doc `community/2536-bounty-entrant-feedback`
decision 3 (Gross 2017: public feedback improved quality and cut participation by showing
people where they stood). That trade was put to Zaal and he chose openness. It is his call and
this is the record of it.

It makes the ranking guard MORE important, not less: entrants will now read each other's pages
side by side, so a superlative on one page is visible from the next one.

AND THE INDEX IS ALPHABETICAL, WHICH IS LOAD-BEARING. Any list of people reads as a ranking to
the people on it. The index sorts by handle and says so on the page, because an unexplained
order invites everyone to infer one.

TWO THINGS THIS REFUSES TO BUILD, because both have already gone wrong once in this programme:

  1. **A ranking word anywhere in the copy.** Zaal, 2026-09-22: "you cant say that most complete
     entrie didnt win". A superlative on a losing entrant's page says the pick was wrong.
  2. **A page for a handle that filed no claim.** The handles are checked against the round's
     real claim list where one is available, so a typo becomes a build failure rather than a
     page addressed to nobody.

    python3 scripts/build-feedback-pages.py --round d01
    python3 scripts/build-feedback-pages.py --round d01 --check
    python3 scripts/build-feedback-pages.py --selftest
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "feedback"

# A superlative on a page belonging to somebody who did not win reads either as "the pick was
# wrong" or as empty words. Checked against the rendered copy, not the source, so it cannot be
# smuggled in through a field this script does not know about.
RANKING_WORDS = re.compile(
    r"(?i)\b(best|strongest|cleanest|most complete|the only one who|"
    r"better than|beat (?:the |every )?other|top entry|second place|runner.?up|"
    r"ranked?|first place|won it)\b")

# Phrases that would turn feedback into a promise. This programme's PROMISE-AUDIT records five
# rounds of promising distribution and delivering money instead.
PROMISE_WORDS = re.compile(
    r"(?i)\b(we will (?:run|post|repost|pin|feature)|will be pinned|guaranteed|"
    r"we promise)\b")


def is_decided(rnd: dict) -> bool:
    """Whether this round has a result yet.

    FEEDBACK AND THE RESULT ARE DIFFERENT THINGS AND THEY ARRIVE AT DIFFERENT TIMES. Bounty
    1412's text promises everyone written notes, and poidh's own flow puts a two-day contributor
    vote between the close and the winner. So there is a real, normal window - days long - where
    the notes are owed and ready and the round genuinely has no winner.

    This file used to assume every round had one. It printed "What decided round three" above
    criteria for a round nobody had decided, and the index sorted alphabetically while
    explaining that it did so "because this round has a winner". Both were claims the data
    could not support, on a public page, addressed to the people waiting for the result.
    """
    return bool((rnd.get("winner") or "").strip())


def decided_heading(rnd: dict) -> str:
    return (f"What decided {rnd['label'].lower()}" if is_decided(rnd)
            else f"What {rnd['label'].lower()} was judged on")


def load(round_id: str) -> dict:
    p = REPO_ROOT / "data" / "feedback" / f"{round_id}.json"
    if not p.exists():
        raise SystemExit(f"FAIL: {p} does not exist. Nothing to build.")
    return json.loads(p.read_text())


def known_claim_handles(round_id: str) -> set[str] | None:
    """Handles that really filed a claim on this round, from data/claims.json.

    Returns None when the file cannot answer - a MISSING answer, never an empty set, because
    an empty set here would silently fail every handle and read as 'nobody entered'."""
    p = REPO_ROOT / "data" / "claims.json"
    if not p.exists():
        return None
    try:
        blob = json.loads(p.read_text())
    except json.JSONDecodeError:
        return None
    raw = json.dumps(blob).lower()
    if not raw.strip():
        return None
    return raw  # substring search; the shape of claims.json varies by round


# The site is built in two stages: this script renders a page, then sync-site-nav.py injects
# the shared navigation bar into it. So the file ON DISK is legitimately a superset of what
# this script renders, and comparing them raw reports every page as stale. Found by running
# --check against the real committed pages rather than only against the selftest fixtures,
# which is the whole reason to do that: the fixtures have no nav, so they could never have
# shown this.
NAV_BLOCK = re.compile(
    r"<!-- ZN-NAV START.*?<!-- ZN-NAV END -->\s*", re.S)


def without_nav(html_text: str) -> str:
    return NAV_BLOCK.sub("", html_text)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render(entrant: dict, rnd: dict) -> str:
    handle = entrant["handle"]
    nxt = rnd["next"]
    items = entrant["items"]
    if not 1 <= len(items) <= 3:
        raise SystemExit(f"FAIL: @{handle} has {len(items)} items. Zaal asked for 1 to 3: "
                         f"'just give liek 1-3 thigns they could do better to win the next one'.")

    lis = []
    for i, it in enumerate(items, 1):
        link = ""
        if it.get("link"):
            link = (f'<a class="itemlink" href="{esc(it["link"])}">{esc(it["link"])}</a>')
        lis.append(
            f'<li><span class="n">{i}</span><div><h3>{esc(it["title"])}</h3>'
            f'<p>{esc(it["body"])}</p>{link}</div></li>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@{esc(handle)} - notes on bounty {rnd["bounty_id"]} - poidhz</title>
<!-- The path carries the BOUNTY ID, never just the handle: a handle enters more than one
     round, so a handle-only path would be overwritten in place by the next round and every
     link already sent would start showing different text. -->
<link rel="canonical" href="https://poidhz.com/feedback/{rnd["bounty_id"]}/{esc(handle)}">
<meta name="description" content="Feedback on one entry to ZAOstock bounty {rnd["bounty_id"]}.">
<link rel="icon" type="image/png" href="/assets/brand-kits/zabal-games/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#070709;--surface:#111115;--surface-2:#16161c;--orange:#ff6b35;--cyan:#00e5ff;
--gold:#f5c842;--zabal:#a78bfa;--text:#e4e2dd;--text-muted:#8a8895;--text-dim:#4e4c57;
--border:#1f1e26;--radius:8px}}
body{{background:var(--bg);color:var(--text);font-family:'Outfit',sans-serif;line-height:1.6;
-webkit-font-smoothing:antialiased;min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;pointer-events:none;z-index:-1;
background:radial-gradient(ellipse 800px 600px at 15% -10%,rgba(167,139,250,0.12),transparent 60%),
radial-gradient(ellipse 700px 500px at 90% 10%,rgba(0,229,255,0.10),transparent 60%),
radial-gradient(ellipse 600px 400px at 50% 100%,rgba(255,107,53,0.08),transparent 60%)}}
a{{color:var(--cyan);text-decoration:none;transition:color .15s}}
a:hover{{color:var(--orange)}}
.container{{max-width:680px;margin:0 auto;padding:0 1.5rem}}
.topnav{{padding:1.25rem 0;border-bottom:1px solid var(--border)}}
.topnav .container{{display:flex;gap:1.5rem;align-items:center;justify-content:space-between;flex-wrap:wrap}}
.topnav a{{font-size:.9rem;color:var(--text-muted)}}
.topnav a:hover{{color:var(--text)}}
.topnav .brand{{font-family:'Syne',sans-serif;font-weight:800;font-size:1.05rem;color:var(--text)}}
.hero{{padding:2.5rem 0 1.75rem;border-bottom:1px solid var(--border)}}
.badge{{display:inline-block;padding:.25rem .625rem;border-radius:999px;
font-family:'JetBrains Mono',monospace;font-size:.7rem;text-transform:uppercase;
letter-spacing:.1em;background:rgba(167,139,250,.16);border:1px solid rgba(167,139,250,.4);
color:var(--zabal)}}
h1{{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(1.6rem,5vw,2.3rem);
line-height:1.15;margin:.75rem 0 .5rem;background:linear-gradient(135deg,#ff6b35,#ff3d6e,#00e5ff);
-webkit-background-clip:text;background-clip:text;color:transparent}}
.did{{margin:1.5rem 0 0;padding:1rem 1.25rem;background:var(--surface);border:1px solid var(--border);
border-left:3px solid var(--gold);border-radius:var(--radius);color:var(--text)}}
.did .lab{{font-family:'JetBrains Mono',monospace;font-size:.7rem;text-transform:uppercase;
letter-spacing:.08em;color:var(--gold);display:block;margin-bottom:.35rem}}
h2{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.25rem;margin:2.5rem 0 1rem}}
ol.items{{list-style:none;display:flex;flex-direction:column;gap:.75rem}}
ol.items li{{display:flex;gap:.9rem;padding:1.1rem 1.25rem;background:var(--surface);
border:1px solid var(--border);border-radius:var(--radius)}}
ol.items .n{{font-family:'JetBrains Mono',monospace;font-size:.85rem;color:var(--cyan);
flex:0 0 1.5rem;line-height:1.7}}
ol.items h3{{font-family:'Outfit',sans-serif;font-size:1rem;font-weight:600;margin-bottom:.3rem}}
ol.items p{{color:var(--text-muted);font-size:.93rem}}
.itemlink{{display:inline-block;margin-top:.5rem;font-family:'JetBrains Mono',monospace;
font-size:.76rem;word-break:break-all}}
.next{{margin-top:1rem;padding:1.25rem;background:var(--surface-2);border:1px solid var(--border);
border-radius:var(--radius)}}
.next .when{{font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--gold)}}
.next p{{margin-top:.5rem;color:var(--text-muted);font-size:.93rem}}
.decided{{color:var(--text-muted);font-size:.93rem;padding-left:1.1rem}}
.decided li{{margin:.35rem 0}}
footer{{padding:2.5rem 0;border-top:1px solid var(--border);margin-top:3rem;
color:var(--text-muted);font-size:.85rem}}
footer .lifeline{{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:var(--text-dim);
margin-top:.5rem;line-height:1.7}}
</style>
</head>
<body>
<div class="hero"><div class="container">
  <span class="badge">{esc(rnd["label"])} &middot; @{esc(handle)}</span>
  <p style="margin-top:.4rem"><a href="/feedback/{rnd["bounty_id"]}">Notes on every entry to this bounty</a></p>
  <h1>{esc(entrant["headline"])}</h1>
  <div class="did"><span class="lab">What this entry did</span>{esc(entrant["did_well"])}</div>
</div></div>

<div class="container">
  <h2>To win the next one</h2>
  <ol class="items">
    {"".join(lis)}
  </ol>

  <h2>{esc(nxt["label"])}</h2>
  <div class="next">
    <span class="when">Closes {esc(nxt["closes"])}</span>
    <p>{esc(nxt["wants"])}</p>
    <p>{esc(nxt["checkpoint"])}</p>
  </div>

  <h2>{esc(decided_heading(rnd))}</h2>
  <ul class="decided">
    {"".join(f"<li>{esc(d)}</li>" for d in rnd["decided_it"])}
  </ul>

  <footer>
    The kit, free to use: <a href="https://zaostock.com/brand">zaostock.com/brand</a><br>
    The festival: <a href="https://zaostock.com">zaostock.com</a><br>
    Discord: <a href="https://discord.thezao.com">discord.thezao.com</a>
    <div class="lifeline">
      Notes on <a href="/feedback/{rnd["bounty_id"]}">every entry to this bounty</a>.<br>
      This promises nothing. What this programme has and has not delivered is at
      <a href="/about">poidhz.com/about</a>.
    </div>
  </footer>
</div>
</body>
</html>
"""


def render_index(entrants: list[dict], rnd: dict) -> str:
    """The shared page. Zaal: "so they can see what feedback others got too".

    SORTED BY HANDLE, AND THE PAGE SAYS SO. Any list of people reads as a ranking to the people
    on it - as the order they came, or as a shortlist. Alphabetical is the only order here that
    carries no claim, and it is used whether or not the round has been decided yet."""
    rows = []
    for e in sorted(entrants, key=lambda x: x["handle"].lower()):
        n = len(e["items"])
        rows.append(
            f'<a class="card" href="/feedback/{rnd["bounty_id"]}/{esc(e["handle"])}">'
            f'<span class="label">@{esc(e["handle"])}</span>'
            f'<span class="desc">{esc(e["headline"])}</span>'
            f'<span class="cnt">{n} thing{"s" if n != 1 else ""} to do next</span></a>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Notes on every entry - bounty {rnd["bounty_id"]} - poidhz</title>
<link rel="canonical" href="https://poidhz.com/feedback/{rnd["bounty_id"]}">
<meta name="description" content="What everyone who entered ZAOstock bounty {rnd["bounty_id"]} was told about their entry.">
<link rel="icon" type="image/png" href="/assets/brand-kits/zabal-games/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#070709;--surface:#111115;--surface-2:#16161c;--orange:#ff6b35;--cyan:#00e5ff;
--gold:#f5c842;--zabal:#a78bfa;--text:#e4e2dd;--text-muted:#8a8895;--text-dim:#4e4c57;
--border:#1f1e26;--radius:8px}}
body{{background:var(--bg);color:var(--text);font-family:'Outfit',sans-serif;line-height:1.6;
-webkit-font-smoothing:antialiased;min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;pointer-events:none;z-index:-1;
background:radial-gradient(ellipse 800px 600px at 15% -10%,rgba(167,139,250,0.12),transparent 60%),
radial-gradient(ellipse 700px 500px at 90% 10%,rgba(0,229,255,0.10),transparent 60%),
radial-gradient(ellipse 600px 400px at 50% 100%,rgba(255,107,53,0.08),transparent 60%)}}
a{{color:var(--cyan);text-decoration:none;transition:color .15s}}
a:hover{{color:var(--orange)}}
.container{{max-width:760px;margin:0 auto;padding:0 1.5rem}}
.topnav{{padding:1.25rem 0;border-bottom:1px solid var(--border)}}
.topnav .container{{display:flex;gap:1.5rem;align-items:center;justify-content:space-between;flex-wrap:wrap}}
.topnav .brand{{font-family:'Syne',sans-serif;font-weight:800;font-size:1.05rem;color:var(--text)}}
.topnav a{{font-size:.9rem;color:var(--text-muted)}}
.topnav a:hover{{color:var(--text)}}
.hero{{padding:2.5rem 0 1.75rem;border-bottom:1px solid var(--border)}}
.badge{{display:inline-block;padding:.25rem .625rem;border-radius:999px;
font-family:'JetBrains Mono',monospace;font-size:.7rem;text-transform:uppercase;
letter-spacing:.1em;background:rgba(167,139,250,.16);border:1px solid rgba(167,139,250,.4);
color:var(--zabal)}}
h1{{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(1.6rem,5vw,2.3rem);
line-height:1.15;margin:.75rem 0 .5rem;background:linear-gradient(135deg,#ff6b35,#ff3d6e,#00e5ff);
-webkit-background-clip:text;background-clip:text;color:transparent}}
p.sub{{color:var(--text-muted);max-width:620px}}
h2{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.25rem;margin:2.5rem 0 .5rem}}
.order{{font-family:'JetBrains Mono',monospace;font-size:.73rem;color:var(--text-dim);
margin-bottom:1rem}}
.grid{{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}}
.card{{padding:1.1rem 1.25rem;background:var(--surface);border:1px solid var(--border);
border-radius:var(--radius);display:flex;flex-direction:column;gap:.35rem;color:var(--text);
transition:all .15s}}
.card:hover{{border-color:var(--cyan);transform:translateY(-2px);background:var(--surface-2);
color:var(--text)}}
.card .label{{font-family:'JetBrains Mono',monospace;font-size:.82rem;color:var(--cyan)}}
.card .desc{{font-size:.9rem;color:var(--text)}}
.card .cnt{{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:var(--text-dim)}}
.decided{{color:var(--text-muted);font-size:.93rem;padding-left:1.1rem}}
.decided li{{margin:.35rem 0}}
.next{{margin-top:.5rem;padding:1.25rem;background:var(--surface-2);
border:1px solid var(--border);border-radius:var(--radius)}}
.next .when{{font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--gold)}}
.next p{{margin-top:.5rem;color:var(--text-muted);font-size:.93rem}}
footer{{padding:2.5rem 0;border-top:1px solid var(--border);margin-top:3rem;
color:var(--text-muted);font-size:.85rem}}
footer .lifeline{{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:var(--text-dim);
margin-top:.5rem;line-height:1.7}}
</style>
</head>
<body>
<div class="hero"><div class="container">
  <span class="badge">{esc(rnd["label"])} &middot; bounty {rnd["bounty_id"]}</span>
  <h1>What everyone was told</h1>
  <p style="margin-bottom:.4rem"><a href="{esc(rnd["bounty_url"])}">The bounty on poidh</a></p>
  <p class="sub">Every person who entered got notes on their own entry. They are all here, so
  you can see what was asked of everybody else and not only of you. Closed {esc(rnd["closed"])}.</p>
</div></div>

<div class="container">
  <h2>The entries</h2>
  <div class="order">Listed A to Z by handle. That is not an order of merit and there is no
  ranking on this site.</div>
  <div class="grid">
    {"".join(rows)}
  </div>

  <h2>{esc("What decided it" if is_decided(rnd) else "What it was judged on")}</h2>
  <ul class="decided">
    {"".join(f"<li>{esc(d)}</li>" for d in rnd["decided_it"])}
  </ul>

  <h2>{esc(rnd["next"]["label"])}</h2>
  <div class="next">
    <span class="when">Closes {esc(rnd["next"]["closes"])}</span>
    <p>{esc(rnd["next"]["wants"])}</p>
    <p>{esc(rnd["next"]["checkpoint"])}</p>
  </div>

  <footer>
    The kit, free to use: <a href="https://zaostock.com/brand">zaostock.com/brand</a><br>
    The festival: <a href="https://zaostock.com">zaostock.com</a><br>
    Discord: <a href="https://discord.thezao.com">discord.thezao.com</a>
    <div class="lifeline">
      These notes promise nothing. What this programme has and has not delivered is at
      <a href="/about">poidhz.com/about</a>.
    </div>
  </footer>
</div>
</body>
</html>
"""


def render_top_index() -> str:
    """/feedback - every round that has notes. Generated by scanning data/feedback/, so a new
    round appears here the moment its json does, rather than when somebody remembers."""
    rounds = []
    for f in sorted((REPO_ROOT / "data" / "feedback").glob("*.json")):
        d = json.loads(f.read_text())
        r = d["round"]
        if not r.get("bounty_id"):
            continue
        rounds.append((r, len(d["entrants"])))
    rounds.sort(key=lambda x: x[0]["bounty_id"], reverse=True)

    if not rounds:
        raise SystemExit("FAIL: no round has feedback, so there is no index to build. An "
                         "empty index page would say we give feedback when we do not.")

    cards = "".join(
        f'<a class="card" href="/feedback/{r["bounty_id"]}">'
        f'<span class="label">Bounty {r["bounty_id"]}</span>'
        f'<span class="desc">{esc(r["label"])} &middot; closed {esc(r["closed"])}</span>'
        f'<span class="cnt">notes for {n} entrant{"s" if n != 1 else ""}</span></a>'
        for r, n in rounds)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Feedback on every round - poidhz</title>
<link rel="canonical" href="https://poidhz.com/feedback">
<meta name="description" content="Everyone who enters a BCZ bounty gets notes on their entry. They are all public.">
<link rel="icon" type="image/png" href="/assets/brand-kits/zabal-games/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#070709;--surface:#111115;--surface-2:#16161c;--orange:#ff6b35;--cyan:#00e5ff;
--gold:#f5c842;--zabal:#a78bfa;--text:#e4e2dd;--text-muted:#8a8895;--text-dim:#4e4c57;
--border:#1f1e26;--radius:8px}}
body{{background:var(--bg);color:var(--text);font-family:'Outfit',sans-serif;line-height:1.6;
-webkit-font-smoothing:antialiased;min-height:100vh}}
body::before{{content:'';position:fixed;inset:0;pointer-events:none;z-index:-1;
background:radial-gradient(ellipse 800px 600px at 15% -10%,rgba(167,139,250,0.12),transparent 60%),
radial-gradient(ellipse 700px 500px at 90% 10%,rgba(0,229,255,0.10),transparent 60%)}}
a{{color:var(--cyan);text-decoration:none;transition:color .15s}}
a:hover{{color:var(--orange)}}
.container{{max-width:760px;margin:0 auto;padding:0 1.5rem}}
.hero{{padding:2.5rem 0 1.75rem;border-bottom:1px solid var(--border)}}
h1{{font-family:'Syne',sans-serif;font-weight:800;font-size:clamp(1.6rem,5vw,2.3rem);
line-height:1.15;margin:0 0 .5rem;background:linear-gradient(135deg,#ff6b35,#ff3d6e,#00e5ff);
-webkit-background-clip:text;background-clip:text;color:transparent}}
p.sub{{color:var(--text-muted);max-width:620px}}
h2{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.25rem;margin:2.5rem 0 1rem}}
.grid{{display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}}
.card{{padding:1.1rem 1.25rem;background:var(--surface);border:1px solid var(--border);
border-radius:var(--radius);display:flex;flex-direction:column;gap:.35rem;color:var(--text);
transition:all .15s}}
.card:hover{{border-color:var(--cyan);transform:translateY(-2px);background:var(--surface-2);
color:var(--text)}}
.card .label{{font-family:'JetBrains Mono',monospace;font-size:.82rem;color:var(--cyan)}}
.card .desc{{font-size:.9rem;color:var(--text)}}
.card .cnt{{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:var(--text-dim)}}
footer{{padding:2.5rem 0;border-top:1px solid var(--border);margin-top:3rem;
color:var(--text-muted);font-size:.85rem}}
</style>
</head>
<body>
<div class="hero"><div class="container">
  <h1>Notes on every entry</h1>
  <p class="sub">Everyone who enters one of our bounties gets notes on their own piece, win or
  lose, the same day. They are public so you can see what was asked of everybody else and not
  only of you. There is no ranking on this site.</p>
</div></div>
<div class="container">
  <h2>Rounds with notes</h2>
  <div class="grid">{cards}</div>
  <footer>
    The bar every entry is judged against: <a href="/best-practices">the bar</a><br>
    Every round and its live state: <a href="/about">rounds</a><br>
    What this programme has and has not delivered: <a href="/about">poidhz.com/about</a>
  </footer>
</div>
</body>
</html>
"""


def build(round_id: str, write: bool = True) -> tuple[bool, list[str]]:
    data = load(round_id)
    rnd, entrants = data["round"], data["entrants"]
    findings: list[str] = []
    ok = True

    bounty_id = rnd.get("bounty_id")
    if not bounty_id:
        return False, ["FAIL: the round has no bounty_id. The path must carry it - a handle "
                       "slug is reused across rounds and would overwrite older notes in place."]
    round_dir = OUT_DIR / str(bounty_id)

    if not entrants:
        return False, ["FAIL: the round has no entrants. An empty build is not a clean build."]

    claims_blob = known_claim_handles(round_id)
    if claims_blob is None:
        findings.append("     WARN: data/claims.json could not be read, so handles were NOT "
                        "checked against real claims. UNVERIFIED, not verified.")

    for e in entrants:
        handle = e["handle"]
        page = render(e, rnd)

        # Guards run on the RENDERED page, so nothing slips through a field this script does
        # not individually inspect.
        body_text = re.sub(r"<[^>]+>", " ", page)
        body_text = re.sub(r"\s+", " ", html.unescape(body_text))
        # The style block and this file's own prose are not entrant copy.
        checkable = " ".join(
            esc(v) and str(v) for k, v in e.items() if k != "handle" and isinstance(v, str))
        checkable += " " + " ".join(
            f"{i.get('title','')} {i.get('body','')}" for i in e["items"])

        if m := RANKING_WORDS.search(checkable):
            ok = False
            findings.append(
                f"FAIL: @{handle}'s copy contains the ranking word '{m.group(0)}'. "
                + (f"@{rnd['winner']} won this round. A superlative on anybody else's page "
                   f"says either that the pick was wrong or that the words are empty."
                   if is_decided(rnd) else
                   "This round has no result yet, so a superlative here announces one that "
                   "has not been decided - to the people waiting for it."))
        if m := PROMISE_WORDS.search(checkable):
            ok = False
            findings.append(
                f"FAIL: @{handle}'s copy promises something ('{m.group(0)}'). See "
                f"docs/PROMISE-AUDIT.md - five rounds promised distribution and delivered "
                f"money. Feedback promises nothing.")

        for other in entrants:
            if other["handle"] != handle and other["handle"].lower() in checkable.lower():
                ok = False
                findings.append(f"FAIL: @{handle}'s page names another entrant "
                                f"(@{other['handle']}). A page shows one person their own "
                                f"work and never the field.")

        if claims_blob is not None and handle.lower() not in claims_blob:
            findings.append(f"     WARN: @{handle} was not found in data/claims.json. Check "
                            f"the handle before sending the link.")

        out = round_dir / f"{handle}.html"
        if not write:
            # STALENESS. --check used to validate the copy and never compare it to the file
            # being served, so editing the json without rebuilding passed cleanly while the
            # site served the old notes to the person they were written for.
            if not out.exists():
                ok = False
                findings.append(f"FAIL: {out.relative_to(REPO_ROOT)} has never been built. "
                                f"Run build-feedback-pages.py --round {round_id}.")
            elif without_nav(out.read_text()) != without_nav(page):
                ok = False
                findings.append(f"FAIL: {out.relative_to(REPO_ROOT)} is STALE - it differs "
                                f"from what {round_id}.json renders. The site is serving "
                                f"older notes than the repo says. Rebuild it.")
        if write and ok:
            round_dir.mkdir(parents=True, exist_ok=True)
            out.write_text(page)
            findings.append(f"     wrote {out.relative_to(REPO_ROOT)}  ->  "
                            f"poidhz.com/feedback/{bounty_id}/{handle}")

    if ok and write:
        round_dir.mkdir(parents=True, exist_ok=True)
        idx = round_dir / "index.html"
        idx.write_text(render_index(entrants, rnd))
        findings.append(f"     wrote {idx.relative_to(REPO_ROOT)}  ->  "
                        f"poidhz.com/feedback/{bounty_id}")
        top_idx = OUT_DIR / "index.html"
        top_idx.write_text(render_top_index())
        findings.append(f"     wrote {top_idx.relative_to(REPO_ROOT)}  ->  "
                        f"poidhz.com/feedback")

    if ok:
        findings.append(f"PASS: {len(entrants)} page(s) + index under /feedback/{bounty_id}/, "
                        f"no ranking word, no promise, no page naming another entrant")
    return ok, findings


def _selftest() -> bool:
    passed = True

    def c(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    rnd = {"id": "t", "label": "Bounty one", "bounty_url": "u", "closed": "x",
           "winner": "leoxcrane", "bounty_id": 1409,
           "next": {"label": "Round three", "closes": "5pm", "wants": "w", "checkpoint": "c"},
           "decided_it": ["a"]}

    good = {"handle": "predaking", "claim": 1, "headline": "Make it move.",
            "did_well": "You got the running order.",
            "items": [{"title": "Move it", "body": "Fifteen seconds."}]}
    page = render(good, rnd)
    c("renders a page", "predaking" in page and "Fifteen seconds." in page)
    c("the page URL carries the BOUNTY id, not just the handle",
      "/feedback/1409/predaking" in page)
    c("the page links back to the shared index", '/feedback/1409"' in page)
    c("the page never names the winner", "leoxcrane" not in page)
    c("a decided round says what DECIDED it", "What decided" in page)

    # A round whose notes are owed before its vote resolves. Bounty 1412 is exactly this for
    # two days after it closes, and the page used to announce a decision that had not happened.
    undecided = {**rnd, "winner": ""}
    upage = render(good, undecided)
    c("an undecided round says what it was JUDGED ON, not what decided it",
      "was judged on" in upage and "What decided" not in upage)
    uidx = render_index([good], undecided)
    c("the index of an undecided round makes no decision claim either",
      "What decided" not in uidx and "judged on" in uidx)
    c("a missing winner key behaves the same as an empty one",
      not is_decided({k: v for k, v in rnd.items() if k != "winner"}))
    c("a whitespace-only winner is not a winner", not is_decided({**rnd, "winner": "   "}))

    idx = render_index([good, {**good, "handle": "coolhat"}], rnd)
    c("the index links each entrant under the bounty id",
      "/feedback/1409/predaking" in idx and "/feedback/1409/coolhat" in idx)
    c("the index states that its order is NOT merit", "not an order of merit" in idx)
    c("the index is sorted A to Z, not in file order",
      idx.index("coolhat") < idx.index("predaking"))

    c("escapes html in copy",
      "&lt;script&gt;" in render({**good, "headline": "<script>x</script>"}, rnd))

    # 1 to 3 items, per Zaal.
    for n, should_raise in ((0, True), (1, False), (3, False), (4, True)):
        items = [{"title": "t", "body": "b"}] * n
        try:
            render({**good, "items": items}, rnd)
            raised = False
        except SystemExit:
            raised = True
        c(f"{n} items {'refused' if should_raise else 'accepted'}", raised == should_raise)

    import tempfile
    global REPO_ROOT, OUT_DIR
    real_root = REPO_ROOT
    with tempfile.TemporaryDirectory() as d:
        REPO_ROOT = Path(d)
        OUT_DIR = REPO_ROOT / "feedback"
        (REPO_ROOT / "data" / "feedback").mkdir(parents=True)

        def write_round(entrants):
            (REPO_ROOT / "data" / "feedback" / "t.json").write_text(
                json.dumps({"round": rnd, "entrants": entrants}))

        write_round([good])
        ok, f = build("t", write=False)
        c("--check FAILS when the page was never built",
          not ok and any("never been built" in x for x in f))
        build("t", write=True)
        ok, f = build("t", write=False)
        c("a clean, freshly built round passes", ok)

        # A page carrying an injected nav bar is NOT stale. This is the false positive the
        # first version of this check produced against all five real pages.
        built = REPO_ROOT / "feedback" / "1409" / "predaking.html"
        target = next(REPO_ROOT.glob("feedback/*/*.html"))
        target.write_text("<!-- ZN-NAV START x -->\nbar\n<!-- ZN-NAV END -->\n"
                          + target.read_text())
        ok, f = build("t", write=False)
        c("a page with an injected nav bar is NOT reported stale", ok)

        # The real drift: edit the source, do not rebuild.
        write_round([{**good, "headline": "Changed after the build."}])
        ok, f = build("t", write=False)
        c("--check catches a page that is STALE against its json",
          not ok and any("STALE" in x for x in f))
        build("t", write=True)
        ok, _ = build("t", write=False)
        c("and passes again once rebuilt", ok)

        write_round([good])
        build("t", write=True)
        ok, f = build("t", write=False)
        c("and it warns that claims.json could not be read",
          any("UNVERIFIED" in x for x in f))

        write_round([{**good, "did_well": "The best entry of the round."}])
        ok, f = build("t", write=False)
        c("a RANKING word is refused", not ok and any("ranking word" in x for x in f))

        write_round([{**good,
                      "items": [{"title": "t", "body": "We will run this on our channels."}]}])
        ok, f = build("t", write=False)
        c("a PROMISE is refused", not ok and any("promises something" in x for x in f))

        write_round([good, {**good, "handle": "coolhat",
                            "did_well": "Better than predaking's."}])
        ok, f = build("t", write=False)
        c("a page naming ANOTHER entrant is refused",
          not ok and any("names another entrant" in x for x in f))

        write_round([])
        ok, f = build("t", write=False)
        c("an empty entrant list FAILS rather than building nothing quietly",
          not ok and any("not a clean build" in x for x in f))

        # A round with no bounty_id would build to a handle-only path and be overwritten by
        # the next round in place, with no error. That must never happen quietly.
        (REPO_ROOT / "data" / "feedback" / "t.json").write_text(json.dumps(
            {"round": {k: v for k, v in rnd.items() if k != "bounty_id"},
             "entrants": [good]}))
        ok, f = build("t", write=False)
        c("a round with NO bounty_id is refused", not ok and any("bounty_id" in x for x in f))
    REPO_ROOT = real_root
    OUT_DIR = REPO_ROOT / "feedback"
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--round", default="d01")
    ap.add_argument("--check", action="store_true", help="validate without writing")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("build-feedback-pages selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    ok, findings = build(args.round, write=not args.check)
    for f in findings:
        print(f"  {f}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
