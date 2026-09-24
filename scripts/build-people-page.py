#!/usr/bin/env python3
"""Render /people - who has actually made something for this programme, and who came back.

WHY. The site could tell you what every ROUND did and nothing about who turned up. The most
interesting fact in this whole dataset is not a pot size: it is that **eight people have
entered more than one bounty, and five of those were around for the BCZ YapZ rounds in May and
came back for ZAOstock in September.** That is a community forming, and it was invisible.

WHAT IT REFUSES TO BE. Not a ranking. The leaderboard score is a count of accepted claims -
participation, not quality - and the page says so in its own words where a reader cannot miss
it. This repo already refuses ranking words on the feedback pages for the same reason: a
ranking published next to someone's name reads as a verdict on their work.

WHY PUBLISHING HANDLES IS FINE HERE. Every handle comes from a claim the entrant filed
publicly on a public chain, or from the Empire Builder leaderboard, which is public. The
feedback pages already name people, on Zaal's explicit ruling of 2026-09-22 - "so they can see
what feedback others got too". Nothing on this page is private, and nothing is inferred about
anybody.

    python3 scripts/build-people-page.py
    python3 scripts/build-people-page.py --check
    python3 scripts/build-people-page.py --selftest
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
OUT = REPO_ROOT / "people.html"
FEEDBACK = REPO_ROOT / "feedback"

# The ZAOstock run, as distinct from the BCZ YapZ / ZABAL Gamez / WaveWarZ rounds before it.
ZAOSTOCK = {1409, 1410, 1412}


def esc(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def load() -> dict:
    if not RICH.exists():
        raise SystemExit(f"FAIL: {RICH} does not exist. Run refresh-poidh-leaderboard.py.")
    d = json.loads(RICH.read_text())
    if not d.get("claims"):
        raise SystemExit("FAIL: claims.json has no claims. An empty people page would say "
                         "this programme has no people, which is a measurement failure, not "
                         "a fact.")
    return d


def build(d: dict) -> dict:
    """One record per person who has an accepted claim, plus the counts the page leads with."""
    lb = {r["address"].lower(): r for r in d.get("leaderboard", [])}
    titles = {b["id"]: b["title"] for b in d.get("bounties", [])}

    by = defaultdict(list)
    for c in d["claims"]:
        by[c["issuer"].lower()].append(c)

    people = []
    for addr, claims in by.items():
        row = lb.get(addr, {})
        bounties = sorted({c["bounty_id"] for c in claims})
        handle = (row.get("farcaster_username") or row.get("twitter_handle")
                  or row.get("displayName") or addr[:10] + "...")
        people.append({
            "addr": addr,
            "handle": handle,
            "resolved": bool(row.get("farcaster_username") or row.get("twitter_handle")),
            "fc": row.get("farcaster_username"),
            "x": row.get("twitter_handle"),
            "bounties": bounties,
            "claims": len(claims),
            "zaostock": sorted(set(bounties) & ZAOSTOCK),
            "older": sorted(set(bounties) - ZAOSTOCK),
        })

    # Order: most bounties entered, then most claims, then handle. NOT by score, and the
    # page says why.
    people.sort(key=lambda p: (-len(p["bounties"]), -p["claims"], p["handle"].lower()))

    returning = [p for p in people if len(p["bounties"]) > 1]
    bridge = [p for p in people if p["zaostock"] and p["older"]]
    return {"people": people, "returning": returning, "bridge": bridge, "titles": titles}


def feedback_links(handle: str) -> list[tuple[int, str]]:
    """Every feedback page that exists for this handle, by bounty. Measured off disk, so the
    page never links a note that was never written."""
    out = []
    if not FEEDBACK.is_dir():
        return out
    for d in sorted(FEEDBACK.iterdir()):
        if d.is_dir() and d.name.isdigit() and (d / f"{handle}.html").exists():
            out.append((int(d.name), f"/feedback/{d.name}/{handle}"))
    return out


def render(model: dict) -> str:
    people, returning, bridge = model["people"], model["returning"], model["bridge"]
    rows = []
    for p in people:
        fb = feedback_links(p["handle"])
        notes = " ".join(f'<a href="{u}">notes</a>' for _, u in fb) or \
                '<span class="dim">-</span>'
        # FARCASTER FIRST, AND X ONLY WHEN THERE IS NO FARCASTER. Two of the X handles
        # carried on the leaderboard return 404 - onlybased_god and i_d0_care - and both of
        # those people have a live Farcaster account. A Farcaster username resolves through
        # the fname registry; an X handle on this feed is a string that was true once. Both
        # dead links disappear without dropping a single person's way of being reached.
        links = []
        if p["fc"]:
            links.append(f'<a href="https://farcaster.xyz/{esc(p["fc"])}">fc</a>')
        elif p["x"]:
            links.append(f'<a href="https://x.com/{esc(p["x"])}">x</a>')
        who = f'@{esc(p["handle"])}' if p["resolved"] else \
              f'<span class="dim" title="{esc(p["addr"])}">{esc(p["handle"])}</span>'
        era = []
        if p["older"]:
            era.append(f'<span class="tag old">{len(p["older"])} before ZAOstock</span>')
        if p["zaostock"]:
            era.append(f'<span class="tag new">{len(p["zaostock"])} ZAOstock</span>')
        rows.append(
            f'<tr><td>{who}<div class="sub">{" ".join(links)}</div></td>'
            f'<td>{len(p["bounties"])}</td><td>{p["claims"]}</td>'
            f'<td>{"".join(era)}</td><td>{notes}</td></tr>')

    bridge_list = ", ".join(f'@{esc(p["handle"])}' for p in bridge)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The people - poidhz</title>
<link rel="canonical" href="https://poidhz.com/people">
<meta name="description" content="Everyone who has made something for a ZAO bounty, how many rounds they entered, and the notes they got back.">
<meta property="og:title" content="The people who make things for ZAO bounties">
<meta property="og:description" content="{len(people)} people have filed an accepted claim. {len(returning)} have entered more than one round. {len(bridge)} were here before ZAOstock and came back.">
<meta property="og:url" content="https://poidhz.com/people">
<meta property="og:image" content="https://poidhz.com/assets/og/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://poidhz.com/assets/og/og.png">
<link rel="icon" type="image/png" href="/assets/brand-kits/zabal-games/icon.png">
<style>
:root{{--bg:#0d0b0a;--card:#161211;--line:#2a2320;--text:#f3ece6;--text-muted:#a99d94;
--text-dim:#6f645c;--orange:#e07a3f;--green:#7fa650;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);
font:16px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;}}
.wrap{{max-width:900px;margin:0 auto;padding:2rem 1rem 4rem}}
h1{{font-size:1.9rem;margin:.2rem 0 .4rem;letter-spacing:-.02em}}
h2{{font-size:1.15rem;margin:2.2rem 0 .6rem;letter-spacing:-.01em}}
p{{color:var(--text-muted);margin:.5rem 0}}
a{{color:var(--orange)}}
.lede{{font-size:1.05rem;color:var(--text)}}
.stats{{display:flex;flex-wrap:wrap;gap:.6rem;margin:1.2rem 0}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:.7rem 1rem;min-width:120px}}
.stat b{{display:block;font-size:1.5rem}}
.stat span{{color:var(--text-muted);font-size:.8rem}}
table{{width:100%;border-collapse:collapse;margin-top:.6rem;font-size:.92rem}}
th{{text-align:left;color:var(--text-dim);font-weight:600;font-size:.75rem;
text-transform:uppercase;letter-spacing:.06em;padding:.5rem .6rem;
border-bottom:1px solid var(--line)}}
td{{padding:.6rem;border-bottom:1px solid var(--line);vertical-align:top}}
.sub{{font-size:.78rem}} .sub a{{margin-right:.4rem}}
.dim{{color:var(--text-dim)}}
.tag{{display:inline-block;font-size:.7rem;padding:.12rem .45rem;border-radius:5px;
margin-right:.3rem;white-space:nowrap}}
.tag.old{{background:#2a2320;color:var(--text-muted)}}
.tag.new{{background:#2a2012;color:var(--orange)}}
.note{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--green);
border-radius:8px;padding:.9rem 1rem;margin:1.2rem 0;font-size:.92rem}}
footer{{margin-top:3rem;padding-top:1.2rem;border-top:1px solid var(--line);
color:var(--text-dim);font-size:.85rem}}
</style>
</head>
<body>
<div class="wrap">

  <h1>The people</h1>
  <p class="lede">Everyone who has made something for a ZAO bounty and had the claim accepted.
  Not a ranking - see the note below.</p>

  <div class="stats">
    <div class="stat"><b>{len(people)}</b><span>people</span></div>
    <div class="stat"><b>{len(returning)}</b><span>entered more than once</span></div>
    <div class="stat"><b>{len(bridge)}</b><span>came back for ZAOstock</span></div>
    <div class="stat"><b>{sum(p["claims"] for p in people)}</b><span>accepted claims</span></div>
  </div>

  <h2>The thing worth knowing</h2>
  <p>Seven bounties have run since May, across four completely different briefs - a podcast
  clip, an advert for poidh, a ZABAL Gamez ad, a WaveWarZ stream clip, then three ZAOstock
  rounds. <strong>{len(bridge)} people entered both an early round and a ZAOstock one:
  {bridge_list}.</strong> They had no reason to come back except that they wanted to.</p>

  <div class="note">
    <strong>This page is not a leaderboard and the order is not a verdict.</strong>
    It sorts by how many bounties someone entered, which is a count of showing up, not a
    judgement of the work. Somebody with one entry may have made the best thing here. No
    ranking of quality is published on this site, ever - the same rule the
    <a href="/feedback">feedback pages</a> are built to enforce.
  </div>

  <h2>Everyone, by how many rounds they turned up for</h2>
  <table>
    <thead><tr><th>Who</th><th>Bounties</th><th>Claims</th><th>When</th><th>Their notes</th></tr></thead>
    <tbody>
    {"".join(rows)}
    </tbody>
  </table>

  <footer>
    Built from <a href="/data/claims.json">claims.json</a>, which is regenerated from the chain
    and from the Empire Builder leaderboard - never typed by hand. Handles come from claims
    people filed publicly; four addresses have no linked handle and are shown as an address.<br>
    Every round: <a href="/">poidhz.com</a> &middot; What entrants were told:
    <a href="/feedback">the notes</a> &middot; What this programme has and has not delivered:
    <a href="/about">the record</a>.
  </footer>
</div>
</body>
</html>
"""


