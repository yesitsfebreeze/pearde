#!/usr/bin/env python3
"""pearde collect — close a finished PRD in one call: verify, commit, done.

    collect [<prd>…] [--dry] [--fail] [--trust] [--widen <path>]…
            [--also <path> --also-note <text>] [--as <id>] [--board <path>]
    collect --snapshot <prd>          what `claim` records, until it does

For each PRD named — or every PRD in `scan`'s **collect** section when none
is — the seven steps of @references/parts/loop.md step 6, in order:

  1  the finished condition off both files      `standing()` in plan.py
  2  every spec's `## Verify and Proof` block    run in `repo`, output kept
     then the board's `gate:`                    against the claim's baseline
  3  the paths: specs' footprints ∪ the PRD's ∪ the PRD dir ∪ `--also`
     — the PRD's own folder is the board's record: added whole, always —
       never by hunk, never a stop
     — a dirty path outside it is inherited: listed, never added
     — a dirty path inside it that the claim predates: exit 1, `--widen`
     — a file holding both: only the hunks the claim does not predate,
       staged as the working file with the inherited hunks reversed,
       and the staged blob checked for parse and placement before 4
     — a hunk that is in neither the baseline nor the worker's diff —
       two edits on adjacent lines, merged by `-U0` — is refused:
       `two authors on one hunk: <file>:<line>`; `--widen` takes the
       file whole, or the worker leaves one untouched line between
  4  the record — `actual:` written, `claim:` cleared, `done`, the report
     posted — then one commit per repo, message per
     @references/parts/commits.md; everything collect wrote is in it
  5  `commit:` — the one key that cannot be in the commit it names — in a
     second, one-key commit `<prd> — record`, right behind
  6  `POST /report` to the daemon when it is up — before the commit, so
     `## Report` is in it
  7  the progress line, the transition row

A container — a parent whose every child is `done`, with no spec and no
open box of its own — has nothing to verify and nothing to commit but its
record. `dispatchable()` in plan.py is the one word for it (`container:
every child done — pearde collect closes it` — what `claim` refuses on and
`scan` lists under collect with), and `close_container()` here sets `done`,
`actual:` the sum of the children's, `commit:` the last child's, in one
commit `<parent> — done: every child landed`. A parent with specs or an
open box of its own is ordinary work, and its boxes decide it.

A step that stops writes nothing after it. The worker's word is never taken
for the verify: `--trust` is the orchestrator's word, said on the line.

**The baseline.** "The claim predates it" is answered by what `claim`
recorded under `.pearde/.claims/<prd>/` — the tracked diff, the untracked
list, the gate's output — through `snapshot()` here. With no record, a
file's mtime against the claim's timestamp decides for the whole file, and
the gate has no baseline to be measured against, so it has to exit 0.

**Board state written between transitions rides.** `answer` writes a
`prd.md` no collect is about to commit; `owe()` lists that path in
`.pearde/.claims/riders` and the next collect on the board adds it and names
it on the line. What collect itself writes never rides — it is in the
commit it makes.

Reads through plan.py, writes through edit.py. Python 3 stdlib only.
"""
import contextlib
import datetime
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))
import pearde_path  # noqa: E402,F401 — @resources/pearde_path.py, the one rule
import plan as planlib  # noqa: E402 — beside this script
import edit as editlib  # noqa: E402 — beside this script
import transitions as translib  # noqa: E402 — the one printer of the line
import specs as specslib  # noqa: E402 — SPECCED/REFINE reuse its own gates
import lanes as laneslib  # noqa: E402 — every other use of it is lazy, but
# `except lanes.Conflict` needs the class at the moment the clause is read
LaneConflict = laneslib.Conflict

# collect writes done/failed transitions straight to the same log
# transitions.py record() appends to — never to .history.jsonl, the
# daemon's one-row-a-day burn-down.
TRANSITION_FILE = translib.TRANSITIONS_FILE
CLAIMS_DIR = ".claims"
RIDERS_FILE = "riders"
# The declaration — transitions.py `Args` is the parser, shared with every
# command pearde.py discovers; an undeclared flag is refused with this list,
# exit 2, before the board is read.
FLAGS = translib.Flags(("as", "board", "also", "also-note", "widen",
                        "snapshot", "report"), ("dry", "fail", "trust"),
                       multi=("also", "widen"))
# The verdict words a report is allowed to carry, and the transition each
# one runs — @references/parts/loop.md step 6, @references/parts/workers.md
# "On return". Anything else — missing, or a word not in this tuple — is
# refused rather than guessed at.
VERDICTS = ("SPECCED", "REFINE", "QUESTION", "DONE", "BLOCKED", "FAILED")
HELD = ("analyzing", "claimed", "blocked")
# Whose uncommitted work a collect can run into. `HELD` is the in-flight
# band the board schedules around; contending for a DIRTY PATH is wider
# than that, because a worker leaves code in the tree on every verdict, not
# only while it holds the PRD — an analyst's probe is uncommitted by
# instruction, so a `specced`, `question` or `refine` sibling has code
# standing exactly as a `claimed` one does. `done` is out: its work is in a
# commit. `open` is out: nothing has been worked, and it has no spec to
# carry a footprint anyway.
CONTENDING = ("analyzing", "refine", "question", "specced",
              "claimed", "blocked", "failed")


class Stop(Exception):
    """A step said no. The message is what the user reads; nothing after the
    step ran."""


# ── argv ──────────────────────────────────────────────────────────────────────

def parse_args(argv):
    a = translib.Args(argv, FLAGS, "collect")     # FlagRefused → exit 2
    # the persona the way every transition resolves it — `--as`, else
    # PEARDE_AS, else the one refusal transitions.py raises: collect's line
    # is the record of who acted, and a default would write it unasked
    persona = (a.opt.get("as") or os.environ.get("PEARDE_AS", "")).strip()
    opts = {"prds": [x.strip("/") for x in a.pos],
            "also": a.opt.get("also", []), "widen": a.opt.get("widen", []),
            "also_note": a.opt.get("also-note", ""),
            "as": persona or translib.persona_default("collect"),
            "board": a.opt.get("board"), "snapshot": a.opt.get("snapshot"),
            "report": a.opt.get("report")}
    for k in ("dry", "fail", "trust"):
        if k in a.flags:
            opts[k] = True
    if opts["also"] and not opts["also_note"]:
        raise Stop("--also needs --also-note — the message names what the "
                   "run taught")
    return opts


def also_places(board_root, a):
    """Where one `--also` entry is looked for, in the order it is looked:
    the board root first, the caller's cwd second — *look in the notes
    first, then where you are standing*, the user's call on 2026-09-02
    (`.pearde/memos/also-resolves-against-the-board-first.md`). An absolute
    entry is taken as given and is its own only place. The list is what a
    refusal prints, so the message names every place that was tried and
    nothing that was not."""
    if os.path.isabs(a):
        return [os.path.abspath(a)]
    board = os.path.abspath(os.path.join(board_root, a))
    cwd = os.path.abspath(a)
    return [board] if cwd == board else [board, cwd]


def also_path(board_root, a):
    """One `--also` entry as an absolute path: the first place that holds it,
    so a name both roots hold is the **board's**. The one place `--also` is
    turned into a path — `check_also` and `sort_paths` both read it here, so
    the path a refusal names and the path a commit carries cannot drift.
    When no place holds it the board's is returned and `check_also`, which
    runs first, has already refused the call."""
    places = also_places(board_root, a)
    for p in places:
        if os.path.exists(p):
            return p
    return places[0]


def check_also(board_root, opts):
    """Every `--also` entry names something one of its two places holds, or
    the whole call stops before a single PRD is read.

    The footprint loop in `sort_paths` has always refused a path the repo
    does not hold; `--also` had no such guard, so an entry that resolved
    nowhere was handed to `git add` and then named in the commit message —
    a record naming a file the commit does not contain. The user's call at
    the drill was refusal over a warning, and refusal of the *call*: this
    runs in `cmd_collect` ahead of the per-PRD loop, which swallows a `Stop`
    and carries on to the next PRD, so a guard inside `collect_one` would
    still let a later PRD commit."""
    for a in opts.get("also", []):
        places = also_places(board_root, a)
        if any(os.path.exists(p) for p in places):
            continue
        raise Stop(f"--also {a}: no such path — looked for "
                   f"{' and '.join(places)}; board root {board_root}; "
                   f"nothing written, nothing committed")


# ── reads ─────────────────────────────────────────────────────────────────────

def spec_files(prd):
    sdir = os.path.join(prd["dir"], "specs")
    if not os.path.isdir(sdir):
        return []
    return [os.path.join(sdir, f) for f in sorted(os.listdir(sdir))
            if f.endswith(".md")]


def open_boxes(prd):
    """[(file, line)] — every unticked box the `done` gate would refuse:
    `prd.md` whole-file, each spec under `## Acceptance`. The verdict is
    `standing()`'s; this names what it saw."""
    out = []
    pmd = os.path.join(prd["dir"], "prd.md")
    for line in open(pmd, encoding="utf-8").read().splitlines():
        if planlib.opens_an_unticked_box(line):
            out.append((pmd, line.strip()))
    for f in spec_files(prd):
        text = open(f, encoding="utf-8").read()
        for sec in re.split(r"(?m)^##\s+", text)[1:]:
            head = sec.split("\n", 1)[0].strip().lower()
            if not head.startswith("acceptance"):
                continue
            for line in sec.splitlines()[1:]:
                if planlib.opens_an_unticked_box(line):
                    out.append((f, line.strip()))
    return out


def section(text, name):
    """The body of `## <name>` up to the next `## `, or ""."""
    m = re.search(r"(?m)^##\s+" + re.escape(name) + r"\s*$", text)
    if not m:
        return ""
    rest = text[m.end():]
    n = re.search(r"(?m)^##\s+", rest)
    return rest[:n.start()] if n else rest


def fenced(text):
    """The fenced blocks of a section, joined — the verify is the whole
    block, and a spec with two fences runs both."""
    return "\n".join(m.group(1) for m in
                     re.finditer(r"(?ms)^```[^\n]*\n(.*?)^```", text))


def verify_blocks(prd):
    """[(specNN, script)] — one per spec that carries a block."""
    out = []
    for f in spec_files(prd):
        text = open(f, encoding="utf-8").read()
        script = fenced(section(text, "Verify and Proof")).strip()
        if script:
            out.append((os.path.basename(f)[:-3], script))
    return out


def spec_goals(prd):
    """[(specNN, goal)] from each spec's `# specNN — goal` line."""
    out = []
    for f in spec_files(prd):
        _, title, _ = planlib.parse_prd(f)
        name = os.path.basename(f)[:-3]
        goal = title or name
        if " — " in goal:
            goal = goal.split(" — ", 1)[1].strip()
        out.append((name, goal))
    return out


def contract_line(prd):
    """`<prd> — <contract>`: the title's own dash, else the title whole."""
    t = prd["title"]
    if " — " in t:
        return t.split(" — ", 1)[1].strip()
    return t


def repo_of(prd, board, board_root):
    """Where the PRD's code lives. `repo:` that is a directory — absolute, or
    relative to the board's repo — is it. With no `repo:`: when the board is
    its own git repo (`board_root == board` — a nested `.pearde` with a
    `.git` of its own), the repo enclosing it, `repo_root` of the board's
    own parent — a nested board defaults to the code repo it sits in, never
    to itself. When the board is not its own repo — `board_root` was found
    walking up *past* the board, so it already is the code repo — unchanged,
    the board's own repo, exactly as before this default existed.

    Then, last: the running SESSION's own worktree of that repo, when the
    ledger names one (`session.instead_of`). Every answer above is a
    checkout resolved by walk-up, and the checkout is the one place the
    parent PRD says nothing may run — three sessions shared it and two lost
    work. So the walk-up answer is the repo this session's tree was cut
    FROM, and the tree is what the command gets. A command outside a
    session, or a session that never took one, gets the walk-up answer
    unchanged: the rule adds a case, it removes none."""
    import session as sessionlib
    raw = str(prd["fm"].get("repo", "") or "").strip()
    if raw:
        for cand in (raw, os.path.join(board_root, raw)):
            if os.path.isdir(cand):
                root = planlib.repo_root(cand)
                if root:
                    return sessionlib.instead_of(board, root)
    if board_root == board:
        enclosing = planlib.repo_root(os.path.dirname(board_root))
        if enclosing:
            return sessionlib.instead_of(board, enclosing)
    return sessionlib.instead_of(board, board_root)


def parse_when(s):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(s.replace("Z", ""), fmt)
        except ValueError:
            continue
    return None


def fmt_hours(h):
    s = f"{h:.2f}".rstrip("0").rstrip(".")
    return (s or "0") + "h"


# ── the worker's report ──────────────────────────────────────────────────────
# `collect --report <path>` reads the verdict a report.md carries and runs
# the transition @references/parts/workers.md maps it to — the same
# `pearde specced` / `pearde refine` / `pearde release` a person would type,
# called in-process through the COMMANDS every one of them already exports,
# so every gate those commands check still runs unchanged. `collect` itself
# is DONE's transition — no dispatch needed, the rest of `cmd_collect` is it.

VERDICT_RE = re.compile(
    r"(?im)^\s*#{0,3}\s*\*{0,2}verdict\*{0,2}\s*:?\s*\*{0,2}([A-Za-z]+)")


def verdict_of(text):
    """The word after the report's `Verdict` marker, read from its head only
    — the first 40 lines — so a later, unrelated sentence using the word
    is never mistaken for it. "" when no marker is there at all; the word
    found, upper-cased, otherwise — even one `VERDICTS` does not hold, so
    the caller can say which."""
    head = "\n".join(text.splitlines()[:40])
    m = VERDICT_RE.search(head)
    return m.group(1).upper() if m else ""


