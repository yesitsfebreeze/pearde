# The unit suite runs offline in under a minute — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/the-unit-suite-runs-offline-in-under-a-minute` (`prd.md`).
Scope: one leaf. `just test runtime` is offline, hermetic, uses one test layout and runs under 60 s.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **REBASE**.

Delivered by the rewrite:
- `.cartridge/tests/unit/src/tests/folders.rs` (the Bun/submodule test) is gone;
- `settle()` is gone, and the remaining `sleep`s in `tests/host.rs` are bounded polling loops;
- `cartridge.ctg/justfile` `test` is `cargo test --workspace` with no Bun step.

Still open on `ba198f4`:
- Two test layouts. Six `#[path]` modules point into `.cartridge/tests/unit/`, and `src/transport/tests/` has six files. This conflicts with decision `cartridge-repositories-keep-records-and-executable-memos`.
- An orphaned Bun integration test, `.cartridge/tests/integration/tool-observations.test.ts`, uses the removed `op:"call"` wire.
- Host tests boot in the real `/tmp/cartridge-<uid>`: `host/socket.rs::base`, with no test override found by `rg`.
- Wall time has not been measured since `bd3b5e7`.

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `645eb0c7885468325d48cf036f1a7cc5ccd41ba42adfe8ff5622d3edf5ec2a6e`. Prior text: `1dbcff8b5532f626119ac650c65b6c350cdf980dbc4e6458ab219a6686e674a6`.
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 19 | A hermetic, fast gate is what every other leaf's verification relies on; the delivered parts were removed from scope. −1. |
| Ownership and reuse | 18 | Runtime-owned; follows the recorded test-location decision. −2: the socket-base injection touches `host/socket.rs`, shared with other leaves. |
| Dependencies and slices | 18 | Hard need on the landing leaf; file move and socket base land as separate commits. −2: the time target may need a further split after measurement. |
| Acceptance and baseline | 17 | Offline command with a cwd, a before/after listing, a layout rule, a disposition for the TS test. −3: "warm registry" and the 60 s wall time depend on the machine; the baseline is not yet measured. |
| Failure and compatibility | 18 | Revert per commit; the 48-byte `base()` filter pitfall is named. −2: about 320 words, above the 300 aim. |
| Reviewer total | 90 / 100 | |

Result: **PASS**.
Findings: non-blocking — record the measured baseline before specs.
Unresolved blocking findings: none.
Disposition: keep (rebased).
Validation (read-only):
- `rg '#\[path'` and `rg 'settle|sleep|bun|Command::new'` over the tests;
- `ls .cartridge/tests`;
- `rg 'XDG_RUNTIME_DIR|set_var'` in the tests;
- a read of `host/socket.rs:30-57` and the `cartridge.ctg/justfile`;
- `shasum -a 256`.

Tests were not run.
User rating: not required; none supplied.
Rounds used / remaining: 2 / 3.
Next action: wait for the landing leaf, then measure.