def _selftest() -> bool:
    passed = True

    def c(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    d = {
        "bounties": [{"id": 1151, "title": "old one"}, {"id": 1409, "title": "zaostock one"},
                     {"id": 1412, "title": "zaostock three"}],
        "leaderboard": [
            {"address": "0xaaa", "farcaster_username": "pascaline", "twitter_handle": "p7933"},
            {"address": "0xbbb", "farcaster_username": "newcomer"},
            {"address": "0xccc"},
        ],
        "claims": [
            {"issuer": "0xAAA", "bounty_id": 1151, "claim_id": 1},
            {"issuer": "0xAAA", "bounty_id": 1409, "claim_id": 2},
            {"issuer": "0xAAA", "bounty_id": 1412, "claim_id": 3},
            {"issuer": "0xBBB", "bounty_id": 1412, "claim_id": 4},
            {"issuer": "0xCCC", "bounty_id": 1151, "claim_id": 5},
        ],
    }
    m = build(d)
    c("one record per person, not per claim", len(m["people"]) == 3)
    c("the person in three bounties sorts first", m["people"][0]["handle"] == "pascaline")
    c("returning = entered more than one bounty", len(m["returning"]) == 1)
    c("bridge = entered BOTH eras", [p["handle"] for p in m["bridge"]] == ["pascaline"])
    c("someone only in ZAOstock is not a bridge",
      "newcomer" not in [p["handle"] for p in m["bridge"]])
    c("someone only in the old rounds is not a bridge either",
      len(m["bridge"]) == 1)
    c("an address with no handle is marked unresolved",
      any(not p["resolved"] for p in m["people"]))
    c("issuer case does not split one person into two",
      sum(p["claims"] for p in m["people"]) == 5)

    page = render(m)
    c("the page renders every person", all(f'@{p["handle"]}' in page or p["addr"][:10] in page
                                           for p in m["people"]))
    c("it says out loud that it is not a ranking",
      "not a leaderboard" in page and "not a verdict" in page)
    c("it never prints a score", "score" not in page.lower())
    c("the bridge names are in the copy", "pascaline" in page)
    # Two X handles on the real feed 404 and both of those people have Farcaster.
    c("X is not linked when Farcaster exists", "x.com/p7933" not in page)
    c("Farcaster is linked when it exists", "farcaster.xyz/pascaline" in page)
    xonly = build({**d, "leaderboard": [{"address": "0xaaa", "twitter_handle": "only_x"}],
                   "claims": [{"issuer": "0xAAA", "bounty_id": 1409, "claim_id": 1}]})
    c("X IS linked when there is no Farcaster", "x.com/only_x" in render(xonly))

    try:
        build({"claims": [], "leaderboard": [], "bounties": []})
        c("an empty claim set still builds (load() is what refuses it)", True)
    except Exception:
        c("an empty claim set still builds (load() is what refuses it)", False)
    try:
        import tempfile
        global RICH
        keep = RICH
        with tempfile.TemporaryDirectory() as t:
            RICH = Path(t) / "nope.json"
            try:
                load()
                c("a missing claims.json is REFUSED", False)
            except SystemExit:
                c("a missing claims.json is REFUSED", True)
        RICH = keep
    except Exception:
        c("a missing claims.json is REFUSED", False)
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        print("build-people-page selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    m = build(load())
    page = render(m)
    if a.check:
        if OUT.exists() and OUT.read_text() == page:
            print(f"  PASS: people.html matches the data - {len(m['people'])} people, "
                  f"{len(m['returning'])} returning")
            return 0
        print("  FAIL: people.html is stale. Run scripts/build-people-page.py.")
        return 1
    OUT.write_text(page)
    print(f"  wrote {OUT.relative_to(REPO_ROOT)} -> poidhz.com/people")
    print(f"  {len(m['people'])} people, {len(m['returning'])} entered more than one bounty, "
          f"{len(m['bridge'])} bridge both eras")
    print("  bridge: " + ", ".join(f"@{p['handle']}" for p in m["bridge"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
