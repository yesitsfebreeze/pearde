---
state: open
origin: requested
priority: 96
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @gitfs/tool-results-interoperate
footprint:
  - /Users/feb/dev/cartridge/memory.ctg/src/cartridge.rs
  - /Users/feb/dev/cartridge/memory.ctg/tests/cartridge.rs
  - /Users/feb/dev/cartridge/memory.ctg/cartridge.json
  - /Users/feb/dev/cartridge/memory-tool.ctg
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/default/init.lua
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/mcp/init.lua
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/proxy/init.lua
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/proxy/config.lua
  - /Users/feb/dev/cartridge/cartridge.ctg/workspace/Cargo.toml
  - /Users/feb/dev/cartridge/cartridge.ctg/repositories.json
  - /Users/feb/dev/cartridge/cartridge.ctg/builtin/memory-tool
  - /Users/feb/dev/cartridge/.gitmodules
---

# Memory owns its service and tool interface

The memory-tool process forwards two operations and owns no independent state. Memory should expose the adapter itself while retaining its database/CLI boundary.

## Ownership and scope

Owner: `memory`. Participating repositories: `memory.ctg`, `memory-tool.ctg`, `cartridge.ctg`, `root`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Use an isolated memory branch/worktree as required by memory.ctg/AGENTS.md. Factor a shared engine-call function used by the native service and tool adapter; do not recurse through the host into the same service.
2. Move query/ingest context validation, synchronous-ingest semantics, and error translation into the cartridge feature. Enforce advertised text/k/raw bounds and resolve the undocumented sync input explicitly.
3. Register memory and tool.memory from one cartridge. Capture exact tool lists for default, MCP, and proxy before changing composition; preserve proxy's current lack of exposed memory writes through explicit filtering/configuration.
4. Migrate profiles and build catalog, then retire the wrapper member/link/submodule only after mixed-version consumers are covered. Preserve its source history through normal Git migration, not destructive cleanup.

## Acceptance contract

- Memory query and ingest produce the same successful output and explicit failed-ingest error through native and tool entry points.
- Invalid context and out-of-range input are rejected before opening a store or calling a model endpoint.
- Replacement preserves committed data and releases the old writer; a bad candidate leaves the current generation usable.
- Default and MCP expose one memory tool each; proxy exposure and policy do not expand accidentally.
- Standalone memory builds without the cartridge feature; the composed checkout builds without a memory-tool package after the retirement step.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test memory --test cartridge
just check memory
just test memory
just links
just smoke mcp
```

## Failure and recovery

A second engine instance claims the same writer, or wildcard discovery exposes new writes. Test lifecycle and exact tool sets.

Rollback: Keep the wrapper available until consumers land; restore its composition entries if necessary. Never downgrade or migrate store bytes for an adapter move.

## Prior context

Related existing runtime memo leaf names: `one-search-covers-the-record-and-memory`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
