---
complexity: 6
footprint:
  - resources/health.py
  - references/health.md
  - references/templates/health.md
---

# spec01 — every tracked file carries a score, and the worst are on one page

`resources/health.py` scores every tracked file 1-100 on six axes — lines,
branching, longest function, fan-out, fan-in and cross-community links —
writes one note per file under `.pearde/health/files/<slug>.md` with a closed
frontmatter set, and a `.pearde/health/ranking.md` ordered worst first. The
three graph axes are read from `.pearde/graphify/graph.json` through each
node's `source_file`, never by deriving an id; without a graph they read
`none` and the score comes from the other three on the same scale. The verbs
are `score`, `list`, `show`, `check`, `init`, stdlib only, forwarded as
`pearde health`.

## What already stands

All of it, committed. `resources/health.py` is 43 KB of stdlib-only Python
(`ast`, `datetime`, `json`, `math`, `os`, `re`, `subprocess`, `sys` and
nothing else — probe I3). Longest function is measured, not guessed: Python
through `ast`, other languages by keyword and nesting heuristic with the note
saying which was used and why (probe H1), markdown by section. The closed
frontmatter set is the fifteen keys the contract names — `health`, `file`,
`language`, `score`, `lines`, `branching`, `nesting`, `longest`, `fan_out`,
`fan_in`, `links`, `worst`, `date`, `commit`, `graph` — and `check` exits 1
naming any key outside it. `references/health.md` is the format doc,
`references/templates/health.md` the note template.

On this repo now: `151 scored · 151 on the ranking · 18 skipped · 5 under 40 ·
graph f986510`, and the worst five are `view.css 4`, `plan.py 19`,
`serve.py 28`, `collect.py 31`, `view.js 39` — the three files the PRD's
first box names are all under the floor.

## What is left

Nothing in the code. The implementer re-runs the probe and the two commands
below against fresh output and reports. A red here is a regression, not
spec-from-scratch work.

## Acceptance

- [x] `python3 resources/health.py score` writes one note per scored file and
  a ranking, and `view.js`, `plan.py` and `collect.py` are all under the
  floor on it.
  `152 scored · 152 on the ranking · 18 skipped · 5 under 40 · graph 954b906` ·
  (two numbers moved from the analyst pass, neither ours: graphify rebuilt
  `graph.json` at `built_at_commit 954b906`, and a live sibling landed
  `resources/board/lanes.py` at 14:45:40, taking the file total 151 → 152.
  `5 under 40` and every score is unchanged. The block asserts the summary's
  **shape** and the three named files, never a literal total that a live
  checkout moves) ·
  ranking rows `| **19** | resources/board/plan.py |`, `| **31** | resources/board/collect.py |`,
  `| **39** | resources/board/view.js |`
- [x] `health check` is silent and exits 0 on a fresh record, and exits 1
  naming the key when a note carries an undeclared one.
  `  ok    C1 check exits 0` · `  ok    C2 check prints nothing` ·
  `  ok    D1 a note with an undeclared key exits 1` · `  ok    D2 and names the key`
- [x] `health score` on a repo with no `graph.json` exits 0, the summary and
  every note say `graph: none`, and the three graph axes read `none`.
  `  ok    A1 score exits 0 without a graph` · `  ok    A2 the summary says graph none` ·
  `  ok    A3 deep.py's note says graph none` · `  ok    A4 deep.py's fan_in is none`
- [x] The graph axes are read through node `source_file`, and a note carries
  the graph's own commit.
  `  ok    E2 deep.py's fan_in is 1` · `  ok    E3 deep.py's Callers list tiny.py` ·
  `  ok    E4 the note carries the graph's commit` · `  ok    E5 tiny.py's fan_out is 1`
- [x] Every note's score is an integer 1-100, binaries and minified files get
  no note, and a subset score leaves the other notes untouched.
  `  ok    B1 every note's score is an integer 1-100` ·
  `  ok    A8 the binary and the minified file have no note` ·
  `  ok    F1 deep.py's note is untouched by a subset score` ·
  `  ok    F2 the ranking still lists every note`
- [x] `health.py` imports stdlib only and an unknown verb exits 2.
  `  ok    I3 health.py imports stdlib only` · `  ok    I1 an unknown verb exits 2`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
N=0
bash .pearde/prds/files-score-their-health-and-the-brief-names-the-unhealthy/probe/verify.sh 2>&1 | tail -1 | grep -E '^[0-9]+ checks . [0-9]+ pass . 0 fail$' || N=$((N+1))
python3 resources/health.py score | tail -1 | grep -E '^[0-9]+ scored . [0-9]+ on the ranking . [0-9]+ skipped . [0-9]+ under 40 . graph ' || N=$((N+1))
python3 resources/health.py list --under 40 | grep -E 'resources/board/plan\.py' || N=$((N+1))
python3 resources/health.py list --under 40 | grep -E 'resources/board/collect\.py' || N=$((N+1))
python3 resources/health.py list --under 40 | grep -E 'resources/board/view\.js' || N=$((N+1))
python3 resources/health.py check || N=$((N+1))
echo "spec01 failures: $N"
[ "$N" = 0 ]
```
