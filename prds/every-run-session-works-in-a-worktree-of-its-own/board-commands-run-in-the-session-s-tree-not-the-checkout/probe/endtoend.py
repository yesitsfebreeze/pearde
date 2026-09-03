#!/usr/bin/env python3
"""One PRD, start to finish, while a session holds a worktree of its own.

    python3 endtoend.py <scratch-dir>

claim → lane → the worker writes → collect → land. Asserts at every step
which tree moved and which did not: the checkout the person reads must not
move until `session land`, and then it must hold exactly the collect's
commit.
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
PEARDE = os.path.join(fx.RES, "pearde.py")
FAIL = []


def git(root, *args):
    return fx.git(root, *args, check=False).stdout.strip()


def check(name, got, want):
    ok = got == want
    print(("  ok   " if ok else "  FAIL ") + f"{name}: {got!r}"
          + ("" if ok else f" != {want!r}"))
    if not ok:
        FAIL.append(name)


def pearde(env, *args):
    r = subprocess.run([sys.executable, PEARDE] + list(args),
                       capture_output=True, text=True, timeout=300, env=env)
    print(f"$ pearde {' '.join(args[:2])} → {r.returncode}")
    tail = (r.stdout or "") + (r.stderr or "")
    for line in tail.strip().splitlines()[-6:]:
        print("    " + line)
    return r


def main(argv):
    root = os.path.abspath(argv[0] if argv else "/tmp/pearde-session-e2e")
    repo, board = fx.build(root)
    base = git(repo, "rev-parse", "HEAD")

    holder = subprocess.Popen(["sleep", "900"])
    env = dict(os.environ, PEARDE_SESSION_PID=str(holder.pid))
    try:
        r = subprocess.run([sys.executable,
                            os.path.join(BOARDLIB, "session.py"),
                            "take", "--board", board, "--json"],
                           capture_output=True, text=True, env=env)
        row = json.loads(r.stdout)
        tree, br = row["worktree"], row["branch"]
        print(f"session tree {tree}\nsession branch {br}\n")

        print("== the session commits something of its own ==")
        # the session's branch moves ahead of the checkout, so "the lane was
        # cut off the session tree" and "off the checkout" stop looking alike
        with open(os.path.join(tree, "src", "only.py"), "w") as f:
            f.write("# only the session has this\n")
        fx.git(tree, "add", "-A")
        fx.git(tree, "commit", "-qm", "session-only")
        check("session branch ahead before the claim",
              git(repo, "rev-list", "--count", f"main..{br}"), "1")

        print("== claim ==")
        pearde(env, "claim", "p1", "probe-worker", "--board", board)
        lane = os.path.join(board, ".lanes", "p1")
        check("lane on disk", os.path.isdir(lane), True)
        # the lane must be cut off the SESSION's branch, not off the checkout
        check("lane's upstream commit", git(lane, "rev-parse", "HEAD"),
              git(tree, "rev-parse", "HEAD"))
        check("lane holds the session-only file",
              os.path.isfile(os.path.join(lane, "src", "only.py")), True)

        print("\n== the worker writes in its lane ==")
        with open(os.path.join(lane, "src", "app.py"), "w") as f:
            f.write("print('two')\n")
        with open(os.path.join(board, "prds", "p1", "specs", "spec01.md")) as f:
            spec = f.read()
        with open(os.path.join(board, "prds", "p1", "specs", "spec01.md"),
                  "w") as f:
            f.write(spec.replace("- [ ]", "- [x]"))

        print("\n== collect ==")
        pearde(env, "collect", "p1", "--board", board)

        print("\n== where did the commit land ==")
        check("collect landed it on main itself",
              git(repo, "rev-list", "--count", f"main..{br}"), "0")
        check("checkout src/app.py now says two",
              open(os.path.join(repo, "src", "app.py")).read(),
              "print('two')\n")
        check("session tree src/app.py",
              open(os.path.join(tree, "src", "app.py")).read(),
              "print('two')\n")
        landed = git(tree, "rev-parse", "HEAD")

        print("\n== land again — nothing left ==")
        r = pearde(env, "session", "land", "--board", board)
        check("land exit", r.returncode, 0)
        check("checkout main is the session's commit",
              git(repo, "rev-parse", "main"), landed)
        check("checkout src/app.py now says two",
              open(os.path.join(repo, "src", "app.py")).read(),
              "print('two')\n")
        check("main..session empty", git(repo, "rev-list", "--count",
                                         f"main..{br}"), "0")
        check("one commit for the PRD",
              git(repo, "rev-list", "--count", f"{base}..main"), "2")
    finally:
        try:
            os.kill(holder.pid, signal.SIGKILL)
        except OSError:
            pass
    print("\n" + ("FAILED: " + ", ".join(FAIL) if FAIL else "all checks pass"))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
