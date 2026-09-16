# @harness/slim-failed-turn-distillation review history

Plan: @harness/slim-failed-turn-distillation, `boards/harness/prds/slim-failed-turn-distillation/prd.md`.
Scope: one observable outcome. A named failed tool-using run leaves one retrievable memory line. This is a leaf with spec01.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; ratings are delegated by the user.
Inherited rounds: none. The split inherited none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: prd.ctg 522cbf9e working tree. Files not in that commit: `prd.md` (claimed, `state: analyzing`) and `specs/spec01.md`. Code base: harness.ctg 9c144a3.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `da8af402016e78f7631d083de09642627ee7c5ad64dd488e57cd9607ec79896d` |
| Specs | `specs/spec01.md` sha256 `348f995839b3a61023918023d461f6854ea698247c5f58af2ece8c270af4b05c` |
| Material contracts/dependencies | `boards/agent/prds/the-turn-end-ring-call-names-the-run-that-finished/prd.md` sha256 `eb60f19e…2a49`<br>harness.ctg 9c144a3: `src/lib.rs` 769-870 (`read_transcript`/`ring`/`evict`), 1570 (dispatch), `.cartridge/tests/integration/{ring,support}.rs`<br>agent.ctg `src/lib.rs` 204, 568, 592, 776; `src/sse.rs` 258/278<br>`reflex-tool-audit-loop` `## Decision`<br>analyst-1.md |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The outcome is small and clear: one line for failures only, and nothing for successes. The PRD is inside the word budget. Deductions: live value depends entirely on the agent companion, since today `Run::finish` sends a bare `{op:"ring"}` (agent lib.rs:592). "Ingested exactly once" is only true per call, because the plan has no dedupe for a repeated ring on the same run. "The bank's `query` returns it" is proved only against a substring fake, not memory.ctg. |
| Ownership and reuse | 17 | The plan reuses `read_transcript`, the committed-ingest contract from `evict` (lib.rs:858-869) and the `ring.rs`/`support.rs` fixture pattern. It adds no dependency. It respects the sibling decision: no ledger, and sessions keeps counting. The no-`needs` claim holds: dispatch calls `ring(&h,&c)` without args (lib.rs:1570), so unknown args are ignored today. Deduction: `.cartridge/help.md:11` and `.cartridge/docs/README.md` "The turn ring" document the ring op and its settings, but no step updates them and neither file is in the footprint. |
| Dependencies and implementable slices | 15 | One leaf with four footprint files. The steps map to the code. The transcript shapes the analyst cited are correct: `record()` carries `run`, `tool_finished` carries `tool` and `result`, error results are `{content,error:true}`, `run_finished.phase`, and assistant `content` may be `null` with `tool_calls` (sse.rs:278), which the "last string content" rule handles. Deductions: B1 (the second Verify pass writes the live dylib) and B2 (a post-integration box that cannot be ticked before collect). |
| Observable acceptance and baseline evidence | 14 | The tests can fail. `cargo test --test slim` errors while no `[[test]] slim` exists, and the python check exits 1 on the base because `settings.slim` is absent (KeyError). The blocks run with no `cd`: every path is cwd-relative to the crate root, which is correct in both passes. `CARTRIDGE_BIN` is absolute, exists (release build from 2026-09-15) and matches the lane's `../cartridge.ctg` default. The analyst's gate and cold-build timings are plausible and consistent with ring.rs. Deductions: N1 (PRD box 1 and box 2 contradict each other), N2 (whether the `slim` reply key is present is unspecified), N3 (the Step 4 case list omits the empty-`memory` case that spec box 2 asserts). |
| Failure, recovery and compatibility | 16 | The plan fails open: the ring returns Ok, the error goes to `slim.error` plus stderr, and the sweep is unaffected. Slim runs before the sweep, so the named session cannot be evicted before it is read. `slim=false` is the rollback. An unnamed ring behaves as today. Deductions: B1 (running Verify can hot-reload the live daemon with a test build), and N4 (no bound or dedupe when the same run is rung twice, for example a retry). |
| Reviewer total | 78 / 100 | |

