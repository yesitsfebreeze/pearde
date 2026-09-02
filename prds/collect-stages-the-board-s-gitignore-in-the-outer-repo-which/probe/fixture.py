#!/usr/bin/env python3
"""Build the layout this PRD is about, in a fresh temp dir, and run
`collect` on it.

The layout, which is this repo's since 2026-09-02:

    <code>/                 git repo, branch main
      .gitignore            holds `/pearde` — the code repo IGNORES the board
      resources/board/session.py
      pearde/               a git repo of its own — the BOARD
        .gitignore          tracked in the BOARD repo, untracked in <code>
        prds/p1/prd.md      claimed, every box closed
        prds/p1/specs/spec01.md   footprint: a code path AND `pearde/.gitignore`
        .lanes/p1           the worker's worktree, cut off <code>

A spec whose footprint names a file under the board is what `pearde
session` needed (`.sessions/` had to get a row in the board's own
`.gitignore`), and it is what collect cannot do: the footprint is filed
against the CODE repo, so `git add -- pearde/.gitignore` runs in a tree
that ignores that path and holds no such file.

Usage:  python3 fixture.py [<dir>]     — builds and runs, prints what happened
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def _src():
    """The checkout under test. `PEARDE_SRC` wins; otherwise the first tree
    at or above the working directory that holds `resources/board/collect.py`
    — so the probe measures the lane it is run from and not whichever tree
    its author happened to be in."""
    if os.environ.get("PEARDE_SRC"):
        return os.environ["PEARDE_SRC"]
    d = os.getcwd()
    while True:
        if os.path.isfile(os.path.join(d, "resources/board/collect.py")):
            return d
        up = os.path.dirname(d)
        if up == d:
            raise SystemExit("fixture: no resources/board/collect.py at or "
                             "above the working directory — run it from the "
                             "checkout under test, or set PEARDE_SRC")
        d = up


SRC = _src()


def sh(cwd, *args, check=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"fixture: {' '.join(args)} in {cwd} failed:\n"
                         f"{r.stdout}{r.stderr}")
    return r


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


PRD = """---
state: claimed
origin: requested
priority: 50
complexity: 4
blast-radius: low
claim: probe 2026-09-02 10:00
---

# p1 — a session ledger gets its row in the board's own gitignore
"""

SPEC = """---
complexity: 4
footprint:
  - resources/board/session.py
  - pearde/.gitignore
---

# spec01 — the session tree is not dirt on the board branch

## Acceptance

- [x] `session.py` stands
- [x] the board's ignore file names `.sessions/`

## Verify

```bash
true
```
"""

SETTINGS = """---
board: probe
language: English
max-complexity: 40
max-specs: 6
---

# settings
"""


def build(root):
    code = os.path.join(root, "code")
    board = os.path.join(code, "pearde")
    os.makedirs(code)
    sh(code, "git", "init", "-q", "-b", "main")
    sh(code, "git", "config", "user.email", "probe@example.com")
    sh(code, "git", "config", "user.name", "probe")
    write(os.path.join(code, ".gitignore"), "/pearde\n")
    write(os.path.join(code, "resources/board/session.py"), "# session\n")
    sh(code, "git", "add", "-A")
    sh(code, "git", "commit", "-qm", "base")

    # the board: its own repo, ignored by the code repo
    os.makedirs(board)
    sh(board, "git", "init", "-q", "-b", "pearde")
    sh(board, "git", "config", "user.email", "probe@example.com")
    sh(board, "git", "config", "user.name", "probe")
    write(os.path.join(board, ".gitignore"), ".lanes/\n.claims/\n.state/\n")
    write(os.path.join(board, "settings.md"), SETTINGS)
    write(os.path.join(board, "prds/p1/prd.md"), PRD)
    write(os.path.join(board, "prds/p1/specs/spec01.md"), SPEC)
    sh(board, "git", "add", "-A")
    sh(board, "git", "commit", "-qm", "board")
    return code, board


def work(code, board):
    """What the worker leaves standing: the code edit in its lane, and the
    board edit in the board — the only tree that holds that file."""
    sys.path.insert(0, os.path.join(SRC, "resources", "board"))
    import lanes as laneslib
    lane = laneslib.create(board, code, "p1")
    write(os.path.join(lane, "resources/board/session.py"),
          "# session\ndef take():\n    pass\n")
    gi = os.path.join(board, ".gitignore")
    if os.path.isfile(gi):          # only the nested-repo layout has one
        with open(gi, "a", encoding="utf-8") as f:
            f.write(".sessions/\n")
    return lane


FLAT_SPEC = """---
complexity: 4
footprint:
  - resources/board/session.py
