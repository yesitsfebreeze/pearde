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
canonical-scope: improve-memory-tool-correct
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
---

# Correct or forget one identified fact through the tool boundary

Place the implementation in memory's surviving adapter, after exact get and operation policy. Split correction and forget into separately reviewable specs; both identify a fact and expected revision. Correction is one atomic engine operation preserving source history; forget follows the existing engine's deletion/tombstone semantics, documented before exposure.

## Acceptance

- [ ] A stale correction or wrong-store ID leaves all facts unchanged; valid correction returns the exact new identity/revision and retained provenance.
- [ ] Forget affects only the reviewed ID and explicitly authorized dependent effects; no bulk deletion is inferred.
- [ ] Retry after unknown completion performs exact status/readback reconciliation and never blindly repeats a mutation. New operations remain opt-in throughout wrapper migration.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-tool-correct`; maximum five rounds.
