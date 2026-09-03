#!/usr/bin/env python3
"""The loop's guard — the rules in @references/parts/loop.md, enforced.

    guard.py pre     PreToolUse  — reads the hook payload on stdin, allows or denies
    guard.py post    PostToolUse — reminds the pass to write down what it just moved
    guard.py check   prints what the guard would say about the board it is run in
    guard.py on [<repo>]      writes the hooks block into <repo>/.claude/settings.json —
                              the three guard hooks and the SessionStart hook
                              that brings the board's view up
    guard.py off [<repo>]     removes exactly what `on` wrote, nothing else
    guard.py status [<repo>]  doctor's guard row alone — exit 0 ok, 1 off, 2 broken

A sentence in a reference file is advice. This is the same sentence as a
mechanism: the three ways the 2026-08-27 pass burned 318,584 tokens are the
three things it refuses.

    a hand-walked board          → `plan.py scan` says it in one call
    the same board read twice    → nothing changed since; the answer is unchanged
    the manual read three times  → it has not moved; the pass file is the note
    a state moved, nothing written → `.pearde/.state/pass.md` survives a compaction
    a `state:` written by hand   → `pearde set` checks the gate; an editor checks nothing
    the skill written from another board → the install is links into this tree; file a PRD here

It denies only what is provably redundant: a repeat whose inputs have not
changed since the first run. Everything else passes through untouched, and a
board it cannot find is not its business.
"""
import hashlib
import json
import os
import re
import sys
import time

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402 — @resources/pearde_path.py, the one rule
try:
    import quiet  # noqa: E402 — @resources/board/quiet.py, stdlib-only; a broken module denies nothing
except Exception:
    quiet = None

ROOT = pearde_path.RES                  # the skill's resources/
PEARDE = pearde_path.skill_root(__file__) or os.path.dirname(ROOT)
# One JSON file per session, in the board's own corner:
# `<board>/.state/guard/<session>.json`. The install is not a place this tool
# writes — the invariant `every-artifact-lands-inside-the-board` — so there is
# no machine-wide cache and no path that is not relative to a `.pearde/`.
# `PEARDE_GUARD_STATE` moves the directory for the writer here and the reader
# in @resources/board/plan.py both: a harness feeding hook JSON to a temp
# project must never write into a real board.
GUARD_STATE_ENV = "PEARDE_GUARD_STATE"
# Duplicated from @resources/board/plan.py's own BOARD_DIR/PRDS_DIR rather
# than imported — same reason member_dirs() gives for reading settings.md by
# hand: the guard imports nothing from the planner, so a broken planner
# never blocks a tool call.
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
PRDS_DIR = "prds"
PASS_FILE = os.path.join(".state", "pass.md")

# The context budget. A pass costs its context on every turn: 1,000 turns at
# 500k is half a billion cache-read tokens for a session whose unique content
# was 500k once. The orchestrator is meant to be slim — the board is on disk
# and `.pearde/.state/pass.md` is what it carries — so the budget is a
# ceiling, not a window. `context-budget` in .pearde/settings.md moves it;
# `off` removes it.
#
# It is measured from the session's own floor, never from zero. A window opens
# already holding the system prompt, the tool schemas, the project's CLAUDE.md
# and the skill — 50,229 tokens on the /pearde session of 2026-09-01, before
# the pass had done anything at all. Measured absolutely, half the budget was
# spent on the first turn and the ceiling fired on a pass that had read one
# scan. `floor` is the smallest window this session has been billed for, and
# the budget is what the pass grew on top of it.
BUDGET_DEFAULT = 100_000
BUDGET_WARN = 0.70          # note once at 70%, once at 85%
BUDGET_KEY = re.compile(r"^context-budget:[ \t]*(\S+)", re.M)
# What stays allowed at the ceiling — everything the handover itself needs.
ESCAPE = re.compile(r"\.pass\.md$|/(loop|pass|dispatch)\.md$")

# The manual does not change mid-pass, so a repeat read of one of its files
# returns the bytes already in the window. These two are the exception:
# @references/parts/pass.md sends a compacted pass back to the steps, and
# that has to stay possible however often it happens.
REREADABLE = {"loop.md", "pass.md", "dispatch.md"}
MANUAL = ("references" + os.sep, "skills" + os.sep)

# The scan the guard offers instead of a hand walk. plan.py is found under
# resources/, never spelled — @resources/pearde_path.py `script`.
SCAN = "python3 %s scan" % (pearde_path.script("plan.py") or "plan.py")

# The board's own tools write through edit.py and are never refused — a
# transition repeated is a different board, and a refused one costs nothing.
# `resources/<dir>/<mod>.py` matches wherever a module lands: the directory
# is a wildcard, so a file that moves stays recognised as one of ours.
TOOLS = re.compile(r"\b(pearde|plan|guard)\.py\b|resources/\w+/\w+\.py")
STATE_RE = re.compile(r"^state:[ \t]*(.*?)[ \t]*$", re.M)

# A board walked by hand. `find … prd.md`, `grep -r state:`, `ls prds/*/prd.md`
# — every spelling of the sweep step 1 stopped asking for.
WALKS = (
    re.compile(r"\bfind\b[^|;&]*\bprd\.md\b"),
    re.compile(r"\bgrep\b[^|;&]*(-\w*r\w*)[^|;&]*\bstate:"),
    re.compile(r"\bls\b[^|;&]*\bprds/[^|;&]*\*"),
)

