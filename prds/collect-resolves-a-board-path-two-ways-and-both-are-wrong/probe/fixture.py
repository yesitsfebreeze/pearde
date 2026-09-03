#!/usr/bin/env python3
"""Fixture boards for the three layouts `foot_root` has to tell apart.

Every fixture is built in a directory made at run time (`tempfile.mkdtemp`),
never under the board — a directory holding `prd.md` anywhere under the board
is a PRD.

  L1 plain      code repo R, board R/.pearde, a plain directory.
                board_root (repo_root of the PRD dir) is R, board != root.
  L2 own-repo   code repo R, board R/pearde with a `.git` of its own.
                board_root == board; repo_of returns the enclosing R.
  L3 under      board B, its own repo, and the CODE repo checked out
                UNDERNEATH it at B/work — what a run-session worktree and a
                lane both are. `repo:` in the PRD names it.
"""
import os
import subprocess
import tempfile


def git(cwd, *args, check=True):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True,
                          text=True, check=check)


def init(d):
    os.makedirs(d, exist_ok=True)
    git(d, "init", "-q", "-b", "main")
    git(d, "config", "user.email", "probe@example.com")
    git(d, "config", "user.name", "probe")
    return d


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    return path


SETTINGS = """---
name: probe
language: English
workers: 1
pipeline: 1
weight-default: 20
gantt-day: 8h
complexity-cap: 40
specs-cap: 6
---

# The probe board
"""


def prd(footprints, repo=None, name="finished"):
    feet = "\n".join(f"  - {f}" for f in footprints)
    r = f"repo: {repo}\n" if repo else ""
    return f"""---
state: claimed
origin: requested
priority: 55
complexity: 10
blast-radius: low
{r}claim: worker-probe 2020-01-01 12:00
footprint:
{feet}
---

# {name} — every box closed, a worker still holding it

The band to collect.
"""


def spec(footprints):
    feet = "\n".join(f"  - {f}" for f in footprints)
    return f"""---
complexity: 10
footprint:
{feet}
---

# spec01 — the unit

## Acceptance

- [x] the unit is written

## Verify and Proof

```sh
true
```
"""


def board_files(bdir, footprints, repo=None):
    write(os.path.join(bdir, "settings.md"), SETTINGS)
    p = os.path.join(bdir, "prds", "finished")
    write(os.path.join(p, "prd.md"), prd(footprints, repo))
    write(os.path.join(p, "specs", "spec01.md"), spec(footprints))
    return p


def commit_all(d, msg="fixture"):
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", msg, check=False)


def l1_plain(root=None):
    """Board is a plain directory inside the code repo."""
    r = init(root or tempfile.mkdtemp(prefix="probe-l1-"))
    write(os.path.join(r, "src", "util.py"), "x = 1\n")
    board = os.path.join(r, ".pearde")
    board_files(board, ["src/util.py"])
    commit_all(r)
    return {"repo": r, "board": board}


def l2_own_repo(root=None):
    """Board is a git repo of its own, nested in the code repo.

    Its PRD's footprint names a file the BOARD holds, spelled the board's
    own way — `prds/finished/probe/verify.sh`, which is where every probe
    this board runs is told to live.
    """
    r = init(root or tempfile.mkdtemp(prefix="probe-l2-"))
    write(os.path.join(r, "src", "util.py"), "x = 1\n")
    write(os.path.join(r, ".gitignore"), "pearde/\n")
    commit_all(r)
    board = init(os.path.join(r, "pearde"))
    p = board_files(board, ["src/util.py",
                            "prds/finished/probe/verify.sh"])
    write(os.path.join(p, "probe", "verify.sh"), "#!/bin/sh\ntrue\n")
    commit_all(board)
    return {"repo": r, "board": board}


def l3_code_under_board(root=None):
    """The code repo is checked out UNDERNEATH the board.

    A lane worktree (`<board>/.lanes/<prd>`) and a run-session worktree are
    both this shape. The footprint is spelled against that code repo.
    """
    top = root or tempfile.mkdtemp(prefix="probe-l3-")
    board = init(os.path.join(top, "board"))
    work = init(os.path.join(board, "work"))
    write(os.path.join(work, "src", "util.py"), "x = 1\n")
    commit_all(work)
    write(os.path.join(board, ".gitignore"), "work/\n")
    board_files(board, ["src/util.py"], repo=work)
    commit_all(board)
    return {"repo": work, "board": board}


LAYOUTS = {"l1": l1_plain, "l2": l2_own_repo, "l3": l3_code_under_board}
