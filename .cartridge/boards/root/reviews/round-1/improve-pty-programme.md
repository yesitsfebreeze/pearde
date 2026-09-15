---
kind: work
description: "Deliver the three PTY and shared shell improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-pty-shell-identity](../../../pty/prds/improve-pty-shell-identity/prd.md)"
  - "[improve-pty-input-ownership](../../../pty/prds/improve-pty-input-ownership/prd.md)"
  - "[improve-pty-command-wait](../../../pty/prds/improve-pty-command-wait/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning pty improvements", "reviewing pty cartridge readiness"]
---

# PTY and shared shell improvement plan

## Outcome

Deliver the three improvements requested for PTY and shared shell, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Return explicit shell and working-directory identity | [improve-pty-shell-identity](../../../pty/prds/improve-pty-shell-identity/prd.md) |
| 2. Coordinate human and agent input on the shared terminal | [improve-pty-input-ownership](../../../pty/prds/improve-pty-input-ownership/prd.md) |
| 3. Wait and retrieve output for one terminal command | [improve-pty-command-wait](../../../pty/prds/improve-pty-command-wait/prd.md) |

## Downside coverage

1. Human/agent input can collide: explicit ownership and human preemption.
2. Terminal screens are less structured than command results: publish phase, IDs and shell metadata.
3. Output tails can omit evidence: expose truncation and bounded command-output retrieval.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [sub-agents-share-the-terminal](../../../agent/prds/sub-agents-share-the-terminal/prd.md), [pty-encodes-input](../../prds/pty-encodes-input/prd.md). Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated PTY and shared shell behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test pty
just check pty
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
