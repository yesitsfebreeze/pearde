# @root/a-verify-build-never-restarts-a-live-cartridge review history

Plan: @root/a-verify-build-never-restarts-a-live-cartridge, `prd.ctg/.cartridge/boards/root/prds/a-verify-build-never-restarts-a-live-cartridge/prd.md`.
Scope: leaf. A cargo test/build that rewrites a loaded cartridge's `target/debug` dylib no longer restarts that cartridge in a running host; `cartridge reload <id>` / `just proxy` still does.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-16

Presented revision: prd.ctg 9bcdcab0 (prd.md and spec01.md committed, clean); superproject ab2bdca; cartridge.ctg a965d6e (feature under narrowing: 771e046).

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-verify-build-never-restarts-a-live-cartridge/prd.md` sha256 `aee335e88a06b3ee76906d84a1d86672a056e7583317d125095da62bd1c9775d` |
| Specs | `prds/a-verify-build-never-restarts-a-live-cartridge/specs/spec01.md` sha256 `354b7e383b6540077f4c227a878c00657a630a7678349daab6cbf8f96eafe95c` |
| Material contracts/dependencies | `.state/loop/a-verify-build-never-restarts-a-live-cartridge/attempt.patch` sha256 `7764d446c131ecc33383b136d7090896a691d363804c92ce7f328e9e9ddb1809`; `analyst-1.md` sha256 `64ec871a57e852d8e247e894c39a1e2ba7360292a17a2dae8caf502a221ce9df`; root `.cartridge/memos/routine/cartridge-proxy.md` sha256 `944cd38f…1410`; root `.cartridge/memos/routine/cartridge-runtime.md` sha256 `6cf7be43…4f1a`; `.cartridge/memos/routine/cartridge-development.md` (`build` = `_cargo build` + `links` + `install`, no reload); `.cartridge/justfile` `_one test lifecycle`; cartridge.ctg a965d6e `src/loader/document.rs:305-312`, `src/host/watch.rs`, `src/host/mod.rs:565-584`, `.cartridge/tests/unit/src/tests/mod.rs:26` (`built` honours `CARGO_TARGET_DIR`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Real, current harm: any gate whose tests run `cargo build --lib` (harness/agent/memory/memo) restarts live cartridges and drops other sessions' calls; five specs also run `just build <owner>` in the live checkout. One outcome, one owner, small diff. -3: 771e046's purpose (`just build proxy` hot-restarts the proxy, the @root/one-daemon audit gap "a rebuilt native module does not reload nodes") is dropped, and the plan does not record that this audit item is now closed as "reload is explicit" rather than silently reopened. |
| Ownership and reuse | 17 | Reuses the existing `reload` → `Host::replace` path (fresh `cartridge node` process dlopens the current file); no new host convention; `native_candidates` stays as `load_native`'s list. -3: the doc-fix step is not in the Steps list, and the spec body still calls `cartridge-proxy.md` "out of footprint" while the footprint and coordinator note include it (contradiction inside one spec). |
| Dependencies and implementable slices | 16 | No `needs`; one spec; ordered steps; prototype applies cleanly to a965d6e. -4, BLOCKING (F1): footprint incomplete. `.cartridge/memos/routine/cartridge-runtime.md:20` says a changed cartridge restarts "(`cartridge reload <id>`, or on its own when its module is rebuilt)". That becomes false with this change, is composed into agent prompts, and is outside both footprints, so the implementer cannot fix it and collect would reject the edit. |
| Observable acceptance and baseline evidence | 15 | Spec test reproduced both directions in an isolated host (see Validation): FAILS at a965d6e with "a test build restarted the node" (left 2, right 4), passes with the patch; trust test, fmt, clippy, lifecycle all green. The test pins `name: "native_fixture"` so it is not vacuous (analyst's first draft was). -5, BLOCKING (F2): PRD box 1 ("With a daemon running, `cargo test` in a loaded cartridge's submodule using the default target dir leaves that cartridge's generation unchanged") is not what any Verify proves and is not meaningful as worded: per analyst's own probe, plain `cargo test`/`clippy`/`check` never touch the dylib, so the box passes at a965d6e for most submodules; it needs a live daemon plus a default target, which the rules forbid; and no "generation" is observed. The spec's box 2 (rewrite the dylib in an isolated host, node keeps running; reload starts a new node) is the real check. Non-blocking (F4): the reload leg re-copies byte-identical bytes, so it proves a new node process, not that new content is loaded. |
| Failure, recovery and compatibility | 17 | Isolated `CARGO_TARGET_DIR` default, temp `CARTRIDGE_HOME`, takeover test uses its own `XDG_RUNTIME_DIR` and scratch roots; no block touches the live daemon; no writes inside the footprint (`/target/` is gitignored at root). Rollback is a one-commit revert. `init.lua`/`cartridge.json` edits still restart by design. -3: the workflow regression (`just build proxy` no longer restarts the proxy) is handled only by prose; the plan does not say why `just build` should not simply call `cartridge reload` (see F3), so a later implementer may "fix" it that way and reintroduce the bug. |
| Reviewer total | 82 / 100 | |

Findings and concrete revisions:

- **F1 BLOCKING — footprint misses a second stale doc.** `.cartridge/memos/routine/cartridge-runtime.md:20` ("or on its own when its module is rebuilt"). Add it to the PRD and spec01 footprints; add a Step: "edit `cartridge-proxy.md:13-15` and `cartridge-runtime.md:20` to say a rebuilt module is picked up by `just proxy` / `cartridge reload <id>`"; remove the spec's contradictory "Out of footprint" paragraph; add a Verify line such as `if grep -nE 'on its own when its module is rebuilt|does the same on its own' .cartridge/memos/routine/cartridge-runtime.md .cartridge/memos/routine/cartridge-proxy.md; then exit 1; fi`. Other hits checked and fine: `PROMPT.md:177` already names `just proxy` / `cartridge reload <id>`; `prd.ctg/.cartridge/templates/spec.md:25` (isolated target still harmless, optional follow-up); @root/smoke-passes-mcp-and-proxy spec and @root/one-daemon prd.md:52 are history.
- **F2 BLOCKING — PRD acceptance box 1 is unprovable and near-vacuous as worded.** Replace it with the spec's observable check: "In an isolated host, rewriting a loaded cartridge's `target/debug/lib<name>.dylib` the way a test's `cargo build --lib` does leaves its node running (call counter continues)", and state that plain `cargo test` never rewrites the dylib, so the risky case is tests that nest `cargo build`. Keep box 2 and 3.
- **F3 non-blocking — do not make `just build` reload.** A cheap `just build <owner>` → `cartridge status && cartridge reload <owner>` would restore 771e046's convenience but reintroduce the bug: Verify blocks already run `just build <owner>` in the live checkout (e.g. boards/gitfs/overlay-mutations-report-revisions spec01:106-108 and boards/runtime/shipped-gitfs-profiles-grant-change-recording spec01:53-55, both on the default target). `just build runtime` also needs `daemon --replace`, not reload. Record this rationale in spec01's "Option chosen" so the regression is deliberate, and note the one-daemon audit item as closed by "reload is explicit". If an explicit shortcut is wanted later, an opt-in `just reload <owner>` is the shape; not needed now (`cartridge reload` exists).
- **F4 non-blocking — reload leg proves a new process, not new bytes.** Acceptable because `replace` spawns a fresh `cartridge node` that dlopens the current path; optionally assert the node's pid changed, or note the limitation.
- **F5 non-blocking — Verify block 1's `grep native_candidates document.rs` pins implementation shape.** Behaviour is already proven by the host test; the grep is a redundant brittle guard. Keep or drop.
- **F6 non-blocking — analyst claim (3) holds.** Plain `cargo test`/`clippy` do not rewrite the dylib; nested `cargo build --lib` in tests does (analyst probe, inode+mtime change). This makes the spec's rewrite simulation the right test and PRD box 1 the wrong one (F2).

Disposition: revise (keep scope; fix footprint, acceptance wording and rationale).

Validation (reviewer, scratch worktree of cartridge.ctg at a965d6e under the session scratchpad, `CARGO_TARGET_DIR` = scratch clone of the analyst's target, scratch root with `.cartridge`/`justfile` symlinked; the live daemon and live `target/` untouched):
- Test-only hunk of attempt.patch at a965d6e: `cargo nextest run --workspace -E 'test(=tests::host::a_rewritten_native_module_restarts_only_on_reload) | test(=trust::tests::a_built_native_module_is_a_source_so_its_rebuild_restarts_the_cartridge)'` → exit non-zero, host test FAIL 6.6 s "a test build restarted the node" (left 2, right 4); old trust test PASS.
- Full patch, Verify block 1 commands (cwd scratch root): grep finds no `native_candidates`; nextest 3 passed, 6.2 s.
- Block 2: `cargo build --bin cartridge` 0.08 s (warm); `CARTRIDGE_HOME=$(mktemp -d) just test lifecycle` → 11 pass, 42.5 s, "test lifecycle pass"; no leftover `cartridge-takeover` processes.
- Block 3: `cargo fmt --all --check` ok; `cargo clippy --workspace --all-targets -D warnings` exit 0, 2.8 s.
- Blocks were run as their literal commands (a `sh -eu -c "$(cat block)"` wrapper was refused by the local safety hook). Cold target: block 1's nextest into a fresh empty `CARGO_TARGET_DIR` took 25 s, exit 0 (3 passed), well under the 120 s block limit.
- Grep for reliance on auto-restart across root memos, justfiles, PROMPT.md, AGENTS.md, .claude/skills, prd.ctg boards/templates, cartridge.ctg docs: hits listed under F1/F3.

Reviewer identity: independent reviewer agent (coordinator cartridge-c4).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (82/100, 2 blocking findings).
Unresolved blocking findings: F1 (cartridge-runtime.md outside footprint, no doc step/Verify), F2 (PRD box 1 unprovable/near-vacuous).
Rounds used / remaining: 1 / 4.
Next action: one bounded revision of prd.md and spec01.md for F1–F3, then round 2.

## Round 2 — 2026-09-16

Presented revision: prd.ctg 0f32da2e with `prd.md` and `specs/spec01.md` dirty (the round-2 revision,
uncommitted); superproject b3a1660, gitlink `cartridge.ctg` = a965d6e (unchanged base; spec01 still
says "gitlink at root ab2bdca", stale wording only — `git ls-tree HEAD cartridge.ctg` is a965d6e).

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-verify-build-never-restarts-a-live-cartridge/prd.md` sha256 `2fa9785aba435a5504a9a7c42bb7a440c228a91b74a71bc2854b5f99886a941e` (round 1: `aee335e8…`) |
| Specs | `prds/a-verify-build-never-restarts-a-live-cartridge/specs/spec01.md` sha256 `d6cb882bd12812a4e29a99746be911eb85857db03e434717e9ec5792e0a724d3` (round 1: `354b7e38…`) |
| Material contracts/dependencies | `.state/loop/…/attempt.patch` sha256 `7764d446…1809` (unchanged since round 1); `analyst-2.md` sha256 `570b5c9a290addde85d1c2438ce008c59d0e61e0215520ae5fc6bae7486768a6`; root `.cartridge/memos/routine/cartridge-proxy.md` sha256 `944cd38f…1410` and `cartridge-runtime.md` sha256 `6cf7be43…4f1a` (both unchanged, still stale at base); `prd.ctg/src/lifecycle.ts` footprint rules (`:134`, `:153`, `:174`) and lane creation (`:217`); `prd.ctg/.cartridge/templates/spec.md:16-31`; cartridge.ctg a965d6e |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Scope unchanged and still current: a gate whose tests nest `cargo build --lib` rewrites a live cartridge's dylib and restarts it. The revision adds the round-1 missing rationale — the new "Why `just build` must not call `cartridge reload`" subsection records that losing 771e046's convenience is deliberate, cites the two board specs that run `just build <owner>` in the live checkout, and closes the @root/one-daemon audit item as "reload is explicit". -1: the PRD Outcome still ends "The analyst picks one and records why" although spec01 has chosen option 2; a reader of prd.md alone cannot tell the decision is made (cosmetic). |
| Ownership and reuse | 20 | Round-1 F1's two sub-gaps are closed: step 4 now owns the doc edit and the contradictory "Out of footprint … cartridge-proxy.md" paragraph is gone (grepped: no "Out of footprint" text remains in spec01). Independent sweep of `.cartridge/memos`, `PROMPT.md`, `AGENTS.md`, both justfiles, `prd.ctg/.cartridge/templates` and all of cartridge.ctg found no third document promising an automatic restart: only `cartridge-proxy.md:14-15`, `cartridge-runtime.md:20` (both in footprint) and the test name that step 2 renames. Still no new host convention; `reload` → `Host::replace` reused. |
| Dependencies and implementable slices | 18 | No `needs`; one spec; `attempt.patch` applies clean to a965d6e (`git apply --check` exit 0). All three blocks run as their literal commands well inside the 120 s limit (26.8 s / 43.5 s / 6.9 s, cold target), paths repo-root relative, no `cd`, `CARGO_TARGET_DIR` exported at the top of each of the three blocks. Footprint now covers every touched path: `cartridge.ctg` (a directory entry; `lifecycle.ts:134` and `:153` accept `file.startsWith(f + '/')`, so the `src/loader/*` and `.cartridge/tests/*` paths are covered by the gitlink entry) plus both memos verbatim — collect would commit the doc edits. -2: (N1) the new guard is `if grep -nE … fileA fileB`, so a renamed or missing memo makes grep exit 2 and the guard silently pass — `test -f` on both files, or a positive grep for the new wording, would close it. (N2) if a lane is ever created for this PRD, pass 1 cannot run: I reproduced that a fresh worktree of the superproject leaves `cartridge.ctg` an empty directory (`git worktree add --detach`, `ls` → empty), so `--manifest-path cartridge.ctg/Cargo.toml` would not resolve. Board-wide, not introduced here — `.lanes/` is empty and this loop claims at `analyzing`, so `lifecycle.ts:127` runs verify once in `repo` — but the coordinator must not claim this PRD from `specced` (which would create a lane at `lifecycle.ts:217`). |
| Observable acceptance and baseline evidence | 18 | F2 resolved: PRD box 1 is now exactly what Verify block 1 proves, and it is a discriminator, not a restatement. Reproduced both directions in a scratch worktree: with only the test hunks applied (loader at a965d6e) the host test FAILS at `host.rs:1312` "a test build restarted the node" (left 2, right 4) and the renamed trust test FAILS (base `sources.len()` is 3); with the full patch all three named tests PASS in 12.4 s. The memo guard was verified in both states: at base it exits 1 printing `cartridge-proxy.md:14` and `cartridge-runtime.md:20` plus "routine memo still promises an automatic restart"; after making step 4's documented edits in a scratch copy of the two memos it exits 0. Block 2 `just test lifecycle` 11 pass / 0 fail, 43.3 s; block 3 fmt and clippy exit 0. -2: PRD box 2 ("the documented rebuild path still picks up a new build") is still only half-proven — the host test's reload leg re-copies byte-identical bytes, so it demonstrates a fresh `cartridge node` dlopening the current path, not that new content is loaded, and neither `just proxy` nor the `cartridge reload` CLI is exercised by any block (round-1 F4, now disclosed in step 3 rather than closed). Minor: the trust test asserts only `sources.len() == 2` instead of naming the excluded module. |
| Failure, recovery and compatibility | 19 | Verified no block writes inside the footprint: after all three blocks the patched worktree showed only the two intended modified test files with `--untracked-files=all`, and the native fixture crate got no `target/` of its own (the isolated `CARGO_TARGET_DIR` is inherited), so pass 2's `source footprint changed during integrated verification` check (`lifecycle.ts:174`) is safe; root `.gitignore:2` ignores `/target/` anyway. Pass 2 in the live checkout cannot disturb the live daemon: `takeover.test.ts:16-17,34` builds its own `XDG_RUNTIME_DIR` and scratch project roots and block 2 sets a temp `CARTRIDGE_HOME`; the binary under test comes from the isolated target. Rollback stays a one-commit revert plus two doc sentences. -1: step 4 specifies the replacement wording only in prose and the guard checks it only negatively, so a careless rewrite could still leave a misleading sentence; and spec01's "gitlink at root ab2bdca" is now stale. |
| Reviewer total | 94 / 100 | |

