# a-lua-cartridge-runs-in-a-restricted-environment review history

Plan: `@runtime/the-runtime-reaches-top-tier-quality/a-lua-cartridge-runs-in-a-restricted-environment` (`prd.md`, `specs/spec01.md`).
Scope: one leaf outcome — Lua cartridges confined to their manifest grant.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../../workflows/review-plan.md).

## Round 1 — 2026-09-14

Presented revision: source HEAD `b4d553f` (cartridge.ctg, reviewed via `git show HEAD:`; the main tree carries another session's uncommitted refactor).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `9f2a713c7fe98b2cd451e0a9cae0266acc6c48c92f29094c0b248394c84395a7` (claimed, state analyzing) |
| Specs | `specs/spec01.md` SHA-256 `d40033a7046239b0caf1a4b587acd07775ce7400df91858a73e6ae6cc12cb8b9` |
| Material contracts/dependencies | `src/lua.rs`, `src/sandbox.rs`, `src/loader.rs`, `src/context.rs`, `src/cartridge.rs`, `src/settings.rs`, `settings.json` at `b4d553f`; mlua 0.12.1 |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | Probe proves the gap. Outcome unreachable while `cartridge.process` spawns any program unconfined; `src/cartridge.rs:332` uses plain `Command::new`, and nothing under `src/` calls `sandbox::` at HEAD. |
| Ownership and reuse | 15 | Reuses `granted_paths`/`granted_exec`/`sandbox::command`. Footprint misses `src/cartridge.rs`; the sibling async-Lua PRD rewrites the same call sites and invalidates the per-OS-thread entry mark; no ordering stated. |
| Dependencies and implementable slices | 13 | One slice bundles env split, grant-checked io/os/exec, and limits; unnamed dependencies on the offline-suite and async-Lua PRDs. |
| Observable acceptance and baseline evidence | 15 | Good baseline probe. Limit tests are uncontrollable (`settings::host()` is a process `OnceLock`); no pcall-escape or `cartridge.process`-escape test. |
| Failure, recovery and compatibility | 13 | Verify gate cannot pass: full `cargo test --lib` takes ~124 s against a 120 s timeout and `folders.rs::recorded_memory_layout_uses_the_separate_submodule` fails at HEAD. Missing entry marks; unbounded `os.execute` wait. |
| Reviewer total | 72 / 100 | |

Findings and concrete revisions:

1. BLOCKING — `cartridge.process` bypasses confinement: an ungranted bare `.lua` can return `cartridge.process({"/bin/sh","-c",...})`, spawned unsandboxed at discovery and start. Route discovery/start through `sandbox::command` and require non-own programs in `grant.exec`, or depend on a process-confinement PRD and narrow the outcome.
2. BLOCKING — verify gate: filter to affected tests with a lane-local target dir, or make `the-unit-suite-runs-offline-in-under-a-minute` a hard prerequisite.
3. BLOCKING — `while true do pcall(function() while true do end end) end` survives a count hook; after the deadline switch the hook to every instruction and keep erroring; test it.
4. BLOCKING — inject `lua_call_ms`/`lua_memory_bytes` into the host (defaulting to `settings::host()`) so tests can use 50 ms / 1 MiB.
5. Unmarked entries (`__gc` finalizers, state close): define no-mark hook behaviour.
6. Lock wait counts against the budget: start the deadline at the first hook tick after the mark.
7. `os.execute` blocks holding the state: bound by the deadline, kill on expiry, null/capture stderr.
8. Refuse `io.lines()` without a filename; check both `os.rename` paths; load chunks with `ChunkMode::Text`.
9. Docs: `sandbox.rs` claims children are confined but nothing calls it at HEAD; state shared-table, string-metatable, uninterruptible C function and shared memory-limit ceilings.
10. Removing `require`/`load` from globals also affects `config.lua` layers (`loader.rs:858`); document it.
11. The `process.rs` fixture conversion changes entry ids/paths; the write grant must name the canonical log path.

Disposition: revise, and re-sequence behind the in-flight Lua refactor.
Validation: reviewer read HEAD sources; coordinator confirmed finding 1 with `git show HEAD:src/cartridge.rs` (plain `Command::new`) and `git grep -n "sandbox::" HEAD -- src` (no matches), cwd `cartridge.ctg`. Probe command recorded in spec01. No product gate run.
Reviewer identity: independent general-purpose sub-agent spawned by session cartridge-9a (Claude Opus 5).
User rating: not supplied.
User feedback/provenance: "use just `prd next --board runtime` to work on the fixes" (2026-09-14).
Result: FAIL.
Unresolved blocking findings: 1, 2, 3, 4.
Rounds used / remaining: 1 / 4.
Next action: hold. Session cartridge-ctg-40 is landing a user-requested uncommitted refactor of `src/lua.rs`, `context.rs`, `loader.rs`, `settings.rs` (async coroutines, `crate::lua::interpreter()`); revise spec01 on top of that commit, then request round 2.

## Round 2 — 2026-09-14

Reconciliation verdict: **DELIVERED** (pending verification).

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `47c4f0b47486212a9326a391e5a783248a6173f7e8d3d12f056b4551bf4cc859`. The change is frontmatter and the review pointer only; the body is the round-1 text, and the prior prd.ctg HEAD text is `33b9f1fb1689c7a2fa4e1f2d77f39432137ffcaab8b428111884b8a6280e8c3e`. `specs/spec01.md` is historical: it targets `src/context.rs` and `src/cartridge.rs`, both deleted.
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`, clean;
- `ws/cartridge.ctg` `transport-design` `ba198f4`, clean;
- prd.ctg `077e57a2`, dirty.

Inherited rounds: this leaf's own round 1 and the parent's round 1 cover the same date and audit. The count is 1, not 2, so this is round 2.

Evidence, identical on both lines unless noted:
- **Interpreter.** `src/lua.rs::interpreter` (`d2a761e`) builds `StdLib::ALL_SAFE ^ IO ^ PACKAGE`, trims `os` to `clock/date/difftime/getenv/time`, and removes `dofile`/`loadfile`. `.cartridge/tests/unit/src/lua/tests.rs` asserts that `io`, `package`, `require`, `debug`, `os.execute/exit/remove/rename` are nil.
- **Process confinement.** Since `939e7d1`, every Lua cartridge runs as its own node process spawned through `crate::sandbox::command(&command, &plan.grant, ...)` (`src/host/process.rs:36`). The OS confines it by its grant, and programs it spawns inherit the sandbox. Round-1 blocker 1 (`cartridge.process` unconfined) is closed by construction.
- **Memory.** `node.rs` sets `lua.set_memory_limit(settings::host().lua_memory_bytes)` (`e8a4da3:106-110`, `ba198f4:100`), and a unit test covers it (`a_memory_limit_bounds_what_a_chunk_can_allocate`).
- **Runaway code.** A runaway listener is bounded by event deadlines (`transport/cartridge.rs` `Outcome::TimedOut`; host test `a_hung_listener_times_out_and_its_node_keeps_serving`). It stalls only its own process.
- **Docs.** `docs/architecture.txt` NODES and the `src/sandbox.rs` module doc state the two layers.

Round-1 blockers:
1. Closed, as above.
2. Closed: `folders.rs` is gone.
3. Superseded: the per-instruction hook gave way to process isolation plus deadlines.
4. Superseded: limits come from the host settings.

Residual gaps, not blocking:
- There is no instruction-count hook, so a busy loop burns CPU until its deadline answers the caller.
- Linux refuses to spawn nodes; that is owned by `@runtime/linux-policy`.

Result: no score (verdict round). Status: `delivered-pending-verification`. Recommend retiring `specs/spec01.md` with the leaf.
Unresolved blocking findings: none.
Validation (read-only):
- reads of `src/lua.rs`, `src/node.rs:25-120`, `src/host/process.rs:20-60`, `src/sandbox.rs:1-30`, the lua unit tests and `docs/architecture.txt:60-90`;
- `rg 'sandbox::|set_memory_limit|set_hook'` on both lines;
- `shasum -a 256`.

Tests were not run. Verification step for the coordinator: `just test runtime` includes `lua::tests` and `tests::host`.
Rounds used / remaining: 2 / 3.
Next action: the coordinator collects or retires the leaf after the gate runs.
