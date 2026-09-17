---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
footprint:
- "src/transport/cartridge.rs"
- "src/transport/rpc.rs"
- "src/node/mod.rs"
---

# A cartridge call can be cancelled

## Outcome

A caller that gives up on a cartridge call releases that call's resources on the
provider's side. When a bound expires, the provider is told, its in-flight
permit is returned and its listener stops, instead of the caller merely dropping
its own future while the work runs on to completion.

## Evidence

Established 2026-09-17 by the analyst of `@mcp/a-cartridge-call-is-cancellable-and-bounded`,
reading `cartridge.ctg` at HEAD `63ff234` with `git show` rather than the dirty
working tree.

- A caller-side bound tells the provider nothing. `src/transport/cartridge.rs:389-393`
  wraps the RPC in `tokio::time::timeout`; on expiry the future is dropped and
  the only cleanup is `impl Drop for Waiting` (`src/transport/rpc.rs:292-304`),
  which removes the id from the **caller's local** pending map. No frame leaves
  the process.
- Nothing in the protocol can cancel. `handle` matches exactly `apply`,
  `directory`, `dispose` and `event`; anything else is `METHOD_NOT_FOUND`.
- The slot is provider-side and held to completion. `IN_FLIGHT = 64`
  (`src/transport/cartridge.rs:27`) is acquired at `:836` and released only
  after `handle` returns (`:841-843`). A caller timeout never touches it.
- The work is structurally uncancellable: `src/transport/cartridge.rs:924-933`
  runs the listener as `spawn_blocking(|| runtime.block_on(listener(data)))`,
  which runs to completion whatever happens to its handle.

So the caller's timer firing is precisely the failure this outcome names, and
it needs two changes in the host, not one: a cancel the provider can observe,
and a listener shape that can stop.

## Acceptance

- [ ] An expired bound sends the provider a cancellation it observes, rather
      than only dropping the caller's future.
- [ ] The provider's in-flight permit is released when a call is cancelled, so
      a cancelled call no longer consumes one of the 64 slots.
- [ ] The listener stops doing the cancelled work, or the plan states exactly
      why it cannot and what it costs.

## Known hazard

The comment at `src/transport/cartridge.rs:924-926` names a real deadlock that
the current `spawn_blocking(block_on(listener))` shape avoids. Whatever replaces
it must keep avoiding that deadlock; an analyst who cannot show it does is not
finished. This is the analysis this PRD owns.
