---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: delivered-pending-verification
canonical-scope: memory-owns-its-tool
needs:
- '@gitfs/tool-results-interoperate'
---

# Memory serves query and ingest through its own adapter

Keep database/CLI ownership in memory and use the existing writer boundary; retain memory-tool forwarding during migration.

## Acceptance

- [ ] Real query/ingest reaches one store writer.
- [ ] The adapter never recursively calls itself through the host.
- [ ] Configured endpoint failure is explicit and standalone CLI behavior remains usable.

## Proof and recovery

Start at [cartridge.rs](../../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-owns-its-tool`; maximum five rounds.
