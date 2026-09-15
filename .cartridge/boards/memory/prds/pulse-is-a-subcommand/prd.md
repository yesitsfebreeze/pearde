---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# No CLI verb reaches the clustering pass — `memory pulse` routes one to the daemon's tick queue

## Do

One site mints an unnamed child memory — `spawn_child_clusters`
(`src/tick_loop/src/tick.rs`) inside the daemon's `Cluster` task — and the only
handle on the pass that enqueues it is the MCP `pulse` tool
(`src/commands/src/commands_mcp.rs` -> `tool_pulse`, `src/rpc/src/server.rs`).
`Commands` in `src/commands/src/lib.rs` carries no `Pulse`, so nothing driving
the CLI can force a clustering pass, and the flush half of
[unnamed-promote-routes-to-the-daemon](../unnamed-promote-routes-to-the-daemon/prd.md)'s `Check` stays unmeasurable.

Give the CLI the arm: `Pulse { strength: Option<f64> }` beside `Health`,
dispatched to a handler in `src/commands/src/commands_admin.rs` that
`route_to`s the daemon's `pulse` tool the way `focus add` and `unnamed
promote` route theirs. `f64` rather than a narrower float because that is what
`PulseArgs` and the sibling `mass` already take. Unlike every other routed
verb this one has no local half — the pass runs on the daemon's tick queue —
so `Routed::NoDaemon` fails loudly instead of writing anything locally, and a
daemon answering `noop` (no tick queue configured) is reported as the failure
it is rather than printed as success.

## Acceptance
An e2e test beside the two routing tests that share its blinding
(`tests/e2e/focus_routing.rs`): against a running daemon `memory pulse` reports
the pass taken, and with nothing serving it exits non-zero.

**Landed 2026-09-07.** `Commands::Pulse` -> `cmd_pulse`, held by
`pulse_reaches_the_daemons_tick_queue` — against a started daemon
`memory pulse --strength 0.5` exits 0 printing `pulsed: strength 0.5` — and
`pulse_fails_loudly_with_no_daemon`, where the same call exits non-zero
saying nothing is serving. Two tests rather than one, which is the shape the
routing tests beside them already have: the served half and the no-daemon
half get a project each.
