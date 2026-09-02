---
name: pearde-health
description: Which files resist being worked on — every tracked file scored 1-100 from its lines, branching, longest function and what the knowledge graph knows of its callers, worst first on one page, and the implementer's brief naming the ones in its footprint under the floor. Score the tree, read the ranking, look one file up, check the record. Use for "/health", "score the files", "which files are the worst", "which file is a monolith", "how healthy is this file", "what pulls this file down", "rank the files", "what should we split", "rescore", "check the health record". A score is a pointer, never a verdict.
---

Read @references/parts/health.md for when the tree is scored and what a
worker owes a file the brief names, @references/health.md for the format —
the six axes and their thresholds, the two knobs, the closed frontmatter set,
the check. @references/templates/health.md is the note, with the rules in its
comments. The scope is `@@health`.

```sh
python3 @resources/pearde.py health score [path...] [board]   # the record, whole or for these paths
python3 @resources/pearde.py health list [--under <n>] [path...] [board]   # worst first, off the ranking
python3 @resources/pearde.py health show <path> [board]       # one file's note
python3 @resources/pearde.py health check [board]             # what doctor reports for `health`
```

`health` forwards to @resources/health.py, the only reader of that format.
`score` writes `.pearde/health/files/<slug>.md` per file and
`.pearde/health/ranking.md` worst first, both regenerable and ignored on the
board. `list` reads the ranking and rescores nothing; `pearde brief` calls
it over a PRD's footprint to fill `<health>` in the implementer's block.

Six axes: lines, branching, longest function, fan-out, fan-in, links. The
first three are measured — Python through `ast`, other languages by keyword
and nesting heuristics, markdown by section. The last three are read from
`.pearde/graphify/graph.json` when @references/graph.md has written one, and
are `none` when it has not; the score is drawn from what was measured, on
the same scale either way. Under `health-floor` (default 40) a file is
unhealthy.

A score says where to look and what pulls the file down. It does not say
split: a generated file or a table of constants can sit at 5 and be exactly
what it should be. Whether the file changes is the PRD's call; what a worker
owes a named file is bounded to the spec's scope, per the part doc.

The record lives at `.pearde/health/`, so a board is needed to write one.
With none in scope, say where it would be; scoring is an orchestrator write,
and it does not happen uninvited.
