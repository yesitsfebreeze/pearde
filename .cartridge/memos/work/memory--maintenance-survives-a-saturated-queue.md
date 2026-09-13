---
kind: work
level: 10
status: done
description: a full tick queue drops 84 tasks for every one it runs, so every consolidating task is lost exactly when the load that needs it arrives
read_when: "executing the convergence plan, or touching the tick queue"
---

# maintenance-survives-a-saturated-queue

Carries the half [[@prd/work/memory--count-the-shed-tick-tasks.md]] measured but did not fix, under
[[@prd/work/memory--the-graph-converges.md]].

## Do

`Queue::enqueue` (`src/tick/src/tick_queue.rs:123`) rolls back its pending
marker, counts a shed and returns `false` when the 512-slot channel
(`TICK_QUEUE_CAPACITY`, `src/base/src/base_constants.rs:29`) is full. Measured
on this store 2026-09-06: `queue 512 | done 179` against `15054 shed` — 84
dropped for every one finished, with arrivals at 8/s and tasks averaging
1028 ms. Shedding is correct under saturation
(`the-tick-queue-is-permanently-full` argues that and this does not reopen it).
What is wrong is that shedding is *undifferentiated*: `Persist` and
`StigmergyGc` are dropped on the same coin-flip as the `Name` call that wants
an LLM round trip, so the cheap work that keeps the store coherent dies with
the expensive work that made the queue full.

**Ranking alone does not close it.** The pulse spends the hourly cadence slot
before it offers the task and never reads the `false` a shed returns
(`the-hourly-slot-is-spent-even-when-the-task-is-shed`), so a `StigmergyGc`
that loses a rank contest has still consumed its interval. Roll the cadence cell
back on a failed enqueue in the same change; it is one line at each of the two
pulse sites.

Give `TaskKind` a rank and shed by it: when `try_send` fails, drop only tasks
at or below the rank of the arrival, and let a higher-ranked task displace a
queued lower one. Rank by what a loss costs, not by what a task costs to run —
`Persist` and `StigmergyGc` above `Enrich`, `Name` and `SeedQuestions`, which
are re-enqueued by the next pulse anyway (`tick_pulse.rs:36-111`).

Do not raise the capacity and do not block the pulse: both were refused in
[[@prd/work/memory--count-the-shed-tick-tasks.md]] and the refusal stands. This is about which task
dies, never about how many.

## Check

A unit test in `src/tick/src/tests/tick_queue_test.rs` fills a `Queue::new(1)`
with a low-ranked task, enqueues a high-ranked one, and reads the high-ranked
one back off the channel with the shed count at 1. On this store, `memory health`
under the same load reports a non-zero shed count while `Persist` faults stay
at zero.

Landed 2026-09-06 in `d5d5ca62`: `TaskKind::rank` (persist, GC, consolidation
and the idle sweep at 2; the access ledger, propagation and reembed at 1; the
six LLM tasks at 0), `Queue` a deque behind the same `Receiver` API, an
arrival displacing the newest queued task of a lower rank or shed itself, and
`claim_slot` handing back the stamp it replaced so all three pulse sites
restore it when their enqueue is shed. The unit half of the Check passes in
`tick_queue_test.rs` (`Queue::new(1)`, low then high, high read back, shed 1)
and `tick_pulse_test.rs` (a shed sweep spends no interval). The live half —
`memory health` under load with shed non-zero and `Persist` faults at zero —
is not run: it needs the binary installed as `~/.cargo/bin/memory`, and this tree
is mid-edit by another session, so an install would hand every daemon a build
that is not this commit. Blocked on that install.

**Unblocked 2026-09-07.** The install this part waited on has happened:
`~/.cargo/bin/memory` is `memory 2.0.0`, written 10:53 today, after every commit
that carries `TaskKind::rank` — `d5d5ca62` is an ancestor of `41275c65` and the
rank stands at `tick_queue.rs:39-53` — and the trunk is clean, so no session is
holding the tree mid-edit. This part was never blocked on
`does-a-merge-cross-origins` either, whatever [[@prd/work/memory--the-graph-converges.md]] says of
both its children ([[the-convergence-block-outlived-its-question]]).

What is left of the `Check` is one run, not one install. `memory health` already
prints the counter it reads — the `degraded:` line ends `0 shed by a full queue`
— but those counters are per process, so a CLI invocation reads its own zeros
(measured 2026-09-07 11:15: `tick: queue 166 | done 8`, every degraded counter
at 0). The live half needs the daemon up and under the load that made the queue
full, then that same line read for a non-zero shed against zero `Persist`
faults.
