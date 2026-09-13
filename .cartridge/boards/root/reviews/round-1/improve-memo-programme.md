---
kind: work
description: "Deliver the three Memo improvements with explicit risk coverage"
status: open
subwork:
  - "[[@prd/work/root--improve-memo-compact-landscape.md]]"
  - "[[@prd/work/root--improve-memo-stale-evidence.md]]"
  - "[[@prd/work/root--improve-memo-types-drilldown.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["planning memo improvements", "reviewing memo cartridge readiness"]
---

# Memo improvement plan

## Outcome

Deliver the three improvements requested for Memo, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Bound landscape discovery and offer inventory drilldown | [[@prd/work/root--improve-memo-compact-landscape.md]] |
| 2. Distinguish stale source references from current guidance | [[@prd/work/root--improve-memo-stale-evidence.md]] |
| 3. Read type declarations individually | [[@prd/work/root--improve-memo-types-drilldown.md]] |

## Downside coverage

1. Metadata needs maintenance: surface missing declarations and preserve source ownership.
2. Lexical retrieval misses paraphrases: reuse the existing ranking work and retain a query regression corpus.
3. Observations are caller reports: label them as reported evidence, never independent verification.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [[@prd/work/root--a-search-ranks-current-guidance-over-delivered-history.md]], [[handle-memory-staleness-and-conflicts]]. Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Memo behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test memo
just check memo
just test landscape
just check landscape
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
