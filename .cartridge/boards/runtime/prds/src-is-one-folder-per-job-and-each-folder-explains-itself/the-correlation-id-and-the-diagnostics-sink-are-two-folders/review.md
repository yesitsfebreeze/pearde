# @runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/the-correlation-id-and-the-diagnostics-sink-are-two-folders review history

Plan: @runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/the-correlation-id-and-the-diagnostics-sink-are-two-folders (`prd.md`, `specs/spec01.md` in this directory).
Scope: one observable outcome. `src/trace` keeps the correlation id and `src/log` takes the diagnostics sink. This is a leaf under the `src-is-one-folder-per-job-and-each-folder-explains-itself` rollup.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-19

Presented revision:
- prd.ctg is at `86dae107` (dirty working tree).
- cartridge.ctg HEAD is `324f36e`, the spec's base. Nothing under the footprint has moved since then: `git log 324f36e..HEAD` over the footprint is empty.
- The prd.md footprint had just been widened by the coordinator to match the spec.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `8041d8e82fd11dcc56ff5e069215b9ebba4fb13d9a93a29304cdbd5974d82861` |
| Specs | `specs/spec01.md` sha256 `7c192c90e3d94e346fa71463ef43f2d57b13474a4fc6990bb3dd9b007b31aa5f` |
| Material contracts/dependencies | `.state/loop/…/analyst-1-probe.patch` sha256 `2f042fbc…9066`; `analyst-1.md` sha256 `aa744143…3d54`; the parent `prd.md`; the sibling `every-src-folder-has-a-fresh-eyes-readme-and-the-audit-demands-it/prd.md` (the README shape); the live cartridge.ctg dirty paths `src/cli/{mod,args,host}.rs`, `README.md`, `src/asp/*` and `src/host/mod.rs`, which belong to other sessions |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The plan implements the user's 2026-09-19 layout decision directly (`trace/` + `log/`). It is one leaf with no behaviour change. −2 because the prd.md acceptance is stale against the spec: :31 names `src/trace/tests`, which does not exist (the tests live at `.cartridge/tests/unit/src/trace/tests.rs`), and :33 says "the same test names", but the module path changes from `trace::tests::` to `log::tests::`. Only the leaf names stay the same. |
| Ownership and reuse | 16 | The owner is right (runtime, cartridge.ctg). The code moves verbatim, and `log/` is split one file per responsibility (`redact`, `sink`, `layer`, `mod`). No re-export is left: the probe proved that `cartridge::trace::{subscribe,flush,diagnostic,diagnostic_line,Layer}` fail with E04xx. −4 because the trace README the spec prescribes (spec01.md:63) is wrong. It says "`log`, `transport` and `host` call it", but at base plus the patch the only caller of `crate::trace` is `src/log/mod.rs:8` (`current`). `transport/cartridge.rs:113-119` has its own `TRACE` task-local and never uses `crate::trace`, and `host` calls `log`, not `trace`. The sibling README PRD requires `Talks to` to agree with the real `use` edges, and the spec itself claims it does. |
| Dependencies and implementable slices | 17 | The footprint matches the patch exactly, plus `docs/architecture.txt` for step 5. I found no caller outside it: rg over every `*.ctg` shows only `cli/mod.rs:38,50` and `host/process.rs:173`. `proxy.ctg`'s `trace` is its own module, and `node/mod.rs:209 cartridge::trace()` is the transport fn. The plan is independent of its siblings. −3 because the plan does not state the ordering constraint against the other session's uncommitted `src/cli/mod.rs` edit (see Failure). |
| Observable acceptance and baseline evidence | 17 | Every block discriminates, and I re-ran them myself (see Validation). The test block names all six tests, and they ran (`6 passed; 168 filtered out`). The timings fit 120 s from a cold target. There are no inert `! grep` or AND-OR guards: `test "$n" -eq 6` and `test "$lines" -le 25` stand alone. Deductions: −1 because "`mod.rs` holds only the correlation id" is not enforced. A mutant that leaves a private `struct Sink` and `fn redact` in `trace/mod.rs` passes the census and the probe, so the diff reading is the only backstop. −1 because the `docs/architecture.txt` edit is neither in the probe patch nor gated. −1 because the census sends `cargo test --list` stderr to `/dev/null`, so a compile failure exits 1 with no message. |
| Failure, recovery and compatibility | 12 | The spec has no recovery or landing section, and prd.md:35-37 says only "Not run". The analyst names the hazard (analyst-1.md "Risks"), but it never reached the plan. The hazard is real: live `src/cli/mod.rs` carries another session's `Command::Launch { passthrough }` hunk, which depends on its uncommitted `src/cli/args.rs` and `src/cli/host.rs` edits. Collect's receipt commits every dirty in-footprint path, so it would commit that hunk without its dependencies. I reproduced that state (patch + foreign diff, with `args.rs`/`host.rs`/`README.md` set aside): `cargo check` fails with `E0026 variant args::Command::Launch does not have a field named passthrough` and `E0061 this function takes 4 arguments but 5 arguments were supplied`. The collected sha would not build. −8. |
| Reviewer total | 80 / 100 | |

