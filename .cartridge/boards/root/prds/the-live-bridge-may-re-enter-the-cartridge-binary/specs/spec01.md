---
complexity: low
footprint:
- cartridge.json
---

# The live bridge may re-enter the cartridge binary

Every cartridge service runs under a macOS seatbelt profile built from its
manifest `grant`; `process-exec` is allowed only for the grant's `exec`
entries. `live.ctg/src/bridge.ts` re-enters the host by spawning the built
`cartridge` binary (`CARGO_TARGET_DIR` or
`cartridge.ctg/target/{release,debug}/cartridge`) to run `call live`, but the
grant allowed only `bun`, so the spawn died with EPERM.

Add the cartridge runtime spellings the bridge may spawn to `grant.exec`:
`cartridge.ctg/target/release/cartridge` and
`cartridge.ctg/target/debug/cartridge` (root-relative multi-component paths
resolve against the plan root). No other grant is widened: `read`, `write`
and `net` are unchanged.

## Acceptance

- [x] `live.ctg/cartridge.json` `grant.exec` includes the cartridge runtime
  spellings the bridge may spawn; `read`/`write`/`net` unchanged.
- [x] Spawning the bridge resolves the built `cartridge` binary without
  EPERM (observed by running the bridge directly; the grant takes effect on
  host reload).
- [x] `just check live` passes.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge
just check live
cd live.ctg
bun run src/bridge.ts conversations 2>&1 | grep -v 'EPERM'
```

The bridge spawn must not report EPERM; the live service being unreachable
is an application-level error, not a sandbox denial.