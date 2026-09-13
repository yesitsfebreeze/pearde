---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-tools-programme
needs:
- '@runtime/improve-tools-preflight'
- '@runtime/improve-tools-worktree-resume'
- '@runtime/improve-tools-bundle-provenance'
---

# Workspace tools improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Preview workspace-tool effects before execution](../improve-tools-preflight/prd.md)
- [Recover interrupted worktree creation safely](../improve-tools-worktree-resume/prd.md)
- [Ship bundles with source and dependency provenance](../improve-tools-bundle-provenance/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-tools-programme`; maximum five rounds.
