---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: memory-health-loads-its-own-graph-beside-the-daemon
---

# memory-health-loads-its-own-graph-beside-the-daemon

Resolve the canonical store owner first and use its bounded health RPC when compatible. Verify that the CLI does not load a second graph with an instrumented fixture counter. With no serving daemon, retain the existing local read-only path; an incompatible/stale endpoint is explicit and cannot bypass writer ownership.

## Acceptance

- [ ] Served and unserved fixtures report equivalent entity/thought/reason counts for the same snapshot.
- [ ] The served path performs zero local graph loads and finishes within its configured RPC deadline; a fixed small local fixture records latency separately from an arbitrary machine-wide promise.
- [ ] Wrong-store endpoint, timeout and owner restart produce explicit status/retryability without deleting locks or starting another writer.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-health-loads-its-own-graph-beside-the-daemon`; maximum five rounds.
