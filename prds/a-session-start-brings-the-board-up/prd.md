---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 40       # higher first
complexity: 15      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.71h
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

# a session start brings the board up

The user's words, 2026-09-02: *"I want, when we start a session, that we
ensure that the board is brought up."*

**What exists when this is done.** Opening a Claude Code session in a repo
that holds a board brings the view daemon up and registers that board with
it, with nobody typing `pearde view`. Concretely: a `SessionStart` hook,
installed beside the guard's `PreToolUse`/`PostToolUse` hooks in the
project's `.claude/settings.json`, runs `python3
@resources/board/serve.py ensure <board>` — the command `serve.py` already
documents as *"safe on every session start, so a board re-announces
itself"* (`resources/board/serve.py:45`). After a reboot, the first session
in any board's repo turns `doctor`'s `view` row from `off` to `ok` without
a `--fix`, and `@references/install.md:186`'s sentence — *"which every
session start does"* — becomes true instead of aspirational.

**Why it matters.** After a machine restart the daemon is down and nothing
restarts it: there is no launchd agent, no session hook, and `serve.py
ensure` is called only by `pearde view`, `init` and `doctor --fix`. The
manual claims otherwise. A board whose live page is down until someone
notices is a board read from stale HTML, and the claim in the manual is the
kind of line `correct-a-documented-claim` exists for — except here the
user chose to make the line true rather than to delete it.

**Constraints and non-goals.**

- The hook is the guard's neighbour: same file, same shape, same absolute
  path to this checkout. It must be quiet on success (a session start prints
  nothing extra), must never block or fail the session when the daemon
  cannot start (a port held, no Python), and must cost under a second when
  the daemon is already up — `ensure` on a running daemon is a register
  call, not a start.
- The install must lay it down: whatever writes the guard hooks into a
  project's `.claude/settings.json` (`resources/install.sh` / the install
  manual) writes this one too, and `doctor` says when it is missing —
  the same way it reports the guard hooks.
- No launchd agent, no machine-wide list, no cron. Nothing lands outside a
  board and the project's own `.claude/settings.json` —
  `.pearde/memos/every-artifact-lands-inside-the-board.md` binds.
- Not in scope: a session started outside any board's repo (the hook finds
  no `.pearde/` and exits 0 silently); the twelve leaked `serve.py`
  daemons of `leaked-background-services-outlive-their-fixtures`.

**Pointers.** `resources/board/serve.py` (`ensure`, line 5 and 45);
`resources/doctor.sh:660-680` (the `view` row and its `--fix`);
`.claude/settings.json` (the guard hooks, the shape to copy);
`references/install.md:186`; `references/parts/doctor.md`.

<!-- Three more headings exist, and none of them is a slot to copy down. Each
     is a claim about the state of this PRD, so an empty copy of it is a false
     one: an empty `## Questions` stops the board on nothing, an empty
     `## Answers` reads as answered, an empty `## Failure` reads as a failed
     attempt. Write the heading when it has content; until then it is absent,
     which is the honest state. @resources/questions.py reports the empty
     ones, and `doctor`'s `questions` row runs it. -->

<!-- `## Questions` — analyst-only, when blocked on the user: one pass in the
     format of drill.md — `### Q1: <title>`, the fork in two sentences ending
     in "?", then exactly three prepared answers, each a complete decision,
     the best one first and marked `(recommended)`. Only real forks the user
     must settle (naming, scope,
     cost) — never facts a worker could look up, never the PRD restated. A PRD
     parked on the user with no such pass never says what it is asking.
     Written in plain words for the person who asked, never for the board — no
     backtick, no path, no PRD name, no board word, 60 words in the fork and 25
     in an answer: the table in @references/drill.md is the whole rule, and
     @resources/questions.py refuses a pass that breaks it. -->

<!-- `## Answers` — orchestrator-only (or the view), written after asking the
     user: `**Q1** — <the picked answer verbatim, or the user's own words>`,
     numbers matching the pass above it. Analysts read these before speccing.
     An `## Answers` with no `## Questions` above it answers nothing. -->

