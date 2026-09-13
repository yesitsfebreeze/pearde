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
canonical-scope: improve-memory-tool-get
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
---

# Retrieve a recalled fact by stable ID

Add exact-ID readback in the surviving memory adapter and use it for Landscape memory references. Preserve query/ingest defaults and validate operation-specific schemas before dispatch; unknown fields are refused and sync is either formally declared or rejected consistently.

## Acceptance

- [ ] Query then get the returned store-qualified ID through a real MCP bridge returns matching text, identity and provenance.
- [ ] Invalid k, oversized text, absent ID, wrong-store ID, unknown field and missing fact have explicit distinct contract errors before unintended work.
- [ ] A old consumer calling unsupported get fails clearly during migration; no semantic second query substitutes for exact readback.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-tool-get`; maximum five rounds.