def scores_of(text):
    """`(blast, workflow)` off the report's `## Scores` block — the values
    `pearde specced --blast <x> --workflow <slug>` already takes by hand."""
    sec = section(text, "Scores")
    blast = re.search(r"(?im)^blast-radius:\s*(\S+)", sec)
    workflow = re.search(r"(?im)^workflow:\s*(\S+)", sec)
    return (blast.group(1).strip() if blast else None,
            workflow.group(1).strip() if workflow else None)


@contextlib.contextmanager
def _stdin_as(text):
    """`refine` and `specced --route -` read `sys.stdin.read()` — the report
    text stands in for the pipe a shell call would use."""
    old = sys.stdin
    sys.stdin = io.StringIO(text)
    try:
        yield
    finally:
        sys.stdin = old


def route_report(board, rel, report_path, opts, out=print):
    """`--report <path>`: the verdict decides the transition, never a guess.
    Returns the exit code the transition it ran returned."""
    if not os.path.isfile(report_path):
        raise Stop(f"{rel}: --report {report_path} — no such file")
    text = open(report_path, encoding="utf-8").read()
    word = verdict_of(text)
    if not word:
        raise Stop(f"{rel}: {report_path} names no `Verdict:` — nothing "
                   f"written")
    if word not in VERDICTS:
        raise Stop(f"{rel}: {report_path} verdict `{word}` is not one of "
                   + ", ".join(VERDICTS) + " — nothing written")
    board_flag = ["--board", board]
    persona_flag = ["--as", opts["as"]]
    dry_flag = ["--dry"] if opts.get("dry") else []
    tail = persona_flag + board_flag + dry_flag
    if word == "DONE":
        return collect_one(board, rel, opts, out=out)
    if word == "SPECCED":
        blast, workflow = scores_of(text)
        argv = [rel] + tail
        if blast:
            argv += ["--blast", blast]
        if workflow:
            prds = planlib.scan(board)
            lib = specslib.library(board, prds[rel])
            argv += ["--workflow", workflow]
            if lib.get(workflow, {}).get("kind") != "workflow":
                argv += ["--route", "-"]
        with _stdin_as(text):
            return specslib.COMMANDS["specced"](argv)
    if word == "REFINE":
        with _stdin_as(text):
            return specslib.COMMANDS["refine"]([rel] + tail)
    if word == "QUESTION":
        return translib.COMMANDS["release"]([rel, "question"] + tail)
    if word == "BLOCKED":
        return translib.COMMANDS["release"]([rel, "blocked"] + tail)
    # FAILED, and — per loop.md — anything an implementer returns short of
    # DONE/BLOCKED that still names a real verdict word
    return translib.COMMANDS["release"]([rel, "failed"] + tail)


# ── git ───────────────────────────────────────────────────────────────────────

def run(cmd, cwd, script=None):
    """(exit, output) — stdout and stderr in one stream, the order a reader
    saw them in."""
    try:
        if script is not None:
            # The block goes in as an ARGUMENT, never on stdin, and stdin is
            # closed. Fed on stdin, the first command in the block that reads
            # stdin with no operand — a bare `cat`, `grep PAT`, `sort`, a
            # `python3` with no script — eats the REST of the block: every
            # statement after it never runs and bash exits 0. Measured: a
            # block whose assertion sits behind a bare `cat` exits 0 on a
            # broken tree, and collect records that as green.
            r = subprocess.run(list(cmd) + ["-c", script], cwd=cwd,
                               stdin=subprocess.DEVNULL,
                               capture_output=True, text=True)
        else:
            r = subprocess.run(cmd, cwd=cwd, stdin=subprocess.DEVNULL,
                               capture_output=True, text=True)
    except OSError as e:
        return 127, str(e)
    return r.returncode, r.stdout + r.stderr


# ── guarding a verify block against the checkout it runs in ────────────────
# A verify or gate block is arbitrary shell, run by `run()` above directly in
# a checkout other sessions and other PRDs share — `repo` for a spec's own
# block, `board_root` for the board's `gate`. It runs AFTER the lane lands,
# so `unland` only exists for a red *check*; nothing stands between a green
# script and the checkout it just ran destructive shell in, and nothing
# catches a script that never fails but still `rm -rf .`s something that
# is not this PRD's. Measured: `git reset --hard`, `git clean -fdx` and
# `rm -rf .` all reach past the PRD's own footprint into whatever else is
# dirty there — the exact shape of the incident this PRD is filed from,
# one step earlier than `unland`.
#
# `_park` moves every path dirty in `cwd` that is OUTSIDE the footprint into
# a stash by pathspec, so the script cannot reach it at all — not "reach it
# and get caught after," genuinely absent from the working tree for the
# run. `_heal` looks at what changed outside the footprint once the script
# is done and reverts it: a tracked path back to HEAD's blob (index and
# tree both, so a foreign `git add` is undone too), a new untracked foreign
# path removed. `_restore_head` puts the branch back if the script moved it
# — the same compare-and-swap `commit_private` already writes a ref with,
# so a real concurrent commit is refused rather than clobbered. The PRD's
# OWN footprint is touched by none of this: on the non-lane path that is
# the uncommitted work verify exists to measure, and a script destroying
# its own PRD's footprint is that PRD's own fault, not the checkout's.
def _dirty(cwd):
    """`[(XY, path)]` for everything git calls dirty in `cwd`, read from the
    `-z` form because the human one lies about paths.

    `git status --porcelain` QUOTES any path holding a space or a non-ASCII
    byte — `core.quotePath` is on unless a board turns it off — so ` M "src/a
    b.py"` comes back and `line[3:]` hands every caller the quotes as part of
    the name. Every consumer here then gets it wrong at once: `inside()`
    matches no footprint, so an owned file reads as foreign and the block
    measures a clean HEAD; `_park` feeds the quoted string in as a pathspec,
    git refuses it, and ONE such path runs the whole block unguarded;
    `_snapshot` finds the real path in neither `moved` nor `indexed`; and
    `_unerase` writes HEAD's bytes over uncommitted work while printing
    `put back:` as though it had saved it.

    `-z` never quotes. Records are NUL-separated, and a rename or copy spends
    a second record on its source — consumed here, since the ` -> ` the human
    form uses does not exist in this one and a path may legitimately contain
    it.

    `--untracked-files=all` because the default collapses a wholly untracked
    directory to one row spelled `other/`. That row is a bad pathspec subject
    for `inside()` — a footprint deeper than the directory reads as foreign
    against it — and it makes `_heal` take a whole tree aside and name the
    directory rather than the file a peer actually wrote."""
    r = subprocess.run(["git", "-C", cwd, "status", "--porcelain", "-z",
                        "--untracked-files=all"], capture_output=True,
                       text=True)
    if r.returncode != 0:
        return []
    recs = r.stdout.split("\0")
    rows, i = [], 0
    while i < len(recs):
        rec = recs[i]
        i += 1
        if len(rec) < 4:            # "XY p" is the shortest real record
            continue
        code, path = rec[:2], rec[3:]
        if "R" in code or "C" in code:
            i += 1                  # the rename/copy source, its own record
        rows.append((code, path))
    return rows


_HOLDER = {}


def holder(path):
    """The git checkout that actually HOLDS `path` — `rev-parse
    --show-toplevel` asked from the nearest directory that exists, cached
    per directory so a footprint list costs one fork per directory and not
    one per path.

    Membership is a question only git can answer. A string prefix cannot:
    a checkout nested UNDER another one — a lane at `<board>/.lanes/<prd>`,
    a run-session worktree — is inside the outer path and belongs to
    neither its index nor its worktree. `planlib.repo_root`'s walk-up is
    the fallback when git cannot be run at all; it is right for every
    layout this board ships on and wrong only where git's own rules
    (`core.worktree`, a `.git` file pointing elsewhere, a ceiling) part
    from a walk."""
    d = os.path.abspath(path)
    while d and not os.path.isdir(d):
        nxt = os.path.dirname(d)
        if nxt == d:
            return None
        d = nxt
    if d in _HOLDER:
        return _HOLDER[d]
    root = None
    try:
        r = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True,
                           stdin=subprocess.DEVNULL)
        if r.returncode == 0:
            root = r.stdout.strip() or None
    except OSError:
        root = None
    _HOLDER[d] = root or planlib.repo_root(d)
    return _HOLDER[d]


def same_dir(a, b):
    """Two spellings of one directory. `os.path.samefile` and not a string
    compare: the board is reached as `.pearde` (a symlink to `pearde`) by
    one caller and by its real name by git, and both are the same root."""
    if not a or not b:
        return False
    if os.path.abspath(a) == os.path.abspath(b):
        return True
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def foot_places(p, board, board_root, repo):
    """Where one footprint spelling could resolve, in the order it is tried:
    the code repo first — a footprint is spelled relative to `repo` by
    contract — then the checkout that repo was cut from, then the board,
    then the board's own repo. The list is what a refusal prints, so the
    message names every place that was tried and nothing that was not.

    The second place is `spelling_root`, and it is a place only while a run
    session holds a tree: `repo` is then `<board>/.sessions/<id>`, and a
    board path the code repo ignores (`.pearde/.gitignore`) is not in a fresh
    worktree of it at all — no place would hold it and the footprint would
    fall through to the session tree. `spelling_root` is `repo` itself in
    every other case, and the dedupe below drops it, so a board with no
    session tries exactly the three places it always tried."""
    if os.path.isabs(p):
        return [os.path.abspath(p)]
    out = []
    for base in (repo, spelling_root(board, board_root, repo), board,
                 board_root):
        if not base:
            continue
        full = os.path.abspath(os.path.join(base, p))
        if full not in out:
            out.append(full)
    return out


def foot_root(p, board, board_root, repo):
    """`(root, path)` — the repo that HOLDS this footprint path, and its
    spelling inside that repo.

    A footprint is spelled relative to `repo`, the code repo. Since the
    board became a git repo of its own — `.pearde/` here, and every board
    carrying a `.git` — a path under the board is spelled the
    BOARD's way (`prds/<prd>/probe/verify.sh`, where every probe is told to
    live) or the code repo's way (`.pearde/.gitignore`), and either way it
    lives in NEITHER the code repo's index nor its worktree: the code repo
    ignores the board, so `git add -- .pearde/.gitignore` there is `fatal:
    pathspec … did not match any files`, which took down a whole lane's
    merge and every PRD gated behind it. This is the one place that answers
    which repo, so the lane's add, the guard's fence and step 3's grouping
    cannot disagree.

    The answer is git's, never a string's. Each place in `foot_places` is
    tried in order and the first one the filesystem or an index holds wins;
    `holder` says which checkout that is. The prefix test this replaced
    read "inside the board's path" as "the board's file", which is false
    the moment a code checkout is nested under the board — a lane, a
    run-session worktree — and every footprint of that repo was then routed
    to the board, staged against an index that ignores it, and committed as
    nothing at all.

    A footprint no place holds yet — the file a spec is about to create —
    resolves to the first place, so a spec that has not run yet groups
    under the code repo exactly as it always did."""
    known = [r for r in (repo, board_root, board) if r]

    def spell(root):
        for k in known:
            if same_dir(k, root):
                return k
        return root

    places = foot_places(p, board, board_root, repo)
    for full in places:
        root = holder(full)
        if not root:
            continue
        if not os.path.exists(full) and not tracked_in(root, full):
            continue
        root = spell(root)
        return root, os.path.relpath(full, root).replace(os.sep, "/")
    root = spell(holder(places[0]) or repo)
    return root, os.path.relpath(places[0], root).replace(os.sep, "/")


def tracked_in(root, full):
    """`full` is in `root`'s index though the working tree does not hold it —
    a footprint the spec deletes, or one a peer's checkout has not written.
    Asked only when nothing on disk answered, so it costs a fork per miss."""
    try:
        rel = os.path.relpath(full, root)
    except ValueError:
        return False
    if rel.startswith(".."):
        return False
    return bool(git_out(root, "ls-files", "-z", "--", rel).strip("\0"))


def under(parent, child):
    """Is `child` inside `parent`? By REAL path: a board upgraded by an
    older release is reached both as the legacy `pearde/` and through the
    `.pearde` symlink beside it, and a session tree named through one while the board
    is named through the other compares unequal under `abspath` and equal
    under `realpath`. A symlinked ancestor — `/tmp` on macOS — does the same
    to a board nothing links to."""
    p, c = os.path.realpath(parent), os.path.realpath(child)
    return c == p or c.startswith(p + os.sep)


def checkout_of(board, board_root):
    """The board's code repo by walk-up ALONE — `repo_of` with the session
    step left off. The checkout, in other words: the tree a session's own
    worktree was cut from."""
    if os.path.abspath(board_root) == os.path.abspath(board):
        return planlib.repo_root(os.path.dirname(board_root)) or board_root
    return board_root


def spelling_root(board, board_root, repo):
    """The second place `foot_places` tries a footprint's spelling.

    Normally `repo` itself, and then it is not a second place at all. But a
    session's worktree lives at `<board>/.sessions/<id>` — under the board,
    the way a lane lives under it — and `repo` is that worktree once a
    session holds one. A worktree of the code repo does not carry the paths
    that repo ignores, and the board is one of them: `.pearde/.gitignore` is
    absent from `<board>/.sessions/<id>/.pearde/` and from the board's own
    tree, so no place holds it and the footprint falls through to the
    session tree, which does not hold it either.

    A worktree and the checkout it was cut from spell every tracked path
    identically — that is what makes them the same repo — so asking the
    checkout as well costs nothing where the session tree already answered,
    and is the only place that answers for a path the code repo ignores.

    STRICTLY under, and neither the board nor the board's own repo. A board
    that is its own code repo — `repo` and `board` one directory — is under
    itself by `under`'s own equality arm, and answering the enclosing
    checkout there routes a footprint the board genuinely holds out of it:
    measured against `the-verify-guard-parses-git-s-own-output-before-it-
    trusts-it`, `resources/board/collect.py` left the board for the repo one
    level up and came back spelled `../../../../../../..`. The case this
    exists for is a tree cut BELOW the board, which is a session's and a
    lane's alone."""
    if not repo or same_dir(repo, board) or same_dir(repo, board_root):
        return repo
    return checkout_of(board, board_root) if under(board, repo) else repo


