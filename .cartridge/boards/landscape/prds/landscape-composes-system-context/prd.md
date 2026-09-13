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
canonical-scope: landscape-composes-system-context
needs:
- '@landscape/landscape-composes-system-context/context-contributor-contract'
- '@landscape/landscape-composes-system-context/memory-context-contributor'
- '@landscape/landscape-composes-system-context/live-file-context-contributors'
- '@memo/landscape-context-facade'
---

# Landscape answers across kernel, directories, memo, memory, and live state

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [Contributors return bounded attributable context rows](context-contributor-contract/prd.md)
- [Memory hits resolve to exact source evidence](memory-context-contributor/prd.md)
- [File and live context retain owner and freshness](live-file-context-contributors/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `landscape-composes-system-context`; maximum five rounds.

- [Native context facade](../../../memo/prds/landscape-context-facade/prd.md)
