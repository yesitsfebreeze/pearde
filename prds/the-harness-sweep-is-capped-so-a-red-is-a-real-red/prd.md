---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 40        # higher first
complexity: 18      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius: mid
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 9.71h
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

# The harness sweep is capped so a red is a real red

`doctor --harnesses` launches all forty-eight harnesses at once and several
compete for the same three fixed ports, so a failure in the run is not evidence
of a fault. When this is done, a red from the sweep is a real red, and the
number it prints can be believed without re-running anything by hand.

**The user's decision, taken at the drill:** *"Run them a few at a time, so a
failure is always a real one."* A concurrency cap is the fix; per-harness
skip-when-busy was the fork the user did **not** pick, and accepting the noise
was the fork the user rejected.

**The evidence, from the sweep of 2026-09-01 23:20 (67s) — cite, do not
re-establish.** The sweep read `harnesses broken — 7 of 48 green · 40 unpinned
· 9 failed`. Re-running all nine **serially** at 23:26 split them cleanly:
**four of the nine were sweep artifacts** — green alone, red only under
contention: `an-acceptance-box-that-cannot-fail-is-refused` (2/2),
`nothing-left-open/the-line-tells-the-truth` (85/85),
`seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green`
(37 checks · 36 pass · 1 skip). Nearly half the failures were luck.

**The mechanisms, all three of them in scope.**

1. **No job cap.** `resources/doctor.sh:743-750` runs a bare `&` per iteration
   then one bulk `wait`. The code's own comment at `:740` already says a
   `wait -n` cap should be added if needed. It is needed.
2. **Unguarded fixed ports.** `.pearde/prds/…/the-view-row-names-a-variable-that-exists/probe/verify.sh`
   binds **8477, 8478 and 8479** at `:82`, `:97` and `:111` with no
   availability check. A proven `port_busy()` one-liner already exists at
   `the-doctor-completes-without-a-home/probe/verify.sh:244` and correctly
   *skips* rather than passing — reuse it, do not invent a second one.
3. **A leak that makes the collision permanent.** That same harness never
   initialises `SRVPID3`: `:27` sets only `SRVPID` and `SRVPID2`; `SRVPID3` is
   first assigned at `:112`; `cleanup()` at `:31` reads it under `set -u`
   (`:16`) with `trap … EXIT` (`:34`). Any exit before `:112` dies inside
   cleanup, skips the `rm -rf` at `:32`, and leaves 8477 and 8478 listening.
   Latent today — no 84xx listener was found during or after the sweep — and
   it must be fixed with the cap, or the cap will hide it.

**Also in scope, because it is the same class and was mis-diagnosed once
already:** `seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green`'s
`probe/verify.sh:35` picks a spare port by binding port 0 and **closing the
socket before use** — a TOCTOU that is a port race, not a stale check. It is
explicitly excluded from the stale-checks PRD and belongs here.

**Why this matters to what ships.** `doctor --harnesses` is the number a
session reads to decide whether the board is healthy. Today that number cannot
be believed without re-running every failure serially by hand, which is what
the sweep exists to avoid.

**Constraints and non-goals.**

- The cap is a number, not a rewrite: keep the existing sweep shape and the
  line it prints.
- Do not serialise the whole run — the point is a trustworthy run, not a slow
  one. Name the chosen cap and say why in the report.
- Do not re-aim any check that fails on its merits; the four stale ones are a
  separate PRD and must not be touched here.
- Acceptance is a demonstration. It was written as an **elimination** — the
  sweep run twice in a row returning the same set of failures, equal to what a
  serial re-run returns. **Re-aimed at the drill of 2026-09-02** (see
  `## Answers` Q1) to the **rate cut** the mechanism can actually deliver:
  five capped sweeps must produce **no more** reds in the contending class
  than **one** uncapped sweep does — a fivefold cut in the per-run rate — and
  every red that survives is named in the report. The residue is not the cap's
  to remove: it comes from harnesses asserting on wall-clock or on a whole
  `doctor` report, which reads machine-global state, and no cap above one
  settles those. That remainder is filed separately as
  `two-self-tests-fail-on-timing-not-on-code`.

## Questions

### Q1: How clean the checks have to be

Running the checks a few at a time cut false failures about fivefold, but not
to zero — roughly one run in five still shows a failure that is not real. The
original bar was zero: do you accept the fivefold cut, or hold out for none?

1. **Accept the fivefold cut** — take the big improvement now, judge the checks against what it can deliver, and handle the last few separately. (recommended)
2. **Hold out for none** — keep this work open until five runs in a row show no false failure at all.
3. **Call it good and stop measuring** — accept it as it stands and spend no more time counting how often a failure is false.

or write your own

<!-- for the board: the cap stands; the residue is three neighbour harnesses
     asserting on wall-clock and on whole doctor reports, routed separately -->

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

## Answers

**Q1** *(answered 2026-09-02 08:41)* — Accept the fivefold cut — take the big improvement now, judge the checks against what it can deliver, reword the acceptance to match what the mechanism can deliver, and file the remainder separately.
