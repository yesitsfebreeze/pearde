---
complexity: medium
footprint:
  - src/lua.rs
  - src/sandbox.rs
  - src/loader.rs
  - src/context.rs
  - src/settings.rs
  - settings.json
  - docs/architecture.txt
  - .cartridge/tests/unit/src/tests/mod.rs
  - .cartridge/tests/unit/src/tests/lua_sandbox.rs
  - .cartridge/tests/unit/src/tests/process.rs
---

# spec01 — Confine a Lua cartridge to its grant

## Probe

Source HEAD `b4d553f`, cwd `cartridge.ctg`. A disposable unit test loaded a bare
`p.lua` whose chunk ran `os.execute('touch <tmp>/executed')` and
`io.open('/etc/passwd')` through `Host::component`; with
`RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR=$PWD/target/lua-sandbox cargo test --lib probe_ungranted -- --nocapture`
it printed `PROBE loaded=true marker_exists=true`. The test was removed afterwards.

## Contract

One interpreter serves the profile and every Lua cartridge, so confinement is
per chunk environment, not per state.

- The state is `Lua::new_with(COROUTINE|TABLE|IO|OS|STRING|UTF8|MATH)`: no
  `package`, `require` or `debug` exist anywhere. `load`, `loadfile` and
  `dofile` are removed from globals.
- The profile's own `init.lua`/`config.lua` are evaluated against globals and
  keep `os`/`io`: they are the user's composition (`config.lua` reads
  `os.getenv`), stated as such in the docs.
- A cartridge chunk (`load_component`) is evaluated with `set_environment` on a
  fresh table: the pure base functions, `coroutine`, `string`, `table`, `math`,
  `utf8`, `cartridge`, `_G` pointing at itself. `os`, `io`, `collectgarbage`,
  `load*`, `dofile` are absent.
- `Declared` carries the manifest `grant` (bare `.lua`: empty) and its folder.
  A nonempty `read`/`write` installs `io.open`/`io.lines`; a nonempty
  `write`/`exec` installs `os`, with `os.remove`/`os.rename` (write) and
  `os.execute` (exec). Paths resolve relative to the cartridge folder, `..`
  components are refused, and the target's canonical spelling must lie under a
  `sandbox::granted_paths` form of a granted entry; the canonical path is what
  is opened. Read modes need read or write; `w`/`a`/`+` need write.
  `os.execute` splits argv without a shell, requires the program to resolve to
  a granted `exec` entry, and spawns through `sandbox::command` with the same
  grant (stdin/stdout null), returning `true|nil, "exit", code`.
- `host.lua_memory_bytes` (default 268435456) feeds `set_memory_limit`;
  `host.lua_call_ms` (default 60000) bounds one Rust-to-Lua entry, measured as
  wall time from the outermost entry on the OS thread (host calls it waits on
  count), enforced by a global instruction hook. Every Rust-to-Lua entry in
  `lua.rs`, `context.rs` and `loader.rs` goes through that entry mark.

Known ceilings, stated in docs: cartridges share library tables and the string
metatable (confined from the machine, not from each other); a check-then-open
race exists against a symlink swapped inside a writable grant.

## Acceptance

- [ ] An ungranted cartridge: `os`, `io`, `require`, `load`, `dofile`, `debug`, `package` are nil; `os.execute` and `io.open("/etc/passwd")` cannot run.
- [ ] A granted cartridge reads a granted file and writes a granted path; `/etc/passwd`, `..` escapes and write-mode opens on a read-only grant are refused; `os.execute` of an ungranted program is refused.
- [ ] A Lua loop past the call limit and an allocation past the memory limit both return errors; both keys are declared in `settings.json` and typed in `settings::Host`.
- [ ] Existing Lua fixtures still load: the full lib suite passes, with `process.rs`'s logging cartridge given a manifest `write` grant.
- [ ] `docs/architecture.txt` PERMISSIONS and the `src/sandbox.rs` module doc state Lua and process confinement separately.

## Verify and Proof

```sh
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR=/Users/feb/dev/cartridge/cartridge.ctg/target/lua-sandbox cargo test --lib
```

Recovery: the change is one commit on the lane; reverting it restores the
unconfined state. No stored data changes.