---

# spec01 — the flat layout, where the board is not its own repo

## Acceptance

- [x] `session.py` stands

## Verify

```bash
true
```
"""


def build_flat(root):
    """The other layout, and the regression check: the board is `.pearde/`
    INSIDE the code repo and is not a repo of its own, so `board_root` and
    `repo` are the same root and no footprint path is ever rerouted."""
    code = os.path.join(root, "code")
    board = os.path.join(code, ".pearde")
    os.makedirs(code)
    sh(code, "git", "init", "-q", "-b", "main")
    sh(code, "git", "config", "user.email", "probe@example.com")
    sh(code, "git", "config", "user.name", "probe")
    write(os.path.join(code, ".gitignore"), ".pearde/.lanes/\n")
    write(os.path.join(code, "resources/board/session.py"), "# session\n")
    write(os.path.join(board, "settings.md"), SETTINGS)
    write(os.path.join(board, "prds/p1/prd.md"), PRD)
    write(os.path.join(board, "prds/p1/specs/spec01.md"), FLAT_SPEC)
    sh(code, "git", "add", "-A")
    sh(code, "git", "commit", "-qm", "base")
    return code, board


def run(code, board):
    env = dict(os.environ, PEARDE_PORT="1")
    return subprocess.run(
        [sys.executable, os.path.join(SRC, "resources/board/collect.py"),
         "p1", "--board", board, "--as", "engineer", "--trust"],
        cwd=code, capture_output=True, text=True, env=env)


def flat(root):
    code, board = build_flat(root)
    lane = work(code, board)
    r = run(code, board)
    print(f"flat layout: collect exit {r.returncode}")
    print(r.stdout.rstrip())
    if r.stderr.strip():
        print("stderr:\n" + r.stderr.rstrip())
    print("code status after: " + subprocess.run(
        ["git", "-C", code, "status", "--porcelain"],
        capture_output=True, text=True).stdout.strip().__repr__())
    return r.returncode


def check():
    """Both layouts, asserted. Exit 0 only when the nested-repo board gets
    its `.gitignore` COMMITTED IN THE BOARD REPO and the flat board is
    untouched by the routing. Red against the tree before the fix."""
    bad = []
    root = tempfile.mkdtemp(prefix="pearde-gitignore-check-")

    n = os.path.join(root, "nested")
    os.makedirs(n)
    code, board = build(n)
    work(code, board)
    r = run(code, board)
    if r.returncode != 0:
        say = ((r.stderr or r.stdout).strip().splitlines() or [""])[-1]
        bad.append(f"nested: collect exit {r.returncode} — {say}")
    dirt = subprocess.run(["git", "-C", board, "status", "--porcelain",
                           "--", ".gitignore"], capture_output=True,
                          text=True).stdout.strip()
    if dirt:
        bad.append(f"nested: the board's .gitignore is still dirty ({dirt}) "
                   "— collect did not commit it in the board repo")
    log = subprocess.run(["git", "-C", board, "log", "--name-only",
                          "--pretty=format:", "-3"], capture_output=True,
                         text=True).stdout.split()
    if ".gitignore" not in log:
        bad.append("nested: no board commit holds .gitignore")

    f = os.path.join(root, "flat")
    os.makedirs(f)
    code2, board2 = build_flat(f)
    work(code2, board2)
    r2 = run(code2, board2)
    if r2.returncode != 0:
        bad.append(f"flat: collect exit {r2.returncode} — the flat layout "
                   "regressed")

    for line in bad:
        print("FAIL " + line)
    if not bad:
        print("PASS both layouts: the board's own file is committed in the "
              "board repo, the flat layout is unchanged")
    print(f"fixture: {root}")
    return 1 if bad else 0


def mutant():
    """Prove `--check` can fail. Copy the tree under test, neuter
    `foot_root` so it routes nothing — the behaviour before this PRD — and
    assert the check goes RED against that copy. Exit 0 when it did.

    A check nobody has watched fail is a green box, not a guard."""
    import shutil
    d = tempfile.mkdtemp(prefix="pearde-gitignore-mutant-")
    tree = os.path.join(d, "src")
    shutil.copytree(SRC, tree, symlinks=True, ignore=shutil.ignore_patterns(
        ".git", ".lanes", ".sessions", "node_modules", "__pycache__"))
    src = os.path.join(tree, "resources/board/collect.py")
    text = open(src, encoding="utf-8").read()
    marker = "def foot_root(p, board, board_root, repo):"
    if marker not in text:
        print("FAIL mutant: no foot_root in the tree under test")
        return 1
    head, _, rest = text.partition(marker)
    body = "\n    return repo, p          # mutant: route nothing\n"
    open(src, "w", encoding="utf-8").write(head + marker + body + rest)
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--check"],
                       cwd=tree, capture_output=True, text=True,
                       env=dict(os.environ, PEARDE_SRC=tree))
    shutil.rmtree(d, ignore_errors=True)
    if r.returncode == 0:
        print("FAIL mutant: the check passed against a tree that routes "
              "nothing — it proves nothing")
        return 1
    print("PASS mutant: the check goes red when foot_root routes nothing")
    return 0


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(
        prefix="pearde-gitignore-probe-")
    if "--mutant" in sys.argv:
        return mutant()
    if "--check" in sys.argv:
        return check()
    if "--flat" in sys.argv:
        os.makedirs(root, exist_ok=True)
        return flat(root)
    if os.path.exists(os.path.join(root, "code")):
        raise SystemExit(f"fixture: {root}/code exists — pick a fresh dir")
    os.makedirs(root, exist_ok=True)
    code, board = build(root)
    lane = work(code, board)
    print(f"fixture: {root}")
    print(f"  code repo  {code}   ignores /pearde")
    print(f"  board repo {board}  tracks .gitignore")
    print(f"  lane       {lane}")
    print("  lane holds pearde/.gitignore? "
          + str(os.path.exists(os.path.join(lane, "pearde", ".gitignore"))))
    print()
    # PEARDE_PORT at a dead port: the fixture must not reach the machine's
    # live daemon, and reaching it CRASHES collect — `post_report` calls
    # `os.path.abspath` on a registered board's `path`, and a master board
    # registers with `path: None`. Separate defect, reported, not fixed here.
    env = dict(os.environ, PEARDE_PORT="1")
    r = subprocess.run(
        [sys.executable, os.path.join(SRC, "resources/board/collect.py"),
         "p1", "--board", board, "--as", "engineer", "--trust"],
        cwd=code, capture_output=True, text=True, env=env)
    print(f"collect exit {r.returncode}")
    print(r.stdout.rstrip())
    if r.stderr.strip():
        print("stderr:")
        print(r.stderr.rstrip())
    print()
    print("board .gitignore committed? " + subprocess.run(
        ["git", "-C", board, "status", "--porcelain", "--", ".gitignore"],
        capture_output=True, text=True).stdout.strip().__repr__())
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
