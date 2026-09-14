---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 3
review-status: delivered-pending-verification
canonical-scope: memory-owns-its-tool
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
- '@memory/memory-owns-its-tool/memory-consumer-parity'
- '@memory/memory-owns-its-tool/memory-wrapper-retirement'
---

# Memory owns its service and tool interface

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [Memory serves query and ingest through its own adapter](memory-adapter-core/prd.md)
- [Old and new consumers see one compatible memory tool](memory-consumer-parity/prd.md)
- [Retiring the wrapper preserves stores and consumers](memory-wrapper-retirement/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memory-owns-its-tool`; maximum five rounds.