# A walk carried as data is not a walk. The shell never runs a heredoc body
# or the inside of a quoted string — a script piped to python, a fixture, a
# refusal quoted into a memo. It does run the string a walker itself takes
# (`grep -r 'state:'`) and the one `sh -c` is given. `data_free` returns the
# command with the data blanked, and the WALKS rules match on that.
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n(.*?)\n\2[ \t]*(?=\n|$)",
                     re.S)
RUNS_ITS_STRING = {"find", "grep", "rg", "ls", "sh", "bash", "zsh", "eval"}


def data_free(cmd):
    """`cmd` with heredoc bodies and quoted strings blanked, except a string
    given to a command that runs it."""
    cmd = HEREDOC.sub(lambda m: m.group(0)[:m.start(3) - m.start(0)]
                      + "\n" + m.group(2), cmd)
    out, i, n, word = [], 0, len(cmd), ""
    at_start = True
    while i < n:
        c = cmd[i]
        if c in "|;&\n":
            at_start, word = True, ""
            out.append(c); i += 1
            continue
        if c in "'\"":
            j = i + 1
            while j < n and cmd[j] != c:
                j += 2 if (c == '"' and cmd[j] == "\\") else 1
            keep = word in RUNS_ITS_STRING
            out.append(cmd[i:j + 1] if keep else " ")
            i = j + 1
            continue
        if at_start and not c.isspace():
            m = re.match(r"[\w./-]+", cmd[i:])
            tok = m.group(0) if m else c
            if m and cmd[i + len(tok):i + len(tok) + 1] == "=":
                m = re.match(r"\S+", cmd[i:])      # `X=1` — a prefix, whole
                out.append(m.group(0)); i += len(m.group(0))
                continue
            word = os.path.basename(tok)
            if word in ("sudo", "env", "command", "time", "exec", "nice"):
                word = ""          # a prefix — the next word is the command
            else:
                at_start = False
            out.append(tok); i += len(tok)
            continue
        out.append(c); i += 1
    return "".join(out)


# Commands that only look. A repeat of one of these over an unchanged board
# returns the bytes it returned last time, which is the whole argument for
# refusing it.
READERS = {"find", "grep", "rg", "ls", "cat", "head", "tail", "wc", "sed",
           "awk", "stat", "file", "tree", "diff", "python3", "python"}
WRITERS = re.compile(r"(^|[|;&]\s*)(rm|mv|cp|mkdir|touch|tee|install|chmod)\b"
                     r"|>>?|\bgit\s+(add|commit|checkout|reset|rm|mv|stash)\b")


_GITBASH_DRIVE_RE = re.compile(r"^/([A-Za-z])(/.*)?$")


def is_board_dir(p):
    """A directory is a board only when it CARRIES one — `settings.md`, or a
    `prds/`. Duplicated from @resources/board/plan.py for the same reason the
    two names above are. The name alone is not proof: `pearde` is an ordinary
    word, and a folder called that beside a real board would shadow it."""
    return os.path.isdir(p) and (
        os.path.isfile(os.path.join(p, "settings.md"))
        or os.path.isdir(os.path.join(p, PRDS_DIR)))


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
    board-directory configuration. @resources/board/plan.py `named_boards`
    carries the reasoning; at most two come back."""
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
    carrying `settings.md`.

    Two such children is None here and a refusal everywhere else. The guard
    is a hook on every tool call, not the part of this tool that tells a
    person to rename a directory: a project it cannot name one board in is a
    project it has no opinion about, and doctor's `board` row is what reports
    it. Nothing else consults this, so nothing else is made quiet by it."""
    found = named_boards(d)
    return found[0] if len(found) == 1 else None


def board_of(start):
    """The nearest ancestor carrying a board, or None — the same walk
    @resources/board/plan.py `find_board` does, so the guard and `scan` name
    the same board from the same cwd. Carrying, not named: a folder called
    `pearde` that holds no board is not one, and a board a project had to
    call something else is one. The guard has no opinion about a directory
    that is not a board.

    Two passes, so a board under a known name wins at any depth over a
    discovered one nearer the cwd — @resources/board/plan.py `board_above`
    says why: `resources/board/example/` in this repo IS a board, and a
    single pass would count a session's blocks against that fixture whenever
    the cwd sat in `resources/board/`."""
    start = start or os.getcwd()
    if os.name == "nt":
        # Git Bash's own `cwd` (and `pwd`/`dirname` output doctor.sh builds
        # from it) is POSIX-style, `/c/Users/...` — os.path.abspath under a
        # native Windows interpreter does not read that as a drive letter,
        # it prepends the current drive instead: `/c/Users/...` becomes
        # `C:\c\Users\...`, a path that never exists, so `.pearde/` is
        # never found and the guard silently no-ops on every real Bash tool
        # call.
        m = _GITBASH_DRIVE_RE.match(start)
        if m:
            start = f"{m.group(1)}:{m.group(2) or '/'}"
    d = os.path.abspath(start)
    return walk_up(d, board_named) or walk_up(d, board_scanned)


def walk_up(d, find):
    """`find` applied to `d` and every ancestor, first answer wins."""
    while True:
        b = find(d)
        if b:
            return b
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def prds_dir(board):
    return os.path.join(board, PRDS_DIR)


