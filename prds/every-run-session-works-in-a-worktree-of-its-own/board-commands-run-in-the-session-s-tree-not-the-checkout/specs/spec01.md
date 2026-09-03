---
complexity: 12
footprint:
  - resources/board/session.py
  - resources/board/plan.py
---

# spec01 — the session's tree is what "the code repo" means, and `land` puts it where a person reads

`@resources/board/session.py` gives a session a worktree and a ledger row.
Nothing reads that row. This unit makes the row an answer: one resolver every
code-repo lookup on the board goes through, and one verb that puts the
session's branch on the branch a person opens the repo on.

**What already stands.** `take`, `list`, `reap` and `owns`, the ledger at
`<board>/.state/sessions.json`, `session_pid`'s walk up the process tree, and
`repo_of(board)` — which stays session-blind, because it is what `take` uses
to find the repo to cut the worktree FROM.

**What this unit adds to `session.py`.**

`my_id()` — `s<pid>` for the session this process runs inside, cached for the
life of the process. `session_pid` costs one `ps` fork per step of the walk,
and the resolver below is asked once per PRD by every scan, the daemon's
included, once a second per board. A process cannot change which session it is
inside, so the answer is computed once. `cached_ledger(board)` is
`read_ledger` behind an `(mtime_ns, size)` check, for the same reason: 140
PRDs must not mean 140 parses of one file.

`held(board, repo=None)` — the worktree THIS session holds, or None. **None is
the ordinary answer, not a failure.** A command outside a session, a session
that never took a tree, a worker inside its own lane, and a ledger row whose
tree is no longer on disk all answer None, and every one of them then resolves
exactly what it resolved before this unit existed. `repo`, when given, is the
checkout the caller resolved by walk-up, and a row for a different repo is not
this board's answer — that is what stops a master board handing one member's
PRD another member's session tree. `instead_of(board, repo)` is the call every
resolver makes: it returns `repo` when there is no session, never returns None
and never raises, so a resolver that was correct stays correct when the ledger
is empty, unreadable, or holds a tree somebody deleted.

Paths compare by `realpath`, not `abspath` — this board is reached as `pearde/`
and as the `.pearde` symlink beside it, and a tree named through one while the
board is named through the other compares unequal under `abspath`.

`land(board)` — rebase `session/<id>` onto the branch the checkout is on, then
`merge --ff-only` there. `lanes.merge` one level up and for the same reason: a
plain merge writes a second commit for one PRD and
@references/parts/commits.md allows one, and `--squash` leaves the branch
reading unmerged forever. The target is the checkout's own HEAD branch, read
from git — never `main` by name, so a repo whose trunk is `master` and a person
parked on a release branch are both served. The rebase runs in the worktree
that holds the branch, because git refuses to move a branch another worktree
has checked out. **`merge --ff-only` is the whole of what runs in the
checkout**: a checkout with uncommitted work fails the merge and keeps that
work, and none of the four commands the memo puts out of bounds is used.
Measured with two sessions landing in turn: the second rebased first, history
stayed linear, and neither took the other's commit away.

`plan.prd_repo` ends in `session_tree(board, root)`, a two-line function whose
import of `session` is inside it — `session` imports `plan`, so a module-level
import either way round is a cycle.

**Deliberately not routed**, and each for a reason a later reader will need:
`session.repo_of` (it finds the repo to cut the tree from); `machine.py`'s
footprint resolver (the daemon's watch set needs one stable absolute path per
footprint across every session, and it runs outside a session anyway);
`ramp.repo_of` (a marker survey whose answer is the same in either tree);
`plan.repo_root` itself (the primitive walk-up every other rule is built on).

## Acceptance

- [x] `session.held` returns None with no ledger, with no session process, and when the ledger's worktree path is not on disk
- [x] `session.held` returns None for a ledger row whose `repo` is not the repo the caller asked about
- [x] `session.instead_of` returns the repo it was handed, unchanged, in every case where `held` is None, and raises nothing when the ledger is malformed
- [x] `session.my_id` calls `session_pid` once however many times it is asked
- [x] `plan.prd_repo` returns the session's worktree when the running session holds one, and the checkout when it does not
- [x] a board reached through the `.pearde` symlink and a session tree named under `pearde/` still resolve to each other
- [x] `pearde session land` is listed by the verb's refusal line and by `pearde help`
- [x] `session land` with nothing to land exits 0 and says the reading branch already holds it
- [x] `session land` puts the session's commits on the branch the checkout is on, as a fast-forward, with no merge commit
- [x] `session land` targets the checkout's own HEAD branch, not the name `main`
- [x] a second session's `land`, run after the first has landed, rebases and fast-forwards without removing the first's commit
- [x] `session land` into a checkout holding uncommitted work fails, exits 1, and leaves that work byte-identical
- [x] `session land` refuses when the checkout is on the session's own branch, rather than merging a branch into itself
- [x] `session.repo_of` still answers the checkout while a session holds a tree — `take` must not cut a worktree from a worktree of itself
- [x] `plan.py` imports and runs with `session.py` absent from `sys.path`

## Verify and Proof

```sh
board=$(python3 -c "import sys; sys.path.insert(0, 'resources/board'); import plan; print(plan.find_board(None))")
probe="$board/prds/every-run-session-works-in-a-worktree-of-its-own/board-commands-run-in-the-session-s-tree-not-the-checkout/probe"
export PEARDE_RES="$(pwd)/resources"

# the resolver, and the two cases the end-to-end run does not cover
python3 "$probe/measure.py" "$(mktemp -d)"
python3 "$probe/cases.py" "$(mktemp -d)"

# the verb is routed and the refusal names it
python3 -c "import ast; ast.parse(open('resources/board/session.py').read())"
python3 resources/pearde.py session && rc=0 || rc=$?
[ "$rc" = 2 ]
verbs=$(python3 resources/pearde.py session 2>&1 || true)
printf '%s\n' "$verbs" | grep -q 'land'
```
