---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memo
work-kind: rollup
review-round: 3
review-status: delivered-pending-verification
canonical-scope: improve-memo-programme
needs:
- '@landscape/improve-memo-compact-landscape'
- '@memo/improve-memo-stale-evidence'
- '@memo/improve-memo-types-drilldown'
---

# Memo improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Bound landscape discovery and offer inventory drilldown](../../../landscape/prds/improve-memo-compact-landscape/prd.md)
- [Distinguish stale source references from current guidance](../improve-memo-stale-evidence/prd.md)
- [Read type declarations individually](../improve-memo-types-drilldown/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memo-programme`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-memo-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Memo improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Memo, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Bound landscape discovery and offer inventory drilldown | [improve-memo-compact-landscape](../../../landscape/prds/improve-memo-compact-landscape/prd.md) |
| 2. Distinguish stale source references from current guidance | [improve-memo-stale-evidence](../improve-memo-stale-evidence/prd.md) |
| 3. Read type declarations individually | [improve-memo-types-drilldown](../improve-memo-types-drilldown/prd.md) |

### Downside coverage

1. Metadata needs maintenance: surface missing declarations and preserve source ownership.
2. Lexical retrieval misses paraphrases: reuse the existing ranking work and retain a query regression corpus.
3. Observations are caller reports: label them as reported evidence, never independent verification.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [a-search-ranks-current-guidance-over-delivered-history](../../../landscape/prds/a-search-ranks-current-guidance-over-delivered-history/prd.md), [handle-memory-staleness-and-conflicts](../handle-memory-staleness-and-conflicts/prd.md). Their current source, status and owner take precedence over a stale assessment.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Memo behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test memo
just check memo
just test landscape
just check landscape
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