def member_dirs(board):
    """A master board's members, read straight out of `settings.md` — the
    guard imports nothing from the planner, so a broken planner never blocks
    a tool call."""
    out, inside = [], False
    try:
        text = open(os.path.join(board, "settings.md"), encoding="utf-8").read()
    except OSError:
        return out
    for line in text.splitlines():
        if re.match(r"\s*members:\s*$", line):
            inside = True
            continue
        if inside:
            m = re.match(r"\s*-\s+(?:([\w.-]+)\s*:\s*)?(\S+)\s*$", line)
            if not m:
                break
            path = m.group(2)
            if not os.path.isabs(path):
                path = os.path.normpath(os.path.join(board, path))
            if os.path.isdir(path):
                out.append(path)
    return out


def stamp(board):
    """One number for "has anything on this board moved". The newest mtime of
    any `.md` under the board and its members — cheap enough to run on every
    tool call, exact enough that an unchanged stamp means an unchanged answer."""
    newest = 0.0
    for root_dir in [board] + member_dirs(board):
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")
                       and d not in ("__pycache__", "node_modules")]
            for f in files:
                if not f.endswith(".md"):
                    continue
                try:
                    newest = max(newest, os.stat(os.path.join(root, f)).st_mtime)
                except OSError:
                    pass
    return round(newest, 3)


def guard_state(board):
    """`<board>/.state/guard`, or whatever `PEARDE_GUARD_STATE` names. The
    same spelling @resources/board/plan.py `guard_dir()` reads back."""
    return os.environ.get(GUARD_STATE_ENV) or os.path.join(
        board, ".state", "guard")


def state_path(session, board):
    d = guard_state(board)
    os.makedirs(d, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_-]", "", session or "nosession")[:64] or "x"
    return os.path.join(d, safe + ".json")


def load(session, board):
    try:
        return json.load(open(state_path(session, board), encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save(session, board, data):
    try:
        with open(state_path(session, board), "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    except OSError:
        pass


def clock(t):
    return time.strftime("%H:%M:%S", time.localtime(t))


# ── the count ─────────────────────────────────────────────────────────────────
# The guard sees every tool call a session makes on a board, so it is the one
# place the pass's cost can be counted without a second hook. Per board,
# under `boards` in the session file: `calls`, `reads`, `bash`, `edits` and
# `refused` — counted since the session first saw the board — `since`, the
# time of the last transition, `transitions`, how many there were, and
# `mark`: the counters as they stood at that transition, with `tokens`, the
# transcript's output-token sum then. A row's count is counter minus mark;
# "reset" is the mark moving, so `status` still has the session's totals.
# transitions.py `hand_over` writes the row and moves the mark; plan.py
# `status` prints the block.
COUNTERS = ("calls", "reads", "bash", "edits", "refused")
KIND = {"Read": "reads", "Bash": "bash", "Edit": "edits", "Write": "edits"}
_LIVE = {}      # session, st, board — set by `count`, read by `deny`


def block_of(st, board):
    boards = st.setdefault("boards", {})
    b = boards.setdefault(os.path.realpath(board), {})
    for k in COUNTERS:
        b.setdefault(k, 0)
    b.setdefault("since", time.time())
    b.setdefault("transitions", 0)
    b.setdefault("mark", {})
    return b


def count(session, st, board, tool, data):
    """One call seen on `board`: `calls` and the tool's own counter move, and
    the transcript path is kept so a transition can price the window."""
    b = block_of(st, board)
    b["calls"] += 1
    if tool in KIND:
        b[KIND[tool]] += 1
    if data.get("transcript_path"):
        st["transcript"] = str(data["transcript_path"])
    save(session, board, st)
    _LIVE.update(session=session, st=st, board=board)


def deny(reason):
    if _LIVE:
        block_of(_LIVE["st"], _LIVE["board"])["refused"] += 1
        save(_LIVE["session"], _LIVE["board"], _LIVE["st"])
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason}}))
    sys.exit(0)


def note(reason, event="PreToolUse"):
    out = {"hookSpecificOutput": {"hookEventName": event,
                                  "additionalContext": reason}}
    if event == "PreToolUse":
        out["hookSpecificOutput"]["permissionDecision"] = "allow"
        out["hookSpecificOutput"]["permissionDecisionReason"] = reason
    print(json.dumps(out))
    sys.exit(0)


def ok():
    sys.exit(0)


def reads_only(cmd):
    if WRITERS.search(cmd):
        return False
    for seg in re.split(r"[|;&]+", cmd):
        seg = seg.strip()
        if not seg:
            continue
        head = seg.split()[0]
        head = os.path.basename(head)
        if head in ("cd", "echo", "sort", "uniq", "cut", "xargs", "test", "["):
            continue
        if head not in READERS and head != "git":
            return False
        if head == "git" and not re.search(r"\bgit\s+(status|log|diff|show|"
                                           r"ls-files|rev-parse|branch)\b", seg):
            return False
    return True


def manual(path):
    """A file of this skill's own reference tree, reached through any install
    link — the links are what an install builds, so the real path is the only
    identity that holds."""
    real = os.path.realpath(path)
    if not real.startswith(PEARDE + os.sep):
        return ""
    rest = real[len(PEARDE) + 1:]
    if rest.startswith(MANUAL) or rest in ("README.md", "index.md", "SKILL.md"):
        return real
    return ""


