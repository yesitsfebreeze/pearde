---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: mcp
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-mcp-approval-route
needs:
- '@policy/improve-policy-operation-rules'
- '@policy/improve-policy-explain'
footprint:
- src/service.rs
- src/main.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/tests/integration/approval.test.ts
- .cartridge/docs/approval.md
commit: "f5a740517bc2668b50cf4f61fe81a1e37bb4cfad"
---

# Make headless operation authorization usable and truthful

An MCP client can discover whether an operation is allowed and understand how a denied/ask operation can be authorized.

## Acceptance

- [x] A temporary profile allows gitfs reads and refuses writes, with the matching rule and a concrete operator path in the response.
- [x] Forged context/approval fields do not authorize a mutation; existing allow/ask/deny clients remain compatible.

- [x] Keep standard MCP negotiation and current client compatibility. New diagnostics must be additive or separately discoverable. Test configured grants in temporary profiles, never loosen live policy to make a check pass.

## Proof and recovery

Source: `mcp.ctg/src/service.rs` and `.cartridge/tests/unit/tests.rs`.

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test mcp` from the composed root with the acceptance fixtures. The 15-test public gate, real stdio policy fixture and public check now pass; see verification.json.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-mcp-approval-route`; maximum five rounds.
