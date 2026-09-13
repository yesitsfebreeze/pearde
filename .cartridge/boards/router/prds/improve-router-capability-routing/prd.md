---
repo: /Users/feb/dev/cartridge/router.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: router
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-router-capability-routing
footprint:
- /Users/feb/dev/cartridge/router.ctg/frontier.rs
- /Users/feb/dev/cartridge/router.ctg/catalog.rs
- /Users/feb/dev/cartridge/router.ctg/health.rs
- /Users/feb/dev/cartridge/router.ctg/protocol.rs
- /Users/feb/dev/cartridge/router.ctg/settings.rs
---

# Require compatible model capabilities before fallback

A request requiring tools, vision, context size or wire features routes only to a known-compatible provider or fails explicitly.

## Acceptance

- [ ] A tool/vision request never falls back to an incompatible fixture provider; no compatible provider yields a clear no-route error.
- [ ] Provider changes preserve required wire features; stale/unknown catalog values are distinguishable from confirmed support.

- [ ] Retain local credential ownership and avoid live provider calls in ordinary tests. New metadata is additive; routing requirements fail explicitly rather than silently downgrade. Roll back rules while preserving actual-attempt traces.

## Proof and recovery

Start at [frontier.rs](../../../frontier.rs), [catalog.rs](../../../catalog.rs), [health.rs](../../../health.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test router` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-router-capability-routing`; maximum five rounds.
