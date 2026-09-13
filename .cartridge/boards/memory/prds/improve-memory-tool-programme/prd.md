---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memory
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-memory-tool-programme
needs:
- '@memory/improve-memory-tool-get'
- '@memory/improve-memory-tool-correct'
- '@memory/improve-memory-tool-errors'
---

# Memory tool adapter improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Retrieve a recalled fact by stable ID](../improve-memory-tool-get/prd.md)
- [Correct or forget one identified fact through the tool boundary](../improve-memory-tool-correct/prd.md)
- [Return actionable memory failures and enforce the tool schema](../improve-memory-tool-errors/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-tool-programme`; maximum five rounds.
