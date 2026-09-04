---
complexity: 10
footprint:
  - resources/invariants/one-dispatcher-per-physical-board.sh
  - references/parts/run.md
  - references/files.md
---

# spec03 — the lock is written down, and a tracked check fails when it goes

The probe that measured the lock lives under the board, which this repo
ignores, so nothing in the tracked tree fails when the lock regresses. This
unit gives the rule a section a reader finds and a script a run can fail on,
on the pattern the six existing invariants already follow.

**What already stands**: nothing. `references/parts/run.md` has no section on
the lock, and `resources/invariants/` holds six scripts, none of them this one.

**What is left**:

1. `resources/invariants/one-dispatcher-per-physical-board.sh` — builds a
   board under a run-time temp dir (never under a board directory: a directory
   holding a prd.md anywhere under the board IS a PRD), gives it one `open`
   PRD and a stand-in adapter binary that sleeps, points `PEARDE_ADAPTER_BIN`
   at it, starts one `pearde run`, and while that one is inside its poll loop
   starts a second on the same physical board. Exit 0 while the second refuses
   naming the first's pid; exit 1 the moment both dispatch. The tree to scan is
   `$1`, defaulting to the working directory — the shape
   `no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh` already
   uses. Prove the check can fail: run it once against a copy whose
   `lock_boards` is stubbed to return `([], [])` and assert it goes red.
2. `references/parts/run.md` — a `## One dispatcher per board` section under
   `## Dispatch`, saying: identity is the realpath and never the spelling; the
   lock is `flock` on `<board>/.state/run.lock` and never a pidfile, so nothing
   is stale and nothing is reaped; the pid in the file is a note for the
   refusal to quote; `--dry` takes the lock too, because `pearde plan` is the
   read that moves nothing; and one held board does not stop the others. Add a
   bullet to `## What it does not do` saying the lock file is per board and is
   not the persisted registry that section already refuses.
3. `references/files.md` — one row for the new script, in the
   `@resources/invariants/` block, saying what it asserts.

The memo `kind: invariant` that names this script in its `verify:` is the
board's own artefact and is written by `pearde memo add` when the PRD lands,
not by this spec: memos live under the board this repo ignores, and this
footprint is the tracked tree.

## Acceptance

- [ ] `bash resources/invariants/one-dispatcher-per-physical-board.sh` exits 0 against this tree and prints what it asserted
- [ ] The script builds every fixture under a directory it makes at run time and removes it, leaving no `prd.md` anywhere under a board
- [ ] The script is shown to fail: against a tree whose `lock_boards` returns no locks and no refusals it exits 1 and names the two dispatchers that both ran
- [ ] The script starts no worker that outlives it — the stand-in adapter sleeps and is reaped, and no real adapter binary is invoked
- [ ] `references/parts/run.md` carries a section on the lock naming `flock`, `<board>/.state/run.lock`, realpath identity, `--dry`, and one held board not stopping the rest
- [ ] `references/parts/run.md`'s `## What it does not do` says the per-board lock file is not a machine-wide registry
- [ ] `references/files.md` holds a row for the new script under the `@resources/invariants/` block
- [ ] `python3 resources/index.py check` reports no new line beyond the four it already prints

## Verify and Proof

```sh
cd "$PEARDE_LANE"
bash resources/invariants/one-dispatcher-per-physical-board.sh
python3 resources/index.py check 2>&1 | tee /dev/stderr | wc -l   # still 4
grep -n 'run.lock' references/parts/run.md
grep -n 'one-dispatcher-per-physical-board.sh' references/files.md
```
