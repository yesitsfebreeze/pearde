---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: passed
needs:
- "@runtime/the-runtime-reaches-top-tier-quality/the-in-flight-rewrite-lands-in-reviewable-commits"
---

# No panic answers a recoverable failure

## Outcome

A run-time failure in the host, a node or the transport reaches the caller as an error; it does not abort the process. The audited sites in `src/main.rs`, `src/runtime.rs`, `src/sdk.rs` and `src/loader.rs` were deleted by `d2a761e`/`939e7d1`. What remains on `origin/main` `ba198f4` (same set on local `e8a4da3`), outside tests:

- about 36 `lock().expect` calls on `std::sync::Mutex` in `transport/cartridge.rs`, `transport/rpc.rs`, `node.rs`, `trace.rs` and `host/process.rs`, although `parking_lot` is already a dependency (`host/mod.rs:18`);
- `transport/mod.rs:18` token generation panics when `getrandom` fails;
- `host/run.rs:108` `ledger.get(&path).expect("ledger entry")`;
- `node.rs:32` `RUNTIME.get().expect` when a native module thread calls before the node runtime is set;
- `transport/settings.rs:288` `declared` panics on a malformed document, and lines 94/100 unwrap a bound already matched.

About 20 other `expect`s name a local invariant and stay.

## Acceptance

- [ ] `cargo clippy --all-targets -- -W clippy::unwrap_used -W clippy::expect_used` (cwd `cartridge.ctg`) reports only test code and sites whose message names a local invariant. The before/after counts are recorded in the collection receipt.
- [ ] No `std::sync` lock is `expect`ed: shared state uses `parking_lot`.
- [ ] Unit tests under `.cartridge/tests/unit/` show four failures each returning an error value rather than panicking: token generation failure, a missing ledger entry, a malformed document passed to `declared`, and a call before the runtime is set.
- [ ] `just check runtime` and `just test runtime` pass from `/Users/feb/dev/cartridge`.

## Proof and recovery

Run the clippy command first and save its list. Land one mechanical commit per module on the reconciled line, with no wire or API change beyond `Result` returns. A module that regresses is reverted alone. If `declared` is only ever called with a compile-time `include_str!`, a documented invariant replaces the error.

## Review

[Review history](review.md): round 2/5 (1 inherited from the parent).
