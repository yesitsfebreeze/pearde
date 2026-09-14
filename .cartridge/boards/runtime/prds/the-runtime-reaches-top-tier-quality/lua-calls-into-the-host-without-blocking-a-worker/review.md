# Lua calls into the host without blocking a worker — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/lua-calls-into-the-host-without-blocking-a-worker` (`prd.md`).
Scope: one leaf. Lua host calls yield instead of parking a Tokio worker.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **DELIVERED** (pending verification). The API it names is superseded.

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `c8f5dbff9a200d4d47420ea343fdc6149df5df453f58e5cc49656d4c4ff3ebfb` (frontmatter only; prior text `4a247c3acea7929cd29eecc7a90bb1f7e63321df5d9e1e6df4a52cb82f6e511d`).
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

Evidence:
- **Deleted targets.** The cited `src/context.rs` and the `ctx:emit/bail/gather/parallel` bridge in `src/lua.rs:398-511` were deleted by `939e7d1`/`ee7e295`. Lua reaches the host through the injected `cartridge` global in `src/node.rs`.
- **Local `main`.** `c9ef10b` ("a yielding Lua bridge") added `node.rs::either`. It creates each host function with `lua.create_async_function`, which yields when `coroutine.isyieldable()`. It falls back to `wait` (`block_in_place` + `block_on`) only where Lua cannot yield: inside a native module's C call or on a module's own thread. The doc comment at `node.rs:29-31` states this.
- **`origin/main` / `transport-design`.** The same design landed independently: `29dbff6` "listeners run as coroutines; waits on the base yield", `node.rs:34,53,56`.
- **Worker scope.** Each node is its own process with its own runtime (`src/cli/mod.rs:40-47`), so a parked worker can no longer starve another cartridge.
- **Re-entrant call.** The host test `a_call_that_comes_back_into_its_sender_is_answered` covers the deadlock case (`.cartridge/tests/unit/src/tests/host.rs`), and `gather_and_emit_reach_every_listener` covers gather.

Residual gaps, not blocking:
- There is no explicit `current_thread` flavor test.
- There is no 64-way concurrent gather test.
- The blocking fallback stays for native modules by design.

Result: no score (verdict round). Status: `delivered-pending-verification`.
Unresolved blocking findings: none.
Validation (read-only):
- `rg 'block_in_place|block_on|create_async_function|isyieldable'` on both lines;
- a read of `src/node.rs:1-80` on `e8a4da3`;
- `git log` on both lines;
- `rg 'fn '` over `tests/host.rs`;
- `shasum -a 256`.

Tests were not run. The coordinator's verification is `just test runtime` (`tests::host`).
Rounds used / remaining: 2 / 3.
Next action: the coordinator collects the leaf after the gate runs on the reconciled head.
