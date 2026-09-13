---
kind: work
description: "Deliver the three Policy improvements with explicit risk coverage"
status: open
subwork:
  - "[[@prd/work/root--improve-policy-operation-rules.md]]"
  - "[[@prd/work/root--improve-policy-resource-scope.md]]"
  - "[[@prd/work/root--improve-policy-explain.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["planning policy improvements", "reviewing policy cartridge readiness"]
---

# Policy improvement plan

## Outcome

Deliver the three improvements requested for Policy, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Authorize individual operations with stable precedence | [[@prd/work/root--improve-policy-operation-rules.md]] |
| 2. Constrain granted file operations to declared resources | [[@prd/work/root--improve-policy-resource-scope.md]] |
| 3. Explain the effective policy without executing a tool | [[@prd/work/root--improve-policy-explain.md]] |

## Downside coverage

1. Tool-wide rules are coarse: use explicit operation matching.
2. Codex and cartridge permissions differ: explain both boundaries without weakening either.
3. Policy is not a sandbox: preserve the separate runtime isolation work and state the enforcement boundary.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [[@prd/work/root--headless-policy-approval-channel.md]]. Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Policy behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test policy
just check policy
just smoke policy
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