def owned_by(prd, board_root, repo, feet, board=None):
    """{root: [paths relative to that root]} this PRD owns — the same
    grouping `sort_paths` makes for what it is about to commit, so the guard
    and the commit agree on one answer to "whose is this?".

    A footprint path is spelled relative to `repo`, NOT to `board_root`:
    `sort_paths` resolves every one of them as `os.path.join(repo, p)`. The
    two roots are the same only where the board is not its own git repo. On
    a board that IS one — this repo, and every board carrying a `.git` of
    its own — `repo_of` returns the enclosing
    checkout and they differ, so a footprint rebased against `board_root`
    names a path that exists in neither root: the file under test then reads
    as foreign, gets parked, and the verify block measures a clean HEAD
    instead of the change it was written to measure.

    The board's own root also owns the PRD's directory, exactly as
    `sort_paths` seeds `groups` with it — a verify block that writes its
    proof under `prds/<prd>/` is writing where this PRD already commits.
    `spec_data` qualifies a member PRD's footprint with its member sigil;
    it comes off here for the PRD's own board and a path carrying another
    member's sigil is left out, both as `sort_paths` does it."""
    own = (f"{planlib.MEMBER_SIGIL}{prd['board']}/"
           if prd.get("board") else None)
    groups = {}
    prd_rel = os.path.relpath(prd["dir"], board_root)
    if not prd_rel.startswith(".."):
        groups[os.path.abspath(board_root)] = {prd_rel}
    for f in feet:
        if own and f.startswith(own):
            p = f[len(own):]
        elif not f.startswith(planlib.MEMBER_SIGIL):
            p = f
        else:
            continue
        # a footprint path under a board that is its own repo is the board
        # repo's, spelled its way — `foot_root` is the one answer to that
        root, p = foot_root(p, board or board_root, board_root, repo)
        groups.setdefault(os.path.abspath(root), set()).add(p)
    groups.setdefault(os.path.abspath(repo), set())
    return {k: sorted(v) for k, v in groups.items()}


def _park(cwd, feet, out=print):
    # This `stash push -u` is NOT one of the four commands
    # `a-session-that-writes-a-shared-checkout-can-revert-another-session-s-
    # work` puts out of bounds, and @resources/board/refuse.py is deliberately
    # not consulted here. It is a stash-then-POP pair, and the pop is in
    # `guarded_run`'s `finally`: its whole purpose is to move a PEER's dirt
    # out of the verify block's reach and put it back afterwards.
    #
    # Measured, and the measurement is why this comment exists: putting this
    # call under the refusal flipped four checks of
    # `prds/collect-must-not-reset-the-checkout-it-did-not-write` from pass to
    # fail — "the neighbour's uncommitted work is still there" stopped being
    # true, because the verify block then ran over it. Refusing a protective
    # stash destroys exactly the work the refusal exists to protect.
    #
    # A `stash` a session TYPES has no matching pop, which is why the shell
    # half refuses that one and this one stands.
    foreign = sorted({p for _, p in _dirty(cwd) if not inside(p, feet)})
    if not foreign:
        return False
    r = subprocess.run(["git", "-C", cwd, "stash", "push",
                        "--include-untracked", "-u",
                        "-m", "collect: parked foreign dirt for verify",
                        "--"] + foreign, capture_output=True, text=True)
    if r.returncode != 0:
        out(f"  could not park foreign dirt in {cwd} before verify — "
           f"running unguarded: {(r.stderr or r.stdout).strip()}")
        return False
    return "No local changes to save" not in (r.stdout + r.stderr)


def _aside(cwd):
    """A directory to hold what `_heal` takes out of the checkout, inside the
    git dir so it is outside the working tree — never committed, never seen by
    a later block, never cleaned. Resolved through git so a worktree, whose
    `.git` is a file, lands somewhere real."""
    r = subprocess.run(["git", "-C", cwd, "rev-parse", "--absolute-git-dir"],
                       capture_output=True, text=True)
    base = r.stdout.strip() if r.returncode == 0 and r.stdout.strip() \
        else os.path.join(os.path.abspath(cwd), ".git")
    d = os.path.join(base, "collect-aside",
                     datetime.datetime.now().strftime("%y%m%d-%H%M%S-%f"))
    os.makedirs(d, exist_ok=True)
    return d


def _take_aside(cwd, rel, aside):
    """Move one path's current bytes out of the checkout, keeping them.
    Returns where they went, or None if the move failed."""
    src = os.path.join(cwd, rel)
    dst = os.path.join(aside, rel)
    try:
        os.makedirs(os.path.dirname(dst) or aside, exist_ok=True)
        shutil.move(src, dst)
    except (OSError, shutil.Error):
        return None
    return dst


def _head_blob(cwd, rel):
    """`(bytes, mode)` HEAD holds for `rel`, or `(None, None)` if HEAD has no
    such path. Read rather than checked out: `git checkout HEAD -- <p>` writes
    the INDEX too, which is where a peer's staging lives."""
    r = subprocess.run(["git", "-C", cwd, "ls-tree", "-z", "HEAD", "--", rel],
                       capture_output=True, text=True)
    rec = r.stdout.split("\0")[0] if r.returncode == 0 else ""
    if not rec or "\t" not in rec:
        return None, None
    meta = rec.split("\t", 1)[0].split()
    if len(meta) < 3 or meta[1] != "blob":
        return None, None
    b = subprocess.run(["git", "-C", cwd, "cat-file", "blob", meta[2]],
                       capture_output=True)
    if b.returncode != 0:
        return None, None
    try:
        mode = int(meta[0], 8) & 0o7777
    except ValueError:
        mode = 0o644
    return b.stdout, mode


def _heal(cwd, feet, out=print):
    """Put the checkout outside this PRD's footprint back the way the block
    found it — **without deleting anything, and without saying it put back
    what it did not.**

    Pass one reached for `git clean -f -d` on a foreign untracked path and
    `git reset -q HEAD --` on a foreign tracked one, checked no returncode,
    and printed `put back:` over the whole row set regardless. Both reaches
    are wrong for the same reason: this board is written by several sessions
    at once, so a foreign path dirty AFTER the block is a peer's live work as
    readily as it is the block's litter, and nothing here can tell the two
    apart. `clean` deleted a peer's new file outright and the stash pop, which
    never held it, could not bring it back.

    So nothing is deleted. What the block left is moved out of the checkout
    with its bytes intact and its new home printed, and a path HEAD knows is
    written back from HEAD's blob — read and written here rather than
    `git checkout`ed, because checkout writes the index and a peer's staged
    entry is not this block's to discard. The index is left exactly as it is;
    `collect` commits through its own private index, so a foreign entry left
    staged reaches no commit of ours. Returns the paths actually put back."""
    rows = [(c, p) for c, p in _dirty(cwd) if not inside(p, feet)]
    if not rows:
        return []
    aside, moved, back, failed, staged = None, [], [], [], []
    for code, rel in rows:
        # `code[0]` is the INDEX column. Anything but a space or a `?` there
        # means someone ran `git add` on this path inside the verify window,
        # and staging a foreign path is a peer's deliberate act far more often
        # than a verify block's accident. Such a path is left exactly as it
        # is — worktree and index both — and named. `collect` builds its
        # commits in a private index, so what stays staged here reaches no
        # commit of ours.
        if code[0] not in " ?":
            staged.append(rel)
            continue
        full = os.path.join(cwd, rel)
        if os.path.exists(full) or os.path.islink(full):
            aside = aside or _aside(cwd)
            dst = _take_aside(cwd, rel, aside)
            if dst is None:
                failed.append(rel)
                continue
            moved.append(rel)
        data, mode = _head_blob(cwd, rel)
        if data is None:
            continue                      # HEAD never had it — nothing to put
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        try:
            with open(full, "wb") as f:
                f.write(data)
            os.chmod(full, mode)
        except OSError:
            failed.append(rel)
            continue
        back.append(rel)
    if back:
        out(f"  verify touched the checkout outside its footprint in {cwd} — "
            f"put back: {', '.join(back)}")
    if moved:
        out(f"  and what it left there is not deleted — moved aside to "
            f"{aside}: {', '.join(moved)}")
    if staged:
        out(f"  left staged in {cwd} (a peer's index is not ours to reset): "
            f"{', '.join(staged)}")
    if failed:
        out(f"  NOT put back in {cwd} — restore by hand: "
            f"{', '.join(sorted(set(failed)))}")
    return back


# ── and the one thing the fence deliberately leaves outside it ───────────────
# The PRD's own footprint is never parked: on the laneless path it IS the
# uncommitted change the verify block exists to measure, and parking it would
# make every block read a clean HEAD. The cost of that decision is that a
# green block which empties the working tree takes the work under test with
# it, `collect` then commits the deletion and writes `done` — recoverable
# from HEAD on a lane run, gone on the laneless path.
#
# `_snapshot` closes that without re-parking anything: the bytes and mode of
# every owned path that exists on disk before the block, and `_unerase` puts
# back only the ones the block made ABSENT. A path the block modifies stays
# modified (a formatter or a build step editing the file under test is
# legitimate, and indistinguishable from the change itself); a path it
# creates stays created; a path the worker had already deleted before the
# block — a spec whose finish is a deletion, which `sort_paths` supports —
# was never on disk, so was never snapshotted, and is never resurrected.
def _owned_files(cwd, scoped):
    """The paths under `scoped` that exist on disk — a footprint entry may be
    a directory, and only what is there is snapshotted.

    A symlink counts. Pass one skipped every one of them, so a footprint
    symlink a block deleted was never put back — and this repo's own `.pearde`
    is a symlink, which makes that the live shape rather than a corner. A link
    is snapshotted by its TARGET STRING, never by what it points at: following
    it would copy the whole tree below it, and re-creating it is one
    `os.symlink`. `os.walk` is left with `followlinks=False`, so a linked
    directory under a footprint is recorded as the link it is and never
    descended into twice."""
    files = []
    for rel in scoped:
        full = os.path.join(cwd, rel)
        if os.path.islink(full):
            files.append(rel)
            continue
        if os.path.isfile(full):
            files.append(rel)
        elif os.path.isdir(full):
            for root, dirs, names in os.walk(full):
                for d in dirs:
                    f = os.path.join(root, d)
                    if os.path.islink(f):
                        files.append(os.path.relpath(f, cwd))
                dirs[:] = [d for d in dirs
                           if d != ".git" and
                           not os.path.islink(os.path.join(root, d))]
                for n in names:
                    f = os.path.join(root, n)
                    if os.path.islink(f) or os.path.isfile(f):
                        files.append(os.path.relpath(f, cwd))
    return sorted(set(files))


def _blobs(cwd, scoped):
    """{path: index blob sha} for the owned paths git already holds bytes
    for. The pathspec is the footprint, never the file list, so a directory
    footprint costs one call however many files are under it."""
    if not scoped:
        return {}
    r = subprocess.run(["git", "-C", cwd, "ls-files", "-s", "-z", "--"] +
                       list(scoped), capture_output=True, text=True)
    out = {}
    for rec in r.stdout.split("\0"):
        if not rec or "\t" not in rec:
            continue
        meta, path = rec.split("\t", 1)
        bits = meta.split()
        if len(bits) >= 2:
            out[path] = bits[1]
    return out


def _snapshot(cwd, scoped):
    """{path: (kind, payload, mode)} for every owned file on disk.

    The size guard is `kind`. A path that is tracked and clean has its bytes
    in git already, so the snapshot is a 40-character blob name and a
    footprint naming a large directory is not copied at all ("blob"). Only a
    path git does not hold the current bytes of — dirty, staged, or entirely
    untracked — is read into memory ("copy")."""
    files = _owned_files(cwd, scoped)
    if not files:
        return {}
    indexed = _blobs(cwd, scoped)
    moved = {p for _, p in _dirty(cwd)}
    snap = {}
    for rel in files:
        full = os.path.join(cwd, rel)
        if os.path.islink(full):
            # a third kind: the target STRING, not what it points at. `stat`
            # would follow it, and a dangling link would drop out here.
            try:
                snap[rel] = ("link", os.readlink(full), 0)
            except OSError:
                pass
            continue
        try:
            mode = os.stat(full).st_mode & 0o7777
        except OSError:
            continue
        if rel in indexed and rel not in moved:
            snap[rel] = ("blob", indexed[rel], mode)   # git holds the bytes
            continue
        try:
            with open(full, "rb") as f:
                snap[rel] = ("copy", f.read(), mode)   # nothing else does
        except OSError:
            continue
    return snap


def _reverted(cwd, rel, kind, payload):
    """True when the block put HEAD's own bytes back over the PRD's
    uncommitted work at `rel`.

    `spec02` decided that a path the block MODIFIES stays modified: a
    formatter or a build step editing the file under test is legitimate and
    indistinguishable from the change itself. `git reset --hard HEAD` is
    distinguishable, and it is the shape of the incident this whole guard is
    filed from — the file is byte-for-byte HEAD again, and the snapshot holds
    something else. Nothing else lands exactly on HEAD by accident. Only a
    `copy` snapshot can be reverted: a `blob` one already agreed with what
    git holds, and a `link` has no blob to be reset to."""
    if kind != "copy":
        return False
    head, _ = _head_blob(cwd, rel)
    if head is None or head == payload:
        return False
    try:
        with open(os.path.join(cwd, rel), "rb") as f:
            return f.read() == head
    except OSError:
        return False


