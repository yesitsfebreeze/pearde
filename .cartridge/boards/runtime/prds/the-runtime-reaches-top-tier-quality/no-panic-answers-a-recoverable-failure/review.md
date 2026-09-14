# No panic answers a recoverable failure — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/no-panic-answers-a-recoverable-failure` (`prd.md`).
Scope: one leaf. Run-time failures return errors instead of panicking.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **REBASE**. Every cited site is in a file deleted or rewritten by `d2a761e`/`939e7d1`: `src/main.rs:156-345`, `src/lua.rs:64-402`, `src/runtime.rs:337`, `src/sdk.rs`, `src/loader.rs:610/1007/1032`. The outcome is still wanted.

Re-measured on `origin/main` `ba198f4` with `rg`, outside `src/transport/tests`: 65 `unwrap`/`expect` sites. That includes 3 in `cli/manual.rs`'s test module and about 36 `std::sync` lock expects, while `parking_lot` is already used in `host/mod.rs:18`. The non-lock recoverable sites are listed in the revision. Local `main` `e8a4da3` has the same set, shifted by a line.

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `c20313df2a82a22fc03d5aa566fdd02e8d24a22955012481f65469c3c2720095`. Prior text: `56d05c61a537e3ac344c3cc3b5186a7eb4a6892a90e3d00c36e0505bf771d5f6`.
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 18 | A token, ledger or native-thread failure aborts a node or the base today. −2: several sites are near-invariants, so the user-visible gain is modest. |
| Ownership and reuse | 19 | Runtime-owned. Reuses `parking_lot` and clippy's `unwrap_used`/`expect_used`. −1: touches the same files as `failures-carry-a-type`, whose order is stated. |
| Dependencies and slices | 18 | Hard need on the landing leaf resolves; acyclic. −2: per-module commits are named but not enumerated. |
| Acceptance and baseline | 18 | Recorded clippy baseline, four named failure tests, gates with a cwd. −2: "message names a local invariant" is reviewer judgment. |
| Failure and compatibility | 18 | Mechanical, revertible per module, no wire change, `include_str!` escape named. −2: no measure that lock replacement leaves contention unchanged. |
| Reviewer total | 91 / 100 | |

Result: **PASS**.
Findings: the rebased site list replaces the stale one.
Unresolved blocking findings: none.
Disposition: keep (rebased).
Validation (read-only):
- `rg -n '\.unwrap\(\)|\.expect\('` on both lines;
- reads of `transport/mod.rs:12-20`, `transport/settings.rs:85-102,280-290`, `host/run.rs:100-112` and `node.rs:25-40`;
- `rg parking_lot`;
- `shasum -a 256`.

No product gates were run.
User rating: not required; none supplied.
Rounds used / remaining: 2 / 3.
Next action: wait for the landing leaf, then run the clippy probe.
