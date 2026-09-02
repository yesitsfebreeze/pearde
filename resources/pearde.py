#!/usr/bin/env python3
"""pearde — the board's one command. Every tool is a subcommand of it.

    pearde                    the board on one page — the same as `scan`
    pearde <cmd> [args…]      one command; the board argument is optional everywhere
    pearde <cmd> --help       that command's line and the flags it takes, exit 0
    pearde help               one line per command

A dispatcher, not a home. No logic lives here: each name forwards to the
script that owns it, arguments in the order that script takes them, exit
code passed through. The board is resolved by the script that reads it, the
way @resources/board/plan.py `find_board` does — the path given, or the
nearest `.pearde/` walking up from the working directory.

Discovery. Every `*.py` in `resources/` or in any directory directly under
it — @resources/pearde_path.py `dirs`, the same list that is on `sys.path` —
that exposes `COMMANDS = {"<name>": <callable>}` is imported and its names
are routed. A
callable takes the argument list after the name and returns the exit code
(`None` reads as 0); its docstring's first line is the `help` line, and its
`flags` attribute — the declaration @resources/board/transitions.py `Args`
parses — is the `takes:` line under `--help`, so the two cannot drift. A
child adds a module; nothing edits this file. A name two modules claim, or a name
this file already forwards, is refused: `help` prints the clash and exits 1,
and `doctor` reports that under `skills`.

The names that arrive with later children are reserved here and answer
`not yet — <child>` until a module claims them.

Python 3 stdlib only.
"""
import glob
import importlib.util
import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402 — @resources/pearde_path.py, the one rule


def skill_root():
    """The repo this file belongs to: the nearest ancestor holding
    `resources/pearde.py` — this file, the one that cannot move, so it is the
    marker. Works from `resources/pearde.py` and from a probe copy alike."""
    d = pearde_path.skill_root(__file__)
    if d is None:
        print("pearde: no resources/pearde.py above this file",
              file=sys.stderr)
        sys.exit(2)
    return d


ROOT = skill_root()
RES = os.path.join(ROOT, "resources")

# The contract table of @.pearde/prds/the-board-runs-itself/one-command/prd.md, one
# row per name pearde forwards. `script` is a bare basename —
# @resources/pearde_path.py `script` finds it under resources/, so a file can
# move between directories and no row here changes; `verbs` are the
# words the script takes first — when the first argument is one of them the
# arguments go through untouched, otherwise `prefix` is put in front. A row
# with no verbs always gets its prefix.
FORWARD = {
    "scan":      ("plan.py", ["scan"], ()),
    "plan":      ("plan.py", ["plan"], ()),
    "reconcile": ("plan.py", ["reconcile"], ()),
    "gantt":     ("plan.py", ["gantt"], ()),
    "calibrate": ("plan.py", ["calibrate"], ()),
    "status":    ("plan.py", ["status"], ()),
    "members":   ("plan.py", ["members"], ()),
    "view":      ("serve.py", ["ensure"],
                  ("ensure", "status", "stop", "wait", "forget", "run",
                   "reap")),
    "memo":      ("memos.py", [], ("list", "check", "add", "verify",
                                   "index", "retag")),
    "workflow":  ("workflows.py", [], ("list", "show", "brief", "check",
                                       "retag")),
    "grammar":   ("grammar.py", [], ("list", "show", "brief", "add", "check",
                                     "stale", "undefined", "init")),
    "health":    ("health.py", [], ("score", "list", "show", "check", "init")),
    "questions": ("questions.py", ["check"], ("check", "list")),
    "index":     ("index.py", ["check"],
                  ("check", "files", "keywords", "scope")),
    "guard":     ("guard.py", ["status"], ("on", "off", "status")),
    "doctor":    ("doctor.sh", [], ()),
    "install":   ("install.sh", [], ()),
    "update":    ("update.sh", [], ()),
}

# Reserved: a name a later child delivers, answering `not yet — <child>`
# until a module claims it. Empty today — every name the tree named has its
# module. Discovery wins over this table, so a row is never removed by hand
# when a module lands; it is removed when the child's PRD is `done`.
RESERVED = {}

WIDTH = 80


# ── discovery ─────────────────────────────────────────────────────────────────

COMMANDS_RE = re.compile(r"^COMMANDS\s*=", re.M)


def modules():
    """Every `*.py` under `resources/` and under each directory directly
    under it, sorted by basename — the walk @resources/pearde_path.py `dirs`
    defines, so a module is found wherever it lands. A basename claimed by
    two directories is a problem, not a silent win for whichever sorted
    first: both paths come back and `discover` reports the clash."""
    seen = {}
    for d in pearde_path.dirs():
        for path in sorted(glob.glob(os.path.join(d, "*.py"))):
            seen.setdefault(os.path.basename(path), []).append(path)
    return [(name, paths) for name, paths in sorted(seen.items())]


