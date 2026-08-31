---
state: open        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 75        # higher first
complexity: 0      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual:          # a record. Nothing reads it
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
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
     or counting above `specs-above` (both in prds/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# every document names the path the board is on

Every document in the tree names the board's paths as they now are. A reader
following a path out of the docs lands on a file that exists.

The board moved from `prds/` at the repo root to `.pearde/`, and things moved
within it: what was `prds/knowledge/` is `.pearde/wiki/`, the five state
dotfiles are `.pearde/.state/<name>` with their leading dots dropped, and
`memos/`, `workflows/`, `settings.md`, `vision.md` — which used to sit inside
`prds/` alongside the PRDs — are now siblings of `.pearde/prds/`.

The Python under `resources/board/` has already been moved to the new layout
and is not in scope. What is left is prose and the strings inside it:
`skills/*.md`, `references/**`, `README.md`, `index.md`, `resources/*.sh`,
`resources/*.py` docstrings and help text, and
`resources/board/{brief,collect,specs,view.js}`.

Measure before editing — the count at the start of the move was 329
occurrences of `prds/` across 39 files, and the Python share of that is
already gone:

    grep -rn "prds/" skills resources references *.md | wc -l

Apply one mapping, as a script, not file by file. The specific rules must run
before the generic one or the generic rule eats the rest:

    prds/knowledge/         -> .pearde/wiki/
    prds/.plan.json         -> .pearde/.state/plan.json
    prds/.round.md          -> .pearde/.state/round.md
    prds/.history.jsonl     -> .pearde/.state/history.jsonl
    prds/.transitions.jsonl -> .pearde/.state/transitions.jsonl
    prds/.view.html         -> .pearde/.state/view.html
    prds/memos/             -> .pearde/memos/
    prds/workflows/         -> .pearde/workflows/
    prds/settings.md        -> .pearde/settings.md
    prds/vision.md          -> .pearde/vision.md
    prds/<name>/            -> .pearde/prds/<name>/

A bare `prds/` with nothing after it is not covered by that table and must not
be substituted mechanically: in some sentences it means the board root, which
is now `.pearde/`, and in others it means the PRD folder, which is now
`.pearde/prds/`. Each one is read and decided. Count them first — expect a few
dozen. This is a different job from running the table, and the two are
naturally two children; splitting them is the expected shape if the specs run
long.

Two directories moved at the same time and belong in the same sweep, because
they break the manifest the same way:

    agents/  -> references/agents/
    skills/  -> references/skills/

Both are already moved on disk. What is stale is what names them:
`references/files.md` heads a section `## `agents/` — dispatch` with
`@agents/pearde-analyst.md` and `@agents/pearde-implementer.md` under it,
`index.md`'s `@@workers` row names both the same way, and
`references/parts/workers.md` says `agents/` in prose. Nothing registers
`references/skills/` at all. `pearde index` must be silent when this is done.
`resources/install.sh` has already been repointed for both moves and is not in
scope.

Done when the grep above returns only occurrences that are deliberately about
the old layout (a migration note, this PRD's own history), and every path a
document names resolves on disk.

Not in scope: changing behaviour anywhere. This is a rename in prose. No
Python under `resources/board/` is edited except its own docstrings and help
strings.

Pointers: `resources/board/plan.py` for the authoritative constants
(`BOARD_DIR`, `STATE_DIR`, `PRDS_DIR`), `references/parts/board.md`.

<!-- Three more headings exist, and none of them is a slot to copy down. Each
     is a claim about the state of this PRD, so an empty copy of it is a false
     one: an empty `## Questions` stops the board on nothing, an empty
     `## Answers` reads as answered, an empty `## Failure` reads as a failed
     attempt. Write the heading when it has content; until then it is absent,
     which is the honest state. @resources/questions.py reports the empty
     ones, and `doctor`'s `questions` row runs it. -->

<!-- `## Questions` — analyst-only, when blocked on the user: one round in the
     format of drill.md — `### Q1: <title>`, the fork in two sentences ending
     in "?", then exactly three prepared answers, each a complete decision,
     one `(recommended)`. Only real forks the user must settle (naming, scope,
     cost) — never facts a worker could look up, never the PRD restated. A PRD
     parked on the user with no such round never says what it is asking.
     Written in plain words for the person who asked, never for the board — no
     backtick, no path, no PRD name, no board word, 60 words in the fork and 25
     in an answer: the table in @references/drill.md is the whole rule, and
     @resources/questions.py refuses a round that breaks it. -->

<!-- `## Answers` — orchestrator-only (or the view), written after asking the
     user: `**Q1** — <the picked answer verbatim, or the user's own words>`,
     numbers matching the round above it. Analysts read these before speccing.
     An `## Answers` with no `## Questions` above it answers nothing. -->

<!-- `## Failure` — implementer-only, after a FAILED attempt: what broke, what
     was tried. `retry` moves this into the body as history and reopens the
     PRD. -->

| `apply-the-prds-rename-table` | the specific-rule table (plus `.claims/`, `report.md`, `view.user.css/js`, `prds/knowledge` and the `prds/<name>/` pattern) is applied mechanically across the 80 scoped files, and `agents/`→`references/agents/`, `references/skills/` registration is fixed in `references/files.md`, `index.md`, `references/parts/workers.md | — |
| `resolve-bare-board-path-mentions` | every remaining bare `prds/` mention (no table match) across the scoped files is read and rewritten to `.pearde/` or `.pearde/prds/` as its context actually means, verified against the code it describes where the meaning isn't obvious from the sentence alone | apply-the-prds-rename-table |
