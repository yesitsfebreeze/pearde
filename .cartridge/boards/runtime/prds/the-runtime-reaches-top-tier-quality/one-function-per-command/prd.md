---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
---

# One function per command

## Outcome

`src/main.rs` is a thin dispatcher. Each CLI command is a function that takes parsed arguments and returns a result, so a command can be unit tested without spawning the binary, and no function in the crate exceeds about 80 lines without a comment saying why.

## Findings to close

- `src/main.rs` is 1676 lines; `main()` at line 1326 is a 350-line `match` whose arms inline process spawning, socket I/O, signal handling, and table rendering.
- `src/main.rs:hosted_node` 129 lines, `settings_table` 83 lines.
- `src/evidence.rs:collect` 172 lines.
- `src/socket.rs:client` 166 lines.
- `src/cartridge.rs:handle` 162 lines and `start` 149 lines.

## Acceptance

- [ ] `main()` is under 60 lines: parse, settle settings, dispatch.
- [ ] Each `Command` variant maps to one `async fn run_<command>(args, host) -> Result<ExitCode, Error>` in its own module under `src/cli/`; `src/main.rs` is under 200 lines.
- [ ] Each listed function above is split so that the largest remaining function is under 80 lines or carries a comment naming the invariant that keeps it whole.
- [ ] At least one direct unit test per command function that does not spawn the binary (`run`, `daemon`, `call`, `status`, `settings`, `help`, `sweep`).
- [ ] `cargo test` time does not increase.
