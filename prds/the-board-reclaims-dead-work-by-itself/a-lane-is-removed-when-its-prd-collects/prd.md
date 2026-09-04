---
state: specced
origin: requested
priority: 80
complexity: 24
blast-radius: mid
workflow: probe-then-spec
---

# a lane is removed when its prd collects

Nothing removes a lane when its PRD collects, so the board leaks one git
worktree per completed PRD.

Measured 2026-09-03: `git worktree list` reports **54** worktrees on this repo
and `.pearde/.lanes/` holds **49** directories; 26 of those lanes belong to
PRDs whose state is already `done`.

`laneslib.git(repo, "worktree", "prune")` only drops registrations whose
directory has already vanished, so it never touches a lane that is merely
finished. `session.py`'s reap cleans **sessions**, not lanes. The sibling
`no-work-is-lost-on-the-board/a-conflicted-lane-is-reported-not-stranded`
covers what happens to a lane that *conflicts* — not to one that succeeded.

When this is done, a successful collect removes the lane it merged, the
registration goes with the directory, and a run of the board over many PRDs
does not grow the worktree list without bound. Removal happens only after the
merge is committed and only for a lane holding nothing uncommitted — this must
not become a second way to lose work.

Report how many of the 26 existing stale lanes the change would clean, and
whether cleaning the backlog is this PRD's job or a one-off command.

## Blocked

**2026-09-03 20:48 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/board/collect.py`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-03 21:00 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/board/collect.py`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-03 21:57 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 02:23 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 02:38 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 02:46 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 02:48 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `session/s62223`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 02:49 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `session/s85810`; 2 file(s) disagree:

- `resources/board/collect.py`
- `resources/board/lanes.py`

Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 04:03 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 04:06 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.

**2026-09-04 04:20 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-lane-is-removed-when-its-prd-collects` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`.
