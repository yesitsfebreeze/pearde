---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: rollup
review-round: 1
review-status: failed
needs:
- "@runtime/ci-proves-the-supported-terminal-matrix"
- "@runtime/linux-policy"
---

# The runtime reaches top-tier quality

## Outcome

The runtime in `cartridge.ctg` reads, fails, logs and tests the way a mature Rust service does. No worker thread is parked to bridge Lua into async code, and no recoverable failure panics. Every error has a type, logs have levels, and Lua cartridges are confined like process cartridges. The unit suite runs offline in under a minute, and the documents describe the checkout they sit in. This container coordinates the child outcomes below and records their combined evidence. It is done when every child is collected and a repeat of the audit finds nothing new.

## Context

The audit ran on 2026-09-14 against `bd3b5e7` (2026-09-13) plus uncommitted changes. Three later commits changed the audited code: d2a761e (async Lua, typed errors, tracing, sandboxed interpreter), 939e7d1 (host rewritten on the transport) and c9ef10b (yielding Lua bridge). The children still cite deleted files such as `src/context.rs`, `runtime::Error` and a 33-`eprintln!` `src/main.rs`.

Re-measured at `c9ef10b` (source reading only; tests not run):

- `src/error.rs` is a `thiserror` enum.
- `Result<_, String>`: 3 occurrences, all in `src/transport`.
- `eprintln!`: 5 occurrences, all in `src/cli`.
- `.unwrap()`/`.expect(`: 159 occurrences in `src`.
- `src/main.rs` is 8 lines.
- `src/lua.rs` drops `io`, `package` and file loaders.
- `block_in_place` remains at `src/node.rs:35`.
- Socket files are created `0600`.

Each child must be reconciled (CURRENT, REBASE or DELIVERED) before it is claimed. `ci-proves-the-supported-terminal-matrix` (no CI exists) and `linux-policy` (Linux still refuses) remain real prerequisites.

## Children, in suggested order

the-in-flight-rewrite-lands-in-reviewable-commits, no-panic-answers-a-recoverable-failure, failures-carry-a-type, the-host-logs-through-tracing, lua-calls-into-the-host-without-blocking-a-worker, a-lua-cartridge-runs-in-a-restricted-environment, the-socket-name-is-stable-and-the-file-is-private, stream-and-process-edges-are-bounded-and-loud, one-function-per-command, the-unit-suite-runs-offline-in-under-a-minute, dependencies-are-released-and-current, the-shipped-policy-defaults-to-ask, the-documents-describe-this-checkout.

## Acceptance

- [ ] Every child is reconciled against `c9ef10b` or later, then done with a collection receipt or retired with evidence.
- [ ] `just check runtime` and `just test runtime` pass from `/Users/feb/dev/cartridge` on a clean checkout with no network and no sibling repository beyond the recorded submodules.
- [ ] A repeat of the audit (unwrap/expect count, `Result<_, String>` count, `eprintln!` count, longest function, docs cross-check) shows each number at or below the target its reconciled child names.

## Review

[Review history](review.md): round 1/5.
