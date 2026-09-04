---
state: specced
origin: requested
priority: 0
complexity: 14
blast-radius: mid
workflow: probe-then-spec
---

# a lane goes when its prd fails, not only when it collects

<The request, for an analyst who knows the codebase but not this conversation:
what exists at the end and why, what must not change, pointers to files and
prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

Purpose: `release <prd> failed` leaves the lane standing — worktree and
`lane/` branch — by design (`drop_lane`'s docstring: only `sweep` drops).
That covers the retry case and leaks every other: a PRD failed because it
was superseded is never retried, and its worktree then refuses the branch
deletion until someone removes the worktree by hand. Measured 2026-09-04 on
the dotfiles board: `09-simplify/08-litellm-out` released `failed`
(superseded by the user's reversal), lane left; and this repo carries 60
lane worktrees, most for `done` PRDs. The sibling
`the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`
is blocked on a `collect.py` rebase conflict since 2026-09-03 21:00, and
`the-lifecycle-contract-and-purge-reclaims-it` (`pearde purge`) is claimed
but not landed — `pearde purge` is `unknown command` on main today.

## Requirements

- [x] **R1** — `release <prd> failed` drops the lane the way `sweep` does:
      checkpoint commit if dirty, worktree removed; and, unlike sweep, the
      `lane/` branch goes too when the PRD's `## Failure` says it is not to
      be retried. A plain `failed` keeps the branch, as sweep does.
- [x] **R2** — `drop_lane`'s docstring names `failed` as the second edge and
      says why the branch rule differs.
- [x] **R3** — The two sibling nodes named above land first or fold into
      this one; the board holds one answer to "when does a lane go".

## Acceptance

- [x] On a probe board: claim → release failed with a `## Failure` saying
      not to be retried → `git worktree list` shows no lane and `git branch`
      no `lane/<slug>`.
- [x] Same without the marker → worktree gone, branch kept.

## Blocked

**2026-09-04 03:54 — the lane will not rebase**

`lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock a-lane-goes-when-its-prd-fails-not-only-when-it-collects`.

**2026-09-04 03:54 — the lane will not rebase**

`lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock a-lane-goes-when-its-prd-fails-not-only-when-it-collects`.

**2026-09-04 03:55 — the lane will not rebase**

`lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock a-lane-goes-when-its-prd-fails-not-only-when-it-collects`.

**2026-09-04 04:18 — the lane will not rebase**

`lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock a-lane-goes-when-its-prd-fails-not-only-when-it-collects`.
