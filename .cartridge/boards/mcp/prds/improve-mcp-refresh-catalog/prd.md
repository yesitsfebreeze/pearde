---
repo: /Users/feb/dev/cartridge/mcp.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: mcp
work-kind: leaf
review-round: 4
review-status: passed
canonical-scope: improve-mcp-refresh-catalog
footprint:
- src/service.rs
- .cartridge/tests/unit/tests.rs
- .cartridge/tests/integration/refresh.test.ts
- .cartridge/docs/README.md
commit: "f5a740517bc2668b50cf4f61fe81a1e37bb4cfad"
needs:
- "@runtime/mcp-stdio-replies-during-replacement"
- "@gitfs/tool-results-interoperate"
- "@root/improve-tool-result-contract"
---

# Refresh a live client's tool catalog after replacement

A connected MCP client can observe changed, added and removed tools without using a stale descriptor silently.

## Acceptance

- [x] An initialized fixture client observes replacement and removal; subsequent list/call use the current schema and generation.
- [x] A rejected replacement retains the old usable catalog; clients without notification support can re-list successfully.

- [x] Keep standard MCP negotiation and current client compatibility. New diagnostics must be additive or separately discoverable. Test configured grants in temporary profiles, never loosen live policy to make a check pass.

## Proof and recovery

Start at [service.rs](../../../service.rs), [tests.rs](../../../tests.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test mcp` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-mcp-refresh-catalog`; maximum five rounds.

## Current analysis

[Baseline](baseline.json) demonstrates mixed generations when replacement lands
during descriptor collection. Existing service-version invalidation and runtime
composition already provide ordinary re-listing. Validate the version vector
before and after collection, retry boundedly on churn, and publish only a stable
registry. Prove live addition/removal and rejected replacement over one actual
initialized stdio client. Preserve polling compatibility and do not advertise
unsupported push notifications.

## Discovered transport dependency

The actual client proved a missing runtime reply during replacement. Its bounded
runtime repair is a hard prerequisite; see the linked dependency and round 4.

## Verified result

Public `just test mcp` passes all 12 tests, including one actual initialized
stdio client across replacement, rejection, addition and removal. The discovery
race now returns coherent descriptors; persistent churn stops after three
attempts. Public formatting/clippy passes. The runtime reply dependency is
collected at f71b762fd839e6a2644f16565b1de10edf967c9e.

## From the retired work memo

Folded 2026-09-15 from `work/improve-mcp-refresh-catalog.md` (status open). The PRD state above is authoritative.

### Outcome

A connected MCP client can observe changed, added and removed tools without using a stale descriptor silently.

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
- [ ] An initialized fixture client observes replacement and removal; subsequent list/call use the current schema and generation.
- [ ] A rejected replacement retains the old usable catalog; clients without notification support can re-list successfully.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Exercise current per-request describe behavior first. Add negotiated change notifications where supported and snapshot/revision identifiers or a documented re-list path otherwise; reject calls whose required reviewed revision changed.
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
Ready after [improve-tool-result-contract](../../../root/prds/improve-tool-result-contract/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
