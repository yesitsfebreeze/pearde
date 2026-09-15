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
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-mcp-tool-readiness
footprint:
- /Users/feb/dev/cartridge/mcp.ctg/src/service.rs
- /Users/feb/dev/cartridge/mcp.ctg/.cartridge/tests/unit/tests.rs
- /Users/feb/dev/cartridge/mcp.ctg/.cartridge/docs/README.md
needs:
- "@policy/improve-policy-explain"
- "@memory/improve-memory-readiness"
- "@root/improve-tool-result-contract"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-mcp-tool-readiness.md` (status open). The PRD state above is authoritative.

### Outcome

Discovery distinguishes installed, exposed, allowed, dependency-ready and unverified capabilities without running probes.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [headless-policy-approval-channel](../../../root/prds/headless-policy-approval-channel/prd.md), [every-enabled-tool-ships-a-contract-probe](../../../root/prds/every-enabled-tool-ships-a-contract-probe/prd.md), [rpc-contracts-run-across-rust-lua-and-bun](../../../root/prds/rpc-contracts-run-across-rust-lua-and-bun/prd.md).

### Footprint

MCP bridge; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `mcp.ctg/service.rs`
- `mcp.ctg/tests.rs`
- `mcp.ctg/README.md`
- `cartridge.ctg/.cartridge/mcp/config.lua`
- `cartridge.ctg/scripts/smoke.py`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] An exposed memory tool with an unavailable store and an exposed policy-blocked gitfs write are visibly different states.
- [ ] Discovery neither calls models nor mutates stores; unavailable optional diagnostics are labelled unknown rather than hiding the tool.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Consume the shared readiness snapshot and policy explanation as bounded metadata or a dedicated diagnostic operation; avoid altering standard tool fields incompatibly. Document observation-journal dependency failures as partial telemetry.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test mcp
just check mcp
just smoke mcp
```


### Compatibility and recovery

Keep standard MCP negotiation and current client compatibility. New diagnostics must be additive or separately discoverable. Test configured grants in temporary profiles, never loosen live policy to make a check pass.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-memory-readiness](../../../memory/prds/improve-memory-readiness/prd.md), [improve-policy-explain](../../../policy/prds/improve-policy-explain/prd.md), [improve-tool-result-contract](../../../root/prds/improve-tool-result-contract/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
