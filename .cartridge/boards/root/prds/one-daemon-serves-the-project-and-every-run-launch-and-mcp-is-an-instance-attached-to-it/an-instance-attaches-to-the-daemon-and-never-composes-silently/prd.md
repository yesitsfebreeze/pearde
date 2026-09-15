---
state: open
origin: requested
priority: 90
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
capability-owner: runtime
needs: []
footprint:
- "src/cli/host.rs"
- "src/cli/client.rs"
- "src/host/run.rs"
- "src/host/mod.rs"
- "src/transport/typed.rs"
- ".cartridge/docs/"
---

# An instance attaches to the daemon and never composes silently

Child of `one-daemon-serves-the-project-and-every-run-launch-and-mcp-is-an-instance-attached-to-it`.
Covers its "Host attach" analysis item. The parent's Findings name the exact
code paths; this child changes only the attach/start contract, not any
per-cartridge state.

## Outcome

`run`, `call`, `launch` and `mcp` are instances: each finds the daemon through
the project's `host.sock` and sends its events there, or starts the daemon when
none answers — and never starts nodes of its own as a silent fallback. A second
daemon on the same project refuses instead of running nodeless. `unpublish`
removes only a socket it owns. Stopping the daemon uses one documented command,
so no test kills daemons by process name.

## Findings (cartridge.ctg, 2026-09-15)

- `run`, `launch` and `mcp` try `host.sock` first (`src/cli/host.rs:65`,
  `:89-91`, `:150-163`). `client::served` turns every connect or auth error
  into `None` (`src/cli/client.rs:44-46`), which silently starts their own
  composition (`host.rs:72-74`, `:98-110`; `src/host/run.rs:23-59`).
- A second `daemon` never checks for a first one. The bind returns
  `AlreadyRunning`, which it only logs, then keeps running with no nodes
  (`host.rs:240-269`; `src/transport/typed.rs:902-916`).
- `unpublish` deletes `host.sock` without checking ownership
  (`src/host/mod.rs:106-112`, `:567-569`). Any fallback host or losing daemon
  that exits removes the real daemon's socket path, which is the main cause
  of the many compositions observed on 2026-09-15.
- Nothing in cartridge.ctg starts a daemon; `live.ctg/src/launch.ts:46-52`
  spawns `--yolo daemon` undetached when `status` fails (that is the live
  child's to fix, but the attach contract here must make attach-from-a-process
  possible without spawning).

## What changes

- `client::served` distinguishes "no daemon answers" from connect/auth errors:
  only the former may auto-start; an error on a live socket fails loudly.
- An auto-start races two instances started concurrently: both must end up
  attached to the one daemon that won the bind (atomic bind or lockfile).
- A second `daemon` exits non-zero with a clear message when the socket answers
  or the bind says `AlreadyRunning`; it never runs nodeless.
- `unpublish` records socket ownership (pid or lock beside the socket) and
  removes only its own; a losing daemon leaves the winner's socket alone.
- One documented stop command (`cartridge daemon --stop` or equivalent) that
  a test or tool uses; document it beside `daemon` in `.cartridge/docs/`.

## Open questions carried from the parent

- Does `launch` keep its agent process and tmux window while its proxy
  listener stays in the daemon, with the agent pointed at the daemon's proxy
  address? Answer here or in the live child; record where it lands.
- Do solo hosts (`verify_one`, test hosts) stay self-contained so gates never
  depend on a developer's live daemon? The contract must keep them working;
  record the answer here.

## Acceptance

- [ ] With a daemon running, a `run`/`call` whose socket connect fails with an
      error does not start a node process (count `cartridge node` children
      before and after); it reports the error.
- [ ] A second `cartridge daemon` on the same project exits non-zero without
      removing or replacing the first's socket, and the first still serves.
- [ ] A fallback host or losing daemon exiting does not delete a live
      daemon's `host.sock` (verified by owning-pid check).
- [ ] Two instances started concurrently with no daemon end up sharing one
      daemon (matches parent Acceptance box 4).
- [ ] One stop command is documented and works; no new code kills daemons by
      process name.