Findings and concrete revisions:

- **B1 — BLOCKING: the Verify blocks write the live harness dylib in the second pass.** In the second pass the blocks run with cwd = `/Users/feb/dev/cartridge/harness.ctg` and the default target `harness.ctg/target`. The live profile loads harness from `path = "harness.ctg"` (root `.cartridge/init.lua:38`), and `target/debug/libharness.dylib` was rebuilt today. `cargo test --test slim` runs `support::module()`, which executes `cargo build --lib` and writes `target/debug/libharness.dylib`. The clippy block writes into `target/debug` as well. The lane pass is isolated only because the lane has its own target.
  Fix: give both cargo blocks an explicit isolated target, for example
  `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/slim-verify}"`
  at the top of the clippy block and the test block. The child `cargo build` in `support.rs` inherits the environment, so the dylib lands there too. The fmt and python blocks write nothing.
- **B2 — BLOCKING: spec box 6 and the last PRD box cannot be truthfully ticked before collect.** They require `just check harness` and `just test harness` "after integration" from `/Users/feb/dev/cartridge`, but collect needs every box ticked, and no Verify block runs those commands. Running them before integration tests the old harness.ctg and rebuilds the live target. Recently collected PRDs (for example `@mcp/deferred-tool-band`) carry no post-integration box.
  Fix: reword the box to "the Verify blocks pass in the lane and again in harness.ctg (isolated target)", which is what `just check/test harness` runs. Move the owner gate into `## Proof and recovery` as a post-collect note.
- N1 — Box 1 counts a run as failed on `run_finished.phase == "failed"` even when every tool succeeded. Box 2 says a run "whose tools all succeeded stores nothing". A run whose tools all succeed but whose phase is `failed` satisfies both. Fix: box 2 should read "whose tools all succeeded and whose run did not fail". The fixture for that case must use phase `completed`, and a case with successful tools and phase `failed` should expect one line.
- N2 — Step 3 says to put `slim` in the reply, but box 5 says an unnamed ring returns "the same reply as today". State that the `slim` key is absent unless a named ring was attempted (named with `slim=true` and non-empty memory). State what `slim=false` with a named ring returns. Have the test compare the unnamed reply's key set to `{finished,kept,distilled,errors}`.
- N3 — The Step 4 case list omits empty `memory`, which spec box 2 asserts. Add it. It needs a third base boot, or a reload with a different config, so keep an eye on the 120 s block limit.
- N4 — "Ingested exactly once" has no mechanism behind it beyond agent ringing once per run. Either say it is once per ring call and accept duplicates on a repeated ring, or dedupe by probing the bank. The lazy option is to reword.
- N5 — Add `.cartridge/help.md` (the ring op's `session`/`run` args) to the footprint, and optionally the README turn-ring section, with a one-line step. Otherwise the docs go stale, or doc edits break collect.
- N6 — Optional Step 5 names `.cartridge/tests/unit/main/tests.rs`. That file exists, but it is not in the footprint. Either drop the step or add the path now, so the lane does not have to decide it.

Disposition: revise. Keep it as one leaf. No split is needed.
Validation: all checks were read-only. harness.ctg is at 9c144a3 and clean. I ran `git ls-files`, and grep over harness, agent, cartridge and the root `.cartridge/init.lua`. `ls -la` showed `cartridge.ctg/target/release/cartridge` present and `harness.ctg/target/debug/libharness.dylib` with mtime 2026-09-16 09:43. `cargo metadata --locked --offline` was inconclusive: an offline download error, not a lock drift. No builds, no worktrees and no tests were run by the reviewer.
Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (78/100, 2 blocking findings).
Unresolved blocking findings: B1, B2.
Rounds used / remaining: 1 / 4.
Next action: one bounded revision of prd.md and spec01. Add an isolated `CARGO_TARGET_DIR` to the cargo blocks, reword the post-integration box and the box 1/2 failure definition, specify when the `slim` key is present, add the empty-memory case and the help.md footprint. Then send it for round 2 review.
