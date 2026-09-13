---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: mcp
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-mcp-approval-route
needs:
- '@policy/improve-policy-operation-rules'
- '@policy/improve-policy-explain'
footprint:
- /Users/feb/dev/cartridge/mcp.ctg/service.rs
- /Users/feb/dev/cartridge/mcp.ctg/tests.rs
- /Users/feb/dev/cartridge/mcp.ctg/README.md
---

# Make headless operation authorization usable and truthful

An MCP client can discover whether an operation is allowed and understand how a denied/ask operation can be authorized.

## Acceptance

- [ ] A temporary profile allows gitfs reads and refuses writes, with the matching rule and a concrete operator path in the response.
- [ ] Forged context/approval fields do not authorize a mutation; existing allow/ask/deny clients remain compatible.

- [ ] Keep standard MCP negotiation and current client compatibility. New diagnostics must be additive or separately discoverable. Test configured grants in temporary profiles, never loosen live policy to make a check pass.

## Proof and recovery

Start at [service.rs](../../../service.rs), [tests.rs](../../../tests.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test mcp` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-mcp-approval-route`; maximum five rounds.
