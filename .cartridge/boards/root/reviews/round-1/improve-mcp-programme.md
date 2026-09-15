---
kind: work
description: "Deliver the three MCP bridge improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-mcp-approval-route](../../../mcp/prds/improve-mcp-approval-route/prd.md)"
  - "[improve-mcp-tool-readiness](../../../mcp/prds/improve-mcp-tool-readiness/prd.md)"
  - "[improve-mcp-refresh-catalog](../../../mcp/prds/improve-mcp-refresh-catalog/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning mcp improvements", "reviewing mcp cartridge readiness"]
---

# MCP bridge improvement plan

## Outcome

Deliver the three improvements requested for MCP bridge, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Make headless operation authorization usable and truthful | [improve-mcp-approval-route](../../../mcp/prds/improve-mcp-approval-route/prd.md) |
| 2. Discover policy and readiness for exposed tools | [improve-mcp-tool-readiness](../../../mcp/prds/improve-mcp-tool-readiness/prd.md) |
| 3. Refresh a live client's tool catalog after replacement | [improve-mcp-refresh-catalog](../../../mcp/prds/improve-mcp-refresh-catalog/prd.md) |

## Downside coverage

1. Headless ask has no responder: preserve refusal and give an explicit viable route.
2. Wildcard composition changes tool membership: report changes and retain policy bounds.
3. Transport and provider failures overlap: preserve typed, attributed errors.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [headless-policy-approval-channel](../../prds/headless-policy-approval-channel/prd.md), [every-enabled-tool-ships-a-contract-probe](../../prds/every-enabled-tool-ships-a-contract-probe/prd.md), [rpc-contracts-run-across-rust-lua-and-bun](../../prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md). Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated MCP bridge behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test mcp
just check mcp
just smoke mcp
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
