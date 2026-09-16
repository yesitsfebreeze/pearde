---
state: "specced"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/live.ctg"
---

# the live bridge may re-enter the cartridge binary

## Outcome

A `tool.live` call from any harness reaches live's HTTP surface instead of dying at spawn with `EPERM: operation not permitted, posix_spawn '.../cartridge.ctg/target/release/cartridge'`.

## Reason

Every cartridge service runs under a macOS seatbelt profile built from its manifest `grant` (`cartridge.ctg/src/sandbox/mod.rs::profile`); `process-exec` is allowed only for the grant's `exec` entries resolved to literals (`granted_exec`, `cartridge.ctg/src/sandbox/mod.rs:151`). `live.ctg/cartridge.json` grants only `exec: ["bun"]`, but `live.ctg/src/bridge.ts:16-20` re-enters the host by spawning the built `cartridge` binary (`CARGO_TARGET_DIR` or `cartridge.ctg/target/{release,debug}/cartridge`) to run `call live`. The spawn is therefore denied by live's own sandbox. Confirmed 2026-09-16: `live {op:"conversations"}` fails with EPERM while the live bun process is running and serving.

## Acceptance

- [x] `live.ctg/cartridge.json` `grant.exec` includes the cartridge runtime spellings the bridge may spawn: `cartridge.ctg/target/release/cartridge` and `cartridge.ctg/target/debug/cartridge` (root-relative multi-component paths resolve against the plan root, `sandbox/mod.rs:153-158`).
- [ ] `tool.live` `conversations` returns live state through a Claude MCP session in this workspace (no EPERM).
- [x] `cd live.ctg && just check` passes.
- [x] No other grant widened: `read`/`write`/`net` unchanged.

## Observed 2026-09-16

Grant, bridge spellings and `just check live` verified; committed at
live.ctg 6c73e52. The MCP-session box stays open: no live service is running
(`cartridge call live` reports no active listener) and the composed host still
serves the pre-change snapshot, so the new grant takes effect only after a
reload. Running the bridge directly spawns the built binary with no EPERM.

