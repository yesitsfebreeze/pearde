# @runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/declared-settings-live-in-settings review history

Plan: `@runtime/src-is-one-folder-per-job-and-each-folder-explains-itself/declared-settings-live-in-settings` (`prd.ctg/.cartridge/boards/runtime/prds/src-is-one-folder-per-job-and-each-folder-explains-itself/declared-settings-live-in-settings/prd.md`).
Scope: leaf. `src/transport/settings.rs` moves to `src/settings/spec.rs`, the path is rewritten, and `src/settings/README.md` is added. No behaviour changes.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Method: `prd.ctg/.cartridge/workflows/review-plan.md`.

## Round 1 — 2026-09-19

Presented revision: the cartridge.ctg base in the spec is `324f36e`. Live HEAD was `1404881` during the review and `445a87f` at the end. Neither moved anything under `src/settings`, `src/transport`, `docs/settings.txt` or `.cartridge/tests/unit/src/settings` (`git diff --stat 324f36e HEAD -- …` printed nothing). The spec is byte-identical to the analyst's `spec01-draft.md` (`diff` exit 0).

| Input | Content digest |
| --- | --- |
| Plan | `declared-settings-live-in-settings/prd.md` sha256 `13fa22b4fe0db0228528967a4ff73d9e3dce5cd71ead603c52cf971d129e4cb1` |
| Specs | `declared-settings-live-in-settings/specs/spec01.md` sha256 `601244ee747027c98dfcb03c5203850e95d4fc958257fe3e633164fd3befea42` |
| Material contracts/dependencies | parent `prd.md` `3f158474…`; sibling README child `every-src-folder-has-a-fresh-eyes-readme-and-the-audit-demands-it/prd.md` `4e9ce7ed…`; analyst patch `analyst-settings/attempt.patch` `9be2cc94…`; engine `prd.ctg/src/lifecycle.ts:65,93,111`; rule "No legacy retention: superseded code, docs and fixtures are deleted in the same change" (`just prompt` line 32, `system/delete-superseded-work.md`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The outcome is clear and is one step of the parent's layout. It is small and moves no behaviour. −2: the scope stops at `src/`, but the crate's own user-facing manual (`docs/settings.txt`, which `cartridge help` serves through `src/cli/manual.rs`) keeps naming the module this change removes. |
| Ownership and reuse | 17 | `settings` is the right owner. `yolo`/`YOLO_ENV` belong with it: they override the declared `yolo` setting and are re-exported unchanged as `settings::yolo`/`settings::YOLO_ENV`, and outside callers (for example `cartridge::settings::YOLO_ENV` in the agent PRD) keep their path. I grepped the whole superproject with hidden files included: the only users of the old path are `src/settings/mod.rs:8,18` and `docs/settings.txt:89-90`, and no sibling crate depends on cartridge.ctg. −3: the spec calls the docs example "prose, not a crate path" and leaves it out. It is a code sample that names this exact crate module. The siblings it describes (`fs.ctg/src/service.rs:72`, `proxy.ctg/src/service.rs:81`, `harness.ctg/src/lib.rs:1627`) use `crate::settings::declared/merge`. After the move, `transport::settings` names nothing anywhere. |
| Dependencies and implementable slices | 18 | One spec with three steps and exact anchors. The patch applied cleanly at `324f36e` and at `1404881`. The README's `Talks to` matches the real `use` edges at base: it calls `error`, `lua` and `trust`, and is called by `cli`, `host`, `loader`, `lua`, `node`, `sandbox`, `trace` and `trust` (checked with `rg`). The spec says what to do if `composition/` lands first. −2: block 1 compares against the pinned `git show 324f36e:src/transport/settings.rs`. A lane cut from a later HEAD survives this: 324f36e is an ancestor, and I ran the blocks at 1404881 and they passed. But any commit that edits `src/transport/settings.rs` before this lands turns a correct move red, and the gate would then reward reverting that commit. At the moment no open or claimed PRD's footprint names that file; the two deferred PRDs that cite it do so only in prose. |
| Observable acceptance and baseline evidence | 16 | Base is red and the patch is green; the table under Validation has the details. All 9 pinned names pass, and exactly those 9 are selected (165 filtered). I killed mutants M1 and M2. My own measurement backs PRD box 4: `cargo test --workspace --all-targets -- --list` gives the same 196 names at base and after the patch (`diff` exit 0). −4: that equality is argued in the spec, not gated. Mutant M3b, a clean `#[test]` added inside the footprint (`src/settings/mod.rs`), passed every block, with the test block reporting 10 passed. The spec's own box 5 says "No `#[test]` is added or removed". `Talks to` is also ungated, as the spec admits, and the diff reviewer backstops both. The old-path grep leaves out `docs/`, so the docs gap cannot show up. |
| Failure, recovery and compatibility | 14 | Recovery is `git revert` of a pure rename. There is no compatibility shim, which is correct: nothing outside the crate uses the path. Pass 2 runs clippy on the whole dirty live tree. I measured it, clippy with an isolated target and `--locked` exits 0 in 6 s warm today. Every cargo gate here compiles the whole crate under `[lints.rust] warnings = "deny"`, so a peer's half-finished edit can turn any collect red. That is inherent to the engine and was not deducted beyond −1. −5: blocking finding B1, since the change leaves superseded docs behind, against a standing project rule. |
| Reviewer total | 83 / 100 | |

### Findings and concrete revisions

Blocking:

- **B1: superseded docs survive the change.** `cartridge.ctg/docs/settings.txt:89-90` shows `transport::settings::declared(DOCUMENT)` and `transport::settings::merge(...)`. After this change that module exists nowhere. `cartridge help` serves the file (`src/cli/manual.rs` indexes `docs/`). The rule "superseded code, docs and fixtures are deleted in the same change" (`just prompt`, line 32) applies. The PRD's own box 2 says "Every `transport::settings` path in the crate … names `settings::spec`". **Revision:** add `docs/settings.txt` to the PRD and spec footprints. Change the two lines to `crate::settings::declared` and `crate::settings::merge`, which is what the siblings the example describes really call. Widen block 1's grep to `src .cartridge/tests docs`. The fix is 2 lines and one grep path.

Non-blocking:

- **N1: the pinned base sha makes the gate brittle.** Block 1 compares against `324f36e`. A cheaper and sturdier source is the last committed version of the file, for example `c=$(git rev-list -1 HEAD -- src/transport/settings.rs)`, then `git show "$c:src/transport/settings.rs"` if that blob exists, otherwise `"$c^:…"`. Otherwise, write down that any upstream edit to the file forces a spec revision and must never be reverted just to pass the gate.
- **N2: "same test names" is argued, not gated.** M3b survived every block. Either gate it (for example, the footprint's Rust files other than the pre-existing `#[path] mod tests;` lines contain no `#[test]`), or state the ceiling and name the diff reviewer as the backstop in the spec's Notes. Collect evidence: the `--list` diff above (196 = 196, identical).
- **N3: deferred PRDs cite the old path by line number.** `failures-carry-a-type/prd.md:22` and `no-panic-answers-a-recoverable-failure/prd.md:25` cite `transport/settings.rs` line numbers, and so does the claimed `@agent/a-denied-tool-call-journals-its-error-flag` spec. These are prose citations, not footprints, so nothing is stranded. The coordinator should retarget them to `settings/spec.rs` when those PRDs are revived.
- **N4: the scratch paths are fixed.** `${TMPDIR}/ctg-settings-spec-moved.rs` and the shared target dir collide if two reviewers or collects run this spec at once. This is harmless in practice and optional to fix (use `mktemp`).

Disposition: revise. Fix B1, and optionally N1 and N2. Everything else is ready to implement.

### Validation

My own disposable worktree at `scratchpad/reviewer-settings-1/wt`. The blocks were extracted with the engine's regex and run as `sh -eu -c` with cwd set to the worktree root. Cold runs used a fresh `TMPDIR` with `CARGO_BUILD_RUSTC_WRAPPER=` and `RUSTC_WRAPPER=` (no compiler cache).

| Tree | CARTRIDGE_YOLO | b1 | b2 | b3 (rustfmt+clippy) | test block |
| --- | --- | --- | --- | --- | --- |
| 324f36e, cold | unset | 1 ("settings.rs still exists") | 1 ("README.md does not exist") | 1 (rustfmt: no spec.rs) | 0, 45 s, 9/9 pinned ok |
| 324f36e | =1 | 1 | 1 | 1 | 0, 9 s, 9/9 |
| 324f36e + patch, cold | unset | 0 | 0 | 0, 21 s | 0, 35 s, 9/9 |
| 324f36e + patch | =1 | 0 | 0 | 0, 1 s | 0, 12 s, 9/9 |
| 1404881 + patch | unset | 0 | 0 | 0, 7 s | 0, 21 s, 9/9 |
| M1: `return x + 1;` fn appended to settings/mod.rs | unset | 0 | 0 | **101** (clippy::needless_return, denied) | 0 |
| M2: yolo merge removed from `settings::apply` | unset | 0 | 0 | 0 | **101**, `yolo_overrides_the_configured_value_only_where_the_cartridge_declares_it` failed (8/9) |
| M3: `assert!(true)` test in `.cartridge/tests/unit/src/settings/files.rs` | unset | 0 | 0 | 101 (assertions_on_constants), caught only by accident | 0, 10 passed |
| M3b: clean `#[test]` in `src/settings/mod.rs` | unset | 0 | 0 | 0 | 0, 10 passed. **Survived.** |

Worst cold block: the test block at 45 s. About 12–15 s of that is the tests' own runtime. It is well under the 120 s limit.

Other commands I ran:

- `cargo test --workspace --all-targets -- --list`: 196 names at base and 196 after the patch. `diff` exit 0.
- `cargo fmt --all --check` after the patch: exit 0.
- Live `cartridge.ctg`, with an isolated `CARGO_TARGET_DIR` and read-only on source: `cargo clippy --workspace --all-targets --quiet --locked` exit 0 in 6 s. `git status` was the same before and after.
- `rg --hidden 'transport::settings|transport/settings'` across the superproject found code only at `src/settings/mod.rs:8,18` and `docs/settings.txt:89-90`, and the rest in prd records.
- `just prompt` exit 0, which is where the rule came from.

Cleanup: the patch was reverted with `git apply -R`, then `git worktree remove` without `--force` exited 0, and the scratch targets were deleted. The live checkout, the PRD, the spec and the planning state were not touched.

Reviewer identity: independent reviewer subagent (Claude Opus 5), round 1. It did not write the plan.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **FAIL** (83/100, one blocking finding).
Unresolved blocking findings: B1, superseded `docs/settings.txt:89-90` is outside the footprint.
Rounds used / remaining: 1 / 4.
Next action: bounded revision. Widen the footprint to `docs/settings.txt`, fix the two lines, widen the grep, and optionally make N1 and N2 sturdier. Then run review round 2.

## Round 2 — 2026-09-19

Presented revision: spec01 as revised by analyst-2, with the base in the spec at cartridge.ctg `445a87f`. Live HEAD was `445a87f` when the review started and `d03409e` when it ended. The commits in between (`d04ab33`, `f56c442`, `d03409e`) changed nothing under `src/settings`, `src/transport` or `docs/settings.txt` (`git diff --stat 445a87f d03409e -- …` exit 0). They did add tests under `.cartridge/tests/unit/src/tests/composed`. The patch applies cleanly at `d03409e`, and every block is green there. The live cartridge.ctg working tree is dirty with other sessions' edits (`README.md`, `src/cli/{args,host,mod}.rs`), none of them in the footprint. It was not touched.

| Input | Content digest |
| --- | --- |
| Plan | `declared-settings-live-in-settings/prd.md` sha256 `67571a4dfdcf71c1c0043ef25ac6b1d1e1c52fceecc8869067da9fe502e318fc` (footprint now has `docs/settings.txt`) |
| Specs | `declared-settings-live-in-settings/specs/spec01.md` sha256 `48c71ec2eb85919cb06d1d732d984d5dc6a15b2f2a88fe7ac8164fbb187493ce` |
| Material contracts/dependencies | parent `prd.md` `3f15847411f6…`; sibling README child `every-src-folder-has-a-fresh-eyes-readme-and-the-audit-demands-it/prd.md` `4e9ce7edf09d…`; analyst report `.state/loop/declared-settings/analyst-2.md` `3fd6235ec6ce…`; patch `scratchpad/analyst-settings/attempt.patch` `7698cc883eb0cd2d…4c13`; round-1 history `review.md` `a943755aa7bc…`; engine `prd.ctg/src/lifecycle.ts:63-122` (blocks, test block, verify) and `:171-240` (cleanIndex, lane status, pass 2), `src/planner.ts:5` (feet); gates `.cartridge/justfile:136-148` and `cartridge.ctg/justfile:6-11` (`just test runtime` = `cargo nextest run --workspace`, `just check runtime` = `cargo fmt --all --check` + `cargo clippy --workspace --all-targets`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | B1 is fixed. `docs/settings.txt` is in both footprints, step 4 rewrites lines 89-90 to `crate::settings::declared/merge`, which matches `fs.ctg/src/service.rs:72-73`, `proxy.ctg/src/service.rs:81-82` and `harness.ctg/src/lib.rs:1627-1628`, and the grep covers `docs`. An `rg --hidden` over the whole superproject (excluding `target/` and `prd.ctg/`) finds the old path only in `src/settings/mod.rs`, `docs/settings.txt` and the gitignored retired code index. −1: PRD box 2 says every old path "names `settings::spec`". The spec instead routes callers through the `settings::*` re-exports and the docs through `crate::settings::`, and only `src/settings/mod.rs` names `spec::`. The spec is right and the PRD wording is loose, which will make ticking that box ambiguous at collect. |
| Ownership and reuse | 19 | `settings` is the right owner, and no shim is left behind. The README draft matches the code at base. It calls `error`, `lua` and `trust` (`rg -o 'crate::\w+' src/settings/` gives only those three). It is called by `cli host loader lua node sandbox trace trust`. Every type in `Owns` exists (`Kind`, `Spec`, `Specs` in spec.rs, `Host` in host.rs, `Sources` in files.rs). −1: `Start at` names `apply` in `spec.rs`. The entry point that callers actually reach is `settings::apply` in `mod.rs`, which applies the yolo layer first, so a newcomer who starts in spec.rs misses that step. |
| Dependencies and implementable slices | 18 | Five exact steps, and the patch applies at `445a87f` and `d03409e`. −2 (N5): step 1 says `git mv`. That stages the rename: I ran `git mv` in the worktree, `git diff --cached --name-only` then printed `src/settings/spec.rs`, and `git status --porcelain` printed `R  src/transport/settings.rs -> src/settings/spec.rs`. Collect's lane pass throws on both, first at `cleanIndex` ("repository has staged changes; preserve them before collection", `lifecycle.ts:172`) and then at the rename check in the status loop ("collection requires explicit handling of renames", `:218`). Lanes are normally left uncommitted: `445a87f` is itself a collect-made `Implement …` commit. So an implementer who follows step 1 to the letter gets a collect that is refused. The analyst never hit this because the patch is applied with `git apply`, which stages nothing. |
| Observable acceptance and baseline evidence | 18 | N2 is fixed. Block 4 kills M3b in the lane shape and in the pass-2 shape, on repeated runs, and with CARTRIDGE_YOLO inherited. Block 1 kills docs-left-behind. My own mutants also died: C (validation bypass) failed 3 of the 9 pinned tests, and a `Start at` of `appl` was caught by `\b` in block 2. The analyst's blocks-at-base claim is not quite what I saw (see N7). −1: PRD box 4 says the tests `just test runtime` runs "all pass", but the spec gates only the 9 settings tests. The full suite is fast enough to gate: `cargo nextest run --workspace` on the patched tree gave 196/196 in 27 s warm, exit 0. The spec neither gates it nor names who runs it. −1: `Owns` and `Talks to` are ungated. A README-lies mutant (`Owns: Frobnicator`, `Talks to: calls asp`) passed block 2. This is a known ceiling, and the diff reviewer is the backstop. |
| Failure, recovery and compatibility | 17 | Recovery is `git revert` of a pure move. N1 is fixed: with an upstream commit that edits `src/transport/settings.rs`, block 1 passes on the edited content and fails on the stale content, in both the lane and the pass-2 shape. N4 is fixed for scratch: `mktemp` plus a trap, and no `ctg-settings-spec.*` directories were left behind. −2 (N6): the Notes say the shared target is safe because "cargo's own lock makes concurrent runs safe". That is false. The root package's artifact name does not depend on its path, so block 4's before-copy and the tree under test both write `debug/deps/cartridge-e31ef922f87b2f0b`. At base, a test block run after block 4 executed the before-copy's binary, whose baked-in `CARGO_MANIFEST_DIR` (`…/ctg-settings-spec.s96X9S/before`, confirmed with `strings`) had already been deleted. `refused_settings_do_not_wedge_the_process_when_diagnostics_are_on` then failed with ENOENT at `tests/mod.rs:33`, 8/9, twice in a row. The same test block run alone passed 9/9. Inside one collect this cannot happen, because block 1 forces different file sets and so both sides rebuild. A second run from another tree with the same `TMPDIR` in the window between block 4 and the test block can execute the other tree's binary, which gives a spurious red or a false green. −1: as in round 1, pass 2 compiles the dirty live tree three times, which the engine forces. |
| Reviewer total | 91 / 100 | |

### Findings and concrete revisions

Round-1 findings, rechecked:

- **B1: resolved.** The footprint (PRD and spec), step 4 and the widened grep are all in place. With `docs/settings.txt` restored from base, block 1 exits 1 with "the old transport settings path is still named" and prints lines 89-90, under both YOLO settings.
- **N1: resolved.** The before-tree logic holds in both passes. With the patch uncommitted, `before=HEAD`. With the move committed, `before=$(git rev-list -1 HEAD -- old)^`. I also added an upstream probe commit that edited the file and checked four cases: lane, edited content, exit 0; lane, stale content, exit 1; pass 2, edited, exit 0; pass 2, stale, exit 1. Block 4 on the post-upstream pass-2 tree exits 0.
- **N2: resolved.** See the mutant table below.
- **N4: resolved** for the scratch files. The shared target is deliberate, but the reason the Notes give for it is wrong (N6).
- **N3: left to the coordinator**, as in round 1.

Blocking: none.

Non-blocking:

- **N5: `git mv` in step 1 makes collect refuse the lane.** Evidence is in the dimensions table. **Revision:** say "move the file (`mv`, or `git mv` then `git reset -q`); leave the index clean for collect", or tell the implementer to commit in the lane. Both shapes are proven green.
- **N6: the reason given for the shared target dir is wrong.** **Revision:** delete the sentence about the cargo lock and write the actual constraint. Blocks 4 and 5 must run in that order with no other tree using the same target. Alternatively, use the engine-facts form, `export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/declared-settings-verify}"`, which gives one target per tree. That keeps pass 2 away from `target/debug` and removes cross-tree swaps, at the cost of a cold pass 2.
- **N7: running the blocks at base produces a spurious red that looks like a baseline failure.** Block 4 at base (identical file sets) leaves the before-copy's test binary as the fresh artifact, so the test block then fails with ENOENT, as described under N6. This does not happen during collect, because block 1 fails first at base. It does contradict analyst-2's "base, test block 0, 9/9", and anyone measuring a baseline should run the test block in its own target or before block 4.
- **N8: PRD box 4 ("all pass") is broader than the gate.** Either add `run: env -u CARTRIDGE_YOLO CARGO_TARGET_DIR=… cargo nextest run --workspace` as a second test block (27 s warm today), or state in the spec that the full suite is the verifier's evidence rather than a Verify gate.
- **N9: the PRD box 2 wording.** It should say callers keep `crate::settings::*` and only `settings/mod.rs` names `spec::`. This is a body-only edit to the PRD.

`--test-threads=1` hides nothing. Parallel `cargo test --lib settings` passed 5 runs out of 5, 9/9 each. `cargo nextest run --lib -E 'test(settings)'`, one process per test, passed 9/9. So no test depends on order, and the flag only works around the harness race on process-global `CARTRIDGE_HOME`, which is the same isolation `just test` gets from nextest. `env -u CARTRIDGE_YOLO` in the `run:` line is necessary: with `CARTRIDGE_YOLO=1` and no unset, `an_untrusted_project_config_is_refused_at_its_read` fails (8/9).

The before-tree logic in block 4 is sound in both passes, with one condition: its correctness depends on the file set changing between before and after. When the file sets differ, cargo sees a dep-info file missing on each side and rebuilds both trees. Block 1 guarantees they differ whenever block 4 runs inside collect. The analyst's known gap remains: a partial lane commit that leaves the deletion uncommitted puts a `#[test]` added in that commit on both sides. The diff reviewer is the backstop for that.

Disposition: keep. Proceed to implementation. Fold N5 and N6 into the spec before the implementer starts (each is a one-line edit), and N8 and N9 if convenient.

### Validation

Worktree: `scratchpad/reviewer-settings-2/wt`, created with `git worktree add … HEAD --detach` at `445a87f`. I extracted the blocks from a snapshot of spec01 using the engine's `verificationBlocks` regex: 4 `sh` blocks and 1 `test` block. The `sh` blocks ran as `sh -eu -c` with cwd set to the worktree root. The test block ran through the engine's wrapper (`PRD_TEST_REPORT…; exec >log 2>&1; set --\n<run>`), and each `pass:` name was matched as `^test (…::)?name ... ok$`. Each scenario had its own `TMPDIR` under the scratch directory. Cold runs were fresh `TMPDIR`s with `CARGO_BUILD_RUSTC_WRAPPER= RUSTC_WRAPPER=`, and a `cargo build -v` probe confirmed that plain `rustc` ran with no kache. YOLO=1 means `env CARTRIDGE_YOLO=1` for the whole block, and YOLO unset means `env -u CARTRIDGE_YOLO`.

| Tree | YOLO | b1 | b2 | b3 fmt+clippy | b4 names | test block |
| --- | --- | --- | --- | --- | --- | --- |
| 445a87f base, cold | unset | 1 "settings.rs still exists" | 1 "README.md does not exist" | 1 (no spec.rs) | 0, 196 = 196, 15 s | 101, 8/9 (N7: ENOENT, before-copy binary) |
| 445a87f base | =1 | 1 | 1 | 1 | 0, 1 s | 101, 8/9 (N7) |
| base, test block alone, cold target | unset / =1 | | | | | 0, 9/9, 28 s / 5 s |
| + patch uncommitted (lane shape), cold | unset | 0 | 0 | 0, 10 s | 0, 196 = 196, 16 s | 0, 9/9, 9 s |
| + patch uncommitted, cold | =1 | 0 | 0 | 0, 10 s | 0, 15 s | 0, 9/9, 12 s |
| + patch committed (pass-2 shape), cold | unset | 0 | 0 | 0, 11 s | 0, 19 s | 0, 9/9, 12 s |
| + patch committed, warm | =1 | 0 | 0 | 0, 0 s | 0, 16 s | 0, 9/9, 18 s |
| + patch committed, warm | unset | 0 | 0 | 0, 1 s | 0, 14 s | 0, 9/9, 11 s |
| d03409e + patch uncommitted | unset | 0 | 0 | 0, 4 s | 0, 200 = 200, 10 s | 0, 9/9, 9 s |
| d03409e + patch uncommitted | =1 | | | | 0, 7 s | 0, 9/9, 5 s |

The slowest cold block was 28 s (the test block alone), and the slowest block 4 was 19 s, both against a 120 s limit.

| Mutant (on the patch) | Result |
| --- | --- |
| M3b: `#[test] fn m3b_extra() {}` appended to `src/settings/mod.rs`, pass-2 shape | b1 0, b2 0, b3 0, **b4 1** (`> settings::m3b_extra: test`), test block 0 with 10 passed. The second run of b4: **1**. b4 with YOLO=1: **1** |
| M3b, lane shape (uncommitted) | b1 0, **b4 1** |
| Docs left behind (`docs/settings.txt` from base) | **b1 1**, unset and =1 |
| Own C: `settings::apply` returns the unvalidated config (`spec::apply(..).map(\|_\| config)`) | b1 0, b3 0, b4 0, **test block 101**: `keys_inside_an_absent_optional_table_stay_absent`, `naming_the_table_fills_the_keys_inside_it` and `yolo_overrides_…` failed |
| Own: README `Start at: \`appl\`` (prefix of `apply`) | **b2 1** "names appl, which is no function under src/settings" |
| Own: README `Owns: Frobnicator`, `Talks to: calls asp` | b2 0, **survived** (known ceiling; the diff reviewer is the backstop) |
| Upstream probe commit edits `src/transport/settings.rs`, then the move | lane with edited content b1 0, stale content **1**; pass 2 with edited content b1 0, stale content **1**; pass 2 b4 0 |

Other commands:

- `cargo fmt --all --check` on the patch: exit 0.
- `cargo nextest run --workspace` on the patch: 196/196 passed, exit 0, 27 s.
- `cargo nextest run --lib -E 'test(settings)'`: 9/9, exit 0.
- `cargo test -q --lib settings`, run in parallel 5 times: 9/9 each time.
- `CARTRIDGE_YOLO=1 cargo test --lib settings -- --test-threads=1`: exit 101, `an_untrusted_project_config_is_refused_at_its_read` failed.
- `strings` on `deps/cartridge-e31ef922f87b2f0b` after the base run shows the deleted `…/ctg-settings-spec.s96X9S/before` as its manifest dir.
- `git mv` probe: `R  src/transport/settings.rs -> src/settings/spec.rs`, and the cached list is non-empty.
- `rg --hidden` over the superproject for the old path, as described above.

Every cargo command used a scratch `CARGO_TARGET_DIR`. No `just` target was run. No process was killed.

Cleanup: the patch was reverted with `git apply -R`, and the worktree status was clean. `git worktree remove` without `--force` exited 0. No branch was created, and the probe commits `111f76c`, `93a0136` and `b56b9a2` exist only as dangling objects. **Two items are still outstanding:**

- A safety hook refused `git stash drop`. The stash `9b5a51629ce1e34f86cd927a92fea09e711f8338` ("WIP on (no branch): 445a87f", holding only the analyst patch) is still at `stash@{0}` in cartridge.ctg's shared stash list, above four stashes that belong to other sessions. Drop it by that sha.
- A safety hook also refused `rm -rf` on the scratch cargo targets `scratchpad/reviewer-settings-2/t1`–`t5`, about 3 GB. They are still there.

The live checkout, the PRD, spec01, review.md and the planning state were not touched. `git -C cartridge.ctg status` was identical before and after the review.

Reviewer identity: independent reviewer subagent (Claude Opus 5), round 2. It did not write the plan or the round-1 review.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: **PASS** (91/100, no blocking finding).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation. Before the implementer starts, make the one-line edits for N5 (no staged `git mv`) and N6 (correct the note on the shared target, or use one target per tree). These do not change the gates' semantics, and the diff should be recorded to keep this rating.

### Coordinator note after round 2

Coordinator cartridge-20 applied N5 after the pass: step 1 now says plain `mv` instead of `git mv`, because collect refuses a lane with staged changes. No gate, footprint or acceptance box changed. N6 to N9 are non-blocking and go to the implementer and the diff reviewer.
