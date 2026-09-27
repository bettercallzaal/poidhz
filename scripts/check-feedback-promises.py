#!/usr/bin/env python3
"""Check the feedback promises a round's bounty text actually makes.

WHY THIS EXISTS. Three of the eleven promises in round four's ledger are about
written notes: EVERYONE WHO ENTERS GETS WRITTEN NOTES, "one thing your piece did
and one thing to do better", and "they go up at poidhz.com/feedback - every
entrant gets their own page". All three are "every entrant" promises, so none of
them can be checked against anything except the FIELD AT THE CLOSE - and that is
a number this repo only learned to record on 2026-09-27.

Every one of these was verified by hand at 15:4x on 2026-09-27, one curl at a
time. That is the part worth mechanising: the check is identical every round, it
runs at a fixed moment, and doing it by hand is how a round ships with an entrant
who never got notes.

THREE WAYS IT WOULD HAVE LIED IF WRITTEN CARELESSLY, all three hit for real
during that hand pass:

1. The page path is /feedback/<bounty_id>/<handle>. Probing it with a CLAIM ID
   returns 404 for every entrant AND for the control, so a wrong URL shape looks
   exactly like missing pages. The control must be a handle, not a bogus number.
2. A field present in the json does not mean the rendered page prints it. Both
   are checked, against the live html.
3. "No entrant is missing notes" from an empty entrant list is vacuously true.
   An empty field, an empty roster or a failed fetch is exit 2, never a pass.

EXIT CODES: 0 the promises hold, 1 one is broken, 2 the check could not run.
"""

import argparse
import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FEEDBACK_DATA = REPO_ROOT / "data" / "feedback"
SITE = "https://poidhz.com"


class CannotRun(Exception):
    """The check could not be performed. Never reported as a pass."""


def load_round(round_id):
    p = FEEDBACK_DATA / f"{round_id}.json"
    if not p.exists():
        raise CannotRun(f"{p} does not exist, so there is nothing to check against")
    if p.stat().st_size == 0:
        raise CannotRun(f"{p} is 0 bytes")
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        raise CannotRun(f"{p} is not valid json: {e}")
    entrants = data.get("entrants")
    if not isinstance(entrants, list) or not entrants:
        raise CannotRun(
            f"{p} has no entrant rows. 'no entrant is missing notes' would be "
            "vacuously true, which is the shape this refuses."
        )
    return data, entrants, p


def live_claim_handles(bounty_id, chain=8453):
    """The field, from claims.fetchBountyClaims via query-bounty.

    Deliberately NOT from /data, which does not carry isAccepted and has been
    the source of four wrong answers in this repo.
    """
    script = REPO_ROOT / "scripts" / "query-bounty.py"
    if not script.exists():
        raise CannotRun(f"{script} is missing, so the live field cannot be read")
    out = subprocess.run(
        [sys.executable, str(script), "--bounty", str(bounty_id), "--json"],
        capture_output=True, text=True, timeout=120,
    )
    if out.returncode != 0:
        raise CannotRun(f"query-bounty failed for {bounty_id}: {(out.stderr or '').strip()[:200]}")
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError as e:
        raise CannotRun(f"query-bounty returned unparseable json: {e}")
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        raise CannotRun(f"bounty {bounty_id} returned no claims, so the field is unknown, not empty")
    return {int(c["claimId"]) for c in claims if c.get("claimId") is not None}


def fetch_page(url, timeout=30):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except (urllib.error.URLError, OSError) as e:
        raise CannotRun(f"could not reach {url}: {e}")


def visible_text(page):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(page)))


def both_halves(entrant):
    """promise: one thing your piece did, and one thing to do better.

    did_well is the first half; items carry the second. A whitespace-only
    did_well is missing, not present.
    """
    did = (entrant.get("did_well") or "").strip()
    items = entrant.get("items") or []
    return bool(did), len(items)


