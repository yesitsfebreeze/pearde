---
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: delivered-pending-verification
needs:
- "@runtime/launch-authority"
- "@runtime/the-runtime-reaches-top-tier-quality/lua-calls-into-the-host-without-blocking-a-worker"
---

# A Lua cartridge runs in a restricted environment

## Outcome

A Lua cartridge gets the same confinement story a process cartridge gets: nothing beyond its grant. Today `src/lua.rs:63` creates the state with `Lua::new()`, which loads the full safe standard library including `os` and `io`, so any Lua cartridge can execute commands, read and write arbitrary files, and reach the environment while the docs say a cartridge "reaching outside what it declared is stopped by the OS". The sandbox in `src/sandbox.rs` is written for process children, but at `b4d553f` nothing calls it: `src/cartridge.rs` spawns with a plain `Command::new`, so `cartridge.process` is an unconfined escape from any Lua confinement. `launch-authority` owns routing launches through `sandbox::command`; the async Lua bridge rewrites the call sites the time limit must mark.

## Acceptance

- [ ] The Lua state is built with an explicit `StdLib` set: `os`, `io`, `package`, `debug`, and `load`/`loadstring`/`dofile`/`require` are absent unless the manifest grant asks for them.
- [ ] A grant with `read`/`write`/`exec` lists installs a restricted `io`/`os` table that checks paths against the grant with the same `granted_paths` rendering `src/sandbox.rs` uses for process cartridges.
- [ ] The Lua fixtures in `.cartridge/tests/unit/src/tests/` still load; a new test proves `os.execute` and `io.open("/etc/passwd")` fail in an ungranted cartridge.
- [ ] `docs/architecture.txt` PERMISSIONS section and the `src/sandbox.rs` module doc state what confines Lua and what confines processes, separately.
- [ ] Memory and instruction limits: the state has `set_memory_limit` and a hook that aborts a Lua function running longer than a declared `host` setting, with the setting declared in `settings.json`.

## Review

[Review history](review.md): round 2/5, reconciled DELIVERED at `e8a4da3`/`ba198f4`; round-1 hold and spec01 are historical.