def discover():
    """(commands, problems). commands: name -> (module basename, callable).
    Only a module whose source says `COMMANDS =` is imported — importing
    plan.py or serve.py to find out they have none would cost every call."""
    found, problems = {}, []
    for base, paths in modules():
        path = paths[0]
        if len(paths) > 1:
            problems.append(f"{base} is in "
                            + " and ".join(os.path.basename(os.path.dirname(q))
                                           for q in paths)
                            + " — one basename, one directory")
            continue
        try:
            src = open(path, encoding="utf-8").read()
        except OSError as e:
            problems.append(f"{os.path.basename(path)}: {e}")
            continue
        if not COMMANDS_RE.search(src):
            continue
        mod = os.path.basename(path)[:-3]
        try:
            spec = importlib.util.spec_from_file_location(f"pearde_{mod}", path)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
        except Exception as e:  # a broken child must not take the rest down
            problems.append(f"{mod}.py failed to import: {e}")
            continue
        cmds = getattr(m, "COMMANDS", None)
        if not isinstance(cmds, dict):
            problems.append(f"{mod}.py: COMMANDS is not a dict")
            continue
        for name, fn in cmds.items():
            if not callable(fn):
                problems.append(f"{mod}.py: COMMANDS[{name!r}] is not callable")
                continue
            if name in FORWARD:
                problems.append(f"`{name}` is forwarded by pearde.py and "
                                f"claimed by {mod}.py")
                continue
            if name in found:
                problems.append(f"`{name}` is claimed by both "
                                f"{found[name][0]}.py and {mod}.py")
                continue
            found[name] = (mod, fn)
    # An empty walk is not an answer. A `resources/` gone or unreadable
    # yields no module, no exception and no problem, and every subcommand
    # then falls through to the did-you-mean arm — which tells the reader
    # their verb was wrong when the truth is that the install is not there.
    # Say it once, in the one place that can tell the difference. The walk
    # is now every directory under `resources/`, so the emptiness worth
    # naming is an empty `found`, not an empty glob over one directory.
    if not found:
        problems.append(f"no subcommands: no *.py under {RES} or any "
                        f"directory under it exposes COMMANDS — the install "
                        f"is incomplete, not the command wrong")
    return found, problems


# ── help, from docstrings ─────────────────────────────────────────────────────

USAGE_RE = re.compile(r"^\s*(?:python3\s+|bash\s+)?(?:@?[\w./-]*/)?(\w+\.(?:py|sh))\s+(\S.*)$")


def docstring(script):
    """A .py's module docstring, or a .sh's leading `#` block."""
    path = pearde_path.script(script)
    if path is None:
        return ""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return ""
    if script.endswith(".sh"):
        out = []
        for line in text.splitlines()[1:]:
            if not line.startswith("#"):
                break
            out.append(line[1:])
        return "\n".join(out)
    m = re.search(r'"""(.*?)"""', text, re.S)
    return m.group(1) if m else ""


def split_usage(rest):
    """`plan  [board] [--workers N]   the frontier` → (verb, args, desc).
    The verb is a bare first word; the arguments are the `[…]`, `<…>` and
    `--flag` tokens after it, a bracket group kept whole; what follows is
    the description. Whitespace is not the separator — the docstrings do not
    agree on how many spaces sit before a description."""
    toks, depth, cur = [], 0, ""
    for ch in rest:
        if ch.isspace() and depth == 0:
            if cur:
                toks.append(cur)
            cur = ""
            continue
        depth += ch in "[<"
        depth -= ch in "]>"
        cur += ch
    if cur:
        toks.append(cur)
    verb, args, i = "", [], 0
    if toks and re.fullmatch(r"[a-z][\w-]*", toks[0]):
        verb, i = toks[0], 1
    while i < len(toks) and toks[i][:1] in "[<-":
        args.append(toks[i])
        i += 1
    return verb, " ".join(args), " ".join(toks[i:])


def usage_lines(script):
    """[(verb, args, description)] from the docstring: a usage line names
    the script, and the indented lines under it continue its description."""
    base = os.path.basename(script)
    rows = []
    for line in docstring(script).splitlines():
        m = USAGE_RE.match(line)
        if m and m.group(1) == base:
            rows.append(list(split_usage(m.group(2))))
        elif rows and line.startswith(" " * 16) and line.strip():
            rows[-1][2] += " " + line.strip()
        elif rows and not line.strip():
            break
    return [tuple(r) for r in rows]


def title_line(script):
    """`pearde plan — the board, read and ordered.` → after the dash."""
    first = docstring(script).strip().splitlines()[:1]
    if not first:
        return ""
    return re.sub(r"^.*?—\s*", "", first[0]).rstrip(".")


def fit(left, desc):
    line = f"  {left:<28} {desc}".rstrip()
    if len(line) <= WIDTH:
        return line
    cut = line[:WIDTH - 1]
    return cut[:cut.rfind(" ")] + "…"


