---
repo: /Users/feb/dev/cartridge/proxy.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: proxy
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-proxy-programme
needs:
- '@proxy/improve-proxy-total-usage'
- '@proxy/improve-proxy-tool-trace'
- '@proxy/improve-proxy-continuation-recovery'
---

# Proxy improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Account for every internal model round consistently](../improve-proxy-total-usage/prd.md)
- [Inspect internal proxy tool work by request identity](../improve-proxy-tool-trace/prd.md)
- [Make continuation lifetime and restart recovery explicit](../improve-proxy-continuation-recovery/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-proxy-programme`; maximum five rounds.
