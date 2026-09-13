---
repo: /Users/feb/dev/cartridge/harness.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: harness
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-harness-programme
needs:
- '@harness/improve-harness-token-accounting'
- '@harness/improve-harness-compaction-diff'
- '@harness/improve-harness-quality-eval'
---

# Harness improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Show token estimates alongside serialized bytes](../improve-harness-token-accounting/prd.md)
- [Inspect what each compaction retained and removed](../improve-harness-compaction-diff/prd.md)
- [Measure multi-round context quality with real task outcomes](../improve-harness-quality-eval/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-harness-programme`; maximum five rounds.
