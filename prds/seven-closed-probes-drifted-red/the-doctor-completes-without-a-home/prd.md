---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 0        # higher first
complexity: 6      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 1.39h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
needs:
  - the-fixtures-meet-the-tool
workflow: probe-then-spec
commit: ca29535 5ebefc7
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

# the-doctor-completes-without-a-home — doctor.sh finishes every row when the shell holds no HOME — the vault row's register read is guarded and nothing aborts — and the view-row probe reads green end to end

doctor.sh finishes every row when the shell holds no HOME — the vault row's register read is guarded and nothing aborts — and the view-row probe reads green end to end

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
guarded
builtin-first
arm-broken
  ok    no unguarded $HOME read anywhere in doctor.sh
  ok    no unbound-variable line in doctor's report under a scrubbed env
  ok    every row below vault still prints with no HOME (board vault view plan)
  ok    the vault row reports rather than aborting — vault       broken  /tmp/pearde-nohome.KaFv7J/repo/.pearde/.obsidian is not in Obsidian's vault register — ▸vault opens the nearest registered ancestor instead
  ok    no HOME reaches the same verdict as HOME=/Users/feb on one board — vault       broken  /tmp/pearde-nohome.KaFv7J/repo/.pearde/.obsidian is not in Obsidian's vault register — ▸vault opens the nearest registered ancestor instead (exit 1 both)
  ok    HOME with a register naming the board still reads ok, registered
  ok    HOME holding no Obsidian config still reads ok, nothing to register
  ok    an unregistered board is still called broken — the guard did not mute the row
  ok    XDG_CONFIG_HOME finds the register over a home that holds no macOS register
  ok    with no usable python3 the scrubbed run still reaches the with-HOME verdict — a python3 stub that exits 1, a thin PATH with no python3, and no PATH exported
  ok    the last-resort arm reports broken and claims only that the home could not be resolved
  ok    the view-row harness reads green end to end — 6 checks · 6 pass · 0 fail
12 checks · 12 pass · 0 fail · 0 skip
probe harness complete
  skip  the view-row harness is left to the sweep's own run of it — it binds 8477-8479 and this is a sweep; not asserted here
12 checks · 11 pass · 0 fail · 1 skip
probe harness complete
  ok    the view block defines PBOARD before its elif reads it
  ok    every variable the view row names is defined
  ok    no unbound-variable line anywhere in doctor's report
  ok    view ok when the service holds the spelling doctor walks
  ok    view ok across a symlinked START — pwd -P bridges the spelling
  ok    the ok line names the board, spelled /tmp/pearde-viewrow.1RVa7I · /status holds it
6 checks · 6 pass · 0 fail
probe harness complete
index problems not naming the neighbour's drop: 0 · naming this footprint: 0
  index       broken  115 problems
  vault       ok      ./.pearde/.obsidian · registered with Obsidian — ▸vault opens this board
index is the only broken row
.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh: line 28: 38502 Terminated: 15          python3 "$D/srv1.py"
.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh: line 28: 38721 Terminated: 15          python3 "$D/srv2.py"
.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh: line 28: 38945 Terminated: 15          python3 "$D/srv3.py"
