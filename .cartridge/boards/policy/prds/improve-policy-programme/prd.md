---
repo: /Users/feb/dev/cartridge/policy.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: policy
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-policy-programme
needs:
- '@policy/improve-policy-operation-rules'
- '@policy/improve-policy-resource-scope'
- '@policy/improve-policy-explain'
---

# Policy improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Authorize individual operations with stable precedence](../improve-policy-operation-rules/prd.md)
- [Constrain granted file operations to declared resources](../improve-policy-resource-scope/prd.md)
- [Explain the effective policy without executing a tool](../improve-policy-explain/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-policy-programme`; maximum five rounds.