Findings and concrete revisions:

- **F1 (round 1, BLOCKING) — RESOLVED.** `.cartridge/memos/routine/cartridge-runtime.md` is in the PRD footprint (frontmatter, the one authorized touch) and in spec01's footprint; step 4 owns both edits; spec Acceptance gained a box for it; Verify block 1 opens with the grep guard. Checked by reproduction: guard exit 1 at base (both memos hit, at the cited lines 14 and 20), exit 0 after the documented edits; both paths are accepted by `lifecycle.ts`'s footprint rule, so collect would commit them.
- **F2 (round 1, BLOCKING) — RESOLVED.** PRD box 1 replaced by the observable isolated-host check, which Verify block 1's host test proves and which fails at a965d6e. The new Outcome paragraph records that plain `cargo test`/`clippy`/`check` never rewrite the dylib (closing F6 too), so the box is no longer near-vacuous. Boxes 2 and 3 unchanged and still untricked in the sense that neither can pass by accident; box 2 remains partially proven (see F4).
- **F3 (round 1, non-blocking) — RESOLVED.** spec01's new subsection records the deliberate loss of 771e046's convenience, the two live-checkout `just build <owner>` Verify blocks that make a reload-inside-build a re-introduction of the bug, `just build runtime` needing `daemon --replace`, the audit item closed as "reload is explicit", and `just reload <owner>` as the shape if ever wanted.
- **F4 (round 1, non-blocking) — DISCLOSED, not closed.** Step 3 now states the reload leg proves a fresh node process dlopening the current path, not new bytes. Accepted; asserting a changed node pid or copying a distinguishable second build would close it.
- **F5 (round 1, non-blocking) — RESOLVED.** The `grep -n native_candidates … document.rs` guard is dropped with a recorded reason; the host test still proves the behaviour (verified: it fails without the loader change).
- **F6 (round 1, non-blocking) — RESOLVED.** Recorded in the PRD Outcome.
- **N1 non-blocking (new) — the memo guard passes vacuously if a memo file is missing or renamed.** `grep` exits 2 on a missing file, which the `if` reads as "no match". Cheap fix: prefix with `test -f .cartridge/memos/routine/cartridge-runtime.md && test -f .cartridge/memos/routine/cartridge-proxy.md`.
- **N2 non-blocking (new) — do not claim this PRD from `specced`.** A lane is a worktree of the superproject (`lifecycle.ts:217`), and a fresh superproject worktree has an empty `cartridge.ctg` (reproduced), so pass 1's `--manifest-path cartridge.ctg/Cargo.toml` would not resolve. With no lane, verify runs once in `repo` (`lifecycle.ts:127`, `templates/spec.md:21`), which is what this loop does today. Board-wide caveat for the coordinator, not a defect of this plan.
- **N3 non-blocking (new) — stale base line.** spec01 says "gitlink at root ab2bdca"; root HEAD is b3a1660 and the gitlink still resolves to a965d6e, so the reviewed base is unchanged. Update the wording at the next edit.

