---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: derived    # requested = the user asked | derived = the board found it
from: the-harness-sweep-is-capped-so-a-red-is-a-real-red  # derived only — the PRD whose work surfaced this one
priority: 35        # higher first
complexity: 22      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.26h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
workflow: probe-then-spec
commit: 758b040
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

# Two self tests fail on timing not on code

Two harnesses judge by how long something took, or by the state of the whole
machine, so they can go red while the code they cover is perfectly correct.

**What was decided.** Rewrite them to judge the code, so a red always means
something is actually broken. Not to mark them unreliable and stop counting.

**The two.** `readme-in-three-rings` and
`scan-parses-the-board-once-and-caches-it-by-mtime`. Both assert on a
wall-clock margin or on a whole `doctor` report, and a `doctor` report reads
machine-global state — another board, another daemon, another session's
uncommitted tree all move it.

**Scope, corrected.** A third harness, `init-seeds-a-board-doctor-calls-green`,
has the same defect but is **inside**
`the-harness-sweep-is-capped-so-a-red-is-a-real-red`'s footprint — that PRD's
spec03 exists to fix it and its body names it. It is not this PRD's.

**Why the cap cannot help.** Measured: cap 2 both flaked *and* cost about 70%
more wall-clock than cap 4 (140s against 82s). No cap above 1 settles a
machine-global assertion, and lowering the cap makes it worse.

**The consequence for a requested PRD.**
`the-harness-sweep-is-capped-so-a-red-is-a-real-red` accepts a residual false
red it cannot remove, because these harnesses produce it. Every PRD after it
reads its own verify output through a sweep that can redden for no reason, so
a red carries no information until this lands.

**A hazard any rewrite must survive.** A sandboxed shell's clock on this
machine lags the host's by about 6.7 hours. Any wall-clock assertion that
compares a timestamp taken in one shell against one taken in another is
already wrong for that reason alone; compute both ends in the same call.

**Sibling, outside this contract.** `the-fixtures-meet-the-tool`'s
`F no file under resources/` row reads the whole working tree's `git diff` and
reddens on any neighbour's uncommitted work.

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
ok   files walked (True)
ok   a cold walk reads every file once (14)
ok   a warm walk reads nothing (0)
ok   one changed mtime costs exactly one re-read (1)
ok   the check can fail: without the cache the walk reads every file (14)
parse-cache verify: pass
--- good: exit 0
    ok   files walked (True)
    ok   a cold walk reads every file once (14)
    ok   a warm walk reads nothing (0)
    ok   one changed mtime costs exactly one re-read (1)
    ok   the check can fail: without the cache the walk reads every file (14)
    parse-cache verify: pass
--- never: exit 1
    ok   files walked (True)
    ok   a cold walk reads every file once (14)
    FAIL: a warm walk reads nothing — got 14, want 0
    FAIL: one changed mtime costs exactly one re-read — got 14, want 1
    ok   the check can fail: without the cache the walk reads every file (14)
    parse-cache verify: FAILED
--- stale: exit 1
    ok   files walked (True)
    ok   a cold walk reads every file once (14)
    ok   a warm walk reads nothing (0)
    FAIL: one changed mtime costs exactly one re-read — got 0, want 1
    ok   the check can fail: without the cache the walk reads every file (14)
    parse-cache verify: FAILED

spec02: exit 0
A. size and order
B. the quickstart is five lines
C. the diagram names the nine states, and no other
D. the pass is loop.md's seven rows
E. the rings, the glossary, the addressing
F. every claim is true to the code
G. the footprint beside the README
H. the five lines, end to end

75 checks · 75 pass · 0 fail
old logic — a plain diff of the two whole reports:
  rows differing: 2  (the old check demanded 0) -> RED
re-aimed logic — a control pair:
  moved with the home held constant, so not judged: view
  home-dependent rows, reproduced on a second pair: ''
  -> green
--- good (baseline): 0 fail
--- skill: adds 0 over the baseline
--- home: adds 2 over the baseline
    + FAIL: 6 ...and the scrubbed home breaks no row the checkout had not already broken
    + FAIL: 6 no row but vault reads the home
--- board: adds 2 over the baseline
    + FAIL: 2 the board init wrote breaks no doctor row
    + FAIL: 6 ...and the scrubbed home breaks no row the checkout had not already broken
FLIP: green on the input it must pass, red on the input it must catch
