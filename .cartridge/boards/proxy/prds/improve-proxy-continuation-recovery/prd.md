---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: proxy
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-proxy-continuation-recovery
footprint:
- src/main.rs
- src/service.rs
- src/streaming.rs
- src/continuation.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/docs/continuations.md
commit: "0c9d4e9bd2bb7fef98dd1bc2f593f314b7a090e2"
---

# Make continuation lifetime and restart recovery explicit

Clients can distinguish valid, expired and lost-on-restart continuation IDs and recover with full conversation input.

## Acceptance

- [x] Create a continuation, evict it and restart the fixture proxy: each path returns the documented outcome with no cross-client mapping.
- [x] Full-input recovery succeeds; any optional durable mode has restart, retention and wrong-profile tests, otherwise the limitation is explicitly retained.

- [x] Keep native request/response wire semantics and caller-owned conversation history. New telemetry is opt-in/additive and bounded. Reverting continuation changes must report invalid mappings rather than resolve to the wrong provider/client.

## Proof and recovery

Start at owner-local `src/service.rs`, `src/streaming.rs` and `src/wire.rs`. See [bounded specification](specs/spec01.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test proxy` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-proxy-continuation-recovery`; maximum five rounds.
