---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 4
review-status: passed
canonical-scope: every-mutation-holds-the-store-writer-boundary
commit: "a124fd30d59bcd06062b5464810188a0288e461e"
---

# every-mutation-holds-the-store-writer-boundary

Enumerate every current graph mutation entry point from CLI, daemon, cartridge adapter and maintenance operations. Each path holds exclusive writer ownership from load/attach through commit, using the existing canonical store lock. The output is a mutation census with regression tests for any discovered gap, not a new tombstone/merge subsystem.

## Acceptance

- [x] Two competing processes released at a barrier cannot both commit to one store; the loser changes no bytes.
- [x] A stale local snapshot cannot resurrect a row removed by the owner, including after a crash/restart boundary.
- [x] Tests cover each enumerated mutation entry or a shared proven boundary, with exact current commands and source revisions; read-only operations remain usable under their existing contract.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `every-mutation-holds-the-store-writer-boundary`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--every-mutation-holds-the-store-writer-boundary.md` (status open, estimate 1d). The PRD state above is authoritative.

> all graph mutations route to the daemon or retain the writer lock from load through commit

### Do

Every graph mutation has exactly one store writer: the serving daemon, or a
local caller retaining writer ownership before load until commit. A competing
mutation refuses without writing; a holder check alone is not ownership.
A stale unrelated mutation cannot resurrect a removed row. Existing daemon
routing and lock primitives remain the boundary, without a new tombstone set,
base-image merge or per-process removed-ID workaround.

This implements [[does-a-removal-need-a-tombstone]] for
[the-graph-converges](../the-graph-converges/prd.md). Bitemporal claim retirement remains distinct from
physical cleanup.
