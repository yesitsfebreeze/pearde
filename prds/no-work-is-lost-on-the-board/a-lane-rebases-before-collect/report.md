# a-lane-rebases-before-collect — implementer report

Verdict: DONE

## Workflow probe-then-spec

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | read-the-contract | passed | `prd.md` + both specs read; `git status --short` in the lane is clean, `e0890c8` already carries both specs' code, rebased onto the checkout's `4a94475` (which itself carries the sibling `a-conflicted-lane-is-reported-not-stranded`); `git -C <checkout> merge-base --is-ancestor HEAD lane/<slug>` exits 0, confirming the earlier analyst pass's rebase/conflict-resolution stands |
| 2 | capture-the-harness-baseline | passed | second-pass shape: nothing to baseline pre-edit, this pass makes no new edit. Hit the documented fails-when row for a lane behind a `.pearde` symlink — a bare `bash .../probe/run.sh` / `probe/verify.sh` walks `pwd -P` back through the symlink to the live board and measures the checkout, not the lane |
| 3 | attempt-the-build | passed (nothing to build) | both specs' footprint files (`resources/board/lanes.py`, `resources/board/collect.py`, `references/parts/commits.md`) already carry the contracted code per `e0890c8`; second-pass rule applies, no new spec authored |
| 4 | re-run-the-harnesses | passed | re-run with `PEARDE_ROOT=<lane>` exported (see below) — spec01's `probe/run.sh`: 5/5 PASS, exit 0. spec02's `probe/verify.sh`: 7/7 PASS, exit 0 |
| 5 | write-the-specs | passed | applied both specs' `## Acceptance` tables to the standing code rather than authoring — every box re-verified true, see below |

### Edits

none — both fails-when rows the run hit (uncommitted-but-clean-tree on a lane; a lane behind a `pearde` symlink) are already in `workflows/capture-the-harness-baseline.md` and matched exactly.

## What this pass found

The contract stood from a prior analyst pass (report already at this path, `SPECCED`, dated 15:09): it rebased the lane onto `main` after `pearde unblock` on the recorded merge conflict, resolved the one real hunk in `collect_one` (combining the sibling's `except LaneConflict` with this PRD's 3-tuple unpack), and reverified. This implementer pass re-measured that claim independently rather than trusting it: `git -C <checkout> merge-base --is-ancestor HEAD lane/<slug>` (exit 0) proves the lane's `e0890c8` sits on the checkout's current `4a94475`, and both harnesses re-run green.

One real gotcha hit while re-verifying: running the probes bare (`bash .pearde/prds/.../probe/{run,verify}.sh`) from inside the lane resolves `.pearde` (a symlink to the live board) with `pwd -P`, so `BOARD`/`ROOT` land on the **checkout**, not the lane — and the checkout's `resources/board/lanes.py` has no `cut_base`/`moved_since_cut` yet (this PRD hasn't collected). That produced spurious `FAIL`s (`AttributeError: module 'lanes' has no attribute 'cut_base'` under the hood, surfacing as the daemon's generic "another shape" error and three missing assertions). Re-run with `PEARDE_ROOT=<the lane>` exported, both harnesses are fully green — this is the exact `capture-the-harness-baseline` fails-when row already on file, and no workflow edit was needed.

## Specs

- `specs/spec01.md` — 6/6 boxes, re-verified true against the file:
  - `bash probe/run.sh` (PEARDE_ROOT=lane): 5 `PASS`, exit 0.
  - `cut_base`/`moved_since_cut` defined in `resources/board/lanes.py` — static check passes.
  - `moved_since_cut` read before `laneslib.merge` in `land_lane`, and `post_report` guards `b.get("path")` — static checks pass.
- `specs/spec02.md` — 5/5 boxes, re-verified true against the file:
  - `probe/verify.sh` exists, executable, exits 0, 7 `PASS` / 0 `FAIL` (PEARDE_ROOT=lane).
  - Covers the control (scenario 2, no line when main stood still).
  - `references/parts/commits.md` names the printed line ("moved under the lane") and says the read happens before the rebase — `grep -q` confirms.
  - Gate: `python3 resources/index.py check` and `python3 resources/memos.py check` (PEARDE_ROOT=lane) — same pre-existing findings as the standing baseline (`resources/common.py` no row, `hotreload-test.js` named twice; ~20 memos missing `tags:`), nothing this PRD's footprint introduced. `bash resources/doctor.sh` (PEARDE_ROOT=lane): `index`/`memos`/`workflows`/`knowledge`/`questions` rows are the same pre-existing broken/ok states reported by the prior pass on both main and the lane.

Footprint (union): `resources/board/lanes.py`, `resources/board/collect.py`, `references/parts/commits.md`. `git status --short` in the lane after this pass: clean — no new edit, only re-verification.

## Findings, not fixed

- `doctor.sh --questions` flags this PRD's own `## Answers` with no `## Questions` above it — pre-existing, the PRD's `## Answers` text says so itself ("this is not question, wrong format"), not this PRD's contract to correct.
- `doctor.sh` rows `knowledge`, `questions` broken identically on `main` and the rebased lane; none of it names this footprint.

## Scores

complexity: 14
blast-radius: mid
workflow: probe-then-spec
