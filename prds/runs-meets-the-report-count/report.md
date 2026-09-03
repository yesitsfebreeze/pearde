Verdict: DONE

# runs meets the report count — implementer

Both specs stood on the probe pass's uncommitted code in the lane
(`lane/runs-meets-the-report-count`). This pass ran every check, closed all
six boxes against output, and made one accuracy edit inside spec01's
footprint. 6/6 boxes ticked, 0 blocked.

## spec01 — the workflow check counts report sections against `runs:`

All four boxes `[x]`.

`python3 .pearde/prds/runs-meets-the-report-count/probe/probe_report_count.py`:

```
OK — 2 problem(s):
  broken-flow.md: 4 report sections in prds/*/report.md, runs: 3 — the counter is behind the evidence
  prds/p2/report.md:1: `## Workflow` — a report section heading names no slug
```

That one run closes boxes 1–3: the `runs: 3` fixture names both `4` and `3`;
the `ok-flow` fixture (same four sections, `runs: 4`) produces no line at all;
the slugless heading is named by file and line.

Box 4 — `doctor.sh` unedited (`git status --short resources/doctor.sh` in the
lane is empty). The same fixture board written to disk and `doctor.sh` run
against it:

```
  workflows   broken  2 workflows · 1 atomic · 2 problems
                      broken-flow.md: 4 report sections in prds/*/report.md, runs: 3 — the counter is behind the evidence
                      prds/p2/report.md:1: `## Workflow` — a report section heading names no slug
```

The row goes `broken` and prints both lines with no edit to `doctor.sh` — the
comparison landed in the one shared function every caller routes through.

### One edit this pass

`report_workflow_counts`'s docstring declared its second return as
`[(path, lineno)]`; it returns `{(path, lineno): line}`, which is what spec01
specifies and what `check()` iterates. Corrected the docstring line. No
behaviour change; the probe re-ran green after it.

## spec02 — the failure documented in `references/workflow.md`

Both boxes `[x]`.

```
$ grep -n "outnumber its own \`runs:\`" references/workflow.md
152:  outnumber its own `runs:` — never the other way: a report is overwritten
$ grep -n "report-section heading naming no slug" references/workflow.md
155:- a `## Workflow` report-section heading naming no slug
```

Two bullets, one per failure, in the same shape as the rest of `## The check`.
The first states the asymmetry in its own clause ("never the other way"), so
the list cannot be read as an equality check.

## The repo's own gate

`bash resources/doctor.sh` from the lane root. The `workflows` row is now
`broken` on the live board, and every line is a real case:

```
  workflows   broken  7 workflows · 23 atomics · 4 problems
                      implementer-continue.md: 1 report section in prds/*/report.md, runs: 0 — the counter is behind the evidence
                      probe-then-spec.md: 77 report sections in prds/*/report.md, runs: 66 — the counter is behind the evidence
                      prds/one-board-path-resolver-fewer/report.md:76: `## Workflow` — a report section heading names no slug
                      prds/the-tree-holds-only-what-a-board-uses/legacy-migrations-retire/report.md:128: `## Workflow` — a report section heading names no slug
```

`grammar`, `health`, `knowledge`, `briefs`, `view`, `plan` all `ok`. The
`memos` and `questions` rows are `broken` on missing `tags:` and on `##
Answers` without `## Questions` in three other PRDs — both pre-existing, both
outside this footprint, neither touched by this change.

The 77-vs-66 line is not a double count: 77 distinct `report.md` files each
carry exactly one `## Workflow probe-then-spec` heading
(`grep -rc … | awk -F: '$2>1'` returns nothing). The counter really is eleven
behind its evidence, which is the fault the PRD opens with, now visible.

## Findings — outside this PRD's footprint, reported not fixed

- `implementer-continue.md` carries `runs: 0` with one live report section on
  disk. A real instance of a run that wrote its report and never bumped the
  counter. One edit fixes it; it is another file's contract, not mine.
- `prds/one-board-path-resolver-fewer/report.md:76` and
  `prds/the-tree-holds-only-what-a-board-uses/legacy-migrations-retire/report.md:128`
  each write a bare `## Workflow` heading with no slug. Editing another PRD's
  report prose is outside this footprint.
- `probe-then-spec.md`: `runs: 66` against 77 sections. Whether the counter is
  backfilled to 77 or the gap is accepted is the library owner's call — the
  PRD rules out auto-repair by design.

## Health floor

The brief listed nothing under the floor in this footprint. `resources/
workflows.py` and `references/workflow.md` both stayed above it; the docstring
correction above is the only thing that moved.

## Scores

complexity: 5
blast-radius: low
workflow: implementer-continue
