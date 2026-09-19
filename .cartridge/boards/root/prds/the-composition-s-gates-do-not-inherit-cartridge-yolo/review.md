# @root/the-composition-s-gates-do-not-inherit-cartridge-yolo review history

Plan: @root/the-composition-s-gates-do-not-inherit-cartridge-yolo
(`prd.ctg/.cartridge/boards/root/prds/the-composition-s-gates-do-not-inherit-cartridge-yolo/prd.md`).
Scope: leaf. The composed gates report the same verdict whether or not `CARTRIDGE_YOLO=1` is exported.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-19

Reviewer: coordinator-4b fresh agent, round 1.

Presented revision: superproject HEAD c84b3a4. `.cartridge/justfile`, the
development memo and the agent.ctg (620857d) and cartridge.ctg (324f36e) pins
are unchanged since the spec's base 80a6b09. The live `.cartridge/justfile` is
dirty with another session's `_fan` isolation hunk.

| Input | Content digest |
| --- | --- |
| Plan | prd.md 6694dac965fb0543050c87571c26c6dbac4042381b5bf7693589ad3821749964 |
| Specs | specs/spec01.md 7bc6f08f6b0eb27d99bfa968c1ab88b65bfc044ea8dfdb4694cf7a5833797b66 |
| Material contracts/dependencies | .state/loop/.../justfile.patch a2d97707…e6fef6d; analyst-1.md 9c567ee2…04a4; HEAD:.cartridge/justfile 5d8b1ec9…682c; HEAD:.cartridge/memos/routine/cartridge-development.md 0340f82d…c383; prd.ctg src/lifecycle.ts at a1c49f37 (seedSubmodules, runTestBlock) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The outcome is real. Reproduced: `CARTRIDGE_YOLO=1 just test agent` fails on HEAD with 12 passed and 1 failed (`multiple_tool_calls_execute_and_persist_in_response_order`), and the cartridge nextest filter fails. The diff is minimal: three lines plus one memo paragraph. -2: PRD box 1 says "any other recipe that spawns cargo or a nested `just`". Every memo-run recipe spawns a nested `just`. The spec narrows this to the cargo-spawning recipes and gives the reason (the operational recipes must keep passing yolo to a daemon), but it does not record the narrowing against box 1 in so many words. |
| Ownership and reuse | 18 | The root board owns `.cartridge/justfile`. The plan follows the `TAKEOVER_ENV` strip precedent, and rejecting global `unexport` is correct. No recipe that spawns cargo was missed. `audit`, `links`, `install`, `proxy` and the operational memos spawn no cargo; smoke, policy and memory go through `_one`. -1: `_fan`'s `unset` and `_one`'s `unset` are redundant for every gate path (measured below). -1: the memo says "the host trusts every file and skips policy". The host merges `yolo: true` (settings/mod.rs:15); the policy skip is agent.ctg's own `config.yolo` branch (agent.ctg/src/lib.rs:634). Suggested wording: "the host merges `yolo: true` into every cartridge that declares it, so files are trusted and the agent skips policy". |
| Dependencies and implementable slices | 15 | One spec, and the base sha is named. The landing risk from the foreign `_fan` hunk is acknowledged: the patch applies to the dirty live file (`patch --dry-run` exits 0, rerun by this reviewer), and the spec says to check `git status` before collect. -5: the plan misses a hard runtime dependency of the agent loop test. `base_binary()` (agent.ctg/.cartridge/tests/integration/loop.rs:52-63) needs `CARTRIDGE_BIN` or `../cartridge.ctg/target/release/cartridge`. A lane seeds cartridge.ctg as a fresh detached worktree (`seedSubmodules`, lifecycle.ts:34), which has no `target/`. The analyst's mini root symlinked the live siblings, so it hid this. |
| Observable acceptance and baseline evidence | 12 | Block 1 (probe) runs: exit 1 on HEAD ("a gate handed CARTRIDGE_YOLO to cargo-test: 1"), exit 0 patched, exit 1 with the `build` edit reverted ("…cargo-build: 1"). Block 4 runs in a lane-shaped tree: exit 1 on HEAD (nextest FAIL), exit 0 patched (PASS line, which the engine regex matches), 35 s from cold. Blocks 2 and 3 fail in the lane shape on the patched tree: all 13 loop tests panic "the base is not built". Pass 1 of collect would therefore fail. With `CARTRIDGE_BIN` set to the live release host, block 2 is exit 1 on HEAD and exit 0 patched, and block 3 is exit 0 on both (37–51 s). -5 for that blocker. -2: the probe cannot tell whether `_one` strips on its own. A variant with only `_fan`'s `unset` passes (exit 0), and so does one with only `_one`'s, so spec box 1's "`_one` can also be called on its own" is unproved. Add `CARTRIDGE_YOLO=1 PATH=… just --justfile .cartridge/justfile _one test agent` to the probe. -1: the memo gate is a name grep, with the diff reviewer as the declared backstop (acceptable). |
| Failure, recovery and compatibility | 17 | The operational recipes and `--yolo` stay unchanged, and the reasoning on the `lifecycle` target is sound: takeover.test.ts:17 sets `CARTRIDGE_YOLO: "1"` in its own child env. `env -u` works on macOS `env`. The probe's stand-in cargo fails `build`, so `links`/`install` never touch the live tree, and every cargo run uses `target/prd-yolo-verify`, which `/target/` ignores. The blocks set or unset the variable themselves, so they hold under a collector that carries `CARTRIDGE_YOLO=1`. -3: nothing gives a recovery path for the missing base binary. Pass 2 passes only because the live `cartridge.ctg/target/release/cartridge` happens to exist. |
| Reviewer total | 80 / 100 | |

