---
complexity: 5
footprint:
  - resources/workflows.py
---

# spec01 — the workflow check counts report sections against `runs:`

`workflows.check()` gains one more comparison, asymmetric per the PRD's
answered Q1: a workflow whose `## Workflow <slug>` report sections in
`<board>/prds/**/report.md` outnumber its own `runs:` is a problem naming
both numbers; `runs:` at or above the count is never flagged, so the
steady-state gap left by a `report.md` a later pass overwrites (33 sections
on `probe-then-spec`, `runs: 61`, on the live board) does not trip it. A
`## Workflow` heading naming no bare slug is a second, separate problem,
the file and line named the way a dangling slug is named — this is not
speculative: probed against the live board it caught two real instances
(`prds/one-board-path-resolver-fewer/report.md:76` and
`prds/the-tree-holds-only-what-a-board-uses/legacy-migrations-retire/report.md:128`,
both a bare `## Workflow` heading with no slug).

Already stands (built during the probe pass, uncommitted in the tree):
`report_workflow_counts(board)` walks `<board>/prds/**/report.md` (skipping
the workflows library directory the same way `_refs_one` does), returns
`({slug: count}, {(path, lineno): line})`; `check()` calls it once, compares
per workflow inside the existing per-slug loop right after the existing
`runs:` integer validation, and appends the malformed-heading problems once
after the steps loop. Nothing is left to finish — this spec is verification
that what was built stands.

## Acceptance

- [x] A workflow with four `## Workflow <slug>` report sections on disk and
      `runs: 3` is a `check()` problem naming both `4` and `3`.
- [x] The same fixture with `runs: 4` (or higher) produces no problem for
      that slug.
- [x] A `## Workflow` report-section heading with no slug after it is a
      `check()` problem naming the file and line, not silently dropped.
- [x] `resources/doctor.sh`'s `workflows` row goes `broken` on the above
      with no edit to `doctor.sh` — it already prints every line `check()`
      returns.

## Verify and Proof

```sh
python3 .pearde/prds/runs-meets-the-report-count/probe/probe_report_count.py
```

The probe builds its own fixture and asserts every box above against it; the
live board is never a gate — on a live multi-session board `check()` finds
real problems written by other sessions' workers between two runs, and a
verify block cannot assert a board-wide invariant on evidence that moves
under it.
