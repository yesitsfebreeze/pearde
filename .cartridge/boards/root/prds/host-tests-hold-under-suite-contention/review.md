# @root/host-tests-hold-under-suite-contention review history

Plan: @root/host-tests-hold-under-suite-contention, `prds/host-tests-hold-under-suite-contention/prd.md` with `specs/spec01.md`.
Scope: one observable outcome, a leaf: the host's `check` and `test` gates are green when the whole suite runs at once.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none recorded. The Result section mentions an earlier "independent review 93/100", but no review record for it exists, so it is not counted as a round here.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: prd.ctg `c11877c2` (the PRD directory is clean). The implementation is cartridge.ctg `bceb644`. The review ran at cartridge.ctg HEAD `d840064`, with a clean tree, and the superproject gitlink also points at `d840064`. Earlier timing runs used `319995e` plus foreign uncommitted work. That work was committed as `d840064` during the review.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `ce9e919b007fdf618b32d0b04c03235527e1e83186c869ea21da8d215dccd1e7` |
| Specs | `specs/spec01.md` sha256 `7fcab056eda228aff7e78dc8480dfc692e4f8f66cdab624c4ef9159e6f671916` |
| Material contracts/dependencies | `prd.ctg/src/lifecycle.ts` (Verify/Proof blocks, `sh -eu -c`, 120 s, 65 KB); `.cartridge/justfile` `_fan`/`_one`; `cartridge.ctg/justfile` `test`/`check`; cartridge.ctg `bceb644`, `319995e`, `d840064` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | A red host gate blocks every collect that runs it, so fixing it has real value. The scope is one outcome and two boxes, and it folds the two older duplicate items. −2: the PRD's `state: analyzing` and its `claim` contradict the "collected" Result. |
| Ownership and reuse | 18 | The fix lives in the owning cartridge. It reuses nextest, which the gate toolchain already requires (`.cartridge/justfile` `needed=(cargo cargo-nextest …)`). The diff is small: 3 files, +16/−3. −2: the `CARTRIDGE_HOME` `set_var` sites are only isolated by the runner, not removed (`tests/mod.rs:20`, `cli/setup.rs:96,203,229`, `cli/trust.rs:7`). The spec says this openly. |
| Dependencies and implementable slices | 17 | There is one spec with a precise footprint, and it matches the landed diff exactly. −3: the spec's line citations are stale (`setup.rs:92,197,223` are now `:96,203,229`). The Proof text says the CARTRIDGE_HOME grep "doesn't need a block", but the Verify section still has a grep block. |
| Observable acceptance and baseline evidence | 10 | Baseline evidence is strong (the 11:35 probe, and the HEAD 655beb6 evidence in the spec). The Verify blocks are now one gate per block and each fits easily (timings under Validation). −10: box 1, "`just check cartridge` exits 0", is **false at HEAD `d840064`** (see F1). Box 2's clause "pass on macOS CI" is ticked without any CI evidence; the Result itself defers it to the wave-4 CI item (F2). |
| Failure, recovery and compatibility | 16 | Block 1 now fails on a dirty tree. The YOLO=1 runs fail if the settings save/clear regresses. A poisoned lock now recovers, and `cargo test --workspace` still works. −4: nothing fails if the `trust_home()` poison recovery is reverted, because nextest isolates it and block 8 only fails on a panic. Block 8's result depends on the caller's ambient `CARTRIDGE_YOLO`. All gate blocks share `cartridge.ctg/target` with other sessions (F4). |
| Reviewer total | 79 / 100 | |

Findings and concrete revisions:

- **F1 — BLOCKING.** At HEAD `d840064` (clean tree), `just check cartridge` exits 1 in 0.6 s. `cargo fmt --all --check` reports diffs in `.cartridge/tests/unit/src/host/plan.rs:127,134,138` and `src/host/mod.rs:693`. Both files were last changed by `d840064` ("One host per project…"). `plan.rs` passes rustfmt at `bceb644` and at `319995e`, so this PRD's fix did not cause the failure. Still, the ticked box 1 and Verify block 2 do not hold at HEAD, and collection would fail. Revision: the owner of `d840064` runs `cargo fmt --all` in cartridge.ctg and commits; then rerun all Verify blocks from a clean tree. Do not weaken the gate. Until then, untick box 1 or note in the Result that HEAD regressed.
- **F2 — non-blocking, needs a revision.** Box 2's "the `cli::setup` and `cli::trust` tests pass on macOS CI" is ticked, but no CI run exists and the Result defers it to the wave-4 CI item. Revision: reword the box to "…pass locally on macOS (darwin, nextest)" and name the CI PRD in `needs`/Folds, or untick that clause.
- **F3 — non-blocking.** The timing question is resolved: every block is well under 120 s (see Validation). The per-gate split is correct but more than needed. Keep it; there is no need to merge.
- **F4 — non-blocking.** On the dirty tree, one in-process `CARTRIDGE_YOLO=1 cargo test --workspace` failed. `tests::host::a_waiting_cartridge_starts_when_the_descriptor_adds_its_listener` got `sandbox-exec: execvp() of …/target/debug/cartridge failed: No such file or directory`, because a concurrent build replaced the shared binary. That flake comes from the environment, not from `bceb644`, but it can redden collection. Revision: pin block 8 as `cd cartridge.ctg && CARTRIDGE_YOLO=1 cargo test --workspace`, so it does not depend on the caller's environment. Also note in the spec that a Verify run needs no concurrent cargo build in `cartridge.ctg/target`.
- **F5 — non-blocking.** No block fails if the `trust_home()` `unwrap_or_else(PoisonError::into_inner)` recovery is reverted. Accept this as a code-review check (state it in Proof), or add a unit test that poisons `trust_home()` and then takes the lock.
- **F6 — non-blocking.** Hygiene: update `state` and drop the stale `claim` through the lifecycle, refresh the spec's line citations, and remove the Proof sentence about the grep or the grep block, so the two agree.

