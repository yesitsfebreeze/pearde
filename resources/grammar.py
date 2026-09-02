#!/usr/bin/env python3
"""pearde grammar — the board's vocabulary: read it, grow it, and check it.

    python3 grammar.py check [board]      one problem per line; silent when clean
    python3 grammar.py list  [board]      term · group · meaning
    python3 grammar.py show  <term> [board]
                                          one term, and its collision row where it has one
    python3 grammar.py brief [board]      the vocabulary as one page, `term — meaning`
    python3 grammar.py add   <term> <meaning> [board] [--group <g>]
                                          append a row, print the path
    python3 grammar.py stale [board]      rows whose term appears nowhere else in the repo
    python3 grammar.py undefined [board]  words the board uses that no row defines
    python3 grammar.py init  [board]      write the file from the template

A grammar is `.pearde/grammar.md`. It is not a PRD: no state, never claimed,
never dispatched, invisible to the loop and to the progress line. It records
what every word this repo coined means, so a session, a worker and a person
name the same thing the same way. @references/grammar.md is the format. This
file is its only reader, so the format has one home.

Python 3 stdlib only.
"""
import datetime
import os
import re
import sys

REQUIRED = ("grammar", "subject", "date")
OPTIONAL = ("updated",)

KEY_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A markdown table row: leading pipe, cells, trailing pipe. The separator row
# (`|---|---|`) is every cell dashes and colons, and is skipped by shape.
SEP_RE = re.compile(r"^[\s:|-]+$")
BOARD_DIR = "pearde"
# `.pearde` — the hidden name every board carried until 2026-09-02,
# still found so a board that never migrated keeps working
# (@references/obsidian.md says why the dot had to go).
LEGACY_BOARD_DIR = ".pearde"
BOARD_DIRS = (BOARD_DIR, LEGACY_BOARD_DIR)
# The board's directory name is configurable, and a directory holding
# `settings.md` is how it is configured — @resources/board/plan.py
# `named_boards`. These names are never a board and are skipped unstatted;
# everything hidden is skipped by the dot rule.
SCAN_SKIP = frozenset(("node_modules", "target", "vendor", "__pycache__",
                       "build", "dist"))


def _clean(v):
    return re.sub(r"\s+#.*$", "", v).strip().strip("\"'")


