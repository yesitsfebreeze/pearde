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
canonical-scope: improve-router-route-explanation
needs:
- '@router/improve-router-capability-routing'
footprint:
- Cargo.toml
- src/main.rs
- src/catalog.rs
- src/requirements.rs
- src/proxy.rs
- src/decision.rs
- .cartridge/tests/unit/proxy/capabilities.rs
- .cartridge/tests/unit/catalog/capabilities.rs
- .cartridge/docs/decisions.md
commit: "07b77ff754ab740a1efb01dfade7e3fc953c204d"
---

# Explain why a provider was selected

Each routing decision exposes chosen model, candidates, rejection reasons and the policy/catalog revision used.

## Acceptance

- [x] Fixture candidates rejected for health, capacity and capability have distinct reasons; the selected model matches execution.
- [x] Explanations omit tokens, headers and credential values and retain actual fallback identity.

- [x] Retain local credential ownership and avoid live provider calls in ordinary tests. New metadata is additive; routing requirements fail explicitly rather than silently downgrade. Roll back rules while preserving actual-attempt traces.

## Proof and recovery

Start at [frontier.rs](../../../frontier.rs), [catalog.rs](../../../catalog.rs), [health.rs](../../../health.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test router` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-router-route-explanation`; maximum five rounds.
