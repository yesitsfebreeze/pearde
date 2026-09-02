---
state: done
origin: derived
from: every-task-is-a-verb-under-one-skill/the-machine-is-the-run-verb
priority: 95
complexity: 11
blast-radius: high
workflow: probe-then-spec
actual: 0.37h
---

# collect must not reset the checkout it did not write

`collect`'s rollback runs `git reset --hard` in the orchestrator's own
checkout. Every uncommitted change in that checkout is destroyed — the PRD's
own work, and every other session's work standing beside it.

Measured at 2026-09-02 17:08 on this board. It destroyed the whole
implementation of `every-task-is-a-verb-under-one-skill/the-machine-is-the-run-verb`
— sixteen files of an `machine` → `run` rename, verified green by hand ten
minutes earlier, never committed. Reproduced from the reflog:
`HEAD@{0}: reset: moving to 35878179b1a7`, printed as
`lane unmerged — checkout back at 35878179b1a7`.

## The mechanism

`resources/board/collect.py`:

```python
def unland(repo, pre, out=print):
    """Put the checkout back where `land_lane` found it. Called when step 2
    goes red: a verify that fails must not leave the lane's code standing
    in the checkout..."""
    if not pre:
        return
    laneslib.git(repo, "reset", "--hard", pre, check=False)
```

Two things are wrong with it.

1. **`reset --hard` is not the inverse of a fast-forward merge.** `land_lane`
   moved the branch pointer; the inverse is moving the pointer back —
   `git reset --keep` or `git merge --ff-only` in reverse. `--hard` also
   throws away the working tree and the index, which the merge never touched.
   The docstring says "must not leave the lane's code standing in the
   checkout"; nothing in it asks for the checkout's own dirt.
2. **It runs even when nothing was merged.** In this failure `land_lane`
   returned `n = 0` — it printed `merged nothing` — but still returned `pre`,
   so `unland` reset for a merge that did not happen. There was no lane code
   standing in the checkout to remove.

The combination means: **a red verify block deletes the work the verify block
was checking.** That is the opposite of what a gate is for, and the loss is
silent — the line printed is `lane unmerged — checkout back at <sha>`, which
reads like bookkeeping.

## What exists when this is done

- `unland` moves the branch pointer and nothing else. `git reset --keep` is
  the least it can be; refusing outright when the checkout is dirty outside
  the lane's own paths is better.
- `unland` is not called at all when `land_lane` merged nothing.
- Before any destructive git in the orchestrator's checkout, `collect` says
  what it is about to discard and refuses when it is not its own — the same
  rule `collect --widen` already follows for a dirty path a claim predates.
- A harness case: a checkout dirty outside the footprint, a spec whose verify
  block exits non-zero, and the dirt still present afterwards.

## Why this is not deferred

`every-task-is-a-verb-under-one-skill/the-machine-is-the-run-verb` is the
requested PRD this got wrong — it destroyed its implementation outright, and
its two dependants `the-skills-fold-into-one-index` and
`every-task-is-a-verb-under-one-skill` are gated behind it. It will do the
same to the next PRD whose verify block goes red, and several sessions share
this checkout, so the work it takes need not even be the collecting PRD's.

## Out of scope

- The lane mechanism itself (`every-worker-runs-in-its-own-worktree` landed at
  16:46 and is sound — a worker's lane was never touched here).
- Whether `collect` should run verify in the lane rather than in the
  checkout. That is `a-harness-measures-the-tree-its-worker-built-in`.

## Report

spec01: exit 0
A. reproduced at 3587817: a red verify block deletes the checkout's own work
  ok   A1 the old collect exits 1 on the red
  ok   A1 ...and says the checkout went back
  ok   A1 the neighbour's uncommitted work is GONE
  ok   A1 ...and nothing said what was being discarded
A. reproduced at 3587817: it resets even when the merge merged nothing
  ok   A2 the old collect exits 1
  ok   A2 ...and still says the checkout went back
  ok   A2 nothing had been merged
  ok   A2 the neighbour's work is GONE for a merge that never happened
B. a red verify block leaves the checkout's own work standing
  ok   B1 exit 1 on the red — the gate still refuses
  ok   B1 the neighbour's uncommitted work is still there
  ok   B1 the checkout is back on the commit before the merge
  ok   B1 the lane's code does not stand in the checkout
  ok   B1 the line names what it discarded
  ok   B1 the lane branch still holds the worker's commit
  ok   B1 the PRD is still claimed
B. nothing merged: nothing is rolled back
  ok   B2 exit 1 on the red
  ok   B2 no rollback line — there was no merge to undo
  ok   B2 the checkout never moved
  ok   B2 the neighbour's work is untouched
B. a green verify block is unaffected
  ok   B3 exit 0
  ok   B3 done
  ok   B3 the worker's code landed
  ok   B3 the neighbour's work is still uncommitted, and still there
C. a rollback that cannot keep the work refuses, and says so
  ok   C1 exit 1
  ok   C1 the verify block's half-written output survives
  ok   C1 collect named the refusal
  ok   C1 ...and gave the command that finishes it
  ok   C1 the neighbour's work survives too
  ok   C1 the lane branch still holds the worker's commit
  ok   C1 the PRD is still claimed
Z. hygiene
  ok   Z no fixture committed a lane worktree dir

31 checks · 31 pass · 0 fail
spec01: 0 problem(s)

spec02: exit 0
31:moves the checkout's **branch pointer** back to the commit it was on —
spec02: 0 problem(s)