Findings and concrete revisions:

1. BLOCKING. specs/spec01.md, the first two `test` blocks (`run:` lines for
   `test agent`). In the lane pass, every loop test panics at loop.rs:59
   ("the base is not built … ../cartridge.ctg/target/release/cartridge"),
   because a seeded lane submodule has no `target/`. Fix: prefix both `run:`
   lines with
   `CARTRIDGE_BIN="${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}"`.
   The spec template allows naming absolute tools with an env default. Also add
   a `sh` precondition,
   `test -x "${CARTRIDGE_BIN:-/Users/feb/dev/cartridge/cartridge.ctg/target/release/cartridge}"`,
   whose message names `just build runtime --release`/`cargo build --release`.
   Then correct the analyst's timing and pass claims, which were measured with
   symlinked live siblings.
2. Minor. Block 1 cannot prove the `_one`-standalone path. Add a direct
   `just … _one test agent` call under `CARTRIDGE_YOLO=1` with the stand-in
   cargo. Or drop one of the two `unset`s, and say which one is kept and why.
3. Minor. Memo wording: attribute the policy skip to the agent's `yolo` setting
   rather than to the host (see the ownership row).
4. Minor. State in the spec's Acceptance that PRD box 1's "nested `just`"
   clause is deliberately narrowed to the cargo-spawning recipes, and why.

Disposition: revise. The mechanism is correct; the Verify blocks are not runnable in the lane.

Validation (every command run as `env -u CARTRIDGE_YOLO …` or with the variable
set explicitly as shown). The tree was a throwaway `git worktree add --detach`
of superproject HEAD (c84b3a4). agent.ctg 620857d and cartridge.ctg 324f36e were
seeded as detached worktrees, the same shape `seedSubmodules` produces, with the
patched justfile copied in and the memo paragraph applied. cwd was the worktree
root. The worktrees were removed afterwards with `git worktree remove` (no
`--force`).

