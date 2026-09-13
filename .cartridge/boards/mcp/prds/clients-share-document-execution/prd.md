---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: mcp
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: clients-share-document-execution
needs:
- '@mcp/clients-share-document-execution/client-document-contract'
- '@agent/agent-document-client'
- '@mcp/clients-share-document-execution/mcp-document-client'
- '@proxy/proxy-document-client'
---

# Agent, MCP, and proxy share discovery and execution behavior

Coordinate the linked outcomes. Claim and implement a leaf; this parent records their combined acceptance.

## Acceptance

- [ ] Each linked leaf has revision-bound proof and passes its own review.
- [ ] The included outcomes work together at the same pinned owner revisions.

## Work items

- [Clients share query read and execute contracts](client-document-contract/prd.md)
- [The agent executes the selected document revision](../../../agent/prds/agent-document-client/prd.md)
- [MCP discovery and calls use the common runner](mcp-document-client/prd.md)
- [Proxy tool calls retain the shared execution outcome](../../../proxy/prds/proxy-document-client/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `clients-share-document-execution`, `an-mcp-server-carries-the-tools`, `zirkles-tools-serve-any-agent`; maximum five rounds.
