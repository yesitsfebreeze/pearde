# the-agent-calls-it-cites-its-sources-and-policy-can-refuse-it review history

Plan: `@root/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/the-agent-calls-it-cites-its-sources-and-policy-can-refuse-it`
(`prds/the-voice-can-look-something-up-on-the-internet-when-the-answer-is-not-in-the-repository/the-agent-calls-it-cites-its-sources-and-policy-can-refuse-it/prd.md`).
Scope: leaf — the composition uses `web`: tool on the agent's list, a system memo telling the model when to reach for it and to cite the URL, and a per-operation policy rule that refuses it.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-19

Presented revision: superproject HEAD `7446db2` (spec written against `4104d36`; no footprint path changed in between), prd.ctg `87de727f`, planning files uncommitted.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` e25eebd93748b96237593d73cae043d55dd9ba14e28de49dcc50ffe8d3c6200d |
| Specs | `specs/spec01.md` 626d3d08c0864c5c9c6c6fac6d33129d36cf2afe3b8911ab1aa9bd78759766d0 |
| Material contracts/dependencies | `web.ctg/.cartridge/.gitignore` 14142f36…3d; `policy.ctg/init.lua` 460b77a2…d9; `agent.ctg/src/lib.rs` aec999da…40; `prd.ctg/src/lifecycle.ts` (verify/collect) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome, no code change, two files. The reworded box 3 keeps the outcome: the original named `config.lua` as where the *test* rule goes, not a standing rule. The live composition has `default="allow"` and no web rule, so "can refuse" is a capability, and a fixture composing the real `policy.ctg` + `web.ctg` proves it. −2: PRD box 1 requires "`just prompt` includes that line", but the spec's box 1 drops that clause without saying so. |
| Ownership and reuse | 17 | Reuses the `smoke.test.ts` symlink-fixture pattern. The test lives in the composition's tests (correct per isolation memo). −3: the footprint leaves out `web.ctg/.cartridge/.gitignore`, which the memo cannot land without (B1). |
| Dependencies and implementable slices | 16 | Both sibling needs are collected, and the exact memo and test content are given. I measured that the memo tool accepts the reference body verbatim and writes it to `web.ctg/.cartridge/memos/system/…` (identical bytes, `saved:true`). −4: the landing path is broken (B1, B2). |
| Observable acceptance and baseline evidence | 12 | Base check is correct (block 1 exits 1). −8: block 2 exits 1 in every lane (B2). In pass 2 it passes when the core proof is skipped (B3). The test's `reported` assertion is built by the test itself (N1). The analyst's "lane 1 pass 1 skip, exit 0" claim only holds with a binary supplied from outside the lane. |
| Failure, recovery and compatibility | 15 | The foreign `config.lua`/`justfile` dirt is handled correctly, and the dropped `git diff --quiet` guard is well reasoned. Using a loopback server with async `Bun.spawn` is correct. −5: an ignored memo is never committed, so pass 2 fails block 1 after the fast-forward. |
| Reviewer total | 78 / 100 | |

Findings and concrete revisions:

- **B1 (blocking): the memo is gitignored and will never be collected.** `web.ctg/.cartridge/.gitignore` is a whitelist (`/*`, `!/.gitignore`, `!/docs/`, `!/help.md`, `!/tests/`). `git check-ignore -v web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md` → `web.ctg/.cartridge/.gitignore:5:/*`. Collect stages from `git status --porcelain --untracked-files=all -- <footprint>` (`lifecycle.ts:145`), which omits ignored files. The lane commit therefore leaves the memo out, and pass 2 then fails block 1's first `test -f`. Revision: add `web.ctg/.cartridge/.gitignore` to the spec footprint with `!/memos/` and `/memos/.lock` (the same form as `docs.ctg/.cartridge/.gitignore`). Add a block-1 line such as `! git check-ignore -q web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md`.
- **B2 (blocking): block 2 fails in every lane.** `cartridge.ctg` is a submodule and is empty in the lane, so `${CARGO_TARGET_DIR:-$PWD/cartridge.ctg/target}/debug/cartridge` is missing. The collector sets no `CARGO_TARGET_DIR` (`runProcess` inherits the env). Measured on a fresh detached worktree with the reference applied, under `env -i`: block 2 exit 1, "Build the runtime first". Revision (probed): derive the main checkout from `git rev-parse --path-format=absolute --git-common-dir`, `export CARTRIDGE_BIN="${CARTRIDGE_BIN:-$main/cartridge.ctg/target/debug/cartridge}"`, and have the test read `process.env.CARTRIDGE_BIN` first. Lane result: exit 0, 1 pass, 1 skip.
- **B3 (blocking): the gate does not guarantee that pass 2 runs the core proof.** `total=pass+skip=2, pass>=1` also accepts a skip in the live checkout. Measured on a main-checkout clone with an empty `policy.ctg`: the original block 2 exits 0 while box 3 is unproven. Revision (probed): as the last line, `if test "$(git rev-parse --path-format=absolute --git-dir)" = "$(git rev-parse --path-format=absolute --git-common-dir)"; then test "$skip" -eq 0; fi`. On the main-checkout clone: policy absent → exit 1, policy present → exit 0 (2 pass, 11 expects). In a lane worktree the guard does not fire (exit 0, 1 skip). With this line, skipping in the lane is honest, because pass 2 is then guaranteed to run the proof.
- **N1: the `reported` assertion is a tautology.** `const reported = value.decision === "allow" ? undefined : {content:"permission denied",error:true}` is constructed by the test itself and says nothing about `agent.ctg`/`mcp.ctg`. Delete it. Name `agent.ctg/src/lib.rs:658` / `mcp.ctg/src/service.rs` `refusal()` as a diff-reading backstop (the step-4 ceiling), not as a test assertion.
- **N2: "carrying the reason" overstates the agent path.** `agent.ctg` returns `{"content":"permission denied","error":true}` with no reason. Only the policy decision (`"Policy denies web.fetch"`) and mcp's refusal carry one. Reword PRD box 3 / spec box 3 to match.
- **N3: `just prompt` inclusion is true but not recorded.** Measured: in a scratch worktree (memo.ctg source + built dylib, scratch `CARTRIDGE_HOME`), `cartridge run memo {"op":"system",cwd}` composed `- When the answer is not on this disk, use the web tool … name the source URL in the answer you give. Body: @web/system/reach-the-web-and-name-the-source.md`. Put this in the spec's measured table and restore the clause in spec box 1. Don't add it as a Verify block: `cartridge run` starts a daemon in the checkout.
- **N4: "written through the memo tool" is only prose.** Name the exact call: `cartridge run memo '{"op":"write","cwd":"<abs>/web.ctg","path":"system/reach-the-web-and-name-the-source.md","body":…}'`. Note that it needs `web.ctg/.cartridge/` to exist (it does). A Verify block cannot tell a tool write from a hand write; accept that as a ceiling.
- **N5: box 4 ceiling is honest.** Whether a model turn cites the URL is non-deterministic. The spec checks the memo instruction and relies on the fact that `url` is always present on search results and fetched pages (sibling specs). Accepted as recorded; no further gate round.
- **N6: block 1 has a weak check.** `grep 'tool.web -> web' || grep 'tool\\.web'` is loose. Pinning the regex literal from the test is enough.

Disposition: revise (B1–B3 and N1–N4 in one coherent revision, then round 2).
Validation (all `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`, blocks extracted from `## Verify and Proof`):
- base, detached worktree (lane shape): block 1 exit 1, block 2 exit 1.
- reference applied, lane shape: block 1 exit 0, block 2 **exit 1** (binary missing). With `CARGO_TARGET_DIR` supplied from outside: exit 0, 1 pass, 1 skip.
- reference applied, pass-2 shape (policy.ctg content and binary present): block 1 exit 0, block 2 exit 0, 2 pass, 11 expects, 3.4 s.
- original block 2 in a main-checkout clone with `policy.ctg` empty: exit 0 (silent skip, B3).
- revised block 2 (B2+B3): lane exit 0 (1 pass 1 skip); main-checkout clone with policy absent exit 1; main-checkout clone with policy present exit 0 (2 pass).
- memo tool write and `system` op in a scratch worktree: verbatim write succeeded, and the composed prompt contains the line. The scratch host was stopped with `cartridge stop`. `git check-ignore` confirms B1. All scratch worktrees and clones were removed and pruned. Nothing was written in the live checkout except this file.

Reviewer identity: reviewer-cites-1 (independent review sub-agent, Opus 5).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL (78/100, blocking findings).
Unresolved blocking findings: B1, B2, B3.
Rounds used / remaining: 1 / 4.
Next action: the analyst revises spec01 (footprint + gitignore, binary lookup, pass-2 no-skip guard, drop the tautology, record the prompt measurement), rewords box 3's "carrying the reason", then round 2.

## Round 2 — 2026-09-19

Presented revision: superproject HEAD `7446db2`, prd.ctg `87de727f`, planning files uncommitted (revised `prd.md` body and `specs/spec01.md`; analyst report `.state/loop/…/analyst-cites-2.md`).

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` 06b6e2f3202ad5edd37228b8c629f8a616c83dbc66ea304f2937882a5e8b7107 |
| Specs | `specs/spec01.md` 3a7123848109b5d0536a1a8427c1f202c2041e661c30e8c9173ef947affd63cc |
| Material contracts/dependencies | `prd.ctg/src/lifecycle.ts` 177200f0…4b11 (collect/verify); `prd.ctg/src/planner.ts` fd60f4c7…fcfe (`feet()`); `web.ctg/.cartridge/.gitignore` 14142f36…403d (base) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Still one outcome and three files. Box 1's `just prompt` clause is restored, and box 3 is reworded precisely (N2). −1: N3's prompt measurement is cited from round 1, not re-run against the revised memo bytes. The description line is unchanged, so this is cosmetic. |
| Ownership and reuse | 18 | The `.gitignore` edit is byte-identical to `docs.ctg/.cartridge/.gitignore` (`diff` empty). It reuses the template's `CARTRIDGE_BIN` naming and the symlink-fixture pattern. −2: the PRD's own footprint still reserves `.cartridge/config.lua`, a file this plan no longer touches and that foreign work already holds (B4). |
| Dependencies and implementable slices | 16 | Exact content is given for all three files, and the memo-tool call is named (N4). −4: the collect path is still broken, now by the frontmatter footprint (B4) and no longer by the spec. |
| Observable acceptance and baseline evidence | 19 | Every block result was reproduced (below). B1–B3 are all closed by measured gates. N1's tautology is gone, and N6 is pinned to the literal. −1: box 4 stays at the recorded ceiling (N5, accepted). |
| Failure, recovery and compatibility | 13 | The lane and pass-2 gates are correct. −7: the spec's landing note says "this spec's footprint does not touch" `config.lua`, but collect unions the PRD's `footprint` with the spec's (`planner.ts:7` `feet()`). With the live `config.lua` dirty, collect fails as described in B4. |
| Reviewer total | 85 / 100 | |

Findings and concrete revisions:

- **B1 resolved.** The `.gitignore` reference equals `docs.ctg`'s byte for byte. In a lane with the reference applied, `git status --porcelain=v1 --untracked-files=all` lists `?? web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md`, so collect now stages it. Mutation test: with the `.gitignore` edit reverted, block 1 exits 1.
- **B2 resolved.** In the lane, `--git-common-dir` gives `/Users/feb/dev/cartridge/.git`, so `CARTRIDGE_BIN` resolves to the live binary with no env and no `cd`. Block 2 exits 0 (1 pass, 1 skip).
- **B3 resolved.** In a standalone clone (git-dir == common-dir, the same shape as live `/Users/feb/dev/cartridge`, where both print `/Users/feb/dev/cartridge/.git`), block 2 exits 1 with policy absent (1 pass, 1 skip) and exits 0 with policy present (2 pass, 10 expects, 3.41 s).
- **N1, N2, N4, N6 resolved. N3 recorded (cited). N5 ceiling accepted.**
- **B4 (blocking, new): the PRD frontmatter `footprint` still names `.cartridge/config.lua`** (and also `web.ctg/.cartridge/memos` and `.cartridge/tests/integration`). `feet(prd)` = PRD `footprint` ∪ spec `footprint` (`planner.ts:7`). Both collect's staging scope (`lifecycle.ts:145`) and the post-integration check (`lifecycle.ts:174`, `git diff --name-only candidate -- …verifiedPaths` in `repo`) use it. Live `.cartridge/config.lua` is dirty (`git diff --stat`: 14 lines, not ours). The consequences:
  - With a lane, pass 2 runs after `merge --ff-only`, and then line 174 throws "source footprint changed during integrated verification". HEAD has already advanced, and no receipt is written.
  - With no lane (`tree === code`), the foreign `config.lua` edit is staged and committed into "Implement …".
  - `clash()` also reserves `config.lua` against other held PRDs.

  Revision: through the prd writing path (not a hand edit of the frontmatter), set the PRD `footprint` to the spec's three paths or remove it, so that `.cartridge/config.lua` and `.cartridge/justfile` leave `feet()`. Correct the spec's landing note so it says the PRD footprint was changed too. The analyst report states that the frontmatter was left untouched, which is how this survived.

Disposition: revise (B4 only; the spec itself is ready).
Validation: every block was extracted with `verificationBlocks` semantics (2 blocks) and run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`, under `scratchpad/reviewer-cites-2/`.
- Lane shape (detached superproject worktree with empty submodules):
  - base: block 1 exit 1, block 2 exit 1.
  - reference: block 1 exit 0, block 2 exit 0 (1 pass, 1 skip).
  - mutant without the `.gitignore` edit: block 1 exit 1.
- Pass-2 shape (standalone `git clone`, git-dir == common-dir, binary symlinked in):
  - base: block 1 exit 1, block 2 exit 1.
  - reference with policy absent: block 1 exit 0, block 2 **exit 1** (the guard works).
  - reference with policy present: block 1 exit 0, block 2 exit 0 (2 pass, 0 fail, 10 expects).
- The collect path was read, not run. No `prd` transition was performed.
- Cleanup: the worktree and clone were removed, then `git worktree prune`. The mutation step's `git stash` push/pop was net zero. The live checkout's `git status` is unchanged. Nothing was written except this file.

Reviewer identity: reviewer-cites-2 (independent review sub-agent, Opus 5).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL (85/100, blocking finding B4).
Unresolved blocking findings: B4.
Rounds used / remaining: 2 / 3.
Next action: remove `.cartridge/config.lua` (and redundant entries) from the PRD `footprint` through prd's validated writing path, and correct the landing note. Then round 3, which should be a quick check because the spec's gates already pass.

## Round 3 — 2026-09-19

Presented revision: superproject HEAD `7446db2`, prd.ctg `87de727f`, planning files uncommitted. The PRD frontmatter `footprint` has been narrowed and a "Footprint narrowed" section added. The spec's landing note is corrected. The spec's content and Verify blocks are otherwise unchanged from round 2.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` 2541c36fff5b62b154bf282a36f48895ec188b47ec1485c3bb3d451e0c617a8b |
| Specs | `specs/spec01.md` 308911459c00f467a1bac4ee6e45bc6319f4283ce7bba4808edb480357779a57 |
| Material contracts/dependencies | `prd.ctg/src/planner.ts` fd60f4c7…fcfe (`feet()`, `clash()`); `prd.ctg/src/lifecycle.ts` 177200f0…4b11 (collect); `docs.ctg/.cartridge/.gitignore` (model for the `.gitignore` edit) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Unchanged: one outcome, three files, and the box wording is precise. −1: the `just prompt` measurement is still cited from round 1 rather than re-run (cosmetic, because the description is unchanged). |
| Ownership and reuse | 19 | The PRD footprint now reserves only paths this plan writes. The `.gitignore` reference is still byte-identical to `docs.ctg`'s (`diff` empty). −1: the PRD entry `web.ctg/.cartridge/memos` is a directory and so broader than the spec's single file. That is harmless, because the memo tool writes there and `.lock` is ignored. |
| Dependencies and implementable slices | 19 | B4 is closed (see below). Both needs are `done`. −1: the spec header still reads "Round 2, revising round 1", and the PRD's older "Landing warning" paragraph is not marked as resolved (N7). |
| Observable acceptance and baseline evidence | 19 | Reproduced this round: base fails and reference passes, in the lane shape and in the policy-present shape. −1: the box 4 ceiling remains (N5, accepted). |
| Failure, recovery and compatibility | 18 | `feet()` no longer contains `.cartridge/config.lua` or `.cartridge/justfile`. No foreign dirt lies inside the footprint, and running the Verify blocks writes nothing inside it (checked with `--ignored`). The post-integration check at `lifecycle.ts:174` therefore has nothing to trip on. −2: the pass-2 main-checkout shape was not re-run this round. It was measured in round 2, and the blocks have not changed. |
| Reviewer total | 94 / 100 | |

Findings and concrete revisions:

- **B4 resolved.** The PRD frontmatter `footprint` is now `web.ctg/.cartridge/.gitignore`, `web.ctg/.cartridge/memos` and `.cartridge/tests/integration/web-tool-policy.test.ts`. `feet()` (`planner.ts:5-8`) is the de-duplicated union of these with the spec's three paths. Each spec path equals a PRD path or lies under one, so neither `.cartridge/config.lua` nor `.cartridge/justfile` is in `feet()` any longer. The union claim in the PRD and the landing note matches the code. `git status --porcelain` on those paths in the live checkout is empty, so there is no foreign dirt, and the live dirt (`config.lua`, `justfile`, submodule pointers, `MANIFEST.md`, `ideas.md`) is all outside the footprint. In the worktree with the reference applied, `git status --porcelain=v1 --untracked-files=all` lists exactly ` M web.ctg/.cartridge/.gitignore`, `?? .cartridge/tests/integration/web-tool-policy.test.ts` and `?? web.ctg/.cartridge/memos/system/reach-the-web-and-name-the-source.md`, all inside `feet()`, with nothing else dirty. `clash()`: the other boards whose footprints mention `.cartridge/tests` are either `open` (not held) or target a different `repo` (`cartridge.ctg`).
- **No regressions.** The spec's Files section, reference content and Verify blocks are unchanged in substance from round 2. Only the landing note changed.
- **N7 (non-blocking):** the spec header still says "Round 2", and the PRD's "Landing warning" paragraph could point at the "Footprint narrowed" section. Both are cosmetic.

Disposition: keep. Proceed to implementation.
Validation: the reference was extracted from `spec01.md`'s fenced blocks (the `.gitignore`, the memo and the test) and applied in a detached superproject worktree at `scratchpad/reviewer-cites-3/`. Each Verify block was run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c "<block>"`, with cwd = the worktree root.
- Base: block 1 exit 1, block 2 exit 1.
- Reference, lane shape (policy.ctg empty): block 1 exit 0, block 2 exit 0 (1 pass, 1 skip, 0 fail). The B3 guard does not fire in a linked worktree.
- Reference, policy.ctg content present (rsync of the live source without `.git`): block 2 exit 0 (2 pass, 0 fail, 10 expect() calls). Afterwards, `git status --ignored` under `web.ctg` and `.cartridge/tests` shows no new files.
- The collect path was read, not run. No `prd` transition was performed. The worktree was reverted, removed and pruned. The live checkout's `git status` is unchanged. Nothing was written except this file.

Reviewer identity: reviewer-cites-3 (independent review sub-agent, Opus 5).
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: PASS (94/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: proceed to implementation (write the memo through the memo tool, as specified). N7 can be fixed in passing.
