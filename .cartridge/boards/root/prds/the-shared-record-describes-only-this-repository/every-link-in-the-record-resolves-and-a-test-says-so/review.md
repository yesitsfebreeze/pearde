# @root/the-shared-record-describes-only-this-repository/every-link-in-the-record-resolves-and-a-test-says-so review history

Plan: @root/the-shared-record-describes-only-this-repository/every-link-in-the-record-resolves-and-a-test-says-so (prd.md, specs/spec01.md).
Scope: leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: none (split 2026-09-19 with none used).

## Round 1 — 2026-09-19

Presented revision: superproject 801aa8e (dirty; footprint test file and decision memos clean, `.cartridge/memos/note` holds 2 untracked foreign memos), prd.ctg 4fb90e79 with prd.md dirty and specs/ untracked. Reviewed spec01 includes the coordinator's amended step 1 (memo tool with `cwd` set to the lane).

| Input | Content digest |
| --- | --- |
| Plan | `prds/the-shared-record-describes-only-this-repository/every-link-in-the-record-resolves-and-a-test-says-so/prd.md` a9a4b39019c6e51736a7b5aa39763707dee6ee4506cd209ecc5f1438e96cf250 |
| Specs | `specs/spec01.md` 4288938c995ec378fed6a2ac257324b9b729ed6e3d0af13d6e697fba455c8304 |
| Material contracts/dependencies | `.cartridge/tests/integration/source-layout.test.ts` 7977e6ad…5848; prd.ctg `src/lifecycle.ts` (verify/collect), `src/records.ts` `specs()`; memo.ctg `src/service.rs` `native()`/`call()`, `src/record.rs` `Input`/`root()`; cartridge.ctg `src/cli/project.rs` `locate`, `src/loader/mod.rs` `root()`, `src/cli/host.rs` `run`/`attach`; prd.ctg pinned sha 2bfe1e94 |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | One observable outcome, one owner (the superproject's record and its layout test), and a real defect: 23 dead links, confirmed by an independent scan. -3: prd.md is 488 words (over the 400-word split line) because it still pastes the analyst's draft, which contradicts spec01 (see F4). |
| Ownership and reuse | 14 | It reuses the clean `source-layout.test.ts`, its `source/fs/os/path` imports and the existing `just test layout` target, and it leaves the dirty justfile alone. The memo-tool route satisfies `system/memos.md` ("write only through the tool") in principle. I verified that the native `memo` service honours `cwd`: `native()` removes `cwd` and calls `record::execute(&cwd, …)`, and `root()` resolves to `<cwd>/.cartridge/memos` because the lane has a tracked `.cartridge`. A live probe `cartridge run memo '{"op":"read","cwd":"/Users/feb/dev/cartridge",…}'` from the repo root returned `text` plus `revision`. -6: step 1 says to run the command from the lane with `cwd=$PWD`. `cartridge` picks its project from the process cwd (`loader::root()` walks up to the nearest `.cartridge/init.lua`, which is tracked, so it exists in the lane). The lane therefore becomes its own project, with no daemon, a HEAD-version `config.lua` subject to `trust::verify`, and `attach` trying to reach or start a second host. See F2. |
| Dependencies and implementable slices | 13 | The lane seeding holds: no lane exists yet, so the claim-time seeding applies, and all 40 live sibling links exist in prd.ctg at the pinned sha 2bfe1e94 (checked with `git cat-file -e`). `bed3eaaa` really deletes `boards/ui/prds/{copy-mode-interacts-with-the-text,the-gutter-is-the-boundary}`. -7: the footprint reserves the whole directory `.cartridge/memos/note`, which is shared and actively written. Two untracked foreign memos landed there at 14:30, after the analysis. That breaks collect (F1) and holds a claim over roughly 140 unrelated memos. |
| Observable acceptance and baseline evidence | 17 | Census right: my scan of `.cartridge/memos/**/*.md`, fences skipped and scheme/anchor links ignored, finds exactly 23 dead links (3 decision, 20 `ui-design-*`, not 19) and 40 live ones. Baseline fails. `bun test ./…source-layout.test.ts -t 'link'` exits 1 with "regex \"link\" matched 0 tests" (skipping 1). The sh block's `grep -n 'boards/ui/'` hits all 3 decision memos. The missing-`./` note is right: without it bun reports "filters did not match any test files". `-t 'link'` excludes the snapshot test ("recorded memory source and SDK build…"), so the block runs in well under 120 s. The planted test asserts the exact list `['note/memo.md:2: ./missing.md']`, so a no-op checker (`[]`) and a fence-ignoring one (2 entries) both fail. Test names match the JUnit `<testcase name>` exactly. The guards are set-e safe (`if grep …; then exit 1; fi`, bare `grep -q`). -3: the stale prd.md Verify draft (F4). Step 1 cites `expected_revision`, but the command omits it (F5). |
| Failure, recovery and compatibility | 13 | Blocks write only to tmpdir and `$PRD_TEST_REPORT`, never inside the footprint, and use relative paths with no cargo. -7: F1 makes collect abort after the fast-forward, so the code lands with no receipt. The spec's claim that "every footprint path is clean (`git status --porcelain` is empty)" is false today. Pass 2 walks live untracked memos outside the footprint: the risk is acknowledged but not mitigated (F3). |
| Reviewer total | 74 / 100 | |

Findings and concrete revisions:

- **F1 (blocking): the directory footprint turns a foreign untracked memo into a collect abort.** Evidence: `git status --porcelain -- .cartridge/memos/note` shows `?? note/asp-is-the-fabric-with-a-better-protocol.md` and `?? note/user-correction-api-keys-go-through-auth.md` (mtime 14:30, another session). After the `git merge --ff-only`, collect runs `git ls-files --others --exclude-standard -- <footprint>` in the live repo and throws "source footprint changed during integrated verification" (`lifecycle.ts:242`). By then the code has already landed and no receipt is written. `completionProblem` would also keep reporting "verified source footprint changed after collection" (`:162`). Fix: replace `.cartridge/memos/note` in both the prd.md frontmatter and the spec01 footprint with the 20 explicit `note/ui-design-<style>.md` paths. Frontmatter is the coordinator's to edit, not a body-only worker's. Drop the "every footprint path is clean" sentence, or state it per file.
- **F2 (blocking): the memo-tool command must run from the live root, not the lane.** Evidence: `project::locate` calls `loader::root()`, which walks up from the process cwd to the first `.cartridge/init.lua`. The lane has one, so `cartridge run memo` from the lane targets a lane-rooted project with no daemon. `host::run` → `attach` then either errors ("unanswered") or starts a second host there, and `trust::verify` runs against the lane's HEAD `config.lua`, while the live file is dirty. That is the "one host per project" hazard. The native service does honour an explicit `cwd`, which I verified in the source and with a live read. Fix: run `cartridge run memo "$(jq -n --arg cwd <absolute lane path> …)"` from the live repo root (`/Users/feb/dev/cartridge`) with `cwd` set to the absolute lane path. Check that each result's `path` or revision comes from the lane, for example by confirming with `git -C <lane> status` that the edits appear there and not in the live tree. The coordinator's decision itself is acceptable: validated writes into the lane, with collect carrying them to the live record, meet "write only through the tool" and avoid live dirt in the footprint. Only the invocation site is wrong. `.cartridge/memos/.lock`, which the tool creates, is gitignored, so it does not block lane removal.
- **F3 (non-blocking): pass 2 checks memos outside this PRD.** Pass 2 walks every live `.md`, including the untracked `ranking/`, `routine/rank-cartridges.md`, `system/*`, `type/ranking.md` and the 2 new `note/` memos. Pass 1 walks only tracked files. None has a dead link today (my scan covers the live tree). Fix, pick one: (a) have `deadLinks` walk `git ls-files -z -- .cartridge/memos` output, so both passes judge the same tracked record; or (b) keep it and record in the spec that a pass-2 failure naming an untracked path is out of scope and is fixed by a separate PRD, not by editing this footprint. Option (a) is the stronger one.
- **F4 (non-blocking): prd.md still pastes the stale analyst draft.** The Analysis says 19 notes (actual: 20), "the whole dir is clean", and "frontmatter byte-identical"-era hand edits. Its fenced `test` block uses `-t 'record'` without `./`, which would select the heavy snapshot test and hit bun's filter-not-path error. It sits under `## Analysis` and is not executed (only spec `## Verify` sections run), but it contradicts spec01 and pushes the leaf to 488 words. Fix: cut the Analysis to about 5 lines and point to spec01 and analyst-1.md. Align Acceptance box 3 with spec01's wording (names the slug, cites `bed3eaaa`).
- **F5 (non-blocking): step 1 mentions `expected_revision` but its command omits it.** Fix: add `--arg rev <revision from the read>` and `expected_revision:$rev` to the jq template, so a concurrent edit is refused rather than overwritten.

Disposition: revise (keep the scope; the fixes are footprint, invocation site and record hygiene).
Validation (cwd `/Users/feb/dev/cartridge` unless noted):
- `bun test ./.cartridge/tests/integration/source-layout.test.ts -t 'link'` → exit 1, "regex \"link\" matched 0 tests".
- The same command without `./` → bun "filters did not match" note.
- An independent link scan with bun over `.cartridge/memos` → DEAD 23, LIVE 40.
- `git cat-file -e 2bfe1e94:<path>` for all 40 live targets in prd.ctg → none missing.
- `git show --name-status bed3eaaa` → the `boards/ui/prds/*` deletions.
- `cartridge run memo '{"op":"read","cwd":"/Users/feb/dev/cartridge","path":"note/ui-design-bauhaus.md"}'` → exit 0 with `text` and `revision`.
- `git status --porcelain -- .cartridge/memos/note` → 2 untracked files.
- Source reads as listed under material inputs.
- No files edited, nothing committed, no transitions.

Reviewer identity: fresh reviewer agent, coordinator-5c-6.
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: F1, F2.
Rounds used / remaining: 1 / 4.
Next action: the coordinator narrows the footprint (F1) and fixes the step 1 invocation site (F2), optionally F3–F5, then requests round 2.

VERDICT: FAIL

## Round 2 — 2026-09-19

Presented revision: superproject 801aa8e (dirty outside the footprint; all 24 footprint paths tracked and clean), prd.ctg 4fb90e79 with prd.md modified (footprint + body only; `state`/`claim`/`commit` match `.state/fields/…/every-link-in-the-record-resolves-and-a-test-says-so.json`) and specs/ untracked. Author's change log: revision-1.md, every claim rechecked below.

| Input | Content digest |
| --- | --- |
| Plan | `prds/the-shared-record-describes-only-this-repository/every-link-in-the-record-resolves-and-a-test-says-so/prd.md` cfdabb9fe95530086c2450462173841e11c566c597d631ea79d4001e973aadd9 |
| Specs | `specs/spec01.md` ca6138ddb5c0a40cd12e76c325cee3695436e377c89c58b55fd49ae849e7ba7d |
| Material contracts/dependencies | `.cartridge/tests/integration/source-layout.test.ts` 7977e6ad…5848 (unchanged since round 1); prd.ctg `src/lifecycle.ts` `lane()` :22, `seedSubmodules` :34, `testBlock`/`verify` :68–111, collect :182–250; `src/records.ts` `CONTROLLED` :83; memo.ctg `src/record.rs` `root()` :490, `journal()` :819; superproject HEAD `.gitignore` (`/.cartridge/memos/.lock`, `/.cartridge/resolver/`); prd.ctg pinned 2bfe1e94 |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One observable outcome, one owner, a real defect (23 dead links, re-measured). prd.md body is 168 words with no stale draft (F4 fixed). The Outcome is scoped to tracked memos. -1: the new test becomes a standing `just test layout` gate over 40 links into prd.ctg's root board. Any later PRD rename or retirement there turns the gate red, and the plan does not say who owns that (see N1). |
| Ownership and reuse | 18 | It reuses `source-layout.test.ts`'s `source`/`fs`/`os`/`path` and the existing `layout` target, and the justfile is untouched. F2 fixed: step 1 runs from `/Users/feb/dev/cartridge` with `cwd` = the absolute lane path. That path matches `lane()`: `path.join(prd.board,'.lanes', local.replace(/[^A-Za-z0-9._-]+/g,'-'))` with board `prd.ctg/.cartridge/boards/root` gives `…/.lanes/the-shared-record-describes-only-this-repository-every-link-in-the-record-resolves-and-a-test-says-so`, which is exactly what the spec says. `record::root()` walks up from the lane to its real, tracked `.cartridge` and returns the lane's `memos`. F5 fixed: `expected_revision:$rev` is in the template. -2: the lane does not exist yet (claim is in `analyzing`), so the lane-`cwd` write path has been verified in source but has never run. The `--rawfile body <draft>` location is unspecified, and a draft placed in the lane would be an untracked lane file (N2). |
| Dependencies and implementable slices | 18 | F1 fixed. The footprint lists the 20 `note/ui-design-*.md` files individually, and the prd.md and spec01 lists are identical (diffed: 24 = 24). All 24 paths pass `git ls-files --error-unmatch`, and `git status --porcelain -- <each>` is empty. The two untracked foreign `note/` memos are no longer in scope. Lane seeding: every submodule link target is in prd.ctg (43 = 40 live + 3 dead), and `seedSubmodules` seeds prd.ctg at its pinned sha 2bfe1e94. My HEAD-plus-pinned-sha simulation of pass 1 finds the same 23 dead links and 40 live ones. -2: pass 2 resolves those 40 targets in the live prd.ctg working tree (HEAD 4fb90e79, not the pin), which other coordinators edit (N1). |
| Observable acceptance and baseline evidence | 18 | The `git ls-files` walk is correct in both passes. `source = path.resolve(import.meta.dir,'../../..')` is the lane root in pass 1 and the repo root in pass 2. In the lane, git finds the worktree's own `.git` file first, even though the lane sits inside prd.ctg's working tree. In both passes `git ls-files -- .cartridge/memos` lists only superproject-tracked blobs: 387 regular 100644 files, no gitlinks, and no submodule files, because `.cartridge/memos` is not inside a submodule. Submodule content enters only as link targets resolved on disk, never as walked files. The lane is cut from HEAD, and pass 2 runs after `merge --ff-only`, so both passes see 387 files and the >100 floor holds in both. The Verify fails at base: `bun test ./…source-layout.test.ts -t 'link' --reporter=junit …` exits 1 with "regex \"link\" matched 0 tests", and the sh block's `if grep -n boards/ui/ …; then exit 1; fi` exits 1. It cannot pass vacuously: the `pass:` lines force both tests to run, the floor rules out an empty walk, and the planted test's exact-list assertion catches a no-op or fence-blind checker. Prototype rerun: the real checker fails the record test with the 23 links and passes the planted test. `NOOP=1` passes the record test but fails the planted test. `NOFENCE=1` fails both. The guards are set-e safe, the paths are relative and there is no cargo. -2: the spec specifies the fixture as `fs.mkdtempSync(os.tmpdir())` (N3). That creates a sibling of `$TMPDIR`, not a directory inside it, unlike the existing test and the prototype. |
| Failure, recovery and compatibility | 17 | The collect abort from round 1 is gone (explicit file footprint). `.cartridge/memos/.lock` and `.cartridge/resolver/` are ignored in HEAD's `.gitignore`, so the tool's side files do not block `git worktree remove`. The post-write check (`git -C "$LANE" status --porcelain` = exactly 23 memos; live footprint status empty) catches stray lane files and live-tree writes. -3: there is no recovery note for a pass-2-only failure, where a prd.ctg link target moves between the lane pass and the repo pass. The code has then already fast-forwarded and no receipt is written (N1). |
| Reviewer total | 90 / 100 | |

Round 1 blockers:

- **F1: resolved.** Explicit 20-file list in both frontmatters. Per-path status is empty, and every path is tracked.
- **F2: resolved.** The command runs from the live root with `cwd` = the absolute lane path, and the path agrees with `lane()` in lifecycle.ts. F3, F4 and F5 are also resolved as the change log claims. I found no false claim in revision-1.md.

Findings and concrete revisions (all non-blocking):

- **N1 (non-blocking): pass 2 and the standing gate depend on the live prd.ctg board layout.** Evidence: 40 live links go from the record into `prd.ctg/.cartridge/boards/root/prds/…`. Pass 1 resolves them at pin 2bfe1e94, and pass 2 and every later `just test layout` resolve them in the live prd.ctg tree (4fb90e79, dirty). If a PRD is moved between the two passes, collect throws after `merge --ff-only`. Fix: add a Verify note. A pass-2 failure that names only a `prd.ctg/…` target means the board moved underneath the run. Recovery is a follow-up link fix in its own PRD, followed by `prd collect` again, which reports done via `completionProblem`, or an inspection of HEAD. Also state that the standing gate intentionally holds the record to the live board.
- **N2 (non-blocking): say where the `--rawfile` drafts live.** Put them in a scratch directory outside the lane, never in it. The post-write status check would catch a stray draft, but only after the fact.
- **N3 (non-blocking): the fixture path in the spec is wrong.** Replace `fs.mkdtempSync(os.tmpdir())` with `fs.mkdtempSync(path.join(os.tmpdir(), 'record-links-'))`, as the prototype and the existing test do. The current text creates `$TMPDIR`'s parent-level sibling `T<random>`, which a sandboxed run may not be allowed to write.

Disposition: keep; proceed to implementation. Folding N1–N3 in is optional and would not reopen review, because none of them changes the design or the Verify.
Validation (cwd `/Users/feb/dev/cartridge` unless noted):
- `bun test ./.cartridge/tests/integration/source-layout.test.ts -t 'link' --reporter=junit --reporter-outfile=<scratch>/r.xml` → exit 1, "regex \"link\" matched 0 tests. Searched 1 file (skipping 1 test)".
- The sh block's decision-memo loop under `sh -eu -c` → exit 1 (the `boards/ui/` hits).
- `git ls-files -z -- .cartridge/memos` → 387 entries, all mode 100644, no gitlinks.
- Diff of the prd.md and spec01 footprint lists → identical, 24 paths. `git ls-files --error-unmatch` plus `git status --porcelain --` on each → tracked, empty.
- Simulation (`scratchpad/review2/sim.ts`) over the tracked list: walked content = `git show HEAD:<memo>`, targets checked with `git cat-file -e` at HEAD or the pinned submodule sha (pass 1), and on disk (pass 2). Both give 23 dead and 40 live. All submodule targets are in prd.ctg.
- `scratchpad/links-analyst/proto2.test.ts`: real, `NOOP=1` and `NOFENCE=1` runs, outcomes as above.
- Source reads: `lane()`, `seedSubmodules`, the collect path and `testBlock`/`verify` in lifecycle.ts; `CONTROLLED` in records.ts (footprint is not controlled; recorded fields match the frontmatter); `root()`/`journal()` in memo.ctg record.rs; `git show HEAD:.gitignore`.
- No files edited except this round file. Nothing committed, no transitions.

Reviewer identity: fresh reviewer agent, coordinator-5c-6.
User rating: not supplied (delegated).
User feedback/provenance: none for this revision.
Result: PASS.
Unresolved blocking findings: none.
Rounds used / remaining: 2 / 3.
Next action: the coordinator appends this round to review.md, optionally folds in N1–N3, and proceeds to claim and implement.

VERDICT: PASS
