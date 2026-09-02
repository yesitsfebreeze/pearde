#!/usr/bin/env python3
"""pearde_path — the one rule by which a module under `resources/` finds its
siblings, its repo root and the scripts it launches.

Importing this module puts `resources/` and every directory directly under it
on `sys.path`, so a bare `import plan` resolves from any of them. A file can
move between those directories with no second edit anywhere.

Every module under `resources/` opens with the same two lines, whatever
directory it sits in:

    sys.path.insert(0, RES_FROM(__file__))
    import pearde_path  # noqa: E402,F401

which in practice is written out, because nothing can be imported before the
path is set:

    _D = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                    else os.path.dirname(_D))
    import pearde_path  # noqa: E402,F401

`skill_root()` is the repo above `resources/`, found by `resources/pearde.py`
— the one file that cannot move. `script(name)` finds a script by its
basename anywhere under `resources/`, for the callers that launch a sibling
as a subprocess, where `sys.path` does nothing.

Python 3 stdlib only. Imported for its side effect; it imports nothing of
this tree itself, so it can never be part of a cycle.
"""
import os
import sys

RES = os.path.dirname(os.path.abspath(__file__))


def dirs():
    """`resources/` and every directory directly under it, in the order they
    go on `sys.path`. A name starting `.` or `_` is skipped — `__pycache__`
    is not a package of ours — and so is `node_modules`."""
    out = [RES]
    try:
        names = sorted(os.listdir(RES))
    except OSError:
        return out
    for n in names:
        if n.startswith((".", "_")) or n == "node_modules":
            continue
        d = os.path.join(RES, n)
        if os.path.isdir(d):
            out.append(d)
    return out


def _install():
    for d in reversed(dirs()):
        if d not in sys.path:
            sys.path.insert(0, d)


_install()


def skill_root(start=None):
    """The repo this tree belongs to: the nearest ancestor holding
    `resources/pearde.py`. `resources/pearde.py` is the dispatcher and the
    one file that cannot move, so it is the marker. Returns None when there
    is none above `start` — the caller decides what that costs."""
    d = os.path.dirname(os.path.abspath(start or __file__))
    while True:
        if os.path.isfile(os.path.join(d, "resources", "pearde.py")):
            return d
        nxt = os.path.dirname(d)
        if nxt == d:
            return None
        d = nxt


def script(name):
    """The path of a script under `resources/`, by basename — `serve.py`,
    `doctor.sh`. Searched in `dirs()` order, `resources/` first. Returns None
    when no directory under `resources/` holds it.

    `sys.path` does nothing for a subprocess spelled by path, so every caller
    that launches a sibling asks here instead of spelling its directory."""
    for d in dirs():
        p = os.path.join(d, name)
        if os.path.isfile(p):
            return p
    return None
