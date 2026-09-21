#!/usr/bin/env python3
"""Refuse a bounty description whose line breaks a markdown renderer will silently eat.

WHY THIS EXISTS, MEASURED 2026-09-20. Every file in this repo said "Poidh renders plain text,
so keep the line breaks exactly as they are." That was wrong, and nobody found out until Zaal
pasted bounty one into the create form and read the PREVIEW tab back. Poidh renders markdown.
Three blocks were mangled, and every one of them was a single newline the renderer joined
into the paragraph above it:

  1. "Tagging @bettercallzaal ... is not required today" sat one blank line under a numbered
     list and was absorbed as a FIFTH numbered item. The single line whose whole job was to
     say a thing is optional rendered as a requirement.
  2. The rubric's group labels - Reach, Craft, Substance - sat directly above their bullets
     with no blank line, and were swallowed as lazy continuations of the bullet before them.
     The preview read "Someone who is not in this bounty shared it Craft".
  3. The five asset-kit links were five consecutive lines, so they collapsed into one
     paragraph and the most useful block in the description became a wall.

WHY IT IS WORTH A SCRIPT. A poidh description is IMMUTABLE once cast. There is exactly one
moment to catch this - the preview tab - and it depends on a human reading carefully at the
moment they are most eager to press the button. Thirteen days of this run each get a
description. The estate measures honor-system rules at 3-40% compliance and enforced ones at
~100%.

WHAT IT DOES NOT DO. It is not a markdown renderer and it does not claim to be. It refuses
the three SHAPES that actually bit us, which is a claim it can support, rather than promising
that the output will render correctly, which it cannot check. Read the preview anyway.

    python3 scripts/check-render-safe.py rounds/daily/d01/description.md
    python3 scripts/check-render-safe.py --all
    python3 scripts/check-render-safe.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PASTE_START = "<!-- PASTE BELOW THIS LINE -->"
PASTE_END = "<!-- PASTE ABOVE THIS LINE -->"

LIST_ITEM = re.compile(r"^\s*(?:\d+[.)]|[-*+])\s+\S")
URL_LINE = re.compile(r"https?://")
# A short line with no sentence-ending punctuation: a label, not prose.
LABEL = re.compile(r"^[A-Za-z][A-Za-z0-9 /&'-]{0,40}$")


def paste_body(text: str) -> str:
    if PASTE_START in text and PASTE_END in text:
        return text.split(PASTE_START, 1)[1].split(PASTE_END, 1)[0].strip() + "\n"
    return text


def check_text(body: str) -> list[str]:
    """Return one finding per render hazard. Empty list means none of the three were found."""
    lines = body.split("\n")
    findings = []

    for i, line in enumerate(lines):
        s = line.strip()
        prev = lines[i - 1].strip() if i > 0 else ""
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""

        # 1. A label directly above a list, with no blank line. It gets eaten by the list,
        #    or by the bullet above it. This is what happened to Craft and Substance.
        if s and LABEL.match(s) and not LIST_ITEM.match(line) and LIST_ITEM.match(nxt or ""):
            findings.append(
                f"line {i+1}: label {s!r} sits directly above a list item with no blank line "
                f"between. The renderer joins them - this is what turned 'Craft' into part of "
                f"the bullet above it. Put a blank line under the label.")

        # 2. Prose directly under a list item with no blank line: absorbed as another item.
        #    This is what made the optional tagging line read as a requirement.
        if s and not LIST_ITEM.match(line) and LIST_ITEM.match(prev or ""):
            findings.append(
                f"line {i+1}: {s[:48]!r} follows a list item with no blank line, so it renders "
                f"as part of that list. If it is not a list item, separate it with a blank "
                f"line and give it its own ALL-CAPS label.")

        # 3. Two consecutive URL-bearing lines that are not list items: they collapse into
        #    one paragraph. This is what flattened the asset kit.
        if (s and nxt and URL_LINE.search(s) and URL_LINE.search(nxt)
                and not LIST_ITEM.match(line) and not LIST_ITEM.match(nxt)):
            findings.append(
                f"line {i+1}: two link lines in a row with no blank line and no bullet. They "
                f"collapse onto one line - this is what flattened THE ASSET KIT. Make each a "
                f"'- ' bullet.")

    return findings


def _selftest() -> bool:
    passed = True

    def check(label, cond):
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and bool(cond)

    # The three real 2026-09-20 defects, verbatim in shape.
    eaten_label = "- A physical placement beats a post nobody saw\n\nCraft\n- Looks finished\n"
    check("catches a label glued to the list under it",
          any("sits directly above a list" in f for f in check_text(eaten_label)))

    absorbed = ("1. Use the brand kit.\n2. Post it publicly.\n"
                "Tagging @bettercallzaal helps and is not required today.\n")
    check("catches prose absorbed into the list above it",
          any("renders as part of that list" in f for f in check_text(absorbed)))

    flat_links = ("Everything in one download: https://zaostock.com/brand/kit.zip\n"
                  "The brand page: https://zaostock.com/brand\n")
    check("catches two link lines that collapse into one",
          any("collapse onto one line" in f for f in check_text(flat_links)))

    # The fixed shapes must pass, or the guard just bans the correct answer too.
    fixed_label = "- A physical placement beats a post\n\n\nCRAFT\n\n- Looks finished\n"
    check("passes the fixed label shape", check_text(fixed_label) == [])

    fixed_absorbed = ("1. Use the brand kit.\n2. Post it publicly.\n\n\nOPTIONAL\n\n"
                      "Tagging @bettercallzaal helps.\n")
    check("passes the fixed optional-note shape", check_text(fixed_absorbed) == [])

    fixed_links = ("- Everything in one download: https://zaostock.com/brand/kit.zip\n"
                   "- The brand page: https://zaostock.com/brand\n")
    check("passes links as bullets", check_text(fixed_links) == [])

    # Things that must NOT trip it, or nobody will keep it on.
    check("ordinary prose paragraphs are fine",
          check_text("A poster, a clip, a meme - whatever you want.\n\nZAOstock is free.\n") == [])
    check("one link line alone is fine",
          check_text("The festival: https://zaostock.com\n") == [])
    check("a sentence under a heading is fine",
          check_text("THE REWARD\n\nWinner takes the whole pot.\n") == [])

    # The operator header above the sentinels is not the cast text.
    framed = f"Notes: see https://a.example\nand https://b.example\n{PASTE_START}\nClean.\n{PASTE_END}\n"
    check("reads only the paste body", check_text(paste_body(framed)) == [])
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", help="a description.md")
    ap.add_argument("--all", action="store_true",
                    help="every description under rounds/daily/ - the live run")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        print("check-render-safe selftest")
        ok = _selftest()
        print("selftest:", "passed" if ok else "FAILED")
        return 0 if ok else 1

    if args.all:
        targets = sorted((REPO_ROOT / "rounds" / "daily").rglob("description.md"))
        if not targets:
            print("Refusing: matched no descriptions under rounds/daily/. The layout changed "
                  "or the glob is wrong. An empty set is not a pass.")
            return 1
    elif args.path:
        p = Path(args.path)
        targets = [p if p.is_absolute() else REPO_ROOT / p]
    else:
        ap.error("give a description path, or --all, or --selftest")

    bad = 0
    for t in targets:
        if not t.exists():
            print(f"FAIL {t}: not found")
            bad += 1
            continue
        findings = check_text(paste_body(t.read_text()))
        rel = t.relative_to(REPO_ROOT) if t.is_relative_to(REPO_ROOT) else t
        if findings:
            bad += 1
            print(f"\nFAIL {rel}")
            for f in findings:
                print(f"  {f}")
        else:
            print(f"ok   {rel}")

    print(f"\nChecked {len(targets)} description(s), {bad} with render hazards.")
    print("This checks three known shapes, not the whole renderer. READ THE PREVIEW TAB "
          "BEFORE CASTING - the description is immutable.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
