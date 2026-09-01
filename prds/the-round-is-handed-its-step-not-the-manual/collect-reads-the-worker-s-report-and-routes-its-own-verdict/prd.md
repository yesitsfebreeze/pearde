---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 20        # higher first
complexity: 25      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.17h
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

# `collect` reads the worker's report and routes its own verdict

Loop step 6 maps a worker's returned verdict onto a transition — SPECCED to
`pearde specced`, REFINE to `pearde refine`, DONE to `pearde collect`, BLOCKED
to `pearde release <prd> blocked`, anything less to `pearde release <prd>
failed`. That table lives in `references/parts/workers.md`, 20.1 KB and the
largest single file a round loads, read so that the model can perform a lookup.

What exists when this is done: `collect` can be handed the report itself — a
flag naming the file, the exact spelling settled at spec time — and it reads
the verdict, performs the matching transition, and refuses a report whose
verdict is missing or unrecognised rather than guessing at it. The
orchestrator's remaining decision is the half that is genuinely judgment:
whether to believe the report at all, and whether a `## Workflow` edit was the
atomic's fault or the code's. That half stays prose. `workers.md` loses the
table and keeps the judgment.

Constraints. Every gate each transition already checks still runs — routing
must not become a way around them, and a red verify is still exit 1 with
nothing written. The `## Workflow` rows stay the orchestrator's to apply or
refuse; this PRD does not automate that. One writer stays one writer: two
reports naming one atomic in one round is still two collects. `pearde collect`
keeps working exactly as it does today when no report is named.

Pointers: `resources/board/collect.py`, `resources/board/transitions.py`,
`references/parts/workers.md`, `references/parts/loop.md` step 6, memo
`the-tool-moves-the-states`.

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

## Report

spec01: exit 0
PROSE-OK

spec02: exit 0
ROUTE-OK
warn: spec01.md:15: the verify block names no path under the footprint — the whole-workspace smell
warn: spec01.md:15: the verify block names no path under the footprint — the whole-workspace smell
collect: redder: spec01 exit 1 — nothing written
collect: nov: /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/pearde-probe-zmpx_60_/r-nov.md names no `Verdict:` — nothing written
collect: unk: /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/pearde-probe-zmpx_60_/r-unk.md verdict `MAYBE` is not one of SPECCED, REFINE, QUESTION, DONE, BLOCKED, FAILED — nothing written
warn: spec01.md:15: the verify block names no path under the footprint — the whole-workspace smell
pearde specced: refused — /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/pearde-probe-zmpx_60_/k/.pearde/prds/badspec/specs/spec01.md:1: no `## Acceptance` section
