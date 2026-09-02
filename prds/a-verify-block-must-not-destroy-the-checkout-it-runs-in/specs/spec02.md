---
complexity: 10
footprint:
  - resources/board/collect.py
---

# spec02 — a block cannot delete the work it was written to measure

`spec01` leaves the PRD's own footprint outside the fence on purpose: on the
laneless path that footprint is the uncommitted change verify exists to
measure, and parking it would make every verify read a clean HEAD. The cost
is measured, not assumed — `probe/probe_unit.py` case
"foreign dirt survives a block that empties the checkout" asserts that a
green block emptying the working tree takes the footprint file with it and
nothing puts it back. `collect` then commits the deletion and writes `done`.
On a lane run the merged work is recoverable from HEAD; on the laneless path
— every claim taken before lanes, and every board outside a git repo — it is
gone.

This unit closes that without re-parking anything. Before the block,
`guarded_run` snapshots the bytes and mode of every owned path in `cwd` that
exists on disk. After the block, an owned path that existed before and is
absent now is written back from the snapshot and named on `collect`'s own
output line. Nothing else about the footprint changes: a path the block
modifies stays modified, because a formatter or a build step editing the
file under test is legitimate and indistinguishable from the change itself;
a path the block creates stays created; and a path the worker had already
deleted before the block — a spec whose finish is a deletion, which
`sort_paths` explicitly supports — is never snapshotted and so is never
resurrected.

## Standing after pass three

Built and green. `probe/verify.sh` prints `24 passed, 0 failed`.

- `_owned_files`, `_blobs`, `_snapshot` and `_unerase` in
  `resources/board/collect.py`; `guarded_run` snapshots after `_park` and
  calls `_unerase` in its `finally`, between `_heal` and the stash pop.
- The size guard is the snapshot's `kind`. A path that is tracked and clean
  is held as its index blob sha — a footprint naming a large directory costs
  no copy at all. Only a path git does not hold the current bytes of —
  dirty, staged, or untracked — is read into memory. Both branches are
  measured, in one case, in `probe/probe_unit.py`.
- `probe/probe_unit.py`, 13 cases (6 from `spec01`, 7 here).
- `probe/probe_roots.py`, 6 cases — two of them flipped from `spec01`'s
  "the guard leaves it taken" to "the snapshot puts it back", which is the
  behaviour this unit changes.
- `probe/verify.sh`, 24 assertions — `spec01`'s 14 plus a section E driving
  `pearde collect` end to end on a laneless board, and the same fixture on
  `spec01`'s `collect` beside it.

Two repairs to the harness, both inside this PRD's own directory:

- Section A was pinned at `HEAD` on the reasoning that "the guard is
  uncommitted". It is not, by the time it matters: this harness IS the
  verify block of the PRD that builds the guard, so `collect` runs it after
  `land_lane` has merged the guard into the checkout's branch, and the
  reproduction would have quietly stopped reproducing at exactly the run
  that collects it. `PINNED` now walks `collect.py`'s own history for the
  last commit with no `def guarded_run` in it, which is right on both sides
  of the landing. Rehearsed against a checkout with the guard committed:
  still `24 passed, 0 failed`.
- Section C2 re-derived the board through `find_board`, which matches by
  NAME — so the same directory was or was not a board depending on whether
  the path the harness was invoked by went through the `.pearde` symlink.
  It now takes the board the harness's own walk already found.

## Acceptance

- [x] a green block that deletes an owned footprint file has it put back
      with its pre-block bytes and its pre-block mode
- [x] the same block run through `spec01`'s `guarded_run` without the
      snapshot loses the file — the witness that makes the box above able to
      fail
- [x] a footprint path the block MODIFIES is left modified, byte for byte as
      the block left it
- [x] a footprint path the block CREATES is left in place
- [x] a footprint path deleted before the block ran stays deleted — the
      guard does not resurrect a deletion that is the spec's own finish
- [x] a footprint entry that is a directory is snapshotted by the files
      under it, and a file the block deletes from inside it is put back
- [x] `collect` names every restored path on its own output line, the way
      `_heal` names what it put back
- [x] `pearde collect` end to end on a LANELESS board: a green destructive
      verify block, and the PRD's uncommitted footprint change is what gets
      committed — not the deletion
- [x] the same laneless fixture on `spec01`'s `collect` commits the deletion
      — the reproduction that makes the box above able to fail

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
python3 -c "import ast; ast.parse(open('resources/board/collect.py', encoding='utf-8').read())" && echo "collect.py parses"
bash .pearde/prds/a-verify-block-must-not-destroy-the-checkout-it-runs-in/probe/verify.sh
python3 .pearde/prds/a-verify-block-must-not-destroy-the-checkout-it-runs-in/probe/probe_unit.py
```
