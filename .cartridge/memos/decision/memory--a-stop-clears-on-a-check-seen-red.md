---
kind: decision
date: 2026-09-09
status: decided
description: an unexpected failure stops the work that raised it, the stop is a line in the record because no process schedules agent work, and only a check observed failing on the same binary may clear it
read_when: "reporting work green again, citing an absent error row as evidence, or asking who pauses and resumes agent work"
---

# a-stop-clears-on-a-check-seen-red

## Decision

An unexpected build, test, deployment or runtime failure stops the feature work
that raised it. Diagnosis, repair and verification go on; unrelated sessions,
lanes and daemons do not stop, and a negative test that fails on purpose is not
a failure and raises nothing. The stop is a line in the record — `status:
blocked` on the memo with the failure as its first question ([[@prd/routine/run-board.md]]) — because
nothing in this tree schedules agent work: `memory plan` computes a `ready` band,
a pass of [[@prd/routine/run-board.md]] reads it and an agent dispatches it, so pause and resume
belong to whoever runs the pass and there is no queue for code to suspend.

One check clears the stop, and it counts only when it has been observed failing
on the same binary and the same surface that will report it passing. An absence
— no error row, a clean log, a green line — is evidence of nothing until the
presence has been produced there once.

## Why

The clause exists because the tree has already been fooled by it. A lane
offered "no fault row in the daemon log" as its evidence of a clean run. The
fault arm that writes those rows landed at 2026-09-08 23:02:46 in `2efe3b69`;
the installed `~/.cargo/bin/memory` was built at 22:05:29, fifty-seven minutes
earlier, and `.memory/daemon.log` had last been written at 13:45 — nine hours
before the arm existed. The log's only line matching `fault` is the word
`default` in a config message. The claim was true, reproducible, and worth
nothing: the binary that wrote that log had no arm that could have emitted the
row whose absence was the proof. A check nothing can fail proves nothing when
it passes, which [[gates]] already demands of a rule-test's red fixture and
[[gates-are-tests]] of every rule the repo enforces on itself; this extends the
same negative control from a gate to any evidence that clears a stop.

## Consequences

- Evidence written as an absence carries the positive control with it: the
  version or commit of the binary observed, and the one observation that proved
  the surface can report the thing being claimed missing. Without it the line
  is not evidence and the stop does not clear.
- A stop is visible on the board, not held in a session's head: the memo carries
  `status: blocked` and the failure, so a pass that never spoke to the failing
  session still sees the queue is stopped and why.
- Overturned the day a process owns the queue — a scheduler that can hold and
  release dispatched work — at which point pause and resume become its state and
  this memo names only what may clear them.
