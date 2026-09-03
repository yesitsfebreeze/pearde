#!/usr/bin/env python3
"""Cut resources/board/plan.py into modules beside it, by responsibility.

Run:  python3 cut.py <repo-root>

The cut is expressed as line ranges over the file as it stands, so it is
re-runnable from a clean checkout and reviewable as a table. Every range is
moved verbatim; the only rewriting is the import header each new module gets
and the one cross-module global the split would otherwise snapshot.
"""
import ast
import os
import sys

# The revision of plan.py this table addresses. `plan.py.orig` beside this
# script is that file byte for byte, and BASE_LINES is its length. The check
# on it in `main` refuses two mistakes the `uncovered` guard cannot see: an
# input that is the ALREADY-CUT plan.py (a second run silently re-cuts the
# 637-line stub into ten smaller stubs and every count collapses), and an
# input from a revision the table was not written for.
BASE = "31620bb"
BASE_LINES = 3242

# module -> ordered line ranges (1-based, inclusive) of plan.py
#
# The table is line numbers, so it is pinned to one revision of the file: it
# was first written against the 3060-line plan.py kept beside this script as
# `plan.py.orig`, `board_at` grew a 139-line board-discovery pass in
# `1880990`, and `NotABoard`, `state_dir`'s husk guard and `session_tree`
# added 43 more across `39c0cab..31620bb`. Re-running it against a moved
# plan.py is a re-cut, not a merge — map every boundary through a diff of
# `plan.py.orig` against the new file, refresh `plan.py.orig` and BASE_LINES,
# and the `uncovered` guard below proves the table still covers the file. It
# fires on the first line the table forgot.
CUT = {
    "boards": [(55, 424), (1102, 1106), (3102, 3117), (3121, 3121), (3139, 3180)],
    "prdfile": [(425, 559), (715, 975), (1108, 1113), (2346, 2446)],
    "repos": [(1294, 1392)],
    "registry": [(560, 714), (1115, 1156), (1281, 1292), (1962, 1968), (2945, 2950)],
    "silence": [(976, 1100)],
    "needs": [(2000, 2103)],
    "vision": [(1158, 1279), (2975, 3029)],
    "schedule": [(1875, 1960), (1970, 1998), (2105, 2322), (2448, 2586), (2838, 2844)],
    "mapfile": [(1394, 1753), (1755, 1818), (2324, 2344)],
    "plan": [(1820, 1873), (2588, 2836), (2846, 2943), (2952, 2973), (3031, 3100),
             (3120, 3120), (3123, 3137), (3182, 3242)],
}

# import order: a module may only depend on ones before it
ORDER = ["boards", "prdfile", "repos", "registry", "silence", "needs",
         "vision", "schedule", "mapfile", "plan"]

DOC = {
    "boards": "where a board is on disk, and how a new one is made",
    "prdfile": "one PRD file: its frontmatter, its boxes, its typed numbers",
    "repos": "the git tree under a board, and the lanes cut off it",
    "registry": "the PRDs a board holds and the boards a master merges",
    "silence": "whether a held PRD is still moving",
    "needs": "what a PRD waits on before it may run",
    "vision": "the axis prds/vision.md declares, and the depth along it",
    "schedule": "what may run now, and in what order",
    "mapfile": "the plan on disk, the journals, and the payload the view reads",
}

PREAMBLE_RANGE = (26, 53)   # the stdlib imports and the sibling-script preamble

HEAD = '#!/usr/bin/env python3\n"""pearde {mod} — {doc}.\n\nCut out of plan.py; plan.py re-exports every name here, so every caller that\nimports `plan` keeps working. Python 3 stdlib only.\n"""\n'