### Findings and concrete revisions

- **B1 (blocking)**: prd.md:35-37 and spec01.md:83 have no landing precondition for the shared `src/cli/mod.rs`. Fix: in the prd.md "Proof and recovery" and a spec "Landing" note, state that collect runs only when `git -C cartridge.ctg diff --quiet -- src/cli/mod.rs` exits 0, meaning the other session's `Launch { passthrough }` edit has landed or been withdrawn. Otherwise the coordinator waits or rebases. State the recovery too: if a receipt swept a foreign hunk, check the collected sha in a throwaway worktree (`cargo check --lib --bins`) and revert or complete it before anything else lands.
- **B2 (blocking)**: spec01.md:63 has a wrong `Talks to` for `trace`. Fix: `Talks to:  calls nothing in the crate; \`log\` calls it`. Do the same in the probe patch's `src/trace/README.md` so the implementer does not copy the error.
- N1: prd.md:31 and :33 are stale. Point :31 at `.cartridge/tests/unit/src/trace/tests.rs`, and make :33 say "the same leaf test names, the six sink tests now under `log::tests::`". prd.md belongs to the coordinator, so this is a body-only edit.
- N2: the census could fail when `src/trace/mod.rs` still defines sink items. For example, add `if grep -nE 'struct (Sink|Layer)|fn (redact|drain|diagnostic)' src/trace/mod.rs; then exit 1; fi`, or cap the file at about 60 lines. This is optional, because the diff reading remains the backstop.
- N3: add a check for the architecture line, e.g. `if grep -q 'trace ids and the diagnostics sink' docs/architecture.txt; then exit 1; fi` in the census.
- N4: send the census's `cargo test --list` stderr to a file and print it on failure, instead of `2>/dev/null`.
- Observation, not this PRD's scope: `trace::{mint,of,stamp,scope,carry}` have no production caller in any `*.ctg`. Only `log` calls `current`, and transport runs its own task-local `TRACE`. So the "correlation id" folder holds an API that nothing sets, and `current()` always returns `None` outside tests. The parent rollup should learn this; ASP.md:87 describes `src/trace/` as the correlation id.
- Housekeeping: the analyst's probe worktree `scratchpad/analyst-3/wt` was left registered (analyst-1.md). The coordinator still has to remove it.

Disposition: revise (B1 and B2 are one-paragraph and one-line fixes). Keep the scope.

### Validation

Every command below ran as `env -u CARTRIDGE_YOLO -u CARGO_TARGET_DIR sh -eu -c "<block>"`, from the root of a detached worktree of cartridge.ctg at `324f36e` under `scratchpad/reviewer-trace-1/wt`. No sibling symlinks were needed: Cargo.toml has no path deps. The kache rustc-wrapper was on, and each block used a fresh default target `target/prd-trace-log-split-verify`.

- `git apply --check analyst-1-probe.patch`: exit 0.
- Unpatched tree (discrimination):
  - census: exit 1 in 23 s ("log::tests::a_credential_or_a_prompt_body_is_omitted_and_named is not in the census").
  - probe: exit 101 in 17 s. The positive control fails with E0433, as it should.
  - lint: exit 1 (rustfmt: `src/log/*.rs` does not exist).
- Patched tree, cold target:
  - census: exit 0 in 19 s.
  - probe: exit 0 in 22 s.
  - lint (`rustfmt --check` + `cargo clippy --workspace --all-targets -D warnings`): exit 0 in 11 s.
  - test block: exit 0, 6 passed, 168 filtered out.
- Mutant, `pub use crate::log::{…}` re-export added to `trace/mod.rs`: the probe exits 1 ("cartridge::trace::subscribe() still resolves"). The census exits 0, which is expected; this is the probe's job.
- Mutant, private `struct Sink; fn redact(){}` left in `trace/mod.rs`: the census exits 0 and the probe exits 0. The gate does not catch it (N2).
- Simulated repo pass (patch plus the live cartridge.ctg dirty diff at review time: README, `src/asp/{ask,mod,own}.rs`, `src/cli/{args,host,mod}.rs`, `src/host/mod.rs`):
  - census: exit 0 in 12 s.
  - probe: exit 0 in 7 s.
  - lint: exit 0 in 7 s.