# ── the skill tree ────────────────────────────────────────────────────────────
# The install is links into this repo (@references/install.md), so a pass on
# any board on the machine that edits the skill edits this working tree —
# .pearde/memos/the-install-is-live-symlinks.md counts what that cost. A write
# under the skill root from a session whose board is another repo's is
# refused; the same repo, or no board in scope, passes as before.
SKILL = os.path.realpath(PEARDE)
MEMO = ".pearde/memos/the-install-is-live-symlinks.md"


def skill_file(path):
    """The real path of a file in this skill's own tree, reached through any
    install link or by name — or "". The board under it is not the skill:
    its `.pearde/prds/` is where another board files a PRD, which is the way in."""
    real = os.path.realpath(path)
    if not real.startswith(SKILL + os.sep):
        return ""
    if any(real.startswith(os.path.join(SKILL, n, PRDS_DIR) + os.sep)
           for n in BOARD_DIRS):
        return ""
    return real


def another_boards_write(inp, cwd):
    """`Edit|Write` into the skill tree from a pass on another board —
    refused, naming the real path the link resolves to, the memo, and the
    two ways out. The session's board is the nearest `.pearde/` above its
    working directory, as `find_board` reads it; none, or this repo's own,
    and the write is not this rule's business."""
    given = str(inp.get("file_path") or "")
    real = skill_file(given)
    if not real:
        return
    board = board_of(cwd)
    if not board or os.path.realpath(os.path.dirname(board)) == SKILL:
        return
    via = (f"{given} resolves to {real}" if os.path.abspath(given) != real
           else real)
    deny(f"A pass on another board does not write the skill: {via} — the "
         f"pearde working tree — and this session's board is {board}. The "
         f"install is links into that tree — {MEMO} — so the edit would land "
         "uncommitted among hunks the sessions on that board are staging. "
         "Two ways out: file a PRD on the skill's own board (`pearde add "
         f"\"<title>\"` from {SKILL}), or hand the edit to a session "
         "working it.")


def fm_state(text):
    """The `state:` value of a frontmatter block, or None."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    m = STATE_RE.search(text[3:end] if end > 0 else "")
    return m.group(1) if m else None


def after_edit(path, tool, inp):
    """(before, after): the file's text now, and as the tool would leave it.
    `after` is None when the input does not say."""
    try:
        cur = open(path, encoding="utf-8").read()
    except OSError:
        cur = ""
    if tool == "Write":
        return cur, str(inp.get("content") or "")
    old, new = inp.get("old_string"), inp.get("new_string")
    if old is None or new is None or old not in cur:
        return cur, None
    return cur, (cur.replace(old, new) if inp.get("replace_all")
                 else cur.replace(old, new, 1))


def state_by_hand(tool, inp):
    """`Edit|Write` on a `prd.md` that changes its `state:` line — refused,
    naming the command. A body edit passes; the pass file reminder is
    `post`'s. `transitions.py` writes through edit.py, never through a
    tool, so it is never here."""
    path = os.path.abspath(str(inp.get("file_path") or ""))
    if os.path.basename(path) != "prd.md":
        return
    board = board_of(os.path.dirname(path))
    if not board:
        return
    before, after = after_edit(path, tool, inp)
    if after is None or fm_state(before) == fm_state(after):
        return
    rel = os.path.relpath(os.path.dirname(path), prds_dir(board))
    if not before:
        deny(f"A PRD is made by a command, never written by hand: "
             f"`pearde add \"<title>\"` for a new one, `pearde refine <prd> "
             f"< split` for children — each arrives `state: open` from the "
             f"template. Writing {rel}/prd.md with a `state:` of your own "
             "skips the gate every command checks.")
    deny(f"`state:` is written by the tool, never by hand — use `pearde set "
         f"{rel} {fm_state(after) or '<state>'}`: it checks the gate of "
         "@references/parts/states.md, prints the progress line and records "
         "the row; `--force` writes any transition and says so on the line. "
         "Every other transition has its own command — claim, release, "
         "answer, specced, refine, collect, sweep.")


# Every artifact this tool makes lands inside a board's `.pearde/` — the
# invariant `every-artifact-lands-inside-the-board` on this repo's own board.
# The commands hold to it on their own: every writer routes through
# `plan.py state_dir(board)`, so a `.state/` corner is always `<board>/.state`.
# A pass writing the same file by hand does not: `.state/pass.md` is how the
# guard's own notes and half the manual spell it, and a relative path resolves
# against the session's cwd — the repo root, one level above the board. That
# is exactly how an untracked `<repo>/.state/pass.md` appeared on 2026-09-01.
# Named basenames only, never the bare `.state` component: a project may keep
# a `.state/` of its own, and the guard refuses what it can prove.
STATE_OWNED = re.compile(
    r"^(pass(\.[^/]+)?\.md|ask\.md|plan\.json|parse-cache\.json"
    r"|history\.jsonl|transitions\.jsonl|view\.html)$")


def board_artifact_astray(inp, board):
    """`Edit|Write` of one of the board's own machine-local files into a
    `.state/` that is not this board's — refused, naming the path it belongs
    at. `board` is the nearest `.pearde/`; a write already inside it is this
    rule's whole exemption."""
    path = os.path.abspath(str(inp.get("file_path") or ""))
    parts = path.split(os.sep)
    if ".state" not in parts[:-1] or not STATE_OWNED.match(parts[-1]):
        return
    inside = os.path.join(os.path.realpath(board), "")
    if os.path.realpath(path).startswith(inside):
        return
    tail = os.sep.join(parts[parts.index(".state"):])
    want = os.path.join(board, tail)
    deny(f"Every file this tool makes lands inside the board: {path} is "
         f"outside {board}, and a `.state/` at the repo root is untracked "
         "scratch nothing reads.\nWrite "
         f"{want} instead — `.state/…` anywhere in the manual means "
         f"`{board}/.state/…`, and a relative path resolves against this "
         "session's working directory, one level above the board. If a "
         "pass file of your own is meant, name it "
         f"{os.path.join(board, '.state', 'pass.<what-you-are-on>.md')} so "
         "it never overwrites another session's.")


