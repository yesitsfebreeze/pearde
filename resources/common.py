#!/usr/bin/env python3
"""pearde common — what every board reader beside the planner shares.

    find_board(arg, prog)          the board `arg` names, or the one above the cwd
    split_frontmatter(text)        (fm, first body line) in the board's dialect
    parse_frontmatter(text)        (fm, title, body) — the same, with the `# ` title cut out
    atomic_write(path, text)       tmp + os.replace, so a reader never sees half a file
    set_list_key(text, key, items) the `key:` block rewritten as `- item` lines
    read_text(path)                the text, or "" when it cannot be read
    pop_flag(argv, name)           (value, rest) for one `--flag value`
    Collection                     a directory of `<slug>.md` records under the board
    prd_shape(dir)                 one PRD's (fm, title, body, specs, children, problems)
    run_git(root, *args, ...)      one `git -C root ...`, shaped to each caller's own return-or-raise
    section(text, name, ...)       the body under `## <name>`, shaped to each caller's own match and shape

Stdlib only, and it imports nothing from @resources/board/: memos.py stands
on this file and @resources/board/plan.py imports memos.py, so a link back
would close a circle. The resolver is the planner's, kept as a copy for the
reason @resources/guard.py gives — a reader keeps its own error prefix
(`prog`) and does not depend on the planner to find a board.
"""
import os
import re
import subprocess
import sys

# ── the board ────────────────────────────────────────────────────────────────

# The board's directory, at the project root. `pearde` is the visible name
# it carried on 2026-09-02, still found so a board that never moved back
# keeps working — @resources/board/plan.py spells the same pair.
BOARD_DIR = ".pearde"
LEGACY_BOARD_DIR = "pearde"
BOARD_DIRS = (BOARD_DIR, LEGACY_BOARD_DIR)
# The board's directory name is configurable, and a directory holding
# `settings.md` is how it is configured — `named_boards`. These names are
# never a board and are skipped unstatted; everything hidden is skipped by
# the dot rule.
SCAN_SKIP = frozenset(("node_modules", "target", "vendor", "__pycache__",
                       "build", "dist"))


def is_board_dir(p):
    """A directory is a board only when it CARRIES one — `settings.md`, or a
    `prds/`. The name alone is not proof: `pearde` is an ordinary word, and a
    folder called that beside a real board would shadow it."""
    return os.path.isdir(p) and (
        os.path.isfile(os.path.join(p, "settings.md"))
        or os.path.isdir(os.path.join(p, "prds")))


def board_link(p):
    """A board reached through a compatibility symlink is not called what
    the link is called — the directory it points at is. One level, resolved
    beside the link, never `realpath`, so a symlinked ANCESTOR stays spelled
    the way the caller spelled it."""
    if not os.path.islink(p):
        return p
    return os.path.normpath(os.path.join(os.path.dirname(p), os.readlink(p)))


def named_boards(d):
    """Immediate children of `d` carrying `settings.md` — how a board called
    neither `.pearde` nor `pearde` is found, and the whole of the
    board-directory configuration: renaming the directory is the only act
    that configures it. At most two come back, because one is the answer
    and two is a refusal."""
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
    """`<d>/.pearde`, or `<d>/pearde` when only that carries a board — the
    two names the tool knows, either read through its compat symlink."""
    for name in BOARD_DIRS:
        p = os.path.join(d, name)
        if is_board_dir(p):
            return board_link(p)
    return None


def board_scanned(d, prog):
    """The board of `d` that is called something else — one immediate child
    holding `settings.md`, and a refusal when there are two."""
    found = named_boards(d)
    if len(found) > 1:
        sys.exit(f"{prog}: two directories under {d} carry a board — "
                 f"{os.path.basename(found[0])}/ and "
                 f"{os.path.basename(found[1])}/; a project has one board, "
                 "so rename or remove one of them")
    return found[0] if found else None


def board_in(d, prog):
    """The board inside project dir `d` — the named one, then the scanned
    one. The answer for a directory a caller pointed at deliberately."""
    return board_named(d) or board_scanned(d, prog)


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


