#!/usr/bin/env python3
"""Probe every external link the site actually offers a visitor, with controls.

WHY. `check-site-claims.py` verifies INTERNAL links and round claims. Nothing checked the
outbound ones, and this site's whole job is sending people somewhere else: the brand kit, the
lineup, the bounty, the leaderboard, Discord. A dead kit link on a page telling somebody to
build with the kit is the most expensive dead link here.

WHAT IT REFUSES TO COUNT AS A LINK, because a first pass at this reported 5 failures and all
five were the checker's fault rather than the site's (2026-09-22, 51 urls, 46 clean):

  - **`rel="preconnect"` and `dns-prefetch` hints.** `https://fonts.googleapis.com` with no
    path returns 404 by design. It is a performance hint, not something a visitor can click.
  - **Anything inside a `<script>` block.** A regex over `href="..."` happily matches the
    middle of a JavaScript string: `'.../tree/main/'+esc(folder)+'...'` came back as the URL
    `https://github.com/.../tree/main/+esc(folder)+`, and
    `'https://poidh.xyz/account/ ' + esc(currentAccount)` failed to connect at all. Neither is
    a link; both are code.

CONTROLS RUN FIRST AND THE CHECK ABORTS IF EITHER FAILS. A link checker that cannot reach the
network reports every URL dead, and a link checker behind a captive portal reports every URL
alive. Both look like results. So: one URL that must answer, one that must not.

**A connection failure is NOT a pass.** The first run of this by hand treated curl's `000` as
acceptable alongside 200, which would have hidden a host that had stopped resolving entirely.
It is counted and reported separately.

This is deliberately NOT a PR gate - it depends on other people's servers, and a check that
fails for reasons the author cannot fix is a check that gets ignored.

    python3 scripts/check-external-links.py
    python3 scripts/check-external-links.py --selftest
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SCRIPT_BLOCK = re.compile(r"<script\b.*?</script>", re.S | re.I)
# A <link> whose rel is a connection hint, not a destination.
HINT_LINK = re.compile(r"<link\b[^>]*rel=[\"'](?:preconnect|dns-prefetch)[\"'][^>]*>", re.I)
HREF = re.compile(r'href="(https?://[^"]+)"')

CONTROL_LIVE = "https://example.com"
CONTROL_DEAD = "https://poidhz.com/definitely-not-a-real-path-9f3a2c"


def pages(root: Path = REPO_ROOT) -> list[Path]:
    out = sorted(root.glob("*.html")) + sorted((root / "docs").glob("*.html"))
    fb = root / "feedback"
    if fb.is_dir():
        out += sorted(fb.rglob("*.html"))
    return out


def links_in(text: str) -> set[str]:
    """Only the hrefs a visitor could click."""
    text = SCRIPT_BLOCK.sub(" ", text)
    text = HINT_LINK.sub(" ", text)
    return {m.group(1).rstrip(".,") for m in HREF.finditer(text)}


def probe(url: str, timeout: int = 20) -> str:
    try:
        r = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}",
             "-A", "Mozilla/5.0", "--max-time", str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 10)
        return (r.stdout or "000").strip()
    except Exception:
        return "000"


def run(root: Path = REPO_ROOT) -> tuple[bool, list[str]]:
    findings: list[str] = []

    live = probe(CONTROL_LIVE)
    dead = probe(CONTROL_DEAD)
    if live != "200":
        return False, [f"ABORT: control {CONTROL_LIVE} returned {live}, not 200. No network, "
                       f"or something is intercepting requests. Every result would read as "
                       f"dead, which is not a finding."]
    if dead == "200":
        return False, [f"ABORT: control {CONTROL_DEAD} returned 200. Something answers every "
                       f"request, so every result would read as alive."]
    findings.append(f"     controls ok: live={live}, dead={dead}")

    found: dict[str, set[str]] = defaultdict(set)
    ps = pages(root)
    if not ps:
        return False, ["FAIL: found no html pages at all. An empty sweep is not a clean site."]
    for p in ps:
        for u in links_in(p.read_text()):
            found[u].add(str(p.relative_to(root)))
    if not found:
        return False, [f"FAIL: {len(ps)} page(s) scanned and not one external link found. "
                       f"The pattern is wrong, or the pages changed shape."]

    ok = broken = failed = 0
    for url in sorted(found):
        code = probe(url)
        where = ", ".join(sorted(found[url])[:3])
        if code == "200":
            ok += 1
        elif code == "000":
            failed += 1
            findings.append(f"FAIL: could not connect at all - {url}  ({where})")
        else:
            broken += 1
            findings.append(f"FAIL: HTTP {code} - {url}  ({where})")

    total = len(found)
    assert ok + broken + failed == total, "tally does not account for every url"
    findings.append(f"     {total} external link(s) across {len(ps)} page(s): "
                    f"{ok} ok, {broken} non-200, {failed} unreachable")
    if not broken and not failed:
        findings.append("PASS: every external link the site offers a visitor answers")
    return (broken == 0 and failed == 0), findings


def _selftest() -> bool:
    passed = True

    def c(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    # The three real false positives from the first hand-run.
    page = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<a href="https://zaostock.com/brand">kit</a>
<script>
  var x='<a href="https://github.com/bettercallzaal/zpoidh/tree/main/'+esc(folder)+'">R</a>';
  var y='https://poidh.xyz/account/ ' + esc(acct);
</script>'''
    got = links_in(page)
    c("a real anchor is found", "https://zaostock.com/brand" in got)
    c("preconnect hints are NOT treated as links",
      not any("fonts.g" in u for u in got))
    c("hrefs inside <script> are NOT treated as links",
      not any("tree/main" in u for u in got))
    c("exactly one link in that page", len(got) == 1)

    c("a trailing comma is stripped",
      links_in('<a href="https://zaostock.com/brand,">k</a>') == {"https://zaostock.com/brand"})

    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs").mkdir()
        ok, f = run(root)
        c("no pages at all FAILS rather than reporting clean",
          not ok and any("no html pages" in x for x in f))

        (root / "index.html").write_text("<html><body>nothing external</body></html>")
        ok, f = run(root)
        c("pages with zero external links FAILS rather than reporting clean",
          not ok and any("not one external link" in x for x in f))
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        print("check-external-links selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    ok, findings = run()
    for f in findings:
        print(f"  {f}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
