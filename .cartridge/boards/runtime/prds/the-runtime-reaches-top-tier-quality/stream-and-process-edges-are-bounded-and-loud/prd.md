---
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: superseded-recommend-retire
---

# Stream and process edges are bounded and loud

## Outcome

Every queue, counter, and identity in the stream and process layers has a stated bound and a visible failure. Nothing is dropped without a record.

## Findings to close

- `src/stream.rs:116` history replay uses `let _ = tx.try_send(...)`; an overflow loses envelopes with no notice. Either the capacity arithmetic in `src/settings.rs:514` (`subscriber_events = history_events + headroom`) guarantees room and a test proves it, or the drop is counted and the subscriber is told.
- `src/stream.rs:63-65` the per-channel byte total uses unchecked `+=`; use `saturating_add`.
- `src/stream.rs:185-196` a slow subscriber is detected at capacity `<= 1`, told once, and dropped; the SDK side (`src/sdk.rs:270-272`) does the same check in a different order. One shared rule, one test.
- `src/process.rs:45-57` `Child::drop` calls `start_kill` then spawns a wait task only if a runtime handle exists; on shutdown the task may never run and the child is not reaped. Reap synchronously in the shutdown path.
- `src/cartridge.rs:246-262` a process identity is the `Arc` pointer cast to `usize`. Replace with a monotonic id from an `AtomicU64`, the way `service.rs` already numbers versions.

## Acceptance

- [ ] A test fills a subscriber past `history_events + subscriber_headroom` and asserts either no loss or an explicit `lagged` frame with the count.
- [ ] A test drops a `Child` after the runtime has shut down and asserts the process is gone (`kill -0` fails) within the reap timeout.
- [ ] `process_id()` is an integer that survives moving the `Remote`; a test asserts reload tracking still matches after the value is moved into a new `Arc`.
- [ ] The slow-subscriber rule lives in one function used by both `stream.rs` and `sdk.rs`.
