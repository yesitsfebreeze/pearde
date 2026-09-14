---
state: "analyzing"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
claim: "claude-opus-5 2026-09-14T10:01:06.849Z"
---

# A Lua cartridge runs in a restricted environment

## Outcome

A Lua cartridge gets the same confinement story a process cartridge gets: nothing beyond its grant. Today `src/lua.rs:63` creates the state with `Lua::new()`, which loads the full safe standard library including `os` and `io`, so any Lua cartridge can execute commands, read and write arbitrary files, and reach the environment while the docs say a cartridge "reaching outside what it declared is stopped by the OS". The sandbox in `src/sandbox.rs` only wraps process children.

## Acceptance

- [ ] The Lua state is built with an explicit `StdLib` set: `os`, `io`, `package`, `debug`, and `load`/`loadstring`/`dofile`/`require` are absent unless the manifest grant asks for them.
- [ ] A grant with `read`/`write`/`exec` lists installs a restricted `io`/`os` table that checks paths against the grant with the same `granted_paths` rendering `src/sandbox.rs` uses for process cartridges.
- [ ] The Lua fixtures in `.cartridge/tests/unit/src/tests/` still load; a new test proves `os.execute` and `io.open("/etc/passwd")` fail in an ungranted cartridge.
- [ ] `docs/architecture.txt` PERMISSIONS section and the `src/sandbox.rs` module doc state what confines Lua and what confines processes, separately.
- [ ] Memory and instruction limits: the state has `set_memory_limit` and a hook that aborts a Lua function running longer than a declared `host` setting, with the setting declared in `settings.json`.