Disposition: keep. Proceed to implementation as specced; no further revision required for the gate.

Validation (independent reviewer; scratch worktree of cartridge.ctg at a965d6e under the session scratchpad, scratch root with `justfile` and every `.cartridge` entry symlinked except a writable copy of `memos`, `cartridge.ctg` symlinked to the worktree; `CARGO_TARGET_DIR` left to the blocks' own default inside the scratch root; the live daemon, the live `target/` and the live memos untouched — both live memo digests unchanged after the run). Blocks were run as their literal commands, in block order; a `sh -eu <file>` wrapper was refused by the local safety hook, as in round 1.

| # | Command (cwd = scratch root unless noted) | Exit | Observed |
| --- | --- | ---: | --- |
| 1 | `git -C <wt> apply --check attempt.patch` then `git apply` | 0 | applies clean to a965d6e; 4 files modified |
| 2 | block 1 guard: `if grep -nE 'on its own when its module is rebuilt\|does the same on its own' .cartridge/memos/routine/cartridge-runtime.md .cartridge/memos/routine/cartridge-proxy.md; then … exit 1; fi` (memos at base) | 1 | `cartridge-proxy.md:14`, `cartridge-runtime.md:20`, then "routine memo still promises an automatic restart" |
| 3 | same guard after applying step 4's documented edits to the scratch memo copies | 0 | no match |
| 4 | block 1: `cargo nextest run --manifest-path cartridge.ctg/Cargo.toml --workspace -E 'test(=tests::host::a_rewritten_native_module_restarts_only_on_reload) \| test(=trust::tests::a_built_native_module_is_not_a_source_so_a_test_build_keeps_the_cartridge) \| test(=tests::host::a_native_module_reaches_the_base_through_the_global)'` (cold target) | 0 | 3 passed, 167 skipped; compile 13.4 s, tests 12.4 s, block total 26.8 s (limit 120 s) |
| 5 | block 2: `cargo build --manifest-path cartridge.ctg/Cargo.toml --bin cartridge` | 0 | 0.13 s (warm after block 1) |
| 6 | block 2: `CARTRIDGE_HOME="$(mktemp -d)"; just test lifecycle` | 0 | 11 pass, 0 fail, 1181 expects, 42.5 s; "test lifecycle pass"; block total 43.3 s |
| 7 | block 3: `cargo fmt --manifest-path cartridge.ctg/Cargo.toml --all --check` | 0 | 0.18 s |
| 8 | block 3: `cargo clippy --manifest-path cartridge.ctg/Cargo.toml --workspace --all-targets -- -D warnings` | 0 | 6.7 s |
| 9 | negative leg: `git apply -R --include='src/loader/*' attempt.patch`, then nextest on the two discriminating tests | non-zero | both FAIL — host test `host.rs:1312` "a test build restarted the node" (left 2, right 4), trust test fails on `sources.len()` (3 at base) |
| 10 | `git -C <wt> status --porcelain --untracked-files=all`; `ls .cartridge/tests/unit/src/tests/fixtures/native/` | 0 | only the two intended modified test files; no `target/` under the fixture — no write inside the footprint |
| 11 | `git -C /Users/feb/dev/cartridge worktree add --detach <scratch>/lanetest HEAD`; `ls <scratch>/lanetest/cartridge.ctg` | 0 | directory empty — basis for N2 |
| 12 | `just --evaluate` in the scratch root | 0 | `root` = scratch root, so the lifecycle gate never reached the live checkout |
| 13 | independent doc sweep (`grep -rniE` over `.cartridge/memos`, `PROMPT.md`, `AGENTS.md`, both justfiles, `prd.ctg/.cartridge/templates`, all of cartridge.ctg) | 0 | only the two in-footprint memos and the test name step 2 renames |
| 14 | `git worktree remove` for both scratch worktrees (no `--force`) | 0 | both removed; `worktree list` clean; live memo digests unchanged |

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: PASS (94/100, no blocking findings).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: proceed to implementation against this revision. Carry N1 (guard `test -f`), N2 (do not claim from `specced`, or populate the submodule in the lane) and N3 (stale base line) as cheap cleanups; F4 stays a disclosed limitation.

## Round 3 — 2026-09-16

Presented revision: the box-2 closure and the rebase. `prd.ctg` HEAD `cd8ec93c` with `prd.md` and
`specs/spec01.md` dirty (planning records, uncommitted); superproject lane branch
`lane/root-a-verify-build-never-restarts-a-live-cartridge` @ `ef45bef` (two routine memos, from root
`b3a1660`); submodule branch `lane/root-a-verify-build` = `906b39a` → `484bbe7` → `4b13113` (live
`cartridge.ctg` `main`) → `92e0490` → `a965d6e`. Root `main` has since moved to `0e3916c` and its
`cartridge.ctg` gitlink is now `4b13113`. Reviewed as a delta on round 2; rounds 1 and 2 are not
re-litigated.

| Input | Content digest |
| --- | --- |
| Plan | `prds/a-verify-build-never-restarts-a-live-cartridge/prd.md` sha256 `4a88b810d52e5c727c0fc26c1bedd41ca67b8efe48fd4b97f92f7353d9300d72` (body unchanged since round 2; the diff versus `prd.ctg` HEAD is round 2's revision plus `state: claimed` and the `claim` line — no Acceptance box ticked) |
| Specs | `prds/a-verify-build-never-restarts-a-live-cartridge/specs/spec01.md` sha256 `3036a11d10287fca2cebc7ebdc764c2dd62f6ef544b787c037d21f652821ff41` (round 2: `d6cb882b…`) |
| Material contracts/dependencies | cartridge.ctg `906b39a` (and `484bbe7`, `4b13113`); lane superproject `ef45bef`; memo blobs at `ef45bef`: `cartridge-proxy.md` sha256 `a6d78f625c9e8e6735be3729deb8ddea5c4d8b3f4b1f17f2ee1067fc88a4d3fa`, `cartridge-runtime.md` sha256 `a9b953ae7e59d100563b300aaff1392250867865767f43a3b0673de384d60001`; `verifier-1.md` sha256 `b2aad76908b40d741569ceedf906195c5c65cf28192e762c251c0d86360ca5c0`; `implementer-1.md` sha256 `14f061d873bf024eb0064bbfd4cabed157566d03ad9f909dda5fe21402bb38e9`; `prd.ctg/src/lifecycle.ts:134,153,165,174`; `.cartridge/tests/integration/takeover.test.ts:218`; cartridge.ctg `src/cli/mod.rs:131`, `src/host/socket.rs:451-453` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Scope unchanged. The delta is the right one for this PRD specifically: this change removes the automatic restart, so proof that the *deliberate* one loads new content is the safety net, not a nicety — closing F4 was worth a round. Nothing was added beyond that: one inert `[features] rebuilt` on an existing test fixture, one extra leg and one extra assertion. -1 (carried, unchanged): the PRD Outcome still ends "The analyst picks one and records why" although spec01 chose option 2; `prd.md`'s body was not touched this round. |
| Ownership and reuse | 20 | The cheapest shape that closes the gap: the *same* fixture, one `cfg!(feature = …)` constant (`FACTOR`), and the existing `built()` helper — which parses cargo's `--message-format=json` `filenames` (`tests/mod.rs:26-58`), so `--target-dir` is honoured and the second artifact's real path comes back. No new fixture crate, no new host code, no new convention; `cartridge reload` → `Host::replace` is still the reused path. The `rebuild` closure was generalised to take a source path rather than duplicated. |
| Dependencies and implementable slices | 18 | Rebase verified sound and content-identical: `git diff a965d6e e4b1514` and `git diff 4b13113 484bbe7` have the **same patch-id** `e83dde6a9d8000ac775385d24d8aed9bbd730ad3`, and diffing the two diffs textually shows only the `host.rs` blob index (`852d343..e302c5c` → `2a6132d..1992726`) and one hunk offset (`@@ -1259` → `@@ -1302`) — `4b13113`'s block lands at `host.rs:1259-1301`, the test appends after it; the other three files are byte-identical. `906b39a` descends from live `main` `4b13113` (`merge-base --is-ancestor` true). Footprint complete: the six paths the two submodule commits touch (`src/loader/{document.rs,mod.rs}`, `trust/tests.rs`, `tests/host.rs`, `fixtures/native/{Cargo.toml,src/lib.rs}`) are all listed in spec01, and the PRD's bare `cartridge.ctg` entry covers every one of them under `lifecycle.ts:134,153`'s `file === f \|\| file.startsWith(f + '/')`; both memos are listed verbatim in both footprints. All three blocks inside budget (26.1 s / 43.5 s / 4.9 s; limit 120 s). -2: (a) the base line is stale again (N3 recurrence) — it says "the `cartridge.ctg` gitlink at root b3a1660 is still a965d6e, two commits behind", but root is now `0e3916c` and its gitlink is already `4b13113`, i.e. exactly the spec's base; (b) the lane superproject `ef45bef` is based on `b3a1660` and no longer contains root HEAD (`merge-base --is-ancestor HEAD ef45bef` false), so `prd collect` would abort at `lifecycle.ts:165` "lane diverged from source HEAD"; step 5 still says only "advance the root gitlink". Both are coordinator-facing, neither is a defect of the change. |
| Observable acceptance and baseline evidence | 18 | **The numbers re-derived from source, not taken from the report.** The fixture is `const FACTOR: i64 = if cfg!(feature = "rebuilt") { 3 } else { 2 }` with `twice(n) = n * FACTOR`; the Lua entry is `local calls = 0; listen("count", function() calls = calls + 1; return native.twice(calls) end)`. So: call 1 on the default build → 2 (asserted); leg (a) rewrite with identical bytes, call 2 → 4 if the node survived, 2 if it restarted (asserted 4); leg (b) rewrite with the `rebuilt` build, call 3 → 6 only if the node both survived *and* still holds the old image (a restart would give 3, a restart onto the old build 2) (asserted 6); leg (c) `host.replace`, call 1 on a fresh node → 3 only if it dlopened the file on disk now — the surviving node would give 4 × 2 = 8 and a fresh node on the old build 1 × 2 = 2 (asserted 3). The claim holds: **3 is reachable no other way**, so one value proves new process *and* new content. The second `--target-dir` is load-bearing and its stated reason is accurate: `tests::host::a_native_module_reaches_the_base_through_the_global` (`host.rs:400-437`) copies whatever `built()` returns from the default target and asserts `twice(21) == 42`, which a shared target holding the `FACTOR 3` artifact would turn into 63. Both non-vacuity legs reproduced independently (see Validation rows 4 and 5), at the exact file:line and left/right values claimed. Six spec boxes, none ticked, each mapped to a command. -2: (a) PRD box 2 as literally worded names `just proxy` and `cartridge reload <id>`; what is observed is `Host::replace`, plus — separately — the real `reload` CLI end to end in `takeover.test.ts:218` (Lua entry, liveness/address/fd only, never new content), and `just proxy` is inspection-only (`cartridge-proxy.md:37`, `exec "$binary" reload proxy`). spec01's box 3 is honest about this (it parenthesises `Host::replace`); the PRD box is not — see the verdict and the exact reword below; (b) step 3 still sends a reader to `attempt.patch` for leg (a) ("it FAILS at the base"), but that file is the pre-rebase, pre-F4 prototype: it contains no `rebuilt` leg (`grep -c rebuilt` → 0) and its `host.rs` pre-image blob is `852d343`, the `a965d6e` version, not `4b13113`'s `2a6132d`, so it no longer applies at the declared base. |
| Failure, recovery and compatibility | 19 | Re-verified for the delta, not assumed: after all three blocks the `906b39a` worktree was clean with `--untracked-files=all` — no `target/` under the fixture (the default build inherits the isolated `CARGO_TARGET_DIR`, the second build is redirected to a `tempfile::tempdir()`), and the fixture's tracked `Cargo.lock` was not rewritten by the `--features rebuilt` build, so pass 2's `source footprint changed during integrated verification` check (`lifecycle.ts:174`) stays safe. The live checkout, the live `target/` and the live memos were never written (live memo digests unchanged; `just --evaluate` in the scratch root reports `root` = the scratch root). No `cartridge-takeover` leftovers. Rollback is still a revert of two commits plus two doc sentences; `init.lua`/`cartridge.json` edits still restart by design. `elsewhere` (the second target dir) outlives its use in leg (b). -1: the two fixture-using tests are now implicitly coupled through a feature — the sibling test's `twice(21) == 42` silently requires the *default* fixture build, and nothing in the fixture, the spec or a comment states "the default build must keep `FACTOR` 2". The fixture is its own workspace (`[workspace]` in its `Cargo.toml`), so no workspace-wide `--all-features` reaches it and the risk today is nil; it is an unstated invariant, not a live bug. |
| Reviewer total | 94 / 100 | |

### Verdict on PRD Acceptance box 2

Box as written: "The documented rebuild path (`just proxy` or `cartridge reload <id>`) still picks up a new build."

**Supported in substance, not as literally worded. Do not tick it as it stands; apply the reword below, then tick.**

What is now proven, and how far each link is carried:

1. **A deliberate reload loads new content.** PROVEN, non-vacuously. Leg (c) asserts `3`; I re-derived
   that constant from the fixture and the Lua counter (above) and confirmed the assertion is sensitive
   to the *file's content at reload time*, not to process identity: with leg (b) altered to leave the
   old build on disk, the test FAILS at `host.rs:1388` with left `Some(Number(2))`, right
   `Some(Number(3))`. Round 1's F4 is **closed**, not disclosed.
2. **`cartridge reload <id>` is that code path.** The CLI is a one-to-one dispatch:
   `src/cli/mod.rs:131-132` (`Command::Reload { cartridge }` → `client::ask(project, "reload", …)`) →
   `src/host/socket.rs:451-453` (`Some(id) => host.replace(id).await`). No extra logic sits between
   them. The socket hop itself is exercised end to end by `just test lifecycle`
   (`takeover.test.ts:218`, real `cartridge reload fronted`, exit 0, node active again) — but for a Lua
   entry, and it asserts address/fd/liveness, never that new content took effect. So the box's
   `cartridge reload <id>` leg is carried by one observation of the content and one observation of the
   CLI, not by a single combined one.
3. **`just proxy`.** Inspection only. `.cartridge/memos/routine/cartridge-proxy.md:37` is
   `if "$binary" status >/dev/null 2>&1; then exec "$binary" reload proxy; fi` — literally the CLI in
   (2) — but no Verify block runs it.

That is enough to tick a box that says what was observed, and not enough for a box that names a shell
recipe nobody ran. Exact wording this evidence proves, to replace PRD box 2 (one line, body-only edit):

```
- [ ] A deliberate reload picks up a new build: `Host::replace` — what `cartridge reload <id>` dispatches to (`src/cli/mod.rs:131` → `src/host/socket.rs:451-453`) and what `just proxy` runs (`cartridge-proxy.md:37`, `exec cartridge reload proxy`) — starts a node that answers out of the rebuilt module (3, which neither the node that was running (8) nor a fresh node on the old build (2) can give).
```

Applying **exactly** that wording is pre-approved by this round and does not make this rating stale:
it narrows the box to what was verified here and adds no new claim. Any other wording is a new
substantive revision and needs round 4.

Per-box dispositions for the coordinator (tick strictly from these):

| Record | Box | Verdict |
| --- | --- | --- |
| PRD | 1 — isolated host, rewritten dylib leaves the node running | TICK (Validation rows 1 and 5) |
| PRD | 2 — documented rebuild path picks up a new build | TICK **after** the reword above; not as currently worded |
| PRD | 3 — `just test lifecycle` passes | TICK (row 2) |
| spec01 | 1 — `resolve` no longer lists a built native module | TICK (rows 1, 5) |
| spec01 | 2 — node survives a rewrite, even a behaviourally different build (legs a, b) | TICK (rows 1, 4, 5) |
| spec01 | 3 — `cartridge reload <id>` (`Host::replace`) answers out of the file on disk now (leg c) | TICK — worded honestly already |
| spec01 | 4 — neither routine memo promises an automatic restart | TICK (rows 1, 3, and the positive read) |
| spec01 | 5 — `just test lifecycle` passes against the built host | TICK (row 2) |
| spec01 | 6 — `fmt --check` and `clippy -D warnings` clean | TICK (row 3) |

Findings and concrete revisions:

- **F4 (round 1, non-blocking) — RESOLVED/CLOSED.** The reload leg now loads a behaviourally
  different build and observes it. Re-derived and reproduced in both directions (Validation rows 1, 4).
- **R3-1 non-blocking — PRD box 2's wording outruns the evidence.** Reword as given above, then tick.
- **R3-2 non-blocking — `attempt.patch` is stale and step 3 still points at it.** It has no `rebuilt`
  leg and its pre-image `host.rs` blob is `852d343` (the `a965d6e` version), so it does not apply at
  the declared base `4b13113`. Either drop the sentence "Leg (a) is the reusable attempt in
  `attempt.patch`" or refresh the file from `906b39a`. Cosmetic; no gate reads it.
- **R3-3 non-blocking — base line stale again (N3 recurrence).** "the `cartridge.ctg` gitlink at root
  b3a1660 is still a965d6e, two commits behind" is true of `b3a1660` but root is now `0e3916c`, whose
  gitlink is already `4b13113` — the spec's base. Fix at the next edit; it now understates how easy
  the landing is.
- **R3-4 non-blocking, coordinator action — the lane superproject diverged from root HEAD.**
  `ef45bef` is on `b3a1660`; root is `0e3916c` and does not descend into the lane, so
  `prd collect` aborts at `lifecycle.ts:165` ("lane diverged from source HEAD"). The three intervening
  root commits touch only `prd.ctg`, `agent.ctg`, `cartridge.ctg`, `proxy.ctg`, `router.ctg` gitlinks —
  not the two memos — so rebasing `ef45bef` onto `0e3916c` is conflict-free. The gitlink bump then goes
  to `906b39a` (the live gitlink is already at the rebase base `4b13113`).
- **R3-5 non-blocking — unstated fixture invariant.** Note in the fixture (one comment) that the
  default build must keep `FACTOR` 2, because `a_native_module_reaches_the_base_through_the_global`
  asserts `twice(21) == 42` against the default artifact.
- **N1 (round 2) — done and re-verified**: block 1 opens with the `test -f` loop over both memos.
  **N2 (round 2) — superseded in part**: a lane does exist and its `cartridge.ctg` submodule worktree
  *is* populated, so pass 1 resolves `--manifest-path cartridge.ctg/Cargo.toml`; what bites instead is
  R3-4. **N3 (round 2) — regressed**, see R3-3.

Disposition: keep. The plan and its specs are sound at `906b39a` / `ef45bef`; proceed to landing after
R3-1's reword and R3-4's rebase.

Validation (independent reviewer; scratch worktree of `cartridge.ctg` at `906b39a` under the session
scratchpad, scratch root with `justfile` and every `.cartridge` entry symlinked except a writable copy
of `memos` carrying `ef45bef`'s two edited files, `cartridge.ctg` symlinked to the worktree;
`CARGO_TARGET_DIR` left to each block's own `$PWD/target/…-verify` default inside the scratch root,
so nothing reached the live target. `just --evaluate` → `root` = the scratch root. The live daemon,
the live checkout and the live memos were never written; live memo digests unchanged afterwards.)
Blocks were run as their literal commands, in block order, via `sh -eu -c "$(cat <block>)"` — the
engine's own invocation (`templates/spec.md:16-18`); unlike rounds 1 and 2 the local safety hook did
not refuse it this time.

| # | Command (cwd = scratch root unless noted) | Exit | Elapsed | Observed |
| --- | --- | ---: | ---: | --- |
| 1 | Verify block 1, literal (`test -f` memo loop; `grep -nE 'on its own when its module is rebuilt\|does the same on its own' …runtime.md …proxy.md`; `cargo nextest run --manifest-path cartridge.ctg/Cargo.toml --workspace -E 'test(=tests::host::a_rewritten_native_module_restarts_only_on_reload) \| test(=trust::tests::a_built_native_module_is_not_a_source_so_a_test_build_keeps_the_cartridge) \| test(=tests::host::a_native_module_reaches_the_base_through_the_global)'`), **cold** target | **0** | **26.1 s** | guards silent; compile 12.10 s; `3 tests run: 3 passed, 169 skipped` in 12.939 s (the reload test itself 12.938 s). Matches the implementer's 26 s; limit 120 s |
| 2 | Verify block 2, literal (`cargo build --manifest-path cartridge.ctg/Cargo.toml --bin cartridge`; `CARTRIDGE_HOME="$(mktemp -d)"`; `just test lifecycle`) | **0** | **43.5 s** | build 0.07 s; bun `11 pass / 0 fail`, 1397 expects, 42.53 s; `test lifecycle pass` |
| 3 | Verify block 3, literal (`cargo fmt … --all --check`; `cargo clippy … --workspace --all-targets -- -D warnings`) | **0** | **4.9 s** | both silent, clippy `Finished dev profile in 4.70s` |
| 4 | Non-vacuity (i): scratch copy of `906b39a` with leg (b) changed to `rebuild(&module)` (old build left on disk at reload; the now-unused binding renamed `_rebuilt` to satisfy `-D warnings`), own `CARGO_TARGET_DIR` | **non-zero** (nextest FAIL) | 14.6 s | `a_rewritten_native_module_restarts_only_on_reload` FAILS at `.cartridge/tests/unit/src/tests/host.rs:1388` — "reload did not pick up the rebuilt module", left `Some(Number(2))`, right `Some(Number(3))`. Exactly the implementer's claim: the assertion tracks the file's **content** at reload, not process identity |
| 5 | Non-vacuity (ii): scratch copy with `src/loader/{document.rs,mod.rs}` restored to `4b13113`, own `CARGO_TARGET_DIR`, block 1's three-test filter | **100** | 10.3 s | `3 tests run: 1 passed, 2 failed`. `a_rewritten_native_module_restarts_only_on_reload` FAIL at `host.rs:1368` — "a test build restarted the node", left `Some(Number(2))`, right `Some(Number(4))`; `a_built_native_module_is_not_a_source_so_a_test_build_keeps_the_cartridge` FAIL at `trust/tests.rs:284`, left 3 right 2, third source `…/x/target/debug/libx_y.dylib`; `a_native_module_reaches_the_base_through_the_global` still PASS. Reproduces the verifier's row 7 at the **combined** revision |
| 6 | `git diff a965d6e e4b1514 \| git patch-id --stable` vs `git diff 4b13113 484bbe7 \| git patch-id --stable` | 0 | — | identical id `e83dde6a9d8000ac775385d24d8aed9bbd730ad3`; textual diff-of-diffs shows only the `host.rs` index line and hunk offset — `484bbe7` is content-identical to the pre-rebase `e4b1514` |
| 7 | `git -C cartridge.ctg merge-base --is-ancestor 4b13113 906b39a` | 0 | — | the lane submodule head descends from live `main` |
| 8 | `git merge-base --is-ancestor HEAD ef45bef` in the live superproject | non-zero | — | lane does **not** contain root HEAD `0e3916c` (basis for R3-4); `git log --name-only b3a1660..0e3916c` → only `prd.ctg`, `agent.ctg`, `cartridge.ctg`, `proxy.ctg`, `router.ctg` gitlinks, no memo |
| 9 | block 1's `grep -nE` guard against the **live, unedited** memos | 0 (match) | — | `cartridge-proxy.md:14`, `cartridge-runtime.md:20` → the block would exit 1; the guard still discriminates |
| 10 | positive read of `ef45bef`'s memos | — | — | proxy.md:14-16 "does not restart anything by itself: a rebuilt module is picked up by the next `just proxy` (or `cartridge reload proxy`)…"; runtime.md:20-21 "(`cartridge reload <id>`, or `just proxy` for the proxy). A rebuilt native module is picked up on that deliberate reload, never by itself." The `--replace`-is-for-a-new-host-build sentence is kept |
| 11 | `git -C <wt> status --porcelain --untracked-files=all` and `ls fixtures/native/` after rows 1-3 | 0 | — | worktree clean; fixture dir holds only `build.rs Cargo.lock Cargo.toml src` — no `target/`, `Cargo.lock` unmodified: no write inside the footprint |
| 12 | `git -C /Users/feb/dev/cartridge status --porcelain .cartridge/memos/routine/cartridge-{proxy,runtime}.md`; `ps` for `cartridge-takeover` | 0 | — | live memos unchanged; no takeover leftovers |
| 13 | `grep -c rebuilt attempt.patch`; `head -5 attempt.patch` | 0 | — | 0 occurrences; pre-image blob `852d343` (the `a965d6e` `host.rs`), hunk `@@ -1259` — basis for R3-2 |
| 14 | `git -C /Users/feb/dev/cartridge/cartridge.ctg worktree remove <scratch>/wt` (no `--force`) | **0** | — | removed; `worktree list` shows no scratchpad/r3 entry; scratch target dirs deleted |

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: PASS (94/100, no blocking findings).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: apply R3-1's exact reword to PRD box 2 and tick the boxes per the table above; rebase the
lane superproject `ef45bef` onto root `0e3916c` and bump the gitlink to `906b39a` before `prd collect`
(R3-4). R3-2, R3-3 and R3-5 are cheap cleanups at the next edit.