def touches_board(cmd, board):
    return ("prds" in cmd or "prd.md" in cmd
            or os.path.basename(os.path.dirname(board)) + "/prds" in cmd)


def budget_of(board):
    """`context-budget` off .pearde/settings.md, in tokens. `off`/`0` disables
    it. A bare number is tokens; `120k` is 120,000."""
    try:
        text = open(os.path.join(board, "settings.md"), encoding="utf-8",
                    errors="replace").read()
    except OSError:
        return BUDGET_DEFAULT
    m = BUDGET_KEY.search(text)
    if not m:
        return BUDGET_DEFAULT
    v = m.group(1).strip().lower()
    if v in ("off", "none", "0"):
        return 0
    try:
        return int(float(v[:-1]) * 1000) if v.endswith("k") else int(float(v))
    except ValueError:
        return BUDGET_DEFAULT


def context_now(data):
    """The window this turn was billed for, off the transcript's last
    assistant usage. 0 when there is no transcript to read — the guard never
    guesses a number it would then refuse on."""
    path = data.get("transcript_path") or ""
    if not path or not os.path.isfile(path):
        return 0
    try:
        with open(path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            fh.seek(max(0, size - 262144))
            tail = fh.read().decode("utf-8", "replace").splitlines()
    except OSError:
        return 0
    for line in reversed(tail):
        line = line.strip()
        if not line.startswith("{") or '"usage"' not in line:
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") != "assistant":
            continue
        u = ((d.get("message") or {}).get("usage")) or {}
        n = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
             + u.get("cache_creation_input_tokens", 0))
        if n:
            return n
    return 0


def agent_of(data):
    """Which window this call was made in: "" for the session that was asked,
    the worker's own id for anything it dispatched. One session id and one
    transcript path cover the orchestrator and every worker it sends out, so
    this is the only thing that tells two windows apart — and the repeat-read
    and repeat-command stamps are per window, not per session. A pass worked
    by successive `pearde-pass` dispatches would otherwise have its second
    pass refused the first read of a file its first pass had read: a fresh
    window, refused for what it never saw."""
    return str(data.get("agent_id") or data.get("agent_type") or "")


def stamp_key(data, prefix, ident):
    """A stamp key for `ident`, scoped to the window that asked."""
    return prefix + hashlib.sha1(
        (agent_of(data) + "\0" + ident).encode()).hexdigest()[:16]


def dispatched(data):
    """True when this tool call belongs to a worker the orchestrator sent
    out, not the pass's own turn. session_id and transcript_path are the
    SAME file for every worker and the orchestrator alike — the hook payload
    shares one session across a whole pass — so they cannot tell one from
    the other. `agent_id`/`agent_type` can: the orchestrator's own tool
    calls carry neither; a dispatched analyst, implementer or any other
    subagent carries both. Confirmed empirically, not from documentation —
    see the PRD's report."""
    return bool(data.get("agent_id") or data.get("agent_type"))


def budget(data, st, session, board, tool, inp):
    """Refuse the window that outgrew its own ceiling. Everything the handover
    needs stays open: the scan, the pass file, and the files that say what a
    handover is.

    Dispatched-only: a worker's window cannot be measured from here — the
    transcript this hook is handed is the dispatcher's, and a worker's turns
    are not in it — so a call carrying `agent_id`/`agent_type` never reaches
    the cap check, the 70%/85% notes, or the ESCAPE bypass below. A pass
    worker ends itself by the count in @references/parts/dispatch.md, not by
    this ceiling, and this is also what keeps a worker from being told, by the
    ceiling's own deny text, to write a pass file that is not its own.

    Measured from the floor. `ctx` is the whole window, and a window opens
    holding the system prompt, the tools, CLAUDE.md and the skill before the
    pass exists. `floor` is the smallest this session has been billed for;
    `grew` is what the pass put on top of it, and that is what the budget
    is a budget for."""
    if dispatched(data):
        return
    cap = budget_of(board)
    if not cap:
        return
    ctx = context_now(data)
    if not ctx:
        return
    floor = st.get("budget_floor")
    if floor is None or ctx < floor:
        st["budget_floor"] = floor = ctx
        save(session, board, st)
    grew = ctx - floor
    if grew < cap:
        band = 0.85 if grew >= cap * 0.85 else (
            BUDGET_WARN if grew >= cap * BUDGET_WARN else 0)
        if band and st.get("budget_band", 0) < band:
            st["budget_band"] = band
            save(session, board, st)
            note(f"This window has grown {grew // 1000}k over its "
                 f"{floor // 1000}k floor, of the {cap // 1000}k budget. Every "
                 "turn from here re-reads all of it. Write .pearde/.state/pass.md now "
                 "— what is established, decided, asked and owed — so the "
                 "handover at the ceiling costs one scan and not a "
                 "re-derivation.")
        return
    path = str(inp.get("file_path") or "")
    if tool in ("Edit", "Write", "Read") and ESCAPE.search(path):
        return
    if tool == "Bash" and TOOLS.search(str(inp.get("command") or "")):
        return
    if tool in ("TodoWrite", "AskUserQuestion", "Agent", "Task"):
        return
    deny(f"This window has grown {grew // 1000}k over its floor, past the "
         f"{cap // 1000}k budget — it has stopped being cheap to continue.\n"
         f"Every turn now bills {ctx // 1000}k of cache read for work the "
         "board already holds on disk.\n\nHand the rest over rather than "
         "stopping: write .pearde/.state/pass.md whole — established, decided, "
         "asked, edits, owed — and dispatch `pearde-pass` to carry on from "
         "it (@references/parts/dispatch.md). That worker opens on a fresh "
         "window, reads the pass file, runs the scan and is where this one "
         "is for one percent of the tokens. Only when you were asked for one "
         "pass and it is finished do you stop and say so.\n\nStill allowed: "
         "the pass file, references/parts/dispatch.md, "
         "references/parts/loop.md, references/parts/pass.md, dispatching a "
         "worker, asking the user, and the board's own commands.")


