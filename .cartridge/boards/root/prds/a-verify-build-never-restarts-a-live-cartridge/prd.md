---
state: "analyzing"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
footprint:
  - cartridge.ctg
  - .cartridge/memos/routine/cartridge-proxy.md
claim: "coordinator-c4-530 2026-09-16T09:33:52.383Z"
---

# a verify build never restarts a live cartridge

## Outcome

Since cartridge.ctg 771e046 the host hot-restarts a cartridge whenever the
target/debug dylib it loaded changes. A `cargo test` or `cargo clippy` run in a
submodule, such as collect's second Verify pass or a worker's gate, rewrites
that dylib and restarts live cartridges, which drops other sessions' in-flight
calls. Specs work around this today with an isolated `CARGO_TARGET_DIR`. The
host should restart only on a deliberate rebuild: for example, it loads a copy
of the dylib, or it reloads only on `cartridge reload` / `just proxy`, or on a
build marker that `cargo test` never writes. The analyst picks one and records
why.

## Acceptance

- [ ] With a daemon running, `cargo test` in a loaded cartridge's submodule using the default target dir leaves that cartridge's generation unchanged.
- [ ] The documented rebuild path (`just proxy` or `cartridge reload <id>`) still picks up a new build.
- [ ] `just test lifecycle` passes.