- Simulated receipt (the same, with `src/cli/args.rs`, `src/cli/host.rs` and `README.md` set aside): `cargo check --lib --bins` fails with E0026 and E0061 in `src/cli/mod.rs` (B1).
- Callers: `rg --type rust 'cartridge::trace|trace::(mint|current|of|stamp|scope|carry)'` over `*.ctg` finds only the three code callers in the spec's table. rg over the prd.ctg boards for `cartridge.ctg/src/trace` finds only this PRD, the ASP rollup's note, and a deferred sessions PRD. Both describe the correlation id, so they stay valid.
- Worktree cleanup: removed with `git worktree remove` after both patches were reverse-applied. No `--force` was used and no stash was left behind.

Reviewer identity: coordinator-4b fresh agent, round 1.
User rating: not required under delegation.
User feedback/provenance: none for this revision.
Result: FAIL (80/100, two blocking findings).
Unresolved blocking findings: B1, B2.
Rounds used / remaining: 1 / 4.
Next action: make one bounded revision. Add the landing precondition and recovery (B1), correct the trace README in the spec and the probe patch (B2), and optionally apply N1–N4. Then run round 2.

## Round 2 — 2026-09-19

Presented revision:
- prd.ctg is at `ce911ede` (dirty working tree).
- cartridge.ctg HEAD is `445a87f`. `git diff --stat 324f36e 445a87f` over the footprint is empty, so the spec's `324f36e` anchor still holds. Live dirt: `README.md` and `src/cli/{args,host,mod}.rs` (another session's launch `passthrough` edit).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `9a714530ae48a0b91f0abbf56575af301cc8b19add6e7b52963592f757e5b338` |
| Specs | `specs/spec01.md` sha256 `6f40fd6272cdc7f2a90a279b6fae725aea6f1e91fe80b52ee941c0ab25aa7956` |
| Material contracts/dependencies | `analyst-1-probe.patch` sha256 `325c22f65b787cb0aa360df3c9cab0cdebccd431b5abf5997a9f150ba500134c`; `analyst-1.md` (revision 1); the parent `prd.md`; the README-shape sibling `every-src-folder-has-a-fresh-eyes-readme-and-the-audit-demands-it/prd.md`; `@runtime/the-correlation-id-is-minted-by-transport-so-src-trace-is-dead-code/prd.md` (footprint `src/trace`, `src/lib.rs`); the live dirty diff of cartridge.ctg |

Round 1 findings:
- B1 is fixed. The spec's "Landing" section and prd.md "Proof and recovery" state the precondition (`git -C cartridge.ctg diff --quiet -- src/cli/mod.rs`), explain why it cannot be a Verify block, and give a concrete recovery. The precondition is sound: the coordinator checks it before collect, when the lane's edit is not yet in the live tree, so a non-zero exit can only mean foreign dirt. It is red today, as it should be.
- B2 is fixed. The trace README's `Talks to` reads "calls nothing in the crate; `log` calls it" in both the spec and the patch. I checked it against the patched tree: the only `crate::trace` use is `src/log/mod.rs:8` (`current`). The log README's "calls `trace` and `settings`; `cli` and `host` call it" also matches: `crate::settings::host()` at `log/mod.rs:59,64` and `log/sink.rs:35`; callers `cli/mod.rs:38,50` and `host/process.rs:173`.
- N1 through N4 are fixed. prd.md acceptance names the real test path and `log::tests::`. The probe's stand-alone `trace` crate closes N2. The census gates `docs/architecture.txt`, and it prints cargo's stderr on failure.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | This is the parent's layout decision, done as one leaf with no behaviour change. prd.md is 323 words. −1: the prescribed trace README says "Gives one unit of work an id and carries it across tasks, messages and processes", and its Why says requests "cannot be joined" without it. Nothing in production mints or scopes that id today (round 1's observation; cc's PRD). A fresh-eyes reader is told the folder does something the running system does not do. |
| Ownership and reuse | 20 | Owner is runtime/cartridge.ctg. `log/` is one file per responsibility (`mod`, `redact`, `sink`, `layer`). Only visibility changes. Nothing is re-exported: the probe checks all 19 names for E0432. Both READMEs' `Talks to` lines match the real `use` edges (verified above). |
| Dependencies and implementable slices | 19 | The footprint covers every changed path. `rg` over the other `*.ctg` crates finds no external caller. The patch applies with `git apply --check` to HEAD, and on top of the live dirty diff. −1: this row moves the only production use of `trace::current` into `src/log/mod.rs`. cc's dead-code PRD has footprint `src/trace` and `src/lib.rs` only, so once this lands, deleting `trace` also needs `src/log`. The plan does not hand that on. It is not a conflict: the two footprints overlap, so the rows serialise. |
| Observable acceptance and baseline evidence | 18 | I re-ran every block, and each one discriminates (Validation). −2: the no-behaviour-change claim rests only on the six sink tests and the diff reading. My mutant B dropped the `redact` call on a non-string `msg` in `diagnostic_line`, and all four blocks still passed. So "code moves verbatim" is not gated, and the spec names the diff reviewer as backstop only for the README text, not for the moved bodies. |
| Failure, recovery and compatibility | 18 | The landing precondition and recovery are concrete and correct. −1: there is a check-then-collect window in which another session can dirty `src/cli/mod.rs` again. The recovery covers it, but the plan does not say to re-run the check right before collect. −1: "Until then, wait" has no bound or escalation. If the passthrough session never lands or withdraws its hunk, the row stalls with nothing to trigger a decision. |
| Reviewer total | 94 / 100 | |

