---
state: failed
origin: derived
from: every-worker-runs-in-its-own-worktree  # derived only — the PRD whose work surfaced this one
priority: 75
complexity: 34
blast-radius: high
workflow: probe-then-spec
---


# a harness measures the tree its worker built in

The harness set was written when one orchestrator built in one checkout. It
now runs on a board where every worker builds in a lane of its own and
several run at once, and two of its assumptions are false because of that.
Both were measured by `every-worker-runs-in-its-own-worktree`'s implementer
and reported as outside its scope.

**A board harness can never read a lane.** Every `probe/verify.sh` computes
its root by walking up from its own path:

    ROOT="$(cd "$(dirname "$0")/../../../../.." && pwd)"

That path is the harness's location on the board, which is always the
orchestrator's checkout — never the lane the worker is building in. So a
worker's build is invisible to every board harness until `collect` merges it,
and a box ticked on a harness run reads a tree that holds none of the work
it claims to prove. The workaround that unit used — a scratch root whose
`.pearde` is a symlink to the live board, so the walk-up resolves to a merged
tree — is a measurement trick, and it is now a row in
`capture-the-harness-baseline`'s `## Fails when`. It is not a fix.

**`nothing-left-open`'s `E14` is decided by scheduling, not by the tree.** It
asserts that no `/tmp/pearde-index-*` exists — a machine-wide glob, not one
scoped to the fixture that made it. Any sibling harness running `collect` at
the same time reddens it. Measured: red in a four-way parallel sweep, green
serially, on the same tree.

## What exists when this is done

- A harness takes its root from the runner rather than from `$0`, so a worker
  running the set in its lane measures its lane. The existing walk-up stays
  as the fallback for a harness run by hand.
- `E14` is scoped to the fixture's own temporary directory, so a concurrent
  sibling cannot decide it.
- The set is run once serially and once in a parallel sweep, and the same
  harnesses pass both times.

## Why this is not deferred

`every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index` is the
requested PRD this gets wrong. Its implementer will run in a lane and fold
seventeen skill files into one index, then run `index.py check` and the
manifest harnesses to prove it. Every one of those reads the orchestrator's
checkout, where the fold has not happened — so the boxes go green on a tree
that has none of the work, and the unit lands unverified. Its sibling
`the-machine-is-the-run-verb` renames a module the same harnesses name by
path, with the same result.

`the-machine-frontier-is-dispatched-in-parallel` and
`every-worker-runs-in-its-own-worktree` both landed this week, so parallel
lane work is the board's normal mode from now on, not an edge case.

## Out of scope

- Rewriting any harness's assertions. Only where a harness reads from.
- `collect-keeps-its-word`, which rebuilds a pinned `collect` with `git show`
  and so cannot run in any copy of the tree lacking the history. That is a
  real constraint, not a defect, and it wants one line in its own header
  saying so.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 20:58 — claim impl-harness-root 2026-09-02 17:20, silent 8.9h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/a-harness-measures-the-tree-its-worker-built-in`, whose worktree this sweep removed — the branch is kept.

## Failure

swept 2026-09-04 02:41 — claim impl-nova2-a-harness-me 2026-09-03 21:40, silent 4.8h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/a-harness-measures-the-tree-its-worker-built-in`, whose worktree this sweep removed — the branch is kept.
