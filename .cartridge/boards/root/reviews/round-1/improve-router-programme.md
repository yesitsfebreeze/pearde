---
kind: work
description: "Deliver the three Router improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-router-route-explanation](../../../router/prds/improve-router-route-explanation/prd.md)"
  - "[improve-router-capability-routing](../../../router/prds/improve-router-capability-routing/prd.md)"
  - "[improve-router-cost-latency](../../../router/prds/improve-router-cost-latency/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning router improvements", "reviewing router cartridge readiness"]
---

# Router improvement plan

## Outcome

Deliver the three improvements requested for Router, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Explain why a provider was selected | [improve-router-route-explanation](../../../router/prds/improve-router-route-explanation/prd.md) |
| 2. Require compatible model capabilities before fallback | [improve-router-capability-routing](../../../router/prds/improve-router-capability-routing/prd.md) |
| 3. Report attributable route cost and latency estimates | [improve-router-cost-latency](../../../router/prds/improve-router-cost-latency/prd.md) |

## Downside coverage

1. Providers expose different capabilities: gate routes by explicit requirements.
2. Fallback changes quality: report actual provider/model and reject incompatible fallback.
3. Credentials/catalogs age: attach timestamps and redact secrets from diagnostics.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [the-router-ranks-and-recovers](../../prds/the-router-ranks-and-recovers/prd.md). Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Router behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test router
just check router
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
