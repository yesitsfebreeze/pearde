# Dependencies are released and current — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/dependencies-are-released-and-current` (`prd.md`).
Scope: one leaf. Released pins, edition 2024, clippy pedantic, and dependency checks in `just check runtime`.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **REBASE**. This is a minor rebase, because the core findings are still current on both lines:
- `Cargo.toml` has `notify = "9.0.0-rc.5"`, `edition = "2021"` and `rust-version = "1.89"`;
- `[lints.rust]` exists, but there is no `[lints.clippy]`.

What is stale:
- The finding "`thiserror` used in one file" is stale: it appears in 3 files and backs `src/error.rs`.
- `sha2` exists only on local `main` (trust).
- The prior text had no proof, recovery or gate cwd.

Tools present locally: `cargo-deny 0.20.2` and `cargo-machete 0.9.2`; `cargo audit` is absent. The registry cache holds `notify` 8.2.0 and 9.0.0-rc.5. No test covers `src/host/watch.rs`.

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `3e9ea579b6026c1d6907e1c8799914d2c2ab14c9135145dbee4e6e121312fcae`. Prior text: `de54660851dad1fb3e5b4fbca2aa9b6e9beced5e33e5f3b530a153a2d0165aa8`.
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 17 | A production release candidate plus missing lint and supply-chain checks. −3: hygiene work with no user-visible behavior. |
| Ownership and reuse | 20 | Runtime-owned; reuses installed `cargo-deny` and `cargo-machete` and the existing `check` recipe. |
| Dependencies and slices | 18 | Hard need on the landing leaf, because `Cargo.toml`/`Cargo.lock` changed on both lines; three independent commits. −2. |
| Acceptance and baseline | 19 | Four checks with a cwd, and the missing watcher test is made explicit. −1: the "released 9.x if published" branch is decided at implementation time. |
| Failure and compatibility | 19 | The rc pin is kept with a recorded reason if the watcher breaks; the advisories check is kept out of the offline gate. −1. |
| Reviewer total | 93 / 100 | |

Result: **PASS**.
Findings: the stale `thiserror`/`sha2` finding was replaced; a watcher test was added as a prerequisite for the bump.
Unresolved blocking findings: none.
Disposition: keep (rebased).
Validation (read-only):
- a read of `Cargo.toml` on both lines;
- `rg -l` per dependency crate over `src` on `ba198f4`;
- `cargo deny --version`, `cargo machete --version` and `cargo audit --version` (absent);
- `ls ~/.cargo/registry/cache/*/ | grep notify`;
- `rg` for watch tests;
- `shasum -a 256`.

No product gates were run.
User rating: not required; none supplied.
Rounds used / remaining: 2 / 3.
Next action: wait for the landing leaf.
