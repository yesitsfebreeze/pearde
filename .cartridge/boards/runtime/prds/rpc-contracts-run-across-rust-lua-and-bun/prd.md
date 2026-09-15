---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: rpc-contracts-run-across-rust-lua-and-bun
footprint:
- /Users/feb/dev/cartridge/cartridge.ctg/src/node.rs
- /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs
- /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/tests/fixtures/values.json
---

# Lua listeners and spawned helpers keep JSON values and pending requests intact

Since `ee7e295` only the base speaks the transport. Other languages meet it in `src/node.rs` at two points: the JSON↔Lua value conversion and the `cartridge.spawn` line protocol. Neither has tests for exact values, or for a helper that exits during a request. `src/transport/tests/rpc.rs` and `host.rs` already cover ids, error objects, notifications, closed waiters, oversized frames and `timed_out`.

## Acceptance

- [ ] A committed `values.json` holds null members, false, `[]`, `{}`, nested empties, non-BMP text and 2^53, with no top-level `id`. It round-trips through a real Lua listener, and as `reply.data` through a shell helper. Each case returns equal JSON, or the send fails naming that case.
- [ ] A helper that exits with three requests pending fails each one within 1 s under a 30 s `timeout_ms`. A request made after it exits fails just as fast. The helper stays marked closed.
- [ ] Concurrent requests to a helper that answers in reverse order each get their own reply. A line with an unknown id goes to `on_line`.

## Proof and recovery

Probe first. The reader loop in `node.rs` stops at EOF but leaves `pending` alive, so waiters probably sit out the full timeout. Start the helper under the sandbox before anything else: macOS `/bin/sh` execs `/bin/bash`, so grant `/bin/sh`, `/bin/bash` and `/bin/zsh`, and use shell builtins only. Name the new tests `a_spawned_…`. Gates, run in `cartridge.ctg`: `cargo test --workspace a_spawned` and `cargo test --workspace`. No Bun and no network. Changes are confined to `node.rs`, and the helper API is unchanged.

## Dependencies and review

No hard `needs`. The unported `wire.ts` copies are out of scope. [Review](review.md) is at round 3 of 5, inheriting round 1 from the root draft.
