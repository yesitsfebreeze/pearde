# Health

A PRD says what to build, a memo says what was decided, a grammar says what
the words mean. A **health record** says how much each file resists being
worked on — one number per file, 1 to 100, 100 healthy, worst first on one
page — so a monolith is named before a worker meets it.

```
.pearde/health/
  ranking.md            every scored file, worst first
  files/<slug>.md       one note per file
```

- No `state`. Never claimed, specced, or dispatched — invisible to `scan` and
  to the progress line, yet on the board, where the brief looks.
- **Regenerable, never in the history.** `pearde health score` rebuilds the
  whole record from the tree; the board's `.gitignore` carries `health/`.
- One reader: @resources/health.py. The format has one home.
- A score is a **pointer, never a verdict**. It says where to look, and what
  pulls the file down; whether the file should change is the PRD's call.

## The axes

| axis | measures | no problem at | the whole problem at | weight |
|---|---|---|---|---|
| `lines` | physical lines. Documents: 300 → 3000 | 150 | 1500 | 25 |
| `branching` | branch points in the one function that has most (`if`, loops, `try` and each handler, `with`, boolean operators, comprehension filters, `match` cases) blended 60/40 with the deepest nesting. Module-level code is a function called `<module>`, so a flat script is not exempt | 10, nesting 4 | 50, nesting 10 | 30 |
| `longest` | lines of the longest function. No functions: the file is one. Documents: the longest `##` section, 80 → 800 | 40 | 400 | 20 |
| `fan_out` | distinct other files this one calls, imports or references, per the graph | 3 | 20 | 5 |
| `fan_in` | distinct other files that call, import or reference this one | 2 | 25 | 10 |
| `links` | the share of the graph's code files this one is wired to, either direction | 0.10 | 0.50 | 10 |

Each axis reads 0 under its first threshold, 1 over its second, log or linear
between. The score is `100 · (1 − Σ weight · badness / Σ weight)` over the
axes the file **measured**, clamped to 1-100. An axis a file did not measure
— the three graph axes without a graph, `branching` on CSS or markdown — is
left out of both sums, so a graph-less tree scores on the same scale and the
note says which axes it stood on. `worst` names the two axes that pulled
hardest, weighted.

Thresholds are constants: a threshold moved per board makes two boards' 40s
two different numbers. Weights and the floor are knobs:

```yaml
health-floor: 40
health-weights: lines=25 branching=30 longest=20 fan_out=5 fan_in=10 links=10
```

`health-floor` is the score under which a file is **unhealthy** — the one
the brief names. A weight or floor that cannot be read is one problem line
and the default stands.

## How a file is measured

| language | `lines`, `longest`, `branching` by |
|---|---|
| Python | `ast`. A file the parser refuses falls back to the heuristic and the note says `measured by heuristic (ast: SyntaxError line 12)` |
| JavaScript, TypeScript, Go, Rust, Java, Kotlin, Swift, C, C++, PHP, Perl, shell, Ruby, Lua | branch keywords counted per function, functions found by their opening line, nesting by brace depth or indentation. Close enough to say which function is long; never exact |
| Markdown, HTML | sections. `branching` is `none` |
| CSS | lines only |

Skipped, and counted under `skipped:` on the ranking: anything under
`node_modules`, `vendor`, `third_party`, `dist`, `build`; lockfiles; data
and assets (`.json`, `.yml`, `.toml`, `.txt`, images, fonts); `.min.js`;
binaries; files over 2 MB; `.pearde/` itself; a file with no language.

## The graph

`.pearde/graphify/graph.json`, when @references/graph.md has written one.
Files are found through each node's `source_file`, never by deriving an id
from a path. Edges counted: `calls`, `imports`, `references`, `method`,
`indirect_call`, `inherits`, `extends`. A graph that names fewer than half
the scored files was built from another root and is read as none — the
summary line says `graph none (graph paths match 12 of 61 files)`.

Communities are not read. graphify clusters close to one community per
file, so "edges that leave the community" would be every edge.

## The note

```
---
health: file
file: resources/board/init.py
language: python
score: 58
lines: 905
branching: 31
nesting: 6
longest: 128
fan_out: 6
fan_in: 4
links: 0.15
worst: branching lines
date: 2026-09-02
commit: 9df1035
graph: 9df1035
---
# resources/board/init.py — 58

branching 31 in `cmd_init` (10 is the line, nesting 6) and 905 lines pull it down.
measured by ast

## Callers
- resources/pearde.py

## Calls
- resources/board/edit.py
```

| key | is |
|---|---|
| `health` | `file` on a note, `ranking` on the ranking |
| `file` | the repo-relative path. The truth; the filename is only its slug |
| `language` | what it was measured as |
| `score` | 1-100 |
| `lines` `branching` `nesting` `longest` `fan_out` `fan_in` `links` | the raw measures, never the badness. `none` where the axis was not measured |
| `worst` | the two axes that pulled hardest, weighted. Empty when nothing did |
| `date` | the day it was scored |
| `commit` | HEAD of the repo when it was scored, or `none` outside git |
| `graph` | the graph's `built_at_commit`, or `none` |

The set is **closed**, like a memo's — a misspelled key reads as present.
Callers and Calls list files, sorted, capped at thirty. Without a graph the
sections are absent and one line says `no graph — scored on lines,
branching, longest`.

The filename is `files/<slug>.md`, the slug the path with every run of
characters outside `[\w.-]` turned into `-`: `resources/board/init.py` is
`resources-board-init.py.md`.

## The ranking

```
---
health: ranking
date: 2026-09-02
commit: 9df1035
graph: 9df1035
files: 61
skipped: 86
floor: 40
unhealthy: 3
---
# Health — worst first

| score | file | language | lines | branching | longest | fan_in | fan_out | links | why |
|---|---|---|---|---|---|---|---|---|---|
| **31** | resources/board/view.js | javascript | 4724 | 222 | 212 | 0 | 0 | 0.0 | lines, branching |
| 58 | resources/board/init.py | python | 905 | 31 | 128 | 4 | 6 | 0.15 | branching, lines |
```

Ascending, path as the tie-break, a score under the floor in bold.
`skipped:` is there so a person can see that 86 of 147 files were not
scored, rather than wonder.

## The check

`python3 @resources/health.py check` — the `doctor` row `health`. Silent
and exit 0 when `.pearde/health/` is absent or the record is clean. One
line per problem, exit 1, when:

- a note's fence is missing or unterminated, a key is outside the closed
  set, or a required key is missing
- `score` is not an integer 1-100, `lines` or `longest` not an integer,
  `date` not ISO 8601
- a note's `file:` is no longer tracked, or is now skipped
- the slug of `file:` is not the note's filename, or two notes name one file
- `ranking.md` is missing while `files/` holds notes, its `files:` differs
  from the note count, or a row names a file with no note
- `health-floor` or `health-weights` cannot be read

Printed, but exit 0 — a note, not a defect, each ending in the command that
clears it: `stale: ranking is 34 commits behind HEAD` (over twenty), and
`stale: graph 9df1035 is newer than the ranking's 5f3270a`.

`check` rescores nothing, so it costs what every other doctor row costs.

## Handed to a worker

@references/parts/workers.md's implementer block carries `<health>`, which
`pearde brief` fills with `health list --under <floor>` over the PRD's
footprint — one line per unhealthy file, its score and its `worst`, or one
line saying there is no record, or nothing under the floor. What the worker
owes is in @references/parts/health.md.