def help_lines(name):
    """The `help` lines for one name: one per verb where the script has
    verbs, one per usage row where it has none, one for the forwarded verb
    otherwise. A verb the docstring does not list gets the script's title."""
    if name not in FORWARD:
        return []
    script, prefix, verbs = FORWARD[name]
    rows = usage_lines(script)
    title = title_line(script)
    out = []
    if verbs:
        for v in verbs:
            _, args, desc = next((r for r in rows if r[0] == v),
                                 (v, "", title))
            shown = (f"pearde {name}" if prefix and v == prefix[0]
                     else f"pearde {name} {v}")
            out.append(fit(f"{shown} {args}".rstrip(), desc))
        return out
    if prefix:
        _, args, desc = next((r for r in rows if r[0] == prefix[0]),
                             ("", "", title))
        return [fit(f"pearde {name} {args}".rstrip(), desc)]
    for _, args, desc in rows or [("", "", title)]:
        out.append(fit(f"pearde {name} {args}".rstrip(), desc))
    return out


def cmd_help(found, problems):
    print("pearde — the board's one command; every tool is a subcommand")
    print()
    print(fit("pearde", "the board on one page — `scan`"))
    for name in FORWARD:
        for line in help_lines(name):
            print(line)
    for name, (mod, fn) in sorted(found.items()):
        doc = (fn.__doc__ or "").strip().splitlines()[:1]
        print(fit(f"pearde {name}", doc[0] if doc else f"{mod}.py"))
    for name, child in RESERVED.items():
        if name not in found:
            print(fit(f"pearde {name}", f"not yet — {child}"))
    print(fit("pearde help", "this list"))
    if problems:
        for p in problems:
            print(f"pearde: {p}", file=sys.stderr)
        return 1
    return 0


# ── forwarding ────────────────────────────────────────────────────────────────

def run(script, args):
    path = pearde_path.script(script)
    if path is None:
        print(f"pearde: no {script} under {RES}", file=sys.stderr)
        return 2
    cmd = (["bash", path] if script.endswith(".sh")
           else [sys.executable, path]) + list(args)
    try:
        return subprocess.call(cmd)
    except KeyboardInterrupt:
        return 130


def forward(name, args):
    script, prefix, verbs = FORWARD[name]
    if args and verbs and args[0] in verbs:
        return run(script, args)
    return run(script, prefix + args)


def cmd_view(args):
    """`view` is `serve.py ensure`, then the URL it printed is opened. The
    other verbs pass through. `--no-open` keeps the browser shut — a harness
    wants the registration, not a window."""
    if args and args[0] in FORWARD["view"][2]:
        return run("serve.py", args)
    want_open = "--no-open" not in args
    rest = [a for a in args if a != "--no-open"]
    path = pearde_path.script("serve.py")
    if path is None:
        print(f"pearde: no serve.py under {RES}", file=sys.stderr)
        return 2
    p = subprocess.run([sys.executable, path, "ensure"] + rest,
                       capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.stderr.write(p.stderr)
    if p.returncode != 0:
        return p.returncode
    m = re.search(r"https?://\S+", p.stdout)
    if m and want_open:
        import webbrowser
        webbrowser.open(m.group(0))
    return 0


# ── main ──────────────────────────────────────────────────────────────────────

def main(argv):
    args = list(argv[1:])
    found, problems = discover()
    if not args:
        return forward("scan", [])
    name, rest = args[0], args[1:]
    if name in ("help", "-h", "--help"):
        return cmd_help(found, problems)
    for p in problems:
        print(f"pearde: {p}", file=sys.stderr)
    if name in found:
        if "--help" in rest or rest[:1] == ["-h"]:
            fn = found[name][1]
            print(fit(f"pearde {name}",
                      (fn.__doc__ or "").strip().split("\n")[0]))
            flags = getattr(fn, "flags", None)
            if flags:
                print(f"  takes: {flags}")
            return 0
        rc = found[name][1](rest)
        return 0 if rc is None else int(rc)
    if name in FORWARD:
        if "--help" in rest or "-h" in rest:
            for line in help_lines(name):
                print(line)
            return 0
        if name == "view":
            return cmd_view(rest)
        return forward(name, rest)
    if name in RESERVED:
        if "--help" in rest:
            print(fit(f"pearde {name}", f"not yet — {RESERVED[name]}"))
            return 0
        print(f"not yet — {RESERVED[name]}", file=sys.stderr)
        return 1
    names = list(FORWARD) + sorted(found) + [n for n in RESERVED
                                             if n not in found]
    near = [n for n in names if n.startswith(name[:2])]
    hint = f" — did you mean {', '.join(near)}?" if near else ""
    print(f"pearde: unknown command `{name}`{hint} · `pearde help` lists them",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