def _unerase(cwd, snap, out=print):
    """Put back each owned path the block made absent — or reverted to HEAD —
    and name it, the shape `_heal`'s line already takes."""
    back = []
    for rel in sorted(snap):
        full = os.path.join(cwd, rel)
        kind, payload, mode = snap[rel]
        there = os.path.exists(full) or os.path.islink(full)
        if there and not _reverted(cwd, rel, kind, payload):
            continue
        if kind == "link":
            try:
                if there:
                    os.unlink(full)
                os.makedirs(os.path.dirname(full) or cwd, exist_ok=True)
                os.symlink(payload, full)
            except OSError as e:
                out(f"  verify deleted the link {rel} in {cwd} and it could "
                    f"not be put back: {e}")
                continue
            back.append(rel)
            continue
        if kind == "blob":
            r = subprocess.run(["git", "-C", cwd, "cat-file", "blob",
                                payload], capture_output=True)
            if r.returncode != 0:
                out(f"  verify deleted {rel} in {cwd} and its blob "
                    f"{payload[:12]} is gone — not put back")
                continue
            data = r.stdout
        else:
            data = payload
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        try:
            with open(full, "wb") as f:
                f.write(data)
            os.chmod(full, mode)
        except OSError as e:
            out(f"  verify deleted {rel} in {cwd} and it could not be put "
                f"back: {e}")
            continue
        back.append(rel)
    if back:
        out(f"  verify deleted this PRD's own work in {cwd} — "
            f"put back: {', '.join(back)}")
    return back


