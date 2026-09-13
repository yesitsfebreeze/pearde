---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: keep-the-tree-and-record-true
needs:
- '@memory/memory-002'
- '@memory/memory-004'
- '@memory/the-graph-converges'
---

# keep-the-tree-and-record-true

Track the linked current outcomes as a finite scope snapshot. Historical framework and product proposals remain source history.

## Acceptance

- [ ] Each included leaf has its own current acceptance and owner.
- [ ] Close this snapshot only against observed child evidence; later enhancements get separate work items.

## Work items

- [Memory counts use consistent public terminology](../memory-002/prd.md)
- [Mixed and cold recall preserve per-ability ranking](../memory-004/prd.md)
- [the-graph-converges](../the-graph-converges/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `keep-the-tree-and-record-true`; maximum five rounds.
