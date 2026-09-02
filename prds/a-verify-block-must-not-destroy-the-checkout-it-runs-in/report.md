# a-verify-block-must-not-destroy-the-checkout-it-runs-in — implementer

Verdict: DONE

Both specs are built and green in the lane. `probe/verify.sh` prints
`24 passed, 0 failed`; `probe/probe_unit.py` prints `ALL PASS` over 13 cases
and `probe/probe_roots.py` over 6. 22 of 22 acceptance boxes ticked — 13 in
`spec01`, 9 in `spec02` — each against a run quoted below.

Lane: `lane/a-verify-block-must-not-destroy-the-checkout-it-runs-in`, one
file changed outside this PRD's own directory:
`resources/board/collect.py`.

## spec01 — 13/13, re-measured, not inherited

`spec01` arrived already built by the analyst's pass two. Every box was left
open on the reasoning that "the run that ticks a box is the run that
re-measures it", and this run re-measured all thirteen rather than
inheriting them. Nothing in `collect.py` needed changing for `spec01`.

```
$ python3 -c "import ast; ast.parse(open('resources/board/collect.py').read())"
collect.py parses
$ grep -n "code, output = guarded_run" resources/board/collect.py
1494:            code, output = guarded_run(["bash", "-e", "-o", "pipefail"],
$ grep -c "^def guarded_run\|^def owned_by\|^def _park\|^def _heal\|..." collect.py
7
$ test -z "$(grep -n '_foot_in' resources/board/collect.py)" && echo ...
no _foot_in left
```

## spec02 — 9/9, built this pass

`guarded_run` now snapshots before the block and puts back only what the
block made ABSENT. New in `resources/board/collect.py`:

- `_owned_files` — the files under each owned path that exist on disk; a
  footprint entry may be a directory, and only what is there is snapshotted.
- `_blobs` — `git ls-files -s` over the footprint pathspec, never over the
  expanded file list, so a directory footprint costs one call.
- `_snapshot` — `{path: (kind, payload, mode)}`. `kind` IS the size guard
  the spec asked for: a tracked, clean path is held as its index blob sha,
  so a footprint naming a large directory is not copied at all; only a path
  git does not hold the current bytes of — dirty, staged, or untracked — is
  read into memory. Measured directly: on a fixture with one clean tracked
  file, one dirty tracked file and one untracked file, `_snapshot` returns
  `blob`, `copy`, `copy` respectively.
- `_unerase` — writes back each absent path with its pre-block bytes and
  mode and names them on one line, the shape `_heal`'s line already takes:
  `verify deleted this PRD's own work in <cwd> — put back: <paths>`.

`guarded_run` takes the snapshot after `_park` and calls `_unerase` in its
`finally`, between `_heal` and the stash pop. Nothing else about the
footprint changes — modified stays modified, created stays created, and a
path the worker deleted before the block was never on disk to snapshot, so
is never resurrected.

## What the probes now cover

`probe/probe_unit.py` grew 7 cases (13 total). Two pass-one assertions had
to flip, and both flips are the behaviour this unit changes, not a
weakening: `foreign dirt survives a block that empties the checkout` used to
assert the footprint stayed deleted, and `probe_roots`' R2 and R3 asserted
the same for the footprint file and for the PRD's own directory under
`board_root`. Each now asserts the file comes back with the DIRTY text it
had, not with `HEAD`'s. The witness that keeps them able to fail is
`spec01_guard` — `spec01`'s `guarded_run` reassembled from `_park`,
`_head_of`, `run`, `_restore_head`, `_heal` and the pop, with no snapshot —
and it still loses the file.

`probe/verify.sh` grew section E (24 assertions total): `pearde collect`
driven end to end on a LANELESS board, where the PRD's uncommitted footprint
is the work under test and there is no lane to recover it from. E1 asserts
`collect` reaches `done`, names the path it put back, leaves `def helper` on
disk and COMMITS it rather than the deletion. E2 is the reproduction: the
same fixture on `spec01`'s `collect`, and there the work is gone from the
checkout and the deletion is what got committed.

`spec01`'s collect is built for E2 by taking the shipped `collect.py` and
removing the two lines `spec02` added, asserting first that they are there —
so the witness cannot silently stop witnessing. That reproduction could not
be spelled as a git ref: the unit under test is uncommitted like the rest.

## Two repairs to the harness, both inside this PRD's directory

Neither is in `spec02`'s "Left to finish"; both were found by running it.

**Section A was pinned at `HEAD`.** Its comment reasoned "the guard is
uncommitted, so HEAD is before". That stops being true at exactly the run
that matters: this harness IS the verify block of the PRD that builds the
guard, so `collect` runs it AFTER `land_lane` has merged the lane into the
checkout's branch. At that moment `HEAD` is "after", section A's
reproduction would have quietly stopped reproducing, A1 would have gone red,
and this PRD would have failed its own collection. `PINNED` now walks
`collect.py`'s own history for the last commit with no `def guarded_run` in
it — right on both sides of the landing. Rehearsed against a clone with the
guard committed as `land_lane` would leave it: `24 passed, 0 failed`, with
section A still reproducing at `e5abc5b`.

**Section C2 matched the board by name.** It re-derived the board through
`planlib.find_board`, which matches a directory against `BOARD_DIR`. This
repo's board is `pearde/`, reachable as `.pearde` only through a symlink, so
C2 passed or died depending on whether the path the harness was invoked by
went through that symlink — an invocation-path dependency, not a code
property. It now takes the board the harness's own walk already found. Both
invocations now give `24 passed, 0 failed`.

## The gate

`resources/index.py check` is red in the checkout on three rows, all of them
older than this claim and none in this footprint:
`references/skills/pearde-machine.md` has no row in `references/files.md`,
`references/language.md` references `@references/personas/writer.md` and
`resources/board/edit.py` references `@questions.py`, neither on disk.
`resources/memos.py check` is green. `resources/doctor.sh` exits 0 with the
`health` row broken on two files no longer tracked and a stale ranking —
again older than this claim. Reported, not fixed: they are outside this
PRD's scope and belong to whoever is holding those files.

Run inside the lane, `index.py check` also reports the
`references/skills/pearde-machine.md` and `@questions.py` rows — the lane is
cut from `e5abc5b`, before those landed, so this is the same pre-existing
red, not a regression the lane introduces.

## Health

The brief named no file in this footprint under the floor.
`resources/board/collect.py` gained 116 lines this pass and is a long file;
splitting it is a defect outside this scope and is reported here, not done.

## Notes

No word was needed that `grammar.py` does not define. No fact was learned
outside this repo, so nothing was written to `knowledge.py`.

One thing a later pass should know: the two specs' `## Verify and Proof`
blocks open with `cd /Users/feb/dev/infra/pearde` and then grep
`resources/board/collect.py` for `guarded_run`. That is the post-land
checkout and is correct for `collect`, but it is wrong for a worker holding
the lane — the guard is only in the lane until `land_lane` runs. Every
verify in this report was therefore run against the lane, with
`PEARDE_ROOT` pointing at it, which is what `verify.sh` already supports.
