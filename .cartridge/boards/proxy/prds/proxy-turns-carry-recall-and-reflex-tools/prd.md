---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: proxy
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: proxy-turns-carry-recall-and-reflex-tools
footprint:
- Cargo.toml
- cartridge.json
- src/main.rs
- src/service.rs
- src/context.rs
- src/wire.rs
- src/streaming.rs
- src/usage.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/tests/unit/context.rs
- .cartridge/tests/integration/recall.test.ts
- .cartridge/docs/context.md
needs:
- '@landscape/landscape-composes-system-context/context-contributor-contract'
- '@landscape/landscape-composes-system-context/memory-context-contributor'
- '@memo/landscape-context-facade'
commit: "9ddcc08807a059579c21227ad9d3523d242ddf86"
---

# proxy-turns-carry-recall-and-reflex-tools

Move bounded context preparation into proxy/harness consuming Landscape; memory supplies source-labelled query/readback only. Keep client-owned history/tools and native wire framing. Optional context failure yields an explicit degraded observation while forwarding the original valid request.

## Acceptance

- [x] A fixture request receives relevant bounded memory context once with provenance and no elevation to system authority.
- [x] Missing memory/selection failure preserves client streaming, cancellation and provider error semantics without a nested agent loop.
- [x] Tool preparation cannot expand profile grants or hide required client tools; the same selected snapshot is inspectable without an inference call.

## Proof and recovery

Start at [service.rs](../../../../../../proxy.ctg/src/service.rs), [streaming.rs](../../../../../../proxy.ctg/src/streaming.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 3 independent agent review](review.md). Inherits round 1 from `proxy-turns-carry-recall-and-reflex-tools`; maximum five rounds.
