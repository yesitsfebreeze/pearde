---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: root
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: capabilities-live-with-their-owners
needs:
- '@memo/memo-write-document'
- '@fs/direct-fs-document'
- '@gitfs/gitfs-document'
- '@pty/pty-document'
- '@sessions/sessions-document'
- '@router/router-document'
---

# Each capability ships its own executable documentation

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [A document invokes validated memo writes](../../../memo/prds/memo-write-document/prd.md)
- [A document preserves guarded direct file edits](../../../fs/prds/direct-fs-document/prd.md)
- [A document preserves session overlay semantics](../../../gitfs/prds/gitfs-document/prd.md)
- [A shell document uses the owned persistent terminal](../../../pty/prds/pty-document/prd.md)
- [A document reads bounded session history](../../../sessions/prds/sessions-document/prd.md)
- [A document explains routing without exposing secrets](../../../router/prds/router-document/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `capabilities-live-with-their-owners`, `the-tool-surface-is-search-and-shell`; maximum five rounds.
