---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 30        # higher first
complexity: 0      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.76h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
commit: eca3408
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

# The round is handed its step, not the manual

Today a round worker loads the loop's prose on every window it opens:
`references/parts/loop.md` (11.7 KB), `references/parts/workers.md` (20.1 KB),
`references/parts/states.md`, `references/parts/round.md`,
`references/parts/guard.md` and `references/drill.md` — about 62 KB, roughly
15k tokens, on top of a session floor measured at 50,229 tokens on 2026-09-01
before the round had done anything. Context is billed on every turn a window
survives, so that prose is paid for again per turn, not once.

The board already decided the direction: `the-tool-moves-the-states` says the
sentences in `references/parts/` that state a gate are deleted as each command
lands, and the parts become the spec of the commands. This PRD is the next
stretch of that same program, aimed at the two largest remaining loads.

What exists when this is done: a round worker can learn which loop step it is
on and what it owes from one command, and can hand a worker's report to
`collect` without reading a verdict-to-command table. Both prose files shrink
to what a command cannot print — the judgment calls.

Non-goals. No change to what any state means and no new state. No rewrite of
the tool in another language: that was measured on 2026-09-01 and rejected.
`.pearde/.state/transitions.jsonl` records command-only transitions at ~120
tokens against 24,411 and 37,484 for the ones a worker reasons through, so the
implementation language is not on the token path; the speed half of that
question is filed separately as the scan cache.

Pointers: `resources/pearde.py` (the dispatcher, 63 commands),
`resources/board/transitions.py` (the gates and the progress line),
`resources/board/brief.py` (the just-in-time-prompt pattern to copy),
`resources/board/collect.py`, and memos `the-tool-moves-the-states`,
`the-scan-is-one-call`, `the-round-has-a-context-ceiling`.

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

container: every child done — pearde collect closes it

children: the-round-is-handed-its-step-not-the-manual/pearde-next-prints-the-step-and-the-decision-it-owes, the-round-is-handed-its-step-not-the-manual/collect-reads-the-worker-s-report-and-routes-its-own-verdict
