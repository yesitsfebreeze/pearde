---

kind: work
level: 10
status: done
estimate: 4h
description: "`crossings_in_flight()` counts every live blocking crossing into the async world, and its only three readers are the shutdown drain and two tests — so the watchdog exits guessing \"graph deadlock or worker starvation\" while the number that distinguishes them sits in the same process"
read_when: "debugging a watchdog exit, or adding a health counter"
---

# the-number-that-names-the-stall-is-computed-and-unread

## Do

Every crossing from sync code into a future goes through
`llm::block_on_in_place`, which takes a guard first:
`let _crossing = util::lifecycle::crossing();` (`src/llm/src/llm.rs:538`).
`crossing()` increments an atomic and the guard decrements it on drop
(`src/util/src/lifecycle.rs:138-150`), so `crossings_in_flight()` (`:153-155`)
is, at any instant, exactly how many workers are parked inside a blocking
bridge.

`rg -n crossings_in_flight src tests` answers four lines beyond the definition:
`drain_crossings` at `:164` and `:167`, which is the shutdown wait;
`lifecycle_test.rs:126`; and `tests/tick_shutdown.rs:167`. **No live surface
reads it.** It is absent from `health`, from the `degraded:` line
(`src/commands/src/commands_health.rs:161-171`), and from the watchdog.

The watchdog is where it is missed. On thirty seconds of the 1-second heartbeat
not advancing it prints "async runtime stalled ~{}s (graph deadlock or worker
starvation)" and exits 101 (`commands/src/commands_serve.rs:442-478`) — a guess between
two causes that the atomic separates outright: crossings at or near the worker
count is starvation, crossings at zero is a lock. The denominator is missing
too, and for the same reason: `workers` is a local in `main`
(`src/main.rs:53`), computed and never stored.

It is one number, not an instrumentation gap. Swept 2026-09-06: all twelve
per-store counters in `graph::Counters` reach a printed surface — six on
`degradation_lines`' `degraded:` line, six more on `tick_health_lines`' own
(`src/commands/src/commands_health.rs:203-212`), with `ingest_tombstoned`
deliberately on a line
of its own and `ingest_hygiene_rejected` in the health JSON
(`server.rs:249`). Outside that system there are five process-global atomics;
two are flags, and of the three that are metrics, `SHUTDOWN_REFUSED` is
published as `llm_shutdown_refused` (`server.rs:332`) and `STARTED_AT_MS` as
`uptime_ms` on the wire. `IN_FLIGHT` is the only one with no surface — and it
is minted in the same function as `SHUTDOWN_REFUSED`, `block_on_in_place_counting`
(`llm.rs:527-545`), five lines apart.

A stall that ends in this exit leaves nothing in the log to say which half of
the message applied. And the worker floor of 4 in `src/main.rs` names its
blocking bridges by hand while nothing counts them.

Publish both numbers. `crossings_in_flight()` and the runtime's worker count
join the `degraded:` line when the crossings are non-zero, the way
[[@prd/work/memory--count-the-shed-tick-tasks.md]] put `Queue::shed` there; and the watchdog's exit
message carries both instead of naming two causes, so the next stall says which
it was in the line it dies on.

**Done 2026-09-08.** `set_worker_threads` / `worker_threads` live beside
`IN_FLIGHT` in `src/util/src/lifecycle.rs`, published once by `main` where the
number was a local; `crossings_in_flight` and `worker_threads` cross the wire on
`HealthRes`, are emitted from `health_stats` next to `watchdog_restarts`, and
print as `crossings:   N blocking bridges in flight of M runtime workers` from
`crossing_health_lines` (`src/commands/src/commands_admin.rs`). That line is
unconditional where the `Do` said "when the crossings are non-zero": a gauge
read only once the process is stalled has no healthy reading to be compared
against, and it follows `ingest_health_lines` — daemon-sourced, absent when
nothing serves. The watchdog exit now reads
`async runtime stalled ~30s (N blocking crossings in flight of M runtime
workers)`.

## Check

`memory health` prints the live crossing count against the worker count, a
watchdog exit line names both numbers rather than "graph deadlock or worker
starvation", and `just all` is green.