<!-- `## Failure` — implementer-only, after a FAILED attempt: what broke, what
     was tried. `retry` moves this into the body as history and reopens the
     PRD. -->

## Report

spec01: exit 0
── A. guard on writes the SessionStart entry
  ok   A on names SessionStart
  ok   A on names serve.py ensure
  ok   A five + lines — the env cap and four hooks
  ok   A four of them are hooks
  ok   A one SessionStart entry
  ok   A the entry carries no matcher
  ok   A the command
  ok   A hook type command
  ok   A the three guard hooks are still there
  ok   A indent 2, trailing newline
── B. on is idempotent, off takes exactly it out
  ok   B a second on changes nothing
  ok   B four - lines
  ok   B off names SessionStart
  ok   B off empties hooks
  ok   B off leaves the env key
── C. a foreign SessionStart entry is kept
  ok   C the foreign entry stays first
  ok   C ours is appended
  ok   C off leaves the foreign entry
  ok   C off leaves it alone
── D. guard status notes a missing SessionStart hook
  ok   D wired: no note
  ok   D unwired: guard row still ok
  ok   D unwired: the note
  ok   D unwired: the note says the fix
  ok   D unwired: still exit 0
── E. doctor carries the same note
  ok   E doctor notes the missing hook
  ok   E wired: doctor is quiet about it
── F. the command itself: quiet, cheap, exit 0 anywhere
  ok   F cold: exit 0
  ok   F cold: silent
  ok   F cold: the board is registered
  ok   F warm: exit 0
  ok   F warm: silent
  ok   F warm: under a second (0.0761568546295166 s)
  ok   F outside a board: exit 0
  ok   F outside a board: silent
  ok   F unusable port: exit 0
  ok   F unusable port: silent
── G. doctor's view row flips on one session start
  ok   G before: view is off
  ok   G after one hook run: view is ok
  ok   G and no --fix was needed
── H. the docs say it
  ok   H guard.md holds the SessionStart block
  ok   H guard.md says why || true
  ok   H install.md names the hook
  ok   H install.md no longer only aspires
── I. live: a real session start brings the board up
  ok   I the session answered
  ok   I the session start printed nothing extra
  ok   I the board is registered

46 checks · 46 pass · 0 fail · 0 skip
— the refusal
  ok   A1 an Edit through the link from another board is denied
  ok   A2 the deny names the real path the link resolves to
  ok   A3 the deny names the path as given, resolving
  ok   A4 the deny names the memo
  ok   A5 the deny names the session's board
  ok   A6 way out one: file a PRD on the skill's own board
  ok   A7 way out one is a command, run from the skill root
  ok   A8 way out two: hand the edit to a session working it
  ok   A9 the deny is one PreToolUse JSON object
  ok   A10 a Write through the link is denied the same way
  ok   A11 a Write of a new file through the references link is denied — realpath resolves the link above it
  ok   A12 the real path by name, no link, is denied too — the leak is the write, not the link
  ok   A13 a real path is named once, not 'resolves to' itself
  ok   A14 resources/ through the link is skill tree
  ok   A15 skills/ through the SKILL.md link is skill tree
  ok   A16 the cwd given as its real path (/private/var on darwin) is still another board
  ok   A17 each refusal is counted on the session's block (refused=7)
  ok   A18 nothing written under resources/board/state/ — PEARDE_GUARD_STATE moved it
— what passes
  ok   P1 an Edit under the project's own prds/ passes
  ok   P2 a Write under the project's own prds/ passes
  ok   P3 the same Edit from a working directory in this repo passes
  ok   P4 a working directory inside this repo's board passes
  ok   P5 no board in scope passes — the guard refuses only a round provably another board's
  ok   P6 no board in scope, the real path by name, passes
  ok   P7 a write under this repo's own prds/ from another board passes — filing here is the way in
  ok   P8 a Read through the link is not this rule's business
  ok   P9 a body edit of the project's prd.md still passes (state_by_hand untouched)
  ok   B1 the Bash hook does not match a shell write through the link — the caveat guard.md states