def main():
    root = os.path.abspath(sys.argv[1])
    src_path = os.path.join(root, "resources", "board", "plan.py")
    src = open(src_path).read()
    lines = src.splitlines(keepends=True)
    if len(lines) != BASE_LINES:
        raise SystemExit(
            "%s is %d lines; the table addresses %s, which is %d. Restore the "
            "input from plan.py.orig beside this script (or from the base "
            "revision) before cutting, or re-map the table onto the new file."
            % (src_path, len(lines), BASE, BASE_LINES))
    tree = ast.parse(src)

    where = {}
    for n in tree.body:
        start = n.lineno
        for d in getattr(n, "decorator_list", []):
            start = min(start, d.lineno)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            where[n.name] = start
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    where[t.id] = start

    line_mod = {}
    for mod, ranges in CUT.items():
        for a, b in ranges:
            for ln in range(a, b + 1):
                if ln in line_mod:
                    raise SystemExit("line %d claimed by %s and %s"
                                     % (ln, line_mod[ln], mod))
                line_mod[ln] = mod

    uncovered = [ln for ln in range(55, len(lines) + 1)
                 if ln not in line_mod and lines[ln - 1].strip()]
    if uncovered:
        raise SystemExit("uncovered non-blank lines: %s" % uncovered[:30])

    home = {name: ln for name, ln in where.items()}
    home = {name: line_mod[ln] for name, ln in home.items() if ln in line_mod}

    needs = {m: {} for m in CUT}
    for n in tree.body:
        start = n.lineno
        for d in getattr(n, "decorator_list", []):
            start = min(start, d.lineno)
        mod = line_mod.get(start)
        if mod is None:
            continue
        for sub in ast.walk(n):
            if isinstance(sub, ast.Name) and sub.id in home and home[sub.id] != mod:
                needs[mod].setdefault(home[sub.id], set()).add(sub.id)

    # A rebound module global cannot travel by `from x import name` — the
    # importer would hold the value it had at import time. Only the parse
    # cache has one; its readers address it through the module.
    THROUGH_MODULE = {"_PCACHE_DIRTY", "_PCACHE", "_PCACHE_LOADED"}

    preamble = "".join(lines[PREAMBLE_RANGE[0] - 1:PREAMBLE_RANGE[1]])
    out_dir = os.path.join(root, "resources", "board")
    report = []
    for mod in ORDER:
        body = "\n".join("".join(lines[a - 1:b]).rstrip("\n") for a, b in CUT[mod]) + "\n"
        head = []
        if mod == "plan":
            head.append("".join(lines[0:PREAMBLE_RANGE[1]]))
        else:
            head.append(HEAD.format(mod=mod, doc=DOC[mod]))
            head.append(preamble)
        for dep in ORDER:
            if dep == mod:
                continue
            got = set(needs[mod].get(dep, ()))
            through = got & THROUGH_MODULE
            got -= THROUGH_MODULE
            if through:
                head.append("import %s  # noqa: E402 — a rebound global, read live\n" % dep)
                for name in sorted(through):
                    body = body.replace(name, dep + "." + name)
            if got:
                head.append("from %s import (%s)  # noqa: E402,F401\n"
                            % (dep, ", ".join(sorted(got))))
        if mod == "plan":
            # The three parse-cache globals are rebound at run time, so they
            # cannot be re-exported by value — and a caller outside this
            # package still has to reach them: the parse-cache harness pokes
            # `planlib.prdfile._PCACHE`. The module object is the only handle
            # that stays live, so `plan` carries it whether or not `plan`'s
            # own body names one.
            head.append("import prdfile  # noqa: E402,F401 — _PCACHE and "
                        "friends are rebound at run\n")
            head.append("\n# The module every caller imports. Each name below stands where it\n"
                        "# always stood; only the file holding it changed.\n")
            by_mod = {}
            for name, m in home.items():
                if m != "plan":
                    by_mod.setdefault(m, []).append(name)
            for dep in ORDER:
                if dep not in by_mod:
                    continue
                rest = sorted(n for n in by_mod[dep]
                              if n not in needs["plan"].get(dep, set())
                              and n not in THROUGH_MODULE)
                if rest:
                    head.append("from %s import (%s)  # noqa: E402,F401\n"
                                % (dep, ", ".join(rest)))
        if mod == "boards":
            # `cmd_example` prints the command a person is to run next, and it
            # spelled it with its own `__file__`. Moved, that prints boards.py
            # — a command that exists and does something else. The entry point
            # is plan.py wherever this code lives, so name it.
            body = body.replace(
                'print(f"      python3 {os.path.abspath(__file__)} scan {dest}")',
                'print(f"      python3 {os.path.join(HERE, \'plan.py\')} scan {dest}")')
            head.append('HERE = os.path.dirname(os.path.abspath(__file__))\n')
        if mod == "plan":
            # `cmd_calibrate` prints where the margin is hand-set. `TUNE`
            # leaves for mapfile.py, so the sentence the tool prints goes
            # false the moment the cut lands. Rewritten here rather than by
            # hand, so a re-cut from a clean checkout carries it too.
            body = body.replace("hard-coded in plan.py)",
                                "hard-coded in mapfile.py)")
        text = "".join(head) + "\n" + body
        open(os.path.join(out_dir, mod + ".py"), "w").write(text)
        report.append((mod, len(text.splitlines())))
    for mod, n in report:
        print("%-10s %5d lines%s" % (mod, n, "   OVER 700" if n > 700 else ""))


if __name__ == "__main__":
    main()
