#!/usr/bin/env python3
"""Throwaway one-shot migration: a prds/ board -> the .pearde/ layout.

Run once per board, then delete from the tree — no dual-path support, no
permanent command (the decision on record). Python 3 stdlib only.

    migrate.py <board-root>...      # a repo dir holding prds/ — run once each
    --serve <serve.json>            # rewrite registry rows for the moved boards
    --quiet                         # only warnings and the summaries

Per board (the same move this repo had done to it by hand):
    prds/                     -> .pearde/          (git mv when tracked, mv else)
    inside it: mkdir prds/ and .state/
    every PRD directory       -> prds/
    knowledge/                -> wiki/
    memos/ and workflows/     -> stay where they land, siblings of prds/
    settings.md and vision.md -> stay at the board root
    the five state dotfiles   -> .state/<name>, leading dot dropped
    the board's .gitignore    -> rewritten for the new paths
Board-relative members rows (`- ../x/prds`) in the master's settings.md and the
machine registry (serve.json) are rewritten to the new board dirs — without
them the moved code reads every member and every registered board as empty.
A state file both the loose dotfiles and the old prds/.state/ supplied keeps
the loose copy (the fuller record); the loser is reported under .state/ with
its origin in the name, never deleted.
"""
import json
import os
import re
import subprocess
import sys

BOARD_DIR = ".pearde"
PRDS_DIR = "prds"
STATE = ".state"
# the five state dotfiles, destination names — leading dot dropped
STATE_FILES = ("history.jsonl", "plan.json", "round.md",
               "transitions.jsonl", "view.html")
# dirs that stay at the board root as siblings of prds/ — memos/ and
# workflows/ "stay where they land"; the rest is machine-local corner
KEEP_DIRS = {PRDS_DIR, STATE, ".claims", ".obsidian", "memos", "wiki",
             "workflows", "knowledge", "graphify", ".git"}
# other stray files at the old board root that stay put
KEEP_FILES = (".gitignore", ".DS_Store")
# gitignore line shapes from the old layout, word-boundary on the tail
GIT_MAP = (
    ("prds/.history.jsonl", BOARD_DIR + "/.state/history.jsonl"),
    ("prds/.plan.json", BOARD_DIR + "/.state/plan.json"),
    ("prds/.round.md", BOARD_DIR + "/.state/round.md"),
    ("prds/.view.html", BOARD_DIR + "/.state/view.html"),
    ("prds/.transitions.jsonl", BOARD_DIR + "/.state/transitions.jsonl"),
    ("prds/.plane.env", BOARD_DIR + "/.plane.env"),
    ("prds/.claims", BOARD_DIR + "/.claims"),
    ("prds/.state", BOARD_DIR + "/.state"),
)

WARN = []


def warn(msg):
    WARN.append(msg)
    print(f"WARNING: {msg}")


def die(msg, code=2):
    print(f"migrate: {msg}", file=sys.stderr)
    sys.exit(code)


