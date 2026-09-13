---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: memo
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: memo-board-template
needs:
- '@memo/memo-board-template/initialize-board'
- '@memo/memo-board-template/board-engine-integration'
---

# The memo cartridge supplies a Pearde-compatible project template

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [Preview and install a board without overwriting edits](initialize-board/prd.md)
- [The generated board uses the pinned Pearde workflow](board-engine-integration/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `memo-board-template`; maximum five rounds.
