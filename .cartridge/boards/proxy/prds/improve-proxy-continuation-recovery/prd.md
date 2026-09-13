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
canonical-scope: improve-proxy-continuation-recovery
footprint:
- /Users/feb/dev/cartridge/proxy.ctg/service.rs
- /Users/feb/dev/cartridge/proxy.ctg/streaming.rs
- /Users/feb/dev/cartridge/proxy.ctg/wire.rs
- /Users/feb/dev/cartridge/proxy.ctg/tests.rs
- /Users/feb/dev/cartridge/proxy.ctg/README.md
---

# Make continuation lifetime and restart recovery explicit

Clients can distinguish valid, expired and lost-on-restart continuation IDs and recover with full conversation input.

## Acceptance

- [ ] Create a continuation, evict it and restart the fixture proxy: each path returns the documented outcome with no cross-client mapping.
- [ ] Full-input recovery succeeds; any optional durable mode has restart, retention and wrong-profile tests, otherwise the limitation is explicitly retained.

- [ ] Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Proof and recovery

Start at [service.rs](../../../service.rs), [streaming.rs](../../../streaming.rs), [wire.rs](../../../wire.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-proxy-continuation-recovery`; maximum five rounds.
