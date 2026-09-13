---
repo: /Users/feb/dev/cartridge/tools.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: tools
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: development-tooling-has-one-home
needs:
- '@runtime/runtime-development-package'
- '@runtime/development-clean-checkout'
---

# Development commands and verification have one owning implementation

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [Existing development commands run from one package](../../../runtime/prds/runtime-development-package/prd.md)
- [Development documents work from a clean checkout](../../../runtime/prds/development-clean-checkout/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `development-tooling-has-one-home`; maximum five rounds.
