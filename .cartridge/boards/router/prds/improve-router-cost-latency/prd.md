---
repo: /Users/feb/dev/cartridge/router.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: router
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-router-cost-latency
needs:
- '@router/improve-router-route-explanation'
footprint:
- src/catalog.rs
- src/decision.rs
- src/proxy.rs
- src/telemetry.rs
- src/main.rs
- .cartridge/tests/unit/proxy/capabilities.rs
- .cartridge/tests/unit/telemetry.rs
- .cartridge/docs/cost-latency.md
commit: "0a216cb100ea40aa0535509d44c38b16a009b9cc"
---

# Report attributable route cost and latency estimates

Routing diagnostics report observed latency and estimated costs with timestamp, source and unknown values.

## Acceptance

- [x] Fixtures show estimates versus actual usage and record missing pricing as unknown rather than zero.
- [x] A fallback report names both attempts and their costs/durations without double counting; old observations show their age.

- [x] Retain local credential ownership and avoid live provider calls in ordinary tests. New metadata is additive; routing requirements fail explicitly rather than silently downgrade. Roll back rules while preserving actual-attempt traces.

## Proof and recovery

Start at [frontier.rs](../../../frontier.rs), [catalog.rs](../../../catalog.rs), [health.rs](../../../health.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test router` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-router-cost-latency`; maximum five rounds.
