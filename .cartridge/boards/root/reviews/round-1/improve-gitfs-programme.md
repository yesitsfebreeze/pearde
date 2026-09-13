---
kind: work
description: "Deliver the three GitFS and ship improvements with explicit risk coverage"
status: open
subwork:
  - "[[@prd/work/root--improve-gitfs-readable-diff.md]]"
  - "[[@prd/work/root--improve-gitfs-snapshot-selection.md]]"
  - "[[@prd/work/root--improve-gitfs-reviewable-ship.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["planning gitfs improvements", "reviewing gitfs cartridge readiness"]
---

# GitFS and ship improvement plan

## Outcome

Deliver the three improvements requested for GitFS and ship, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Inspect session changes without a mutation grant | [[@prd/work/root--improve-gitfs-readable-diff.md]] |
| 2. Snapshot exactly the selected owned paths | [[@prd/work/root--improve-gitfs-snapshot-selection.md]] |
| 3. Preview and control shipping with accurate attribution | [[@prd/work/root--improve-gitfs-reviewable-ship.md]] |

## Downside coverage

1. Builds read disk rather than the overlay: show revisions/materialization state and test the intended tree.
2. The optional LLM gate fails open: expose the gate result and support an explicit required-gate mode.
3. Undo rewrites history: preview targets and prefer revert for shared branches; retain lease checks for explicit rewind.

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
- [ ] The integrated GitFS and ship behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test gitfs
just check gitfs
just smoke mcp
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