— status and doctor
  ok   S1 guard status ok says skill tree guarded
  ok   S2 guard status exits 0
  ok   S3 guard status still names the settings file
  ok   S4 status has a broken row for the second rule — the words are earned by a probe
  ok   S5 doctor.sh's ok row carries the two words
  ok   S6 doctor.sh moved one line
— the text
  ok   T1 guard.md refusals table has the row
  ok   T2 the row names the two ways out
  ok   T3 the row names the memo
  ok   T4 guard.md says the Bash hook does not match a shell write
  ok   T5 install.md's link bullet says the guard refuses a write through them from another board
  ok   T6 install.md names the memo
  ok   T7 guard.py's docstring lists the rule beside the other four

41 checks · 41 pass · 0 fail
  guard       ok      wired in /Users/feb/dev/infra/pearde/.claude/settings.json · MAX_THINKING_TOKENS=8000 · skill tree guarded
                      no SessionStart hook — the view is not brought up on a session start; pearde guard on writes it

spec02: exit 0
── A. guard on writes the SessionStart entry
  ok   A on names SessionStart
  ok   A on names serve.py ensure
  ok   A five + lines — the env cap and four hooks
  ok   A four of them are hooks
  ok   A one SessionStart entry
  ok   A the entry carries no matcher
  ok   A the command
  ok   A hook type command
  ok   A the three guard hooks are still there
  ok   A indent 2, trailing newline
── B. on is idempotent, off takes exactly it out
  ok   B a second on changes nothing
  ok   B four - lines
  ok   B off names SessionStart
  ok   B off empties hooks
  ok   B off leaves the env key
── C. a foreign SessionStart entry is kept
  ok   C the foreign entry stays first
  ok   C ours is appended
  ok   C off leaves the foreign entry
  ok   C off leaves it alone
── D. guard status notes a missing SessionStart hook
  ok   D wired: no note
  ok   D unwired: guard row still ok
  ok   D unwired: the note
  ok   D unwired: the note says the fix
  ok   D unwired: still exit 0
── E. doctor carries the same note
  ok   E doctor notes the missing hook
  ok   E wired: doctor is quiet about it
── F. the command itself: quiet, cheap, exit 0 anywhere
  ok   F cold: exit 0
  ok   F cold: silent
  ok   F cold: the board is registered
  ok   F warm: exit 0
  ok   F warm: silent
  ok   F warm: under a second (0.07178688049316406 s)
  ok   F outside a board: exit 0
  ok   F outside a board: silent
  ok   F unusable port: exit 0
  ok   F unusable port: silent
── G. doctor's view row flips on one session start
  ok   G before: view is off
  ok   G after one hook run: view is ok
  ok   G and no --fix was needed
── H. the docs say it
  ok   H guard.md holds the SessionStart block
  ok   H guard.md says why || true
  ok   H install.md names the hook
  ok   H install.md no longer only aspires
── I. live: a real session start brings the board up
  ok   I the session answered
  ok   I the session start printed nothing extra
  ok   I the board is registered

