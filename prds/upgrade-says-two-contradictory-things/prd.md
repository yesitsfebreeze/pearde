---
state: deferred        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: derived    # requested = the user asked | derived = the board found it
from: upgrade-leaves-the-memo-index-stale  # derived only — the PRD whose work surfaced this one
priority: 10        # higher first
complexity: 0      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
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
     or counting above `specs-above` (both in .pearde/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# Upgrade says two contradictory things

`pearde upgrade` reports failure and success in consecutive lines. It prints
that it could not regenerate the memo index, then immediately that there was no
memo to index. Both come from the same silent return value, so neither line
tells the reader what actually happened.

**What was decided.** Separate the two cases so each prints what actually
happened.

**Where.** `index_memos()` in `resources/board/init.py` returns `None` for
**both** "there is no memos directory" and "the regeneration failed", and
`cmd_upgrade` branches on that one value twice. It landed as part of
`upgrade-leaves-the-memo-index-stale`, commit `bc1c589`, and was found by that
PRD's own implementer.

**The consequence for a requested PRD.** `upgrade` is how an older board is
brought onto the current contract. A person who runs it on a board that is fine
is told it is broken, and a person who runs it on a board whose index genuinely
failed to rebuild is told there was nothing to rebuild. Either way the command's
own report is not evidence, which defeats the point of printing one.

**Cosmetic sibling, not this PRD's.** `knowledge.py board` counts
`memos/README.md` as a memo on both paths.

**Filed `deferred` rather than `open`** so the derived tree stays under the
`@references/parts/derived.md` tripwire while three requested PRDs are still
active. The decision above stands; only the scheduling is parked.

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
     the best one first and marked `(recommended)`. Only real forks the user
     must settle (naming, scope,
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
