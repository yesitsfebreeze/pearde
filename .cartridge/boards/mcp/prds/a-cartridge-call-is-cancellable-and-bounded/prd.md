---
state: "open"
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/mcp.ctg"
---

# A cartridge call is cancellable and bounded

## Outcome

A caller that gives up on a cartridge call — timeout, cancellation, a turn that
ends — releases the resources of that call. Either the call finishes inside a
bound the caller can name per event, or the caller sees why it did not.

## Evidence

Observed 2026-09-16/17, session cartridge-8e and its dispatched workers. A
caller-side tokio timeout around a cartridge call is inert: the request keeps
running under the harness and holds the slot until the provider's own manifest
timeout fires. Worker agents died mid-turn to "harness did not answer in time"
with no way to cancel the underlying call, and repeated coordinator MCP calls
returned `mcp did not answer in time` while the daemon kept the work. The
recorded lesson (auto-memory "a caller cannot cancel a cartridge call") is that
bounds exist only when the provider's manifest declares `timeout_ms`; callers
have no bound of their own.

## Acceptance

- [ ] A caller that times out on a cartridge call observes the call abandoned
      (its slot and in-flight work released), not just its own timer fired.
- [ ] An event whose provider declares `timeout_ms` is bounded by that value
      without any caller-side timeout.
- [ ] A slow or wedged provider leaves the caller free to continue other work,
      and the wedged call's eventual result or failure is reported to the
      session rather than lost.

## Refinement (2026-09-17, coordinator cartridge-2e, from analyst-1)

This is a rollup, not a task. The analyst established against HEAD — not the
dirty working trees — that acceptance clause 1 cannot be met inside `mcp.ctg`
at all, and that the cartridge already ships MCP cancellation which is dead code
by construction.

The mechanism, all read with `git show <HEAD>:<path>`:

1. A caller-side bound tells the provider nothing.
   `cartridge.ctg/src/transport/cartridge.rs:389-393` wraps the RPC in
   `tokio::time::timeout`; expiry drops the future, and the only cleanup is
   `impl Drop for Waiting` (`src/transport/rpc.rs:292-304`), which removes the
   id from the caller's local pending map. No frame leaves the process.
2. Nothing in the protocol can cancel: `handle` matches exactly `apply`,
   `directory`, `dispose` and `event`.
3. The in-flight slot is provider-side and held to completion
   (`IN_FLIGHT = 64` at `transport/cartridge.rs:27`, acquired `:836`, released
   after `handle` returns `:841-843`).
4. The work is structurally uncancellable:
   `transport/cartridge.rs:924-933` runs the listener as
   `spawn_blocking(|| runtime.block_on(listener(data)))`.

So the caller's timer firing *is* clause 1's failure mode, and closing it needs
two host changes. Clause 2 already holds in the host, but `mcp.ctg`'s own `mcp`
event declares no `timeout_ms`, so every MCP line inherits the 60000 ms default
and fails as a bare `mcp did not answer in time`. Clause 3 does not hold: the
bridge is free, but one wedged `tool.*` call blocks every later MCP line behind
the Lua lock, and `Ctx::bail` (`:416-425`) discards the late answer.

Children, and the two host PRDs they need:

- `a-cancelled-tool-call-reaches-its-running-tool` (this board, 75) — make
  `service.rs:232-243` actually fire. Needs the runtime cancel.
- `the-mcp-event-declares-its-own-bound` (this board, 75) — declare `timeout_ms`
  on the `mcp` event. Landable today; the proxy sibling closes the proxy side of
  the same mechanism and neither widens into the other's cartridge.
- `@runtime/a-cartridge-call-can-be-cancelled` (75) — an expired bound sends a
  cancel the provider observes; permit and listener work released.
- `@runtime/a-wedged-call-reports-its-late-answer` (70) — needs the above;
  shares `transport/cartridge.rs`, so they land serially.

The host work went to the `runtime` board rather than into this footprint
because a cartridge owns one capability and declares its own surface. Two things
the analyst could not establish are written into the children that own them: the
queueing behind the Lua lock was never observed in a run, and nothing yet
designs what replaces `spawn_blocking(block_on(listener))` without reopening the
deadlock its own comment names.