def parse_fm(text):
    """(frontmatter, first body line index). None when the fence is missing or
    unterminated — the caller reports that, it is not a crash."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    fm = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fm, i + 1
        if line.lstrip().startswith("#"):
            continue
        m = KEY_RE.match(line)
        if m:
            fm[m.group(1)] = _clean(m.group(2))
    return None, 0


def cells(line):
    """The cells of a table row, or None when the line is not one. A row is
    `| a | b |`; the separator under a header is not a row."""
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|") or len(s) < 3:
        return None
    if SEP_RE.match(s):
        return None
    return [c.strip() for c in s[1:-1].split("|")]


def bare(term):
    """The term as it is looked up — the markup around it is emphasis, not
    part of the word. `**sweep**` and `` `sweep` `` are one term."""
    t = term.strip()
    while True:
        for a, b in (("**", "**"), ("*", "*"), ("`", "`")):
            if len(t) > len(a) + len(b) and t.startswith(a) and t.endswith(b):
                t = t[len(a):-len(b)].strip()
                break
        else:
            return t


def grammar_path(board):
    """`.pearde/grammar.md` unless `grammar:` in settings.md points elsewhere —
    several boards over one codebase share one vocabulary."""
    st = os.path.join(board, "settings.md")
    if os.path.isfile(st):
        fm, _ = parse_fm(open(st, encoding="utf-8").read())
        v = (fm or {}).get("grammar")
        if v:
            return os.path.normpath(os.path.join(board, v))
    return os.path.join(board, "grammar.md")


def read(board):
    """{'path','exists','fm','fenced','groups','terms','collisions','problems'}.

    `terms` is {term: {'term','meaning','group','line'}} keyed by the bare
    spelling; `collisions` the same for three-column rows. Parsing never
    raises: everything wrong is a line in `problems`, which is what `check`
    prints and `doctor` reports."""
    path = grammar_path(board)
    out = {"path": path, "exists": os.path.isfile(path), "fm": {},
           "fenced": False, "groups": [], "terms": {}, "collisions": {},
           "problems": []}
    if not out["exists"]:
        return out
    text = open(path, encoding="utf-8").read()
    fm, start = parse_fm(text)
    rel = os.path.relpath(path)
    if fm is None:
        out["problems"].append(f"{rel}: no `---` frontmatter fence, or one unterminated")
        return out
    out["fm"], out["fenced"] = fm, True

    for k in REQUIRED:
        if not fm.get(k):
            out["problems"].append(f"{rel}: required key `{k}` missing")
    for k in fm:
        if k not in REQUIRED + OPTIONAL:
            out["problems"].append(f"{rel}: key `{k}` is not in the closed set — "
                                   f"{', '.join(REQUIRED + OPTIONAL)}")
    for k in ("date", "updated"):
        v = fm.get(k)
        if v and not ISO_RE.match(v):
            out["problems"].append(f"{rel}: `{k}: {v}` is not ISO 8601")
    if (fm.get("updated") and fm.get("date")
            and ISO_RE.match(fm["updated"]) and ISO_RE.match(fm["date"])
            and fm["updated"] < fm["date"]):
        out["problems"].append(f"{rel}: `updated` precedes `date`")

    group = ""
    for n, line in enumerate(text.splitlines()[start:], start=start + 1):
        if line.startswith("## "):
            group = line[3:].strip()
            out["groups"].append(group)
            continue
        c = cells(line)
        if c is None:
            continue
        if len(c) == 2:
            term, meaning = bare(c[0]), c[1].strip()
            if term.lower() in ("term", "the word"):     # the header row
                continue
            if not term:
                out["problems"].append(f"{rel}:{n}: a row with no term")
                continue
            if not meaning:
                out["problems"].append(f"{rel}:{n}: `{term}` has no meaning")
                continue
            if term in out["terms"]:
                out["problems"].append(
                    f"{rel}:{n}: `{term}` is defined twice — "
                    f"first at line {out['terms'][term]['line']}")
                continue
            out["terms"][term] = {"term": c[0].strip(), "meaning": meaning,
                                  "group": group, "line": n}
        elif len(c) == 3:
            term = bare(c[0])
            if term.lower() in ("term", "the word"):
                continue
            if not term or not c[1].strip() or not c[2].strip():
                out["problems"].append(f"{rel}:{n}: a collision row with an empty side")
                continue
            out["collisions"][term] = {"term": c[0].strip(), "here": c[1].strip(),
                                       "and": c[2].strip(), "group": group,
                                       "line": n}
        else:
            out["problems"].append(
                f"{rel}:{n}: a table row of {len(c)} columns — "
                f"a term is two, a collision is three")

    return out


def check(board):
    g = read(board)
    return g["problems"]


def add(board, term, meaning, group=None):
    """Append one row to its group, creating the group at the end when it is
    new. The file is rewritten whole and atomically — one writer, so there is
    nothing to race."""
    g = read(board)
    if not g["exists"]:
        sys.exit(f"grammar: no {os.path.relpath(g['path'])} — "
                 f"`python3 grammar.py init` writes it")
    if bare(term) in g["terms"] or bare(term) in g["collisions"]:
        sys.exit(f"grammar: `{bare(term)}` is already defined — edit the row, "
                 f"do not add a second")
    group = group or (g["groups"][-1] if g["groups"] else "This repo")
    row = f"| {term} | {meaning} |"
    lines = open(g["path"], encoding="utf-8").read().splitlines()

    at = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and line[3:].strip() == group:
            at = i
    if at is None:                       # a group nobody has written yet
        while lines and not lines[-1].strip():
            lines.pop()
        lines += ["", f"## {group}", "", "| term | is |", "|---|---|", row]
    else:                                # the last table row under that heading
        end = len(lines)
        for j in range(at + 1, len(lines)):
            if lines[j].startswith("## "):
                end = j
                break
        last = at
        for j in range(at + 1, end):
            if cells(lines[j]) is not None or SEP_RE.match(lines[j].strip() or "x"):
                last = j
        lines.insert(last + 1, row)

    today = datetime.date.today().isoformat()
    for i, line in enumerate(lines):
        if line.startswith("updated: "):
            lines[i] = f"updated: {today}"
            break
        if line.strip() == "---" and i:
            lines.insert(i, f"updated: {today}")
            break
    tmp = g["path"] + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(tmp, g["path"])
    return g["path"]


def init(board):
    path = grammar_path(board)
    if os.path.isfile(path):
        return path
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tpl = open(os.path.join(root, "references", "templates", "grammar.md"),
               encoding="utf-8").read()
    name = ""
    st = os.path.join(board, "settings.md")
    if os.path.isfile(st):
        fm, _ = parse_fm(open(st, encoding="utf-8").read())
        name = (fm or {}).get("name") or ""
    name = name or os.path.basename(os.path.dirname(os.path.abspath(board)))
    tpl = (tpl.replace("<board>", name)
              .replace("<today>", datetime.date.today().isoformat()))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(tpl)
    os.replace(tmp, path)
    return path


def stale(board):
    """Terms that appear nowhere else in the repo. A candidate for deletion and
    a judgement, never a defect — a word said in passes and never typed is
    exactly the word a grammar exists for."""
    g = read(board)
    repo = os.path.dirname(os.path.abspath(board))
    hay = []
    skip = {".git", "__pycache__", "node_modules", *BOARD_DIRS}
    for r, ds, fs in os.walk(repo):
        ds[:] = [d for d in ds if d not in skip and not d.startswith(".")]
        for f in fs:
            if os.path.splitext(f)[1] in (".md", ".py", ".sh", ".js", ".css",
                                          ".json", ".txt", ".yml", ".yaml"):
                try:
                    hay.append(open(os.path.join(r, f), encoding="utf-8",
                                    errors="ignore").read())
                except OSError:
                    pass
    text = "\n".join(hay)
    out = []
    for term in list(g["terms"]) + list(g["collisions"]):
        if term.lower() not in text.lower():
            out.append(term)
    return sorted(out)


TEXT_EXT = (".md", ".py", ".sh", ".js", ".css", ".json", ".txt", ".yml",
            ".yaml")
KEYWORD_RE = re.compile(r"@@([a-z][a-z0-9-]*)")


def _walk(root, skip=()):
    """Every text file under `root`, sorted, hidden directories skipped. The
    order is the order `undefined` reports first hits in, so it is fixed."""
    for r, ds, fs in os.walk(root):
        ds[:] = sorted(d for d in ds
                       if d not in skip and not d.startswith("."))
        for f in sorted(fs):
            if os.path.splitext(f)[1] in TEXT_EXT:
                yield os.path.join(r, f)


def _text(path):
    try:
        return open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return ""


def undefined(board):
    """Words the board uses that no row defines — the direction `stale` does
    not run, and the one a cold worker trips on.

    Enumerated, never guessed. A definition is a judgement; a spelling is not,
    so this reads only what can be listed without reading prose:

    - every `@@<keyword>` under the board and in the repo's own `index.md`
    - every frontmatter key in `.pearde/prds/**/prd.md` and their `specs/*.md`
    - every key in `.pearde/settings.md`

    That is the limit, and it is a real one: a word reintroduced in prose alone
    is used by nobody this reads, so it is not caught here.

    Never part of `check` and it fails no `doctor` row — the same standing as
    `stale`, and for the same reason: what a word should mean is the author's
    to say. Returns `(word, where)` pairs, one per word, sorted, the first hit
    kept.
    """
    g = read(board)
    known = {t.lower() for t in list(g["terms"]) + list(g["collisions"])}
    repo = os.path.dirname(os.path.abspath(board))
    hits = {}

    def note(word, where):
        if word.lower() not in known and word.lower() not in hits:
            hits[word.lower()] = (word, where)

    def rel(path):
        return os.path.relpath(path, repo)

    index = os.path.join(repo, "index.md")
    for path in ([index] if os.path.isfile(index) else []) + list(_walk(board)):
        for kw in KEYWORD_RE.findall(_text(path)):
            note(kw, f"@@{kw} in {rel(path)}")

    prds = os.path.join(board, "prds")
    for path in _walk(prds):
        base = os.path.basename(path)
        parent = os.path.basename(os.path.dirname(path))
        if base != "prd.md" and parent != "specs":
            continue
        fm, _ = parse_fm(_text(path))
        for key in fm or {}:
            note(key, f"{key}: in {rel(path)}")

    settings = os.path.join(board, "settings.md")
    fm, _ = parse_fm(_text(settings))
    for key in fm or {}:
        note(key, f"{key}: in {rel(settings)}")

    return [hits[k] for k in sorted(hits)]


def is_board_dir(p):
    """A directory is a board only when it CARRIES one — `settings.md`, or a
    `prds/`. Duplicated from @resources/board/plan.py for the same reason the
    two names above are. The name alone is not proof: `pearde` is an ordinary
    word, and a folder called that beside a real board would shadow it."""
    return os.path.isdir(p) and (
        os.path.isfile(os.path.join(p, "settings.md"))
        or os.path.isdir(os.path.join(p, "prds")))


def board_link(p):
    """A board reached through the `.pearde` compatibility symlink is not
    called what the link is called — the directory it points at is. One
    level, resolved beside the link, never `realpath`, so a symlinked
    ANCESTOR stays spelled the way the caller spelled it. Duplicated from
    @resources/board/plan.py for the same reason the walk is."""
    if not os.path.islink(p):
        return p
    return os.path.normpath(os.path.join(os.path.dirname(p), os.readlink(p)))


def named_boards(d):
    """Immediate children of `d` carrying `settings.md` — how a board called
    neither `pearde` nor `.pearde` is found, and the whole of the
    board-directory configuration: renaming the directory is the only act
    that configures it. @resources/board/plan.py `named_boards` carries the
    reasoning. At most two come back, because one is the answer and two is a
    refusal."""
    hits, seen = [], set()
    try:
        names = sorted(os.listdir(d))
    except OSError:
        return hits
    for name in names:
        if name.startswith(".") or name in SCAN_SKIP:
            continue
        p = os.path.join(d, name)
        if not os.path.isfile(os.path.join(p, "settings.md")):
            continue
        real = os.path.realpath(p)         # a link beside its target is one board
        if real in seen:
            continue
        seen.add(real)
        hits.append(p)
        if len(hits) == 2:
            break
    return hits


def board_in(d):
    """The board inside project dir `d`, or None — `pearde/`, then `.pearde/`
    through its symlink, then the one child that carries `settings.md`."""
    for name in BOARD_DIRS:
        p = os.path.join(d, name)
        if is_board_dir(p):
            return board_link(p)
    found = named_boards(d)
    if len(found) > 1:
        sys.exit(f"grammar: two directories under {d} carry a board — "
                 f"{os.path.basename(found[0])}/ and "
                 f"{os.path.basename(found[1])}/; a project has one board, "
                 "so rename or remove one of them")
    return found[0] if found else None


def find_board(arg):
    if arg:
        p = os.path.abspath(arg)
        if os.path.basename(p) in BOARD_DIRS and is_board_dir(p):
            return board_link(p)
        b = board_in(p)
        if b:
            return b
        # the board named directly, under whatever it is called — asked last,
        # so a project holding one still resolves to the board inside it
        if os.path.isfile(os.path.join(p, "settings.md")):
            return p
        sys.exit(f"grammar: no {BOARD_DIR}/ board at {arg}")
    d = os.getcwd()
    while True:
        b = board_in(d)
        if b:
            return b
        nxt = os.path.dirname(d)
        if nxt == d:
            sys.exit(f"grammar: no {BOARD_DIR}/ board found walking up from the cwd")
        d = nxt


def main(argv):
    args = argv[1:]
    group = None
    if "--group" in args:
        i = args.index("--group")
        if i + 1 >= len(args):
            print("grammar: --group needs a value", file=sys.stderr)
            return 2
        group = args[i + 1]
        args = args[:i] + args[i + 2:]
    cmd = args[0] if args else "check"

    if cmd == "add":
        if len(args) < 3 or not args[1].strip() or not args[2].strip():
            print("grammar: add <term> <meaning> [board] [--group <g>]",
                  file=sys.stderr)
            return 2
        board = find_board(args[3] if len(args) > 3 else None)
        print(add(board, args[1], args[2], group))
        return 0
    if cmd == "show":
        if len(args) < 2:
            print("grammar: show <term> [board]", file=sys.stderr)
            return 2
        board = find_board(args[2] if len(args) > 2 else None)
        g, want = read(board), bare(args[1]).lower()
        hit = 0
        for term, t in g["terms"].items():
            if term.lower() == want:
                print(f"{t['term']} — {t['meaning']}   · {t['group']}")
                hit += 1
        for term, c in g["collisions"].items():
            if term.lower() == want:
                print(f"{c['term']} — here: {c['here']}")
                print(f"{' ' * len(c['term'])}   and here: {c['and']}")
                hit += 1
        if not hit:
            print(f"grammar: `{args[1]}` is not defined on this board",
                  file=sys.stderr)
            return 1
        return 0

    board = find_board(args[1] if len(args) > 1 else None)
    if cmd == "check":
        bad = check(board)
        if bad:
            print("\n".join(bad))
        return 1 if bad else 0
    if cmd == "init":
        print(init(board))
        return 0
    if cmd == "list":
        g = read(board)
        for term, t in g["terms"].items():
            print(f"{term:26} {t['group'][:22]:24} {t['meaning']}")
        for term, c in g["collisions"].items():
            print(f"{term:26} {c['group'][:22]:24} {c['here']} · vs · {c['and']}")
        return 0
    if cmd == "brief":
        g = read(board)
        for term, t in g["terms"].items():
            print(f"{term} — {t['meaning']}")
        for term, c in g["collisions"].items():
            print(f"{term} — {c['here']}; and: {c['and']}")
        return 0
    if cmd == "stale":
        for term in stale(board):
            print(term)
        return 0
    if cmd == "undefined":
        for word, where in undefined(board):
            print(f"{word} — {where}")
        return 0
    print(__doc__.strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
