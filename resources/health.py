#!/usr/bin/env python3
"""pearde health — every tracked file scored 1-100, worst first.

    python3 health.py score [path...] [board]  score the tree, or these paths; write the notes and the ranking
    python3 health.py list  [--under <n>] [path...] [board]
                                               one line per file, worst first, off the ranking — no rescoring; --under keeps files under n, default the floor
    python3 health.py show  <path> [board]     one file's note
    python3 health.py check [board]            one problem per line; silent when clean
    python3 health.py init  [board]            make .pearde/health/ and ignore it on the board

A health record is `.pearde/health/`: one note per scored file under
`files/`, and `ranking.md` worst first. It is not a PRD: no state, never
claimed, never dispatched, invisible to the loop. It records how much a file
resists being worked on — lines, branching, longest function, and what the
knowledge graph knows about its callers and dependencies — so the brief can
name the files in a footprint that sit under the floor.
@references/health.md is the format. This file is its only reader, so the
format has one home. A score is a pointer, never a verdict.

Python 3 stdlib only.
"""
import ast
import datetime
import json
import math
import os
import re
import subprocess
import sys

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
OUT_DIR = "health"

NOTE_KEYS = ("health", "file", "language", "score", "lines", "branching",
             "nesting", "longest", "fan_out", "fan_in", "links", "worst",
             "date", "commit", "graph")
NOTE_REQUIRED = tuple(k for k in NOTE_KEYS if k != "worst")
RANK_KEYS = ("health", "date", "commit", "graph", "files", "skipped", "floor",
             "unhealthy")

AXES = ("lines", "branching", "longest", "fan_out", "fan_in", "links")
DEFAULT_WEIGHTS = {"lines": 25, "branching": 30, "longest": 20,
                   "fan_out": 5, "fan_in": 10, "links": 10}
DEFAULT_FLOOR = 40
STALE_AFTER = 20            # commits behind HEAD before `check` says stale

# (0 at, 1 at, scale) — the raw value under the first is no problem, over the
# second is the whole problem. Constants, not settings: a threshold moved per
# board makes two boards' 40s two different numbers.
THRESHOLDS = {
    "lines":    {"code": (150, 1500, "log"), "document": (300, 3000, "log")},
    "branch":   (10, 50, "log"),
    "nesting":  (4, 10, "lin"),
    "longest":  {"code": (40, 400, "log"), "document": (80, 800, "log")},
    "fan_out":  (3, 20, "lin"),
    "fan_in":   (2, 25, "log"),
    "links":    (0.1, 0.5, "lin"),
}

LANG = {".py": "python", ".js": "javascript", ".mjs": "javascript",
        ".cjs": "javascript", ".jsx": "javascript", ".ts": "typescript",
        ".tsx": "typescript", ".sh": "shell", ".bash": "shell",
        ".zsh": "shell", ".nu": "shell", ".css": "css", ".scss": "css",
        ".md": "markdown", ".go": "go", ".rs": "rust", ".rb": "ruby",
        ".java": "java", ".kt": "kotlin", ".swift": "swift", ".c": "c",
        ".h": "c", ".cpp": "cpp", ".cc": "cpp", ".hpp": "cpp",
        ".html": "html", ".vue": "javascript", ".svelte": "javascript",
        ".php": "php", ".lua": "lua", ".pl": "perl"}
SHEBANG = (("python", "python"), ("bash", "shell"), ("zsh", "shell"),
           ("sh", "shell"), ("node", "javascript"), ("ruby", "ruby"),
           ("perl", "perl"))
DOCUMENT = {"markdown", "html"}
NO_BRANCHING = {"markdown", "html", "css"}
SKIP_DIRS = {"node_modules", "vendor", "third_party", "dist", "build",
             "__pycache__", ".git", *BOARD_DIRS}
SKIP_NAMES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml",
              "Cargo.lock", "poetry.lock", "uv.lock", "Gemfile.lock"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
            ".woff", ".woff2", ".ttf", ".otf", ".pdf", ".zip", ".gz", ".tar",
            ".json", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".lock",
            ".txt", ".csv", ".tsv", ".xml", ".plist", ".min.js", ".min.css"}
MAX_BYTES = 2_000_000
MINIFIED_AVG = 300          # average characters per line

GRAPH_RELATIONS = {"calls", "imports", "references", "method",
                   "indirect_call", "inherits", "extends"}

# Branch keywords per language family. `case` counts in every brace language;
# a bare `?` would count every optional-chain in JS so it is left out and the
# ternary is caught by ` ? ` with spaces.
BRANCH_RE = {
    "c":    r"\b(if|for|while|case|catch)\b|&&|\|\||\s\?\s",
    "shell": r"^\s*(if|elif|for|while|until|case)\b|\)\s*$|&&|\|\|",
    "ruby": r"\b(if|elsif|unless|for|while|until|when|rescue)\b|&&|\|\|",
    "lua":  r"\b(if|elseif|for|while|repeat)\b|\band\b|\bor\b",
}
BRANCH_FAMILY = {"javascript": "c", "typescript": "c", "go": "c", "rust": "c",
                 "java": "c", "kotlin": "c", "swift": "c", "c": "c",
                 "cpp": "c", "php": "c", "perl": "c", "python": "python",
                 "shell": "shell", "ruby": "ruby", "lua": "lua"}
