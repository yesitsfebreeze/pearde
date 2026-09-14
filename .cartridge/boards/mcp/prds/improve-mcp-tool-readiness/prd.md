---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: mcp
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-mcp-tool-readiness
needs:
- '@policy/improve-policy-explain'
footprint:
- /Users/feb/dev/cartridge/mcp.ctg/src/service.rs
- /Users/feb/dev/cartridge/mcp.ctg/.cartridge/tests/unit/tests.rs
- /Users/feb/dev/cartridge/mcp.ctg/.cartridge/docs/README.md
---

# Discover policy and readiness for exposed tools

No generic readiness producer exists: landscape is dissolved into core fabric, and under
decision `a-cartridge-brings-its-own-surface` MCP may not ask memory, gitfs or any sibling
about its internals. MCP already knows three facts itself: installed/exposed (its registry
from each tool's `describe`, `src/service.rs`), and allowed with a policy revision
(`cartridge/policy` via the declared `policy.explain` need). This leaf adds one optional
diagnostic view over those facts plus an optional descriptor-declared `readiness` field, the
same way descriptors already declare `reads`. Standard `tools/list` and `tools/call` meanings
do not change. Excluded: adding `readiness` to other cartridges' descriptors (their boards) and
the tui view (`@ui/improve-ui-tool-availability`).

## Acceptance

- [ ] One row per exposed tool records exposed, allowed (with policy revision) and descriptor readiness independently, with observation time.
- [ ] A tool whose descriptor omits `readiness`, or a `policy.explain` failure, shows `unknown`, never ready or denied.
- [ ] Building the view starts no provider, opens no writer, runs no model and grants nothing; a subsequent `tools/call` still checks policy again.
- [ ] A stale row (descriptor revision changed) is marked stale rather than served as current.

## Proof and recovery

First step: run `just test mcp` (cwd `/Users/feb/dev/cartridge`) and record the baseline,
including the one known failure from release-status. Add fixture tools with and without
`readiness` in `.cartridge/tests/unit/tests.rs`; the gate is the same command. Rollback: the
view is an additional experimental method; removing it leaves the catalog unchanged.

## Dependencies and review

Ready: `@policy/improve-policy-explain` is done. The former need on the dissolved landscape contributor contract was dropped; MCP does not consume context rows. [Review history](review.md); rounds inherited from `improve-mcp-tool-readiness`; limit five.
