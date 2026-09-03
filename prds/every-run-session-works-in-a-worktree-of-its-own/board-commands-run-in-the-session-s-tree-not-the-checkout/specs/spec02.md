---
complexity: 12
footprint:
  - resources/board/collect.py
---

# spec02 — collect resolves, spells and lands in the session's tree

`collect.repo_of` is the one rule for "where does this PRD's code live", and
`claim`, `sweep`, `brief`, `snapshot` and `collect` itself all read it. This
unit makes it end at the session's own worktree, fixes the one place that then
answers wrongly, and puts the session's branch on the branch a person reads as
part of finishing.

**Three changes, and the middle one is the whole of the difficulty.**

**`repo_of` ends in `session.instead_of`.** Every answer it had was a checkout
resolved by walk-up, and the checkout is the one place the parent PRD says
nothing may run. The walk-up answer becomes the repo the session's tree was cut
FROM; the tree is what the command gets. Measured: `claim` then cuts the lane
off the session's branch — the lane held a file that existed only on that
branch — `snapshot` takes its baseline there, and `collect` merges the lane and
commits there.

**A footprint spelled against a tree the board hosts.** `foot_root` decides
whether a footprint belongs to the board's repo or the code repo by joining the
path onto the code repo and testing the absolute result for the board's
directory as a string prefix. That is sound only while the code repo sits ABOVE
the board. A session's worktree is `<board>/.sessions/<id>` — below it. Measured
the moment `repo_of` started answering with it: every footprint path landed
inside the board by prefix, `collect` printed `p1: in the board's own repo, not
the lane's — src/app.py` and then `outside the footprint, left in the lane`,
ran the verify against an unchanged tree, and committed nothing. No exception
and no wrong answer named — the footprint was simply routed away from the lane.

The fix is `spelling_root(board, board_root, repo)`: the containment test is
anchored to the checkout — `checkout_of(board, board_root)`, the walk-up with
the session step left off — whenever `repo` itself resolves inside the board,
and to `repo` otherwise. A worktree and the checkout it was cut from spell
every tracked path identically, which is what makes them one repo, so the
answer holds for both. `under()` compares by `realpath`: this board is reached
as `pearde/` and as the `.pearde` symlink beside it. Lanes live under the board
too and never tripped this, because `land_lane` passes the code repo as `repo`
and only the lane's own path is below the board.

**`land_session(board)` runs after the commit, and is advisory.** A commit on
`session/<id>` is a commit nobody reads, so landing it is part of finishing
rather than something to remember afterwards. It runs at step 7, after
`prd.md` says `done` and every commit is made, which is exactly why it may not
raise: an exception there would leave the board finished and the run reporting
a failure it did not have — the same rule `post_report` above it already
follows. A checkout holding uncommitted work refuses the fast-forward, and that
refusal is one phrase on the transition line: measured, `collect` still exited
0, the person's uncommitted file was byte-identical afterwards, and the PRD's
commit was standing on the session branch for `pearde session land` to retry.
The phrase on a success is `landed on <branch>`.

**What is already right and needs no change.** `orphans` reads the checkout's
own branch and asks whether it holds each footprint path. With a land that was
refused, a footprint genuinely has not reached the branch a person reads, and
`orphans` calling it an orphan is the correct report, not a bug to route
around.

## Acceptance

- [x] `collect.repo_of` returns the running session's worktree when the ledger holds one for the repo it resolved, and the checkout when it does not
- [x] `collect.repo_of` with a `repo:` key still resolves that repo, and reaches the session's tree of it by the same last step
- [x] `pearde claim` cuts the lane off the session's branch — a commit made only on that branch is present in the new lane
- [x] `collect.under` answers true for a session tree named through the `.pearde` symlink while the board is named as `pearde/`
- [x] `collect.checkout_of` returns the enclosing checkout for a board that is its own repo, and `board_root` for a board that is a plain directory in one
- [x] `spelling_root` returns the checkout when the code repo resolves inside the board, and `repo` unchanged otherwise
- [x] a footprint under the board still routes to the board's repo while a session holds a tree — the `pearde/.gitignore` case is not broken by the fix
- [x] a collect of a PRD whose footprint is ordinary code stages that code in the lane, not in the board repo, while a session holds a tree
- [x] a collect while a session holds a tree exits 0 and prints `landed on <branch>` on the transition line
- [x] after that collect the checkout's branch holds the PRD's commit and the working tree carries the change
- [x] two sessions collecting two PRDs in turn both reach the checkout's branch, with no merge commit between them
- [x] a collect whose land is refused by a dirty checkout still exits 0, says the land was refused, and leaves the checkout's uncommitted work byte-identical
- [x] `land_session` raises nothing when `session.py` cannot be imported, when the ledger is absent, and when git refuses
- [x] a collect with no session on the ledger commits on the checkout's branch exactly as it did before this unit

## Verify and Proof

```sh
board=$(python3 -c "import sys; sys.path.insert(0, 'resources/board'); import plan; print(plan.find_board(None))")
probe="$board/prds/every-run-session-works-in-a-worktree-of-its-own/board-commands-run-in-the-session-s-tree-not-the-checkout/probe"
export PEARDE_RES="$(pwd)/resources"

# claim → lane → worker → collect → land, and the land that must find nothing
python3 "$probe/endtoend.py" "$(mktemp -d)"
# no session at all, two sessions at once, and a dirty checkout
python3 "$probe/cases.py" "$(mktemp -d)"

python3 -c "import ast; ast.parse(open('resources/board/collect.py').read())"
```