BRANCH_RE["python"] = (r"^\s*(if|elif|for|while|try|except|with|case)\b"
                       r"|\band\b|\bor\b|\bif\b.*\belse\b")
FUNC_RE = {
    "c": re.compile(r"^\s*(?:(?:export|default|static|async|pub|fn|func|def"
                    r"|function|public|private|protected|override|inline"
                    r"|const|let|var)\s+)*[\w<>\[\]:*&, .]*?\b(\w+)\s*(?:<[^>]*>)?"
                    r"\s*\([^;{]*\)\s*(?:->\s*[\w<>\[\]:&*, ]+)?\s*(?:const\s*)?"
                    r"\{\s*$|^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?"
                    r"(?:\([^)]*\)|\w+)\s*=>\s*\{\s*$"),
    "shell": re.compile(r"^\s*(?:function\s+)?([\w.-]+)\s*\(\)\s*\{|^\s*function"
                        r"\s+([\w.-]+)\s*\{|^\s*(?:export\s+)?def\s+([\w-]+)"),
    "ruby": re.compile(r"^\s*def\s+([\w.?!]+)"),
    "lua": re.compile(r"^\s*(?:local\s+)?function\s+([\w.:]+)"),
    "python": re.compile(r"^\s*(?:async\s+)?def\s+(\w+)"),
}
BRACE_FAMILIES = {"c", "shell", "lua"}

KEY_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEP_RE = re.compile(r"^[\s:|-]+$")
HEADING_RE = re.compile(r"^#{1,6}\s")


# ── reading ──────────────────────────────────────────────────────────────────

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


def board_named(d):
    """`<d>/pearde`, or `<d>/.pearde` when only that carries a board — the two
    names the tool knows, the second read through its compat symlink."""
    for name in BOARD_DIRS:
        p = os.path.join(d, name)
        if is_board_dir(p):
            return board_link(p)
    return None


def board_scanned(d):
    """The board of `d` that is called something else — one immediate child
    holding `settings.md`, and a refusal when there are two."""
    found = named_boards(d)
    if len(found) > 1:
        sys.exit(f"health: two directories under {d} carry a board — "
                 f"{os.path.basename(found[0])}/ and "
                 f"{os.path.basename(found[1])}/; a project has one board, "
                 "so rename or remove one of them")
    return found[0] if found else None


def board_in(d):
    """The board inside project dir `d` — the named one, then the scanned
    one. The answer for a directory a caller pointed at deliberately."""
    return board_named(d) or board_scanned(d)


def walk_up(d, find):
    """`find` applied to `d` and every ancestor, first answer wins."""
    while True:
        b = find(d)
        if b:
            return b
        nxt = os.path.dirname(d)
        if nxt == d:
            return None
        d = nxt


def board_above(d):
    """The board `d` belongs to — two passes, a named board winning at any
    depth over a discovered one nearer the cwd. @resources/board/plan.py
    `board_above` says why discovery cannot be part of the climb."""
    return walk_up(d, board_named) or walk_up(d, board_scanned)


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
        sys.exit(f"health: no {BOARD_DIR}/ board at {arg}")
    b = board_above(os.getcwd())
    if b:
        return b
    sys.exit(f"health: no {BOARD_DIR}/ board found walking up from the cwd")


def is_board(arg):
    """Is `arg` a board, or does it hold one — the same tests `find_board`
    makes, and none of its refusals. A predicate answers; two boards under
    one project is still a project with a board in it."""
    p = os.path.abspath(arg)
    return ((os.path.basename(p) in BOARD_DIRS and is_board_dir(p))
            or any(is_board_dir(os.path.join(p, n)) for n in BOARD_DIRS)
            or bool(named_boards(p))
            or os.path.isfile(os.path.join(p, "settings.md")))


def repo_root(board):
    return os.path.dirname(os.path.abspath(board))


def out_dir(board):
    return os.path.join(board, OUT_DIR)


def settings(board):
    """{'floor', 'weights', 'problems'} from `health-floor` and
    `health-weights` in settings.md. Anything wrong is a problem line and the
    default stands — a knob that cannot be read is not a knob at zero."""
    out = {"floor": DEFAULT_FLOOR, "weights": dict(DEFAULT_WEIGHTS),
           "problems": []}
    st = os.path.join(board, "settings.md")
    if not os.path.isfile(st):
        return out
    fm, _ = parse_fm(_text(st))
    fm = fm or {}
    rel = os.path.relpath(st)
    v = fm.get("health-floor")
    if v not in (None, ""):
        try:
            n = int(v)
            if not 1 <= n <= 100:
                raise ValueError
            out["floor"] = n
        except ValueError:
            out["problems"].append(
                f"{rel}: `health-floor: {v}` is not an integer 1-100 — "
                f"reading {DEFAULT_FLOOR}")
    v = fm.get("health-weights")
    if v not in (None, ""):
        for tok in v.split():
            k, _, w = tok.partition("=")
            if k not in AXES:
                out["problems"].append(
                    f"{rel}: `health-weights` names `{k}` — the axes are "
                    f"{', '.join(AXES)}")
                continue
            try:
                n = float(w)
                if not 0 <= n <= 100:
                    raise ValueError
                out["weights"][k] = n
            except ValueError:
                out["problems"].append(
                    f"{rel}: `health-weights` `{tok}` is not a number 0-100 — "
                    f"reading {DEFAULT_WEIGHTS[k]}")
    if not any(out["weights"].values()):
        out["problems"].append(f"{rel}: every `health-weights` weight is 0 — "
                               "reading the defaults")
        out["weights"] = dict(DEFAULT_WEIGHTS)
    return out


