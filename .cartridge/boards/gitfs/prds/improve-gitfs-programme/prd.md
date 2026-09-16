---
repo: /Users/feb/dev/cartridge/fs.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: gitfs
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-gitfs-programme
needs:
- '@gitfs/improve-gitfs-readable-diff'
- '@gitfs/improve-gitfs-snapshot-selection'
- '@gitfs/improve-gitfs-reviewable-ship'
commit: "b8f27c6f1c07888bfc6e5d09f45a8751e8ca7b36"
---

# GitFS and ship improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [x] Each linked leaf passes its own review and observable acceptance.
- [x] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Inspect session changes without a mutation grant](../improve-gitfs-readable-diff/prd.md)
- [Snapshot exactly the selected owned paths](../improve-gitfs-snapshot-selection/prd.md)
- [Preview and control shipping with accurate attribution](../improve-gitfs-reviewable-ship/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-gitfs-programme`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-gitfs-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three GitFS and ship improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for GitFS and ship, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Inspect session changes without a mutation grant | [improve-gitfs-readable-diff](../improve-gitfs-readable-diff/prd.md) |
| 2. Snapshot exactly the selected owned paths | [improve-gitfs-snapshot-selection](../improve-gitfs-snapshot-selection/prd.md) |
| 3. Preview and control shipping with accurate attribution | [improve-gitfs-reviewable-ship](../improve-gitfs-reviewable-ship/prd.md) |

### Downside coverage

1. Builds read disk rather than the overlay: show revisions/materialization state and test the intended tree.
2. The optional LLM gate fails open: expose the gate result and support an explicit required-gate mode.
3. Undo rewrites history: preview targets and prefer revert for shared branches; retain lease checks for explicit rewind.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Review current source and active ownership before implementation; the assessment does not reserve files.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated GitFS and ship behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test gitfs
just check gitfs
just smoke mcp
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
