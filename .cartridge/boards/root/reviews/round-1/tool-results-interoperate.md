---
state: open
origin: requested
priority: 98
blast-radius: high
workflow: develop-one-cartridge
footprint:
  - /Users/feb/dev/cartridge/gitfs.ctg/service.rs
  - /Users/feb/dev/cartridge/gitfs.ctg/ship.rs
  - /Users/feb/dev/cartridge/gitfs.ctg/main.rs
  - /Users/feb/dev/cartridge/gitfs.ctg/cartridge.json
  - /Users/feb/dev/cartridge/mcp.ctg/tests.rs
  - /Users/feb/dev/cartridge/proxy.ctg/tests.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/scripts/smoke.py
---

# Every currently exposed tool completes through its real consumers

A direct gitfs read succeeds today, but MCP gitfs/read and ship/scan fail with invalid tool result envelope. Existing unit tests do not establish consumer compatibility.

## Ownership and scope

Owner: `gitfs`. Participating repositories: `gitfs.ctg`, `mcp.ctg`, `proxy.ctg`, `agent.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Port the assessment's temporary-Git-repository probe into an automated real-host regression for direct calls, MCP, and proxy dispatch.
2. Make successful gitfs and ship results satisfy the existing string-content/boolean-error contract at the owner boundary; preserve structured data by JSON serialization, not field loss.
3. Inventory every enabled tool through its real describe/call path. Cover denial, invalid inputs, and tool errors as distinct outcomes.
4. Make optional router gating explicit in declaration/configuration; characterize configured-gate unavailability and preserve or deliberately revise the documented fail-open behavior with a focused decision.

## Acceptance contract

- Direct gitfs/read, MCP gitfs/read, and ship/scan return equivalent decoded data; MCP reports tool failures as isError, not transport -32603.
- Proxy executes a real fixture tool with the production envelope validator; agent continues after a normal tool error.
- Invalid JSON/envelopes fail before downstream mutation; policy ask/deny never invokes the backend.
- Offline fixtures make no provider request and never push or alter the user's Git repository.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test gitfs
just test mcp
just test proxy
just test agent
just smoke
```

## Failure and recovery

A green tools/list masks a broken invocation. Require actual calls against production tool binaries.

Rollback: Keep existing service names and schema. Revert owner serialization and its consumers together if necessary; no persisted format changes.

## Prior context

Related existing runtime memo leaf names: `every-enabled-tool-ships-a-contract-probe`, `tool-probes-run-and-locate-a-failing-provider`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