### Findings and concrete revisions

No blocking findings. Non-blocking, for the implementer or the coordinator:
- N5: in the spec, name the diff reviewer as the backstop for "moved verbatim". Optionally add a census check: strip visibility and `use` lines from `git show 324f36e:src/trace/mod.rs` and from `cat src/trace/mod.rs src/log/*.rs`, then `comm` the sorted body lines. Mutant B (redaction dropped in `diagnostic_line`) passes every current block.
- N6: make the trace README honest about today's state. For example, its Why could say the id is not minted in production and point to `@runtime/the-correlation-id-is-minted-by-transport-so-src-trace-is-dead-code`, or the Does line could be worded as the API rather than a running behaviour.
- N7: tell cc's dead-code PRD that after this row lands, `src/log/mod.rs:8` imports `crate::trace::current`, so its footprint needs `src/log`.
- N8: state that the landing check is re-run immediately before collect, and give a wait bound: after it, the coordinator asks the owning session of the passthrough edit.

Disposition: keep. Proceed to implementation under the Landing precondition.

### Validation

I extracted the three `sh` blocks verbatim from spec01.md with awk and ran each as `env -u CARTRIDGE_YOLO -u CARGO_TARGET_DIR sh -eu -c "<block>"`. The cwd was the root of a detached worktree of cartridge.ctg at `445a87f` under `scratchpad/reviewer-trace-2/wt`. The kache wrapper was on. Cargo.toml has no path deps, so no sibling symlinks were needed.
- `git apply --check analyst-1-probe.patch` exited 0.
- Unpatched (discrimination):
  - census: exit 1 in 24 s ("log::tests::a_credential_or_a_prompt_body_is_omitted_and_named is not in the census").
  - probe: exit 101 in 16 s (E0433).
  - lint: exit 1 in 0 s (`src/log/*.rs` does not exist).
- Patched, cold target (the unpatched target moved away):
  - census: exit 0 in 28 s.
  - probe: exit 0 in 22 s.
  - lint: exit 0 in 9 s.
  - test block: exit 0 in 1 s, 6 passed, 168 filtered out.
- Simulated pass 2 (HEAD, plus the live dirty diff `README.md`, `src/cli/{args,host,mod}.rs`, plus the patch):
  - census: exit 0 in 5 s.
  - probe: exit 0 in 14 s.
  - lint: exit 0 in 10 s.
  - test block: 6 passed.
  - Pass 2 can pass. The target dir `target/prd-trace-log-split-verify` does not touch `target/{debug,release}`.
- Mutant A, `pub mod old { pub use crate::log::{diagnostic, flush, subscribe, Layer}; }` appended to `trace/mod.rs`: the census exits 0 and the probe exits 1 ("src/trace/mod.rs does not stand alone as the correlation id", E0432). Caught.
- Mutant B, `redact(&mut other, …)` replaced by `let _ = &mut other;` in `log/mod.rs` `diagnostic_line`: census, probe and lint exit 0, and the test block passes 6/6. Not caught (N5).
- Cleanup: I reverse-applied the patch and the dirty diff, which left the worktree clean. `git worktree remove` without `--force` exited 0. Live cartridge.ctg status is unchanged.

Reviewer identity: coordinator-4b fresh agent, round 2.
User rating: not required under delegation.
User feedback/provenance: none for this revision.
Result: PASS (94/100, no blocking findings).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation. Collect only when the Landing precondition exits 0. Apply N5–N8 at the coordinator's discretion.