def board_above(d, prog):
    """The board `d` belongs to — two passes, a named board winning at any
    depth over a discovered one nearer the cwd. @resources/board/plan.py
    `board_above` says why discovery cannot be part of the climb."""
    return walk_up(d, board_named) or walk_up(d, lambda p: board_scanned(p, prog))


def find_board(arg, prog):
    """The board `arg` names — the board itself, a project holding one, or a
    board under any name — else the one above the cwd. Every refusal is
    `sys.exit` with `prog:` in front, the way each tool's other refusals
    read."""
    if arg:
        p = os.path.abspath(arg)
        if os.path.basename(p) in BOARD_DIRS and is_board_dir(p):
            return board_link(p)
        b = board_in(p, prog)
        if b:
            return b
        # the board named directly, under whatever it is called — asked last,
        # so a project holding one still resolves to the board inside it
        if os.path.isfile(os.path.join(p, "settings.md")):
            return p
        sys.exit(f"{prog}: no {BOARD_DIR}/ board at {arg}")
    b = board_above(os.getcwd(), prog)
    if b:
        return b
    sys.exit(f"{prog}: no {BOARD_DIR}/ board found walking up from the cwd")


# ── the board's dialect ──────────────────────────────────────────────────────

# Byte-rule for byte-rule what prd.md uses: a `---` fence, one `key: value`
# per line, `- item` for lists, `#` comments.
KEY_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")
ITEM_RE = re.compile(r"^\s*-\s+(.*?)\s*$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _clean(v):
    # `^` as well as `\s+`: a value that is ONLY a comment (`est:   # the
    # weight, only when complexity is absent` — a key's line whose value is
    # nothing but a trailing note) already had its leading spaces eaten by
    # the caller's key/value split, so the comment sits at position 0 of
    # `v` with nothing before it to match `\s+#`. Left unanchored at the
    # start, that reads as a value rather than an absent one — measured
    # against @resources/board/prdfile.py `strip_comment`, the reader this
    # unifies with, which carried the fix first.
    return re.sub(r"(^|\s+)#.*$", "", v).strip().strip("\"'")


def split_frontmatter(text, lists=True):
    """(frontmatter, first body line index). frontmatter is None when the
    fence is missing or unterminated — the caller reports that, it is not a
    crash. With `lists`, a bare `key:` opens a list the `- item` lines under
    it fill; without, every value is the string on the key's line and an
    item line is skipped — the grammar and the health record are scalar
    formats and read themselves that way."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    fm, key = {}, None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fm, i + 1
        if line.lstrip().startswith("#"):
            continue
        if lists:
            m = ITEM_RE.match(line)
            if m and key is not None:
                if not isinstance(fm.get(key), list):
                    fm[key] = []
                fm[key].append(_clean(m.group(1)))
                continue
        m = KEY_RE.match(line)
        if m:
            key = m.group(1)
            v = _clean(m.group(2))
            fm[key] = v if v or not lists else []
    return None, 0


def parse_frontmatter(text, lists=True):
    """(frontmatter, title, body): the first `# ` line after the fence is
    the title, the rest the body, stripped. (None, "", text) when there is
    no closed fence."""
    fm, start = split_frontmatter(text, lists)
    if fm is None:
        return None, "", text
    title, body = "", []
    for line in text.splitlines()[start:]:
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue
        body.append(line)
    return fm, title, "\n".join(body).strip()


def read_text(path, errors="replace"):
    """The file's text, or "" when it cannot be read — a reader that lists
    problems never raises on one file."""
    try:
        return open(path, encoding="utf-8", errors=errors).read()
    except OSError:
        return ""


# ── one PRD's shape ──────────────────────────────────────────────────────────

def prd_shape(dir_path):
    """One PRD directory read whole: (fm, title, body, specs, children,
    problems).

    specs is `[(name, fm, title, body), ...]` for every `<name>.md` directly
    under `specs/`, name order. children is the sorted basenames of every
    immediate subdirectory that itself holds a `prd.md` — a parked or
    container child, never a grandchild. problems is every way the shape
    was short of whole, as one sentence each: `prd.md`'s fence did not
    close, it closed with no `state:` key, or a spec's fence did not close.

    This is the reading four modules did four ways before: facts and
    problems only, nothing here decides a transition, a gate or a spec's
    completeness — that is `plan.dispatchable`'s and `specs.check_spec`'s,
    unmoved. The board scan's mtime cache sits in front of this, keyed on
    the file it reads; this is what a cache miss calls."""
    path = os.path.join(dir_path, "prd.md")
    fm, title, body = parse_frontmatter(read_text(path))
    problems = []
    if fm is None:
        problems.append(f"{path}: no closed `---` frontmatter fence")
        fm = {}
    elif not fm.get("state"):
        problems.append(f"{path}: no `state:` key")

    specs = []
    sdir = os.path.join(dir_path, "specs")
    for f in sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []:
        if not f.endswith(".md"):
            continue
        spath = os.path.join(sdir, f)
        sfm, stitle, sbody = parse_frontmatter(read_text(spath))
        if sfm is None:
            problems.append(f"{spath}: no closed `---` frontmatter fence")
            sfm = {}
        specs.append((f[:-3], sfm, stitle, sbody))

    children = sorted(
        n for n in (os.listdir(dir_path) if os.path.isdir(dir_path) else [])
        if os.path.isfile(os.path.join(dir_path, n, "prd.md")))

    return fm, title, body, specs, children, problems


def atomic_write(path, text):
    """Written beside, then renamed over: a reader sees the old file or the
    new one, never a partial."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def set_list_key(text, key, items, after=None):
    """`text` with its `key:` block rewritten to `items`, one `  - item` line
    each; written after the `after:` line when it has none, else before the
    closing fence. Returns (text, changed). Frontmatter only — the fence is
    the first `---` and the next one, and a body line reading `key: …` is
    prose, not a key. A block list and not `[a, b]`: `split_frontmatter`
    reads `- item` lines and would hand a checker one string with brackets
    in it."""
    want = [f"{key}:"] + [f"  - {t}" for t in items]
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text, False
    end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if end is None:
        return text, False
    at = next((i for i in range(1, end) if lines[i].startswith(f"{key}:")), None)
    if at is not None:
        stop = at + 1
        while stop < end and ITEM_RE.match(lines[stop]):
            stop += 1
        if lines[at:stop] == want:
            return text, False
        lines[at:stop] = want
    else:
        pos = end
        if after:
            a = next((i for i in range(1, end)
                      if lines[i].startswith(f"{after}:")), None)
            if a is not None:
                pos = a + 1
        lines[pos:pos] = want
    return "\n".join(lines) + ("\n" if text.endswith("\n") else ""), True


def pop_flag(argv, name):
    """(value, rest) — `--name value` taken out of `argv`, value None when
    the flag is absent. Raises ValueError when the flag is the last word;
    the caller prints its own refusal, since what the flag needs (a value,
    a number, a path) is the caller's to say."""
    args = list(argv)
    if name not in args:
        return None, args
    i = args.index(name)
    if i + 1 >= len(args):
        raise ValueError(name)
    return args[i + 1], args[:i] + args[i + 2:]


# ── a directory of records ───────────────────────────────────────────────────

class Collection:
    """A directory of `<slug>.md` records under the board — `memos/`,
    `workflows/` — located through one `settings.md` key, read as one dict,
    and checked for what every such record shares: a closed fence, the
    required keys present, no key outside the closed set, the slug key
    agreeing with the filename, ISO dates, `updated` no earlier than `date`.
    `external` says the key pointed elsewhere — another system's records,
    or a library several boards share; what that exempts is the caller's."""

    def __init__(self, board, settings_key, default_dir, required, optional,
                 index_name="README.md", noun=None):
        self.board = board
        self.settings_key = settings_key
        self.required, self.optional = tuple(required), tuple(optional)
        self.index_name = index_name
        self.noun = noun or settings_key.rstrip("s")
        self.dir, self.external = self._locate(default_dir)

    def _locate(self, default_dir):
        st = os.path.join(self.board, "settings.md")
        if os.path.isfile(st):
            fm, _, _ = parse_frontmatter(read_text(st))
            v = (fm or {}).get(self.settings_key)
            if v and not isinstance(v, list):
                return os.path.normpath(os.path.join(self.board, v)), True
        return os.path.join(self.board, default_dir), False

    def scan(self):
        """{slug: entry} in filename order — the index file skipped, so it
        is never itself a record. An entry is slug, path, fm ({} when the
        file did not parse), parsed, title (the slug when the file has none)
        and body; a caller adds the keys its own format names."""
        if not os.path.isdir(self.dir):
            return {}
        out = {}
        for f in sorted(os.listdir(self.dir)):
            if not f.endswith(".md") or f == self.index_name:
                continue
            path = os.path.join(self.dir, f)
            fm, title, body = parse_frontmatter(
                open(path, encoding="utf-8").read())
            slug = f[:-3]
            out[slug] = {"slug": slug, "path": path, "fm": fm or {},
                         "parsed": fm is not None, "title": title or slug,
                         "body": body}
        return out

    @staticmethod
    def check_fence(entry):
        if entry["parsed"]:
            return []
        return [f"{entry['slug']}.md: no closed `---` frontmatter fence"]

    def check_keys(self, entry, slug_key=None, closed=True):
        """The required keys present; with `closed`, nothing outside the set
        and the slug key agreeing with the filename."""
        fm, at, bad = entry["fm"], f"{entry['slug']}.md", []
        for k in self.required:
            if not fm.get(k):
                bad.append(f"{at}: missing `{k}:`")
        if not closed:
            return bad
        for k in fm:
            if k not in self.required + self.optional:
                bad.append(f"{at}: `{k}:` is not a {self.noun} key — "
                           "a misspelled key reads as present")
        if slug_key and fm.get(slug_key) and fm[slug_key] != entry["slug"]:
            bad.append(f"{at}: `{slug_key}: {fm[slug_key]}` disagrees with "
                       "the filename")
        return bad

    @staticmethod
    def check_dates(entry):
        fm, at, bad = entry["fm"], f"{entry['slug']}.md", []
        date, upd = str(fm.get("date") or ""), str(fm.get("updated") or "")
        if date and not ISO_RE.match(date):
            bad.append(f"{at}: date `{date}` is not ISO 8601 (YYYY-MM-DD)")
        if upd and not ISO_RE.match(upd):
            bad.append(f"{at}: updated `{upd}` is not ISO 8601 (YYYY-MM-DD)")
        elif upd and ISO_RE.match(date or "") and upd < date:
            bad.append(f"{at}: updated {upd} precedes date {date}")
        return bad

    def check_common(self, entry, slug_key=None):
        """Every shared check, in order; a fence that did not close is the
        only line, since nothing under it was read."""
        bad = self.check_fence(entry)
        if bad:
            return bad
        return self.check_keys(entry, slug_key) + self.check_dates(entry)

    def write(self, name, text):
        """`<dir>/<name>` written atomically, the directory made; returns
        the path. Refusing an external dir is the caller's — the refusal
        names the caller's own key."""
        os.makedirs(self.dir, exist_ok=True)
        path = os.path.join(self.dir, name)
        atomic_write(path, text)
        return path


# ── one git runner ───────────────────────────────────────────────────────────

_UNSET = object()


def run_git(root, *args, check=False, default=_UNSET, raise_as=None,
             timeout=60, input=None, env=None, stdout=False, strip=False,
             msg=None):
    """`git -C root <*args>`, both streams captured as text.

    A failure is git not found or the call timing out, or — when `check`
    — a non-zero exit. A failure raises `raise_as(message)` when one is
    given; else it returns `default` when one was passed (even `None` —
    pass nothing to mean "no default"); else a process-level failure is
    re-raised as it came, and a checked non-zero exit with neither becomes
    `RuntimeError(message)` — a combination no caller in this tree uses,
    since every `check=True` caller here also names its own `raise_as`.
    `msg(args, root, completed_or_exc)` builds the failure text when a
    caller's own wording (a prefix naming the root, the failed subcommand)
    is part of its contract; the default is the stripped stderr, or stdout
    when stderr is empty, or `git <args> exit <code>` when both are.

    Success returns the `CompletedProcess` — `.stdout` and `.returncode`
    are the caller's to read, the shape a caller that inspects the exit
    code itself wants (an unchecked non-zero exit is still success here).
    `stdout=True` returns `.stdout` directly instead (`.strip()`ped when
    `strip`), the shape a caller that never reads `.returncode` wants in
    one line.
    """
    def fail(built):
        if raise_as:
            raise raise_as(built)
        if default is not _UNSET:
            return default
        raise RuntimeError(built)

    try:
        r = subprocess.run(("git", "-C", root) + tuple(args),
                           capture_output=True, text=True, timeout=timeout,
                           input=input, env=env)
    except (OSError, subprocess.TimeoutExpired) as e:
        if msg:
            return fail(msg(args, root, e))
        if raise_as:
            raise raise_as(f"git {' '.join(args)}: {e}") from e
        if default is not _UNSET:
            return default
        raise
    if check and r.returncode != 0:
        built = msg(args, root, r) if msg else (
            (r.stderr or r.stdout).strip()
            or f"git {' '.join(args)} exit {r.returncode}")
        return fail(built)
    if stdout:
        out = r.stdout
        return out.strip() if strip else out
    return r


# ── one section extractor ────────────────────────────────────────────────────

_H2_RE = re.compile(r"(?m)^##\s+(.*?)\s*$")


def _h2_spans(text):
    """[(heading text, body start, body end)] for every `## ` line in
    `text`, in order — a body runs from the end of its heading's line
    (before its newline, so the body carries it) to the start of the next
    `## ` line, or the end of the text."""
    heads = list(_H2_RE.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append((m.group(1), m.end(), end))
    return out


def section(text, name, *, all=False, lines=False, prefix=False, word=False,
             ci=True, heading=False, chomp=False, default=None):
    """The body under `## <name>`, up to the next `## ` line — every
    caller here reads the same shape of file, and differs only in how
    loosely `name` matches and how the answer comes back.

    `name` is matched against a heading's text (the line after `## `,
    trailing space trimmed): as the whole line unless `prefix`, in which
    case a heading matches when it *starts with* `name` — `word` then
    requires the character after the shared prefix to end a word, so
    `"Questions"` does not match a heading spelled `"Questionable"`.
    Matched case-insensitively unless `ci=False`. `name` may instead be a
    compiled pattern, matched with `.match()` against the heading text —
    the arbitrary-heading case no string mode reaches.

    The body carries the newline that ends the heading's own line — the
    same substring `text[m.end():next]` a plain regex search on the board's
    dialect gets. `chomp` drops that one leading newline instead (a reader
    that partitions the heading off `name`'s own line never sees it either
    way); `lines` implies `chomp` and splits what is left on the rest.

    One match (the default): the first hit's body — a string, or its lines
    when `lines` — or `default` when nothing matched. `all=True`: every
    hit, in file order, as a list — `[]` when nothing matched, `default`
    unused. `heading=True`: each body comes back as `(heading, body)`
    instead of bare `body`, in both shapes.
    """
    def match(h):
        if hasattr(name, "match"):
            return bool(name.match(h))
        a, b = (h, name) if ci is False else (h.lower(), name.lower())
        if not prefix:
            return a == b
        if not a.startswith(b):
            return False
        return not word or len(a) == len(b) or not (
            a[len(b)].isalnum() or a[len(b)] == "_")

    def shape(h, body):
        if (chomp or lines) and body.startswith("\n"):
            body = body[1:]
        body = body.splitlines() if lines else body
        return (h, body) if heading else body

    hits = [shape(h, text[s:e]) for h, s, e in _h2_spans(text) if match(h)]
    if all:
        return hits
    return hits[0] if hits else default
