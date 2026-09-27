#!/usr/bin/env python3
"""Mark a promise kept on a round's ledger, but only if the gate agrees.

WHY THIS EXISTS, and it is a correction. On 2026-09-27 the round four ledger was
marked kept by a python heredoc typed into a terminal, which ran
check-feedback-promises.py and asserted exit 0 before writing. The commit message then
said "the script refused to write it until they were", and the ledger said the marking
was gated.

No committed script did that. The assert existed for the length of one shell command,
in one session, and nobody else ever got it. An independent reviewer caught the gap
between what the record claimed and what the repository actually contained: the claim
described a PROCEDURE and was written as if it described a MECHANISM. Those are the
same words and a different promise - a procedure is kept by whoever remembers it, and
this programme has measured honour-system rules at a small fraction of compliance.

So this is the mechanism the record was already claiming. It runs the gate, refuses on
any non-zero exit, and only then writes - and the refusal is tested by stubbing the
gate to 1 and asserting the file comes back byte-identical.

It also stamps from the clock in the same operation that writes, because a status of
kept with a hand-typed time is two claims and only one of them was checked.

EXIT CODES: 0 written, 1 the gate refused so nothing was written, 2 could not run.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE = REPO_ROOT / "scripts" / "check-feedback-promises.py"


class CannotRun(Exception):
    """The check could not be performed. Never reported as a pass."""


def run_gate(round_id, bounty):
    """Run the real gate. Returns (exit_code, output)."""
    if not GATE.exists():
        raise CannotRun(f"{GATE} is missing, so nothing can vouch for this marking")
    try:
        p = subprocess.run(
            [sys.executable, str(GATE), "--round", round_id, "--bounty", str(bounty)],
            capture_output=True, text=True, timeout=300,
        )
    except (OSError, subprocess.SubprocessError) as e:
        raise CannotRun(f"could not run the gate: {e}")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def ledger_path(round_id):
    p = REPO_ROOT / "rounds" / "daily" / round_id / "closeout.json"
    if not p.exists():
        raise CannotRun(f"{p} does not exist")
    if p.stat().st_size == 0:
        raise CannotRun(f"{p} is 0 bytes")
    return p


def mark(round_id, bounty, rows, status="kept", gate=run_gate, now=None):
    """Write `status` onto each row, ONLY if the gate exits 0.

    `rows` is a list of (index, evidence). Nothing is written unless every index
    exists and the gate agrees - a partial write would leave a ledger half true.
    """
    path = ledger_path(round_id)
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise CannotRun(f"{path} is not valid json: {e}")
    promises = data.get("promises")
    if not isinstance(promises, list) or not promises:
        raise CannotRun(f"{path} has no promises list")

    for idx, _ in rows:
        if not 0 <= idx < len(promises):
            raise CannotRun(f"promise index {idx} is out of range for {len(promises)} promises")
    if not rows:
        raise CannotRun("no rows given, so there is nothing to mark and nothing to verify")

    code, output = gate(round_id, bounty)
    if code != 0:
        return False, code, output, path

    stamp = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    for idx, evidence in rows:
        promises[idx]["status"] = status
        promises[idx]["evidence"] = evidence
        promises[idx]["recorded_at"] = stamp
    path.write_text(json.dumps(data, indent=2) + "\n")
    return True, code, output, path


def selftest():
    import tempfile, shutil
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    global REPO_ROOT
    real_root = REPO_ROOT
    with tempfile.TemporaryDirectory() as td:
        REPO_ROOT = Path(td)
        rd = REPO_ROOT / "rounds" / "daily" / "t"
        rd.mkdir(parents=True)
        led = rd / "closeout.json"
        fixture = {"promises": [
            {"text": "a", "status": "unrecorded", "evidence": "", "recorded_at": ""},
            {"text": "b", "status": "unrecorded", "evidence": "", "recorded_at": ""},
        ]}

        def reset():
            led.write_text(json.dumps(fixture, indent=2) + "\n")
            return led.read_bytes()

        # THE REFUSAL IS THE WHOLE POINT. A gate that exits 1 must leave the file
        # byte-identical - not merely unmarked, untouched.
        before = reset()
        wrote, code, out, _ = mark("t", 1, [(0, "E")], gate=lambda r, b: (1, "BROKEN: x"))
        ok("a gate exit of 1 does not write", wrote is False)
        ok("and the file is BYTE-IDENTICAL afterwards", led.read_bytes() == before)
        ok("the refusal carries the gate's own output", "BROKEN: x" in out)

        before = reset()
        wrote, _, _, _ = mark("t", 1, [(0, "E")], gate=lambda r, b: (2, "CANNOT RUN"))
        ok("a gate exit of 2 does not write either", wrote is False)
        ok("exit 2 also leaves the file byte-identical", led.read_bytes() == before)

        # Exit 0 writes, and writes everything asked for.
        reset()
        fixed = datetime(2026, 9, 27, 21, 30, 0, tzinfo=timezone.utc)
        wrote, _, _, _ = mark("t", 1, [(0, "E-zero"), (1, "E-one")],
                              gate=lambda r, b: (0, "all good"), now=fixed)
        d = json.loads(led.read_text())
        ok("a gate exit of 0 writes", wrote is True)
        ok("both rows are marked kept", [p["status"] for p in d["promises"]] == ["kept", "kept"])
        ok("each row gets its own evidence",
           d["promises"][0]["evidence"] == "E-zero" and d["promises"][1]["evidence"] == "E-one")
        ok("the stamp comes from the clock passed in, not from the caller's text",
           d["promises"][0]["recorded_at"] == "2026-09-27T21:30:00Z")
        ok("the stamp is the same across rows written together",
           d["promises"][0]["recorded_at"] == d["promises"][1]["recorded_at"])

        # A bad index must refuse BEFORE the gate runs, so a typo cannot half-write.
        before = reset()
        ran = []
        try:
            mark("t", 1, [(0, "E"), (9, "E")], gate=lambda r, b: (ran.append(1), (0, ""))[1])
            ok("an out-of-range index refuses", False)
        except CannotRun as e:
            ok("an out-of-range index refuses", "out of range" in str(e))
        ok("and it refuses before running the gate at all", not ran)
        ok("leaving the file byte-identical", led.read_bytes() == before)

        try:
            mark("t", 1, [], gate=lambda r, b: (0, ""))
            ok("an empty row list refuses", False)
        except CannotRun as e:
            ok("an empty row list refuses", "nothing to mark" in str(e))

        try:
            mark("nope", 1, [(0, "E")], gate=lambda r, b: (0, ""))
            ok("a missing ledger refuses", False)
        except CannotRun as e:
            ok("a missing ledger refuses", "does not exist" in str(e))

        led.write_text("")
        try:
            mark("t", 1, [(0, "E")], gate=lambda r, b: (0, ""))
            ok("a 0-byte ledger refuses", False)
        except CannotRun as e:
            ok("a 0-byte ledger refuses", "0 bytes" in str(e))

    REPO_ROOT = real_root
    ok("the real gate script exists to be run", GATE.exists())

    width = max(len(n) for n, _ in checks)
    for name, passed in checks:
        print(f"  {'ok  ' if passed else 'FAIL'} {name.ljust(width)}")
    failed = [n for n, p in checks if not p]
    print(f"selftest: {len(checks) - len(failed)}/{len(checks)} passed")
    return 0 if not failed else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--round")
    ap.add_argument("--bounty", type=int)
    ap.add_argument("--promise", action="append", default=[], metavar="INDEX=EVIDENCE",
                    help="repeatable; the row index, '=', then the evidence text")
    ap.add_argument("--status", default="kept", choices=["kept", "broken", "na", "unrecorded"])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.round or not args.bounty or not args.promise:
        ap.error("--round, --bounty and at least one --promise are required")

    rows = []
    for spec in args.promise:
        if "=" not in spec:
            print(f"CANNOT RUN: --promise {spec!r} has no '='", file=sys.stderr)
            return 2
        i, ev = spec.split("=", 1)
        try:
            rows.append((int(i), ev))
        except ValueError:
            print(f"CANNOT RUN: {i!r} is not a row index", file=sys.stderr)
            return 2

    try:
        wrote, code, output, path = mark(args.round, args.bounty, rows, status=args.status)
    except CannotRun as e:
        print(f"CANNOT RUN: {e}", file=sys.stderr)
        return 2

    if not wrote:
        print(f"REFUSED: the gate exited {code}, so nothing was written to {path.name}.")
        print(output.rstrip())
        return 1
    print(f"gate exited 0. Marked {len(rows)} row(s) {args.status} in {path}.")
    print(output.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
