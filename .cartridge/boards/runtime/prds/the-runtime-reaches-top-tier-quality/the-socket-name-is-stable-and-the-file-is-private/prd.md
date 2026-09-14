---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: delivered-pending-verification
---

# The socket name is stable and the file is private

## Outcome

Any client built from any toolchain finds the daemon of a project, and only the user who started the daemon can connect to it.

## Findings to close

- `src/socket.rs:88` derives the socket name with `std::collections::hash_map::DefaultHasher`, whose algorithm the standard library documents as unstable across Rust versions. A client and a daemon built with different toolchains compute different names and never meet. `sha2` is already a dependency.
- `src/socket.rs:209` binds without setting a mode; privacy rests on the process umask. On macOS `XDG_RUNTIME_DIR` is unset, so the file lands in `/tmp`.
- `src/socket.rs:82-86` the 100-byte path threshold is a bare number; name the `sun_path` limit and produce an error, not a silent `/tmp` fallback, when the fallback is also too long.
- `src/socket.rs:168-171` `sweep` checks identity, probes, then unlinks; a socket replaced between the probe and the unlink is removed. Open the directory once and unlink by file descriptor relative to it, or compare inode before and after.

## Acceptance

- [ ] The socket name is a SHA-256 prefix of the canonical project path and the user; a test asserts the exact name for a fixed input.
- [ ] After bind the file is `chmod 0600` and a test asserts the mode.
- [ ] On macOS the socket lives under a per-user directory (`$TMPDIR` is per user on macOS, or `~/Library/Application Support/cartridge/run`), not `/tmp`.
- [ ] A sweep test that swaps the socket file between probe and unlink leaves the new file in place.
