---
kind: work
description: "Discover policy and readiness for exposed tools"
status: open
priority: P1
size: M
needs:
  - "[[@prd/work/root--improve-memory-readiness.md]]"
  - "[[@prd/work/root--improve-policy-explain.md]]"
  - "[[@prd/work/root--improve-tool-result-contract.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["discover policy and readiness for exposed tools", "implementing mcp cartridge improvements"]
---

# Discover policy and readiness for exposed tools

## Outcome

Discovery distinguishes installed, exposed, allowed, dependency-ready and unverified capabilities without running probes.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [[@prd/work/root--headless-policy-approval-channel.md]], [[@prd/work/root--every-enabled-tool-ships-a-contract-probe.md]], [[@prd/work/root--rpc-contracts-run-across-rust-lua-and-bun.md]].

## Footprint

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

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] An exposed memory tool with an unavailable store and an exposed policy-blocked gitfs write are visibly different states.
- [ ] Discovery neither calls models nor mutates stores; unavailable optional diagnostics are labelled unknown rather than hiding the tool.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Consume the shared readiness snapshot and policy explanation as bounded metadata or a dedicated diagnostic operation; avoid altering standard tool fields incompatibly. Document observation-journal dependency failures as partial telemetry.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test mcp
just check mcp
just smoke mcp
```


## Compatibility and recovery

Keep standard MCP negotiation and current client compatibility. New diagnostics must be additive or separately discoverable. Test configured grants in temporary profiles, never loosen live policy to make a check pass.

## Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-memory-readiness.md]], [[@prd/work/root--improve-policy-explain.md]], [[@prd/work/root--improve-tool-result-contract.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
