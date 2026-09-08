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
            return f.read()
    except Exception as e:
        print(f"ERROR reading description: {e}")
        return None


# What each section must CONTAIN, not merely be titled. Until 2026-09-08 this file matched
# section header names and read nothing inside them, so a REWARD section could pass while
# promising something the round did not offer - which is exactly what happened: the
# winner-announce template promised every submitter a $ZABAL airdrop for R5, a round with no
# $ZABAL trail at all, and the validator was green throughout.
#
# Each entry is (regex the section body must match, what it is checking for).
SECTION_MUST_CONTAIN = {
    "the_bar": (r"(?im)^\s*(\d+[.)]|[-+*])\s+\S", "at least one numbered or bulleted floor rule"),
    "reward": (r"(?i)\b\d+(\.\d+)?\s*(ETH|USDC|DEGEN|SOL)\b", "a concrete prize amount with its token"),
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


def validate_sections(description: str) -> tuple[bool, list]:
    """Check each required section is present AND says something.

    A header match alone is not evidence. See SECTION_MUST_CONTAIN above for why."""
    findings = []
    all_pass = True

    for section_id, section_label in REQUIRED_SECTIONS:
        header = section_label.split(" - ")[0]
        patterns = [
            r"(?i)" + re.escape(header),
            r"(?i)#+\s*" + re.escape(header.replace("THE ", "").replace("_", " ")),
        ]
        found = any(re.search(p, description) for p in patterns)

        if not found:
            findings.append(f"FAIL: {section_label} - NOT FOUND")
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
    check("fails a REWARD section with no prize amount",
          any("THE REWARD" in x and x.startswith("FAIL") for x in f))

    real_reward = "THE REWARD\n\nBest one wins 0.025 ETH on Base.\n\nDEADLINE\n\nCloses 2026-10-01.\n"
    _, f = validate_sections(real_reward)
    check("passes a REWARD section that names the prize",
          any("THE REWARD" in x and x.startswith("PASS") for x in f))

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

    print("\n--- SECTION VALIDATION ---")
    sections_pass, sections_findings = validate_sections(description)
    for finding in sections_findings:
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
    all_pass = sections_pass and struct_pass
    all_findings = sections_findings + floor_findings + links_findings + struct_findings
    if args.strict:
        all_pass = all_pass and not any(f.startswith("WARN:") for f in all_findings)

    print("\n" + "=" * 60)
    if all_pass:
        print("VERDICT: PASS - Description is ready for casting")
        print("\nHuman gate check:")
        print("- Review the description one more time in the POIDH UI")
        print("- Confirm all links work and point to correct resources")
        print("- Verify floor rules are clear to submitters")
        print("- Check that prize amount and deadline are correct")
        return 0
    else:
        print("VERDICT: FAIL - Description needs revision")
        print("\nFix the items marked FAIL before casting.")
        if not args.strict:
            print("(Run with --strict to treat warnings as failures)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
