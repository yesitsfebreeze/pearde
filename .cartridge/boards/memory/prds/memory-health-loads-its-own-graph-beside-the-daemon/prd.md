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
commit: "439bea56749d6a7361d6c1afb7d1a43bb46c7e9f"
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
