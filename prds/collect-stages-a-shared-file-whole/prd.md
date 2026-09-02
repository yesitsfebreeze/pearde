---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: derived    # requested = the user asked | derived = the board found it
from: the-harness-sweep-is-capped-so-a-red-is-a-real-red  # derived only — the PRD whose work surfaced this one
priority: 45        # higher first
complexity: 33      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: high
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.61h
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

# Collect stages a shared file whole

`pearde collect` stages every file in a PRD's footprint **whole**, even when a
second PRD's uncommitted work sits in the same file. The finished PRD's commit
then carries the unfinished PRD's edits under the wrong name, and nothing is
printed to say so.

**What was decided.** A shared file is either split correctly, or the recording
stops and says why. Silence is not one of the outcomes.

**Reproduced this round, read-only, twice, stable.** `resources/doctor.sh` is
in the footprint of both `the-harness-sweep-is-capped-so-a-red-is-a-real-red`
(claimed) and `the-brief-names-the-verdict-line-collect-requires` (specced).
`git diff -U0` shows four hunks: `@@ -580 +580,3 @@` and `@@ -588 +590 @@` are
the brief PRD's; `@@ -738,4 +740,22 @@` and `@@ -745,0 +766 @@` are the cap
PRD's. `sort_paths` emits
`git add -- references/parts/doctor.md resources/doctor.sh`, with
`partial (hunk-split): {}` and `stop: []`.

**Both halves of the existing guard are blind, for two independent reasons.**
The guard is the `done` PRD
`collect-commits-only-the-prd-s-own-edits-not-the-footprint-s`.

1. Its sibling refusal is scoped to `HELD = ("analyzing","claimed","blocked")`.
   The brief PRD is `specced`, so `others` is empty and no `Stop` is raised.
   Sixteen PRDs name `doctor.sh` and only the cap PRD is HELD. That PRD's
   spec02 already documents an "analyzing window" gap; this is a **third**
   gap — `specced`, with code already standing in the tree.
2. Its hunk-splitter is **structurally dead on this machine.** `snapshot()`
   at `resources/board/collect.py:707` does
   `root = planlib.repo_root(prd["dir"])`. The PRD directory is under
   `.pearde`, which is a **linked worktree** and therefore its own repo root,
   so the claim baseline holds nine board paths and zero code-repo paths.
   `base["hunks"]` never holds a code path, `new_hunks` returns `"all"`, and
   every code-repo footprint file is committed whole, always.

**The consequence for a requested PRD.** Any `collect` on a requested PRD whose
footprint touches a file a second PRD is also editing commits that second PRD's
work under the first's name and message. The commit history — the board's one
record of who changed what — is then wrong, and silently so. It came within one
command of happening to `the-harness-sweep-is-capped-so-a-red-is-a-real-red`
this round.

Same root cause as `filing-refuses-a-file-it-does-not-hold`: a linked worktree
plus `repo_root`.

**Known workaround, until this lands.** Set the contending PRD to `blocked`
before the collect so the `Stop` fires and names the clash; or pass
`--widen <the shared path>` so the sweep is on the record rather than invisible.

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

## Report

spec01: exit 0
PASS 7e-code-dirt-in-the-one-side
---- 17 passed, 0 failed
verify.sh exit 0
47 checks · 47 pass · 0 fail
hunks-land-where-they-came-from: 47 checks · 47 pass · 0 fail

spec02: exit 0
PASS 5a-done-sibling-ok
---- 17 passed, 0 failed
verify.sh exit 0
---- 23 passed, 0 failed
run.sh exit 0
collect-commits-only-the-prd-s-own-edits: 23 passed, 0 failed

spec03: exit 0
PASS 7e-code-dirt-in-the-one-side
---- 32 passed, 0 failed
verify.sh exit 0
selected run made 13 checks
probe tally: 32 passed, 0 failed
