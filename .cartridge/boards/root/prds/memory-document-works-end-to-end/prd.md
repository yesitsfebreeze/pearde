---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: root
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: memory-document-works-end-to-end
---

# Memory's own surface works end to end in a disposable composition

The first end-to-end proof of an owner-shipped surface. Since the transport port (memory.ctg `9cc0f0b`) memory serves `tool.memory` (`query`, `ingest`, `describe`), the `memory` service and `context.memory` on its own socket and ships `.cartridge/help.md`. This slice proves that surface through a real host rather than through a separate document runner. Owner: the root composition's smoke fixture over memory.ctg.

## Acceptance

- [ ] In a disposable profile the host starts memory, `cartridge help` lists it, and `tool.memory` `describe` returns its ops.
- [ ] `ingest` of one fact then `query` recalls it, and the `memory` service `get` with the returned id reads back the same text.
- [ ] With the profile's `config.lua` denying `ingest`, the call is refused and a following `query` finds no such fact.
- [ ] After stopping and restarting memory in the same profile the fact is still recallable; a start with an empty `dir` fails with a named configuration error (`memory config.dir is required` or the host's settings refusal) and creates no bank.

## Proof and recovery

Extend the isolated profile in `/Users/feb/dev/cartridge/.cartridge/tests/integration/smoke.test.ts`, which already composes memory without a model or tick, with a `memory` target, and document it in `.cartridge/memos/routine/cartridge-smoke.md`. Gates from `/Users/feb/dev/cartridge`: `just smoke memory` (to be created by this item) and `just test memory`; not run for this plan. Baseline ([release-status](../../../../../../.cartridge/memos/note/release-status.md)): smoke mcp and proxy fail with `memo inactive`, so run this target alone. No user profile or bank is touched. Nested-board discovery and quality measurement stay with the composed-system gate.

## Dependencies and review

Former needs were dropped, with evidence in [review.md](review.md): the landscape board is dissolved (no landscape.ctg; its fabric graph now lives in `memo.ctg/src/fabric_graph.rs` after cartridge.ctg `939e7d1`); the document runner leaf names starting files that no longer exist; the memory-tool submodule whose parity the third need tested was dropped. 3 of 5 rounds used.
