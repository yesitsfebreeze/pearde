---
complexity: 6
footprint:
  - references/parts/commits.md
---

# spec02 — the harness the board sweeps, and the sentence in the prose

The probe proves the line today and is thrown away with the worker. This unit
turns it into `probe/verify.sh` in the board's own harness shape, so the sweep
`doctor.sh --harnesses` runs re-checks it, and adds the one sentence to
`references/parts/commits.md` that says what the run now prints — that file
already documents the rebase and the merged-tree verify, and stops one clause
short of the names.

## What stands

`probe/run.sh`, `probe/fixture.sh` and `probe/driver.py` — a green probe with
a control, five assertions, and a wrapper that reads the text `post_report` is
handed without standing a daemon up.

## What is left

- `probe/verify.sh`, in the shape of
  `@.pearde/prds/collect-stages-a-shared-file-whole/probe/verify.sh`: `set -u`,
  a `PASS <name>` / `FAIL <name>: <why>` line per check, `PASS`/`FAIL` counters
  and a `BOARD`/`ROOT` walk up from `$0` honouring `PEARDE_ROOT`, so the sweep
  measures the tree the runner names and not the orchestrator's checkout. The
  five assertions in `run.sh` and its control are the checks; the harness pins
  no total.
- One sentence in `references/parts/commits.md`, in the "Where the commit is
  made: the lane" paragraph, after the merged-tree clause: collect prints the
  footprint files the branch changed since the lane was cut, read before the
  rebase because the rebase destroys the cut point, and the same sentence heads
  the PRD's `## Report` — the worker wrote its own report before any of this
  landed and cannot know it.

## Acceptance

- [x] `probe/verify.sh` exists, is executable, exits 0 on this tree, and prints
      a `PASS` line per check and no `FAIL`.
- [x] It walks up from `$0` to find `.pearde` and honours `PEARDE_ROOT`, so
      `PEARDE_ROOT=<a lane> probe/verify.sh` measures that lane.
- [x] It covers the control as well as the positive: a run where nothing moved
      under the lane and the line is absent.
- [x] `references/parts/commits.md` names the printed line and says the read
      happens before the rebase.
- [x] The gate is green: `resources/index.py check`, `resources/memos.py check`
      and `resources/doctor.sh` report nothing this PRD introduced.

## Verify and Proof

```sh
test -x .pearde/prds/no-work-is-lost-on-the-board/a-lane-rebases-before-collect/probe/verify.sh
bash .pearde/prds/no-work-is-lost-on-the-board/a-lane-rebases-before-collect/probe/verify.sh
! bash .pearde/prds/no-work-is-lost-on-the-board/a-lane-rebases-before-collect/probe/verify.sh 2>&1 | grep -q '^FAIL '
grep -q 'moved under the lane' references/parts/commits.md
python3 resources/index.py check
python3 resources/memos.py check
```
