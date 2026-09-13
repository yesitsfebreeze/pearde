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
canonical-scope: memory-owns-its-tool
needs:
- '@memory/memory-owns-its-tool/memory-consumer-parity'
---

# Retiring the wrapper preserves stores and consumers

Remove only a wrapper proven redundant by the consumer matrix; update profiles, catalog, workspace and links as one compatible migration.

## Acceptance

- [ ] Every recorded consumer points at the surviving implementation.
- [ ] A fresh checkout loads the intended profiles without missing dependency paths.
- [ ] Store bytes and source history are preserved and the compatibility entry can be restored.

## Proof and recovery

Start at [cartridge.rs](../../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-owns-its-tool`; maximum five rounds.
