---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: landscape
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: recursive-development-graph
needs:
- '@landscape/recursive-development-graph/recursive-source-census'
- '@landscape/recursive-development-graph/recursive-root-search'
- '@landscape/recursive-development-graph/recursive-source-refresh'
---

# The root landscape searches every child cartridge's development record

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [Declared descendants have distinct source identities](recursive-source-census/prd.md)
- [Root search reads every permitted descendant record](recursive-root-search/prd.md)
- [A descendant edit refreshes only its derived rows](recursive-source-refresh/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `recursive-development-graph`; maximum five rounds.
