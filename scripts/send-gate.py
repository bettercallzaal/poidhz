#!/usr/bin/env python3
"""
Is this draft safe to send yet? Turns a send gate from prose into a query.

Four drafts in this repo carry a banner saying do not send until R5's winner is public:
the Kenny R6 note, the wimpydwi retainer, the launch post, and R5's own announcement is
what they all wait on. Those banners are honor-system. Honor-system rules run at 3-40% in
this estate; enforced ones run at ~100%, and the whole reason the gates exist is that four
of five rounds were paid and left owing something nobody tracked.

Since rounds/rN/closeout.json now records each promise as kept / broken / na / unrecorded,
a gate can be answered instead of trusted: a file that declares

    <!-- SEND-GATE: round=5 -->

is not sendable while round 5 has any promise recorded broken.

    python3 scripts/send-gate.py --file rounds/r6/kenny-note.md
    python3 scripts/send-gate.py --all          # every gated file in the repo
    python3 scripts/send-gate.py --selftest     # offline

Exit 0 means every gate checked is open. Exit 1 means at least one is closed.

WHAT THIS DOES NOT DO: it does not send anything, and it cannot see whether a post went
out. It reads what a human recorded in the ledger. If nobody has recorded R5's promise as
kept, the gate stays shut - which is the correct default, because the failure being
prevented is exactly "we assumed someone had done it".
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE_RE = re.compile(r"<!--\s*SEND-GATE:\s*round=(\d+)\s*-->", re.I)


def gate_of(path: Path) -> int | None:
    try:
        m = GATE_RE.search(path.read_text())
    except Exception:
        return None
    return int(m.group(1)) if m else None


def round_state(round_num: int) -> tuple[list[dict], str] | None:
    """(broken_rows, reason) or None if the round has no ledger."""
    p = REPO_ROOT / "rounds" / f"r{round_num}" / "closeout.json"
    if not p.exists():
        return None
    try:
        rows = json.loads(p.read_text()).get("promises", [])
    except Exception:
        return None
    broken = [r for r in rows if r.get("status") == "broken"]
    unrecorded = [r for r in rows if r.get("status") == "unrecorded"]
    if broken:
        return broken, f"{len(broken)} promise(s) recorded BROKEN"
    if unrecorded:
        return unrecorded, (f"{len(unrecorded)} promise(s) still unrecorded - nobody has "
                            f"said whether they were kept")
    return [], ""


def check_file(path: Path, quiet: bool = False) -> bool:
    """True if sendable."""
    n = gate_of(path)
    rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
    if n is None:
        if not quiet:
            print(f"  ungated  {rel}")
        return True

    st = round_state(n)
    if st is None:
        print(f"  BLOCKED  {rel}")
        print(f"           gate names round {n}, which has no closeout.json - "
              f"scaffold it with postclose-check --scaffold")
        return False

    rows, reason = st
    if not rows:
        print(f"  OPEN     {rel} - round {n} has nothing outstanding")
        return True

    print(f"  BLOCKED  {rel}")
    print(f"           round {n}: {reason}")
    for r in rows[:3]:
        print(f'           - "{r.get("text","")[:88]}"')
    if len(rows) > 3:
        print(f"           ... and {len(rows) - 3} more")
    return False


def sweep() -> int:
    gated = []
    for p in sorted(REPO_ROOT.rglob("*.md")):
        if any(part in {".git", "node_modules", ".handoffs"} for part in p.parts):
            continue
        if gate_of(p) is not None:
            gated.append(p)
    if not gated:
        print("No file in this repo declares a SEND-GATE.")
        print("Add '<!-- SEND-GATE: round=N -->' to any draft that must wait on a round.")
        return 0
    print(f"Send-gate sweep - {len(gated)} gated file(s)\n")
    ok = all([check_file(p) for p in gated])
    print()
    if ok:
        print("Every gate is open.")
        return 0
    print("At least one gate is shut. Nothing here sends anything - this only answers.")
    return 1


def _selftest() -> bool:
    import tempfile
    passed = True

    def check(label: str, cond: bool) -> None:
        nonlocal passed
        print(f"  {'ok  ' if cond else 'FAIL'} {label}")
        passed = passed and cond

    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "note.md"
        f.write_text("# note\n<!-- SEND-GATE: round=5 -->\nbody\n")
        check("finds a declared gate", gate_of(f) == 5)
        f.write_text("# note\nno gate here\n")
        check("returns None when no gate is declared", gate_of(f) is None)
        f.write_text("# note\n<!-- send-gate: ROUND=12 -->\n")
        check("gate marker is case-insensitive", gate_of(f) == 12)

    check("R5's real ledger currently has broken promises",
          (round_state(5) or ([], ""))[0] != [])
    check("R1's real ledger is clean", (round_state(1) or (None, ""))[0] == [])
    check("an unknown round reports no ledger", round_state(99) is None)
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        print("send-gate selftest")
        good = _selftest()
        print("selftest:", "passed" if good else "FAILED")
        return 0 if good else 1
    if a.all:
        return sweep()
    if a.file is None:
        ap.error("--file, --all or --selftest")
    if not a.file.exists():
        print(f"ERROR: {a.file} does not exist")
        return 1
    return 0 if check_file(a.file.resolve()) else 1


if __name__ == "__main__":
    sys.exit(main())
