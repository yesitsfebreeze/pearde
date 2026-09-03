#!/usr/bin/env python3
"""Scope resolution, measured against fixtures built at run time.

    python3 probe/scope.py [<repo>]

`<repo>` is the checkout to measure — the lane by default, never the
orchestrator's. Every fixture board is made under a fresh temp dir and torn
down; no watch set is read and nothing is dispatched.
"""
import os
import shutil
import sys
import tempfile

REPO = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "resources", "board"))
import run as runlib          # noqa: E402
import dispatch as displib    # noqa: E402
import inspect                # noqa: E402

OK = FAIL = 0


def check(name, got, want):
    global OK, FAIL
    if got == want:
        OK += 1
        print(f"  ok   {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name}\n       got  {got!r}\n       want {want!r}")


def board(root, name, groups=None, prds=()):
    b = os.path.join(root, name, "pearde")
    os.makedirs(os.path.join(b, "prds"), exist_ok=True)
    with open(os.path.join(b, "settings.md"), "w") as f:
        f.write("---\nlanguage: English\n"
                + (f"groups: {groups}\n" if groups else "") + "---\n")
    for p in prds:
        d = os.path.join(b, "prds", p)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "prd.md"), "w") as f:
            f.write("---\nstate: open\npriority: 50\ncomplexity: 5\n"
                    "blast-radius: low\n---\n\n# " + p + "\n\nA fixture.\n")
    return b


def main():
    root = tempfile.mkdtemp(prefix="run-scope-")
    try:
        # ── the closed word sets ─────────────────────────────────────────
        check("dispatch is no longer a verb",
              "dispatch" in runlib.READ_VERBS, False)
        check("the four windows",
              runlib.READ_VERBS,
              ("boards", "slots", "progress", "groups"))
        check("here and all are reserved", runlib.RESERVED, ("here", "all"))

        # ── a verb and a scope compose in either order ───────────────────
        check("group and verb read in either order",
              runlib.split_scope(["work", "slots"]),
              runlib.split_scope(["slots", "work"]))
        check("a flag's value is not a scope",
              runlib.split_scope(["--workers", "4", "--dry"])[0], None)
        check("a bare word after flags is the scope",
              runlib.split_scope(["--dry", "private"])[0], "private")
        check("run takes a window as a plain scope word",
              runlib.split_scope(["slots"], verbs=())[0], "slots")

        # ── a label a board may not declare ──────────────────────────────
        b = board(root, "verby", groups="slots all here work")
        check("a window and both reserved words are refused as labels",
              sorted(g for g, _ in runlib.declared(b)[1]),
              ["all", "here", "slots"])
        check("reserved words are refused as labels",
              sorted(runlib.declared(b)[0]), ["work"])
        b2 = board(root, "reserved", groups="here")
        check("here is refused as a label", runlib.declared(b2)[0], [])

        # ── the resolution order ─────────────────────────────────────────
        cwd = board(root, "cwdboard", groups="private",
                    prds=("alpha", "private"))
        known = {"private": ["one"], "infra": ["two"]}
        check("here resolves reserved",
              runlib.resolve_scope("here", known, cwd), ("reserved", "here"))
        check("all resolves reserved",
              runlib.resolve_scope("all", known, cwd), ("reserved", "all"))
        check("a PRD on the cwd board resolves to a PRD",
              runlib.resolve_scope("alpha", known, cwd), ("prd", "alpha"))
        check("a declared label with no PRD resolves to a group",
              runlib.resolve_scope("infra", known, cwd), ("group", "infra"))
        try:
            runlib.resolve_scope("private", known, cwd)
            check("a word that is both is refused", "resolved", "refused")
        except ValueError as e:
            check("a word that is both is refused naming both",
                  ("group" in str(e) and "PRD" in str(e)), True)
        try:
            runlib.resolve_scope("nothing-like-this", known, cwd)
            check("an unknown word is refused", "resolved", "refused")
        except ValueError as e:
            check("an unknown word names the groups that exist",
                  "private" in str(e) and "infra" in str(e), True)

        # ── dispatch is a library, not a command ─────────────────────────
        sig = list(inspect.signature(displib.main).parameters)
        check("dispatch.main takes entries and only",
              sig, ["argv", "entries", "only"])
        src = open(os.path.join(REPO, "resources", "board",
                                "dispatch.py"), encoding="utf-8").read()
        check("--group is gone from dispatch.py", "--group" in src, False)
        check("dispatch.py names pearde run", "pearde run" in src, True)

        # ── the files moved ──────────────────────────────────────────────
        for gone in ("resources/board/machine.py",
                     "references/parts/machine.md"):
            check(f"{gone} is gone",
                  os.path.exists(os.path.join(REPO, gone)), False)
        for made in ("resources/board/run.py", "references/parts/run.md"):
            check(f"{made} is on disk",
                  os.path.exists(os.path.join(REPO, made)), True)
        check("run.py exposes COMMANDS['run']",
              sorted(runlib.COMMANDS), ["run"])
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print(f"\n{OK} ok · {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
