---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 75        # higher first
complexity: 10      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.24h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
needs:
  - apply-the-prds-rename-table
commit: 0321d5d af86629
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

# resolve-bare-board-path-mentions — every remaining bare `prds/` mention (no table match) across the scoped files is read and rewritten to `.pearde/` or `.pearde/prds/` as its context actually means, verified against the code it describes where the meaning isn't obvious from the sentence alone

every remaining bare `prds/` mention (no table match) across the scoped files is read and rewritten to `.pearde/` or `.pearde/prds/` as its context actually means, verified against the code it describes where the meaning isn't obvious from the sentence alone

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
allowed  references/parts/guard.md:15  (WALKS ls-pattern)
allowed  references/parts/workers.md:87  (<prds/> placeholder)
allowed  references/parts/workers.md:334  (<prds/> placeholder)
allowed  resources/guard.py:72  (WALKS ls-pattern)
allowed  resources/guard.py:77  (WALKS regex literal)
bare tokens: 0 | documented exceptions: 5
board-dir ok  references/settings.md: 3 x 'relative to `.pearde/`.'
board-dir ok  references/parts/master.md: 1 x "against the master's `.pearde/`."
board-dir ok  references/parts/doctor.md: 1 x 'pointing outside `.pearde/` is'
board-dir ok  references/parts/doctor.md: 1 x 'returns under `.pearde/`, and nothing else'
forbidden tokens (.pearde/.pearde, prds/prds): 0
py_compile: ok
gate: index + memos green
verify: clean
