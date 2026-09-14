---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: open
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: mcp
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: clients-share-document-execution
needs:
- '@mcp/clients-share-document-execution/client-document-contract'
- '@agent/agent-document-client'
- '@mcp/clients-share-document-execution/mcp-document-client'
- '@proxy/proxy-document-client'
---

# Agent, MCP, and proxy share discovery and execution behavior

Roll-up only; claim a leaf for implementation. Stage one: the contract leaf freezes the
one-shot query/read/execute schema and the owner-qualified name-collision rule; the three
client leaves then adopt it in parallel. Sidecar and event lifecycle modes are refused in
this programme and belong to later work. Each client reaches the runner only through a
declared need (decision `a-cartridge-brings-its-own-surface`); no client carries another
client's protocol. All four leaves are open; the contract is the first ready-to-probe item
once `@root/memory-document-works-end-to-end` is done.

## Acceptance

- [ ] Each linked leaf is done with its own revision-bound proof and passed review.
- [ ] At pinned agent, mcp and proxy revisions, the contract's shared fixtures give the same success, tool-failure, denial and stale-revision outcomes in all three clients.
- [ ] `just test agent`, `just test mcp`, `just test proxy` and `just smoke mcp` (cwd `/Users/feb/dev/cartridge`) pass at those revisions, or each failure is named with its owner.

## Work items

- [Clients share query read and execute contracts](client-document-contract/prd.md)
- [The agent executes the selected document revision](../../../agent/prds/agent-document-client/prd.md)
- [MCP discovery and calls use the common runner](mcp-document-client/prd.md)
- [Proxy tool calls retain the shared execution outcome](../../../proxy/prds/proxy-document-client/prd.md)

## Failure and review

If the contract leaf changes after a client adopted it, that client's acceptance is stale and
is re-proved; if a leaf exhausts its allowance, this parent stays open with its gaps recorded.
[Review history](review.md); limit five rounds.