def destructive_in_another_tree(cmd, cwd, board):
    """`reset --hard`, `checkout --`, `clean` and a real stash, refused in any
    tree this session does not own — the shell half of
    `.pearde/memos/a-session-that-writes-a-shared-checkout-can-revert-another-
    session-s-work.md`. The board's own code is guarded at its call sites by
    @resources/board/refuse.py; this is the same module reading what a session
    types by hand, which is the other way that memo's `reset --hard` reaches a
    peer's tree.

    Everything here is inside one try: `@resources/board/refuse.py` is
    stdlib-only and imports nothing from the planner, but a guard that raises
    is a session that cannot use a tool, so a refusal module that will not
    load or will not answer denies nothing. A missed refusal costs a warning
    the call sites still make; a raised hook costs the whole session."""
    try:
        import refuse as refuselib   # on sys.path via @resources/pearde_path.py
        bad = refuselib.check_line(board, cmd, cwd)
    except Exception:
        return
    if bad:
        verb, tree, reason, why = bad[0]
        deny(refuselib.refuse_line(verb, tree, reason, why))


def pre(data):
    tool = data.get("tool_name") or ""
    inp = data.get("tool_input") or {}
    session = data.get("session_id") or ""
    # an edit is counted on the board its file is in, or the cwd's when the
    # file is outside every board; everything else on the cwd's board
    board = board_of(data.get("cwd"))
    if tool in ("Edit", "Write"):
        board = board_of(os.path.dirname(os.path.abspath(
            str(inp.get("file_path") or "")))) or board
    # Before the board test, not after it: the tree a destructive git would
    # discard is the one whose board decides, and a session types that command
    # from wherever it happens to be standing — including a directory with no
    # board above it at all. Everything below this line is per-board
    # bookkeeping and rightly stops when there is no board.
    if tool == "Bash":
        destructive_in_another_tree(str(inp.get("command") or ""),
                                    data.get("cwd"), board)
    if not board:
        ok()
    st = load(session, board)
    count(session, st, board, tool, data)
    budget(data, st, session, board, tool, inp)
    if tool in ("Edit", "Write"):
        another_boards_write(inp, data.get("cwd"))
        board_artifact_astray(inp, board)
        state_by_hand(tool, inp)
        ok()

    if tool == "Bash":
        cmd = str(inp.get("command") or "")
        r = quiet and quiet.check(cmd, str(data.get("cwd") or ""))
        if r:
            deny(r)
        if any(w.search(data_free(cmd)) for w in WALKS):
            deny("The board is not walked by hand — loop step 1 is one call:\n"
                 f"    {SCAN}\n"
                 "It returns every state, gate, claim and acceptance count on "
                 "one page, including what this command was looking for.")
        # `scan` is the thing this guard sends you to. A pass that lost its
        # context to a compaction has to be able to ask again, and the board
        # not having moved is exactly when the answer is cheapest.
        if TOOLS.search(cmd):
            ok()
        if not (touches_board(cmd, board) and reads_only(cmd)):
            ok()
        key = stamp_key(data, "b", cmd)
        now = stamp(board)
        prev = st.get(key)
        if prev and prev.get("stamp") == now:
            deny(f"You ran this at {clock(prev['at'])} and nothing on the board "
                 "has changed since — the output is byte-for-byte what you "
                 "already have.\nCite it from .pearde/.state/pass.md instead, or write "
                 "it there now if it is not in it.")
        st[key] = {"at": time.time(), "stamp": now}
        save(session, board, st)
        ok()

    if tool == "Read":
        path = os.path.abspath(str(inp.get("file_path") or ""))
        ref = manual(path)
        if ref:
            if os.path.basename(ref) in REREADABLE:
                ok()
            path = ref
        elif not path.startswith(os.path.dirname(board)):
            ok()
        try:
            mtime = round(os.stat(path).st_mtime, 3)
        except OSError:
            ok()
        key = stamp_key(data, "r", path)
        prev = st.get(key) or {}
        n = prev.get("n", 0)
        if n >= 2 and prev.get("mtime") == mtime:
            if ref:
                deny(f"Third read of this reference, unchanged since "
                     f"{clock(prev['at'])} — the manual does not move while a "
                     "pass runs.\nWhat you needed from it belongs in "
                     ".pearde/.state/pass.md. The steps themselves are the exception: "
                     "references/parts/loop.md and references/parts/pass.md "
                     "are always readable.")
            deny(f"Third read of this file, unchanged since {clock(prev['at'])}"
                 " — you have read it twice already and nothing has written to "
                 "it since.\nWhat you needed from it belongs in .pearde/.state/pass.md; "
                 f"board state comes from `{SCAN}`.")
        st[key] = {"n": n + 1, "at": time.time(), "mtime": mtime}
        save(session, board, st)
        if re.search(r"/specs/[^/]+\.md$", path) and n == 0:
            note("Acceptance boxes are counted for you — `boxes c/t` in "
                 f"`{SCAN}`. Read the spec for its contract, never to count.")
        ok()
    ok()


