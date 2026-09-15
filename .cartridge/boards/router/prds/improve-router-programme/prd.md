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

## From the retired work memo

Folded 2026-09-15 from `work/improve-router-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Router improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Router, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Explain why a provider was selected | [improve-router-route-explanation](../improve-router-route-explanation/prd.md) |
| 2. Require compatible model capabilities before fallback | [improve-router-capability-routing](../improve-router-capability-routing/prd.md) |
| 3. Report attributable route cost and latency estimates | [improve-router-cost-latency](../improve-router-cost-latency/prd.md) |

### Downside coverage

1. Providers expose different capabilities: gate routes by explicit requirements.
2. Fallback changes quality: report actual provider/model and reject incompatible fallback.
3. Credentials/catalogs age: attach timestamps and redact secrets from diagnostics.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [the-router-ranks-and-recovers](../../../root/prds/the-router-ranks-and-recovers/prd.md). Their current source, status and owner take precedence over a stale assessment.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Router behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test router
just check router
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
