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
canonical-scope: improve-router-route-explanation
footprint:
- /Users/feb/dev/cartridge/router.ctg/frontier.rs
- /Users/feb/dev/cartridge/router.ctg/catalog.rs
- /Users/feb/dev/cartridge/router.ctg/health.rs
- /Users/feb/dev/cartridge/router.ctg/protocol.rs
- /Users/feb/dev/cartridge/router.ctg/settings.rs
---

# Explain why a provider was selected

Each routing decision exposes chosen model, candidates, rejection reasons and the policy/catalog revision used.

## Acceptance

- [ ] Fixture candidates rejected for health, capacity and capability have distinct reasons; the selected model matches execution.
- [ ] Explanations omit tokens, headers and credential values and retain actual fallback identity.

- [ ] Retain local credential ownership and avoid live provider calls in ordinary tests. New metadata is additive; routing requirements fail explicitly rather than silently downgrade. Roll back rules while preserving actual-attempt traces.

## Proof and recovery

Start at [frontier.rs](../../../frontier.rs), [catalog.rs](../../../catalog.rs), [health.rs](../../../health.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test router` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-router-route-explanation`; maximum five rounds.
