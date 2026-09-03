#!/usr/bin/env python3
"""Every documented command, settings key and memo slug, against what exists.

    claims.py check [board]     one problem per line; silent when clean
    claims.py verbs             every `pearde <verb>` this repo answers
    claims.py keys              every settings and frontmatter key it honours

Documentation drifts one direction only: a name is renamed and the sentence
that named it stays. Nothing else in this repo notices — `index.py check`
reads paths, `memos.py check` reads the memos themselves, and a reference
telling a reader to run `pearde frobnicate` passes every one of them.

Three claims a document makes, and the three places that answer them:

    `pearde <verb>` in references/**/*.md     pearde.py FORWARD + discover()
    a `key:` named as settings or frontmatter  the registry in init.py
    `memos/<slug>.md` in resources/**/*.py     the board's own memos/

Each miss is one line naming `file:line`. The check runs one direction only:
something documented that does not exist. The reverse — a command with no
documentation — is a judgement rather than a defect, and is not reported.

Two things make a naive grep useless here, and both are handled:

  * **Prose is not a claim.** `the pearde board`, `pearde is not working` and
    `pearde already ships` are English, not commands. A claim is only read
    from a backtick span, a fenced block or a skill's `description:` — the
    three places this repo writes a command it means literally.
  * **A citation wraps.** A long memo slug breaks across lines in prose
    (`a-long-\\nslug.md`) and across a Python string concatenation
    (`"a-long-"\\n"slug.md"`). `fold` puts those back together and keeps the
    line each character came from, so the slug is found and still reported at
    the line it starts on.

A document that names a command on purpose that does not exist — a rejected
alternative, an example of drift — says so with `<!-- claims: ignore -->` on
the line or the line above it.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pearde_path  # noqa: E402

sys.path[:0] = pearde_path.dirs()
import common  # noqa: E402
import memos as memoslib  # noqa: E402

PROG = "claims"

IGNORE = "<!-- claims: ignore -->"

# The three places this repo writes something it means literally: a backtick
# span, a fenced block, and the `description:` of a skill's frontmatter —
# which is prose to a reader and a command list to the agent that fires on it.
SPAN_RE = re.compile(r"`([^`\n]+)`|^```[a-z]*\n(.*?)^```|^description:[ \t]*(.*)$",
                     re.M | re.S)

# Inside such a span: `pearde <verb>` or the slash form `/pearde <verb>`.
# `[ \t]` and not `\s` — a fenced block holding `grammar: pearde\nsubject: …`
# is two keys, not the command `pearde subject`.
CMD_RE = re.compile(r"(?:^|[\s\"'(])/?pearde[ \t]+([a-z][a-z-]*)")
# In a `description:` the surrounding text is prose about the board — `the
# pearde board`, `is pearde up to date`. Only the slash form is a command
# there, because that is the only form a person types at one.
SLASH_RE = re.compile(r"/pearde[ \t]+([a-z][a-z-]*)")

# A key claim: `` `key: value` `` written near the file it is claimed to live
# in. The window is what keeps the check honest — `state:`, `needs:` and
# `verify:` are backticked all over this repo and are not settings.
KEY_RE = re.compile(r"`([a-z][a-z0-9-]*):[^`]*`")
WINDOW = 140
SETTINGS_NEAR = "settings.md"
FRONTMATTER_DOC = os.path.join("references", "parts", "contract.md")

# A memo citation in code: any path ending `memos/<slug>.md`.
MEMO_RE = re.compile(r"memos/([a-z0-9][a-z0-9-]*)\.md")

DOC_ROOT = "references"
CODE_ROOT = "resources"


# ── reading files without losing the line ────────────────────────────────────

def walk(root, ext):
    """Every file under root with this extension, sorted, skipping the
    directories nothing in this repo authors."""
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in sorted(dirs)
                   if d not in ("__pycache__", "node_modules")
                   and not d.startswith(".")]
        out += [os.path.join(base, f) for f in sorted(files) if f.endswith(ext)]
    return out


def fold(text):
    """(folded text, line of each character). A hyphen at a line end joins to
    the next line, dropping the whitespace, quotes and comment marks between —
    which is how a long slug wraps in prose and in a Python string. Every
    other newline stays, so a match still reports the line it started on."""
    out, lines, line, i, n = [], [], 1, 0, len(text)
    while i < n:
        c = text[i]
        if c == "-":
            j = i + 1
            while j < n and text[j] in " \"'#":
                j += 1
            if j < n and text[j] == "\n":
                j += 1
                while j < n and text[j] in " \"'#":
                    j += 1
                out.append("-")
                lines.append(line)
                line += 1
                i = j
                continue
        out.append(c)
        lines.append(line)
        line += 1 if c == "\n" else 0
        i += 1
    return "".join(out), lines


def exempt(text, pos):
    """Is the line at pos, or the line above it, marked `<!-- claims: ignore -->`?"""
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    here = text[start:end if end >= 0 else len(text)]
    above = text[text.rfind("\n", 0, start - 1) + 1:start] if start else ""
    return IGNORE in here or IGNORE in above


# ── what exists ──────────────────────────────────────────────────────────────

def verbs(root):
    """Every name `pearde <name>` answers: the forwarded ones, the ones
    discovery finds under resources/, and `help`. Read from pearde.py rather
    than from `pearde help`'s printed lines — the printed form wraps and
    elides, and a check reading a rendering is a check on the renderer."""
    sys.path.insert(0, os.path.join(root, CODE_ROOT))
    import pearde as cli
    found, _ = cli.discover()
    return set(cli.FORWARD) | set(found) | {"help"}


def _registry(root, name):
    """A `NAME = (...)` tuple of bare strings out of init.py, without
    importing it — init.py writes files, and a checker must not.

    The closing paren is found by counting, not by a pattern: `DEFAULTS` ends
    on `("happiness", "0"))` and `SETTING_KEYS` on `"machine-ceiling")`, so
    neither a `^\\)` line nor the first `\\)$` marks the end of either. A regex
    guessing at it swallows the rest of the file and calls every quoted word
    in it a settings key."""
    src = common.read_text(os.path.join(root, CODE_ROOT, "board", "init.py"))
    m = re.search(r"^%s\s*=\s*\(" % name, src, re.M)
    if not m:
        return set()
    i, depth = m.end(), 1
    while i < len(src) and depth:
        depth += (src[i] == "(") - (src[i] == ")")
        i += 1
    return set(re.findall(r'["\']([a-z][a-z0-9-]*)["\']', src[m.end():i - 1]))


def keys(root):
    """(settings keys, frontmatter keys) — the closed sets the board honours,
    read off init.py. `DEFAULTS` is what `pearde init` writes and is a subset:
    a key with no printed default is honoured all the same, and the registry
    is what says so."""
    settings = _registry(root, "SETTING_KEYS") | _registry(root, "DEFAULTS")
    return settings, _registry(root, "FRONTMATTER_KEYS")


# ── the three checks ─────────────────────────────────────────────────────────

def bad_verbs(root):
    known, bad = verbs(root), []
    for path in walk(os.path.join(root, DOC_ROOT), ".md"):
        rel, text = os.path.relpath(path, root), common.read_text(path)
        for m in SPAN_RE.finditer(text):
            span = m.group(1) or m.group(2) or m.group(3) or ""
            if exempt(text, m.start()):
                continue
            line = text.count("\n", 0, m.start()) + 1
            rx = SLASH_RE if m.group(3) else CMD_RE
            for c in rx.finditer(span):
                if c.group(1) not in known:
                    bad.append(f"{rel}:{line}: `pearde {c.group(1)}` — no such command")
    return bad


def bad_keys(root):
    settings, frontmatter = keys(root)
    bad = []
    for path in walk(os.path.join(root, DOC_ROOT), ".md"):
        rel, text = os.path.relpath(path, root), common.read_text(path)
        flat = text.replace("\n", " ")
        for m in KEY_RE.finditer(flat):
            key = m.group(1)
            near = flat[max(0, m.start() - WINDOW):m.end() + WINDOW]
            line = text.count("\n", 0, m.start()) + 1
            if exempt(text, m.start()):
                continue
            if rel == FRONTMATTER_DOC:
                if key not in frontmatter and key not in settings:
                    bad.append(f"{rel}:{line}: `{key}:` — no frontmatter key of that name")
            elif SETTINGS_NEAR in near and key not in settings:
                if key in frontmatter:
                    continue
                bad.append(f"{rel}:{line}: `{key}:` — no settings key of that name")
    return bad


def bad_memos(root, board):
    known = set(memoslib.scan(board)) if board else set()
    bad = []
    for path in walk(os.path.join(root, CODE_ROOT), ".py"):
        if os.path.basename(path) == os.path.basename(__file__):
            continue
        rel = os.path.relpath(path, root)
        text, lines = fold(common.read_text(path))
        for m in MEMO_RE.finditer(text):
            if m.group(1) not in known:
                bad.append(f"{rel}:{lines[m.start(1)]}: memo "
                           f"`{m.group(1)}` — no such memo on this board")
    return bad


def check(root, board):
    """Every problem, one string each. Empty means nothing documented has
    drifted from what exists."""
    return bad_verbs(root) + bad_keys(root) + bad_memos(root, board)


def main(argv):
    verb = argv[0] if argv else "check"
    rest = argv[1:]
    root = pearde_path.skill_root()
    if verb == "verbs":
        print("\n".join(sorted(verbs(root))))
        return 0
    if verb == "keys":
        s, f = keys(root)
        print("\n".join(f"settings  {k}" for k in sorted(s)))
        print("\n".join(f"frontmatter  {k}" for k in sorted(f)))
        return 0
    if verb != "check":
        print(f"{PROG}: unknown verb {verb}", file=sys.stderr)
        return 2
    problems = check(root, common.find_board(rest[0] if rest else None, PROG))
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
