#!/usr/bin/env python3
"""Resolve a GitHub target before any count or SHA is reported from it.

WHY THIS EXISTS. On 2026-09-27 this lane reported "zero open PRs" from
`repos/bettercallzaal/zpoidh/pulls?state=open`. The repo is
`bettercallzaal/poidhz`; `zpoidh` is only the local directory name. The lane
then fed the filter a control - `state=all` on the same wrong repo - which
returned 5, and read that as proof the query worked.

It was proof the endpoint answers. `bettercallzaal/zpoidh` is a real repo with
real pull requests, so a non-empty control is exactly what a working query
against the wrong object looks like. The conclusion happened to hold, which is
worse than if it had broken: a control that cannot fail teaches you to trust
the next one.

The same day, a SHA guard reported `f70836f3` as a commit that "does not
resolve anywhere" after searching ~90 local checkouts and two of this org's
repos. It resolves - it is the head of a pull request in ZAODEVZ/ZAOstock, the
repo the message was entirely about, and the one place the search never looked.

Both failures are one shape: the instrument was fine and the target was never
established. So this script never lets a number or a SHA be printed without the
repo it came from, and it refuses rather than guesses.

EXIT CODES follow the house rule: 0 the claim holds, 1 it fails, 2 the check
could not run - which is the value that stops a typo'd repo becoming a clean
bill of health.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG = REPO_ROOT / "org.config.json"

# owner/name, GitHub's own rules: owner and name are [A-Za-z0-9._-], name may
# not be "." or "..". Deliberately strict - a slug that fails this is a typo or
# a sentence fragment, and "mobile/reduced-motion" being scanned out of prose as
# a repo to check is what made the SHA guard's search set untrustworthy.
SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*$")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


class CannotRun(Exception):
    """The check could not be performed. Never reported as a passing result."""


def load_config(path=None):
    p = Path(path) if path else CONFIG
    if not p.exists():
        raise CannotRun(f"{p} is missing, so no repo target is declared anywhere")
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        raise CannotRun(f"{p} is not valid json: {e}")


def parse_origin(url):
    """Pull owner/name out of an origin URL. None when it is not a GitHub remote."""
    if not url:
        return None
    url = url.strip()
    m = re.search(r"github\.com[:/]+([A-Za-z0-9][A-Za-z0-9._-]*)/([A-Za-z0-9][A-Za-z0-9._-]*?)(?:\.git)?/?$", url)
    if not m:
        return None
    return f"{m.group(1)}/{m.group(2)}"


def git_origin(cwd=None):
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd or REPO_ROOT), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as e:
        raise CannotRun(f"could not run git: {e}")
    if out.returncode != 0:
        raise CannotRun(f"git remote get-url origin failed: {out.stderr.strip() or 'no stderr'}")
    slug = parse_origin(out.stdout)
    if not slug:
        raise CannotRun(f"origin is not a github remote: {out.stdout.strip()!r}")
    return slug


def resolve_self(config, origin):
    """The repo this checkout pushes to, cross-checked against the declared one.

    Disagreement is a refusal, not a preference. If the config and the remote
    name different repos, every count taken today is ambiguous and the right
    answer is to stop, not to pick the more plausible one.
    """
    declared = config.get("self_repo")
    if not declared:
        raise CannotRun("org.config.json declares no self_repo, so nothing cross-checks the remote")
    if not SLUG_RE.match(declared):
        raise CannotRun(f"self_repo {declared!r} is not an owner/name slug")
    if declared != origin:
        raise CannotRun(
            f"self_repo says {declared} and git origin says {origin}. "
            "Two different repos, so no count from either is reportable until this is settled."
        )
    return declared


def resolve_entry(config):
    declared = config.get("entry_repo")
    if not declared:
        raise CannotRun("org.config.json declares no entry_repo")
    if not SLUG_RE.match(declared):
        raise CannotRun(f"entry_repo {declared!r} is not an owner/name slug")
    return declared


def gh_json(path, args=None):
    cmd = ["gh", "api", path] + list(args or [])
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except FileNotFoundError:
        raise CannotRun("gh is not installed, so no remote target can be confirmed")
    except subprocess.SubprocessError as e:
        raise CannotRun(f"gh api failed to run: {e}")
    if out.returncode != 0:
        raise CannotRun(f"gh api {path} failed: {(out.stderr or '').strip()[:300]}")
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError as e:
        raise CannotRun(f"gh api {path} returned unparseable json: {e}")


def open_prs(slug):
    """Open PR count, reported with the full_name GitHub itself echoes back.

    The count and its target come from the same pair of calls, so the number can
    never be copied out of a line that does not say what it counted.
    """
    meta = gh_json(f"repos/{slug}")
    echoed = meta.get("full_name")
    if not echoed:
        raise CannotRun(f"gh api repos/{slug} returned no full_name")
    if echoed.lower() != slug.lower():
        raise CannotRun(
            f"asked for {slug} and GitHub answered as {echoed} - a redirect or a rename. "
            "Report the number against the name GitHub gave, not the one you typed."
        )
    prs = gh_json(f"repos/{slug}/pulls?state=open&per_page=100")
    if not isinstance(prs, list):
        raise CannotRun(f"pulls for {slug} was not a list")
    return echoed, prs


def verify_sha(slug, sha):
    """Resolve a SHA in a NAMED repo and say which repo resolved it.

    A SHA on its own is not evidence. The guard that blocked a real commit had
    searched everywhere except the repo under discussion, and reported absence.
    """
    if not SHA_RE.match(sha):
        raise CannotRun(f"{sha!r} is not a hex sha of 7 to 40 characters")
    commit = gh_json(f"repos/{slug}/commits/{sha}")
    full = commit.get("sha")
    if not full:
        raise CannotRun(f"gh api repos/{slug}/commits/{sha} returned no sha")
    subject = ((commit.get("commit") or {}).get("message") or "").splitlines()
    return full, (subject[0] if subject else "")


def selftest():
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    # parse_origin
    ok("https origin parses", parse_origin("https://github.com/bettercallzaal/poidhz.git") == "bettercallzaal/poidhz")
    ok("https origin without .git parses", parse_origin("https://github.com/bettercallzaal/poidhz") == "bettercallzaal/poidhz")
    ok("ssh origin parses", parse_origin("git@github.com:ZAODEVZ/ZAOstock.git") == "ZAODEVZ/ZAOstock")
    ok("trailing slash parses", parse_origin("https://github.com/a/b/") == "a/b")
    ok("dots in name survive", parse_origin("https://github.com/o/my.repo.git") == "o/my.repo")
    ok("non-github remote is None", parse_origin("https://gitlab.com/a/b.git") is None)
    ok("empty origin is None", parse_origin("") is None)
    ok("None origin is None", parse_origin(None) is None)

    # THE BUG THIS SCRIPT EXISTS FOR: the local directory name is not the repo.
    ok("local dir name is not the remote name",
       parse_origin("https://github.com/bettercallzaal/poidhz.git") != "bettercallzaal/zpoidh")

    # SLUG_RE CANNOT reject the prose fragment the SHA guard mistook for a repo,
    # and pretending otherwise is how this test was first written - with an
    # `or True` on the end, so it passed while asserting something false.
    # "mobile/reduced-motion" is a well-formed owner/name slug. Shape is not
    # identity, so the defence is never the regex: it is that every target in
    # this script comes from org.config.json or git origin, and never from
    # scanning prose for things that look like repos.
    ok("a prose fragment can be shaped exactly like a slug, so shape proves nothing",
       SLUG_RE.match("mobile/reduced-motion") is not None)
    ok("a real slug matches", SLUG_RE.match("ZAODEVZ/ZAOstock") is not None)
    ok("bare word is not a slug", SLUG_RE.match("poidhz") is None)
    ok("three segments is not a slug", SLUG_RE.match("a/b/c") is None)
    ok("leading dot owner rejected", SLUG_RE.match(".a/b") is None)
    ok("empty name rejected", SLUG_RE.match("a/") is None)
    ok("space rejected", SLUG_RE.match("a b/c") is None)

    # SHA_RE
    ok("40 hex is a sha", SHA_RE.match("f70836f3e29fddaba302e1c09975b9e5ff27896f") is not None)
    ok("12 hex is a sha", SHA_RE.match("f70836f3e29f") is not None)
    ok("6 hex is too short", SHA_RE.match("f70836") is None)
    ok("uppercase hex rejected", SHA_RE.match("F70836F3E29F") is None)
    ok("non-hex rejected", SHA_RE.match("g70836f3e29f") is None)

    # resolve_self: the refusal is the feature.
    def raises(fn, needle):
        try:
            fn()
        except CannotRun as e:
            return needle in str(e)
        return False

    ok("missing self_repo refuses",
       raises(lambda: resolve_self({}, "a/b"), "no self_repo"))
    ok("mismatch between config and origin refuses",
       raises(lambda: resolve_self({"self_repo": "bettercallzaal/zpoidh"}, "bettercallzaal/poidhz"), "Two different repos"))
    ok("mismatch names BOTH repos so neither is silently preferred",
       raises(lambda: resolve_self({"self_repo": "x/y"}, "a/b"), "x/y") and
       raises(lambda: resolve_self({"self_repo": "x/y"}, "a/b"), "a/b"))
    ok("non-slug self_repo refuses",
       raises(lambda: resolve_self({"self_repo": "poidhz"}, "poidhz"), "not an owner/name slug"))
    ok("agreement resolves",
       resolve_self({"self_repo": "bettercallzaal/poidhz"}, "bettercallzaal/poidhz") == "bettercallzaal/poidhz")

    ok("missing entry_repo refuses", raises(lambda: resolve_entry({}), "no entry_repo"))
    ok("non-slug entry_repo refuses", raises(lambda: resolve_entry({"entry_repo": "ZAOstock"}), "not an owner/name slug"))
    ok("entry_repo resolves", resolve_entry({"entry_repo": "ZAODEVZ/ZAOstock"}) == "ZAODEVZ/ZAOstock")

    # The live config must actually carry both keys, or this whole script is
    # decoration. Read from disk, not from a literal.
    try:
        cfg = load_config()
        ok("live org.config.json declares self_repo", SLUG_RE.match(cfg.get("self_repo") or ""))
        ok("live org.config.json declares entry_repo", SLUG_RE.match(cfg.get("entry_repo") or ""))
        ok("live self_repo matches git origin", (cfg.get("self_repo") or "") == git_origin())
    except CannotRun as e:
        ok(f"live config readable ({e})", False)

    ok("missing config file refuses",
       raises(lambda: load_config("/nonexistent/org.config.json"), "is missing"))

    width = max(len(n) for n, _ in checks)
    for name, passed in checks:
        print(f"  {'ok  ' if passed else 'FAIL'} {name.ljust(width)}")
    failed = [n for n, p in checks if not p]
    print(f"selftest: {len(checks) - len(failed)}/{len(checks)} passed")
    return 0 if not failed else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--which", choices=["self", "entry"], help="print the resolved repo and stop")
    ap.add_argument("--open-prs", choices=["self", "entry"], help="open PR count, printed with the repo GitHub echoed")
    ap.add_argument("--verify-sha", metavar="SHA", help="resolve a sha in a named repo and say which repo resolved it")
    ap.add_argument("--repo", metavar="OWNER/NAME", help="explicit target for --verify-sha; defaults to entry_repo")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    try:
        config = load_config()

        def target(which):
            return resolve_self(config, git_origin()) if which == "self" else resolve_entry(config)

        if args.which:
            print(target(args.which))
            return 0

        if args.open_prs:
            slug = target(args.open_prs)
            echoed, prs = open_prs(slug)
            print(f"{echoed}: {len(prs)} open pull request(s)")
            for pr in prs:
                print(f"  #{pr['number']} {pr['user']['login']} {pr['title'][:62]}")
            return 0

        if args.verify_sha:
            slug = args.repo or resolve_entry(config)
            if not SLUG_RE.match(slug):
                raise CannotRun(f"--repo {slug!r} is not an owner/name slug")
            full, subject = verify_sha(slug, args.verify_sha)
            print(f"{args.verify_sha} RESOLVES in {slug} as {full[:12]}: {subject[:70]}")
            return 0

        ap.print_help()
        return 0
    except CannotRun as e:
        print(f"CANNOT RUN: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
