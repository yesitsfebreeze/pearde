#!/usr/bin/env python3
"""What does a board command call "the code repo" while a session holds a
worktree of its own?

    python3 measure.py <scratch-dir>

Builds the fixture, starts a stand-in session process, `session take`s a
worktree for it, and then asks every resolver on the board the same
question. Prints one row per resolver: the tree it named, and whether that
is the checkout or the session's own worktree.
"""
import json
import os
import signal
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fixture as fx  # noqa: E402

BOARDLIB = os.path.join(fx.RES, "board")


def run(cmd, env=None, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180,
                       env=env, cwd=cwd)
    return r


def main(argv):
    root = os.path.abspath(argv[0] if argv else "/tmp/pearde-session-probe")
    repo, board = fx.build(root)

    holder = subprocess.Popen(["sleep", "900"])
    env = dict(os.environ, PEARDE_SESSION_PID=str(holder.pid),
               PYTHONPATH=BOARDLIB)
    try:
        r = run([sys.executable, os.path.join(BOARDLIB, "session.py"),
                 "take", "--board", board, "--json"], env=env)
        print("== session take ==")
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode != 0:
            return 1
        row = json.loads(r.stdout)
        tree = row["worktree"]

        ask = f'''
import json, os, sys
sys.path.insert(0, {BOARDLIB!r})
import plan, collect, brief, session
board = {board!r}
prds = plan.scan(board)
prd = prds["p1"]
root = plan.repo_root(prd["dir"])
out = {{
  "plan.repo_root(board)": plan.repo_root(board),
  "plan.prd_repo(prd)": plan.prd_repo(prd),
  "collect.repo_of(prd)": collect.repo_of(prd, board, root),
  "brief.repo_of(prd)": brief.repo_of(prd, board),
  "session.repo_of(board)": session.repo_of(board),
  "session tree on the ledger": {tree!r},
}}
print(json.dumps(out, indent=2))
'''
        r = run([sys.executable, "-c", ask], env=env)
        print("== resolvers ==")
        print(r.stdout or r.stderr)
        if r.returncode != 0:
            return 1
        answers = json.loads(r.stdout)
        print("== verdict ==")
        for k, v in answers.items():
            if k == "session tree on the ledger":
                continue
            where = ("SESSION TREE" if v == tree else
                     "checkout" if v == repo else v)
            print(f"  {k:<28} {where}")
        return 0
    finally:
        try:
            os.kill(holder.pid, signal.SIGKILL)
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
