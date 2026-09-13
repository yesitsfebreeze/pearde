---
state: open
origin: requested
priority: 84
blast-radius: high
workflow: develop-one-cartridge
needs:
  - memory-document-works-end-to-end
footprint:
  - /Users/feb/dev/cartridge/agent.ctg/model_loop.rs
  - /Users/feb/dev/cartridge/agent.ctg/run_state.rs
  - /Users/feb/dev/cartridge/mcp.ctg/service.rs
  - /Users/feb/dev/cartridge/mcp.ctg/tests.rs
  - /Users/feb/dev/cartridge/proxy.ctg/service.rs
  - /Users/feb/dev/cartridge/proxy.ctg/tests.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge
---

# Agent, MCP, and proxy share discovery and execution behavior

Clients currently duplicate tool listing, policy interpretation, identity, cancellation, observations, and result validation.

## Ownership and scope

Owner: `mcp`. Participating repositories: `agent.ctg`, `mcp.ctg`, `proxy.ctg`, `policy.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Route document discovery through landscape and calls through the shared executor. Keep each transport's framing and conversation ownership local.
2. Choose the small stable public surface: context query/read plus execution, with generated legacy listings only where compatibility requires them. Adding a document must require no client source edit.
3. Preserve interactive approvals in agent and explicit refusals for ask in headless MCP/proxy; keep the approved revision/arguments fixed through execution.
4. Unify used/outcome attribution without making observation failure mask tool results; test exact cancellation and bounded in-flight registries.

## Acceptance contract

- The same document/arguments yield equivalent success, failure, denial, and cancellation outcomes in CLI, agent, MCP, and proxy.
- Adding/removing a document changes discovery and usable capabilities without editing transport registries.
- MCP cancellation reaches the correct invocation; proxy disconnect releases its lease and child; agent resumes durable state without replaying mutations.
- No transport exposes a disabled/private document or permits model-supplied session/cwd/service-key overrides.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test agent
just test mcp
just test proxy
just smoke
```

## Failure and recovery

Generated names collide or headless approval accidentally becomes allow. Test both explicitly before changing defaults.

Rollback: Cut over one client/profile at a time with compatibility listings. Keep old descriptors available until exact tool-set and lifecycle tests pass.

## Prior context

Related existing runtime memo leaf names: `an-mcp-server-carries-the-tools`, `zirkles-tools-serve-any-agent`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