def check(round_id, bounty_id, offline=False, fetch=fetch_page, field=None):
    data, entrants, path = load_round(round_id)
    problems, notes = [], []
    handles = [e.get("handle") for e in entrants]
    if any(not h for h in handles):
        raise CannotRun(f"{path} has an entrant row with no handle")
    if len(set(handles)) != len(handles):
        raise CannotRun(f"{path} has duplicate handles: {sorted(h for h in handles if handles.count(h) > 1)}")

    # PROMISE: everyone who enters gets written notes. Only answerable against
    # the field, which is why this needs the close.
    if field is None and not offline:
        field = live_claim_handles(bounty_id)
    if field is not None:
        covered = {int(e["claim"]) for e in entrants if e.get("claim") is not None}
        missing = sorted(field - covered)
        extra = sorted(covered - field)
        if missing:
            problems.append(
                f"EVERYONE WHO ENTERS GETS WRITTEN NOTES is BROKEN: claim(s) {missing} are in the "
                f"field of {len(field)} and have no row in {path.name}"
            )
        else:
            notes.append(f"every one of the {len(field)} claim(s) in the field has a notes row")
        if extra:
            notes.append(
                f"{len(extra)} row(s) cover claim(s) not in the field ({extra}) - a withdrawn claim "
                "still counted, which is right, but say so rather than letting the totals differ silently"
            )
    else:
        notes.append("field NOT read (offline), so the 'everyone' promise is UNKNOWN, not kept")

    # PROMISE: one thing it did and one thing to do better.
    for e in entrants:
        has_did, n_items = both_halves(e)
        if not has_did:
            problems.append(f"{e['handle']}: no did_well, so 'one thing your piece did' is BROKEN")
        if n_items < 1:
            problems.append(f"{e['handle']}: no items, so 'one thing to do better' is BROKEN")

    # PROMISE: every entrant gets their own page at /feedback/<bounty>/<handle>,
    # and the page must PRINT both halves, not merely be reachable.
    live = 0
    if not offline:
        for e in entrants:
            url = f"{SITE}/feedback/{bounty_id}/{e['handle']}"
            status, page = fetch(url)
            if status != 200:
                problems.append(f"{e['handle']}: {url} returns HTTP {status}, so they have no page")
                continue
            live += 1
            txt = visible_text(page)
            did = (e.get("did_well") or "").strip()
            if did and did[:60] not in txt:
                problems.append(f"{e['handle']}: page is up but does not print did_well")
            items = e.get("items") or []
            if items and (items[0].get("title") or "")[:60] not in txt:
                problems.append(f"{e['handle']}: page is up but does not print the first item")
        idx = f"{SITE}/feedback/{bounty_id}"
        status, _ = fetch(idx)
        if status != 200:
            problems.append(f"the round index {idx} returns HTTP {status}")
        else:
            # COUNT WHAT ANSWERED, NOT WHAT WAS ASKED FOR. This line used to read
            # len(entrants), so on 2026-09-27 it printed "6 page(s) live and printing
            # both halves" directly above "dee-13: ... returns HTTP 404, so they have
            # no page". Five were live. A summary that restates the input as though it
            # were the result is the exact failure this script exists to catch, printed
            # by the script itself.
            of = f"{live} of {len(entrants)}" if live != len(entrants) else f"all {live}"
            notes.append(f"{of} page(s) live and printing both halves, plus the round index")

    return problems, notes, len(entrants)