Disposition: keep. Revise F1 (a foreign fmt regression at HEAD), F2 and F4, then re-verify.

Validation (cwd `/Users/feb/dev/cartridge` unless stated; warm target; host has 10 CPUs, load avg about 2.7–4.1; other sessions active):

- Dirty tree over `319995e`: `just test cartridge` exit 0, 168/168, real 10.49 s. `cd cartridge.ctg && cargo test --workspace` exit 0, 153+15, real 7.61 s. `CARTRIDGE_YOLO=1 just test cartridge` ×3 exit 0, real 9.92, 9.86 and 9.98 s. `env -u CARTRIDGE_YOLO just test cartridge` exit 0, real 10.11 s. `CARTRIDGE_YOLO=1 cargo test --workspace` exit 101, the F4 flake, real 7.17 s. `just check cartridge` exit 1, fmt diff in the then-uncommitted `plan.rs`.
- Clean HEAD `d840064`, spec Verify blocks run one at a time with `sh -eu -c`: block 1 (clean tree) rc 0. Block 2 `just check cartridge` rc 1, 0.59 s (F1). Blocks 3–5 `CARTRIDGE_YOLO=1 just test cartridge` rc 0, 168/168, real 9.98 s, one run representative of the three identical blocks. Block 6 `env -u CARTRIDGE_YOLO just test cartridge` rc 0, real 10.00 s. Block 7 grep rc 0. Block 8 `cargo test --workspace` rc 0, 153+15, real 8.04 s. `cargo clippy --workspace --all-targets` finishes clean.
- Estimated full Verify pass: about 50 s warm, run twice (before and after integration). No block is within 10× of the 120 s limit.

Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (79/100, 1 blocking finding).
Unresolved blocking findings: F1, `just check cartridge` red at cartridge.ctg HEAD `d840064` (rustfmt in `host/plan.rs`, `host/mod.rs`).
Rounds used / remaining: 1 / 4.
Next action: get `d840064`'s fmt fixed by its owner, apply F2/F4 (F5/F6 optional), rerun every Verify block from a clean tree, and present round 2.

## Round 2 — 2026-09-16

Presented revision: the PRD directory in prd.ctg is uncommitted. `prd.md` and `specs/spec01.md` are modified and `review.md` is untracked on top of `762fe9a2`, so the revision is bound by the digests below. The review ran at cartridge.ctg HEAD `cdd3124` (fmt fix) on top of `d840064`, `319995e` and `bceb644`, with a clean cartridge.ctg tree. The superproject gitlink still records `d840064`, and collect commits it.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `926ada4739633faaec3b934e42fb7fa313accdf44b756514f2965f533537712a` |
| Specs | `specs/spec01.md` sha256 `c742074ce7fd4c51c0c5c198331cab21f94e6ea14b67055783c45be0b7dc60c8` |
| Material contracts/dependencies | cartridge.ctg `cdd3124` (`src/host/mod.rs`, `.cartridge/tests/unit/src/host/plan.rs`), `bceb644` (`justfile`, `cli/setup.rs`, `tests/settings.rs`); `.cartridge/justfile` gate recipes; engine: `sh -eu -c`, 120 s per block |

Round-1 findings, checked:

