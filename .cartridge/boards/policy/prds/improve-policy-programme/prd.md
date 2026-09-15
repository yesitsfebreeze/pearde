---
repo: /Users/feb/dev/cartridge/policy.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: policy
work-kind: rollup
review-round: 3
review-status: needs-decision
canonical-scope: improve-policy-programme
needs:
- '@policy/improve-policy-operation-rules'
- '@policy/improve-policy-resource-scope'
- '@policy/improve-policy-explain'
---

# Policy improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Authorize individual operations with stable precedence](../improve-policy-operation-rules/prd.md)
- [Constrain granted file operations to declared resources](../improve-policy-resource-scope/prd.md)
- [Explain the effective policy without executing a tool](../improve-policy-explain/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-policy-programme`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-policy-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Policy improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Policy, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Authorize individual operations with stable precedence | [improve-policy-operation-rules](../improve-policy-operation-rules/prd.md) |
| 2. Constrain granted file operations to declared resources | [improve-policy-resource-scope](../improve-policy-resource-scope/prd.md) |
| 3. Explain the effective policy without executing a tool | [improve-policy-explain](../improve-policy-explain/prd.md) |

### Downside coverage

1. Tool-wide rules are coarse: use explicit operation matching.
2. Codex and cartridge permissions differ: explain both boundaries without weakening either.
3. Policy is not a sandbox: preserve the separate runtime isolation work and state the enforcement boundary.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [headless-policy-approval-channel](../../../root/prds/headless-policy-approval-channel/prd.md). Their current source, status and owner take precedence over a stale assessment.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Policy behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test policy
just check policy
just smoke policy
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