- Block 1 (HEAD justfile): exit 1, "a gate handed CARTRIDGE_YOLO to cargo-test: 1".
- Block 1 (patched, outer CARTRIDGE_YOLO=1): exit 0.
- Block 1 (patched without the `build` edit): exit 1, "…cargo-build: 1".
- Block 1 (patched with `_fan`'s unset only): exit 0.
- Block 1 (patched with `_one`'s unset only): exit 0.
- Block 2 run line (patched, no CARTRIDGE_BIN, cold): exit 1 after 47 s, 0 of 13 loop tests passed, "the base is not built".
- Block 2 (patched, CARTRIDGE_BIN=live release host): exit 0, 13 passed, 47 s.
- Block 2 (HEAD, CARTRIDGE_BIN=live release host): exit 1, `multiple_tool_calls… FAILED`, 37 s.
- Block 3 (patched): exit 0, 40 s. Block 3 (HEAD): exit 0, 51 s.
- Block 4 (patched): exit 0, nextest PASS, 35 s. Block 4 (HEAD): exit 1, nextest FAIL at tests.rs:76.
- `patch --dry-run -p1` on a copy of HEAD's justfile, and on the dirty live file: both apply.

Reviewer identity: coordinator-4b fresh agent, round 1.
User rating: not required under delegation.
User feedback/provenance: none.
Result: FAIL (80/100, one blocking finding).
Unresolved blocking findings: 1. Test blocks 2 and 3 fail in the lane pass without CARTRIDGE_BIN.
Rounds used / remaining: 1 / 4.
Next action: a bounded revision of spec01's Verify blocks (CARTRIDGE_BIN default plus a precondition), then round 2.

## Round 2 — 2026-09-19

Reviewer: coordinator-4b fresh agent, round 2.

Presented revision: spec01 revision 1 plus analyst-1.md "Revision 1". Measured
at superproject HEAD 5831e2a, not the spec's anchors (80a6b09, c84b3a4). At
5831e2a the `_fan` isolation hunk has landed in HEAD's `.cartridge/justfile`,
and cartridge.ctg is pinned at 445a87f, not 324f36e. agent.ctg is still pinned
at 620857d. The live footprint is clean (`git status --porcelain` is empty for
both files).

| Input | Content digest |
| --- | --- |
| Plan | prd.md 28d620bffe9486d3beb9882fe4812f9c038194f7966d1edc5ff1780fdd2f1c62 |
| Specs | specs/spec01.md fb73aa64abce5936bf9dd3c4566705df0d0978f0cefeb916f69cfd72b7a4a3f1 |
| Material contracts/dependencies | justfile.patch f82155b4…6f59938; memo.patch 11821e71…6bed86b4; analyst-1.md 8333622f…1f98; HEAD 5831e2a `.cartridge/justfile` (isolation hunk included); prd.ctg src/lifecycle.ts (seedSubmodules, runTestBlock, passedTests) |

Round 1 findings, rechecked:

1. BLOCKING (CARTRIDGE_BIN): fixed. In a lane-shaped tree with `CARTRIDGE_BIN`
   unset, both agent `test` blocks reach the release host and run 13 loop tests.
2. `_one` on its own is unproved: fixed. Mutant: move the `unset` from `_one`
   to `_fan`. Block 1 then exits 1 with "a gate handed CARTRIDGE_YOLO to
   cargo-test: unset 1", so the gate path is stripped and the direct `_one`
   call leaks.
3. Memo credits the wrong component: fixed. The wording now matches
   settings/mod.rs:15-16 and agent.ctg@620857d src/lib.rs:634.
4. Box-1 narrowing is unstated: fixed ("Scope of PRD box 1, narrowed on purpose").

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The outcome is real and reproduced again (see below). The narrowing is now explicit and argued with host.rs:157. -1: box 2's literal "`just test agent` exits 0" rests on a suite that is not deterministic under load (finding A). |
| Ownership and reuse | 19 | The root board owns both files, and the recipe choice is minimal and correct. Rejecting `unexport` is right. -1: the memo says the gates strip the variable "before they spawn anything". `_fan` spawns `tools` first, still carrying it (harmless, `command -v` only). Say "before they spawn cargo, a test runner or the host". |
| Dependencies and implementable slices | 17 | One spec, and the lane dependency on the release host is stated and guarded by block b0. -2: the anchors are stale. The spec names base 80a6b09/c84b3a4 and cartridge.ctg 324f36e, and says another row "lands that hunk first"; HEAD is now 5831e2a with the hunk landed and cartridge.ctg at 445a87f. The patch still applies at the new HEAD (`patch` applies with a +12 offset, and `git apply --check` exits 0), and block 4 passes at 445a87f. Re-anchor, and drop the dirty-file text. -1: the embedded justfile diff in the spec lacks the trailing blank context line that justfile.patch has (cosmetic, both apply). |
| Observable acceptance and baseline evidence | 14 | Discrimination holds (table below): the probe, the yolo agent block and the cartridge block are red on HEAD and green when patched. -5 BLOCKING (finding A): both agent blocks run the whole `just test agent` suite, which contains a load-sensitive flake. `streaming_cancel_mid_stream_releases_once_without_append` (loop.rs:1236, `left: "failed" right: "cancelled"`; a 120 ms sleep races a 300 ms frame) failed in 2 of 6 gate runs here: HEAD b3 and patched-yolo b3. Warm, on an idle machine, it failed 0 of 14 reruns. Collect needs four full-suite greens (2 blocks x 2 passes). -1: the memo gate is a name grep, with the diff reviewer as the declared backstop (acceptable). |
| Failure, recovery and compatibility | 17 | The operational recipes, `--yolo` and the lifecycle target are unaffected (takeover.test.ts:17 sets its own env). All cargo output went to `target/prd-yolo-verify` (checked: no seeded submodule got a `target/` from the blocks). The probe's stand-in cargo stops `build` before links/install. -3: nothing records or absorbs the flake, so a red collect would be misread as a patch defect, which is the very failure this PRD exists to remove. |
| Reviewer total | 86 / 100 | |

Findings and concrete revisions:

- A. BLOCKING. specs/spec01.md, the first two `test` blocks (the `run:` lines
  ending `test agent`).
  - The problem: they gate on a suite with an unrelated load-sensitive flake.
  - Fix: append `--test loop multiple_tool_calls_execute_and_persist_in_response_order`
    to both run lines. The args reach `cargo test -p agent` through
    `_fan`/`_one`/`_cargo`.
  - Measured on the scoped form in the lane tree, with `CARTRIDGE_YOLO=1`:
    patched exits 0 in 23 s with 1 passed; HEAD exits 1 with the test FAILED.
  - Record box 2's whole-suite agreement as a one-time measurement in the
    evidence, not as a gate.
  - File the flake on the agent board.
- B. Minor. Re-anchor the base to the current HEAD and pins, and remove "Another
  row lands that hunk first" and "applies ... to the dirty file".
- C. Minor. Memo wording: "before they spawn anything" is imprecise (see the
  ownership row).
- D. Minor. The spec's embedded justfile diff differs from justfile.patch by
  its trailing context line. Keep them identical.

Disposition: revise (Verify blocks only; mechanism and memo are sound).

Validation. Tree: `git worktree add --detach` of HEAD 5831e2a, every gitlinked
submodule seeded as a detached worktree at its pin, the way `seedSubmodules`
does it, with no `target/`. Blocks were extracted with prd.ctg's own
`verificationBlocks`/`testBlock`. `sh` blocks ran as `sh -eu -c`. `test` blocks
ran as runTestBlock does, and pass names were matched as `passedTests` does.
cwd was the tree root. `CARTRIDGE_BIN` and `CARGO_TARGET_DIR` were unset outside.

| Block | HEAD, CARTRIDGE_YOLO=1 exported | patched, exported | patched, `env -u CARTRIDGE_YOLO` |
|---|---|---|---|
| b0 host check | 0, 0 s | 0, 0 s | 0, 0 s |
| b1 probe | 1, 14 s, "...cargo-test: 1 1" | 0, 4 s | 0, 10 s |
| t yolo agent | 1, 61 s cold, loop.rs:798 FAILED | 0, 32 s, 13 passed | 0, 32 s |
| t unset agent | 1, 33 s, **flake** loop.rs:1236 | 1, 46 s, **flake** loop.rs:1236 | 0, 34 s |
| t yolo cartridge each_file | 1, 32 s cold, tests.rs:76 FAILED | 0, 4 s, nextest PASS | 0, 15 s |

- Mutant (strip in `_fan` instead of `_one`): b1 red, as above.
- The flake, warm, measured by running the test binary directly: 0 of 8 alone
  and 0 of 6 as the whole loop suite. The failures above therefore depend on
  machine load.
- Integrated pass: the isolation hunk is in HEAD, so every row above already
  runs on top of it. `check` now also calls `_one isolation composition`,
  which the `unset` in `_one` covers.
- Every block ran well under 120 s.
- Cleanup: patches reverse-applied, the submodule worktrees removed, then
  `git worktree remove` without `--force`.

Reviewer identity: coordinator-4b fresh agent, round 2.
User rating: not required under delegation.
User feedback/provenance: none.
Result: FAIL (86/100, one blocking finding).
Unresolved blocking findings: A. The agent test blocks gate on a flaky full suite.
Rounds used / remaining: 2 / 3.
Next action: scope the two agent run lines (finding A), re-anchor (B), apply the minors, then round 3.