def selftest():
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    def raises(fn, needle):
        try:
            fn()
        except CannotRun as e:
            return needle in str(e)
        except Exception:
            return False
        return False

    ok("whitespace did_well counts as missing", both_halves({"did_well": "   ", "items": [{}]})[0] is False)
    ok("absent did_well counts as missing", both_halves({"items": [{}]})[0] is False)
    ok("real did_well counts as present", both_halves({"did_well": "x", "items": [{}]})[0] is True)
    ok("no items counts as zero", both_halves({"did_well": "x"})[1] == 0)
    ok("items counted", both_halves({"did_well": "x", "items": [{}, {}]})[1] == 2)

    ok("tags stripped from html", "hello" in visible_text("<p>hello</p>"))
    ok("entities unescaped", "it's" in visible_text("<p>it&#39;s</p>"))
    ok("whitespace collapsed", visible_text("<p>a\n\n  b</p>").strip() == "a b")

    ok("a missing round file refuses",
       raises(lambda: load_round("nope-does-not-exist"), "does not exist"))

    # The vacuous-pass refusals, which are the point of the script.
    import tempfile, os
    with tempfile.TemporaryDirectory() as td:
        global FEEDBACK_DATA
        real = FEEDBACK_DATA
        FEEDBACK_DATA = Path(td)
        try:
            (Path(td) / "empty.json").write_text("")
            ok("a 0-byte round file refuses", raises(lambda: load_round("empty"), "0 bytes"))
            (Path(td) / "noent.json").write_text('{"entrants": []}')
            ok("an EMPTY entrant list refuses rather than passing vacuously",
               raises(lambda: load_round("noent"), "vacuously true"))
            (Path(td) / "bad.json").write_text("{not json")
            ok("unparseable json refuses", raises(lambda: load_round("bad"), "not valid json"))
            (Path(td) / "nohandle.json").write_text('{"entrants": [{"claim": 1}]}')
            ok("an entrant with no handle refuses",
               raises(lambda: check("nohandle", 1, offline=True), "no handle"))
            (Path(td) / "dupe.json").write_text('{"entrants": [{"handle":"a","claim":1},{"handle":"a","claim":2}]}')
            ok("duplicate handles refuse",
               raises(lambda: check("dupe", 1, offline=True), "duplicate handles"))

            # The 'everyone' promise, the one that needs the field.
            (Path(td) / "cov.json").write_text(
                '{"entrants": [{"handle":"a","claim":1,"did_well":"x","items":[{"title":"t"}]}]}')
            probs, notes, n = check("cov", 1, offline=True, field={1, 2})
            ok("a claim in the field with no notes row is reported BROKEN",
               any("EVERYONE WHO ENTERS" in p and "[2]" in p for p in probs))
            probs, notes, n = check("cov", 1, offline=True, field={1})
            ok("full coverage is not reported as a problem", not probs)
            ok("full coverage says how many were covered",
               any("every one of the 1 claim" in x for x in notes))
            # A row covering a claim the field no longer has: a withdrawn claim
            # that still got notes. That is correct behaviour and must be a NOTE,
            # never a break - and the note must say the totals differ on purpose.
            # This assertion was first written as a literal True, which is the
            # same defect as an `or True`: it passed while checking nothing.
            probs, notes, n = check("cov", 1, offline=True, field={2})
            ok("a covered claim absent from the field is a note, not a break",
               any("cover claim(s) not in the field" in x for x in notes))
            ok("that note does not turn into a BROKEN line",
               not any("cover claim(s) not in the field" in p for p in probs))
            ok("but a field claim with no row IS still broken in the same run",
               any("EVERYONE WHO ENTERS" in p for p in probs))
            probs, notes, n = check("cov", 1, offline=True)
            ok("offline with no field says UNKNOWN rather than kept",
               any("UNKNOWN, not kept" in x for x in notes))

            # Both-halves breaks are named per entrant.
            (Path(td) / "half.json").write_text(
                '{"entrants": [{"handle":"a","claim":1,"did_well":"  ","items":[]}]}')
            probs, _, _ = check("half", 1, offline=True, field={1})
            ok("a blank did_well is named as BROKEN", any("one thing your piece did' is BROKEN" in p for p in probs))
            ok("no items is named as BROKEN", any("one thing to do better' is BROKEN" in p for p in probs))

            # A page that 200s but does not print the halves must still fail.
            (Path(td) / "pg.json").write_text(
                '{"entrants": [{"handle":"a","claim":1,"did_well":"THE GOOD BIT","items":[{"title":"THE FIX"}]}]}')
            probs, _, _ = check("pg", 1, field={1},
                                fetch=lambda u, timeout=30: (200, "<p>THE GOOD BIT</p><p>THE FIX</p>"))
            ok("a page printing both halves passes", not probs)
            probs, _, _ = check("pg", 1, field={1},
                                fetch=lambda u, timeout=30: (200, "<p>THE GOOD BIT</p>"))
            ok("a page missing the item is BROKEN even though it returns 200",
               any("does not print the first item" in p for p in probs))
            probs, _, _ = check("pg", 1, field={1},
                                fetch=lambda u, timeout=30: (200, "<p>THE FIX</p>"))
            ok("a page missing did_well is BROKEN even though it returns 200",
               any("does not print did_well" in p for p in probs))
            probs, _, _ = check("pg", 1, field={1}, fetch=lambda u, timeout=30: (404, ""))
            ok("a 404 page is reported as having no page", any("HTTP 404" in p for p in probs))

            # THE NOTE MUST COUNT WHAT ANSWERED. It used to print len(entrants) and so
            # claimed pages were live in the same breath as reporting them 404.
            (Path(td) / "two.json").write_text(
                '{"entrants": ['
                '{"handle":"a","claim":1,"did_well":"G","items":[{"title":"F"}]},'
                '{"handle":"b","claim":2,"did_well":"G","items":[{"title":"F"}]}]}')
            def one_missing(u, timeout=30):
                return (404, "") if u.endswith("/b") else (200, "<p>G</p><p>F</p>")
            probs, notes, _ = check("two", 1, field={1, 2}, fetch=one_missing)
            ok("with one page 404, the note says 1 of 2 rather than 2",
               any("1 of 2 page(s) live" in x for x in notes))
            ok("it never claims all pages are live when one is missing",
               not any("all 2 page(s) live" in x for x in notes))
            ok("and the 404 is still reported as a break",
               any("HTTP 404" in p for p in probs))
            probs2, notes2, _ = check("two", 1, field={1, 2},
                                      fetch=lambda u, timeout=30: (200, "<p>G</p><p>F</p>"))
            ok("with every page live the note says all 2", any("all 2 page(s) live" in x for x in notes2))
        finally:
            FEEDBACK_DATA = real

    width = max(len(n) for n, _ in checks)
    for name, passed in checks:
        print(f"  {'ok  ' if passed else 'FAIL'} {name.ljust(width)}")
    failed = [n for n, p in checks if not p]
    print(f"selftest: {len(checks) - len(failed)}/{len(checks)} passed")
    return 0 if not failed else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--round", help="round id, e.g. d04 (the basename in data/feedback/)")
    ap.add_argument("--bounty", type=int, help="poidh bounty id for that round")
    ap.add_argument("--offline", action="store_true", help="skip the live field and page fetches; the 'everyone' promise then reports UNKNOWN")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.round or not args.bounty:
        ap.error("--round and --bounty are both required")

    try:
        problems, notes, n = check(args.round, args.bounty, offline=args.offline)
    except CannotRun as e:
        print(f"CANNOT RUN: {e}", file=sys.stderr)
        return 2

    print(f"{args.round} / bounty {args.bounty}: {n} entrant row(s) in data/feedback/{args.round}.json")
    for x in notes:
        print(f"  note: {x}")
    if problems:
        for p in problems:
            print(f"  BROKEN: {p}")
        print(f"{len(problems)} promise problem(s). The ledger row stays unrecorded or goes to broken.")
        return 1
    print("Every feedback promise checked here holds. Not checked: whether the notes are any good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
