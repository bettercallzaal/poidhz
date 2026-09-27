#!/usr/bin/env python3
"""Resolve a GitHub target before any count or SHA is reported from it.

WHY THIS EXISTS, and the first version of this paragraph had it wrong.

On 2026-09-27 this lane reported "zero open PRs" from
`repos/bettercallzaal/zpoidh/pulls?state=open`, noticed the repo is really
`bettercallzaal/poidhz`, and wrote that it had counted a different repo by
mistake. That explanation was never measured. `bettercallzaal/zpoidh` is
**this repo's former name**: `gh api repos/bettercallzaal/zpoidh` answers
`full_name: bettercallzaal/poidhz`, `id: 1255383001`, the same id as `poidhz`.
GitHub follows the rename redirect and serves the same repo. So the count of 0
was CORRECT, and the control's "5" was `per_page=5` truncating a list that
returns 100 at `per_page=100` on either name.

The real defect is worse than the one first written down. **A stale name
returns entirely correct data, and nothing in the response says the name is
stale.** There is no failing call to notice, no wrong number to catch, and no
control that can fail - the query works, against the right repo, under a name
nobody should still be using. The only thing that distinguishes it from a slug
that hit an unrelated repo is the numeric id, which is why this script carries
ids and not just names.

The same afternoon a SHA guard reported `f70836f3` as a commit that "does not
resolve anywhere", after searching ~90 local checkouts and two of this org's
repos and never `ZAODEVZ/ZAOstock` - the repo the message was entirely about.
It resolves. That one IS the shape first claimed here: the instrument was fine
and the target was never established.

So this script never lets a number or a SHA be printed without the repo it came
from, it carries numeric ids so a rename can be told from a wrong target, and it
refuses rather than guesses.

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


def declared_id(config, which):
    """The numeric id stored beside a slug, or None when it is absent.

    None is a degraded mode that says so, never a silent pass. A non-integer is
    a refusal: an id that is a string in the config is an id nobody can compare.
    """
    key = f"{which}_repo_id"
    if key not in config:
        return None
    raw = config[key]
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise CannotRun(f"{key} is {raw!r}, which is not an integer repo id")
    if raw <= 0:
        raise CannotRun(f"{key} is {raw}, which is not a positive repo id")
    return raw


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


def check_target(slug, expected_id, meta=None):
    """Confirm a slug still names the repo we mean, using its numeric id.

    THE NAME IS NOT THE IDENTITY, AND A RENAME PROVES IT FROM BOTH SIDES.
    `bettercallzaal/zpoidh` is this repo's former name. GitHub follows the
    rename redirect and serves the same repo, id 1255383001, so a stale slug
    returns entirely correct data and NOTHING in the response says the name is
    out of date. That is the failure this script was written for, and the first
    version of it described the cause wrongly - it assumed a second, unrelated
    repo. The id is what tells the two apart.

    Four outcomes, and only the first is a pass:

    1. name matches and id matches - the target is what we meant
    2. name matches and id does NOT - the slug now points at a DIFFERENT repo,
       because the old name was freed and retaken, or our stored id is stale.
       The most dangerous case: nothing in the name looks wrong.
    3. name differs and id matches - a rename. Exit 2 with both names and the
       one-line config fix, because a rename is a real event and a bare refusal
       on it is how a check gets bypassed.
    4. name differs and id does not - refuse plainly.
    """
    meta = meta if meta is not None else gh_json(f"repos/{slug}")
    echoed = meta.get("full_name")
    if not echoed:
        raise CannotRun(f"gh api repos/{slug} returned no full_name")
    actual_id = meta.get("id")
    same_name = echoed.lower() == slug.lower()

    if expected_id is None or actual_id is None:
        # Degraded, and it says so rather than implying the id agreed.
        why = "no id is declared in org.config.json" if expected_id is None else "GitHub returned no id"
        if not same_name:
            raise CannotRun(
                f"asked for {slug} and GitHub answered as {echoed}, and {why}, "
                "so a rename cannot be told from an unrelated repo. Settle it before reporting anything."
            )
        return echoed, actual_id, f"name matches; id unchecked because {why}"

    if same_name and actual_id == expected_id:
        return echoed, actual_id, "name and id both match"

    if same_name and actual_id != expected_id:
        raise CannotRun(
            f"{slug} still answers to that name but its id is {actual_id}, not the {expected_id} "
            "declared in org.config.json. Either the name was freed and taken by another repo, or "
            "the stored id is stale. Nothing in the name looks wrong, which is why this is checked."
        )

    if actual_id == expected_id:
        raise CannotRun(
            f"{slug} is a RENAME of the repo we mean: same id {actual_id}, now named {echoed}. "
            f"The redirect means every count taken through {slug} was correct and silently stale. "
            f"Fix: set the relevant *_repo in org.config.json to {echoed}."
        )

    raise CannotRun(
        f"asked for {slug}, GitHub answered as {echoed} with id {actual_id} against a declared "
        f"{expected_id}. Different name and different repo, so this is not a rename."
    )


def open_prs(slug, expected_id=None):
    """Open PR count, reported with the full_name GitHub itself echoes back.

    The count and its target come from the same calls, so the number can never
    be copied out of a line that does not say what it counted.
    """
    echoed, actual_id, note = check_target(slug, expected_id)
    prs = gh_json(f"repos/{slug}/pulls?state=open&per_page=100")
    if not isinstance(prs, list):
        raise CannotRun(f"pulls for {slug} was not a list")
    return echoed, prs, note


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
        """True only when fn refuses with CannotRun carrying `needle`.

        Any OTHER exception returns False rather than propagating. Before this,
        deleting the missing-self_repo guard made the whole suite die with a raw
        TypeError - no FAIL line, no summary, no count. A guard whose removal
        crashes the harness is not covered by the harness: it is covered by luck,
        and a crash and a clean run are told apart by a human reading stderr.
        """
        try:
            fn()
        except CannotRun as e:
            return needle in str(e)
        except Exception:
            return False
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

    # --- check_target, the four outcomes. meta is injected so these are offline. ---
    SELF = "bettercallzaal/poidhz"
    OLD = "bettercallzaal/zpoidh"
    RID = 1255383001

    def ct(slug, expected, full_name, rid):
        meta = {"full_name": full_name}
        if rid is not None:
            meta["id"] = rid
        return check_target(slug, expected, meta=meta)

    ok("1. name and id both match passes",
       ct(SELF, RID, SELF, RID)[0] == SELF)
    ok("1. the passing case says the id was checked",
       "id both match" in ct(SELF, RID, SELF, RID)[2])

    # THE MOST DANGEROUS CASE: the name looks entirely right.
    ok("2. same name, different id refuses",
       raises(lambda: ct(SELF, RID, SELF, 999), "not the 1255383001"))
    ok("2. it says the name looks fine, since that is the whole trap",
       raises(lambda: ct(SELF, RID, SELF, 999), "Nothing in the name looks wrong"))

    # THE REAL CASE FROM THIS REPO: zpoidh is poidhz's former name, same id.
    ok("3. a rename is named as a rename, not as a wrong repo",
       raises(lambda: ct(OLD, RID, SELF, RID), "is a RENAME"))
    ok("3. a rename prints BOTH names",
       raises(lambda: ct(OLD, RID, SELF, RID), OLD) and
       raises(lambda: ct(OLD, RID, SELF, RID), SELF))
    ok("3. a rename carries the one-line config fix",
       raises(lambda: ct(OLD, RID, SELF, RID), "set the relevant *_repo in org.config.json"))
    ok("3. a rename says the stale counts were CORRECT, which is why it was invisible",
       raises(lambda: ct(OLD, RID, SELF, RID), "correct and silently stale"))

    ok("4. different name and different id is not called a rename",
       raises(lambda: ct(OLD, RID, "someone/else", 777), "not a rename"))

    # Degraded modes announce themselves rather than implying agreement.
    ok("no declared id, name matches: passes but says the id was unchecked",
       "id unchecked" in ct(SELF, None, SELF, RID)[2])
    ok("no declared id, name differs: refuses because rename is indistinguishable",
       raises(lambda: ct(OLD, None, SELF, RID), "cannot be told from an unrelated repo"))
    ok("github returned no id, name differs: refuses",
       raises(lambda: ct(OLD, RID, SELF, None), "GitHub returned no id"))
    ok("no full_name at all refuses",
       raises(lambda: ct(SELF, RID, None, RID), "no full_name"))

    # --- declared_id ---
    ok("absent id is None, not an error", declared_id({}, "self") is None)
    ok("integer id returns", declared_id({"self_repo_id": RID}, "self") == RID)
    ok("string id refuses", raises(lambda: declared_id({"self_repo_id": "1255383001"}, "self"), "not an integer"))
    ok("bool id refuses", raises(lambda: declared_id({"self_repo_id": True}, "self"), "not an integer"))
    ok("zero id refuses", raises(lambda: declared_id({"self_repo_id": 0}, "self"), "not a positive"))
    ok("negative id refuses", raises(lambda: declared_id({"self_repo_id": -1}, "self"), "not a positive"))

    # raises() itself: finding 1. A non-CannotRun exception must FAIL a check,
    # never take the suite down with it.
    def boom():
        raise TypeError("expected string or bytes-like object, got 'NoneType'")
    ok("a TypeError inside a check returns False instead of killing the run",
       raises(boom, "anything") is False)

    # The live config must carry both ids, or finding 2 is decoration.
    try:
        cfg2 = load_config()
        ok("live config declares self_repo_id", isinstance(declared_id(cfg2, "self"), int))
        ok("live config declares entry_repo_id", isinstance(declared_id(cfg2, "entry"), int))
    except CannotRun as e:
        ok(f"live config ids readable ({e})", False)

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
            slug = resolve_self(config, git_origin()) if which == "self" else resolve_entry(config)
            return slug, declared_id(config, which)

        if args.which:
            print(target(args.which)[0])
            return 0

        if args.open_prs:
            slug, expected_id = target(args.open_prs)
            echoed, prs, note = open_prs(slug, expected_id)
            print(f"{echoed}: {len(prs)} open pull request(s)  [{note}]")
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
