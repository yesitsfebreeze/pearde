---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: mcp
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-mcp-programme
needs:
- '@mcp/improve-mcp-approval-route'
- '@mcp/improve-mcp-tool-readiness'
- '@mcp/improve-mcp-refresh-catalog'
---

# MCP bridge improvement plan

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Make headless operation authorization usable and truthful](../improve-mcp-approval-route/prd.md)
- [Discover policy and readiness for exposed tools](../improve-mcp-tool-readiness/prd.md)
- [Refresh a live client's tool catalog after replacement](../improve-mcp-refresh-catalog/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-mcp-programme`; maximum five rounds.
