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
- "@runtime/the-runtime-reaches-top-tier-quality/no-panic-answers-a-recoverable-failure"
---

# Failures carry a type

## Outcome

Since `d2a761e` the host's `crate::error::Error` (`src/error.rs`) is a `thiserror` enum. The transport beneath it is not typed:

- `src/transport/cartridge.rs:27` aliases `Result<T> = Result<T, String>` across about 20 signatures (`validate`, `host`, `emit`, `bail`, `gather`, `ask`, `notify`, `subscribe`, `listen` and others).
- `src/transport/settings.rs` returns `Result<_, String>` from `check` and `apply`.
- On `origin/main`, `src/host/mod.rs:652` returns a per-entry `Result<Value, String>`.

`node.rs` turns that text into `mlua::Error::RuntimeError` (20 `external` sites) and the host into `Error::Remote` (8 sites). Without parsing prose, no caller can tell an undeclared event from a schema rejection, an unknown cartridge or a closed connection. No crate outside `cartridge.ctg` links the transport (checked `ws/*.ctg`). The listener `Outcome` enum is already typed and stays unchanged.

## Acceptance

- [ ] `rg -n 'Result<[^>]*, ?String>' src` finds nothing outside `src/cli`.
- [ ] `transport` has one `thiserror` enum. Each variant carries the event, cartridge, key or channel it failed on: at least undeclared event, schema rejection, unknown cartridge, connection closed and setting out of bounds. `crate::error::Error` converts from it with `From`, and `Error::Remote` is kept for text a peer answered.
- [ ] Wire frames keep their JSON shape. A local error becomes text once, where the reply frame is built. `src/transport/tests/cartridge.rs` asserts the rendered text of one variant.
- [ ] Tests that matched a local failure by string now match the variant. `just check runtime` and `just test runtime` pass from `/Users/feb/dev/cartridge`.

## Proof and recovery

Probe: `rg -n 'Result<' src/transport` and `rg -n 'contains\(' src/transport/tests .cartridge/tests/unit`. Record which string assertions exist. Convert the transport first and the host call sites second, in separate commits. Remote replies stay text, so a node built before this change still interoperates. Revert per commit.

## Review

[Review history](review.md): round 2/5 (1 inherited from the parent).
