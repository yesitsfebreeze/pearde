---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: mcp
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: clients-share-document-execution
needs:
- '@mcp/clients-share-document-execution/client-document-contract'
---

# MCP discovery and calls use the common runner

Adapt MCP's discovery and execution to the shared one-shot/artifact contract.

## Acceptance

- [ ] New and removed documents refresh the catalog consistently.
- [ ] Private/colliding names cannot select an unintended backend.
- [ ] Headless ask refuses and reconnect does not replay an uncertain mutation.

## Proof and recovery

Start at [service.rs](../../../../service.rs), [tests.rs](../../../../tests.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test mcp` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `clients-share-document-execution`; maximum five rounds.
