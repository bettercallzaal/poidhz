#!/usr/bin/env python3
"""
Stage 3: Validate a POIDH bounty description against the canonical bar.

Checks that a bounty description meets all required sections and criteria
per docs/bounty-best-practices.html before a round runs.

    python3 scripts/validate-bounty-description.py --description path/to/description.md [--strict]

Outputs:
    Returns 0 on PASS, 1 on FAIL
    Prints detailed feedback for each criterion

Human gate: This is a validation stage. It does not modify the description,
only checks it against the canonical bar and reports findings.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


REQUIRED_SECTIONS = [
    ("why", "WHY - one-paragraph link to source episode/event/page"),
    ("the_bar", "THE BAR - 3-5 numbered floor rules"),
    ("the_rubric", "THE RUBRIC - grouped by Distribution/Craft/Substance/Bonus"),
    ("asset_kit", "THE ASSET KIT - link to GitHub brand folder + direct download URLs"),
    ("reward", "THE REWARD - prize + winner-cast distribution + EB ZABAL trail"),
    ("deadline", "DEADLINE - exact PT date/time + winner cast date"),
]

# THE HEADING IS NOT THE SECTION. Measured 2026-09-22 against the description that
# ACTUALLY CAST as bounty two on 2026-09-21: this validator returned three FAILs -
# THE RUBRIC, THE ASSET KIT and DEADLINE - on copy that ran, drew eleven entries over
# two rounds, and carried every one of those things. It was matching literal headers
# that the tightened rewrite had renamed:
#
#     THE RUBRIC     -> WHAT EARNS WEIGHT
#     THE ASSET KIT  -> THE KIT
#     DEADLINE       -> no header at all; the close moved into the opening sentence
#
# A poidh description is IMMUTABLE once cast, so a validator that cries wolf on good
# copy is worse than one that stays quiet: the one time it is right, it has already
# taught its reader to cast anyway. This file's own comment block says a header match
# alone is not evidence. The same reasoning runs the other way, and did not.
#
# So each section now carries the headers it has actually been written under, and a
# section whose content can be proved without any header at all says so rather than
# failing. Add a synonym here when the copy is renamed again; do not delete the check.
SECTION_ALIASES = {
    "why": ["WHY"],
    "the_bar": ["THE BAR"],
    "the_rubric": ["THE RUBRIC", "WHAT EARNS WEIGHT", "WHAT SCORES"],
    "asset_kit": ["THE ASSET KIT", "THE KIT"],
    "reward": ["THE REWARD"],
    "deadline": ["DEADLINE", "CLOSES", "CLOSING"],
}

# A section that can be established from the whole description, header or not. The
# deadline is the only one today: the tightened copy states the close in its first
# sentence and never writes the word. The pattern must be specific enough that prose
# cannot satisfy it by accident - a weekday and a clock time, or a month and a day.
HEADERLESS_EVIDENCE = {
    "deadline": (
        r"(?i)\bcloses?\b[^.\n]{0,80}?"
        r"(\b\d{1,2}\s*(?::\d{2})?\s*(?:am|pm)\b|\b(?:january|february|march|april|may|june|"
        r"july|august|september|october|november|december)\s+\d{1,2}\b)",
        "a stated closing time or date in the body, with no DEADLINE header",
    ),
}

# A CODE ROUND IS A DIFFERENT SHAPE AND THE SKELETON ABOVE IS A MEDIA ROUND'S.
#
# Every round until 2026-09-25 asked for a piece of media, so the required sections encode
# that: a brand kit to build from, a rubric about craft and distribution. Round five asks for
# a PULL REQUEST against ZAODEVZ/ZAOstock. Run against it, this validator demanded THE ASSET
# KIT - a brand-kit download link - on a bounty about TypeScript, and demanded a rubric
# grouped by Distribution and Craft for work that is judged by whether CI passes.
#
# The wrong fix is to bolt a brand-kit section onto a code bounty so the checker goes quiet.
# That is how a validator starts shaping the work instead of checking it. A code round has
# its own equally strict skeleton, and the thing that plays the asset kit's part is THE REPO:
# the one link without which nobody can start.
#
# Pass --kind=code to use it. The default is unchanged, so every existing round validates
# exactly as before.
CODE_REQUIRED_SECTIONS = [
    ("why", "WHY - what this round is for and who it is aimed at"),
    ("the_repo", "THE REPO - the repository link, without which nobody can start"),
    ("what_counts", "WHAT COUNTS - what makes an entry complete, numbered"),
    ("reward", "THE REWARD - prize + EB ZABAL trail"),
    ("deadline", "DEADLINE - exact date/time"),
]

CODE_SECTION_ALIASES = {
    "why": ["WHY", "THIS ONE IS WRITTEN FOR", "WHY THIS ROUND"],
    "the_repo": ["THE REPO", "THE REPOSITORY", "THE CODEBASE"],
    "what_counts": ["WHAT COUNTS", "THE BAR", "WHAT I AM LOOKING FOR"],
    "reward": ["THE REWARD"],
    "deadline": ["DEADLINE", "CLOSES", "CLOSING"],
}

REQUIRED_FLOOR_RULES = [
    ("tag_bcz", "Tag @bettercallzaal on X"),
    ("crosspost_fc", "Cross-post in relevant Farcaster channel"),
    ("submit_url", "Submit X URL on POIDH bounty page"),
    ("audio_rule", "AUDIO rule: official promo MP3 or source-episode audio or clear instrumental"),
]


def load_description(path: Path) -> str | None:
    """Load bounty description from file."""
    if not path.exists():
        print(f"ERROR: Description file not found: {path}")
        return None

    try:
        with open(path) as f:
            text = f.read()
    except Exception as e:
        print(f"ERROR reading description: {e}")
        return None

    return paste_body(text)


PASTE_START = "<!-- PASTE BELOW THIS LINE -->"
PASTE_END = "<!-- PASTE ABOVE THIS LINE -->"


def paste_body(text: str) -> str:
    """The text that actually gets cast, when the file marks it; the whole file otherwise.

    These files carry an operator header above the paste sentinels - the ETH price and when
    it was measured, why the close time is what it is, which links are redirects. That header
    is for us and never reaches the chain. Validating it alongside the body made the new
    prize-figure rule fail `rounds/daily/d01/description.md` for a figure in the header that
    no submitter will ever see, and a rule that fires on the wrong surface is a rule someone
    turns off. Read the body, and say so in the run output so nobody wonders which was read.
    """
    if PASTE_START in text and PASTE_END in text:
        return text.split(PASTE_START, 1)[1].split(PASTE_END, 1)[0].strip() + "\n"
    return text


# What each section must CONTAIN, not merely be titled. Until 2026-09-08 this file matched
# section header names and read nothing inside them, so a REWARD section could pass while
# promising something the round did not offer - which is exactly what happened: the
# winner-announce template promised every submitter a $ZABAL airdrop for R5, a round with no
# $ZABAL trail at all, and the validator was green throughout.
#
# Each entry is (regex the section body must match, what it is checking for).
SECTION_MUST_CONTAIN = {
    "the_bar": (r"(?im)^\s*(\d+[.)]|[-+*])\s+\S", "at least one numbered or bulleted floor rule"),
    # THIS RULE USED TO DEMAND THE OPPOSITE, AND IT WAS WRONG. It required
    # r"\b\d+(\.\d+)?\s*(ETH|USDC|DEGEN|SOL)\b" - "a concrete prize amount with its token" -
    # so a description that correctly left the pot out would FAIL the validator, and the
    # validator would push the number back in. Kenny, 2026-09-20: do not put the amount in
    # the description. On an OPEN bounty the pot grows the moment anyone contributes, and a
    # poidh description is immutable, so a number written here is wrong forever. The REWARD
    # section must still SAY something - that is what the header-match-alone failure below
    # was about - so it now has to point at the live pot instead of naming a figure.
    "reward": (r"(?i)\b(pot|winner takes|this page)\b",
               "a pointer to the live pot (the amount belongs in the form's reward field, not here)"),
    "deadline": (r"(?i)(20\d{2}|\b\d{1,2}\s*(am|pm)\b)", "an actual date or time, not just the word DEADLINE"),
    "asset_kit": (r"https?://\S+", "at least one usable link"),
}


def _section_body(description: str, header: str) -> str | None:
    """Text from a section header to the next ALL-CAPS header or end."""
    m = re.search(r"(?im)^[^\S\n]*" + re.escape(header) + r"\b.*$", description)
    if not m:
        return None
    rest = description[m.end():]
    nxt = re.search(r"(?m)^[A-Z][A-Z \-']{6,}$", rest)
    return rest[:nxt.start()] if nxt else rest


def validate_sections(description: str, kind: str = "media") -> tuple[bool, list]:
    """Check each required section is present AND says something.

    A header match alone is not evidence. See SECTION_MUST_CONTAIN above for why.

    `kind` selects the skeleton. "media" is every round through four and is the default, so
    nothing that validated before changes. "code" is a round that asks for a pull request,
    where a brand-kit link is meaningless and THE REPO is the section nobody can start
    without."""
    required = CODE_REQUIRED_SECTIONS if kind == "code" else REQUIRED_SECTIONS
    alias_map = CODE_SECTION_ALIASES if kind == "code" else SECTION_ALIASES
    findings = []
    all_pass = True

    for section_id, section_label in required:
        canonical = section_label.split(" - ")[0]
        aliases = alias_map.get(section_id, [canonical])

        header = None
        for alias in aliases:
            # ANCHORED TO A LINE START, and that is load-bearing. An unanchored
            # case-insensitive match for a short alias like THE KIT also matches the
            # words "the kit" in a sentence, so the section passes when it has been
            # deleted. Measured 2026-09-22: with the whole kit section cut, an
            # unanchored matcher still reported PASS.
            patterns = [
                r"(?im)^[^\S\n]*" + re.escape(alias) + r"\b",
                r"(?im)^[^\S\n]*#+\s*" + re.escape(alias.replace("THE ", "").replace("_", " ")) + r"\b",
                r"(?im)^[^\S\n]*\*\*" + re.escape(alias) + r"\b",
            ]
            if any(re.search(p, description) for p in patterns):
                header = alias
                break

        if header is None:
            # No header under any name it has been written under. Before failing, ask
            # whether the thing itself is in the copy: a renamed or absent header is a
            # style change, a missing close date is a real defect, and they are not the
            # same finding.
            evidence = HEADERLESS_EVIDENCE.get(section_id)
            if evidence and re.search(evidence[0], description):
                findings.append(f"PASS: {section_label} - {evidence[1]}")
                continue
            findings.append(
                f"FAIL: {section_label} - NOT FOUND under any of: {', '.join(aliases)}"
            )
            all_pass = False
            continue

        rule = SECTION_MUST_CONTAIN.get(section_id)
        if not rule:
            findings.append(f"PASS: {section_label}")
            continue

        pat, what = rule
        body = _section_body(description, header)
        if body is None:
            findings.append(f"PASS: {section_label}")
        elif re.search(pat, body):
            findings.append(f"PASS: {section_label}")
        else:
            findings.append(f"FAIL: {section_label} - header present but the section has no {what}")
            all_pass = False

    return all_pass, findings


def validate_floor_rules(description: str) -> tuple[bool, list]:
    """Check that all required floor rules are mentioned."""
    findings = []
    all_pass = True

    for rule_id, rule_label in REQUIRED_FLOOR_RULES:
        # Look for key phrases from each rule
        keywords = {
            "tag_bcz": ["@bettercallzaal", "tag"],
            "crosspost_fc": ["farcaster", "cross-post", "channel"],
            "submit_url": ["submit", "url", "poidh", "bounty page"],
            "audio_rule": ["audio", "music", "dialog", "instrumental"],
        }

        kw_list = keywords.get(rule_id, [rule_label.lower()])
        found = any(re.search(r"(?i)" + re.escape(kw), description) for kw in kw_list)

        if found:
            findings.append(f"PASS: Floor rule - {rule_label}")
        else:
            findings.append(f"WARN: Floor rule - {rule_label} not explicitly mentioned (verify manually)")
            # Not a hard fail for floor rules since wording varies

    return all_pass, findings


# A prize figure, in any of the shapes this repo has actually written one in. Anchored on
# the NUMBER so a bare mention of "ETH on Base" or "the pot" is untouched.
PRIZE_FIGURE = re.compile(
    r"(?ix)"
    r"( \b\d+(?:\.\d+)? \s* (?:ETH|USDC|DEGEN|SOL)\b"      # 0.0094 ETH
    r"| \$\s?\d+(?:\.\d+)?"                                 # $25
    r"| \b\d+(?:\.\d+)? \s+ dollars?\b )"                   # 25 dollars
)


LICENCE_CLAIM = re.compile(r"(?i)\bCC[- ]?BY\b|\bcreative commons\b|\bpublic domain\b|\bCC0\b")


def validate_no_licence_claim(description: str) -> tuple[bool, list]:
    """Refuse a licence claim about the brand kit in cast text.

    MEASURED 2026-09-21. Bounty one's immutable description says the ZAOstock kit is "CC-BY,
    there is nothing to ask permission for". Nothing licenses it that way: not
    zaostock.com/brand, not /design, and the kit zip contains no licence file at all. The line
    came from this repo's May scaffold, written for BCZ's own kits, and was copied in
    unchecked. One entrant has already repeated "the CC-BY brand kit" in their own public
    description. It was then copied AGAIN into bounty two's draft and the daily template, and
    was minutes from being cast a second time.

    A licence is a legal claim about someone else's work - attabotty's and Candy's. Inviting
    people to use the kit for their entry is ours to give; a licence is not. If a real notice
    ever goes on the brand page, delete this check in the same commit that cites it."""
    hits = [m.group(0) for m in LICENCE_CLAIM.finditer(description)]
    if not hits:
        return True, ["PASS: no licence claim about the kit"]
    return False, [f"FAIL: {h!r} is a licence claim. Nothing on zaostock.com or in the kit "
                   f"licenses it. Say 'use any of this for your entry' - permission is ours to "
                   f"give, a licence is not." for h in hits]


def validate_no_prize_amount(description: str, allow: bool = False) -> tuple[bool, list]:
    """Refuse a prize figure written into the description body.

    WHY THIS IS A HARD CHECK AND NOT A NOTE IN A README. Kenny, 2026-09-20: do not put the
    amount in the description. An OPEN bounty's pot grows the moment anyone contributes, so
    the figure is wrong from the first contribution onward - and a poidh description is
    IMMUTABLE once cast, so it is wrong for the life of the bounty and cannot be corrected.
    The amount belongs in the form's reward field, which poidh renders live.

    This estate has measured honor-system rules at 3-40% compliance and enforced ones at
    ~100%, and the honor-system version of this rule had already lost once: the validator
    REQUIRED a prize amount until this change, so the correct description failed and the
    wrong one passed.

    `allow` is the documented way past it, for a FIXED bounty whose pot cannot move. A guard
    with no escape hatch gets deleted, which is how a guard stops guarding.
    """
    hits = [m.group(0).strip() for m in PRIZE_FIGURE.finditer(description)]
    if not hits:
        return True, ["PASS: no prize figure in the description (the pot lives in the form's reward field)"]
    if allow:
        return True, [f"WARN: prize figure {h!r} allowed by --allow-prize-amount (FIXED bounty only)"
                      for h in hits]
    return False, [f"FAIL: prize figure {h!r} is written into the description. On an OPEN "
                   f"bounty the pot grows and the description is immutable, so this is wrong "
                   f"forever. Put it in the form's reward field. (--allow-prize-amount for a "
                   f"FIXED bounty.)" for h in hits]


def validate_links(description: str) -> tuple[bool, list]:
    """Check for proper links and URLs."""
    findings = []

    # Check for at least one bounty URL
    has_poidh_url = re.search(r"https://poidh\.xyz/.*?bounty", description, re.IGNORECASE)
    if has_poidh_url:
        findings.append("PASS: POIDH bounty URL found")
    else:
        findings.append("WARN: No POIDH bounty URL found (will be added after creation)")

    # Check for brand kit link
    has_brand_kit = re.search(r"(github|brand|kit|assets)", description, re.IGNORECASE)
    if has_brand_kit:
        findings.append("PASS: Brand kit reference found")
    else:
        findings.append("WARN: No brand kit reference found")

    # Check for GitHub links
    has_github = re.search(r"https://github\.com", description)
    if has_github:
        findings.append("PASS: GitHub link found")
    else:
        findings.append("WARN: No GitHub link found for brand kit")

    return True, findings  # Links are not hard-fails


def validate_structure(description: str) -> tuple[bool, list]:
    """Check overall structure and completeness."""
    findings = []
    all_pass = True

    # Check for minimum length
    lines = description.strip().split("\n")
    if len(lines) >= 10:
        findings.append(f"PASS: Description has {len(lines)} lines (minimum 10)")
    else:
        findings.append(f"FAIL: Description too short ({len(lines)} lines, minimum 10)")
        all_pass = False

    # Check for numbered lists (floor rules and rubric often use these)
    has_numbered_lists = re.search(r"^\s*\d+\.", description, re.MULTILINE)
    if has_numbered_lists:
        findings.append("PASS: Numbered lists found (floor rules / rubric)")
    else:
        findings.append("WARN: No numbered lists found (check that floor rules are enumerated)")

    # Check for markdown headers
    has_headers = re.search(r"^#+\s", description, re.MULTILINE)
    if has_headers:
        findings.append("PASS: Markdown headers found")
    else:
        findings.append("WARN: No markdown headers found (consider using # for section structure)")

    return all_pass, findings


def _selftest() -> bool:
    """Offline. Every case here is a real failure this file used to pass."""
    passed = True

    def check(label: str, cond: bool) -> None:
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and cond

    # The case this was built for: a REWARD section that is a header and nothing else.
    empty_reward = "THE REWARD\n\nDetails to follow.\n\nDEADLINE\n\nCloses 2026-10-01.\n"
    _, f = validate_sections(empty_reward)
    check("fails a REWARD section that says nothing",
          any("THE REWARD" in x and x.startswith("FAIL") for x in f))

    live_reward = ("THE REWARD\n\nWinner takes the whole pot, and it grows as others "
                   "contribute.\n\nDEADLINE\n\nCloses 2026-10-01.\n")
    _, f = validate_sections(live_reward)
    check("passes a REWARD section that points at the live pot, naming no figure",
          any("THE REWARD" in x and x.startswith("PASS") for x in f))

    # Kenny, 2026-09-20. The rule above used to REQUIRE the figure these cases refuse.
    for figure in ("0.0094 ETH", "$25", "about 25 dollars", "0.025 ETH on Base"):
        ok, f = validate_no_prize_amount(f"THE REWARD\n\nBest one wins {figure}.\n")
        check(f"refuses {figure!r} in the description", not ok and f[0].startswith("FAIL"))

    ok, f = validate_no_prize_amount(
        "THE REWARD\n\nWinner takes the whole pot. Read the number at the top of this page.\n")
    check("passes a description with no figure at all", ok and f[0].startswith("PASS"))

    # A bare mention of the chain or the pot is not a figure, and must not be caught.
    ok, _ = validate_no_prize_amount("Paid in ETH on Base. The pot grows. Closes 4:00pm Eastern.\n")
    check("does not fire on 'ETH on Base', 'the pot', or a clock time", ok)
    ok, _ = validate_no_prize_amount(
        "Track it: https://www.empirebuilder.world/empire/0xbb48f19b0494ff7c1fe5dc2032aeee14312f0b07\n"
        "ZAOstock is Saturday October 3, 2026, noon to six.\n")
    check("does not fire on a contract address or a date", ok)

    # 2026-09-21: the kit is not CC-BY, and the claim was about to be cast a second time.
    for phrase in ("use any of this, CC-BY", "the CC BY brand kit", "Creative Commons licensed"):
        ok, f = validate_no_licence_claim(f"THE ASSET KIT ({phrase})\n")
        check(f"refuses the licence claim {phrase!r}", not ok and f[0].startswith("FAIL"))
    ok, _ = validate_no_licence_claim("THE ASSET KIT (use any of this for your entry)\nThe moose mark is by attabotty.\n")
    check("passes an invitation to use the kit, which is ours to give", ok)

    ok, f = validate_no_prize_amount("Best one wins 0.025 ETH.\n", allow=True)
    check("--allow-prize-amount lets a FIXED bounty through, as a WARN",
          ok and f[0].startswith("WARN"))

    bar_no_rules = "THE BAR\n\nDo good work.\n"
    _, f = validate_sections(bar_no_rules)
    check("fails a BAR with no numbered or bulleted rules",
          any("THE BAR" in x and x.startswith("FAIL") for x in f))

    bar_rules = "THE BAR\n\n1. Sixty seconds max.\n2. Captions burned in.\n"
    _, f = validate_sections(bar_rules)
    check("passes a BAR that has floor rules",
          any("THE BAR" in x and x.startswith("PASS") for x in f))

    kit_no_link = "THE ASSET KIT\n\nAsk us for the files.\n"
    _, f = validate_sections(kit_no_link)
    check("fails an ASSET KIT with no link",
          any("ASSET KIT" in x and x.startswith("FAIL") for x in f))

    no_deadline_date = "DEADLINE\n\nCloses soon.\n"
    _, f = validate_sections(no_deadline_date)
    check("fails a DEADLINE with no date or time",
          any("DEADLINE" in x and x.startswith("FAIL") for x in f))

    check("a missing section still fails outright",
          any(x.startswith("FAIL") for x in validate_sections("nothing here at all")[1]))

    # THE CODE SKELETON. Round five asks for a pull request, so a brand-kit link is
    # meaningless and THE REPO is the section nobody can start without. The controls run both
    # ways on purpose: a flag that never changes an outcome is decoration.
    code_round = (
        "SHIP CODE, NOT A POSTER. Closes 5:00pm Eastern, Sunday October 4.\n\n"
        "THIS ONE IS WRITTEN FOR AGENTS\n\nBecause an agent that can read a codebase is "
        "doing the thing this programme wants to pay for.\n\n"
        "THE REPO\n\nhttps://github.com/ZAODEVZ/ZAOstock\n\n"
        "WHAT COUNTS\n\n1. It visibly changes something.\n2. It passes CI.\n"
        "3. It explains itself.\n\n"
        "THE REWARD\n\nWinner takes the whole pot. Every submitter is added to the POIDH "
        "Submitters leaderboard on Empire Builder for $ZABAL: "
        "https://www.empirebuilder.world/empire/0xbB48f19B0494Ff7C1fE5Dc2032aeEE14312f0b07\n")
    ok_code, f_code = validate_sections(code_round, "code")
    check("a code round PASSES the code skeleton",
          ok_code or not [x for x in f_code if x.startswith("FAIL")])
    _, f_as_media = validate_sections(code_round, "media")
    check("the SAME code round FAILS the media skeleton, so the flag really switches",
          any("ASSET KIT" in x for x in f_as_media if x.startswith("FAIL")))
    media_round = ("WHY\n\nBecause.\n\nTHE KIT\n\nhttps://zaostock.com/brand\n\n"
                   "THE BAR\n\n1. One.\n2. Two.\n3. Three.\n")
    _, f_media_as_code = validate_sections(media_round, "code")
    check("a media round FAILS the code skeleton for want of THE REPO",
          any("THE REPO" in x for x in f_media_as_code if x.startswith("FAIL")))

    # The operator header above the sentinels is not the cast text and must not be validated.
    framed = (f"**Prize: 0.0094 ETH, about $25** at ETH $2,657.49, measured 2026-09-20.\n"
              f"{PASTE_START}\nWinner takes the whole pot.\n{PASTE_END}\n")
    body = paste_body(framed)
    check("reads only the paste body when the file is framed",
          body.strip() == "Winner takes the whole pot.")
    check("the header's figure does NOT trip the prize rule",
          validate_no_prize_amount(body)[0])
    check("the same figure INSIDE the body still does trip it",
          not validate_no_prize_amount(paste_body(
              f"{PASTE_START}\nBest one wins 0.0094 ETH.\n{PASTE_END}\n"))[0])
    check("an unframed file is read whole, not silently emptied",
          paste_body("no sentinels here") == "no sentinels here")
    return passed


def main() -> int:
    p = argparse.ArgumentParser(
        description="Stage 3: Validate POIDH bounty description against canonical bar"
    )
    p.add_argument(
        "--description",
        type=Path,
        help="Path to bounty description markdown file (required unless --selftest)",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Strict mode: warnings become failures",
    )

    p.add_argument("--kind", choices=("media", "code"), default="media",
                   help="which skeleton to require: a media round (default) or a round that "
                        "asks for a pull request")
    p.add_argument("--allow-prize-amount", action="store_true",
                   help="permit a prize figure in the description. FIXED bounties only - an "
                        "OPEN bounty's pot grows and the description is immutable")
    p.add_argument("--selftest", action="store_true",
                   help="offline checks of the section-content rules")
    args = p.parse_args()

    if args.selftest:
        print("validate-bounty-description selftest")
        good = _selftest()
        print("selftest:", "passed" if good else "FAILED")
        return 0 if good else 1

    if args.description is None:
        p.error("--description is required (or use --selftest)")

    # Load description
    print(f"Validating description: {args.description}")
    description = load_description(args.description)
    if not description:
        return 1
    raw = args.description.read_text()
    print(f"Surface read: {'the paste body between the sentinels' if PASTE_START in raw else 'the WHOLE FILE (no paste sentinels found)'}"
          f" - {len(description)} of {len(raw)} chars")

    print("\n--- SECTION VALIDATION ---")
    sections_pass, sections_findings = validate_sections(description, args.kind)
    for finding in sections_findings:
        print(f"  {finding}")

    print("\n--- PRIZE FIGURE (must NOT be in the description) ---")
    prize_pass, prize_findings = validate_no_prize_amount(description, args.allow_prize_amount)
    for finding in prize_findings:
        print(f"  {finding}")

    print("\n--- LICENCE CLAIM (must NOT be in the description) ---")
    lic_pass, lic_findings = validate_no_licence_claim(description)
    for finding in lic_findings:
        print(f"  {finding}")

    print("\n--- FLOOR RULES VALIDATION ---")
    floor_pass, floor_findings = validate_floor_rules(description)
    for finding in floor_findings:
        print(f"  {finding}")

    print("\n--- LINKS & URLS ---")
    links_pass, links_findings = validate_links(description)
    for finding in links_findings:
        print(f"  {finding}")

    print("\n--- OVERALL STRUCTURE ---")
    struct_pass, struct_findings = validate_structure(description)
    for finding in struct_findings:
        print(f"  {finding}")

    # Final verdict. floor_pass/links_pass are always True by construction (those
    # validators only ever emit WARN, never FAIL) - so --strict's documented promise
    # ("warnings become failures") has to be enforced here, from the actual finding
    # text, not from those functions' return values.
    all_pass = sections_pass and struct_pass and prize_pass and lic_pass
    all_findings = (sections_findings + prize_findings + lic_findings + floor_findings
                    + links_findings + struct_findings)
    if args.strict:
        all_pass = all_pass and not any(f.startswith("WARN:") for f in all_findings)

    print("\n" + "=" * 60)
    if all_pass:
        print("VERDICT: PASS - Description is ready for casting")
        print("\nHuman gate check:")
        print("- Review the description one more time in the POIDH UI")
        print("- Confirm all links work and point to correct resources")
        print("- Verify floor rules are clear to submitters")
        print("- Check the deadline is correct - the description is immutable once cast")
        print("- Set the prize in the form's REWARD field, not in the description text")
        return 0
    else:
        print("VERDICT: FAIL - Description needs revision")
        print("\nFix the items marked FAIL before casting.")
        if not args.strict:
            print("(Run with --strict to treat warnings as failures)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