- **F1 (blocking): resolved.** `cdd3124` changes only formatting. With whitespace stripped, `src/host/mod.rs` has identical tokens at `d840064` and `cdd3124`. `plan.rs` differs by one trailing comma that rustfmt inserted. At HEAD, `just check cartridge` exits 0 (fmt and clippy clean).
- **F2: resolved.** PRD box 2 now says "pass locally in that suite" and hands CI coverage to `@root/ci-runs-the-gates-on-macos-and-linux`.
- **F3: no action needed.** Every block is still far under 120 s.
- **F4: partly resolved.** Block 9 pins `CARTRIDGE_YOLO=1`. The spec still does not say that a Verify run needs no concurrent cargo build in the shared `cartridge.ctg/target`.
- **F5: resolved by content pin.** Block 8 greps for the poisoned-lock recovery and the ambient-yolo save. No test exercises the recovery, and the Proof accepts that.
- **F6: partly resolved.** The Proof acknowledges the stale line numbers, and the grep contradiction is gone. The PRD still has `state: analyzing` and a stale `claim`. Its Result still quotes an unrecorded "independent review 93/100" and does not mention the round-1 FAIL.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Red host gates block every collect that runs them. The PRD has one outcome and two boxes and folds two duplicates. −1: frontmatter `state`/`claim` contradict the "collected" Result (F6). |
| Ownership and reuse | 18 | The fix lives in the owning cartridge and reuses nextest, which the gate toolchain already requires. The diff is small. −2: the `CARTRIDGE_HOME` `set_var` sites remain. The runner isolates them rather than removing them, and the spec says so openly. |
| Dependencies and implementable slices | 18 | There is one spec whose footprint matches `bceb644`. The `cdd3124` fmt fix sits outside the spec footprint but inside the PRD footprint (`cartridge.ctg`). −2: the Result prose is stale (unrecorded 93/100, no round-1 FAIL), and box 1's parenthetical mixes the 09-15 `socket.rs` history with the 09-16 fix. |
| Observable acceptance and baseline evidence | 19 | Both PRD boxes and all five spec boxes match what was observed at `cdd3124`: check green; nextest 168/168 three times with `CARTRIDGE_YOLO=1` and once without; `nextest run --workspace` in the justfile; in-process `cargo test` 153+15. −1: the poison-recovery box is proven by grep, not by behaviour. |
| Failure, recovery and compatibility | 17 | Block 1 fails on a dirty cartridge.ctg tree. Blocks 3–6 cover both yolo environments, and block 9 keeps the in-process runner working. −3: the shared-`target` flake from round-1 F4 is not written down as a precondition. Collection can still redden while another session builds. Block 1 turns red whenever another session dirties cartridge.ctg, which is correct but can stall collection. nextest reported one LEAK (`sandbox::tests::an_exec_grant_that_resolves…`), which is not a failure. |
| Reviewer total | 91 / 100 | |

Findings and concrete revisions:

- **G1 — non-blocking.** Add a line to the spec's Verify preamble: "run with no concurrent cargo build in `cartridge.ctg/target`" (carried over from F4).
- **G2 — non-blocking.** Before collecting, update the Result (round 1 FAIL at 79, round 2 PASS at 91; drop the unrecorded 93/100), and let the lifecycle set `state` and clear `claim` (carried over from F6).
- **G3 — non-blocking.** Trim box 1's parenthetical to the current evidence (`cdd3124`, check green).
- **G4 — non-blocking, environment.** At collect time, `git -C cartridge.ctg status --porcelain` must be empty or block 1 fails. Check this first in a shared checkout.

Disposition: keep. Proceed to collection. G1–G3 are hygiene and can land in the same collect.

Validation: cwd `/Users/feb/dev/cartridge`. Each spec Verify block was extracted and run in order with `sh -eu -c` under a 120 s timeout. Warm target, 10 CPUs, load avg about 4, other sessions active.

| Block | Command | rc | Wall time |
| ---: | --- | ---: | ---: |
| 1 | clean cartridge.ctg tree | 0 | 0.01 s |
| 2 | `just check cartridge` | 0 | 0.75 s |
| 3 | `CARTRIDGE_YOLO=1 just test cartridge` (168/168) | 0 | 16.18 s |
| 4 | same (168/168) | 0 | 10.06 s |
| 5 | same (168/168) | 0 | 11.17 s |
| 6 | `env -u CARTRIDGE_YOLO just test cartridge` (168/168, 1 leaky) | 0 | 10.68 s |
| 7 | grep nextest in justfile | 0 | 0.01 s |
| 8 | grep poison recovery and ambient-yolo save | 0 | 0.01 s |
| 9 | `cd cartridge.ctg && CARTRIDGE_YOLO=1 cargo test --workspace` (153+15, 0 doc) | 0 | 8.52 s |

A full pass takes about 57 s. The largest block is 16 s against the 120 s limit.

Reviewer identity: independent reviewer agent r2 (coordinator cartridge-c4).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: PASS (91/100, no blocking finding).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: commit the PRD revision so the digests above are bound, optionally apply G1–G3, confirm a clean cartridge.ctg tree, and collect (runs the Verify blocks before and after integration and commits the `cartridge.ctg` gitlink at `cdd3124`).
