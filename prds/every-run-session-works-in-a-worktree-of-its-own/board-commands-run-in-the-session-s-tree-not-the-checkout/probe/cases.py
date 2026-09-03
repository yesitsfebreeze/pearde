#!/usr/bin/env python3
"""The two cases the end-to-end run does not cover.

    python3 cases.py <scratch-dir>

`nosession` — nothing on the ledger. Every resolver must answer exactly what
it answered before this PRD existed, and a collect must land on the checkout
the old way. This is the compatibility floor: the rule adds a case, it
removes none.

`two` — two sessions hold trees at once, both collect, both land. The second
land is the interesting one: its branch is no longer a descendant of the
branch a person reads, so it must rebase before it fast-forwards, and it must
not take the first session's commit away.
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
    if r.returncode != 0:
        for line in ((r.stdout or "") + (r.stderr or "")).strip().splitlines()[-4:]:
            print("    " + line)
    return r


def tick(spec):
    """Tick every acceptance box. Written as two statements on purpose: one
    `open(p, "w").write(open(p).read()...)` truncates the file before the
    read runs, and the spec then holds no box at all — collect said
    `no acceptance box in specs/ (0/0)` and the probe read it as a code
    defect for one round."""
    with open(spec, encoding="utf-8") as f:
        text = f.read()
    with open(spec, "w", encoding="utf-8") as f:
        f.write(text.replace("- [ ]", "- [x]"))


def take(board, pid):
    env = dict(os.environ, PEARDE_SESSION_PID=str(pid))
    r = subprocess.run([sys.executable, os.path.join(BOARDLIB, "session.py"),
                        "take", "--board", board, "--json"],
                       capture_output=True, text=True, env=env)
    return env, json.loads(r.stdout)


def nosession(root):
    print("\n=== nosession — no ledger, old behaviour ===")
    repo, board = fx.build(os.path.join(root, "nosession"))
    base = git(repo, "rev-parse", "HEAD")
    # PEARDE_SESSION_PID unset AND no `take`: `held` must answer None twice
    env = {k: v for k, v in os.environ.items() if k != "PEARDE_SESSION_PID"}
    ask = f'''
import json, os, sys
sys.path.insert(0, {BOARDLIB!r})
import plan, collect
board = {board!r}
prd = plan.scan(board)["p1"]
print(json.dumps({{"repo_of": collect.repo_of(prd, board,
                                              plan.repo_root(prd["dir"])),
                  "prd_repo": plan.prd_repo(prd)}}))
'''
    r = subprocess.run([sys.executable, "-c", ask], capture_output=True,
                       text=True, env=env)
    ans = json.loads(r.stdout or "{}")
    check("repo_of is the checkout", ans.get("repo_of"), repo)
    check("prd_repo is the checkout", ans.get("prd_repo"), repo)

    pearde(env, "claim", "p1", "probe-worker", "--board", board)
    lane = os.path.join(board, ".lanes", "p1")
    with open(os.path.join(lane, "src", "app.py"), "w") as f:
        f.write("print('two')\n")
    spec = os.path.join(board, "prds", "p1", "specs", "spec01.md")
    tick(spec)
    pearde(env, "collect", "p1", "--board", board)
    check("checkout main moved", git(repo, "rev-list", "--count",
                                     f"{base}..main"), "1")
    check("checkout src/app.py", open(os.path.join(repo, "src",
                                                   "app.py")).read(),
          "print('two')\n")


def two(root):
    print("\n=== two — two sessions, two lands ===")
    repo, board = fx.build(os.path.join(root, "two"))
    fx.write(os.path.join(board, "prds", "p2", "prd.md"),
             "---\nstate: specced\norigin: requested\npriority: 50\n"
             "complexity: 5\nblast-radius: low\n---\n\n"
             "# p2 — another file changes\n\nanother file changes\n")
    fx.write(os.path.join(board, "prds", "p2", "specs", "spec01.md"),
             "---\ncomplexity: 5\nfootprint:\n  - src/other.py\n---\n\n"
             "# spec01 — another file\n\nAnother file.\n\n"
             "## Acceptance\n\n- [x] src/other.py exists\n\n"
             "## Verify and Proof\n\n```sh\ntest -f src/other.py\n```\n")
    fx.git(board, "add", "-A")
    fx.git(board, "commit", "-qm", "p2")
    base = git(repo, "rev-parse", "HEAD")

    a, b = subprocess.Popen(["sleep", "900"]), subprocess.Popen(["sleep", "900"])
    try:
        envA, rowA = take(board, a.pid)
        envB, rowB = take(board, b.pid)
        check("two trees on the ledger", rowA["worktree"] != rowB["worktree"],
              True)

        pearde(envA, "claim", "p1", "worker-a", "--board", board)
        pearde(envB, "claim", "p2", "worker-b", "--board", board)
        laneA = os.path.join(board, ".lanes", "p1")
        laneB = os.path.join(board, ".lanes", "p2")
        check("lane A off session A", git(laneA, "rev-parse", "HEAD"),
              git(rowA["worktree"], "rev-parse", "HEAD"))
        check("lane B off session B", git(laneB, "rev-parse", "HEAD"),
              git(rowB["worktree"], "rev-parse", "HEAD"))

        open(os.path.join(laneA, "src", "app.py"), "w").write("print('two')\n")
        tick(os.path.join(board, "prds", "p1", "specs", "spec01.md"))
        open(os.path.join(laneB, "src", "other.py"), "w").write("# b\n")

        pearde(envA, "collect", "p1", "--board", board)
        pearde(envB, "collect", "p2", "--board", board)
        check("both collects landed on main themselves",
              git(repo, "rev-list", "--count", "--merges", f"{base}..main"),
              "0")
        check("checkout holds A's file after the collects",
              open(os.path.join(repo, "src", "app.py")).read(),
              "print('two')\n")
        check("checkout holds B's file after the collects",
              os.path.isfile(os.path.join(repo, "src", "other.py")), True)

        r = pearde(envA, "session", "land", "--board", board)
        check("A lands", r.returncode, 0)
        afterA = git(repo, "rev-parse", "main")
        r = pearde(envB, "session", "land", "--board", board)
        check("B lands after A", r.returncode, 0)
        check("A's commit still on main",
              git(repo, "merge-base", "--is-ancestor", afterA, "main") or "0",
              "0")
        check("checkout holds A's file",
              open(os.path.join(repo, "src", "app.py")).read(),
              "print('two')\n")
        check("checkout holds B's file",
              os.path.isfile(os.path.join(repo, "src", "other.py")), True)
        check("linear history", git(repo, "rev-list", "--count",
                                    "--merges", f"{base}..main"), "0")
    finally:
        for h in (a, b):
            try:
                os.kill(h.pid, signal.SIGKILL)
            except OSError:
                pass


def dirty(root):
    print("\n=== dirty — the checkout has uncommitted work of its own ===")
    repo, board = fx.build(os.path.join(root, "dirty"))
    h = subprocess.Popen(["sleep", "900"])
    try:
        env, row = take(board, h.pid)
        # a person is mid-edit in the checkout, on the very file the PRD owns
        with open(os.path.join(repo, "src", "app.py"), "w") as f:
            f.write("print('a person was here')\n")
        pearde(env, "claim", "p1", "worker-a", "--board", board)
        lane = os.path.join(board, ".lanes", "p1")
        with open(os.path.join(lane, "src", "app.py"), "w") as f:
            f.write("print('two')\n")
        tick(os.path.join(board, "prds", "p1", "specs", "spec01.md"))
        r = pearde(env, "collect", "p1", "--board", board)
        check("collect still succeeds", r.returncode, 0)
        check("collect says the land was refused",
              "not landed on the branch a person reads"
              in (r.stdout or "") + (r.stderr or ""), True)
        check("the person's uncommitted work is untouched",
              open(os.path.join(repo, "src", "app.py")).read(),
              "print('a person was here')\n")
        # one commit: the PRD's code, on the session branch. The record
        # commit is the BOARD repo's and never went near the checkout.
        check("the work is on the session branch",
              git(repo, "rev-list", "--count", f"main..{row['branch']}"), "1")
    finally:
        try:
            os.kill(h.pid, signal.SIGKILL)
        except OSError:
            pass


def issame(a, b):
    """Two spellings of one path. `mktemp -d` hands out `/var/…` and
    `repo_root` comes back `/private/var/…` on darwin, so an equality on
    raw strings fails on a pair that names one directory."""
    return bool(a) and bool(b) and os.path.realpath(a) == os.path.realpath(b)


def sub(code):
    r = subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, timeout=300)
    return (r.stdout or "").strip(), (r.stderr or "").strip(), r.returncode


def reset(S, pid):
    """Clear both caches and say which session this process is.

    `my_id` and `cached_ledger` are process-lifetime by design — a process
    cannot change which session it is inside, and the resolver is on the
    scan's per-PRD path. A test that asks one process about several ledgers
    is the one caller that has to clear them."""
    S._MINE.clear()
    S._LEDGER_CACHE.clear()
    if pid is None:
        os.environ.pop("PEARDE_SESSION_PID", None)
    else:
        os.environ["PEARDE_SESSION_PID"] = str(pid)


def units(root):
    """What the resolver answers when there is nothing to resolve, and what
    the three spelling functions say about a tree the board hosts. The
    end-to-end runs above never ask either question directly: they see the
    answer only through a collect that did or did not land."""
    print("\n=== units — the resolver's own answers ===")
    repo, board = fx.build(os.path.join(root, "units"))
    sys.path.insert(0, BOARDLIB)
    import collect as C
    import plan as P
    import session as S

    me = os.getpid()
    ident = "s%d" % me
    reset(S, me)
    check("held with no ledger", S.held(board), None)
    check("instead_of with no ledger is the repo it was handed",
          issame(S.instead_of(board, repo), repo), True)

    # a row naming a tree nobody cut — a reap that raced, or an rm -rf
    S.write_ledger(board, [{"id": ident, "repo": repo, "branch": "session/x",
                            "worktree": os.path.join(board, ".sessions",
                                                     "gone")}])
    reset(S, me)
    check("held when the ledger's worktree is not on disk", S.held(board),
          None)

    env, row = take(board, me)
    reset(S, me)
    check("held is the session's tree", issame(S.held(board, repo),
                                               row["worktree"]), True)
    check("held for a row whose repo is another repo",
          S.held(board, os.path.join(root, "elsewhere")), None)

    orig = S.session_pid
    S.session_pid = lambda: None
    S._MINE.clear()
    check("held with no session process", S.held(board), None)
    check("instead_of with no session process",
          issame(S.instead_of(board, repo), repo), True)
    S.session_pid = orig

    with open(S.ledger_path(board), "w", encoding="utf-8") as f:
        f.write("{ this is not json")
    reset(S, me)
    try:
        got = issame(S.instead_of(board, repo), repo)
    except Exception as e:                                    # noqa: BLE001
        got = "raised " + type(e).__name__
    check("instead_of on a malformed ledger", got, True)
    S.write_ledger(board, [row])

    calls = []
    S.session_pid = lambda: (calls.append(1), me)[1]
    S._MINE.clear()
    os.environ.pop("PEARDE_SESSION_PID", None)
    for _ in range(5):
        S.my_id()
    check("my_id walks the process tree once for five asks", len(calls), 1)
    S.session_pid = orig
    reset(S, me)

    # this board is reached as `pearde/` and as the `.pearde` symlink beside
    # it — a tree named through one and a board named through the other
    link = os.path.join(root, "units", "board-link")
    if os.path.islink(link):
        os.unlink(link)
    os.symlink(board, link)
    reset(S, me)
    check("held through a symlinked board",
          issame(S.held(link, repo), row["worktree"]), True)
    check("under() is a real-path test",
          C.under(link, row["worktree"]), True)

    board_root = P.repo_root(board)
    other = os.path.join(root, "units", "other")
    os.makedirs(other, exist_ok=True)
    fx.git(other, "init", "-q", "-b", "main")
    fx.git(other, "config", "user.email", "probe@example.com")
    fx.git(other, "config", "user.name", "probe")
    fx.write(os.path.join(other, "x.py"), "x\n")
    fx.git(other, "add", "-A")
    fx.git(other, "commit", "-qm", "base")

    check("checkout_of for a board that is its own repo",
          issame(C.checkout_of(board, board_root), repo), True)
    check("checkout_of for a board that is a plain dir in a repo",
          issame(C.checkout_of(os.path.join(repo, "notaboard"), repo), repo),
          True)
    check("spelling_root for a repo the board hosts",
          issame(C.spelling_root(board, board_root, row["worktree"]), repo),
          True)
    check("spelling_root for a repo outside the board",
          issame(C.spelling_root(board, board_root, other), other), True)

    check("a footprint under the board still routes to the board's repo",
          C.foot_root(".pearde/.gitignore", board, board_root,
                      row["worktree"]), (board_root, ".gitignore"))
    check("ordinary code routes to the session's tree",
          C.foot_root("src/app.py", board, board_root, row["worktree"]),
          (row["worktree"], "src/app.py"))

    prd = P.scan(board)["p1"]
    prd["fm"]["repo"] = other
    reset(S, me)
    check("repo_of with a repo: key the ledger does not name",
          issame(C.repo_of(prd, board, board_root), other), True)
    wt = os.path.join(root, "units", "other-tree")
    fx.git(other, "worktree", "add", "-q", "-b", "session/" + ident, wt)
    S.write_ledger(board, [dict(row, repo=other, worktree=wt)])
    reset(S, me)
    check("repo_of with a repo: key the ledger does name",
          issame(C.repo_of(prd, board, board_root), wt), True)
    S.write_ledger(board, [row])
    reset(S, me)

    # `sys.modules[name] = None` is an ImportError on the next import — the
    # module absent, without moving a file another test is reading.
    head = ("import sys\nsys.path.insert(0, %r)\n"
            "sys.modules['session'] = None\n" % BOARDLIB)
    out, err, rc = sub(head + "import plan\n"
                       "print(plan.prd_repo(plan.scan(%r)['p1']))\n" % board)
    check("plan.prd_repo with session.py absent", (rc, issame(out, repo)),
          (0, True))
    out, err, rc = sub(head + "import collect\n"
                       "print(repr(collect.land_session(%r)))\n" % board)
    check("land_session with session.py absent", (rc, out), (0, "''"))

    os.remove(S.ledger_path(board))
    reset(S, me)
    check("land_session with no ledger", C.land_session(board), "")
    S.write_ledger(board, [row])
    reset(S, me)

    def boom(*a, **k):
        raise RuntimeError("git said no")
    orig_land, S.land = S.land, boom
    said = C.land_session(board)
    S.land = orig_land
    check("land_session when land raises",
          said.startswith("not landed on the branch a person reads"), True)
    os.environ.pop("PEARDE_SESSION_PID", None)


def edges(root):
    """The two refusals `land` owes, the trunk that is not called `main`,
    and the help line that has to name the verb."""
    print("\n=== edges — what land refuses, and the branch it aims at ===")
    repo, board = fx.build(os.path.join(root, "trunk"))
    fx.git(repo, "branch", "-m", "main", "trunk")
    h = subprocess.Popen(["sleep", "900"])
    try:
        env, row = take(board, h.pid)
        wt, br = row["worktree"], row["branch"]
        fx.write(os.path.join(wt, "src", "app.py"), "print('two')\n")
        fx.git(wt, "add", "-A")
        fx.git(wt, "commit", "-qm", "in the session")
        r = pearde(env, "session", "land", "--board", board)
        check("land on a trunk that is not called main", r.returncode, 0)
        check("the trunk carries the session's commit",
              git(repo, "rev-list", "--count", f"trunk..{br}"), "0")
        check("no merge commit on the trunk",
              git(repo, "rev-list", "--count", "--merges", "trunk"), "0")
        check("the checkout's own file moved",
              open(os.path.join(repo, "src", "app.py")).read(),
              "print('two')\n")

        # the checkout parked on the session's own branch
        lp = os.path.join(board, ".state", "sessions.json")
        with open(lp, encoding="utf-8") as f:
            data = json.load(f)
        data["sessions"][0]["branch"] = "trunk"
        with open(lp, "w", encoding="utf-8") as f:
            json.dump(data, f)
        r = pearde(env, "session", "land", "--board", board)
        check("land refuses the branch the checkout is already on",
              r.returncode, 1)
        check("and says why", "already the branch a person reads"
              in (r.stdout or "") + (r.stderr or ""), True)
    finally:
        try:
            os.kill(h.pid, signal.SIGKILL)
        except OSError:
            pass

    repo, board = fx.build(os.path.join(root, "dirtyland"))
    h = subprocess.Popen(["sleep", "900"])
    try:
        env, row = take(board, h.pid)
        wt, br = row["worktree"], row["branch"]
        fx.write(os.path.join(wt, "src", "app.py"), "print('two')\n")
        fx.git(wt, "add", "-A")
        fx.git(wt, "commit", "-qm", "in the session")
        mine = "print('a person was here')\n"
        with open(os.path.join(repo, "src", "app.py"), "w") as f:
            f.write(mine)
        r = pearde(env, "session", "land", "--board", board)
        check("land into a dirty checkout exits 1", r.returncode, 1)
        check("the person's uncommitted work is byte-identical",
              open(os.path.join(repo, "src", "app.py")).read(), mine)
        check("the commit is still on the session branch",
              git(repo, "rev-list", "--count", f"main..{br}"), "1")
    finally:
        try:
            os.kill(h.pid, signal.SIGKILL)
        except OSError:
            pass

    r = subprocess.run([sys.executable, PEARDE, "help"], capture_output=True,
                       text=True, timeout=120)
    line = [ln for ln in (r.stdout or "").splitlines()
            if ln.strip().startswith("pearde session")]
    check("pearde help names the verb", bool(line) and "land" in line[0], True)


def main(argv):
    root = os.path.abspath(argv[0] if argv else "/tmp/pearde-session-cases")
    nosession(root)
    two(root)
    dirty(root)
    units(root)
    edges(root)
    print("\n" + ("FAILED: " + ", ".join(FAIL) if FAIL else "all checks pass"))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
