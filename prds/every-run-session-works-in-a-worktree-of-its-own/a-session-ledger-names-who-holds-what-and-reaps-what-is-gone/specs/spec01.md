---
complexity: 16
footprint:
  - resources/board/session.py
---

# spec01 — `pearde session take/list/reap/owns`

One module giving a run session what `resources/board/lanes.py` already gives
a worker: a git worktree of its own, a ledger row saying who holds it and how
to tell that holder is alive, and a reaper that puts everything a dead session
left into the object store before it removes anything. `pearde.py` discovers
it by its `COMMANDS` dict, so no file outside the footprint is edited to route
the command.

**This already stands**, built in this PRD's lane and measured by the probe at
`prds/every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe/verify.sh`
— 25 assertions, green. The four verbs, the ledger, the three-valued liveness
test and the snapshot are all built and exercised. What is left is landing the
file on the branch a person reads; nothing in this spec is unbuilt design.

The four decisions the build settled, each measured rather than argued:

**Identity is the session's own process.** `session_pid()` walks the process
tree up from the calling process to the first whose command is `claude`. Every
command a session runs is a descendant of it, so `take` run from a session's
shell finds that session and no other — measured on the live machine: the id
resolved to `s60704`, and `/tmp/cc-socks/60704.sock` was there for it.
`PEARDE_SESSION_PID` overrides the walk, which is how the probe drives four
sessions without four terminals.

**Liveness is three-valued and only `dead` reaps.** Alive is a running pid
whose `ps -o lstart=` matches the row's. Dead is a pid that is gone, or one
running under a different start time — a reused pid, measured: a row pointed
at a live pid with a 1990 start time read `dead`. **Unknown** is `ps` refusing
to answer, or a row that never recorded a start time, and unknown is kept, not
reaped — measured: a running pid with an empty `started` was reported `keep`
and its directory survived. The false positive here destroys the work the
whole PRD exists to protect, so the test refuses to guess. The socket under
`/tmp/cc-socks/` is corroboration in `list`, never a verdict on its own.

**The reaper snapshots without touching the tree it snapshots.** `git stash
push -u` captures the same content — measured — but stash is one of the four
commands the memo puts out of bounds in a tree the running session does not
own, and it reverts the worktree before a removal that may then fail. So the
snapshot copies the dead worktree's own index, `git add -A` into that copy,
`write-tree`, `commit-tree`, and `update-ref refs/pearde/reaped/<id>`.
Measured in the probe: a tracked edit, a staged rename, an untracked file and
an untracked nested directory all reached the commit, the content of the edit
was readable back out of the object store, the worktree was byte-identical
after the snapshot, and the ref outlived `git worktree remove`. The index is
copied rather than rebuilt with `read-tree HEAD` because a fresh index carries
no skip-worktree bits and reads every sparse-checkout exclusion as a deletion.
Gitignored paths stay out — measured: the board did not enter the snapshot.

**The ledger is machine-local board state.** `<board>/.state/sessions.json`,
beside `serve.json`, written atomically through a temp file and a rename. It
records id, pid, start time, command, worktree, branch, repo, when it was
taken and the host. It is regenerable from `git worktree list` plus `ps`, and
it registers nothing about configuration — it is the same kind of file as the
daemon's own registration, which is why the standing `the watch set is the
whole configuration` invariant is untouched by it.

The session worktree is `<board>/.sessions/<id>` on `session/<id>`, with the
board excluded by the same `--no-cone` sparse-checkout `lanes.create` uses, so
a board command run from a session tree cannot resolve a phantom board. `take`
is idempotent on the path and on the ledger — measured: a second `take` printed
`holds`, and the ledger stayed at one row. The branch survives a reap, the way
`lanes.remove` keeps a swept lane's branch.

## Acceptance

- [x] `resources/board/session.py` exists and `python3 resources/pearde.py help` lists a `pearde session` line
- [x] `pearde session` with no verb refuses, exit 2, naming `take, list, reap, owns`
- [x] `take` creates `<board>/.sessions/<id>` on branch `session/<id>` and writes a row to `<board>/.state/sessions.json`
- [x] the session worktree does not contain the board directory
- [x] a second `take` from the same session reuses the worktree and adds no second ledger row
- [x] `owns` exits 0 for a path inside the running session's own tree and 1 for another session's tree or the main checkout
- [x] `reap` without `--apply` removes nothing and names what it would do
- [x] `reap --apply` leaves a live session's worktree in place and removes a dead session's
- [x] `reap --apply` never removes the running session's own worktree, whatever the ledger says
- [x] a session whose liveness is unknown — `ps` silent, or no recorded start time — is kept, not reaped
- [x] a ledger row whose pid is running under a start time other than the recorded one reads dead
- [x] the snapshot commit at `refs/pearde/reaped/<id>` holds the dead session's tracked edits, its renamed paths, its untracked files and its untracked nested directories
- [x] the content of a reaped edit is readable with `git show refs/pearde/reaped/<id>:<path>` after the worktree is gone
- [x] the gitignored board is not in the snapshot
- [x] the snapshot leaves the worktree byte-identical, and `session/<id>` survives the reap
- [x] the module is Python 3 stdlib only

## Verify and Proof

```sh
# the probe, against the tree the work is in
PEARDE_ROOT="$(pwd)" bash "$(git rev-parse --show-toplevel)/pearde/prds/every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe/verify.sh"
# 29 assertions, "PROBE GREEN", exit 0

# routing: capture, then read. `|| echo` cannot fail a block, and a bare
# `pearde.py help` decides the exit on a file outside this footprint.
help=$(python3 resources/pearde.py help 2>&1 || true)
[ -n "$help" ]
printf '%s\n' "$help" | grep -q 'pearde session'
# the refusal exits 2, so it must not be the last command of a bare list —
# `set -e` would take that exit as the block's.
python3 resources/pearde.py session && rc=0 || rc=$?
[ "$rc" = 2 ]
python3 -c "import ast,sys; ast.parse(open('resources/board/session.py').read())"
```
