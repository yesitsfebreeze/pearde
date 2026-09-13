---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: landscape
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: context-quality-is-measured
needs:
- '@landscape/context-quality-is-measured/context-baseline-corpus'
- '@landscape/context-quality-is-measured/context-comparison-gate'
---

# Landscape quality and cost are tested against a versioned corpus

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [A pinned corpus records the old selector baseline](context-baseline-corpus/prd.md)
- [Context regressions fail an explicit comparison gate](context-comparison-gate/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `context-quality-is-measured`; maximum five rounds.
