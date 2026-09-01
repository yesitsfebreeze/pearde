---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 30        # higher first
complexity: 32      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.59h
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
     or counting above `specs-above` (both in .pearde/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# `pearde next` prints the step and the decision it owes

`references/parts/loop.md` is eight steps, each described as "one command and
one decision". A round reads all 11.7 KB of it to work out which step it is on
— every window, and again after every compaction.

What exists when this is done: `pearde next` returns in one call the loop step
the board is on, the decision that step asks the orchestrator to make, and the
exact command to run. Everything it needs is already computed by `scan` — the
drill count, the collect band, the ready queue in dispatch order, what a worker
holds — plus the `## Owed` line of `.pearde/.state/round.md`. A round that runs
`scan` then `next` needs no `loop.md` in its window for the routine case.

`pearde brief` is the pattern to copy: it already prints a worker's whole
prompt just-in-time rather than making the worker read the reference tree.
`next` is that, for the orchestrator.

Constraints. `next` reads and never writes — no state moves, no round file
written, so it is safe to run at any point. It must be right on a board with
nothing dispatchable (loop steps 7 and 8, where the answer is a drill or a
hand-back) and on a master board, where the ready queue spans members. The
prose in `loop.md` that `next` makes redundant is deleted in this same PRD,
per this board's deliverable rule: the file keeps only the right-hand column,
the judgment a command cannot make.

Pointers: `resources/board/plan.py` (`compute_plan`, `cmd_scan`),
`resources/board/brief.py`, `references/parts/loop.md`,
`references/parts/order.md`, `references/parts/round.md`.

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
owed: **collected 10:40 — collect-verdict SPECCED** → `specced --blast mid
step 6 · collect — 1 finished, waiting to be closed
  decision: whether to believe the report; whether an edit was the atomic's
  pearde collect the-round-is-handed-its-step-not-the-manual/pearde-next-prints-the-step-and-the-decision-it-owes
  pearde next                  the loop step the round is on — its decision…

spec02: exit 0
1
