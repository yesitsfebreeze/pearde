# The host logs through tracing — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/the-host-logs-through-tracing` (`prd.md`).
Scope: one leaf. Diagnostics use `tracing` with levels chosen at run time.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **DELIVERED** (pending verification).

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `c3e2dab1032c3ba7c7eabda90684675e93e637a662d3f2c0cb6ba077766e5def` (frontmatter only; prior text `59f4d925299d377c7feb8d7f184f56d378562317194834157eeba155d1b1e4c9`).
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

Evidence, identical on both lines, from `d2a761e`:
- `Cargo.toml` declares `tracing = "0.1"` and `tracing-subscriber` (fmt, env-filter).
- `src/trace.rs::subscribe` installs the subscriber once, from `cli::main` (`src/cli/mod.rs:38`). Its filter comes from `CARTRIDGE_LOG` (default `warn`), documented in `.cartridge/README.md:39` and `docs/development.txt:43`.
- `tracing` macros are used in `node.rs`, `host/mod.rs`, `host/watch.rs`, `cli/host.rs`, `cli/settings.rs` and `settings/host.rs`.
- `eprintln!` is down from 33 to 5: `cli/mod.rs:26` (`fail`), `cli/setup.rs:83,124` and `cli/manual.rs:381,396`. All are final user-facing CLI output, which the acceptance exempts.
- The synchronous debug tap in `src/lua.rs:134-160` is deleted.

Residual gaps, not blocking:
- `trace.rs::Sink::write` still writes and rotates the diagnostic file with `std::fs` under a mutex. It is disabled unless `CARTRIDGE_DIAGNOSTICS` is set, and capped by `diagnostics_max_bytes`.
- The variable is `CARTRIDGE_LOG`, not `RUST_LOG`.
- No test covers the log line format.

Result: no score (verdict round). Status: `delivered-pending-verification`.
Unresolved blocking findings: none.
Validation (read-only):
- `rg -c 'eprintln!'` and the tracing macro counts on both lines;
- reads of `src/trace.rs:1-30,130-240,435-455`, `src/cli/setup.rs:75-130` and `src/cli/manual.rs:375-400`;
- `rg CARTRIDGE_LOG` in the docs;
- `shasum -a 256`.

Tests were not run.
Rounds used / remaining: 2 / 3.
Next action: collect. If the `std::fs` sink matters, open a new small leaf rather than reopen this one.
