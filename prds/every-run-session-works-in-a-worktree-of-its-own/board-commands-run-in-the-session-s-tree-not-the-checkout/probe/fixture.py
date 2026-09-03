#!/usr/bin/env python3
"""Build a throwaway code repo + board, take a session in it, and report
which tree every board command calls "the code repo".

    python3 fixture.py <dir>          build it, print the paths
    python3 fixture.py <dir> --keep   do not wipe an existing <dir>

The fixture is a plain code repo whose board is a gitignored `.pearde/`
subdirectory — the layout `lanes.board_rel` returns None for, so nothing
here depends on the sparse-checkout exclusion. One PRD, `p1`, footprint
`src/`.
"""
import json
import os
import shutil
import subprocess
import sys

RES = os.environ.get("PEARDE_RES") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..",
    "..", "resources")
RES = os.path.abspath(RES)


def git(root, *args, check=True):
    r = subprocess.run(("git", "-C", root) + args,
                       capture_output=True, text=True, timeout=60)
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} in {root}:\n{r.stderr}")
    return r


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def build(root, keep=False):
    if os.path.isdir(root) and not keep:
        shutil.rmtree(root)
    repo = os.path.join(root, "code")
    board = os.path.join(repo, ".pearde")
    os.makedirs(repo, exist_ok=True)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "probe@example.com")
    git(repo, "config", "user.name", "probe")
    write(os.path.join(repo, ".gitignore"), ".pearde/\n")
    write(os.path.join(repo, "src", "app.py"), "print('one')\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "base")

    # The board is a git repo of its own inside the code repo — the layout
    # this machine runs (`.pearde` is a worktree of the code repo there), and
    # the one `collect.repo_of`'s `board_root == board` branch is written for.
    os.makedirs(board, exist_ok=True)
    git(board, "init", "-q", "-b", "pearde")
    git(board, "config", "user.email", "probe@example.com")
    git(board, "config", "user.name", "probe")

    write(os.path.join(board, ".gitignore"),
          ".lanes/\n.sessions/\n.state/\nprds/.claims/\n")
    write(os.path.join(board, "settings.md"),
          "# settings\n\n- workers: 4\n- claim-ttl: 30m\n")
    write(os.path.join(board, "vision.md"), "# vision\n\nprobe fixture\n")
    write(os.path.join(board, "prds", "p1", "prd.md"),
          "---\nstate: specced\norigin: requested\npriority: 50\n"
          "complexity: 5\nblast-radius: low\n---\n\n"
          "# p1 — one file changes\n\none file changes\n")
    write(os.path.join(board, "prds", "p1", "specs", "spec01.md"),
          "---\ncomplexity: 5\nfootprint:\n  - src/app.py\n---\n\n"
          "# spec01 — change one file\n\nOne file changes.\n\n"
          "## Acceptance\n\n- [ ] src/app.py says two\n\n"
          "## Verify and Proof\n\n```sh\ngrep -q two src/app.py\n```\n")
    git(board, "add", "-A")
    git(board, "commit", "-qm", "board")
    return repo, board


def main(argv):
    root = os.path.abspath(argv[0])
    keep = "--keep" in argv
    repo, board = build(root, keep)
    print(json.dumps({"root": root, "repo": repo, "board": board,
                      "resources": RES}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
