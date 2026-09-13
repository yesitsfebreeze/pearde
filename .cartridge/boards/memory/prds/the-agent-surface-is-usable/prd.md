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
canonical-scope: the-agent-surface-is-usable
needs:
- '@memory/memory-owns-its-tool/memory-adapter-core'
- '@memory/improve-memory-tool-get'
- '@memory/improve-memory-tool-errors'
- '@memory/improve-memory-readiness'
---

# the-agent-surface-is-usable

Track the linked current outcomes as a finite scope snapshot. Historical framework and product proposals remain source history.

## Acceptance

- [ ] Each included leaf has its own current acceptance and owner.
- [ ] Close this snapshot only against observed child evidence; later enhancements get separate work items.

## Work items

- [Memory serves query and ingest through its own adapter](../memory-owns-its-tool/memory-adapter-core/prd.md)
- [Retrieve a recalled fact by stable ID](../improve-memory-tool-get/prd.md)
- [Return actionable memory failures and enforce the tool schema](../improve-memory-tool-errors/prd.md)
- [Report memory readiness separately from registration](../improve-memory-readiness/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-agent-surface-is-usable`; maximum five rounds.