46 checks · 46 pass · 0 fail · 0 skip
  guard       ok      wired in /Users/feb/dev/infra/pearde/.claude/settings.json · MAX_THINKING_TOKENS=8000 · skill tree guarded
                      no SessionStart hook — the view is not brought up on a session start; pearde guard on writes it
  ok    no unguarded $HOME read anywhere in doctor.sh
  ok    no unbound-variable line in doctor's report under a scrubbed env
  ok    every row below vault still prints with no HOME (board vault view plan)
  ok    the vault row reports rather than aborting — vault       broken  /tmp/pearde-nohome.y7OvnU/repo/.pearde/.obsidian is not in Obsidian's vault register — ▸vault opens the nearest registered ancestor instead
  ok    no HOME reaches the same verdict as HOME=/Users/feb on one board — vault       broken  /tmp/pearde-nohome.y7OvnU/repo/.pearde/.obsidian is not in Obsidian's vault register — ▸vault opens the nearest registered ancestor instead (exit 1 both)
  ok    HOME with a register naming the board still reads ok, registered
  ok    HOME holding no Obsidian config still reads ok, nothing to register
  ok    an unregistered board is still called broken — the guard did not mute the row
  ok    XDG_CONFIG_HOME finds the register over a home that holds no macOS register
  ok    with no usable python3 the scrubbed run still reaches the with-HOME verdict — a python3 stub that exits 1, a thin PATH with no python3, and no PATH exported
  ok    the last-resort arm reports broken and claims only that the home could not be resolved
  ok    the view-row harness reads green end to end — 6 checks · 6 pass · 0 skip · 0 fail
12 checks · 12 pass · 0 fail · 0 skip
probe harness complete
  ok    the view block defines PBOARD before its elif reads it
  ok    every variable the view row names is defined
  ok    no unbound-variable line anywhere in doctor's report
  ok    view ok when the service holds the spelling doctor walks
  ok    view ok across a symlinked START — pwd -P bridges the spelling
  ok    the ok line names the board, spelled /tmp/pearde-viewrow.sFazPn · /status holds it
6 checks · 6 pass · 0 skip · 0 fail
probe harness complete
.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh: line 45: 79275 Terminated: 15          python3 "$D/srv1.py"
.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh: line 45: 79530 Terminated: 15          python3 "$D/srv2.py"
.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh: line 45: 79781 Terminated: 15          python3 "$D/srv3.py"

spec03: exit 0
── A. guard on writes the SessionStart entry
  ok   A on names SessionStart
  ok   A on names serve.py ensure
  ok   A five + lines — the env cap and four hooks
  ok   A four of them are hooks
  ok   A one SessionStart entry
  ok   A the entry carries no matcher
  ok   A the command
  ok   A hook type command
  ok   A the three guard hooks are still there
  ok   A indent 2, trailing newline
── B. on is idempotent, off takes exactly it out
  ok   B a second on changes nothing
  ok   B four - lines
  ok   B off names SessionStart
  ok   B off empties hooks
  ok   B off leaves the env key
── C. a foreign SessionStart entry is kept
  ok   C the foreign entry stays first
  ok   C ours is appended
  ok   C off leaves the foreign entry
  ok   C off leaves it alone
── D. guard status notes a missing SessionStart hook
  ok   D wired: no note
  ok   D unwired: guard row still ok
  ok   D unwired: the note
  ok   D unwired: the note says the fix
  ok   D unwired: still exit 0
── E. doctor carries the same note
  ok   E doctor notes the missing hook
  ok   E wired: doctor is quiet about it
── F. the command itself: quiet, cheap, exit 0 anywhere
  ok   F cold: exit 0
  ok   F cold: silent
  ok   F cold: the board is registered
  ok   F warm: exit 0
  ok   F warm: silent
  ok   F warm: under a second (0.0821390151977539 s)
  ok   F outside a board: exit 0
  ok   F outside a board: silent
  ok   F unusable port: exit 0
  ok   F unusable port: silent
── G. doctor's view row flips on one session start
  ok   G before: view is off
  ok   G after one hook run: view is ok
  ok   G and no --fix was needed
── H. the docs say it
  ok   H guard.md holds the SessionStart block
  ok   H guard.md says why || true
  ok   H install.md names the hook
  ok   H install.md no longer only aspires
── I. live: a real session start brings the board up
  ok   I the session answered
  ok   I the session start printed nothing extra
  ok   I the board is registered

46 checks · 46 pass · 0 fail · 0 skip
── A. no .claude/: on, on again, status, off
── B. other keys and hooks: on then off is byte-identical
── C. a set cap stays; not-JSON is refused untouched
── D. no <repo>: the board above the cwd, or a refusal
── E. help, init, the manual

78 checks · 78 pass · 0 fail