def git(repo, *args):
    """git's (rc, stdout, stderr) — silent; the caller decides on rc."""
    p = subprocess.run(["git", "-C", repo, *args],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def tracked(repo, rel):
    """Is rel (repo-relative) under git's index? An untracked path (a whole
    board nobody commits, an ignored state file) rides a plain move."""
    rc, _, _ = git(repo, "ls-files", "--error-unmatch", "--", rel)
    return rc == 0


def move(root, repo, src, dst):
    """git mv where the source is tracked, a plain move where it is not.
    src/dst relative to the board root; root = the board root (realpath'd).
    repo = the git root holding the board, computed once per board."""
    s, d = os.path.join(root, src), os.path.join(root, dst)
    if os.path.exists(d):
        warn(f"{src}: destination exists — not moved")
        return None
    os.makedirs(os.path.dirname(d), exist_ok=True)
    rel = (os.path.relpath(s, repo), os.path.relpath(d, repo))
    if not rel[0].startswith("..") and tracked(repo, rel[0]):
        p = subprocess.run(["git", "-C", repo, "mv", rel[0], rel[1]],
                           capture_output=True, text=True)
        if p.returncode == 0:
            return "git"
        warn(f"git mv {src} failed ({p.stderr.strip()}) — plain move")
    if os.path.exists(s):
        os.rename(s, d)
    else:
        warn(f"{src}: source vanished before the move")
    return "mv"


def rewrite_gitignore(root, quiet):
    """The board's .gitignore rewritten for the new paths. A line the map does
    not cover is reported, never silently rewritten."""
    gi = os.path.join(root, ".gitignore")
    if not os.path.isfile(gi):
        return 0
    n, out = 0, []
    for line in open(gi, encoding="utf-8"):
        new = line
        for old, newp in GIT_MAP:
            new = re.sub(re.escape(old) + r"(?![\w.-])", newp, new)
        if new != line:
            n += 1
        elif re.match(r"^!?/?prds/", line.strip()):
            warn(f".gitignore line not mapped: {line.strip()}")
        out.append(new)
    if n:
        open(gi, "w", encoding="utf-8").write("".join(out))
        if not quiet:
            print(f"  .gitignore: {n} line(s) rewritten")
    return n


MEMBER_ROW = re.compile(
    r"^(\s*-\s*(?:[A-Za-z0-9_.-]+\s*:\s*)?)(\S+?)/prds\s*$")


def rewrite_members(board, quiet):
    """A master's members rows name member boards by their old prds/ spot.
    After the move the row must name the board dir (`../x/.pearde`), else the
    member resolves to a directory that is gone and the master reads it as
    empty — every member PRD silently drops off the master. Only a row whose
    member now has a .pearde/ is rewritten."""
    path = os.path.join(board, "settings.md")
    if not os.path.isfile(path):
        return 0
    n, out = 0, []
    for line in open(path, encoding="utf-8"):
        m = MEMBER_ROW.match(line)
        if m:
            # <x>/prds -> <x>/.pearde, where <x> resolves from the repo dir
            # above the board (plan.py resolves the row from the board dir:
            # ../x/prds from <repo>/.pearde = <repo>/../x — one level too
            # high — so test what the member's migration produced beside
            # the old board root, then name the member's board dir)
            head = m.group(2).strip()
            member_board = os.path.abspath(
                os.path.join(board, head, BOARD_DIR))
            if os.path.isdir(member_board):
                line = f"{m.group(1)}{head}/{BOARD_DIR}\n"
                n += 1
        out.append(line)
    if n:
        open(path, "w", encoding="utf-8").write("".join(out))
        if not quiet:
            print(f"  settings.md members: {n} row(s) rewritten")
    return n


def rewrite_serve(path, quiet):
    """Registry rows name the board dir; a moved board's row must follow or
    the daemon and calibrate walk a dead path. Only a row whose <dir>/.pearde
    now exists is rewritten."""
    try:
        rows = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        warn(f"{path}: unreadable registry — rows left as written")
        return 0
    n = 0
    for i, p in enumerate(rows):
        if p.endswith("/" + PRDS_DIR):
            new = os.path.join(os.path.dirname(p), BOARD_DIR)
            if os.path.isdir(new):
                rows[i] = new
                n += 1
    if n:
        json.dump(rows, open(path, "w", encoding="utf-8"), indent=1)
        if not quiet:
            print(f"  {os.path.basename(path)}: {n} row(s) rewritten")
    return n


def migrate_root(root, quiet):
    """One board: <root>/prds -> <root>/.pearde, resorted inside."""
    old = os.path.join(root, PRDS_DIR)
    board = os.path.join(root, BOARD_DIR)
    if not os.path.isdir(old):
        if os.path.isdir(board):
            print(f"{root}: already on {BOARD_DIR}/ — skipped")
            return
        die(f"{root}: {PRDS_DIR}/ not found — not a board root")
    if os.path.isdir(board):
        print(f"{root}: already migrated — skipped")
        return
    # git root — a board can sit in a dotdir inside its repo (racer/.mi)
    rc, top, _ = git(root, "rev-parse", "--show-toplevel")
    repo = os.path.realpath(top.strip()) if rc == 0 else root
    stats = {"git": 0, "mv": 0}
    PRDS_BASE = root  # the pre-move home of the board: <root>/prds

    def mv(src, dst):
        # every move speaks board-relative; the wholesale move happens
        # before `board` exists, so it passes the board root as the base
        r = move(base_for(src), repo, src, dst)
        if r in stats:
            stats[r] += 1

    def base_for(src):
        return root if src == PRDS_DIR else board

    # 1. the whole board moves, then sorts itself out inside .pearde/
    mv(PRDS_DIR, BOARD_DIR)
    prds = os.path.join(board, PRDS_DIR)
    state = os.path.join(board, STATE)
    os.makedirs(prds, exist_ok=True)

    # 2. what prds/.state held (it arrived at .pearde/.state in the wholesale
    #    move) gives way to the five loose dotfiles, which land first — the
    #    fuller record; a loser keeps its origin in the name, reported.
    if os.path.isdir(state):
        for f in sorted(os.listdir(state)):
            if f in STATE_FILES:
                mv(os.path.join(STATE, f),
                   os.path.join(STATE, f + ".from-state-dir"))

    # 3. the five state dotfiles -> .state/<name>, leading dot dropped
    for f in STATE_FILES:
        if os.path.exists(os.path.join(board, "." + f)):
            mv("." + f, os.path.join(STATE, f))

    # 4. knowledge/ -> wiki/
    if os.path.isdir(os.path.join(board, "knowledge")):
        mv("knowledge", "wiki")

    # 5. every PRD directory -> prds/; memos/, workflows/, settings.md and
    #    vision.md stay where the wholesale move landed them. A loose prd.md
    #    (a root-recorded PRD) rides into prds/, where the scanner ignores it
    #    exactly as it ignored it at prds/ root.
    for name in sorted(os.listdir(board)):
        if name in KEEP_DIRS or name in KEEP_FILES:
            continue
        p = os.path.join(board, name)
        if os.path.isdir(p) or name == "prd.md":
            mv(name, os.path.join(PRDS_DIR, name))
    rewrite_members(board, quiet)
    rewrite_gitignore(root, quiet)
    mode = f"git mv {stats['git']} / plain {stats['mv']}"
    print(f"{root}: moved to {BOARD_DIR}/ ({mode})")


def main(argv):
    args = list(argv)
    serve, quiet = None, False
    while "--serve" in args:
        i = args.index("--serve")
        serve = args[i + 1]
        del args[i:i + 2]
    if "--quiet" in args:
        quiet = True
        args.remove("--quiet")
    if not args:
        print(__doc__)
        return 2
    for a in args:
        migrate_root(os.path.realpath(os.path.abspath(a)), quiet)
    if serve:
        rewrite_serve(os.path.abspath(serve), quiet)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))