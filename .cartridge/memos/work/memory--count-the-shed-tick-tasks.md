---
kind: work
level: 10
status: done
description: a tick task dropped by a full queue is counted and surfaced, so a saturated pulse stops looking like a draining backlog
read_when: "reading the `degraded:` line, or asking what a full tick queue costs"
---

# count-the-shed-tick-tasks

Carries `the-tick-queue-is-permanently-full`.

## Do

`Queue::enqueue` already returns `false` on a full channel and no caller reads
it. Count that path on the queue itself — the same object that owns
`pending`, `inflight` and the latency stats — and surface the number the way
every other degradation is surfaced: a field on `HealthRes`
(`src/transport/src/memory_rpc.rs`), read in `src/rpc/src/server.rs`, printed on
the `degraded:` line in `src/commands/src/commands_admin.rs` beside panics and
failures.

Do not raise `TICK_QUEUE_CAPACITY` and do not make `enqueue` block: a bigger
buffer in front of a consumer that is slower than its producer only moves the
loss, and blocking the pulse on a full queue would hold whatever the pulse
holds. Shedding maintenance is the correct behaviour under saturation — being
unable to tell that it happened is the defect.

The counter belongs to the store, not the process — the health counters
moved onto `graph::graph::Counters` in [[@prd/work/memory--per-store-health-counters.md]]; the
queue is per store too, so the count sits on the `Queue` beside `cadence`.

## Check

A unit test in `src/tick/src/tests/tick_queue_test.rs` fills a `Queue::new(1)`,
enqueues once more, and reads the shed count as 1; `memory health` on a store
whose queue is full prints a non-zero shed count on the `degraded:` line.

The count landed on main (`tick_queue.rs` `shed`, `HealthRes.tasks_shed`,
the `degraded:` clause) with the unit test and the printer test green; the
second half — a non-zero count on the saturated project store — is what
closes this once the installed daemon carries it.
