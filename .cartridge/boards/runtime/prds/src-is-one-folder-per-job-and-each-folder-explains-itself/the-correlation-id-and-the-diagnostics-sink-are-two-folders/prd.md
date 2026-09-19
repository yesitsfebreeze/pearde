---
state: "specced"
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
blast-radius: low
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/trace
  - /Users/feb/dev/cartridge/cartridge.ctg/src/log
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/cli/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/process.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/trace
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/log
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/architecture.txt
---

# the correlation id and the diagnostics sink are two folders

## Outcome

`src/trace/mod.rs` does two jobs in 472 lines, and a README for it would have to say so. The correlation id (`current`, `mint`, `of`, `stamp`, `scope`, `carry`) stays in `src/trace`. The diagnostics sink (`redact`, `Sink`, `Out`, `drain`, `flush`, `diagnostic`, `diagnostic_line`, `Layer`, `Fields`, `subscribe`) moves to `src/log`.

## Acceptance

- [ ] `src/trace` holds only the correlation id and `src/log` holds the sink, the layer and `subscribe`.
- [ ] Every caller names the new path (`cartridge::log::subscribe`, `cartridge::log::flush`, `crate::log::diagnostic_line`); nothing re-exports the old one.
- [ ] The sink tests in `.cartridge/tests/unit/src/trace/tests.rs` move with the code they test, to `.cartridge/tests/unit/src/log/tests.rs`.
- [ ] `src/trace/README.md` and `src/log/README.md` exist in the shape the parent's README child defines.
- [ ] `just test runtime` runs the same leaf test names as before, and all pass. The six sink tests now run under `log::tests::` instead of `trace::tests::`. `just check runtime` reports nothing.

## Proof and recovery

A move and a path rewrite, no behaviour change. `ASP.md` warns that "trace" means only the correlation id; this change makes the folder agree. Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`. Not run.

Landing: `src/cli/mod.rs` has another session's uncommitted `Command::Launch { passthrough }` hunk. That hunk needs that session's uncommitted `src/cli/args.rs` and `src/cli/host.rs` edits, which are outside this footprint. Collect commits every dirty path inside the footprint, so collecting now would produce a sha that does not build (E0026 and E0061).
- Precondition: collect only when `git -C cartridge.ctg diff --quiet -- src/cli/mod.rs` exits 0, run from the superproject. Until then, wait. If HEAD has moved, rebase the lane first.
- Recovery: if a receipt swept a foreign hunk anyway, build the collected sha in a throwaway worktree (`cargo check --lib --bins`, isolated `CARGO_TARGET_DIR`). If it fails, revert the foreign hunk or complete it with its owner before anything else lands. The spec's "Landing" section has the details.
