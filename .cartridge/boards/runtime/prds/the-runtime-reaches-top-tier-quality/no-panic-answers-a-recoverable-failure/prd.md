---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
---

# No panic answers a recoverable failure

## Outcome

Every `unwrap`, `expect`, and slice index on a path that can fail at run time is replaced by an error the caller receives, and every silently dropped failure is reported. A missing binary, an unwritable directory, a malformed value, or a closed channel is a result, not an abort.

## Findings to close

- `src/main.rs:156` `random_hex` opens `/dev/urandom` with `expect`; use `getrandom` or `std::random` and return an error.
- `src/main.rs:182` `spawn` turns non-string JSON env values into empty strings via `unwrap_or_default`; refuse the launch spec instead.
- `src/main.rs:260-264` `hosted_node` discards the write error when recording its PID.
- `src/main.rs:329` `expect("node paths serialize")`.
- `src/main.rs:345` `reentry.spawn().expect("re-enter the resolver")` aborts the whole hosted node when the next node cannot spawn.
- `src/lua.rs:64-99` several `expect` calls in `Host::new`; return `Result` from the constructor.
- `src/lua.rs:134` `expect("debug log parent")`.
- `src/lua.rs:402` `downcast_ref::<Service>().unwrap()`.
- `src/runtime.rs:337` `reg.fibers[&uid]` indexes without a check; use `get` and an error.
- `src/sdk.rs:357-359` child stdio taken with `expect`.
- `src/sdk.rs:128` a tool descriptor that is not valid JSON silently becomes `Null`.
- `src/loader.rs:610` `path.parent().unwrap()` re-derives `root` that line 603 already computed; `src/loader.rs:1007` `ledger.get(...).expect("ledger entry")`.
- `src/loader.rs:315,709,738,1468` the same script-extension check is written four times; one helper.
- `src/loader.rs:1032` `insert(0, _)` inside a loop; build in reverse or use a `VecDeque`.

## Acceptance

- [ ] `grep -nE 'unwrap\(\)|expect\(|\[&' src/*.rs` lists only sites with a comment proving the invariant (lock poisoning under `parking_lot` does not apply; static tables; tests).
- [ ] Each listed site above has a test that drives the failing input and asserts an error value, not a panic.
- [ ] The hosted node exits non-zero with the spawn error on stderr when the next node's binary is missing.
- [ ] A launch spec with a numeric env value is refused with a message naming the key.

## Proof and recovery

`cargo clippy -- -W clippy::unwrap_used -W clippy::expect_used -W clippy::indexing_slicing` gives the full list; consider keeping those lints at `warn` in `Cargo.toml` once the count is zero.
