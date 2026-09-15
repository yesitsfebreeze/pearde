---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: mcp
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: improve-mcp-programme
needs:
- '@mcp/improve-mcp-approval-route'
- '@mcp/improve-mcp-tool-readiness'
- '@mcp/improve-mcp-refresh-catalog'
---

# MCP bridge improvement plan

Roll-up only; claim a leaf for implementation. Approval route (mcp f5a7405) and catalog
refresh (29b20b2) are done; tool readiness remains open and reuses the existing registry and
`cartridge/policy` inspection instead of a second diagnostics path.

## Acceptance

- [ ] Each linked leaf is done with its own revision-bound proof and passed review.
- [ ] At one pinned mcp revision, `just test mcp` and `just smoke mcp` (cwd `/Users/feb/dev/cartridge`) pass, or each remaining failure is named with its owner (release-status currently lists one test failure and a `memo inactive` smoke failure).
- [ ] Remaining limitations are recorded at that revision.

## Work items

- [Make headless operation authorization usable and truthful](../improve-mcp-approval-route/prd.md) — done
- [Discover policy and readiness for exposed tools](../improve-mcp-tool-readiness/prd.md) — open
- [Refresh a live client's tool catalog after replacement](../improve-mcp-refresh-catalog/prd.md) — done

## Failure and review

If a leaf exhausts its review allowance, this parent stays open and records that leaf's gaps;
done leaves are not reopened. [Review history](review.md); limit five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/improve-mcp-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three MCP bridge improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for MCP bridge, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Make headless operation authorization usable and truthful | [improve-mcp-approval-route](../improve-mcp-approval-route/prd.md) |
| 2. Discover policy and readiness for exposed tools | [improve-mcp-tool-readiness](../improve-mcp-tool-readiness/prd.md) |
| 3. Refresh a live client's tool catalog after replacement | [improve-mcp-refresh-catalog](../improve-mcp-refresh-catalog/prd.md) |

### Downside coverage

1. Headless ask has no responder: preserve refusal and give an explicit viable route.
2. Wildcard composition changes tool membership: report changes and retain policy bounds.
3. Transport and provider failures overlap: preserve typed, attributed errors.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [headless-policy-approval-channel](../../../root/prds/headless-policy-approval-channel/prd.md), [every-enabled-tool-ships-a-contract-probe](../../../root/prds/every-enabled-tool-ships-a-contract-probe/prd.md), [rpc-contracts-run-across-rust-lua-and-bun](../../../root/prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md). Their current source, status and owner take precedence over a stale assessment.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated MCP bridge behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test mcp
just check mcp
just smoke mcp
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
