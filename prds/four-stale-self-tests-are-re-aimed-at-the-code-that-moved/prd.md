---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 20        # higher first
complexity: 14      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.62h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: probe-then-spec
commit: f7a76ac
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

# Four stale self-tests are re-aimed at the code that moved

Four of the board's own harnesses fail because the thing each was written to
guard was later changed on purpose, and the check was never re-aimed. When this
is done, each one asserts what the code actually does now, so a red from any of
them means a real regression again.

**The user's decision, taken at the drill:** *"Bring each one back in line with
how things work now, so a failure means something again."* Re-aim, do not
delete, and do not leave them red.

**The four, each verified serially on 2026-09-01 at 23:26 — cite, do not
re-establish. ZERO of them is broken code.**

| harness | the check | what moved underneath it |
|---|---|---|
| `one-page-that-says-whats-up` (2 checks left) | a `purpose` div inside the timeline section; `calc(100vh - 260px)` | `resources/view/render.py:459` moved the div out (`eaa11a1`); `resources/view/view.css:508` now reads `calc(100vh - 104px)` (`4ce11ec`) |
| `the-fixtures-meet-the-tool` `:174` | wants `grep -c parse-cache .pearde/.gitignore` to be **0** | the ignore line has since been added — the check pinned the *absence* of a fix as a non-goal, and the fix happened |
| `the-board-runs-itself/collect-is-a-command` `:425` and `the-board-runs-itself/init-asks-nothing` `:211` | `resources/board/state/serve.json` | that path does not exist: the `every-artifact-lands-inside-the-board` invariant moved the registry to `<board>/.state/` (`resources/board/serve.py:389-391`) |
| `workflows-on-the-board/workflow-improve` `:331` | a table row in `references/parts/workers.md` | the prose was rewritten by `78357ed`; no three-way row is left |

`the-collect-and-brief-harnesses-are-carried-across-the-layout` is **downstream
only** — it sums sibling totals of `collect-is-a-command`. Fix that one and
this clears with it. Do not edit it directly.

**Two traps inside the traps, and both are part of this contract.**

1. `collect-is-a-command` and `init-asks-nothing` each carry a **sibling**
   check — *"the real registry is untouched"* — reading the same vanished
   path. Those pass **vacuously today**, empty compared to empty, and measure
   nothing. Re-aiming the failing check without re-aiming its silent sibling
   leaves the harness green and blind. Both move.
2. `init-seeds-a-board-doctor-calls-green`'s `D doctor exits 0 — got: 1` is
   **not** self-referential. That was refuted twice: it calls `bash "$DOC"
   "$PROJ"` with no `--harnesses`, against a `mktemp -d` fixture, and
   `resources/doctor.sh:726-731` guards nested runs on `PEARDE_HARNESSES`. It
   is a TOCTOU at that harness's `probe/verify.sh:35`, which picks a spare port
   by binding port 0 and **closing the socket before use**. That is a port-race
   defect and belongs to the harness-run PRD, not here — do not fix it twice.

**Why this matters to what ships.** These are the gates a PRD is called done
against. A harness that is red for being out of date teaches the next session
to skim past reds, which is how a real one gets shipped.

**Constraints and non-goals.**

- **Do not change `render.py` or `view.css` to satisfy a check.** Both those
  changes were deliberate, made by the view session that owns those files. The
  check moves to the code, never the reverse. Those two files are another
  session's; if a change to them looks necessary, that is a QUESTION, not an
  edit.
- Do not delete a check to make a harness green. The user rejected that fork
  explicitly.
- Do not touch `the-collect-and-brief-harnesses-are-carried-across-the-layout`;
  it is arithmetic over its sibling.
- Every one of the four must be shown red before and green after, run
  individually, not through a full sweep.

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
31 checks · 31 pass · 0 fail
exit=0
drawer live=True mutated=False | height live=True mutated=False
tally=31/31 fail=0 green drawer-rows=1 height-rows=1 view-files-moved=0

spec02: exit 0
  FAIL C every harness on the board ends on an exit-code-carrying check
  FAIL C the-gate's census row is green
  FAIL E …and the-gate fails only the two rows that read index.py check
  FAIL F no file under resources/ carries any of this
35 checks · 31 pass · 4 fail
exit=1
resources/board/init.py
row-ok=1 row-red=0 in-place=1 spent-non-goal=0 ignore-live=1 ignore-without-the-line=0

spec03: exit 0

133 checks · 133 pass · 0 fail
collect-is-a-command exit=0

89 checks · 89 pass · 0 fail
init-asks-nothing exit=0
verify: 7 checks · 7 pass · 0 fail
probe: 7 checks · 7 pass · 0 fail
downstream exit=0
collect=133/133 fail=0 green init=89/89 fail=0 green downstream=7/7 fail=0 green
R-rows=2 J-rows=2 in-C=2 in-I=2 dead-path=0,0 downstream-edited=0
find 0->1: 0 -> 1 | sentinel: absent -> 2192966820 2

spec04: exit 0
71/71 checks pass
exit=0
all-pass=1 row-ok=1 in-place=1 dead-needle=0 workers-moved=0 sentence-live=1 sentence-gone=0