def post(data):
    inp = data.get("tool_input") or {}
    path = str(inp.get("file_path") or "")
    if os.path.basename(path) != "prd.md":
        ok()
    board = board_of(os.path.dirname(path))
    if not board:
        ok()
    rf = os.path.join(board, PASS_FILE)
    try:
        moved = os.stat(path).st_mtime
    except OSError:
        ok()
    try:
        written = os.stat(rf).st_mtime
    except OSError:
        written = 0
    if written >= moved:
        ok()
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext":
            f"A PRD moved and {rf} has not been rewritten since. The pass "
            "file is what survives the next compaction: what was established "
            "and when, what was decided, what is out to the user, what is "
            "owed. Rewrite it whole with this transition in it."}}))
    ok()


def check():
    board = board_of(os.getcwd())
    if not board:
        print("guard: no board above " + os.getcwd())
        return
    print(f"guard: {board}\n  stamp {stamp(board)}\n"
          f"  state {guard_state(board)}\n"
          f"  scan  {SCAN}")


# ── the command ───────────────────────────────────────────────────────────────
# `pearde guard on` is the reader asking for the block below in their own
# settings file — doctor never writes one. `<repo>` defaults to the repo the
# nearest board is in. The edit keeps every other key and its order, adds
# only what is missing, and says each line it added; `off` removes exactly
# those and leaves the env key, an emptied event list dropped and `hooks`
# itself kept. A file that is not JSON is refused untouched.
SELF = os.path.realpath(__file__)
SERVE = pearde_path.script("serve.py") or ""
THINK = "8000"
# (event, matcher, command, the pattern that recognises an entry as ours
#  however its path is spelled). `SessionStart` carries no matcher: the
#  matcher there is the start reason — startup, resume, clear, compact, fork —
#  and this hook wants every one of them.
#  `>/dev/null 2>&1 || true` is the safety property, not tidiness: a
#  SessionStart hook that exits 2 PREVENTS the session from starting, and
#  `serve.py ensure` exits 2 outside a board. See @references/parts/guard.md.
HOOKS = (("PreToolUse", "Bash|Read", f"python3 {SELF} pre", r"guard\.py\s+pre\b"),
         ("PreToolUse", "Edit|Write", f"python3 {SELF} pre", r"guard\.py\s+pre\b"),
         ("PostToolUse", "Edit|Write", f"python3 {SELF} post", r"guard\.py\s+post\b"),
         ("SessionStart", None,
          f"python3 {SERVE} ensure >/dev/null 2>&1 || true",
          r"serve\.py\s+ensure\b"))
ROW = "  %-11s %-7s %s"          # doctor.sh's row(), byte for byte


class Refused(Exception):
    pass


def repo_of(args):
    if args:
        d = os.path.abspath(args[0])
        if not os.path.isdir(d):
            raise Refused(f"{args[0]} is not a directory")
        return d
    board = board_of(os.getcwd())
    if not board:
        raise Refused("no board above " + os.getcwd()
                      + " — name the repo: pearde guard on <repo>")
    return os.path.dirname(board)


def settings_of(repo):
    return os.path.join(repo, ".claude", "settings.json")


def read_settings(path):
    """(data, text) — {} and "" when the file is absent."""
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return {}, ""
    try:
        data = json.loads(text)
    except ValueError as e:
        raise Refused(f"{path} is not JSON ({e}) — nothing written")
    if not isinstance(data, dict):
        raise Refused(f"{path} is not a JSON object — nothing written")
    return data, text


