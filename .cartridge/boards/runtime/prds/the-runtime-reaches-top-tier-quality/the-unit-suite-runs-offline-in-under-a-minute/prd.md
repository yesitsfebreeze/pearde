---
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: passed
needs:
- "@runtime/the-runtime-reaches-top-tier-quality/the-in-flight-rewrite-lands-in-reviewable-commits"
---

# The unit suite runs offline in under a minute

## Outcome

`just test runtime` (`cargo test --workspace` in `cartridge.ctg/justfile`) needs only Rust and the checkout, writes only to temporary directories, and finishes in under a minute. The rewrite already removed two problems: the Bun/submodule test `folders.rs` and the fixed `settle()` sleep (remaining sleeps are bounded polls). Still open on `origin/main` `ba198f4`:

- Two test layouts. Six modules use `#[path]` into `.cartridge/tests/unit/`. The transport uses `src/transport/tests/` (six files). The repository decision `cartridge-repositories-keep-records-and-executable-memos` puts tests under `.cartridge/tests/`.
- `.cartridge/tests/integration/tool-observations.test.ts` is a Bun test against the removed `op:"call"` wire, and no recipe runs it.
- Host tests build the `cartridge` binary and a native fixture with `cargo build` (`tests/mod.rs`), then boot hosts in the user's real socket directory (`/tmp/cartridge-<uid>`, `src/host/socket.rs`).
- Wall time has not been measured since the rewrite; it was 124 s at `bd3b5e7`.

## Acceptance

- [ ] From `/Users/feb/dev/cartridge`, `CARGO_NET_OFFLINE=true just test runtime` passes on a fresh clone with a warm `~/.cargo` registry and no sibling repositories. The receipt records wall time under 60 s and the ten slowest tests.
- [ ] The run leaves nothing new under `/tmp/cartridge-<uid>`, `$XDG_RUNTIME_DIR/cartridge` or `~/.cartridge`; a listing before and after proves it.
- [ ] Every test lives under `.cartridge/tests/unit/` with one `#[path]` depth convention, documented in `docs/development.txt`, and `src/transport/tests/` is gone.
- [ ] `.cartridge/tests/integration/` either runs from a recipe against the events wire or is deleted, with the reason in the commit message.

## Proof and recovery

Measure first with `time just test runtime`, and time each test binary separately to find the slow tests. Move the files in one commit and change the socket base in another. The socket base needs an injection point, such as a directory set by the test harness, because a `tempdir` path is too long for `base()`'s 48-byte filter. Revert per commit.

## Review

[Review history](review.md): round 2/5 (1 inherited from the parent).
