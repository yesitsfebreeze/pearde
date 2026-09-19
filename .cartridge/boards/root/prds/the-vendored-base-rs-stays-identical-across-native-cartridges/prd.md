---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge"
footprint:
- "agent.ctg"
- "router.ctg"
needs:
- "@mcp/a-cartridge-call-is-cancellable-and-bounded/a-cancelled-tool-call-reaches-its-running-tool"
---

# The vendored base.rs stays identical across native cartridges

## Outcome

`base.rs` is vendored byte for byte into `agent.ctg`, `mcp.ctg` and
`router.ctg` (md5 `593f0a7c…` in all three on 2026-09-19). After mcp gains the
trampoline step protocol under option A, the other two copies carry the same
file, and each cartridge that bails from a handler uses the step loop so its
node is not held during an outbound call. `agent.ctg` bails from a handler at
`module.rs:43` on the on-base branch. `router.ctg` only notifies, so it needs
the file and nothing else.

## Acceptance

- [ ] `agent.ctg/src/base.rs` and `router.ctg/src/base.rs` are byte-identical to `mcp.ctg/src/base.rs`, and a check fails when they drift.
- [ ] `agent.ctg`'s outbound call from a handler goes through the step loop, and a named test shows a second event on the agent node runs while the first waits on another cartridge.
- [ ] `just check` and `just test` pass for agent and router, and `just isolation` reports nothing.
