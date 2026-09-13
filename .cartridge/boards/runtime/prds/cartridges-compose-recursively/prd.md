---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: cartridges-compose-recursively
needs:
- '@runtime/the-profile-is-the-root-composer'
- '@runtime/a-key-starts-its-provider-on-demand'
- '@runtime/a-cartridge-installs-from-its-source'
---

# cartridges-compose-recursively

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [the-profile-is-the-root-composer](../the-profile-is-the-root-composer/prd.md)
- [a-key-starts-its-provider-on-demand](../a-key-starts-its-provider-on-demand/prd.md)
- [a-cartridge-installs-from-its-source](../a-cartridge-installs-from-its-source/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `cartridges-compose-recursively`, `build-the-composition-pillar`, `the-extension-crate`; maximum five rounds.
