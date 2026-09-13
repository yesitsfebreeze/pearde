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
canonical-scope: improve-mcp-tool-readiness
needs:
- '@landscape/landscape-composes-system-context/context-contributor-contract'
- '@policy/improve-policy-explain'
footprint:
- /Users/feb/dev/cartridge/mcp.ctg/service.rs
- /Users/feb/dev/cartridge/mcp.ctg/tests.rs
- /Users/feb/dev/cartridge/mcp.ctg/README.md
---

# Discover policy and readiness for exposed tools

Landscape owns the generic readiness row assembled by the memo facade; memory supplies only its store/model status, and policy supplies a revision-bound decision. The row records installed, exposed, allowed, dependency-ready and verification state independently, with source revision/time. MCP exposes an optional diagnostic view without changing standard tool schema meanings.

## Acceptance

- [ ] A registered unavailable-memory tool, denied GitFS write and unverified healthy tool have distinct rows.
- [ ] Missing diagnostics are unknown/partial; discovery starts no provider, opens no writer and runs no model.
- [ ] MCP and UI consume the same fixture snapshot and do not treat stale observed readiness as execution authorization.

## Proof and recovery

Start at [service.rs](../../../service.rs), [tests.rs](../../../tests.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test mcp` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-mcp-tool-readiness`; maximum five rounds.
