---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: proxy
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-proxy-total-usage
needs:
- '@gitfs/tool-results-interoperate'
footprint:
- /Users/feb/dev/cartridge/proxy.ctg/service.rs
- /Users/feb/dev/cartridge/proxy.ctg/streaming.rs
- /Users/feb/dev/cartridge/proxy.ctg/wire.rs
- /Users/feb/dev/cartridge/proxy.ctg/tests.rs
- /Users/feb/dev/cartridge/proxy.ctg/README.md
---

# Account for every internal model round consistently

JSON and streaming responses provide consistent total usage across internal tool rounds, with final-round usage separately identified.

## Acceptance

- [ ] A three-round fixture reports matching cumulative totals for JSON and SSE and no double counting of final events.
- [ ] Missing usage, partial stream failure and cancellation preserve known totals and label incomplete accounting.

- [ ] Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Proof and recovery

Start at [service.rs](../../../service.rs), [streaming.rs](../../../streaming.rs), [wire.rs](../../../wire.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-proxy-total-usage`; maximum five rounds.
