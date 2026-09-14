---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
needs:
- "@runtime/ci-proves-the-supported-terminal-matrix"
- "@runtime/linux-policy"
---

# The runtime reaches top-tier quality

## Outcome

The runtime in `cartridge.ctg` reads, fails, logs, and tests the way a mature Rust service does: no worker thread is parked to bridge Lua into async code, no recoverable failure panics, every error has a type, logs have levels, Lua cartridges are confined like process cartridges, the unit suite runs offline in under a minute, and the documents describe the checkout they sit in. This container coordinates the child outcomes below and records their combined evidence. It is done when every child is collected and the audit that produced them finds nothing new.

## Context

An audit on 2026-09-14 of the working tree at `bd3b5e7` plus uncommitted changes. Clippy was clean under `warnings = deny`, 191 of 192 unit tests passed, and the one failure was an environment-dependent test. The findings are split into the children. Two existing PRDs already own adjacent gaps and are prerequisites rather than duplicates: `ci-proves-the-supported-terminal-matrix` (there is no CI at all today) and `linux-policy` (`src/sandbox_linux.rs` refuses every process cartridge).

## Suggested order

1. the-in-flight-rewrite-lands-in-reviewable-commits
2. no-panic-answers-a-recoverable-failure
3. failures-carry-a-type
4. the-host-logs-through-tracing
5. lua-calls-into-the-host-without-blocking-a-worker
6. a-lua-cartridge-runs-in-a-restricted-environment
7. the-socket-name-is-stable-and-the-file-is-private
8. stream-and-process-edges-are-bounded-and-loud
9. one-function-per-command
10. the-unit-suite-runs-offline-in-under-a-minute
11. dependencies-are-released-and-current
12. the-shipped-policy-defaults-to-ask
13. the-documents-describe-this-checkout

## Acceptance

- [ ] Every child PRD is done with a collection receipt.
- [ ] `just check runtime` and `just test runtime` pass from a clean checkout with no network and no sibling repository beyond the recorded submodules.
- [ ] A repeat of the audit (unwrap/expect count, `Result<_, String>` count, `eprintln!` count, longest function, docs cross-check) shows each number at or below the target its child names.