def write_settings(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def is_guard(hook, pat):
    return (isinstance(hook, dict)
            and re.search(pat, str(hook.get("command") or "")) is not None)


def entry_for(matcher, command):
    """The settings entry `on` appends. A row with no matcher writes no
    `matcher` key — SessionStart fires on every start reason without one."""
    e = {"hooks": [{"type": "command", "command": command}]}
    return {"matcher": matcher, **e} if matcher is not None else e


def entries_of(hooks, event):
    v = hooks.get(event)
    if v is None:
        return []
    if not isinstance(v, list):
        raise Refused(f"hooks.{event} is not a list — nothing written")
    return v


def guard_on(args):
    """writes the hooks block into <repo>/.claude/settings.json, keeping every other key"""
    path = settings_of(repo_of(args))
    data, _ = read_settings(path)
    added = []
    env = data.get("env")
    if env is None:
        env = data["env"] = {}
    if not isinstance(env, dict):
        raise Refused("env is not an object — nothing written")
    if "MAX_THINKING_TOKENS" not in env:
        env["MAX_THINKING_TOKENS"] = THINK
        added.append(f'env.MAX_THINKING_TOKENS = "{THINK}"')
    hooks = data.get("hooks")
    if hooks is None:
        hooks = data["hooks"] = {}
    if not isinstance(hooks, dict):
        raise Refused("hooks is not an object — nothing written")
    for event, matcher, command, pat in HOOKS:
        entries = entries_of(hooks, event)
        have = [h for e in entries if isinstance(e, dict)
                and e.get("matcher") == matcher
                for h in (e.get("hooks") or []) if is_guard(h, pat)]
        if have:
            continue
        entries.append(entry_for(matcher, command))
        hooks[event] = entries
        added.append(f"{event} {matcher or ''}{' ' if matcher else ''}→ {command}")
    if not added:
        print(f"guard on: {path} — already wired, nothing changed")
        return 0
    write_settings(path, data)
    print(f"guard on: {path}")
    for a in added:
        print("  + " + a)
    print("  a new settings file is read after /hooks or a restart")
    return 0


def guard_off(args):
    """removes exactly the entries `on` wrote; the env key and every other key stay"""
    path = settings_of(repo_of(args))
    data, text = read_settings(path)
    removed = []
    hooks = data.get("hooks")
    if isinstance(hooks, dict):
        for event, matcher, command, pat in HOOKS:
            entries = entries_of(hooks, event)
            keep = []
            for e in entries:
                own = ([h for h in e["hooks"] if is_guard(h, pat)]
                       if isinstance(e, dict) and e.get("matcher") == matcher
                       and isinstance(e.get("hooks"), list) else [])
                if not own:
                    keep.append(e)
                    continue
                removed += [f"{event} {matcher or ''}{' ' if matcher else ''}→ {h['command']}"
                            for h in own]
                rest = [h for h in e["hooks"] if h not in own]
                if rest:
                    e["hooks"] = rest
                    keep.append(e)
            if len(keep) != len(entries):
                if keep:
                    hooks[event] = keep
                else:
                    del hooks[event]
    if not removed:
        print(f"guard off: {path} — not wired, nothing changed")
        return 0
    write_settings(path, data)
    print(f"guard off: {path}")
    for r in removed:
        print("  - " + r)
    return 0


def guard_status(args):
    """doctor's guard row, alone — ok, off or broken"""
    import subprocess
    import tempfile
    repo = repo_of(args)
    path = settings_of(repo)
    # both probes keep their guard state in a temp dir — a probe carries no
    # session, and its block would otherwise land as nosession.json in the
    # real state dir on every status call
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "PEARDE_GUARD_STATE": os.path.join(tmp, "state")}
        probe = json.dumps({"tool_name": "Bash", "cwd": repo,
                            "tool_input": {"command": "find prds -name prd.md"}})
        out = subprocess.run([sys.executable, SELF, "pre"], input=probe,
                             capture_output=True, text=True, env=env).stdout
        if '"deny"' not in out:
            print(ROW % ("guard", "broken",
                         f"{SELF} does not refuse a hand-walked board"))
            return 2
        # the second rule, proved the same way: an Edit of this file from a
        # board that is not this repo's — a temp one holding an empty .pearde/
        os.makedirs(os.path.join(tmp, BOARD_DIR))
        probe = json.dumps({"tool_name": "Edit", "cwd": tmp,
                            "tool_input": {"file_path": SELF,
                                           "old_string": "a", "new_string": "b"}})
        out = subprocess.run([sys.executable, SELF, "pre"], input=probe,
                             capture_output=True, text=True, env=env).stdout
    if '"deny"' not in out:
        print(ROW % ("guard", "broken",
                     f"{SELF} does not refuse a write into the skill tree "
                     "from another board"))
        return 2
    _, text = read_settings(path)
    if "guard.py" in text:
        m = re.search(r'MAX_THINKING_TOKENS"\s*:\s*"(\d*)', text)
        tk = f" · MAX_THINKING_TOKENS={m.group(1)}" if m and m.group(1) else ""
        print(ROW % ("guard", "ok", f"wired in {path}{tk} · skill tree guarded"))
        if not re.search(r"serve\.py ensure", text):
            print(ROW % ("", "", "no SessionStart hook — the view is not "
                                 "brought up on a session start; "
                                 "pearde guard on writes it"))
        return 0
    print(ROW % ("guard", "off", f"not wired in {path}"))
    print(ROW % ("", "", "fix: pearde guard on"))
    return 1


COMMAND = {"on": guard_on, "off": guard_off, "status": guard_status}


def command(verb, args):
    try:
        return COMMAND[verb](args)
    except Refused as e:
        print(f"pearde guard {verb}: refused — {e}", file=sys.stderr)
        return 1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre"
    if mode == "check":
        return check()
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        sys.exit(0)
    if mode == "post":
        return post(data)
    return pre(data)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in COMMAND:
        sys.exit(command(sys.argv[1], sys.argv[2:]))   # a command's error is its own
    try:
        main()
    except Exception:
        # A guard that breaks a tool call is worse than the waste it prevents.
        sys.exit(0)