def _text(path):
    try:
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def _git(root, *args):
    try:
        r = subprocess.run(["git", "-C", root] + list(args),
                           capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout if r.returncode == 0 else None


def head_commit(root):
    out = _git(root, "rev-parse", "--short=7", "HEAD")
    return out.strip() if out else None


def commits_behind(root, commit):
    if not commit or commit == "none":
        return None
    out = _git(root, "rev-list", "--count", f"{commit}..HEAD")
    try:
        return int(out.strip())
    except (AttributeError, ValueError):
        return None


def tracked_files(root):
    """Repo-relative paths, sorted — what git tracks or would track, the
    same call @resources/index.py makes, minus the board itself. No git: the
    tree walked, hidden directories skipped."""
    out = _git(root, "ls-files", "-z", "--cached", "--others",
               "--exclude-standard")
    if out is not None:
        files = [p for p in out.split("\0") if p]
    else:
        files = []
        for r, ds, fs in os.walk(root):
            ds[:] = sorted(d for d in ds if not d.startswith(".")
                           and d not in SKIP_DIRS)
            for f in fs:
                files.append(os.path.relpath(os.path.join(r, f), root))
    files = [os.path.normpath(p) for p in files]
    files = [p for p in files if p.split(os.sep)[0] not in BOARD_DIRS
             and os.path.isfile(os.path.join(root, p))]
    return sorted(set(files))


# ── what is scored ───────────────────────────────────────────────────────────

def language_of(root, rel):
    base = os.path.basename(rel)
    low = base.lower()
    for ext in (".min.js", ".min.css"):
        if low.endswith(ext):
            return None
    ext = os.path.splitext(low)[1]
    if ext in LANG:
        return LANG[ext]
    if ext:
        return None
    try:
        with open(os.path.join(root, rel), "rb") as f:
            head = f.read(200).decode("utf-8", "replace")
    except OSError:
        return None
    if head.startswith("#!"):
        first = head.splitlines()[0]
        for word, lang in SHEBANG:
            if re.search(rf"\b{word}\d*(\s|$)", first):
                return lang
    return None


def skip_reason(root, rel):
    parts = rel.split(os.sep)
    if any(p in SKIP_DIRS for p in parts[:-1]):
        return "vendored or built"
    base = parts[-1]
    if base in SKIP_NAMES:
        return "lockfile"
    low = base.lower()
    if low.endswith((".min.js", ".min.css")):
        return "minified"
    if os.path.splitext(low)[1] in SKIP_EXT:
        return "data or asset"
    path = os.path.join(root, rel)
    try:
        size = os.path.getsize(path)
    except OSError:
        return "unreadable"
    if size > MAX_BYTES:
        return "over 2 MB"
    if is_binary(path):
        return "binary"
    if language_of(root, rel) is None:
        return "no language"
    return None


def is_binary(path):
    try:
        with open(path, "rb") as f:
            head = f.read(8192)
    except OSError:
        return True
    return b"\0" in head


def slug(rel):
    return re.sub(r"[^\w.-]+", "-", rel)


# ── measuring ────────────────────────────────────────────────────────────────

def measure_lines(text):
    return len(text.splitlines())


class _PyVisit(ast.NodeVisitor):
    """Branch points and nesting per function. A nested def is its own
    function; module-level code is the pseudo-function `<module>`, so a flat
    900-line script is not exempt."""

    NEST = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With,
            ast.AsyncWith)

    def __init__(self):
        self.funcs = []          # (name, branches, nesting, lines)
        self.stack = []          # [name, branches, maxdepth, depth]
        if hasattr(ast, "TryStar"):
            self.NEST = self.NEST + (ast.TryStar,)

    def _enter(self, name, node):
        self.stack.append([name, 0, 0, 0])
        self.generic_visit(node)
        n, b, m, _ = self.stack.pop()
        length = (getattr(node, "end_lineno", node.lineno) - node.lineno + 1
                  if hasattr(node, "lineno") else 0)
        self.funcs.append((n, b, m, length))

    def visit_FunctionDef(self, node):
        self._enter(node.name, node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _branch(self, node, n=1, nest=True):
        if self.stack:
            self.stack[-1][1] += n
        if nest and self.stack:
            self.stack[-1][3] += 1
            self.stack[-1][2] = max(self.stack[-1][2], self.stack[-1][3])
            self.generic_visit(node)
            self.stack[-1][3] -= 1
        else:
            self.generic_visit(node)

    def generic_visit(self, node):
        for child in ast.iter_child_nodes(node):
            self.visit(child)

    def visit(self, node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return self._enter(node.name, node)
        if isinstance(node, ast.Try) or (hasattr(ast, "TryStar")
                                         and isinstance(node, ast.TryStar)):
            return self._branch(node, 1 + len(node.handlers))
        if isinstance(node, self.NEST):
            return self._branch(node)
        if isinstance(node, ast.IfExp):
            return self._branch(node, nest=False)
        if isinstance(node, ast.BoolOp):
            return self._branch(node, len(node.values) - 1, nest=False)
        if isinstance(node, ast.comprehension):
            return self._branch(node, 1 + len(node.ifs), nest=False)
        if hasattr(ast, "match_case") and isinstance(node, ast.match_case):
            return self._branch(node)
        return self.generic_visit(node)


def measure_python(text):
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError, RecursionError, MemoryError) as e:
        line = getattr(e, "lineno", None)
        return None, f"{type(e).__name__}" + (f" line {line}" if line else "")
    v = _PyVisit()
    v.stack.append(["<module>", 0, 0, 0])
    v.generic_visit(tree)
    n, b, m, _ = v.stack.pop()
    real = list(v.funcs)
    funcs = real + [(n, b, m, 0)]
    return _fold(funcs, real), "ast"


def _fold(funcs, real):
    """The measures out of (name, branches, nesting, lines) rows. `longest`
    is over real functions; the module pseudo-function has no length."""
    branching = max((f[1] for f in funcs), default=0)
    at = next((f[0] for f in funcs if f[1] == branching), "")
    nesting = max((f[2] for f in funcs), default=0)
    if real:
        longest = max(f[3] for f in real)
        lat = next((f[0] for f in real if f[3] == longest), "")
    else:
        longest, lat = None, ""
    return {"branching": branching, "branching_at": at, "nesting": nesting,
            "longest": longest, "longest_at": lat, "functions": len(real)}


def _spans(lines, language):
    """(name, start, end) per function, by the family's opening pattern and
    either brace depth or indentation. Never exact; close enough to say which
    function is long."""
    fam = BRANCH_FAMILY.get(language, "c")
    frx = FUNC_RE.get(fam)
    if frx is None:
        return []
    spans = []
    if fam in BRACE_FAMILIES:
        depth = 0
        open_ = []           # (name, start, depth before)
        for i, line in enumerate(lines):
            m = frx.match(line)
            code = re.sub(r"//.*$|#.*$", "", line) if fam != "c" else line
            opens = code.count("{")
            closes = code.count("}")
            if fam == "lua":
                opens = len(re.findall(r"\b(function|if|for|while|do|repeat)\b", code))
                closes = len(re.findall(r"\bend\b|\buntil\b", code))
                opens -= len(re.findall(r"\b(for|while)\b.*\bdo\b", code))
                opens -= len(re.findall(r"\bif\b.*\bthen\b.*\bend\b", code))
            if m:
                name = next((g for g in m.groups() if g), "?")
                open_.append((name, i, depth))
            depth += opens - closes
            while open_ and depth <= open_[-1][2] and i > open_[-1][1]:
                name, start, _ = open_.pop()
                spans.append((name, start, i))
        for name, start, _ in open_:
            spans.append((name, start, len(lines) - 1))
    else:
        starts = [(i, len(l) - len(l.lstrip()), next((g for g in frx.match(l).groups() if g), "?"))
                  for i, l in enumerate(lines) if frx.match(l)]
        for i, indent, name in starts:
            end = len(lines) - 1
            for j in range(i + 1, len(lines)):
                l = lines[j]
                if l.strip() and (len(l) - len(l.lstrip())) <= indent \
                        and not l.lstrip().startswith(("#", "end", "}")):
                    end = j - 1
                    break
            spans.append((name, i, end))
    return spans


def measure_heuristic(text, language):
    lines = text.splitlines()
    fam = BRANCH_FAMILY.get(language, "c")
    brx = re.compile(BRANCH_RE.get(fam, BRANCH_RE["c"]), re.M)
    spans = _spans(lines, language)
    covered = set()
    rows = []
    for name, s, e in spans:
        body = "\n".join(lines[s:e + 1])
        rows.append((name, len(brx.findall(body)), _nesting(lines[s:e + 1], fam),
                     e - s + 1))
        covered.update(range(s, e + 1))
    rest = [l for i, l in enumerate(lines) if i not in covered]
    mod = ("<module>", len(brx.findall("\n".join(rest))), _nesting(rest, fam), 0)
    return _fold(rows + [mod], rows)


def _nesting(lines, fam):
    """Max depth: brace depth for a brace family, indentation steps for the
    rest, relative to the shallowest line in the span."""
    if fam in BRACE_FAMILIES:
        depth, top = 0, 0
        for l in lines:
            code = re.sub(r"//.*$|#.*$", "", l)
            depth += code.count("{") - code.count("}")
            top = max(top, depth)
        return top
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    if not indents:
        return 0
    base = min(indents)
    unit = min((i - base for i in indents if i > base), default=4) or 4
    return max((i - base) // unit for i in indents)


def measure_markdown(text):
    lines = text.splitlines()
    heads = [i for i, l in enumerate(lines) if HEADING_RE.match(l)]
    if not heads:
        return {"branching": None, "branching_at": "", "nesting": None,
                "longest": len(lines), "longest_at": "", "functions": 0}
    bounds = heads + [len(lines)]
    longest, at = 0, ""
    for a, b in zip(bounds, bounds[1:]):
        if b - a > longest:
            longest, at = b - a, lines[a].lstrip("#").strip()[:40]
    return {"branching": None, "branching_at": "", "nesting": None,
            "longest": longest, "longest_at": at, "functions": len(heads)}


def measure(root, rel, language):
    """Every raw measure for one file, and how it was measured. Never raises:
    a file that cannot be read returns None and the caller counts it skipped."""
    path = os.path.join(root, rel)
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    m = {"lines": measure_lines(text), "method": "heuristic"}
    if language == "python":
        r, how = measure_python(text)
        if r is None:
            r = measure_heuristic(text, "python")
            m["method"] = f"heuristic (ast: {how})"
        else:
            m["method"] = "ast"
    elif language in DOCUMENT:
        r = measure_markdown(text)
        m["method"] = "sections"
    elif language in NO_BRANCHING:
        r = {"branching": None, "branching_at": "", "nesting": None,
             "longest": None, "longest_at": "", "functions": 0}
        m["method"] = "lines"
    else:
        r = measure_heuristic(text, language)
    m.update(r)
    if m["longest"] is None and language not in NO_BRANCHING:
        m["longest"] = m["lines"]           # no functions: the file is one
    return m


# ── the graph ────────────────────────────────────────────────────────────────

def load_graph(board):
    """{'commit', 'file_of', 'links'} from .pearde/graphify/graph.json, or
    None with a reason. Files are mapped through node `source_file` only —
    never through the id. Communities are not read: graphify clusters close
    to one per file, so "edges leaving the community" is every edge."""
    path = os.path.join(board, "graphify", "graph.json")
    if not os.path.isfile(path):
        return None, "no .pearde/graphify/graph.json"
    try:
        data = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"graph.json unreadable — {e}"
    if not isinstance(data, dict):
        return None, "graph.json is not an object"
    commit = str(data.get("built_at_commit") or "")[:7] or "unknown"
    file_of = {}
    for n in data.get("nodes") or []:
        if not isinstance(n, dict):
            continue
        sf = n.get("source_file")
        nid = n.get("id")
        if not sf or nid is None:
            continue
        sf = os.path.normpath(str(sf))
        file_of[nid] = sf
    links = [l for l in (data.get("links") or []) if isinstance(l, dict)]
    return {"commit": commit, "file_of": file_of, "links": links}, None


def graph_axes(graph, files):
    """{rel: {'fan_out','fan_in','links','callers','calls'}} over the scored
    set, or (None, reason) when the graph does not describe this tree."""
    want = set(files)
    known = {f for f in graph["file_of"].values() if f in want}
    if not known or len(known) * 2 < len(want):
        return None, (f"graph paths match {len(known)} of {len(want)} files "
                      "— built from another root?")
    calls, callers = {f: set() for f in want}, {f: set() for f in want}
    for l in graph["links"]:
        if l.get("relation") not in GRAPH_RELATIONS:
            continue
        sf = graph["file_of"].get(l.get("source"))
        if sf is None and l.get("source_file"):
            sf = os.path.normpath(str(l["source_file"]))
        tf = graph["file_of"].get(l.get("target"))
        if not sf or not tf or sf == tf or sf not in want or tf not in want:
            continue
        calls[sf].add(tf)
        callers[tf].add(sf)

    out = {}
    code = {f for f in known
            if LANG.get(os.path.splitext(f)[1].lower()) not in DOCUMENT}
    others = max(1, len(code) - 1)
    for f in want:
        if f not in known:
            out[f] = {"fan_out": None, "fan_in": None, "links": None,
                      "callers": [], "calls": []}
            continue
        wired = calls[f] | callers[f]
        out[f] = {"fan_out": len(calls[f]), "fan_in": len(callers[f]),
                  "links": round(len(wired) / others, 2),
                  "callers": sorted(callers[f]), "calls": sorted(calls[f])}
    return out, None


# ── scoring ──────────────────────────────────────────────────────────────────

def norm(v, lo, hi, scale):
    if v is None:
        return None
    if v <= lo:
        return 0.0
    if v >= hi:
        return 1.0
    if scale == "log":
        return (math.log(v) - math.log(lo)) / (math.log(hi) - math.log(lo))
    return (v - lo) / (hi - lo)


def badness(m, kind):
    """{axis: 0-1 or None}. None is an axis this file did not measure."""
    t = THRESHOLDS
    b = {"lines": norm(m.get("lines"), *t["lines"][kind])}
    if m.get("branching") is None:
        b["branching"] = None
    else:
        br = norm(m["branching"], *t["branch"])
        ne = norm(m.get("nesting") or 0, *t["nesting"])
        b["branching"] = 0.6 * br + 0.4 * ne
    b["longest"] = norm(m.get("longest"), *t["longest"][kind])
    b["fan_out"] = norm(m.get("fan_out"), *t["fan_out"])
    b["fan_in"] = norm(m.get("fan_in"), *t["fan_in"])
    b["links"] = norm(m.get("links"), *t["links"])
    return b


def score(m, kind, weights):
    """(score, badness, worst two axes)."""
    b = badness(m, kind)
    num = den = 0.0
    pull = {}
    for a in AXES:
        w = weights.get(a, 0)
        if b[a] is None or not w:
            continue
        num += w * b[a]
        den += w
        pull[a] = w * b[a]
    bad = num / den if den else 0.0
    s = max(1, min(100, round(100 * (1 - bad))))
    worst = [a for a, p in sorted(pull.items(), key=lambda kv: -kv[1]) if p > 0][:2]
    return s, b, worst


def _phrase(axis, m):
    at = lambda k: (f" in `{m[k]}`" if m.get(k) else "")
    if axis == "lines":
        return f"{m['lines']} lines"
    if axis == "branching":
        return (f"branching {m['branching']}{at('branching_at')} "
                f"(10 is the line, nesting {m.get('nesting')})")
    if axis == "longest":
        return f"longest {m['longest']} lines{at('longest_at')} (40 is the line)"
    if axis == "fan_out":
        return f"{m['fan_out']} files depended on (3 is the line)"
    if axis == "fan_in":
        return f"used by {m['fan_in']} files (2 is the line)"
    if axis == "links":
        return f"wired to {int(round(m['links'] * 100))}% of the graph's files (10% is the line)"
    return axis


def why(m, worst):
    if not worst:
        return "nothing pulls it down."
    return " and ".join(_phrase(a, m) for a in worst) + " pull it down."


# ── writing ──────────────────────────────────────────────────────────────────

def _val(v):
    if v is None:
        return "none"
    return str(v)


def note_text(rec):
    fm = ["---"]
    for k in NOTE_KEYS:
        if k == "worst":
            fm.append(f"worst: {' '.join(rec['worst'])}" if rec["worst"]
                      else "worst:")
        else:
            fm.append(f"{k}: {_val(rec.get(k))}")
    fm.append("---")
    body = [f"# {rec['file']} — {rec['score']}", "",
            why(rec, rec["worst"]), f"measured by {rec['method']}"]
    if rec["graph"] == "none":
        body.append("no graph — scored on lines, branching, longest")
    elif rec.get("fan_in") is None:
        body.append("not in the graph — scored on lines, branching, longest")
    else:
        for head, key in (("Callers", "callers"), ("Calls", "calls")):
            items = rec.get(key) or []
            body += ["", f"## {head}"]
            if not items:
                body.append("- none")
            for f in items[:30]:
                body.append(f"- {f}")
            if len(items) > 30:
                body.append(f"- … and {len(items) - 30} more")
    return "\n".join(fm + [""] + body) + "\n"


def ranking_text(recs, meta):
    fm = ["---"] + [f"{k}: {_val(meta.get(k))}" for k in RANK_KEYS] + ["---"]
    cols = "| score | file | language | lines | branching | longest | fan_in | fan_out | links | why |"
    sep = "|---|---|---|---|---|---|---|---|---|---|"
    rows = []
    for r in recs:
        s = f"**{r['score']}**" if r["score"] < meta["floor"] else str(r["score"])
        rows.append("| " + " | ".join([
            s, r["file"], _val(r.get("language")), _val(r.get("lines")),
            _val(r.get("branching")), _val(r.get("longest")),
            _val(r.get("fan_in")), _val(r.get("fan_out")), _val(r.get("links")),
            ", ".join(r["worst"]) or "—"]) + " |")
    head = ["# Health — worst first", "",
            f"{meta['files']} files scored, {meta['skipped']} skipped, "
            f"{meta['unhealthy']} under the floor of {meta['floor']}"
            + (f" · graph {meta['graph']}" if meta["graph"] != "none"
               else " · no graph, three axes"),
            ""]
    return "\n".join(fm + [""] + head + [cols, sep] + rows) + "\n"


def write_atomic(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def ensure_layout(board):
    """The directory and the ignore row. Returns what it did, as lines."""
    did = []
    files = os.path.join(out_dir(board), "files")
    if not os.path.isdir(files):
        os.makedirs(files, exist_ok=True)
        did.append(f"made {os.path.relpath(files)}/")
    gi = os.path.join(board, ".gitignore")
    if os.path.isdir(os.path.join(board, ".git")) or os.path.isfile(gi):
        text = _text(gi)
        have = {l.strip() for l in text.splitlines()}
        if f"{OUT_DIR}/" not in have:
            if text and not text.endswith("\n"):
                text += "\n"
            text += f"\n# rebuilt by `pearde health score`\n{OUT_DIR}/\n"
            write_atomic(gi, text)
            did.append(f"ignored {OUT_DIR}/ in {os.path.relpath(gi)}")
    return did


# ── reading the record back ──────────────────────────────────────────────────

def read_notes(board):
    """({rel: fm}, problems). Every wrong thing is a line, never a raise."""
    d = os.path.join(out_dir(board), "files")
    notes, problems = {}, []
    if not os.path.isdir(d):
        return notes, problems
    for name in sorted(os.listdir(d)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(d, name)
        rel = os.path.relpath(path)
        fm, _ = parse_fm(_text(path))
        if fm is None:
            problems.append(f"{rel}: no `---` frontmatter fence, or one unterminated")
            continue
        for k in NOTE_REQUIRED:
            if k not in fm:
                problems.append(f"{rel}: required key `{k}` missing")
        for k in fm:
            if k not in NOTE_KEYS:
                problems.append(f"{rel}: key `{k}` is not in the closed set — "
                                f"{', '.join(NOTE_KEYS)}")
        if fm.get("health") != "file":
            problems.append(f"{rel}: `health: {fm.get('health')}` — a note says `file`")
        try:
            s = int(fm.get("score", ""))
            if not 1 <= s <= 100:
                raise ValueError
        except ValueError:
            problems.append(f"{rel}: `score: {fm.get('score')}` is not an integer 1-100")
        for k in ("lines", "longest"):
            v = fm.get(k)
            if v not in (None, "none") and not v.isdigit():
                problems.append(f"{rel}: `{k}: {v}` is not an integer")
        if fm.get("date") and not ISO_RE.match(fm["date"]):
            problems.append(f"{rel}: `date: {fm['date']}` is not ISO 8601")
        f = fm.get("file", "")
        if f and slug(f) + ".md" != name:
            problems.append(f"{rel}: `file: {f}` slugs to {slug(f)}.md, not this name")
        if f in notes:
            problems.append(f"{rel}: a second note for {f}")
        notes[f or rel] = fm
    return notes, problems


def read_ranking(board):
    path = os.path.join(out_dir(board), "ranking.md")
    if not os.path.isfile(path):
        return None, []
    text = _text(path)
    fm, start = parse_fm(text)
    rel = os.path.relpath(path)
    if fm is None:
        return None, [f"{rel}: no `---` frontmatter fence, or one unterminated"]
    problems = []
    for k in RANK_KEYS:
        if k not in fm:
            problems.append(f"{rel}: required key `{k}` missing")
    for k in fm:
        if k not in RANK_KEYS:
            problems.append(f"{rel}: key `{k}` is not in the closed set — "
                            f"{', '.join(RANK_KEYS)}")
    rows = []
    for line in text.splitlines()[start:]:
        s = line.strip()
        if not s.startswith("|") or SEP_RE.match(s):
            continue
        c = [x.strip() for x in s[1:-1].split("|")]
        if len(c) < 10 or c[0] == "score":
            continue
        try:
            sc = int(c[0].strip("*"))
        except ValueError:
            problems.append(f"{rel}: a row whose score is `{c[0]}`")
            continue
        rows.append({"score": sc, "file": c[1], "language": c[2],
                     "why": c[9]})
    fm["rows"] = rows
    return fm, problems


def check(board):
    """One line per problem; empty when clean. `stale` lines are printed by
    `check` too, but do not count — they end in the command that clears them."""
    d = out_dir(board)
    if not os.path.isdir(d):
        return [], []
    root = repo_root(board)
    st = settings(board)
    problems = list(st["problems"])
    notes, p = read_notes(board)
    problems += p
    rank, p = read_ranking(board)
    problems += p
    tracked = set(tracked_files(root))
    for f in notes:
        if f not in tracked:
            problems.append(f"{OUT_DIR}/files/{slug(f)}.md: {f} is no longer tracked "
                            "— `pearde health score` drops it")
        elif skip_reason(root, f):
            problems.append(f"{OUT_DIR}/files/{slug(f)}.md: {f} is now skipped "
                            f"({skip_reason(root, f)}) — `pearde health score`")
    if notes and rank is None:
        problems.append(f"{OUT_DIR}/ranking.md missing while files/ holds "
                        f"{len(notes)} notes — `pearde health score`")
    notes_lines = []
    if rank is not None:
        try:
            n = int(rank.get("files", ""))
            if n != len(notes):
                problems.append(f"{OUT_DIR}/ranking.md: `files: {n}` but files/ holds "
                                f"{len(notes)} notes — `pearde health score`")
        except ValueError:
            pass
        for r in rank["rows"]:
            if r["file"] not in notes:
                problems.append(f"{OUT_DIR}/ranking.md: row for {r['file']} has no note")
        behind = commits_behind(root, rank.get("commit"))
        if behind is not None and behind > STALE_AFTER:
            notes_lines.append(f"stale: ranking is {behind} commits behind HEAD "
                               "— `pearde health score`")
        g, _ = load_graph(board)
        if g and rank.get("graph") not in (None, "none") \
                and g["commit"] != rank.get("graph"):
            notes_lines.append(f"stale: graph {g['commit']} is newer than the "
                               f"ranking's {rank.get('graph')} — `pearde health score`")
    return problems, notes_lines


# ── commands ─────────────────────────────────────────────────────────────────

def score_tree(board, paths=None, out=print):
    """Score every tracked file, or the tracked files under `paths`; write
    the notes, then rebuild the ranking from every note on disk."""
    root = repo_root(board)
    st = settings(board)
    for p in st["problems"]:
        out(p)
    ensure_layout(board)
    tracked = tracked_files(root)
    if paths:
        want = set()
        for p in paths:
            rp = os.path.normpath(os.path.relpath(os.path.abspath(p), root))
            want |= {f for f in tracked if f == rp or f.startswith(rp + os.sep)}
        subset = sorted(want)
    else:
        subset = tracked
    scored, skipped = [], 0
    for f in tracked:
        if skip_reason(root, f) is None:
            scored.append(f)
        else:
            skipped += 1
    graph, greason = load_graph(board)
    axes = None
    if graph:
        axes, areason = graph_axes(graph, scored)
        if axes is None:
            greason = areason
    gcommit = graph["commit"] if graph and axes else "none"
    today = datetime.date.today().isoformat()
    commit = head_commit(root) or "none"
    fdir = os.path.join(out_dir(board), "files")
    recs = []
    for f in scored:
        if f not in subset:
            continue
        lang = language_of(root, f)
        m = measure(root, f, lang)
        if m is None:
            skipped += 1
            continue
        m["language"] = lang
        m["file"] = f
        ga = (axes or {}).get(f, {"fan_out": None, "fan_in": None,
                                  "links": None, "callers": [], "calls": []})
        m.update(ga)
        kind = "document" if lang in DOCUMENT else "code"
        s, b, worst = score(m, kind, st["weights"])
        m.update({"score": s, "worst": worst, "health": "file", "date": today,
                  "commit": commit, "graph": gcommit})
        write_atomic(os.path.join(fdir, slug(f) + ".md"), note_text(m))
        recs.append(m)
        out(f"{s:>3}  {f}  {', '.join(worst) or '—'}")
    keep = set(scored)
    if not paths:
        for name in os.listdir(fdir):
            if name.endswith(".md") and name[:-3] not in {slug(f) for f in keep}:
                os.remove(os.path.join(fdir, name))
    notes, _ = read_notes(board)
    rows = []
    for f, fm in sorted(notes.items()):
        try:
            rows.append({"file": f, "score": int(fm.get("score", 0)),
                         "language": fm.get("language"),
                         "lines": fm.get("lines"), "branching": fm.get("branching"),
                         "longest": fm.get("longest"), "fan_in": fm.get("fan_in"),
                         "fan_out": fm.get("fan_out"), "links": fm.get("links"),
                         "worst": (fm.get("worst") or "").split()})
        except ValueError:
            continue
    rows.sort(key=lambda r: (r["score"], r["file"]))
    unhealthy = sum(1 for r in rows if r["score"] < st["floor"])
    meta = {"health": "ranking", "date": today, "commit": commit,
            "graph": gcommit, "files": len(rows), "skipped": skipped,
            "floor": st["floor"], "unhealthy": unhealthy}
    write_atomic(os.path.join(out_dir(board), "ranking.md"),
                 ranking_text(rows, meta))
    out(f"{len(recs)} scored · {len(rows)} on the ranking · {skipped} skipped · "
        f"{unhealthy} under {st['floor']} · graph {gcommit}"
        + (f" ({greason})" if gcommit == "none" and greason else ""))
    return 1 if st["problems"] else 0


def list_ranking(board, under=None, paths=None, out=print):
    rank, problems = read_ranking(board)
    if rank is None:
        out("no health record — `pearde health score` writes one")
        return 1
    root = repo_root(board)
    floor = settings(board)["floor"]
    limit = floor if under is None else under
    prefixes = []
    for p in paths or []:
        prefixes.append(os.path.normpath(os.path.relpath(os.path.abspath(p), root)))
    rows = [r for r in rank["rows"] if r["score"] < limit]
    if prefixes:
        rows = [r for r in rows if any(r["file"] == p or r["file"].startswith(p + os.sep)
                                       for p in prefixes)]
    for r in rows:
        out(f"{r['score']:>3}  {r['file']}  {r['why']}")
    return 0


def main(argv):
    args = list(argv[1:])
    under = None
    if "--under" in args:
        i = args.index("--under")
        if i + 1 >= len(args):
            print("health: --under needs a number", file=sys.stderr)
            return 2
        try:
            under = int(args[i + 1])
        except ValueError:
            print(f"health: --under {args[i + 1]} is not a number", file=sys.stderr)
            return 2
        args = args[:i] + args[i + 2:]
    board_arg = None
    if "--board" in args:
        i = args.index("--board")
        if i + 1 >= len(args):
            print("health: --board needs a path", file=sys.stderr)
            return 2
        board_arg = args[i + 1]
        args = args[:i] + args[i + 2:]
    cmd = args[0] if args else "check"
    rest = args[1:]
    if board_arg is None and rest and is_board(rest[-1]):
        board_arg = rest.pop()

    if cmd == "score":
        board = find_board(board_arg)
        return score_tree(board, rest or None)
    if cmd == "list":
        board = find_board(board_arg)
        return list_ranking(board, under, rest or None)
    if cmd == "show":
        if not rest:
            print("health: show <path> [board]", file=sys.stderr)
            return 2
        board = find_board(board_arg)
        root = repo_root(board)
        rel = os.path.normpath(os.path.relpath(os.path.abspath(rest[0]), root))
        path = os.path.join(out_dir(board), "files", slug(rel) + ".md")
        if not os.path.isfile(path):
            print(f"health: no note for {rel} — `pearde health score` writes one",
                  file=sys.stderr)
            return 1
        sys.stdout.write(_text(path))
        return 0
    if cmd == "check":
        if rest:
            print("health: check [board]", file=sys.stderr)
            return 2
        board = find_board(board_arg)
        problems, notes = check(board)
        for line in problems + notes:
            print(line)
        return 1 if problems else 0
    if cmd == "init":
        board = find_board(board_arg)
        did = ensure_layout(board)
        print("\n".join(did) if did else
              f"{os.path.relpath(out_dir(board))}/ already on this board")
        return 0
    print(__doc__.strip(), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
