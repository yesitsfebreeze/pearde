---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: derived    # requested = the user asked | derived = the board found it
from: the-harness-sweep-is-capped-so-a-red-is-a-real-red  # derived only — the PRD whose work surfaced this one
priority: 35        # higher first
complexity: 31      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: high
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 3.09h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: probe-then-spec
commit: 76da1fe
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

# Leaked background services outlive their fixtures

Every harness fixture that starts a board service starts it with
`serve.py run` and none of them stop it. The processes outlive the scratch
directories they point at, by days.

**What was decided.** Each run stops what it started, and the ones already
stranded are cleaned up.

**Counted this round.** Thirteen live `serve.py` processes, up from eleven the
round before. Two were spawned at 01:24:40 and 01:24:42 by this board's own
harness sweeps while the round watched. Two predate 2026-08-31 (pids 78106,
98823). Exactly one is legitimate — pid 98256, the daemon watching the nine
real boards. The rest point at `mktemp` directories that no longer exist.

**Why the existing hygiene does not catch it.** Fixtures register through
`serve.py register`; `save_entry` returns early on an EPHEMERAL path, so no
registry row is written — but the daemon process itself is never reaped. The
registry is clean and the process table is not.

**The consequence for a requested PRD.** Leaked daemons hold ports. Port
contention is precisely the false-red class
`the-harness-sweep-is-capped-so-a-red-is-a-real-red` exists to eliminate, and
its residual red — one contention red over five capped runs — is measured
against a machine carrying thirteen of these. A sweep cannot be proven clean
while its own past runs are still listening.

**Related, and not this PRD's to fix.** `obsidian.json` holds roughly seven
hundred vault registrations, most of them dead fixture paths, churned by the
same fixtures. That is a memo, not work.

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
deleted-board daemon reaped=1 (pid 60820) · live-board daemon still up=1 (pid 60821)
bash: line 40: 60821 Killed: 9               PEARDE_IDLE_EXIT_S=4 PEARDE_PORT="$PB" python3 "$S" run > "$T/b.log" 2>&1

spec02: exit 0
serve: keeping pid 60570 — started 8s ago — inside the 60s grace a session start needs to register its board
serve: keeping pid 61665 · port 61564 — started 1s ago — inside the 60s grace a session start needs to register its board
serve: keeping pid 61666 · port 61566 — started 1s ago — inside the 60s grace a session start needs to register its board
serve: keeping pid 73329 · port 8443 — watching 9 live board(s): pearde, manola, master, mitosys, model, realm, shared, dotfiles, racer-mi
serve: 0 of 4 stranded
serve: would stop pid 61665 · port 61564 — watching no board
serve: keeping pid 61666 · port 61566 — watching 1 live board(s): kept
serve: 1 of 2 stranded
  --pid 'abc' -> exit 2
  --pid '' -> exit 2
  --pid '--' -> exit 2
  --pid '12x' -> exit 2
  --pid '0' -> exit 2
stranded stopped=1 (pid 61665) · live-board daemon kept=1 (pid 61666)
bash: line 73: 61666 Killed: 9               PEARDE_IDLE_EXIT_S=9999 PEARDE_PORT="$PB" python3 "$S" run "$T/kept/.pearde" > "$T/b.log" 2>&1

spec03: exit 0
PASS  no .state/ in this tree but the board's own
PASS  the install holds no state dir of its own
PASS  no MACHINE_DIR outside the one-shot migration
PASS  a driven board wrote nothing outside .pearde/ (bar .gitignore)
PASS  the driven surface left the install unchanged
PASS  the guard refuses a pass file written outside the board
PASS  the guard passes the board's own pass file
17 checks · 17 pass · 0 fail
probe tally: 17 checks · 17 pass · 0 fail
watched before: all dotfiles manola master mitosys model pearde racer-mi realm shared
watched after:  all dotfiles manola master mitosys model pearde racer-mi realm shared
