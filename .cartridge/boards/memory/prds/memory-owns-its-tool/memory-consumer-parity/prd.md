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
review-status: superseded-recommend-retire
canonical-scope: memory-owns-its-tool
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
- '@memory/improve-memory-tool-get'
- '@memory/improve-memory-tool-errors'
---

# Old and new consumers see one compatible memory tool

Test a pinned mixed-version matrix through the surviving adapter and compatibility forwarding entry.

## Acceptance

- [ ] Old/new query and ingest decode identically.
- [ ] Default and MCP expose exactly one tool while proxy retains its existing operation exposure.
- [ ] Old consumers refuse unsupported operations explicitly with no store mutation.

## Proof and recovery

Start at [cartridge.rs](../../../../../../../memory.ctg/src/cartridge.rs), [main.rs](../../../../../../../memory.ctg/src/main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-owns-its-tool`; maximum five rounds.
