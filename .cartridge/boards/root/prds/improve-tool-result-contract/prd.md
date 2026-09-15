---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 90
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: leaf
---

# Make real tool results interoperable across callers

## Outcome

All shipped tool result envelopes are accepted consistently by MCP, proxy and native agent without losing structured payloads, error state or invocation identity.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [rpc-contracts-run-across-rust-lua-and-bun](../rpc-contracts-run-across-rust-lua-and-bun/prd.md).

## Footprint

Shared result contract; source modifications belong to the owning repositories and must coordinate with existing RPC work.
All paths below are relative to /Users/feb/dev/cartridge.

- `gitfs.ctg/service.rs`
- `gitfs.ctg/ship.rs`
- `mcp.ctg/service.rs`
- `mcp.ctg/tests.rs`
- `proxy.ctg/service.rs`
- `proxy.ctg/tests.rs`
- `agent.ctg/model_loop.rs`
- `cartridge.ctg/src/sdk.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Acceptance
- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Real MCP GitFS read and ship scan return successful tool results that decode to the same domain payload as direct service calls; no production repo or remote is touched.
- [ ] String success, structured success normalization, tool error, malformed result, cancelled invocation and partial outcome fixtures produce equivalent semantics through MCP, proxy and native agent.
- [ ] Existing callers remain compatible and decode structured data once; unknown/malformed envelopes fail explicitly without invoking another operation.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. First reproduce the reported GitFS read and ship scan failure with a real host/MCP client in a disposable Git repository, under an explicit read-only test policy. Define one backward-compatible result schema/normalizer at the SDK or shared boundary: preserve the current string-content wire and serialize structured domain payloads there exactly once, unless a versioned negotiation is explicitly introduced. Reject malformed shapes consistently, preserve typed error payloads, and add real-provider fixtures rather than relying only on fake tools. Coordinate shared wire edits with the existing RPC-contract owner.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test gitfs
just test mcp
just test proxy
just test agent
just check gitfs
just check mcp
just check proxy
just check agent
just smoke
just test runtime
just check runtime
```


## Compatibility and recovery

Preserve existing callers through one documented normalization boundary. Do not fork a second tool protocol. Malformed or unsupported shapes fail explicitly; compatibility tests run before replacement. Revert the shared adapter change without altering domain stores.

## Handoff

Priority P0; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