def _head_of(cwd):
    r = subprocess.run(["git", "-C", cwd, "symbolic-ref", "-q", "HEAD"],
                       capture_output=True, text=True)
    ref = r.stdout.strip() if r.returncode == 0 else "HEAD"
    sha = subprocess.run(["git", "-C", cwd, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return ref, sha


def _restore_head(cwd, ref, old_sha, out=print):
    _, now_sha = _head_of(cwd)
    if now_sha == old_sha or not now_sha:
        return
    r = subprocess.run(["git", "-C", cwd, "update-ref", ref, old_sha,
                        now_sha], capture_output=True, text=True)
    if r.returncode != 0:
        out(f"  verify moved {ref} in {cwd} and it could not be put back "
           f"({now_sha[:12]} -> {old_sha[:12]}): "
           f"{(r.stderr or r.stdout).strip()}")
        return
    out(f"  verify moved {ref} in {cwd} — put back at {old_sha[:12]}")


def _reattach(here):
    """Stand the process back in the directory it was invoked from.

    `_park` stashes the foreign dirt, and `git stash push -u` REMOVES a
    directory its last untracked file leaves empty — including, when
    `collect` was called from a subdirectory of the checkout it is guarding,
    the process's own cwd. The pop makes the path again, but the process
    still holds the deleted inode: `os.getcwd()`, `os.path.abspath()` and
    every relative open then raise `FileNotFoundError` for the rest of the
    run. `--also <relative path>` resolves against the caller's cwd, so this
    took out the whole call. Cheap to undo, and undone in the same `finally`
    that puts the rest of the checkout back."""
    if here is None:
        return
    try:
        os.getcwd()
        return
    except OSError:
        pass
    try:
        os.chdir(here)
    except OSError:
        pass


def guarded_run(cmd, cwd, owned, script=None, out=print):
    """`run()`, fenced: nothing this PRD does not own in `cwd` can be
    reached, left changed, or have its branch moved by `cmd` — and nothing
    this PRD DOES own can be left deleted by it.

    `owned` is `owned_by`'s dict. A `cwd` it has no row for owns nothing
    there, so everything dirty is parked — the safe reading, never the
    permissive one."""
    scoped = owned.get(os.path.abspath(cwd), [])
    try:
        here = os.getcwd()
    except OSError:
        here = None
    parked = _park(cwd, scoped, out)
    # the footprint stays in the tree for the block to measure; what it
    # cannot do is leave it deleted
    snap = _snapshot(cwd, scoped)
    ref, old_sha = _head_of(cwd)
    try:
        return run(cmd, cwd, script)
    finally:
        _restore_head(cwd, ref, old_sha, out)
        _heal(cwd, scoped, out)
        _unerase(cwd, snap, out)
        if parked:
            r = subprocess.run(["git", "-C", cwd, "stash", "pop"],
                               capture_output=True, text=True)
            if r.returncode != 0:
                out(f"  foreign dirt not restored in {cwd} — stash pop "
                   f"conflict; resolve by hand: git -C {cwd} stash list")
        _reattach(here)


# ── the private index ─────────────────────────────────────────────────────────
# The checkout's index is shared by every session in it, and `git commit`
# commits the whole index — so a landing carried whatever a sibling had
# staged. collect builds its commits in an index of its own: `read-tree HEAD`
# into a scratch file, its own `add` / `update-index` there, `write-tree`,
# `commit-tree`, and `update-ref <ref> <new> <expected-old>` — refused when a
# sibling moved HEAD in between. The one write to the shared index is
# path-scoped, after the ref moved: `reset -q -- <the paths committed>`, so
# their entries read HEAD's blob — left stale, a sibling's next plain
# `git commit` would carry the old blob and revert the landing.
INDEX = {}                      # root → the scratch index while one is open
BASE = {}                       # root → the HEAD that index was read from


def git_out(root, *args, input=None, shared=False):
    env = None
    if root in INDEX and not shared:
        env = dict(os.environ, GIT_INDEX_FILE=INDEX[root])
    r = subprocess.run(("git", "-C", root) + args, capture_output=True,
                       text=True, input=input, env=env)
    if r.returncode != 0:
        raise Stop(f"git {args[0]} failed in {root}: "
                   f"{(r.stderr or r.stdout).strip()}")
    return r.stdout


class private_index:
    """`with private_index(roots):` — every `git_out` on those roots reads
    and writes a scratch index seeded from HEAD, dropped on exit."""

    def __init__(self, roots):
        self.roots, self.dir = list(roots), None

    def __enter__(self):
        self.dir = tempfile.mkdtemp(prefix="pearde-index-")
        for i, root in enumerate(self.roots):
            INDEX[root] = os.path.join(self.dir, f"index-{i}")
            BASE[root] = git_out(root, "rev-parse", "HEAD").strip()
            git_out(root, "read-tree", BASE[root])
        return self

    def __exit__(self, *exc):
        for root in self.roots:
            INDEX.pop(root, None)
            BASE.pop(root, None)
        shutil.rmtree(self.dir, ignore_errors=True)
        return False


def commit_private(root, message):
    """The private index as one commit on the current branch: write-tree,
    commit-tree on the HEAD the index was read from, update-ref expecting
    that same HEAD — one a sibling moved meanwhile is a Stop, nothing
    written, since the tree was built without their commit. Returns the
    short sha; the next commit in the same index follows this one."""
    old = BASE[root]
    tree = git_out(root, "write-tree").strip()
    new = git_out(root, "commit-tree", tree, "-p", old, input=message).strip()
    r = subprocess.run(["git", "-C", root, "symbolic-ref", "-q", "HEAD"],
                       capture_output=True, text=True)
    ref = r.stdout.strip() if r.returncode == 0 else "HEAD"
    r = subprocess.run(["git", "-C", root, "update-ref", ref, new, old],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise Stop(f"HEAD moved under collect in {root} — another session "
                   f"committed; nothing written, run collect again: "
                   f"{(r.stderr or r.stdout).strip()}")
    BASE[root] = new
    return new[:7]


def settle_shared(root, paths):
    """After the ref moved: the shared index's entries for the paths just
    committed now read HEAD's blob — the one path-scoped write to it."""
    if paths:
        git_out(root, "reset", "-q", "--", *paths, shared=True)


def dirty_paths(root):
    """{path: "tracked" | "untracked" | "rename-source"} for every path
    `git status` reports, relative to `root`. `-uall` so an untracked
    directory is its files, and `-z` so a space in a name is not two names.
    A rename or a copy reports two paths — the new one under its own XY,
    the original under `rename-source` — so a caller staging one side by
    side the other does not lose the deletion a rename's old path carries."""
    raw = git_out(root, "status", "--porcelain", "-uall", "-z")
    out, items, i = {}, raw.split("\0"), 0
    while i < len(items):
        ent = items[i]
        i += 1
        if not ent:
            continue
        xy, path = ent[:2], ent[3:]
        out[path] = "untracked" if xy == "??" else "tracked"
        if xy[0] in "RC":          # the original follows as its own entry
            out[items[i]] = "rename-source"
            i += 1
    return out


def inside(path, union):
    return any(path == u or path.startswith(u + "/") for u in union)


def board_prefix(board, board_root):
    """How the board is spelled inside its OWN repo's paths: `"pearde"` on
    a board nested in the code repo, and `""` on a board that IS its repo.

    `os.path.relpath` answers `"."` for the second case, and `"."` is a
    prefix of no path git ever prints — `inside(p, ["."])` is False for
    every one of them, `scratch` then swallows nothing and the rider sweep
    fires on nothing. That is the third wrong board-path resolution, after
    the two `foot_root` replaced; `""` is the honest answer and
    `under_board` is the one reader of it."""
    b, r = os.path.abspath(board), os.path.abspath(board_root)
    return "" if b == r else os.path.relpath(b, r).replace(os.sep, "/")


def under_board(path, board_rel):
    """`path` respelled relative to the BOARD, or None when it is not under
    the board at all. `path` is relative to the board's own repo root.

    On a board that is its own repo `board_rel` is `""` and every path in
    that repo is under the board, spelled exactly as it stands — which is
    why this is a function and not `inside(path, [board_rel])` plus
    `path[len(board_rel) + 1:]`: that arithmetic chops a character off
    every name the moment the prefix is empty."""
    if board_rel == "":
        return path
    if path == board_rel:
        return ""
    if path.startswith(board_rel + "/"):
        return path[len(board_rel) + 1:]
    return None


def scratch(path, board_rel):
    """A dotfile directly under the board — `.claims/`, `.pass.md`,
    `.history.jsonl`, `.plan.json` — is machine-local and never committed."""
    rest = under_board(path, board_rel)
    return rest is not None and rest.startswith(".")


def split_hunks(diff):
    """{path: (header, [hunk])} from `git diff` output. A hunk is its text
    from `@@` to the next `@@` or file header."""
    files = {}
    for block in re.split(r"(?m)^(?=diff --git )", diff):
        if not block.strip():
            continue
        m = re.search(r"(?m)^\+\+\+ b/(.*)$", block)
        if not m:
            continue
        head, _, rest = block.partition("\n@@")
        hunks = [h for h in re.split(r"(?m)^(?=@@ )", "@@" + rest)
                 if h.strip()] if rest else []
        files[m.group(1)] = (head + "\n", hunks)
    return files


def hunk_body(h):
    """A hunk without its `@@` header — the header's line numbers move when
    another hunk lands above it, the body does not."""
    return h.split("\n", 1)[1] if "\n" in h else ""


def hunk_sides(body):
    """`([minus], [plus])` — a hunk body's two sides, marker stripped, the
    `\\ No newline` note dropped. Lists, in order: a merged hunk holds one
    author's lines and then the other's."""
    minus, plus = [], []
    for line in body.split("\n"):
        if line.startswith("-"):
            minus.append(line[1:])
        elif line.startswith("+"):
            plus.append(line[1:])
    return minus, plus


def sublist(part, whole):
    """True when `part` is a contiguous run of `whole`, `part` non-empty."""
    n = len(part)
    return bool(part) and any(whole[i:i + n] == part
                              for i in range(len(whole) - n + 1))


def two_authors(kept, old_bodies):
    """The working line of the first kept hunk that swallowed a baseline
    hunk, or None. `git diff -U0` merges two edits on adjacent lines into
    one hunk; when one of them was in the claim's baseline, that baseline
    hunk is gone from the diff and its lines sit inside a kept hunk — a
    body that matches neither the baseline nor the worker's own edit, so
    nothing here can say which lines are whose. Line-level splitting is
    not attempted: the file is refused, and `--widen` or one untouched
    line between the edits is the worker's answer."""
    gone = [hunk_sides(b) for b in old_bodies]
    for h in kept:
        minus, plus = hunk_sides(hunk_body(h))
        for om, op in gone:
            if (op and not sublist(op, plus)) or (om and not sublist(om, minus)):
                continue
            if not (op or om):
                continue
            m = HUNK_HEAD.match(h)
            return int(m.group(3)) if m else 0
    return None


HUNK_HEAD = re.compile(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
PARSERS = {".py": ["python3", "-m", "py_compile"],
           ".js": ["node", "--check"], ".mjs": ["node", "--check"],
           ".cjs": ["node", "--check"]}


def parse_hunk(h):
    """{"old": (start, len), "new": (start, len), "minus": [line], "plus":
    [line]} from one `-U0` hunk. Every line keeps its newline except one the
    file has none on (`\\ No newline at end of file`). A context line, should
    one appear, is on both sides."""
    head, _, body = h.partition("\n")
    m = HUNK_HEAD.match(head)
    if not m:
        raise Stop(f"unreadable hunk header: {head!r}")
    old = (int(m.group(1)), 1 if m.group(2) is None else int(m.group(2)))
    new = (int(m.group(3)), 1 if m.group(4) is None else int(m.group(4)))
    minus, plus, last = [], [], []
    for line in body.split("\n"):
        if not line:
            continue
        kind, text = line[0], line[1:] + "\n"
        if kind == "\\":
            for side in last:
                side[-1] = side[-1][:-1]
            continue
        last = {"-": [minus], "+": [plus], " ": [minus, plus]}.get(kind)
        if last is None:
            raise Stop(f"unreadable hunk line: {line!r}")
        for side in last:
            side.append(text)
    if len(minus) != old[1] or len(plus) != new[1]:
        raise Stop(f"hunk {head!r} says {old[1]}/{new[1]} lines and "
                   f"carries {len(minus)}/{len(plus)}")
    return {"old": old, "new": new, "minus": minus, "plus": plus}


def reverse_hunks(text, hunks):
    """`text` — the working file — with every hunk in `hunks` undone, from
    the bottom up so the line numbers above each stay true. The hunks' new
    side is `text`'s own coordinates: a `+N,0` hunk puts its `-` lines back
    after line N; any other hunk holds `text`'s lines N..N+len-1 as its `+`
    lines, checked before they are replaced by its `-` lines. Nothing here
    re-derives a position from a patch's old side."""
    lines = text.splitlines(keepends=True)
    parsed = sorted((parse_hunk(h) for h in hunks),
                    key=lambda p: p["new"][0], reverse=True)
    for a, b in zip(parsed, parsed[1:]):
        if a["new"][0] == b["new"][0]:
            raise Stop(f"two hunks start at line {a['new'][0]} of the "
                       f"working file — the diff is not one this reader "
                       f"understands")
    for p in parsed:
        start, n = p["new"]
        at = start if n == 0 else start - 1
        have = lines[at:at + n]
        if have != p["plus"]:
            raise Stop(f"line {start} of the working file is not what its "
                       f"hunk says: {have!r} against {p['plus']!r}")
        lines[at:at + n] = p["minus"]
    return "".join(lines)


def misplaced(staged, kept, foreign, working_len):
    """Where the staged blob disagrees with the working file: one line per
    kept hunk whose `+` lines are not at the working position minus the
    lines the foreign hunks above it hold, and one when the blob's length
    is not the working file's minus the foreign hunks'. [] is placement
    proven; an exit code of `git apply` never is."""
    lines = staged.splitlines(keepends=True)
    fs = [parse_hunk(h) for h in foreign]
    out = []
    want = working_len - sum(f["new"][1] - f["old"][1] for f in fs)
    if len(lines) != want:
        out.append(f"the staged blob holds {len(lines)} lines, the working "
                   f"file minus the inherited hunks holds {want}")
    for k in (parse_hunk(h) for h in kept):
        start, n = k["new"]
        shift = sum(f["new"][1] - f["old"][1] for f in fs
                    if f["new"][0] < start)
        at = start - shift
        if n == 0:
            if lines[at:at + k["old"][1]] == k["minus"]:
                out.append(f"hunk @@ +{start},0: its removed lines still "
                           f"sit after line {at} of the staged blob")
            continue
        have = lines[at - 1:at - 1 + n]
        if have != k["plus"]:
            where = [i + 1 for i in range(len(lines))
                     if lines[i:i + n] == k["plus"]]
            out.append(f"hunk @@ +{start},{n}: expected at line {at} of "
                       f"the staged blob, found at "
                       f"{', '.join(map(str, where)) or 'no line'}")
    return out


def parse_error(path, text):
    """What the parser for `path`'s suffix says of `text`, "" when it
    parses or no parser is on this machine."""
    cmd = PARSERS.get(os.path.splitext(path)[1])
    if not cmd or not shutil.which(cmd[0]):
        return ""                  # no parser here — nothing to say
    d = os.path.realpath(tempfile.mkdtemp())   # a parser prints the real path
    try:
        tmp = os.path.join(d, os.path.basename(path))
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        code, output = run(cmd + [tmp], d)
        return output.replace(tmp, path).strip() if code else ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


def stage_by_hunk(root, path, foreign):
    """Stage `path` as the working file with the inherited hunks reversed:
    hash the rebuilt text, point the index at it. Returns the text staged."""
    with open(os.path.join(root, path), encoding="utf-8") as f:
        work = f.read()
    blob = reverse_hunks(work, foreign)
    sha = git_out(root, "hash-object", "-w", "--stdin", "--path", path,
                  input=blob).strip()
    entry = git_out(root, "ls-files", "-s", "--", path).split()
    mode = entry[0] if entry else "100644"
    git_out(root, "update-index", "--cacheinfo", f"{mode},{sha},{path}")
    return work, blob


def placement_refusals(root, partial, staged):
    """Every reason not to commit what step 3 staged by hunk: a blob that
    does not parse, or a kept hunk not at its place. `staged` is
    {path: (working text, staged text)}."""
    out = []
    for path, (kept, foreign) in partial.items():
        work, _ = staged[path]
        blob = git_out(root, "show", f":{path}")
        err = parse_error(path, blob)
        if err:
            out.append(f"{path}: the staged blob does not parse — {err}")
        for m in misplaced(blob, kept, foreign,
                           len(work.splitlines(keepends=True))):
            out.append(f"{path}: {m}")
    return out


# ── the baseline ──────────────────────────────────────────────────────────────

def claims_dir(board, rel):
    return os.path.join(board, CLAIMS_DIR, rel)


def snapshot(board, rel, gate=None):
    """Record what is dirty and what the gate says at `claim:` — the
    baseline step 3 and the gate are measured against. Called by `claim`;
    `collect --snapshot <prd>` is the same call by hand.

    TWO repos, not one. `repo_root(prd["dir"])` is the BOARD's repo, and on
    every layout this board ships on — a nested `.pearde` with a `.git` of
    its own, or a linked worktree at `.pearde`, which is what this machine
    runs — that is not the repo the code lives in. A baseline that records
    only the board's dirt can never explain a single code path, so step 3's
    hunk-splitter finds nothing inherited and commits every footprint file
    whole. `repo_of` gives the code repo; when it differs from the board's
    it is snapshotted too, into `diff.repo` / `untracked.repo`, and `repo`
    holds its path. A claim dir written before this holds only the board
    side, and `baseline` reads it as it always did."""
    prds = planlib.scan(board)
    prd = prds.get(rel)
    if not prd:
        raise Stop(f"{rel}: no PRD at that path")
    root = planlib.repo_root(prd["dir"])
    if not root:
        raise Stop(f"{rel}: not inside a git repo")
    d = claims_dir(board, rel)
    os.makedirs(d, exist_ok=True)

    def record(r, suffix):
        dirty = dirty_paths(r)
        with open(os.path.join(d, "diff" + suffix), "w",
                  encoding="utf-8") as f:
            f.write(git_out(r, "diff", "HEAD", "-U0", "--no-color"))
        with open(os.path.join(d, "untracked" + suffix), "w",
                  encoding="utf-8") as f:
            f.write("".join(p + "\n" for p, k in sorted(dirty.items())
                            if k == "untracked"))

    record(root, "")
    code = repo_of(prd, board, root)
    # The lane, when the claim cut one. `transition` calls `cut_lane` and
    # then this, so the worktree is already on disk. The worker writes
    # THERE and not in the checkout, so the code side of the baseline has
    # to be the lane's tree: a baseline taken in the checkout describes a
    # tree the worker never touches, and step 2's `known — every line is
    # in the claim's baseline` softening would then be reading somebody
    # else's dirt. A board with no lane keeps the checkout, as before.
    import lanes as laneslib
    if code and laneslib.exists(board, rel):
        code = laneslib.lane_dir(board, rel)
    for name in ("diff.repo", "untracked.repo", "repo"):
        stale = os.path.join(d, name)          # a re-snapshot never inherits
        if os.path.isfile(stale):              # the last one's second side
            os.remove(stale)
    if code and code != root:
        record(code, ".repo")
        with open(os.path.join(d, "repo"), "w", encoding="utf-8") as f:
            f.write(code + "\n")
    gate = (str(planlib.board_settings(board).get("gate", "") or "").strip()
            if gate is None else gate)
    code, output = (run(["bash", "-e", "-o", "pipefail"], root, gate)
                    if gate else (0, ""))
    with open(os.path.join(d, "gate"), "w", encoding="utf-8") as f:
        f.write(f"exit {code}\n{output}")
    with open(os.path.join(d, "at"), "w", encoding="utf-8") as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    return d


def baseline(board, rel):
    """What `snapshot` recorded, or None. `sides` is keyed `board` and
    `repo` — the two repos `snapshot` records — each `{"hunks", "untracked"}`
    in that repo's own relative paths. A claim dir written before the code
    repo was recorded carries no `repo` side, and every caller reads that as
    "no baseline for this root", which is the behaviour it always had."""
    d = claims_dir(board, rel)
    if not os.path.isfile(os.path.join(d, "diff")):
        return None
    rd = lambda n: open(os.path.join(d, n), encoding="utf-8").read()  # noqa
    gate = rd("gate") if os.path.isfile(os.path.join(d, "gate")) else ""
    m = re.match(r"exit (\d+)\n", gate)

    def side(suffix):
        return {"hunks": {p: {hunk_body(h) for h in hs}
                          for p, (_, hs) in
                          split_hunks(rd("diff" + suffix)).items()},
                "untracked": set(rd("untracked" + suffix).split())}

    sides = {"board": side("")}
    if os.path.isfile(os.path.join(d, "diff.repo")):
        sides["repo"] = side(".repo")
    # `hunks` and `untracked` at the top are the board side under the names
    # they had before there were two, for the readers written against the
    # one-repo shape. On a board that is not its own repo — board and code
    # are one root — they are the whole baseline, exactly as before.
    return {"sides": sides,
            "hunks": sides["board"]["hunks"],
            "untracked": sides["board"]["untracked"],
            "gate_exit": int(m.group(1)) if m else 0,
            "gate_lines": set(gate.splitlines()[1:]) if m else set()}


def owe(board, path):
    """List a board-repo path the tool wrote after the commit it belongs to
    — it rides the next collect."""
    p = os.path.join(board, CLAIMS_DIR, RIDERS_FILE)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    have = set(open(p, encoding="utf-8").read().split()) \
        if os.path.isfile(p) else set()
    if path not in have:
        with open(p, "a", encoding="utf-8") as f:
            f.write(path + "\n")


def owed(board):
    p = os.path.join(board, CLAIMS_DIR, RIDERS_FILE)
    return set(open(p, encoding="utf-8").read().split()) \
        if os.path.isfile(p) else set()


def settle(board, paths):
    p = os.path.join(board, CLAIMS_DIR, RIDERS_FILE)
    keep = owed(board) - set(paths)
    if os.path.isfile(p):
        with open(p, "w", encoding="utf-8") as f:
            f.write("".join(x + "\n" for x in sorted(keep)))


# ── daemon ────────────────────────────────────────────────────────────────────

def daemon_call(path, payload=None, timeout=3):
    port = os.environ.get("PEARDE_PORT", "8443")
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}",
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Content-Type": "application/json"},
        method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        return json.loads(raw) if raw else {}


def post_report(board, rel, text):
    """What happened, in words. Down, wrong, or the board not registered, is
    said and never raised — the verify output is in the PRD's own files too.

    This runs between the done write and the commit, so an exception here
    leaves `prd.md` saying `done` with nothing committed. `URLError, OSError,
    ValueError` is not the whole set a live socket can raise: a port held by
    something that is not this daemon answers with `BadStatusLine`, a daemon
    killed mid-write with `IncompleteRead` — both `HTTPException`, neither an
    `OSError` — and a `/status` of another shape raises `AttributeError` or
    `KeyError` off the parse. Nothing this function can hit is worth a torn
    board, so every one of them is a returned phrase."""
    def said(e):
        return f"{type(e).__name__}: {e}".strip().replace("\n", " ")[:200]
    try:
        st = daemon_call("/status")
    except Exception as e:
        return f"daemon down — report not posted ({said(e)})"
    try:
        # `b["path"]` is None for a board the daemon holds without one — the
        # `all` board is registered that way on this machine — and
        # `os.path.abspath(None)` is a TypeError, which this function then
        # reports as "another shape" and every report on the machine is
        # silently dropped. A pathless board matches nothing; skip it.
        name = next((b["name"] for b in st.get("boards", [])
                     if b.get("path")
                     and os.path.abspath(b["path"]) == os.path.abspath(board)),
                    None)
    except Exception as e:
        return f"daemon answered in another shape — report not posted " \
               f"({said(e)})"
    if not name:
        return "board not registered with the daemon — report not posted"
    try:
        daemon_call("/report", {"board": name, "prd": rel, "text": text})
    except Exception as e:
        return f"POST /report failed — report not posted ({said(e)})"
    return "report posted"


# ── the line ──────────────────────────────────────────────────────────────────

def progress_line(board, rel, frm, to, persona, extra=""):
    """@references/parts/progress.md — every term is transitions.py's, the one
    printer of the line. What collect has to say goes after `@<w> workers`
    and before `as <persona>`, which stays last."""
    line = translib.progress_line(board, rel, frm, to, persona)
    if not extra:
        return line
    head, _, tail = line.rpartition(" · as ")
    return f"{head} · {extra} · as {tail}"


def dry_line(board, prds, rel, prd, persona, paths, out=print):
    """The `dry ·` line every writer prints — the progress line the real
    run would print, on the scan with this PRD moved to `done`. The commit
    shas the real line carries do not exist yet, so `commit` and `record`
    are not on it; `pass file owed` is."""
    frm = prd["state"]
    prd["state"] = prd["fm"]["state"] = "done"
    prd["fm"].pop("claim", None)
    line = translib.dry_line(board, prds, rel, frm, "done", persona)
    head, _, tail = line.rpartition(" · as ")
    translib.say_dry(board, f"{head} · pass file owed · as {tail}",
                     paths + [os.path.join(prd["board_path"], TRANSITION_FILE)],
                     out)


def transition_row(board, rel, frm, to, now):
    """A `{t,prd,from,to}` row appended to `.transitions.jsonl` — the same
    shape and file transitions.py record() writes for every CLI-driven
    move; this is the one collect makes on its own for done/failed."""
    row = {"t": now.strftime("%Y-%m-%d %H:%M"), "prd": rel, "from": frm,
           "to": to}
    with open(os.path.join(board, TRANSITION_FILE), "a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


# ── step 3 ────────────────────────────────────────────────────────────────────

def sort_paths(board, rel, prd, prds, board_root, repo, feet, opts, since,
               landed=None):
    """{root: plan} — for each repo, what to add whole, what to add by hunk,
    what is inherited, what is inherited inside the footprint (the stop),
    what rides, what was widened.

    `landed` is truthy when a lane merged into `repo` moments ago. The
    hunk-splitting and the two-authors refusal below exist because ONE
    working tree held every PRD's dirt at once; a lane is cut clean off
    HEAD, so everything committed in it is one worker's and there is
    nothing to split. So the sharing refusal stops running against the
    CODE repo on a lane run — and stays on for the BOARD repo, which every
    PRD writes into whatever else it does, and for a laneless board, which
    is every claim taken before lanes and every board outside a git repo.
    The path is kept, never deleted."""
    prd_rel = os.path.relpath(prd["dir"], board_root)
    groups = {board_root: {prd_rel}}
    # `spec_data` qualifies a member PRD's footprint with its own member
    # sigil so two members' `src/lib.rs` never compare equal. Here the
    # paths are about to be added in that member's own repo, so its own
    # sigil comes off again; a path carrying ANOTHER member's sigil is a
    # cross-repo footprint and is left out, as before.
    own = (f"{planlib.MEMBER_SIGIL}{prd['board']}/"
           if prd.get("board") else None)
    for f in feet:
        if own and f.startswith(own):
            p = f[len(own):]
        elif not f.startswith(planlib.MEMBER_SIGIL):
            p = f
        else:
            continue
        # a footprint path `repo_of` filed under a repo that does not hold
        # it at all is the exact silent drop this replaces: `collect` must
        # not write `done` over code it never found — refused loudly here,
        # before any group's `dirty_paths` loop ever runs. "Holds it" means
        # on disk (an untracked new file) or in the index (`git ls-files` —
        # still true of a path deleted from the working tree but not yet
        # staged, so a spec whose finish is a deletion still passes); a path
        # that DOES exist but is merely clean is not this — it goes to
        # plan.add=[] further down, no bug, nothing to say.
        # a footprint under a board that is its own repo belongs to the
        # BOARD repo, spelled its way — the code repo ignores the board and
        # holds no such path, so filing it here is what made step 4 stage
        # `.pearde/.gitignore` where it can never exist
        raw = p
        root, p = foot_root(p, board, board_root, repo)
        full = os.path.join(root, p)
        tracked = git_out(root, "ls-files", "-z", "--", p).strip("\0")
        if not os.path.exists(full) and not tracked:
            # Name every place that was tried and nothing that was not. The
            # message used to blame `repo_of`, a function that had not
            # refused anything, and left the author of a board-spelled
            # footprint with nowhere to look.
            tried = ", ".join(foot_places(raw, board, board_root, repo))
            raise Stop(f"{rel}: footprint {raw} is in no repo that holds it "
                       f"— looked for {tried}; nothing written")
        groups.setdefault(root, set()).add(p)
    for a in opts["also"]:
        ap = also_path(board_root, a)   # `check_also` already proved it exists
        root = planlib.repo_root(ap)
        if not root:
            raise Stop(f"--also {a}: not inside a git repo")
        groups.setdefault(root, set()).add(os.path.relpath(ap, root))
    widen = set()
    for w in opts["widen"]:
        wp = os.path.abspath(w) if os.path.isabs(w) else \
            os.path.abspath(os.path.join(board_root, w))
        widen.add(wp)
    base = baseline(board, rel)
    riders = owed(board)
    board_rel = board_prefix(board, board_root)
    # What another held PRD's footprint already claims, relative to the repo
    # the footprints are written against — only siblings whose code lives in
    # this run's `repo` can share a dirty path with it. A dirty path the
    # union holds and a sibling's footprint holds too may carry the
    # sibling's edits: a commit here is this PRD's record, and hunks the
    # claim's baseline does not explain are attributable to no one, so the
    # file is refused — `--widen` takes it whole.
    others = {}
    for r, p in prds.items():
        if r == rel or p["state"] not in CONTENDING:
            continue
        if repo_of(p, board, board_root) != repo:
            continue
        sig = f"{planlib.MEMBER_SIGIL}{p['board']}/" if p.get("board") else None
        claimed = []
        for f in planlib.spec_data(p)[1]:
            if sig and f.startswith(sig):
                claimed.append(f[len(sig):])
            elif not f.startswith(planlib.MEMBER_SIGIL):
                claimed.append(f)
        if claimed:
            others[r] = claimed
    held = [os.path.relpath(p["dir"], board_root) for r, p in prds.items()
            if r != rel and p["state"] in HELD]

    def side(root):
        """The claim baseline for this repo, or None. `snapshot` records the
        board's repo and the code repo; a third root — one `--also` reached
        — has no baseline, and None means what it always meant: the file
        goes whole or not at all."""
        if base is None:
            return None
        if root == board_root:
            return base["sides"].get("board")
        if root == repo:
            return base["sides"].get("repo") or (
                base["sides"].get("board") if repo == board_root else None)
        return None

    def predates(root, p, kind):
        """The whole of this path's dirt is older than the claim."""
        b = side(root)
        if b is not None:
            return (p in b["untracked"] if kind == "untracked"
                    else p in b["hunks"] and not new_hunks(root, p))
        if since is None:
            return False
        try:
            return datetime.datetime.fromtimestamp(
                os.path.getmtime(os.path.join(root, p))) < since
        except OSError:
            return False

    def new_hunks(root, p):
        """`(kept, inherited)` — the hunks of `p` the baseline does not
        hold and the ones it does, each a list of hunk text — or "" when
        every hunk is inherited, "all" when none is. None when there is no
        baseline — the file goes whole or not at all. Zero context on both
        sides, so two edits near each other are two hunks and not one
        merged one."""
        b = side(root)
        if b is None:
            return None
        cur = split_hunks(git_out(root, "diff", "HEAD", "-U0", "--no-color",
                                  "--", p)).get(p)
        if not cur:
            return ""
        _, hunks = cur
        old = b["hunks"].get(p, set())
        keep = [h for h in hunks if hunk_body(h) not in old]
        theirs = [h for h in hunks if hunk_body(h) in old]
        gone = old - {hunk_body(h) for h in theirs}
        line = two_authors(keep, gone) if keep and gone else None
        if line is not None:
            raise Stop(f"{rel}: two authors on one hunk: {p}:{line} — a "
                       f"baseline hunk merged with the worker's; `--widen "
                       f"{p}` takes the file whole, or leave one untouched "
                       f"line between the edits")
        return (keep, theirs) if keep and theirs else ("all" if keep else "")

    plan = {}
    for root, union in groups.items():
        union = sorted(u.rstrip("/") for u in union if u and u != ".")
        p = {"union": union, "add": [], "partial": {}, "inherited": [],
             "stop": [], "riders": [], "widened": []}
        for path, kind in sorted(dirty_paths(root).items()):
            full = os.path.join(root, path)
            # the board's own dotfiles — never anyone's, UNLESS somebody
            # claimed this one: a `footprint:` naming `.pearde/.gitignore`,
            # the PRD's own folder, or `--widen`. Until `board_rel` was
            # honest this branch could not fire on a board that is its own
            # repo, and the claimed case was reached by that accident; with
            # the prefix fixed, an unguarded `continue` here drops a
            # board-owned footprint path silently — measured, it took
            # `a-board-s-own-file-commits-in-the-board-repo` from 12 PASS
            # to 2 FAIL. Every claim below is tested first, so the rule is
            # what it always meant: unclaimed machine-local dirt.
            if (root == board_root and scratch(path, board_rel)
                    and full not in widen and not inside(path, union)
                    and not inside(path, [prd_rel])):
                continue
            if full in widen:
                p["add"].append(path)
                p["widened"].append(path)
            elif root == board_root and inside(path, [prd_rel]):
                # the PRD's own folder is the board's record — one writer,
                # committed whole: never by hunk, never a stop
                p["add"].append(path)
            elif inside(path, union):
                nh = new_hunks(root, path) if kind == "tracked" else None
                # A shared file is either split correctly, or the recording
                # stops and says why — never swept whole in silence. The
                # split comes FIRST: when the baseline explains part of this
                # file's dirt, those hunks are reversed back out and only
                # the rest is staged, which is the whole point of the
                # snapshot. The refusal is what is left when no split is
                # possible — every hunk is post-claim (`"all"`), so nothing
                # tells this PRD's edits from the sibling's.
                if nh not in (None, "", "all"):
                    pass
                elif not predates(root, path, kind):
                    share = sorted(r for r, claimed in others.items()
                                   if root == repo and not landed
                                   and inside(path, claimed))
                    if share:
                        # A claim snapshotted before the baseline recorded
                        # the code repo has nothing to split this file
                        # against, and the refusal above would otherwise
                        # read as "these edits are unattributable" when the
                        # truth is "this claim cannot tell". Say which.
                        stale = (base is not None and root != board_root
                                 and side(root) is None)
                        # One clause, wrapped so the sentence a check reads
                        # sits whole on a line of its own.
                        why = ""
                        if stale:
                            why = (
                                "; this claim was"
                                " recorded before the baseline covered"
                                f" {root}, so there is nothing to split it"
                                " against — `pearde collect --snapshot"
                                f" {rel}` only after the tree is clean")
                        raise Stop(f"{rel}: {path} is in "
                                   + ", ".join(share)
                                   + "'s footprint too — not only this "
                                   f"PRD's edits; `--widen {path}` takes "
                                   "it whole" + why)
                if nh not in (None, "", "all"):
                    p["partial"][path] = nh
                elif predates(root, path, kind):
                    p["stop"].append(path)
                else:
                    p["add"].append(path)
            elif kind == "rename-source" and inside(path, union):
                # a rename's deletion half: the new path entered above (or
                # rides inherited) — staging the old path is what keeps the
                # private index from carrying HEAD's old blob forever
                p["add"].append(path)
            elif root == board_root and path in riders:
                p["add"].append(path)
                p["riders"].append(path)
            elif (root == board_root and base is not None
                  and under_board(path, board_rel) is not None
                  and not inside(path, held)
                  and not predates(root, path, kind)):
                p["add"].append(path)
                p["riders"].append(path)
            else:
                p["inherited"].append(path)
        plan[root] = p
    return plan, prd_rel


# ── one PRD ───────────────────────────────────────────────────────────────────

def commit_message(prd, prd_rel, opts, plan=None):
    """The commit message for this PRD — the contract line, one line per
    spec goal, the `--also` note, `widen:` per widened path, and `prd:`.

    Built HERE and nowhere else, because two commits can carry it: step 4's
    when the work is dirt in the checkout, and the LANE's when the worker
    wrote in a worktree of its own. One PRD gets one commit
    (@references/parts/commits.md) and one message; a second builder would
    be a second copy that drifts. `plan` is step 4's — `land_lane` commits
    before `sort_paths` has run and passes None, which is right: `--widen`
    names paths dirty in the CHECKOUT, and nothing in a lane is widened."""
    slug = str(prd["fm"].get("workflow", "") or "").strip()
    lines = [f"{prd['name']} — {contract_line(prd)}", ""]
    lines += [f"{n}: {g}" for n, g in spec_goals(prd)]
    if opts["also"]:
        lines.append(f"workflow: {slug or 'none'} — {opts['also_note']}")
    for p in (plan or {}).values():
        lines += [f"widen: {x}" for x in p["widened"]]
    lines += ["", f"prd: {prd_rel}"]
    return "\n".join(lines) + "\n"


def moved_onto(repo):
    """The branch the checkout is on, for the line below. `--abbrev-ref` on
    a detached HEAD answers `HEAD`, which names nothing a person recognises;
    the fallback phrase is the honest reading of that."""
    import lanes as laneslib
    br = laneslib.git(repo, "rev-parse", "--abbrev-ref", "HEAD",
                      check=False).stdout.strip()
    return br if br and br != "HEAD" else "the checkout"


def moved_line(rel, onto, moved):
    """One line, printed by the run and written into the report, so the two
    say the same thing in the same words. `moved` is already narrowed to
    the footprint by the caller."""
    return f"{rel}: {onto} moved under the lane — " + ", ".join(moved)


def land_lane(board, rel, prd, repo, opts, out=print):
    """Commit what stands in the PRD's lane and merge it into the branch
    the checkout is on. Returns `(pre, n, moved)` — the checkout's commit
    before the merge, so step 2 can put it back on a red; how many of the
    lane's commits landed; and the footprint files this branch changed
    since the lane was cut. `(None, None, [])` when there is no lane, which
    is every board that never cut one and every claim from before lanes:
    the old path, unchanged.

    `moved` is read before the merge and printed before it — `lanes.merge`
    rebases the lane onto this branch, and after that there is no cut point
    left to compare against. It is also what the report carries: the worker
    wrote its own report before any of this landed, so the only place that
    can say what moved under its feet is here.

    Scope is the footprint, exactly as step 3's is — the lane is cut clean
    off HEAD, so everything dirty in it is this worker's and no hunk needs
    splitting, but a worker that wandered outside its footprint is still
    not committed whole. The paths outside are named and left in the lane.

    A merge conflict raises `lanes.Conflict` — through, not caught. The
    merge is aborted, so the checkout is where it was and the lane branch
    still holds the worker's commits; `collect_one` catches it and writes
    the PRD `blocked` with the files on it. Turning it into a `Stop` here
    is what left a conflicted lane `claimed` forever: the run printed one
    line to stderr and the board recorded nothing, so `pearde scan` went
    on showing a worker holding a PRD no worker was working on. Every
    OTHER `LaneError` is still a `Stop` — a lane git cannot read is a
    broken board, not a wall a person takes down.

    `--dry` says what it WOULD merge — the branch and how many commits —
    and merges nothing; `opts["dry"]` reaches here rather than being
    checked by the caller, so the dry line and the real one are built from
    the same read of the lane."""
    import lanes as laneslib
    if not laneslib.exists(board, rel):
        return None, None, []
    lane = laneslib.lane_dir(board, rel)
    br = laneslib.branch_of(rel)
    _, feet = planlib.spec_data(prd)
    feet = [f for f in feet if not f.startswith(planlib.MEMBER_SIGIL)]
    # The lane is a worktree of the CODE repo, and it is cut without the
    # board: `lanes.create` excludes the board's path by sparse-checkout,
    # and where the code repo ignores the board there is nothing to check
    # out anyway. So a footprint path the board repo holds is not the
    # lane's to stage — `git add` on it is `fatal: pathspec … did not
    # match any files`, which aborts the add whole and lands no commit at
    # all. It is committed in the board repo by step 3, where it lives.
    elsewhere = [f for f in feet
                 if foot_root(f, board, planlib.repo_root(board) or board,
                              repo)[0] != repo]
    feet = [f for f in feet if f not in elsewhere]
    if elsewhere:
        out(f"{rel}: in the board's own repo, not the lane's — "
            + ", ".join(sorted(elsewhere)))
    standing = laneslib.dirty(board, rel)
    outside = [p for p in standing if not inside(p, feet)]
    if outside:
        out(f"{rel}: outside the footprint, left in the lane — "
            + ", ".join(sorted(outside)))
    # What moved under the worker's feet, read BEFORE anything merges:
    # `lanes.merge` rebases the lane onto this branch, and from then on the
    # cut point IS this branch's HEAD and the comparison has no answer left
    # to give. Narrowed to the footprint — a lane is verified against the
    # merged tree whatever else landed, and the names worth a line are the
    # ones this PRD's own files moved under.
    moved = [p for p in laneslib.moved_since_cut(repo, rel)
             if inside(p, feet)]
    if moved:
        out(moved_line(rel, moved_onto(repo), moved))
    if opts.get("dry"):
        ahead = laneslib.git(repo, "rev-list", "--count", "HEAD.." + br,
                             check=False).stdout.strip() or "0"
        mine = [p for p in standing if inside(p, feet)]
        out(f"{rel}: would merge lane {br} — {ahead} commit(s)"
            + (f", and commit {len(mine)} path(s) standing in it first"
               if mine else "")
            + "; merged nothing")
        return None, None, moved
    prd_rel = os.path.relpath(prd["dir"], planlib.repo_root(board)
                              or os.path.dirname(board))
    try:
        if [p for p in standing if inside(p, feet)]:
            laneslib.git(lane, "add", "--", *feet)
            laneslib.git(lane, "commit", "-m",
                         commit_message(prd, prd_rel, opts))
        pre = laneslib.git(repo, "rev-parse", "HEAD").stdout.strip()
        n = laneslib.merge(repo, rel)
    except laneslib.Conflict:
        raise
    except laneslib.LaneError as e:
        raise Stop(f"{rel}: {e} — nothing written; the lane still holds the "
                   f"work on `{br}`")
    if n:
        out(f"{rel}: lane {br} merged — {n} commit(s)")
    return pre, n, moved


def block_conflict(board, rel, prd, pmd, conflict, opts, now, out=print):
    """A lane that will not rebase becomes a `blocked` PRD, and returns 1.

    The wall this puts on the board is `## Blocked` — the heading
    @references/parts/view.md already draws as the wall and `questions.py`
    already refuses a `blocked` PRD for not having. So the reason a person
    reads is written in the one place every reader of this board already
    looks, and nothing new has to learn to render it.

    What it writes: the lane branch, the branch it would not land on, and
    one bullet per file git named on the conflict — git's own list, carried
    as data from `lanes.Conflict` rather than parsed back out of a sentence.
    The claim goes, because no worker is working on it; the state goes to
    `blocked`, because a person has to take the wall down. Nothing else is
    touched: the checkout is where `lanes.merge` left it, and the worker's
    commits are on the lane branch, which is why the reason can say so.

    `blocked` and not `failed`. A `failed` PRD is work that did not do what
    it said; this work may be perfect and merely disagree with what landed
    while it ran. `failed` also routes to `retry`, which would dispatch a
    second worker onto a lane that already holds the answer. `unblock` is
    the edge out, and it lands on `specced` — the PRD is specced work with
    a lane standing, which is exactly what it was before the collect.

    Unconditional, and not behind `--fail`. `--fail` chooses whether a red
    VERIFY is recorded, and a bare `collect` leaving that on the board
    would be a judgement about the code. This is not a judgement: without
    the write the PRD stays `claimed` with no worker, which is the defect
    the contract names. `--dry` never reaches here — `land_lane` returns
    before it merges."""
    files = sorted(set(conflict.files))
    lines = [f"**{now.strftime('%Y-%m-%d %H:%M')} — the lane will not "
             f"rebase**", "",
             f"`{conflict.branch}` does not land on `{conflict.onto}`; "
             + (f"{len(files)} file(s) disagree:" if files
                else "git named no file — `git status` in the lane says "
                     "which."), ""]
    lines += [f"- `{f}`" for f in files]
    lines += ["", f"Nothing is lost: the worker's commits are on "
              f"`{conflict.branch}` and the checkout never moved. Resolve "
              f"the conflict in the lane, then `pearde unblock {rel}`."]
    text = "\n".join(lines)
    if opts.get("dry"):                 # unreachable today; free if it changes
        out(f"{rel}: dry — would block on {conflict.branch}")
        return 1
    editlib.append_section(pmd, "Blocked", text)
    editlib.del_key(pmd, "claim")
    editlib.set_key(pmd, "state", "blocked")
    transition_row(board, rel, prd["state"], "blocked", now)
    # the exception's own words on the line, so the run still prints what
    # git said and not a second paraphrase of it
    out(progress_line(board, rel, prd["state"], "blocked", opts["as"],
                      str(conflict)))
    return 1


def unland(repo, pre, landed, out=print):
    """Put the checkout's BRANCH back where `land_lane` found it, and touch
    nothing else. Called when step 2 goes red: a verify that fails must not
    leave the lane's code standing in the checkout, and the lane branch is
    untouched so a retry merges the same commits again.

    The inverse of a fast-forward merge is moving the pointer back, not
    `reset --hard`. `--hard` throws away the working tree and the index,
    which the merge never touched — and this checkout is shared: the
    uncommitted work standing in it is other sessions' and other PRDs',
    none of it this PRD's to discard. Measured: `--hard` here destroyed
    sixteen files of an unrelated, uncommitted implementation on a red
    verify, and printed it as `lane unmerged`. `--keep` moves the ref,
    updates only the files that differ between the two commits, and
    REFUSES when one of those carries uncommitted work.

    A refusal is reported and obeyed: the merge stays standing and the
    person is told which paths held it. A gate that deletes what it was
    checking is worse than a gate that stops.

    `landed` is `land_lane`'s count. Zero means the merge merged nothing —
    the lane committed nothing, or there was no lane — and there is
    nothing to put back: rolling one back would be a reset for a merge
    that did not happen."""
    if not pre or not landed:
        return
    import lanes as laneslib
    files = [f for f in laneslib.git(repo, "diff", "--name-only",
                                     pre + "..HEAD",
                                     check=False).stdout.split() if f]
    shown = ", ".join(files[:4]) + (f" +{len(files) - 4} more"
                                    if len(files) > 4 else "")
    out(f"  unmerging {landed} commit(s) — dropping {shown or 'no file'} "
        f"from the checkout, back to {pre[:12]}")
    r = laneslib.git(repo, "reset", "--keep", pre, check=False)
    if r.returncode:
        out("  not rolled back — the checkout holds uncommitted work in "
            "those paths, and it is not this PRD's to discard:")
        for line in ((r.stderr or r.stdout).strip().splitlines() or
                     ["git reset --keep refused"]):
            out(f"    {line}")
        out(f"  the lane's code stands in the checkout; roll it back with "
            f"`git -C {repo} reset --keep {pre[:12]}` once those paths are "
            f"clear")
        return
    out(f"  lane unmerged — checkout back at {pre[:12]}")


def collect_one(board, rel, opts, out=print):
    now = datetime.datetime.now()
    prds = planlib.scan(board)
    prd = prds.get(rel)
    if not prd:
        raise Stop(f"{rel}: no PRD at that path")
    board_root = planlib.repo_root(prd["dir"])
    if not board_root:
        raise Stop(f"{rel}: {prd['dir']} is not inside a git repo")
    pmd = os.path.join(prd["dir"], "prd.md")
    cl = planlib.claim_of(prd["fm"])
    since = parse_when(cl["since"]) if cl and cl["since"] else None

    # 1 — finished, off both files
    _, closed, total, ready = planlib.standing(prd)
    if not ready and container(prd, prds, board):
        return close_container(board, rel, prd, prds, board_root, opts,
                               now, out)
    if not ready:
        if prd["state"] not in planlib.HOLDING_STATES:
            raise Stop(f"{rel}: state is `{prd['state']}` — collect closes "
                       f"`claimed` or `blocked`")
        boxes = open_boxes(prd)
        if boxes:
            f, line = boxes[0]
            raise Stop(f"{rel}: open box in {os.path.relpath(f, board_root)}"
                       f": `{line}`" + (f" (+{len(boxes) - 1} more)"
                                       if len(boxes) > 1 else ""))
        raise Stop(f"{rel}: no acceptance box in specs/ — nothing says it "
                   f"is finished ({closed}/{total})")

    # 1b — the lane lands before anything is measured. The worker's code is
    # committed on `lane/<slug>` in its own worktree and does not exist in
    # the checkout at all, so a verify run before the merge measures the
    # tree the work is missing from — which is a red on every PRD that used
    # a lane. Merge first, then verify the MERGED tree: a lane that passes
    # alone and breaks against what landed while it ran is a red here, and
    # that is the whole reason the gate runs after the merge and not in the
    # lane. `pre` is where to put the checkout back if step 2 goes red —
    # the lane branch is never touched, so the worker's commits survive a
    # failed collect and a retry merges them again.
    repo = repo_of(prd, board, board_root)
    try:
        pre, landed, moved = land_lane(board, rel, prd, repo, opts, out)
    except LaneConflict as e:
        return block_conflict(board, rel, prd, pmd, e, opts, now, out)
    base = baseline(board, rel)
    _, feet = planlib.spec_data(prd)
    owned = owned_by(prd, board_root, repo, feet, board)
    report, trusted, known = [], False, False
    if opts.get("trust"):
        trusted = True
    else:
        checks = [(spec, script, repo) for spec, script in verify_blocks(prd)]
        gate = str(planlib.board_settings(board).get("gate", "") or "").strip()
        if gate:
            checks.append(("gate", gate, board_root))
        for name, script, cwd in checks:
            # fenced: nothing outside this PRD's footprint in `cwd` can be
            # reached, left changed, or have its branch moved by the block
            code, output = guarded_run(["bash", "-e", "-o", "pipefail"],
                                       cwd, owned, script, out)
            red = code != 0
            if red and name == "gate" and base is not None:
                # measured against the claim's baseline, not against silence
                new = [l for l in output.splitlines()
                       if l.strip() and l not in base["gate_lines"]]
                red = bool(new)
                if not red:
                    known = True
                    output += "\n(known — every line is in the claim's " \
                              "baseline)"
            report.append(f"{name}: exit {code}\n{output.rstrip()}")
            if red:
                text = "\n\n".join(report)
                out(text)
                # the lane's code never stands on a red — and nothing else
                # in this shared checkout is touched putting it back
                unland(repo, pre, landed, out)
                if opts.get("fail") and not opts.get("dry"):
                    editlib.append_section(pmd, "Failure", text)
                    editlib.del_key(pmd, "claim")
                    editlib.set_key(pmd, "state", "failed")
                    transition_row(board, rel, prd["state"], "failed", now)
                    out(progress_line(board, rel, prd["state"], "failed",
                                      opts["as"], "pass file owed"))
                    return 1
                raise Stop(f"{rel}: {name} exit {code} — nothing written")

    # 3 — the paths
    plan, prd_rel = sort_paths(board, rel, prd, prds, board_root, repo, feet,
                               opts, since, landed=landed)
    stops, inherited = [], []
    for root, p in plan.items():
        stops += [os.path.relpath(os.path.join(root, x), board_root)
                  for x in p["stop"]]
        inherited += [os.path.relpath(os.path.join(root, x), board_root)
                      for x in p["inherited"]]
    if inherited:
        out(f"{rel}: inherited, not added — {len(inherited)} path(s):")
        for x in inherited:
            out(f"  {x}")
    if stops:
        out(f"{rel}: inside the footprint and older than the claim — "
            f"`--widen <path>` takes it:")
        for x in stops:
            out(f"  {x}")
        raise Stop(f"{rel}: {len(stops)} path(s) in the footprint that the "
                   f"claim predates")

    # 4 — the message, one commit per repo
    message = commit_message(prd, prd_rel, opts, plan)
    if opts.get("dry"):
        for root, p in plan.items():
            out(f"{rel}: repo {root}")
            out("  footprint: " + (", ".join(p["union"]) or "(none)"))
            out("  would add: " + (", ".join(p["add"]) or
                                   ("(clean — commit: none)"
                                    if not p["partial"] else "")))
            for x in p["partial"]:
                out(f"  by hunk:   {x}")
            if p["riders"]:
                out("  rides:     " + ", ".join(p["riders"]))
            if p["widened"]:
                out("  widened:   " + ", ".join(p["widened"]))
            if root == board_root:
                out(f"  record:    {prd_rel}/prd.md — done, actual, the "
                    f"claim cleared, in this commit; commit: in a second, "
                    f"`{prd['name']} — record`")
        out("  message:\n    " + message.rstrip().replace("\n", "\n    "))
        dry_line(board, prds, rel, prd, opts["as"], [pmd], out)
        out(f"{rel}: dry — nothing written")
        return 0
    # stage every repo first, each in an index of its own: a refusal here
    # has written nothing anywhere
    said, staged_roots = [], []
    roots = [r_ for r_, p in plan.items() if p["add"] or p["partial"]]
    if board_root not in roots:
        roots.append(board_root)
    with private_index(roots):
      for root, p in plan.items():
        if not p["add"] and not p["partial"]:
            continue
        staged_roots.append(root)
        if p["add"]:
            # `-f`: every path here already came off `dirty_paths()` —
            # tracked (modified/deleted), riders, or `--widen`, never a
            # fresh untracked file `.gitignore` would otherwise hide from
            # that scan. `git add` still refuses an EXPLICIT pathspec
            # that resolves inside an ignored directory even when the
            # path is tracked (`prds/**/probe/` in the board's own
            # `.gitignore`, and every probe file force-tracked before
            # that rule existed) — `-f` is what makes the PRD folder's
            # "added whole, always" promise true for those, not a
            # widening of what gets swept in.
            git_out(root, "add", "-f", "--", *p["add"])
        # a shared file is staged as the working file with the inherited
        # hunks reversed — never as a patch with hunks left out, which
        # `git apply` places by a line number that counts the missing ones
        staged = {path: stage_by_hunk(root, path, foreign)
                  for path, (_, foreign) in p["partial"].items()}
        refusals = placement_refusals(root, p["partial"], staged)
        if refusals:
            out(f"{rel}: staged by hunk and refused — nothing committed, "
                f"nothing staged:")
            for x in refusals:
                out(f"  {x}")
            raise Stop(f"{rel}: {len(refusals)} placement refusal(s) in "
                       f"{root}")
        if p["partial"]:
            said.append("by hunk " + ", ".join(p["partial"]))
        if p["riders"]:
            said.append("rides " + ", ".join(p["riders"]))
        if p["widened"]:
            said.append("widened " + ", ".join(p["widened"]))
      if inherited:
        said.append(f"inherited {len(inherited)}")

      # the record — every key but `commit:`, and the report, BEFORE the
      # commit, so the commit carries them; put back whole if the commit fails
      with open(pmd, encoding="utf-8") as f:
        before = f.read()
      # From here to the commit the record on disk says `done` and git says
      # nothing landed. Whatever raises in that window — the daemon, a git
      # add, a line put here later — puts `prd.md` back the way it was and
      # refuses, so a crash never leaves a PRD finished on the board and
      # unfinished in the repo.
      try:
        hrs = (now - since).total_seconds() / 3600.0 if since else None
        if hrs is not None:
            editlib.set_key(pmd, "actual", fmt_hours(max(hrs, 0.0)))
        editlib.del_key(pmd, "claim")
        editlib.set_key(pmd, "state", "done")
        # 6 — the report to the daemon, which appends `## Report` to prd.md
        text = ("trusted — the verify was not run by collect" if trusted
                else "\n\n".join(report) or "no `## Verify and Proof` block")
        if moved:
            # the report says what moved under the worker's feet, in the
            # same words the run printed — the worker wrote its own report
            # before any of this landed and cannot know it
            text = moved_line(rel, moved_onto(repo), moved) + "\n\n" + text
        posted = post_report(board, rel, text)
        git_out(board_root, "add", "--", prd_rel)
      except BaseException as e:
        editlib.write_atomic(pmd, before)
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        raise Stop(f"{rel}: the record was written and the commit not "
                   f"reached — put back, nothing written: "
                   f"{type(e).__name__}: {e}") from e
      if board_root not in staged_roots:
        staged_roots.append(board_root)
      committed = {r_: list(plan[r_]["add"]) + list(plan[r_]["partial"])
                   for r_ in staged_roots}
      committed[board_root].append(prd_rel)
      # The lane's commit IS this PRD's commit in the repo it merged into:
      # it carries `message` and the code the message names. A second one
      # here would be one PRD with two commits, which
      # @references/parts/commits.md forbids — so where the lane landed,
      # step 4 takes the merged HEAD as its sha and stages nothing new of
      # its own. Whatever the board record put in that index (the PRD's
      # own folder, on a board that shares the code repo) rides the
      # `<prd> — record` commit right behind, so the checkout's branch
      # gains exactly two: the work, and the record.
      lane_root = repo if landed else None
      shas, rode = [], []
      if lane_root and lane_root not in staged_roots:
        # a board in a repo of its own: the code commit is the lane's and
        # is in no `staged_roots`, but `commit:` must still name it or
        # `orphans` reads the footprint as never having reached a branch
        shas.append(git_out(lane_root, "rev-parse", "HEAD",
                            shared=True).strip()[:7])
      for root in staged_roots:
        if root == lane_root:
            shas.append(git_out(root, "rev-parse", "HEAD",
                                shared=True).strip()[:7])
            if root == board_root:      # else nothing of this root's is
                rode += committed[root]  # settled by the record commit
            continue
        try:
            shas.append(commit_private(root, message))
        except Stop as e:
            editlib.write_atomic(pmd, before)
            raise Stop(f"{rel}: git commit failed in {root} — the record "
                       f"put back, nothing written: {e}")
        settle_shared(root, committed[root])
      settle(board, [x for p in plan.values() for x in p["riders"]])

      # 5 — `commit:` — the one key that cannot be in the commit it names:
      # a second, one-key commit right behind, so nothing rides
      editlib.set_key(pmd, "commit", " ".join(shas))
      pmd_rel = os.path.relpath(pmd, board_root)
      git_out(board_root, "add", "--", pmd_rel)
      try:
        said.append("record " + commit_private(
            board_root, f"{prd['name']} — record\n\nprd: {prd_rel}\n"))
      except Stop as e:
        raise Stop(f"{rel}: the record commit failed in {board_root} — "
                   f"`commit:` is written and unstaged: {e}")
      settle_shared(board_root, sorted(set([pmd_rel] + rode)))

    # 7 — the session's branch onto the branch a person reads
    put = land_session(board)

    # 8 — the line, the row
    transition_row(board, rel, prd["state"], "done", now)
    extra = " · ".join(x for x in [
        "trusted" if trusted else "", "gate red, known" if known else "",
        f"commit {' '.join(shas)}", *said, put, posted,
        "pass file owed"] if x)
    out(progress_line(board, rel, prd["state"], "done", opts["as"], extra))
    return 0


def land_session(board):
    """Put this session's commits on the branch a person reads, and say what
    happened in one phrase. Runs after the commit, never before it.

    A commit on `session/<id>` is a commit nobody reads. The session's tree
    is the code repo now, so every PRD lands on that branch first, and the
    contract is that it reaches the branch a person opens the repo on — so
    the merge is part of finishing, not a thing to remember afterwards.

    ADVISORY, like `post_report` and for the same reason: it runs after
    `prd.md` says `done` and the commits are made, so anything raised here
    would leave the board finished and the run reporting a failure it did
    not have. A checkout with uncommitted work refuses the fast-forward, and
    that refusal is a phrase on the line — the work is on the session branch
    either way, `pearde session land` retries it, and nothing is lost. It is
    also why the checkout is never forced: `merge --ff-only` is the whole of
    what runs in a tree this session does not own.

    Empty string when there is nothing to say: no session, no branch, or a
    branch the reading branch already holds."""
    def said(e):
        return f"{type(e).__name__}: {e}".strip().replace("\n", " ")[:160]
    try:
        import session as sessionlib
        if sessionlib.held(board) is None:
            return ""
    except Exception:
        return ""
    try:
        br, target, n = sessionlib.land(board)
    except Exception as e:
        return f"not landed on the branch a person reads ({said(e)})"
    return f"landed on {target}" if n else ""


# ── a container ───────────────────────────────────────────────────────────────

def container(prd, prds, board):
    """`dispatchable`'s word for it — plan.py's one predicate, the same one
    `claim` refuses on and `scan` lists under collect with. An `open` PRD
    only: a held parent is a worker's, and a parked one is a person's."""
    return (prd["state"] == "open"
            and (planlib.dispatchable(prd, prds, board) or ""
                 ).startswith("container:"))


def last_child_commit(kids, board, board_root):
    """The `commit:` of the child that landed last — the newest of the
    children's shas by commit date, each read in the repo the child wrote;
    two in the same second are ordered by how deep in history they sit.
    `none` when no child's sha resolves."""
    best = None
    for c in kids:
        raw = str(c["fm"].get("commit", "") or "").split()
        if not raw or raw[0] == "none":
            continue
        root = repo_of(c, board, board_root)
        r = subprocess.run(["git", "-C", root, "log", "-1", "--format=%ct",
                            raw[0]], capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            continue
        depth = subprocess.run(["git", "-C", root, "rev-list", "--count",
                                raw[0]], capture_output=True, text=True)
        key = (int(r.stdout.strip()), int(depth.stdout.strip() or 0))
        if best is None or key > best[0]:
            best = (key, raw[0])
    return best[1] if best else "none"


def close_container(board, rel, prd, prds, board_root, opts, now, out=print):
    """A parent whose every child is `done`, with no spec and no open box of
    its own: nothing to verify, nothing to add but its own `prd.md`. `done`,
    `actual:` the sum of the children's, `commit:` the last child's, in one
    commit `<parent> — done: every child landed`."""
    kids = [prds[c] for c in prd["children"] if c in prds]
    live = [c["rel"] for c in kids if c["state"] != "done"]
    if not kids or live:
        raise Stop(f"{rel}: standing() calls it finished, but it holds "
                   f"{'no child' if not kids else 'a child not done: ' + ', '.join(live)}"
                   f" — not a container; nothing written")
    pmd = os.path.join(prd["dir"], "prd.md")
    prd_rel = os.path.relpath(prd["dir"], board_root)
    actual = fmt_hours(sum(planlib.hours(c["fm"].get("actual"))
                           for c in kids))
    sha = last_child_commit(kids, board, board_root)
    message = f"{prd['name']} — done: every child landed\n\nprd: {prd_rel}\n"
    phrase = "container: every child done — pearde collect closes it"
    if opts.get("dry"):
        out(f"{rel}: {phrase}")
        out(f"  children:  {', '.join(c['rel'] for c in kids)}")
        out(f"  would add: {prd_rel}/prd.md")
        out(f"  record:    state: done · actual: {actual} · commit: {sha}")
        out("  message:\n    " + message.rstrip().replace("\n", "\n    "))
        dry_line(board, prds, rel, prd, opts["as"], [pmd], out)
        out(f"{rel}: dry — nothing written")
        return 0
    with open(pmd, encoding="utf-8") as f:
        before = f.read()
    # the same window as `collect_one`'s, guarded the same way: the record
    # says `done` and nothing is committed until the commit below
    try:
        editlib.set_key(pmd, "actual", actual)
        editlib.set_key(pmd, "commit", sha)
        editlib.del_key(pmd, "claim")
        editlib.set_key(pmd, "state", "done")
        posted = post_report(board, rel, f"{phrase}\n\nchildren: "
                             + ", ".join(c["rel"] for c in kids))
    except BaseException as e:
        editlib.write_atomic(pmd, before)
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        raise Stop(f"{rel}: the record was written and the commit not "
                   f"reached — put back, nothing written: "
                   f"{type(e).__name__}: {e}") from e
    pmd_rel = os.path.relpath(pmd, board_root)
    with private_index([board_root]):
        git_out(board_root, "add", "--", pmd_rel)
        try:
            own = commit_private(board_root, message)
        except Stop as e:
            editlib.write_atomic(pmd, before)
            raise Stop(f"{rel}: git commit failed in {board_root} — the "
                       f"record put back, nothing written: {e}")
        settle_shared(board_root, [pmd_rel])
    transition_row(board, rel, prd["state"], "done", now)
    extra = " · ".join([f"container, {len(kids)} children",
                        f"commit {sha}", f"record {own}", posted,
                        "pass file owed"])
    out(progress_line(board, rel, prd["state"], "done", opts["as"], extra))
    return 0


def cmd_collect(argv, board=None):
    """The entry: `collect [<prd>…] [flags]`. Exit 0 when every PRD named
    was collected, 1 when any stopped, 2 on usage."""
    try:
        opts = parse_args(argv)
    except (Stop, translib.FlagRefused) as e:
        print(f"collect: {e}", file=sys.stderr)
        return 2
    except translib.Refused as e:       # no persona named — exit 1, nothing read
        print(f"collect: refused — {e}", file=sys.stderr)
        return 1
    board = planlib.find_board(opts["board"] or board)
    # before anything is read or written: a `--also` path the board does not
    # hold refuses the whole call, not the one PRD that noticed it
    try:
        check_also(planlib.repo_root(board) or board, opts)
    except Stop as e:
        print(f"collect: {e}", file=sys.stderr)
        return 1
    if opts["snapshot"]:
        try:
            print(f"snapshot: {snapshot(board, opts['snapshot'].strip('/'))}")
        except Stop as e:
            print(f"collect: {e}", file=sys.stderr)
            return 1
        return 0
    if opts["report"]:
        rels = opts["prds"]
        if len(rels) != 1:
            print("collect: --report <path> takes exactly one PRD",
                 file=sys.stderr)
            return 2
        try:
            return route_report(board, rels[0], opts["report"], opts)
        except Stop as e:
            print(f"collect: {e}", file=sys.stderr)
            return 1
    rels = opts["prds"]
    if not rels:
        r = planlib.compute_plan(board, None, warn=False)
        rels = list(r["collect"]) if r else []
        # a container is finished work too — `scan`'s collect band lists it
        # beside the held-and-finished; the bare `collect` closes both
        for x in sorted(r["todo"]) if r else []:
            if x not in rels and container(r["todo"][x], r["prds"], board):
                rels.append(x)
        if not rels:
            print("collect: nothing finished — the scan's collect section is "
                  "empty")
            return 0
    worst = 0
    for rel in rels:
        try:
            worst = max(worst, collect_one(board, rel, opts))
        except Stop as e:
            print(f"collect: {e}", file=sys.stderr)
            worst = max(worst, 1)
    return worst


cmd_collect.flags = FLAGS       # what `pearde collect --help` prints
COMMANDS = {"collect": cmd_collect}


def main():
    sys.exit(cmd_collect(sys.argv[1:]))


if __name__ == "__main__":
    main()
