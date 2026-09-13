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
canonical-scope: improve-memory-programme
needs:
- '@memory/improve-memory-owner-access'
- '@memory/improve-memory-readiness'
- '@memory/improve-memory-provenance'
---

# Memory improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Query a memory store through its existing owner](../improve-memory-owner-access/prd.md)
- [Report memory readiness separately from registration](../improve-memory-readiness/prd.md)
- [Expose fact provenance freshness and conflicts consistently](../improve-memory-provenance/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-memory-programme`; maximum five rounds.
