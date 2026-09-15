---
kind: work
description: "Deliver the three Proxy improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-proxy-total-usage](../../../proxy/prds/improve-proxy-total-usage/prd.md)"
  - "[improve-proxy-tool-trace](../../../proxy/prds/improve-proxy-tool-trace/prd.md)"
  - "[improve-proxy-continuation-recovery](../../../proxy/prds/improve-proxy-continuation-recovery/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning proxy improvements", "reviewing proxy cartridge readiness"]
---

# Proxy improvement plan

## Outcome

Deliver the three improvements requested for Proxy, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Account for every internal model round consistently | [improve-proxy-total-usage](../../../proxy/prds/improve-proxy-total-usage/prd.md) |
| 2. Inspect internal proxy tool work by request identity | [improve-proxy-tool-trace](../../../proxy/prds/improve-proxy-tool-trace/prd.md) |
| 3. Make continuation lifetime and restart recovery explicit | [improve-proxy-continuation-recovery](../../../proxy/prds/improve-proxy-continuation-recovery/prd.md) |

## Downside coverage

1. Internal rounds are hidden: offer an attributable trace without corrupting the public wire.
2. Extra rounds add latency/failure modes: bound and account for every attempt.
3. Continuation IDs expire: report lifetime and test explicit recovery rather than assuming durability.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Review current source and active ownership before implementation; the assessment does not reserve files.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Proxy behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test proxy
just check proxy
just smoke proxy
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
