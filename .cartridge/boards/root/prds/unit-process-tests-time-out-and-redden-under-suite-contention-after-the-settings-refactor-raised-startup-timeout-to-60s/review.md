# unit-process-tests-time-out-and-redden-under-suite-contention-after-the-settings-refactor-raised-startup-timeout-to-60s review history

Plan: `@root/unit-process-tests-time-out-and-redden-under-suite-contention-after-the-settings-refactor-raised-startup-timeout-to-60s` — `prd.ctg/.cartridge/boards/root/prds/unit-process-tests-time-out-and-redden-under-suite-contention-after-the-settings-refactor-raised-startup-timeout-to-60s/prd.md` (unit process tests waiting on the 60 s startup default).
Scope: one observable outcome: process/stream tests fail fast instead of waiting on the production startup timeout; leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none (no round-1 record for this scope exists under `boards/root/reviews/round-1/`).

Use the shared [review method](../../../../workflows/review-plan.md). Rounds are appended; earlier results are never rewritten. This record does not replace the item's implementation state.

## Round 1 — 2026-09-14

Reconciliation verdict: **SUPERSEDED**

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `3b81aa5cb8fc9dbd5c3763316193294fe411cebd06f7b1801c7fa3b632b27f8b`. Composition: root `24aa2be` (dirty), memo.ctg `9a1cf99`, memory.ctg `c25af4d`, cartridge.ctg `c9ef10b`, prd.ctg `077e57a2` (dirty).
Change: none to the body; frontmatter review fields added. Evidence: cartridge.ctg `939e7d1` ('Rewrite the host on the transport: every cartridge serves its own socket', 2026-09-14 13:03, after this item was written at 12:01) deleted `.cartridge/tests/unit/src/tests/process.rs`; `git log -S unready_fixture` shows it added in `fd8e132` and removed in `939e7d1`. None of `a_child_that_stays_alive_without_ready_times_out_and_is_reaped`, `slow_stream_handlers_*`, `stdout_closed_live_children_*` or `unready_fixture` exists anywhere outside prd.ctg. No test under cartridge.ctg/.cartridge/tests references `startup_timeout`; current hang tests bound themselves with per-event `timeout_ms` (e.g. `a_hung_listener_times_out_and_its_node_keeps_serving`, 300 ms). The 60 s default remains declared in cartridge.ctg/.cartridge/settings.json. Release note records `cargo test -p cartridge --lib` 197/197 at `d2a761e`.

Agent score: none (no score for this verdict). Result: **SUPERSEDED (no score)**.
Findings: The outcome's subject (three named tests and their fixture) was removed by the host rewrite. Residual note for any future defect: `settings::host()` is a process-wide `OnceLock` (cartridge.ctg/src/settings/host.rs:75-108) and `Host::new` reads `startup_timeout()` from it, so a test cannot inject a short startup timeout per host without a code change.
Unresolved blocking findings: none.
Disposition: retire (superseded by cartridge.ctg `939e7d1`); do not change `state:` here.
Validation (cwd /Users/feb/dev/cartridge): existence checks of the named starting files, fixtures and justfile recipes (`.cartridge/justfile`: check, test, smoke, verify; root `justfile`: isolation); `rg` for the named symbols and tests; `git log` in the owner submodules; a script resolving every `needs` target to `boards/<owner>/prds/<slug>/prd.md` and every relative link; `shasum -a 256`. No product gates (`just check`, `just test`, `just smoke`, `just verify`) were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 1 / 4.
Next action: coordinator retires the item; file a new cartridge.ctg defect only if a current test is observed waiting on the startup default.
