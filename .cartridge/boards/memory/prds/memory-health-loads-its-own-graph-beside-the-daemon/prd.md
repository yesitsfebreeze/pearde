---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: "passed"
canonical-scope: memory-health-loads-its-own-graph-beside-the-daemon
needs: ["@memory/every-mutation-holds-the-store-writer-boundary"]
commit: "a124fd30d59bcd06062b5464810188a0288e461e"
---

# memory-health-loads-its-own-graph-beside-the-daemon

Resolve the canonical store owner first and use its bounded health RPC when compatible. Verify that the CLI does not load a second graph with an instrumented fixture counter. With no serving daemon, retain the existing local read-only path; an incompatible/stale endpoint is explicit and cannot bypass writer ownership.

## Acceptance

- [x] Served and unserved fixtures report equivalent entity/thought/reason counts for the same snapshot.
- [x] The served path performs zero local graph loads and finishes within its configured RPC deadline; a fixed small local fixture records latency separately from an arbitrary machine-wide promise.
- [x] Wrong-store endpoint, timeout and owner restart produce explicit status/retryability without deleting locks or starting another writer.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-health-loads-its-own-graph-beside-the-daemon`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--memory-health-loads-its-own-graph-beside-the-daemon.md` (status open, claim session-adcf486f 2026-09-09 02:42, estimate 1h). The PRD state above is authoritative.

> `cmd_health` calls `load_graph` before it asks the daemon anything, so `memory health` pays a full store load — 85 s on the record — even when a daemon serving that store already holds every count it prints

`commands_health.rs` opens with `let g = load_graph(cfg);` and only then calls
`daemon_health()`. So `memory health` against a store a daemon is already
serving builds a second whole graph in the CLI process — 85 s on the record,
measured 2026-09-09 beside a warm daemon — to print counts the daemon holds in
RAM. The daemon's own lines (queues, presets, degradation) already come over
RPC; only the store stats take the slow road.

Found while checking
[a-lane-daemon-pays-twelve-minutes-to-open-its-eyes](../a-lane-daemon-pays-twelve-minutes-to-open-its-eyes/prd.md), whose Check names
`memory health` as the probe for a daemon being up and cannot distinguish the
daemon's 82 s boot from the CLI's own load. It is the same load
[[every-cli-invocation-pays-a-minute]] measured, here with a daemon standing
right next to it holding the answer.

### Do

When a daemon answers for this store, take the entity, memory and reason counts
from it over RPC and skip `load_graph`. No daemon serving keeps the current
in-process path — a read-only CLI on a store nobody serves has no other
source.

### Check

`memory health` against a served store answers in under a second and prints the
same memory, thought and reason counts as the in-process path on the same store;
against an unserved store it still answers with the counts.
