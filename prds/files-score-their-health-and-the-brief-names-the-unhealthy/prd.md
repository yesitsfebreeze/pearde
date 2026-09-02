---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 60        # higher first
complexity: 14      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.63h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: probe-then-spec
---
<!-- Ordering reads three axes and no clock: dependency (needs + footprint),
     vision importance (priority), and complexity/blast-radius. Add your own
     keys freely, at any nesting. Nothing outside state, origin, from,
     priority, complexity, blast-radius, claim, repo, workflow, needs and
     footprint is read, and nothing you add is ever dropped.
       needs:     — PRD dir names this one depends on. A hard gate in `plan`
       footprint: — paths this PRD touches. The overlap check
       workflow:  — the route a worker is handed, expanded into its brief

     One sitting is the limit: specs summing `complexity` above `split-above`
     or counting above `specs-above` (both in .pearde/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# Files score their health and the brief names the unhealthy

Every tracked file in the repo carries a health score, 1 to 100, and the
worst ones are on one page. When an implementer is briefed, the brief names
the files in its footprint that sit under the floor, so a bad file gets
better whenever a PRD touches it — a monolith is named, not discovered.

**What exists when this is done**

- `resources/health.py` — `score`, `list`, `show`, `check`, `init`. Stdlib
  only, the only reader of the health format. Forwarded as `pearde health`.
- `.pearde/health/files/<slug>.md`, one note per scored file with a closed
  frontmatter set (`health`, `file`, `language`, `score`, `lines`,
  `branching`, `nesting`, `longest`, `fan_out`, `fan_in`, `links`, `worst`,
  `date`, `commit`, `graph`), and `.pearde/health/ranking.md` worst first.
  Both regenerable, both gitignored on the board.
- Six axes: lines, branching, longest function (measured — Python through
  `ast`, other languages by keyword and nesting heuristics, markdown by
  section), fan-out, fan-in and cross-community links (read from
  `.pearde/graphify/graph.json` through node `source_file`, never id
  derivation). Without a graph the three graph axes read `none` and the score
  is drawn from the other three on the same scale.
- Two flat knobs in `settings.md`: `health-floor` (default 40) and
  `health-weights` (`lines=20 branching=25 longest=20 fan_out=10 fan_in=10
  links=15`).
- The implementer brief block carries a `<health>` placeholder that
  `brief.py` fills from `health list --under <floor>` over the footprint —
  or one line saying there is no record, or nothing under the floor.
- The part is registered everywhere a part is: `FORWARD`, the skill file,
  the part doc, the format doc, the template, `files.md`, `index.md`,
  `SKILL.md`, `settings.md`, a `doctor` row, `handles.md`, `doctor.md`, the
  grammar template's **part** row plus collision rows for `floor` and
  `health`, and the board's own `.gitignore` through `init.py`.

**Non-goals, this round**

No derived "split this monolith" PRDs, no guard note on editing an unhealthy
file, no rescore at collect, no mtime cache. Named in
`references/parts/health.md` as the next steps.

**Pointers**

`resources/grammar.py` is the model for the script; the `grammar` block in
`resources/doctor.sh` for the row; `references/skills/pearde-grammar.md` for
the skill file. `resources/board/brief.py` `brief_prd` builds the placeholder
dict; `planlib.spec_data(prd)` returns the footprint union. The graph shape is
in `references/graph.md`. `complexity` is the PRD weight and stays untouched.

## Acceptance

- [x] `python3 resources/health.py score` on this repo writes one note per scored file and a ranking, and the bottom of the ranking holds `view.js`, `plan.py`, `collect.py`
- [x] `health check` is silent on a fresh record and names a note with an undeclared key, exit 1
- [x] `health score` on a repo with no `graph.json` exits 0 and writes `graph: none`
- [x] `pearde brief` on a specced PRD whose footprint holds a file under the floor names that file; with no record it says so
- [x] `resources/index.py check`, `memos.py check`, `grammar.py check`, `brief.py --check` and `doctor.sh` are green
- [x] the probe harness is pinned and green

<!-- Three more headings exist, and none of them is a slot to copy down. Each
     is a claim about the state of this PRD, so an empty copy of it is a false
     one: an empty `## Questions` stops the board on nothing, an empty
     `## Answers` reads as answered, an empty `## Failure` reads as a failed
     attempt. Write the heading when it has content; until then it is absent,
     which is the honest state. @resources/questions.py reports the empty
     ones, and `doctor`'s `questions` row runs it. -->

<!-- `## Questions` — analyst-only, when blocked on the user: one pass in the
     format of drill.md — `### Q1: <title>`, the fork in two sentences ending
     in "?", then exactly three prepared answers, each a complete decision,
     the best one first and marked `(recommended)`. Only real forks the user
     must settle (naming, scope,
     cost) — never facts a worker could look up, never the PRD restated. A PRD
     parked on the user with no such pass never says what it is asking.
     Written in plain words for the person who asked, never for the board — no
     backtick, no path, no PRD name, no board word, 60 words in the fork and 25
     in an answer: the table in @references/drill.md is the whole rule, and
     @resources/questions.py refuses a pass that breaks it. -->

<!-- `## Answers` — orchestrator-only (or the view), written after asking the
     user: `**Q1** — <the picked answer verbatim, or the user's own words>`,
     numbers matching the pass above it. Analysts read these before speccing.
     An `## Answers` with no `## Questions` above it answers nothing. -->

<!-- `## Failure` — implementer-only, after a FAILED attempt: what broke, what
     was tried. `retry` moves this into the body as history and reopens the
     PRD. -->

## Report

spec01: exit 0
37 checks · 37 pass · 0 fail
153 scored · 153 on the ranking · 18 skipped · 5 under 40 · graph 954b906
 19  resources/board/plan.py  branching, lines
 31  resources/board/collect.py  branching, lines
 39  resources/board/view.js  lines, branching
spec01 failures: 0

spec02: exit 0
  briefs      ok      5 blocks in references/parts/workers.md · every placeholder named · the verdict line named
spec02 failures: 0

spec03: exit 0
index.py check exit=1
resources/board/lanes.py is on disk with no row in references/files.md
  health      ok      153 files · 5 under 40
  grammar     ok      179 terms · the vocabulary checks out
spec03 failures: 0
