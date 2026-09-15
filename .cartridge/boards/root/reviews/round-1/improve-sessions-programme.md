---
kind: work
description: "Deliver the three Sessions improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-sessions-client-mapping](../../../sessions/prds/improve-sessions-client-mapping/prd.md)"
  - "[improve-sessions-retention](../../../sessions/prds/improve-sessions-retention/prd.md)"
  - "[improve-sessions-recovery](../../../sessions/prds/improve-sessions-recovery/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning sessions improvements", "reviewing sessions cartridge readiness"]
---

# Sessions improvement plan

## Outcome

Deliver the three improvements requested for Sessions, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Map client conversations to cartridge sessions honestly | [improve-sessions-client-mapping](../../../sessions/prds/improve-sessions-client-mapping/prd.md) |
| 2. Preview and apply safe session retention | [improve-sessions-retention](../../../sessions/prds/improve-sessions-retention/prd.md) |
| 3. Explain session damage and narrowly repair eligible snapshots | [improve-sessions-recovery](../../../sessions/prds/improve-sessions-recovery/prd.md) |

## Downside coverage

1. Codex and cartridge sessions can diverge: map external identity only when supplied through a trusted channel.
2. Stored transcripts need retention: preview and pin before deletion.
3. Session identity does not restore external effects: recovery must expose unknown outcomes.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [sub-agent-sessions-record-parent-and-mailbox](../../../sessions/prds/sub-agent-sessions-record-parent-and-mailbox/prd.md), [the-board-is-channels-of-lines](../../../sessions/prds/the-board-is-channels-of-lines/prd.md). Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Sessions behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test sessions
just check sessions
just test mcp
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
