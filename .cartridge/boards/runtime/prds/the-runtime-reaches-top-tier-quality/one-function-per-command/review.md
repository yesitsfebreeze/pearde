# One function per command — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/one-function-per-command` (`prd.md`; the heading was retitled to its remaining outcome and the slug is unchanged).
Scope: one leaf. No host function exceeds 80 lines without a reason.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **REBASE**. The dispatcher half was delivered by `d2a761e`: `src/main.rs` is 8 lines and calls `cli::main()`, and commands live in `src/cli/{args,client,host,listing,manual,project,settings,setup,trust}.rs`. Every audited long function was deleted (`hosted_node`, `evidence::collect`, `socket::client`, `cartridge::handle/start`).

A brace-depth scan over non-test `src` finds 8 functions over 80 lines on `ba198f4` and 8 on `e8a4da3`; the largest is `node::install` (192 / 148). The outcome was narrowed to function length, measured with clippy's `too_many_lines`.

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `7e5e5d8f044cefecd072d253ba443764d4121c90b5c9a404220b032c77acfabf`. Prior text: `fe7df355b0db25c8bd75cde1fd46036abf3ecb20c0e9666d3719bbf7e02edbc9`.
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 16 | A measurable audit target the parent names. −4: maintainability only, with no user-visible behavior. |
| Ownership and reuse | 19 | Runtime-owned; reuses clippy's lint instead of a custom scanner. −1: `node.rs`/`process.rs` overlap with `no-panic`. |
| Dependencies and slices | 18 | Hard need on the landing leaf; one commit per split. −2: the order among siblings touching `node.rs` is not stated. |
| Acceptance and baseline | 19 | Lint threshold, two named splits, same test count, gate with a cwd. −1: the baseline must be re-run on the reconciled head. |
| Failure and compatibility | 18 | Behavior-free and revertible; the "stays whole" exception is bounded. −2: about 310 words, above the 300 aim. |
| Reviewer total | 90 / 100 | |

Result: **PASS**.
Findings:
1. Non-blocking: the heading changed from "One function per command" because that part is delivered.
2. Non-blocking: land after `no-panic` to avoid churn in `node.rs`.

Unresolved blocking findings: none.
Disposition: keep (rebased).
Validation (read-only):
- `wc -l src/main.rs`;
- `ls src/cli`;
- an awk function-length scan over `src/**/*.rs` excluding `tests/`, on both lines;
- `shasum -a 256`.

No product gates or clippy runs.
User rating: not required; none supplied.
Rounds used / remaining: 2 / 3.
Next action: wait for the landing leaf.
