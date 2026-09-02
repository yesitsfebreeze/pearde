# Health

Which files resist being worked on, kept where the brief looks.

A PRD says what to build, a spec how, a workflow the route. None says the file
the route runs through is 2,900 lines with a 68-branch function in the middle.
A **health record** does — one score per tracked file, worst first — so a
monolith is named before a worker meets it, rather than found by the fourth
worker to lose an afternoon in it. @references/health.md is the format, the
axes, the check.

```
.pearde/health/ranking.md
.pearde/health/files/<slug>.md
```

- No `state`. Never claimed, specced or dispatched — invisible to `scan` and to
  the progress line, yet on the board.
- Regenerable. `pearde health score` rebuilds the whole record from the tree and
  the graph; the board's `.gitignore` carries `health/`, written on a fresh
  board by @resources/board/init.py.
- One reader, @resources/health.py. Six axes, two knobs (`health-floor`,
  `health-weights` — @references/settings.md), and a floor under which a file is
  **unhealthy**.

## When it is scored

| moment | what happens |
|---|---|
| a board is set up, or the graph was rebuilt | `pearde health score` — once, whole. Tens of seconds on a large tree, one on this one |
| a PRD landed | `pearde health score <its footprint>` — the notes for those paths, and the ranking rebuilt from every note on disk |
| `doctor` runs | `health check` — the record's shape, and `stale` when the ranking is twenty commits behind or the graph is newer. Rescores nothing |

No pass rescores the record. A score a week old is still the right pointer, and
the `stale` line says when the pointer stops being one.

## Handed to a worker

The implementer's brief carries one paragraph, filled by `pearde brief` from
`health list --under <floor>` over the PRD's footprint:

```
 22  resources/board/plan.py  branching, lines
 39  resources/board/view.js  lines, branching
```

or `none under the floor`, or `no health record — pearde health score writes
one`. What the worker owes is bounded and plain:

- **Leave each named file better than you found it, inside the spec's
  scope.** The function the spec touches gets shorter, the branch the spec
  adds does not deepen the nesting, a thing the spec makes you read twice
  gets a name. Not a refactor of the file — the spec is the scope, and a
  footprint is not a licence.
- **Say in the report what moved.** One line per named file: what changed
  and why the file is better, or why nothing could move inside the scope. A file
  named in the brief and absent from the report was not looked at.
- **A split is a PRD, never a side effect.** A file needing to be broken
  apart goes in the report as a defect outside scope, per
  @references/parts/derived.md — the orchestrator files it, or does not.

## What it is not

- **A gate.** No transition reads a score. `collect` does not refuse a PRD
  whose files got worse; the brief says what to leave better and the report
  says what moved, the whole contract this round.
- **A verdict.** 22 says look here and says why; it does not say split. A
  generated file, a table of constants, a test fixture can sit at 5 and be
  exactly right.
- **A measure of the work.** `complexity` on a PRD is the weight the board
  schedules by, hand-written by the analyst — @references/parts/contract.md.
  A file's health is not in that number and does not change it.

## Next, and not this round

Named here so the next PRD starts from the boundary and not from the idea:

- a derived PRD per file under the floor — `pearde add --parent`, one split
  each, `deferred` until a requested PRD names it
- a guard `note()` on an Edit of an unhealthy file — advisory, never a deny
- rescoring the footprint at `collect` step 7, and the delta on the progress
  line
- an mtime cache under `.pearde/health/` for a tree where a whole score is
  minutes

```sh
python3 @resources/health.py score [path...] [board]   # the record, whole or for these paths
python3 @resources/health.py list  [--under <n>] [path...] [board]   # worst first, off the ranking
python3 @resources/health.py show  <path> [board]      # one note
python3 @resources/health.py check [board]             # what doctor reports for `health`
python3 @resources/health.py init  [board]             # the directory and the ignore row
```
