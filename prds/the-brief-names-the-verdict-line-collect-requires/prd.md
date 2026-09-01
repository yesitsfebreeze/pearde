---
state: specced        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 30        # higher first
complexity: 16      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual:          # a record. Nothing reads it
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: correct-a-documented-claim
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

# The brief names the verdict line collect requires

`collect` refuses any worker report whose first 40 lines carry no `Verdict:`
line — and the brief every worker is handed never says so. When this is done,
a worker that follows the brief verbatim produces a report `collect` accepts,
with no orchestrator reminder in the loop.

**The user's decision, taken at the drill:** *"Add it to the instructions, so
following them produces something that is accepted."* The brief changes; the
tool's requirement does **not** loosen.

**The mechanism, established and verified 2026-09-01 — cite it, do not
re-derive it.**

- `resources/board/collect.py:299` raises ``names no `Verdict:` ``.
- `verdict_of` (`:258`) is generous about decoration — bold, headings — but
  reads only the **first 40 lines** of the report.
- Occurrences of the word `Verdict:` in `references/parts/workers.md`: **0**.
  In `references/templates/`: **0**.
- **Be precise about where the gap is not.** `references/templates/report.md`
  is the *human* report written by `@@report`; `collect` never reads it. It is
  not the gap and must not be edited for this.
- The gap is the brief block at `references/parts/workers.md:163-164`, which
  says *"Return exactly one verdict:"* and names the six words, but never says
  the report file must carry a line beginning `Verdict:` inside its first 40
  lines.

**Folded in, because it is the same file and there is no second reading to
choose between.** `references/parts/workers.md:155-156` — handed verbatim to
every analyst — ships a duplicated half-sentence:

    > fits the build ahead, as you would one the PRD already carries. Then read
    > build ahead, as you would one the PRD already carries. Then read

`git log -L 154,157` places it in `7809756`, which rewrote the line above into
two and did not delete the old continuation from `eef2dba`. The repair is
deleting line 156. Do it in the same pass.

**Why this matters to what ships.** Every worker on every board is handed this
brief. Today it works only because the orchestrator remembers to add the word;
a worker that follows the instructions exactly gets its report refused.

**Constraints and non-goals.**

- Do not loosen `verdict_of` or the 40-line window. The user chose the
  instructions, not the tool.
- Do not touch `references/templates/report.md`.
- `doctor`'s `briefs` row reads `ok — 5 blocks · every placeholder named`, so
  the existing checker does not look for either shape. Whether it should is
  the analyst's call, but a check that would have caught the missing word is
  worth more than one that only counts blocks.

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
