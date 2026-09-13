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
canonical-scope: improve-memory-tool-errors
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
footprint:
- /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
---

# Return actionable memory failures and enforce the tool schema

Translate engine outcomes once in the memory-owned adapter under the existing string-content/error wire. Publish codes for invalid input, incompatible/contended owner, unavailable dependency and refused/committed/unknown ingestion; preserve call identity and safe details.

## Acceptance

- [ ] Invalid arguments invoke no engine operation; contention and model timeout remain distinct errors through real MCP/proxy consumers.
- [ ] A store commit followed by response failure reports unknown or committed according to actual evidence and offers exact readback, not automatic retry.
- [ ] Query/ingest compatibility and profile exposure stay unchanged across wrapper retirement; errors never become successful empty recall.

## Proof and recovery

Start at [cartridge.rs](../../../../../../memory.ctg/src/cartridge.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just check` and `just test` from memory.ctg with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-tool-errors`; maximum five rounds.
