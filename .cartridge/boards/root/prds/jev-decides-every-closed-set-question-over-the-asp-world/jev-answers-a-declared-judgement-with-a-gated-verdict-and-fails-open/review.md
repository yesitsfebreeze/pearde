# jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open review history

Plan: `@root/jev-decides-every-closed-set-question-over-the-asp-world/jev-answers-a-declared-judgement-with-a-gated-verdict-and-fails-open`.
Scope: one leaf. `jev.ctg` answers `decide` with a gated verdict and fails open.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

## Round 1 — 2026-09-19

Presented revision: superproject `ea8ecdb`, jev.ctg seed `790fb65`. The plan changed mid-review (the director moved jev.ctg to a submodule): briefed prd.md sha256 `afe28c8c…ba43a0`, re-read `d2c0cbcab61c9dde4ac4bb61c81243a85716bc77af5ad034d66abb3d8b5c6426`; spec `7fd7e7edb16ac883da501e6450ffd262b3d73b38794a4d41e721b3dd9cb6dea3`. Source read at cartridge.ctg `445a87f`, memo.ctg `4f8903d`, superproject `34c7e43`.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Clear outcome; the parallel-build choice recorded. −2: 925 words. −1: six boxes. |
| Ownership and reuse | 17 | Own cartridge, crosses only by needs and events, never needs `asp`. −1: stale "same collect" bullet. −1: siblings still targeted the superproject. −1: no remote for the gitlink. |
| Dependencies and implementable slices | 14 | −4, blocking B1: an optional need to an undeclared event fails jev at load (`plan.rs:324-333`, `host/mod.rs:390-399`). −2: the spec keeps the tracked-directory layout (B4). |
| Observable acceptance and baseline evidence | 15 | JUnit, correct guard forms, a `cmp`-checked mutant. −2, blocking B3: `just audit jev` and `just isolation` cannot run from the jev lane. −1: the timeout test needs an asynchronous fake node (N1). −1: the `jev.decided` check should read the manifest (N3). −1: the mutant is by hand (N4). |
| Failure, recovery and compatibility | 14 | 8000 < 10000 and jev never waits on auth's 15000/20000. −3, blocking B2: a null or partial auth answer can return `caution` or `act`. −1: the 3000 ms default is unmeasured (N6). −2: by-hand defects (N5). |
| Reviewer total | 77 / 100 | FAIL |

The `auth.jev` contract agrees between the two specs on every point listed; jev's `events.jev` schema should type `state` as auth does.
Blocking: B1 optional need to an undeclared event; B2 forced escalate for a null or partial answer; B3 audit and isolation move to the coordinator's post-collect step; B4 migrate paths and blocks to the submodule layout.
Non-blocking: N1 asynchronous fake node; N2 `apply` requires `timeout_ms`; N3 read declared properties from the manifest; N4 mutant as a Verify block; N5 trust `jev.ctg` only, no `cartridge help`, point `@jev/example-needs-an-llm`; N6 provisional 3000 ms; N7 noul measure without `Math.max(`; N8 announce the profile line (jev shows Failed until `auth.jev` is declared, trust `jev.ctg` only, do not push before the remote exists); N9 the isolation key check is inert for every manifest.
Validation: `just prompt` exit 0; digests as above; `git show` reads at the cited shas exit 0; a worktree probe showed `git worktree remove` without `--force` exits 0 with an ignored `node_modules/` present. Nothing ran against the daemon.
Reviewer identity: independent reviewer subagent of cartridge-b0 (Claude Code session 0738bf3b-f548-466b-b8f2-7a2de6f31033), round 1.
User rating: not required under delegation; none was supplied.
Result: FAIL (77/100).
Unresolved blocking findings: B1, B2, B3, B4.
Rounds used / remaining: 1 / 4.
Coordinator response: the PRD was rewritten to 372 words and five boxes with B1 and B2 in its Direction and Decision; siblings 2 and 3 now target `jev.ctg`; the spec revision goes to the analyst.

## Round 2 — 2026-09-19

Presented revision: superproject `ea8ecdb`, jev.ctg seed `790fb65`. Plan sha256 `7e5931f608ec0daa6aa35a98552c6ff6c498156c147c101e7a06c52a76cf3384` (372 words, 5 boxes); spec sha256 `d5413f3f181aab9fd392d6511d9ee1b4d1c0a28a261ff1d0c4a96b936559a8d4` (analyst revision 3). Source read at cartridge.ctg `d04ab33`, memo.ctg `4f8903d`.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | 372 words, five boxes, history moved out. −1: box 1 bundles four checks. |
| Ownership and reuse | 19 | Own repository, nothing reaches a sibling, needs `auth.jev?` and `memo?`. −1: no remote, so the gitlink bump must not be pushed before it exists. |
| Dependencies and implementable slices | 19 | Load order correct; post-collect waits for both collects. −1: post-collect step 4 assumed no TypeSafe entry. |
| Observable acceptance and baseline evidence | 18 | 14 named tests via JUnit, correct guards, the mutant as a block that fails safe. −1: step 6 ran `bun install` unfrozen. −1: `{answers: []}` passes the object check. |
| Failure, recovery and compatibility | 16 | Every fail-open path escalates; 8000 < 10000 and jev never waits on auth. −4: R1, post-collect trusted `jev.ctg` alone, but a changed `init.lua` fails every `cartridge` command until the project is trusted (`cartridge.ctg` `src/cli/project.rs:23-28`, `src/trust/mod.rs:120-155`). |
| Reviewer total | 91 / 100 | PASS |

B1-B4 and N1-N7 are resolved in the text. R1 was required before post-collect step 1, not blocking implementation. Non-blocking: step 4 accepts either outcome; drop step 6 or freeze it; add `!Array.isArray` to the `answers` check. The coordinator applied all four before `specced`: post-collect now lists foreign uncommitted manifests and Lua files, announces a window, edits `init.lua` and trusts the project back to back, accepts either step-5 outcome, and drops the unfrozen install; the shape check refuses an array.
Validation: digests match; `git show d04ab33:<path>` reads confirmed `unmatched`, `Failed`, the profile trust check and the record walk; `git grep` in memo.ctg `4f8903d` confirmed `@owner/` paths. No daemon, `prd` or trust command ran. No scratch left.
Reviewer identity: independent reviewer subagent of cartridge-b0 (Claude Code session 0738bf3b-f548-466b-b8f2-7a2de6f31033), round 2.
User rating: not required under delegation; none was supplied.
Result: PASS (91/100).
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 5.
