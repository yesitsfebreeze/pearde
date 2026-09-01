# the-harness-sweep-is-capped-so-a-red-is-a-real-red — analyst report

**Verdict: SPECCED** — 3 specs, complexity 18, blast-radius mid, workflow
`probe-then-spec`.

The build went all the way through. All four mechanisms the PRD names are
implemented, uncommitted in the tree, and the PRD's acceptance demonstration
passes: two consecutive capped sweeps returned the identical failure set, and
that set equals what a full serial re-run of every harness returns.

## The number, before and after

| run | line | failures |
|---|---|---|
| baseline, uncapped (this session) | `7 of 48 green · 40 unpinned · 84s · 8 failed` | 8 |
| capped, run A | `8 of 52 green · 43 unpinned · 80s · 1 failed` | 1 |
| capped, run B | `8 of 52 green · 43 unpinned · 80s · 1 failed` | 1 |
| full serial re-run | — | 1, the same one |

Seven of the eight baseline reds were contention. The survivor is
`seven-closed-probes-drifted-red/the-fixtures-meet-the-tool`, red on its merits
and another PRD's business (finding 3 below).

**The cap costs nothing.** 80s capped against 84s uncapped. The uncapped run was
not faster — it was thrashing. This settles the PRD's "do not serialise the whole
run" constraint with measurement rather than argument.

**The chosen cap is 4**, `PEARDE_HCAP` overriding it for an experiment. Above the
number of harnesses that contend for a fixed port or a board service at any one
moment, and far below the box's ten cores, so a harness waiting on a socket with
a timeout is never starved of CPU. Raising it trades trust for wall-clock;
lowering it buys no more trust, only time.

## What was built

All four are in the tree, uncommitted, and every one is asserted by this PRD's
own harness at `probe/verify.sh` (14 checks, 14 pass, green both standalone and
under `PEARDE_HARNESSES=1`).

1. **The cap** — `resources/doctor.sh:738-768`. `HCAP="${PEARDE_HCAP:-4}"` and a
   gate on the running-job count before each `&`. The row keeps its shape and
   its printed line.
2. **The port guard** — the view-row harness stands down to `skip` on each of
   8477/8478/8479 when held, reusing the one existing `port_busy` spelling
   rather than growing a second.
3. **The leak** — `SRVPID`, `SRVPID2` and `SRVPID3` are now initialised together
   before the `EXIT` trap is armed. Demonstrated by running a truncated copy of
   the harness that exits early and confirming nothing is left listening.
4. **The TOCTOU** — `init-seeds`' spare port is re-checked immediately before
   use and re-picked up to five times, failing loudly rather than proceeding
   with an empty value.

## Finding 1 — the comment promised a mechanism this shell does not have

`doctor.sh:740-741` said to "add a `wait -n` job cap only if needed". `wait -n`
arrived in **bash 4.3**; `/bin/bash` on macOS is **3.2.57** and this script's
shebang is `#!/bin/bash`, so `wait -n` exits 2 with `wait: -n: invalid option`.
Had the cap been written the way the comment specified, it would have broken
`doctor` outright on every macOS box.

The portable equivalent is polling `jobs -r`, which holds the cap exactly —
`jobs -r` lists only running jobs and works in a non-interactive shell, and a
`while read … done <<EOF` loop does not put its body in a subshell, so the jobs
it starts are visible to it. Measured holding an exact cap of 3 over 12 jobs.

Written back to the knowledge base as `[[260902-e933]]`, since it is a fact
about bash and macOS rather than about this repo.

## Finding 2 — no harness that reports skips can pin its denominator

`doctor.sh` detects a pinned harness with a regex requiring the literal
spelling `$((PASS+FAIL))` followed by `=` and a number. A harness that stands
checks down — which is exactly what the port guards above require, and what
`init-seeds` and `the-doctor-completes-without-a-home` already do — has a
legitimately variable `PASS+FAIL` and can only pin on `$((PASS+FAIL+SKIP))`,
which the regex does not match.

So the three harnesses on this board that report skips are all counted
`unpinned` even where they fail loudly on a dropped check, and 43 of 52 harnesses
now read unpinned. This PRD's own harness pins honestly on the total and is
still reported unpinned as a result.

Not fixed — re-aiming the detector is a different contract and widening this one
would be initiative, not scope. Filed here as the PRD's report asks.

## Finding 3 — the one surviving red

`seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` fails serially and
in every sweep, with `FAIL F .state/parse-cache.json is still unignored on the
board — a finding, not a fix`. It is red on its merits and untouched, per the
PRD's instruction not to re-aim a check that fails honestly.

## Finding 4 — the board was being written while it was measured

The harness denominator moved 48 → 51 → 52 across this session, and two early
capped sweeps disagreed with each other before settling. That was other sessions
adding PRDs to the board mid-run, not contention. Consequence for whoever
verifies this: the acceptance criterion "the sweep run twice returns the same
set" only means anything on a quiescent board, and a disagreement should be
checked against `git status` before it is read as a cap failure. The two runs
recorded above were taken over a board that stayed still.

## Finding 5 — two fixture defects worth carrying forward as method

Both were caught by the probe reddening on its own fixtures, not on the code
under test, and both are the same shape as the bug this PRD exists to fix.

- **A shared counter file under-reports concurrency.** Measuring peak
  parallelism by appending to one file and truncating it from twelve processes
  races with itself. One file per running process, counted by listing the
  directory, is the measurement that holds.
- **A port holder with `listen(1)` reads as *free*.** An unaccepted connection
  fills a backlog of one, and the next connect is then refused — so `port_busy`
  reports the port free while it is very much held. Any future test that holds a
  port must accept and close in a loop. This is a real caveat on `port_busy`
  itself, though not one that bites the harnesses, whose real servers accept.

## Notes on the record and the route

- The knowledge query returned 11 hits, 7 strong, and enqueued no gap into
  `.pearde/wiki/pending/` — nothing new was needed from it, and one fact was
  written back to it.
- `probe-then-spec` fit without amendment and all five of its steps were taken
  in order, including `capture-the-harness-baseline`, which is the only reason
  the 8 to 1 claim above can be made at all. No new workflow is drafted and no
  recurring job here lacks a file.
- `python3 resources/index.py check` and `python3 resources/memos.py check` are
  both silent.
- `references/parts/workers.md`, `resources/board/brief.py`, `collect.py` and
  `init.py` are modified in the working tree by other sessions. Not mine, not
  touched.

## Scores

complexity: 18
blast-radius: mid
workflow: probe-then-spec
