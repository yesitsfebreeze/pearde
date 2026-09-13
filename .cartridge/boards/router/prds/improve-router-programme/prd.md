---
repo: /Users/feb/dev/cartridge/router.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: router
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-router-programme
footprint:
  - .cartridge/docs/capabilities.md
  - .cartridge/docs/cost-latency.md
  - .cartridge/docs/decisions.md
  - .cartridge/tests/unit/catalog/capabilities.rs
  - .cartridge/tests/unit/proxy/capabilities.rs
  - .cartridge/tests/unit/sync/tests.rs
  - .cartridge/tests/unit/telemetry.rs
  - Cargo.toml
  - src/catalog.rs
  - src/decision.rs
  - src/main.rs
  - src/proxy.rs
  - src/requirements.rs
  - src/sync.rs
  - src/telemetry.rs
needs:
- '@router/improve-router-route-explanation'
- '@router/improve-router-capability-routing'
- '@router/improve-router-cost-latency'
commit: "4ad9cd35dc862ecfe0786612d39913612d93fc45"
---

# Router improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [x] Each linked leaf passes its own review and observable acceptance.
- [x] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Explain why a provider was selected](../improve-router-route-explanation/prd.md)
- [Require compatible model capabilities before fallback](../improve-router-capability-routing/prd.md)
- [Report attributable route cost and latency estimates](../improve-router-cost-latency/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-router-programme`; maximum five rounds.
