---
state: specced
origin: requested
priority: 70
complexity: 14
blast-radius: mid
workflow: probe-then-spec
---

# a lane rebases before collect

Collect rebases the lane onto main before running verify, and the worker's report names every footprint file main changed since the lane was cut — so verify runs against the tree the merge will produce, and the report says what moved under the worker's feet.

## Done means

A lane cut before an unrelated main commit → verify runs on the rebased tree; a lane whose footprint file moved on main → the collect output lists that file.

## Needs

No gate. Pairs with `a-conflicted-lane-is-reported-not-stranded`: that row handles the rebase that fails, this one the rebase that succeeds.

## Blocked

**2026-09-03 14:06 — the lane will not rebase**

`lane/no-work-is-lost-on-the-board-a-lane-rebases-before-collect` does not land on `session/s98669`; 1 file(s) disagree:

- `resources/board/collect.py`

Nothing is lost: the worker's commits are on `lane/no-work-is-lost-on-the-board-a-lane-rebases-before-collect` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock no-work-is-lost-on-the-board/a-lane-rebases-before-collect`.

**2026-09-03 21:36 — the lane will not rebase**

`lane/no-work-is-lost-on-the-board-a-lane-rebases-before-collect` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/no-work-is-lost-on-the-board-a-lane-rebases-before-collect` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock no-work-is-lost-on-the-board/a-lane-rebases-before-collect`.
