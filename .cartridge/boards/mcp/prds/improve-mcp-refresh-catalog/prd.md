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
canonical-scope: improve-mcp-refresh-catalog
needs:
- '@gitfs/tool-results-interoperate'
footprint:
- /Users/feb/dev/cartridge/mcp.ctg/service.rs
- /Users/feb/dev/cartridge/mcp.ctg/tests.rs
- /Users/feb/dev/cartridge/mcp.ctg/README.md
---

# Refresh a live client's tool catalog after replacement

A connected MCP client can observe changed, added and removed tools without using a stale descriptor silently.

## Acceptance

- [ ] An initialized fixture client observes replacement and removal; subsequent list/call use the current schema and generation.
- [ ] A rejected replacement retains the old usable catalog; clients without notification support can re-list successfully.

- [ ] Keep standard MCP negotiation and current client compatibility. New diagnostics must be additive or separately discoverable. Test configured grants in temporary profiles, never loosen live policy to make a check pass.

## Proof and recovery

Start at [service.rs](../../../service.rs), [tests.rs](../../../tests.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test mcp` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-mcp-refresh-catalog`; maximum five rounds.
