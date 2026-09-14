# Failures carry a type — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/failures-carry-a-type` (`prd.md`).
Scope: one leaf. Transport failures are enum values.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **REBASE**. The host half was delivered by `d2a761e`: `src/error.rs` is a `thiserror` enum. The PRD's module list is gone: `loader`, `settings`, `cartridge`, `socket`, `stream`, `sdk`, and `runtime::Error` as the top type.

The untyped remainder is the transport, on both lines:
- `src/transport/cartridge.rs:27` has `pub type Result<T> = std::result::Result<T, String>`.
- `src/transport/settings.rs:73,232` return `Result<_, String>`.
- On `origin/main` only, `src/host/mod.rs:652` returns a per-entry `Result<Value, String>`.
- On `ba198f4`, `node.rs` has 20 `external(String)` sites and the host has 8 `Error::Remote(` sites.

`rg` found no crate outside `cartridge.ctg` importing `cartridge::transport` in `ws/*.ctg`. The PRD was narrowed to the transport.

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `b1483832450f3e20ef82ba852db7c8a991f18a48f1072f3d4caaa5d86496a0ee`. Prior text: `7dba786bb2a8756254ca2446d01ef18a1dbcc72f3e1b02fe4403269b5177960d`.
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Value and scope | 17 | Distinguishing undeclared events, schema rejections and closed connections serves the host, nodes and CLI messages. −3: no current consumer is blocked on matching these errors. |
| Ownership and reuse | 19 | Runtime-owned, with no external Rust consumer. Reuses `thiserror` and keeps `Outcome` and `Error::Remote`. −1. |
| Dependencies and slices | 18 | Needs `no-panic-answers-a-recoverable-failure`, acyclic; transport and host call sites land as separate commits. −2: the shared-file overlap with `no-panic` is sequenced, not split. |
| Acceptance and baseline | 18 | `rg` baseline to zero, five named variants, wire rendering test, gates with a cwd. −2: the list of string-matching tests is a probe, not yet recorded. |
| Failure and compatibility | 19 | Wire JSON is unchanged, so an older node interoperates; revert per commit. −1. |
| Reviewer total | 91 / 100 | |

Result: **PASS**.
Findings: the stale module list and `runtime::Error` were removed, and the scope was narrowed to the transport.
Unresolved blocking findings: none.
Disposition: keep (rebased).
Validation (read-only):
- `rg 'Result<[^,>]*, ?String>'`, `rg -c 'Result<'` and `rg 'external\(|Error::Remote\('` on both lines;
- a read of `src/error.rs` and of `src/transport/cartridge.rs:80-130`;
- `rg 'cartridge::transport'` over `ws/*.ctg`;
- `shasum -a 256`.

No product gates were run.
User rating: not required; none supplied.
Rounds used / remaining: 2 / 3.
Next action: wait for `no-panic`.
