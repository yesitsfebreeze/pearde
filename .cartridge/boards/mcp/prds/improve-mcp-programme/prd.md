---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: open
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
