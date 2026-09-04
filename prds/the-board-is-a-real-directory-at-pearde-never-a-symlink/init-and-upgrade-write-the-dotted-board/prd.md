---
state: failed
origin: requested
priority: 95
complexity: 14
blast-radius: mid
workflow: probe-then-spec
---


# init-and-upgrade-write-the-dotted-board — pearde init` makes a real `.pearde/`, `pearde upgrade` moves a board still at `pearde/` into it and rewrites the ignore block whole instead of appending a second, and the guard on the rename is `is_board_dir`, never `isdir

pearde init` makes a real `.pearde/`, `pearde upgrade` moves a board still at `pearde/` into it and rewrites the ignore block whole instead of appending a second, and the guard on the rename is `is_board_dir`, never `isdir

## History

**failed, retried 2026-09-03 21:20**

released 2026-09-03 19:58 — claim impl-dotted-init 2026-09-03 12:03, held 7h52m
with 0 of 14 boxes ticked and no file of this PRD's moved since 12:03:52. The
worker is gone: no process on this machine predates 13:43, and the session
ledger carries no row for it.

`sweep` read this claim as `silent 36m`, not 7h52m, and the reading is a
measurement artefact, not a live worker: `silence.silent_of` takes the newest
mtime over the PRD's directory AND its footprint paths **in the checkout**,
and `resources/board/init.py` in the shared checkout was last written 18:51 by
another session working another PRD. A footprint two PRDs share therefore
reports the neighbour's work as this one's liveness.

Released with `release <prd> failed` rather than `sweep --apply`, deliberately.
This PRD's partial build — pass one's `resources/board/init.py` and
`.gitignore`, 221 insertions against 102 deletions — is UNCOMMITTED in
`.pearde/.lanes/the-board-is-a-real-directory-at-pearde-never-a-symlink-init-and-upgrade-write-the-dotted-board`;
`lane/…-init-and-upgrade-write-the-dotted-board` carries nothing ahead of
`main`. `sweep --apply` calls `drop_lane`, which removes that worktree and the
dirt in it, and would have printed "partial code stands on branch `lane/…`" —
true of a worker that committed, false here, and the build would have gone.
`release` leaves the worktree and everything uncommitted in it exactly where
the worker left them (`transitions.drop_lane`'s own docstring says so).

Before a retry: the work is in the lane worktree, not on the branch. `purge
--apply` treats a lane whose PRD holds no claim as a candidate, and this PRD
now holds none — commit the lane or read `report.md`, which measures the build,
before running one.

## Failure

swept 2026-09-04 02:41 — claim impl-dotted-init2 2026-09-03 21:21, silent 5.3h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/the-board-is-a-real-directory-at-pearde-never-a-symlink-init-and-upgrade-write-the-dotted-board`, whose worktree this sweep removed — the branch is kept.
