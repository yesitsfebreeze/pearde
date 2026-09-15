---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-sessions-programme
needs:
- '@sessions/improve-sessions-client-mapping'
- '@sessions/improve-sessions-retention'
- '@sessions/improve-sessions-recovery'
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
---

# Sessions improvement plan

Coordinate the three linked owner outcomes at one integrated source revision. The [baseline](baseline.json) shows retention collected at `b772c6e`, while mapping and recovery receipts require refresh after their shared source changed. This rollup adds executable combined verification and no source implementation.

## Acceptance

- [x] Each linked leaf passes its own review and observable acceptance.
- [x] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Map client conversations to cartridge sessions honestly](../improve-sessions-client-mapping/prd.md)
- [Preview and apply safe session retention](../improve-sessions-retention/prd.md)
- [Explain session damage and narrowly repair eligible snapshots](../improve-sessions-recovery/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-sessions-programme`; maximum five rounds.

Reverification at965108d9 after mailbox integration. Add the new transitive source module to verification coverage; behavioral acceptance is unchanged.

Reverification: attributed report at2a6a863 adds native main dispatch; bind src/observations.rs as transitive source, retaining previous acceptance and executable gates.

Named channel registration revalidation at 423ecd32: source footprint includes registered channels and its shared mailbox codec; acceptance and behavior gates remain unchanged.

## From the retired work memo

Folded 2026-09-15 from `work/improve-sessions-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Sessions improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Sessions, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Map client conversations to cartridge sessions honestly | [improve-sessions-client-mapping](../improve-sessions-client-mapping/prd.md) |
| 2. Preview and apply safe session retention | [improve-sessions-retention](../improve-sessions-retention/prd.md) |
| 3. Explain session damage and narrowly repair eligible snapshots | [improve-sessions-recovery](../improve-sessions-recovery/prd.md) |

### Downside coverage

1. Codex and cartridge sessions can diverge: map external identity only when supplied through a trusted channel.
2. Stored transcripts need retention: preview and pin before deletion.
3. Session identity does not restore external effects: recovery must expose unknown outcomes.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [sub-agent-sessions-record-parent-and-mailbox](../sub-agent-sessions-record-parent-and-mailbox/prd.md), [the-board-is-channels-of-lines](../the-board-is-channels-of-lines/prd.md). Their current source, status and owner take precedence over a stale assessment.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Sessions behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test sessions
just check sessions
just test mcp
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
