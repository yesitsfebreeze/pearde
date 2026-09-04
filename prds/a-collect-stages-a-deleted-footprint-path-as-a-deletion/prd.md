---
state: failed
origin: derived
from: every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index
priority: 85
complexity: 6
blast-radius: high
repo: pearde
footprint:
  - resources/board/collect.py
workflow: probe-then-spec
---

# a-collect-stages-a-deleted-footprint-path-as-a-deletion

When this is done, a PRD whose own contract **deletes** a footprint file
collects cleanly: the lane's staging call stages the deletion instead of
refusing the whole call, and every collect gated behind one of those PRDs
moves.

## The measured defect

`land_lane` stages the lane's standing work before merging it
(`resources/board/collect.py:2103` in the session tree of 2026-09-03 20:56):

```python
laneslib.git(lane, "add", "--", *feet)
```

`feet` is the PRD's footprint union. A PRD whose contract deletes a file —
`every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index`
deletes `resources/install.sh`;
`the-tree-holds-only-what-a-board-uses/the-template-twins-fold-into-the-reference`
deletes `references/templates/prd.doc.md` — holds that path in `feet`, and
the lane **does not have the file**: the lane IS the work that deleted it.
`git add -- <a path that does not exist and is not tracked>` is
`fatal: pathspec '<path>' did not match any files`, and the `LaneError`
turns into a whole-commit abort — `nothing written; the lane still holds the
work`. The two PRDs above have finished implementer reports (DONE, boxes
full) and cannot close for this one line.

The sibling fix (`a-collect-does-not-stage-a-tracked-but-ignored-probe-file`,
`9c2b644`/`0d74c21`) put `-f` on the **checkout-side** staging call at
`collect.py:2377` — the same shape, one call earlier in the flow. The
**lane-side** call at `:2103` was not covered: `-f` changes ignore
handling, not a missing pathspec. A deletion has to be staged as a
deletion.

## The fix, as diagnosed

`git add -A -- <paths>` stages a deletion for a path that no longer stands,
and stages modifications for the ones that do — the same set as `--` plus
the gone side. One word on the call at `collect.py:2103`:

```python
laneslib.git(lane, "add", "-A", "--", *feet)
```

## Constraints

- **Do not widen what the lane stages.** `-A` with an explicit pathspec
  stages exactly the named paths — modifications, additions and deletions —
  never unlisted dirt. The set is still `feet`.
- The checkout-side call at `:2377` keeps its `-f` and its behaviour; this
  is a second call, not a rewrite of the first.
- A footprint path deleted in the lane AND still present on the merged tree
  (the sibling PRD's case) must keep collecting exactly as it does today.

## Acceptance

- [x] a fixture PRD whose lane deletes a footprint file collects to `done`, and the collect's commit carries the deletion — `probe/verify.py`: `gone shape: 0 ['state: done'] carries: D resources/install.sh | M resources/keep.txt`
- [x] a fixture PRD whose lane modifies a footprint file still collects, unchanged — `probe/reproduce.py`: `delete=False: landed … M resources/install.sh`
- [ ] the two held PRDs named above collect after the fix lands, with nothing re-implemented

## Pointers

- `resources/board/collect.py:2103` — the lane-side staging call
- `resources/board/collect.py:2377` — the checkout-side call, already `-f`
- `a-collect-does-not-stage-a-tracked-but-ignored-probe-file` — the sibling
  defect and its probe shape; build this one's probe the same way

## Failure

swept 2026-09-04 02:41 — claim impl-deleted-footprint 2026-09-03 21:14, silent 4.9h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/a-collect-stages-a-deleted-footprint-path-as-a-deletion`, whose worktree this sweep removed — the branch is kept.
