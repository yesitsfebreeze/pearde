---
health: file           # `file` on a note, `ranking` on the ranking
file: <repo-relative path>   # the truth; the filename is only a slug
language: <python|javascript|typescript|shell|markdown|css|…>
score: <1-100>         # 100 healthy. 100 · (1 − Σ weight·badness / Σ weight) over the measured axes
lines: <n>             # physical lines. 0 at 150, 1 at 1500, log; documents 300 → 3000
branching: <n|none>    # branch points in the busiest function; `<module>` counts. 0 at 10, 1 at 50, log
nesting: <n|none>      # deepest nesting there. 0 at 4, 1 at 10; blended 60/40 into `branching`
longest: <n|none>      # lines of the longest function. 0 at 40, 1 at 400, log; documents: longest section, 80 → 800
fan_out: <n|none>      # distinct files this one calls, imports or references. 0 at 3, 1 at 20
fan_in: <n|none>       # distinct files calling, importing or referencing this one. 0 at 2, 1 at 25, log
links: <0.00-1.00|none>  # share of the graph's code files this one wires to. 0 at 0.10, 1 at 0.50
worst: <axis> <axis>   # the two that pulled hardest, weighted. Empty when none did
date: <YYYY-MM-DD>     # the day of scoring
commit: <short hash|none>   # the repo's HEAD at scoring time
graph: <short hash|none>    # the graph's `built_at_commit`; `none` = the three graph axes unmeasured
---
<!-- The keys are a CLOSED set, in this order, written by @resources/health.py
     and never by hand — `pearde health score` rewrites every note whole.
     Written is the raw measure, never the badness; the comment thresholds
     are constants in health.py, the weights and floor `health-weights:` and
     `health-floor:` in settings.md. @references/health.md is the format. -->

# <file> — <score>

<the two worst axes in one sentence — `branching 31 in `cmd_init` (10 is the
line, nesting 6) and 905 lines pull it down.` — or `nothing pulls it down.`>
measured by <ast | heuristic (ast: SyntaxError line 12) | sections | lines>

<!-- Without a graph the two sections below are absent, one line in their
     place: `no graph — scored on lines, branching, longest`. -->

## Callers
- <repo-relative path, sorted, at most thirty, then `- … and N more`>

## Calls
- <repo-relative path>
