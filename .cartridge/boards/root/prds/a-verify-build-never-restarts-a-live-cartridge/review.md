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
