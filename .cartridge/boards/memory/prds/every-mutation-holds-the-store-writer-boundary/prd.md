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
commit: "0a7c4a1f729c700f52c650ee0c3efc56a136560f"
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
