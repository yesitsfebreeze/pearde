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
---

# The host logs through tracing

## Outcome

Diagnostics go through `tracing` with levels and structured fields, selectable at run time by `RUST_LOG` or a declared setting, instead of 33 `eprintln!` calls in `src/main.rs` and one in `src/settings.rs`. The debug tap no longer performs blocking file I/O on a Tokio worker.

## Findings to close

- `src/main.rs` has 33 `eprintln!` sites with no level, no target, and no way to silence or raise them.
- `src/lua.rs:134-160` the debug tap opens and appends to the log file synchronously inside a spawned async task, once per message; use `tokio::fs` or a `spawn_blocking` writer with a channel.
- `src/trace.rs:195-235` the trace sink writes and rotates with `std::fs` from async callers.

## Acceptance

- [ ] `grep -c 'eprintln!' src/*.rs` is zero outside the CLI's final user-facing output (usage errors, `cartridge settings` tables).
- [ ] `tracing` and `tracing-subscriber` are dependencies; the subscriber is installed once in `main` and honors `RUST_LOG`.
- [ ] Startup, replacement, socket accept/close, child spawn/exit, and every error path log at an appropriate level with the entry id as a field.
- [ ] No `std::fs` write happens on a Tokio worker in `lua.rs` or `trace.rs`; a test on a multi-thread runtime with `tokio::task::block_in_place` disabled proves it.
- [ ] `cartridge tail` and the debug log keep their current line format.
