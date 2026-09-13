---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memory
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-memory-owner-access
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
- /Users/feb/dev/cartridge/memory.ctg/src/transport/src
- /Users/feb/dev/cartridge/memory.ctg/src/commands/src
- /Users/feb/dev/cartridge/memory.ctg/tests/cartridge.rs
- /Users/feb/dev/cartridge/memory.ctg/CARTRIDGE.md
---

# Query a memory store through its existing owner

Two legitimate cartridge clients can query one store without acquiring competing writer locks or stopping the owner.

## Acceptance

- [ ] With one process owning a temporary store, a second authorized client retrieves a seeded fact; no second writer starts.
- [ ] Owner crash, stale endpoint, canonical path alias and mismatched store identity produce bounded, explicit outcomes without deleting locks or replaying uncertain ingestion.

- [ ] Keep the current exclusive-writer invariant and existing on-disk formats. On attachment/readiness failure return an explicit error; reverting the adapter must not require rewriting the store. Any schema addition needs a backwards-compatible reader and a tested migration boundary.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs), [cartridge.rs](../../../../../../memory.ctg/tests/cartridge.rs), [CARTRIDGE.md](../../../../../../memory.ctg/CARTRIDGE.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-owner-access`; maximum five rounds.
