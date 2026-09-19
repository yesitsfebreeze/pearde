# @root/the-shared-record-describes-only-this-repository/the-record-s-routines-run-in-this-repository review history

Plan: @root/the-shared-record-describes-only-this-repository/the-record-s-routines-run-in-this-repository (prd.md, specs/spec01.md).
Scope: leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: none (split 2026-09-19 with none used).

# @root/the-shared-record-describes-only-this-repository/the-record-s-routines-run-in-this-repository review history

Plan: @root/the-shared-record-describes-only-this-repository/the-record-s-routines-run-in-this-repository (`prd.ctg/.cartridge/boards/root/prds/the-shared-record-describes-only-this-repository/the-record-s-routines-run-in-this-repository/prd.md`, `specs/spec01.md`).
Scope: one observable outcome (no root routine names the foreign layout; no memo links a deleted routine); leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none (split from the parent 2026-09-19 with no rounds used).

## Round 1 — 2026-09-19

Presented revision: superproject `801aa8e`, prd.ctg `4fb90e79` plus dirty planning files below. All seven footprint files are clean at base.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `cc0815adeb54364b…` |
| Specs | `specs/spec01.md` sha256 `af7d3ed7d168c213…` (byte-identical to `.state/loop/.../spec01.md`) |
| Material contracts/dependencies | analyst-1.md `49716fbc48c5abc0…`; routines at base: quality `c7bb802f…`, hygiene `7cc46059…`, legible `fe5288f4…`, improve `4d082a3a…`, self-improve `1cfcf51e…`, new-routine `bc114594…`, distill `d7a5e827…`; `memo.ctg/src/usage.rs` (`lookup_from`/`choose`), `memo.ctg/src/record.rs` (`root`, `workspace`), `memo.ctg/src/service.rs` (`native`), `cartridge.ctg/src/loader/mod.rs` (`root`), `prd.ctg/src/lifecycle.ts` (`verificationBlocks`, `verify`) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | I checked each verdict against the routine bodies. quality (probes over `src/`, `cargo machete`, `tests/one_dispatch.rs`, `just lane`), hygiene (`memos/intake`, `.kern/data`, `kern compact/audit/doctor`), legible (`find src -name '*.rs'`, `head -3 src/*/src/lib.rs`, `just lane legible-<probe>`/`just land`), improve (`memos/intake`, `kern query`, `git -C memos commit`, `just prd scan`), self-improve (`memos/SYSTEM.md`, `.agents/skills`, `mcp__kern__query`, `git -C memos`). All five are foreign throughout, so deleting them is right and there are no stubs. new-routine's job still exists here and it has four live inbound links, so rewriting it is right. The distill edits are accurate: `distill_due` is at `memo.ctg/src/record.rs:426` and `build_system` is at `harness.ctg/src/lib.rs:349`. −2: the landing-pad decision follow-up has no home PRD. None of the parent's siblings (vision, links) covers it. |
| Ownership and reuse | 18 | Uses the memo tool's managed write and the existing `distill` link-repair discipline, and adds no new mechanism. The footprint is the seven files and all are clean. The vision sibling `needs` this PRD and owns `system/vision.md:144`, so that follow-up is homed. −2: `prd.md` `## Analysis` is still the parent's text. It says "Rewrite or delete improve/legible/self-improve", "Remove the `just lane` bullet from new-routine", and points to the parent's analyst file. It also pastes a weaker two-leaf Verify. That record contradicts spec01, which deletes all five routines and rewrites the whole new-routine body. |
| Dependencies and implementable slices | 18 | One spec, one small slice, no cross-owner edits, and no footprint overlap with the siblings (`every-link-…` is `.cartridge/tests/…`, `decision/*`, `note`; vision is `system/vision.md`). The memo write path is correct once the caller is fixed: `service.rs::native` takes `cwd` from the payload, and `record.rs::root` picks the nearest `.cartridge/` above it, which is the lane's own. So a payload `cwd` set to the lane writes into the lane. `.cartridge/memos/.lock` is gitignored at HEAD, so the lane gets no untracked file. −2 for the blocking step-2 caller defect (F1). |
| Observable acceptance and baseline evidence | 16 | Verify is extracted from spec01 only (`lifecycle.ts::verify` reads spec blocks, so prd.md's pasted block is inert). I ran it with `env -i PATH=/usr/bin:/bin sh -eu -c` from the repo root. It exits 1 at base (`not deleted: …/quality.md`) and leaves `git status` unchanged. In a scratch after-state of all 17 records (five deleted, new-routine rewritten, distill edited) it exits 0. Mutants all turn it red: `kern` appended to distill → 1; `[[improve]]` in web.ctg's memo → 1; `[[hygiene]]` in a root decision → 1. It calls no memo tool or daemon, uses no inert `!`/`&&` guards, and uses relative paths only. −4: (F2) the `checked -lt 10` floor does not do what the spec and analyst claim. `web.ctg` is a plain tracked directory with `.cartridge/memos`, so an unseeded lane still counts 5×2=10. My mutant that deleted every submodule record exited **0**. The repo pass still has all records, so the gate as a whole is not vacuous, but the stated guarantee is false. Also (F4) prd.md Acceptance has two checks while spec01 has four. |
| Failure, recovery and compatibility | 14 | Link resolution checks out. `usage.rs::lookup_from` sends a bare leaf to `choose`, which prefers the linking memo's own cartridge, and memory.ctg ships its own `quality`/`hygiene`/`legible`. So memory's ~25 links keep resolving to memory's copies. No other record links `improve`/`self-improve`, and `[[new-routine]]`/`[[distill]]` survive. Recovery is git, which fits the no-retention rule. −6: (F1) step 2/3 as written would run the memo tool from inside the lane (blocking). (F3) The kept frontmatter description advertises a step the new body forbids. (F5) The body cites `type/type.md`, which the root record does not hold. |
| Reviewer total | 84 / 100 | |

Findings and concrete revisions:

- **F1 — blocking. The memo calls run from the lane, which is a separate project.** Spec01 says "Steps (in the lane, cwd = lane root)" and passes `--arg cwd "$PWD"`, so `cartridge run memo` runs with process cwd = lane. The lane checks out the tracked `.cartridge/init.lua` (`git ls-files` confirms it). `cartridge.ctg/src/loader/mod.rs::root()` (and `trust/mod.rs:75`) picks the nearest ancestor holding `.cartridge/init.lua`, so the CLI treats the lane as its own project. The result is no daemon, a second host, or a trust check against the lane's config. The coordinator's note (a parallel reviewer's finding) matches the code. Fix: run both calls in steps 2 and 3 from the live repo root with `cwd` set to the absolute lane path. For example, set `lane=<abs lane path>` and run from `/Users/feb/dev/cartridge`: `cartridge run memo "$(jq -n --arg cwd "$lane" … )"`. The payload `cwd` then routes the write into the lane (`record.rs::root` stops at the lane's `.cartridge/`). Say this in the step, not only in the heading. The same trap applies to anyone following the new `new-routine` body from a lane: add one line there too.
- **F2 — non-blocking. The anti-vacuity floor is miscounted.** `web.ctg/.cartridge/memos` is tracked in the superproject (`git ls-files web.ctg` lists it; there is no gitmodules entry), so `checked` reaches 10 with no submodule seeded. My reproduction: the scratch after-state with every submodule record removed gives exit 0. Fix: require the records the sweep exists for. Either add `for rec in memory.ctg prd.ctg; do if [ ! -d "$rec/.cartridge/memos" ]; then echo "unseeded: $rec"; exit 1; fi; done`, or raise the floor to the real record count (currently 1 + 16 = 17 per leaf). Correct the analyst and spec claim that an unseeded lane fails.
- **F3 — non-blocking. new-routine's description goes stale.** The spec keeps the frontmatter `description` ("… register the handle, prove the gate"), but the new body says no skill file or slash command is written. Fix: rewrite the description to match the Inputs/Do/Check/Failure body, for example "Write a new routine: name the job, gather every ingredient by name, save it through a managed memo write, prove it resolves."
- **F4 — non-blocking. prd.md is out of sync with the spec.** Replace the parent's pasted `## Analysis` with a short pointer to `.state/loop/the-record-s-routines-run-in-this-repository/analyst-1.md` and `specs/spec01.md`: delete five, rewrite new-routine, edit distill. Drop the pasted weaker Verify and bring Acceptance to the spec's 3–4 checks. This edits body sections in place and leaves the frontmatter alone.
- **F5 — non-blocking. The new body cites an unresolvable path.** The root record has no `type/type.md`; 12 cartridges ship one (`memo.ctg`, `memory.ctg`, …). Name `[[@memo/type/type.md]]` (or the path the tool actually resolves), or drop it. distill.md step 1 already has the same citation, so fix both while the file is open.
- **F6 — non-blocking. The superseded landing-pad decision has no home.** `decision/the-trunk-checkout-is-a-landing-pad.md` has no PRD. Add one (`prd add`) under the parent, or record it in the parent's body, so the parent's outcome ("describes only this repository") is not closed with it open.

Disposition: revise (F1 and F2 are single-step spec edits, F3–F6 are record edits). Keep the per-routine verdicts and footprint as they are.

Validation (cwd `/Users/feb/dev/cartridge` unless noted; scratch `/private/tmp/claude-501/-Users-feb-dev-cartridge/a3492fbd-f726-4514-b5ee-796fd5ea14c1/scratchpad/routines-r1/`):
- spec01 Verify extracted to `verify.sh`, run as `env -i PATH=/usr/bin:/bin sh -eu -c "$(cat verify.sh)"` at base: exit 1; `git status --short` identical before and after.
- `sim/` (copies of `.cartridge/memos` and all 16 `*/.cartridge/memos`, simulated after-state): exit 0. Mutants `m1` (foreign token in distill): 1. `m2` (`[[improve]]` in web.ctg): 1. `m3` (`[[hygiene]]` in a root decision): 1. `m4` (all submodule records removed, web.ctg kept): **0**, which is F2.
- `rg --hidden` over every `*.md` for links to the seven leaves, excluding `.lanes`, `.state`, `boards/`: root links only from footprint files. memory.ctg links only to leaves it ships itself, plus `[[new-routine]]`. prd.ctg links only to `[[new-routine]]`. No `@`-qualified links to these leaves.
- Code read: `memo.ctg/src/usage.rs:80-150`, `record.rs:480-513`, `service.rs:452-470`, `cartridge.ctg/src/loader/mod.rs:97-101`, `prd.ctg/src/lifecycle.ts:52-120`. No memo tool, daemon, proxy or reload was invoked.

Reviewer identity: fresh reviewer agent, coordinator-5c-5.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL.
Unresolved blocking findings: F1.
Rounds used / remaining: 1 / 4.
Next action: bounded revision of spec01 steps 2–3 (F1) and the Verify floor (F2), then the record edits F3–F6. Re-review at round 2.

VERDICT: FAIL

## Round 2 — 2026-09-19

Presented revision: superproject `801aa8e`, prd.ctg `5a45336b` plus the dirty planning files below (revision-1). All seven footprint files are still clean at base. new-routine is `bc114594…` and distill is `d7a5e827…`, both unchanged since round 1. `git status --short .cartridge/memos/routine` lists only the untracked `rank-cartridges.md`, which is outside the footprint.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` sha256 `094737fb9bf20a42…` |
| Specs | `specs/spec01.md` sha256 `c20e370bdf72e314…` |
| Material contracts/dependencies | `prd.ctg/src/lifecycle.ts` (`lane`, `verify`), `prd.ctg/src/records.ts:295` (`local`), `memo.ctg/src/record.rs:506` (`root`: canonicalizes `cwd`, fails on a missing path), `record.rs:312` (resolve fields), `service.rs:140` (resolve schema); pins: memory.ctg `3432b133`, prd.ctg `2bfe1e94`, memo.ctg `dcbeb59b`, harness.ctg `91206ee5` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 20 | The verdicts are unchanged and still correct. F6 now has a home: `prds/the-landing-pad-decision-describes-this-repository-s-lanes-not-a-checkout-that-no-longer-exists/prd.md` exists on the root board. The prd.md body is 222 words, one outcome and five checks. |
| Ownership and reuse | 19 | prd.md `## Analysis` is now a short pointer, and the parent's pasted text and weaker Verify are gone (F4 fixed). Acceptance mirrors the spec's five boxes. The plan still uses only the memo tool's managed write and git, with no new mechanism. −1: spec Follow-ups still says the coordinator "is adding" a landing-pad PRD, but that PRD now exists. Cite its ref. |
| Dependencies and implementable slices | 18 | F1 is fixed. The Steps heading, the bold warning and both step-2 and step-3 commands now run from `/Users/feb/dev/cartridge` with `cwd` = `$lane`. Every cited target exists at the pinned shas the lane will seed: `@prd/routine/plan-cartridge-work.md`, `spec-a-prd.md` and `run-board.md` at prd.ctg `2bfe1e94`, and `type/type.md` at memo.ctg `dcbeb59b`. `distill_due` is at memo.ctg `record.rs:426` and `build_system` at harness.ctg `lib.rs:349`, both at the pins. `type/routine.md` and `usage/run-usage.md` are tracked in the root record. The resolve payload (`usage:"run"`, `query`) matches `service.rs:140`, and `run-usage.md` has `name: run`. −2 (F7): the lane path is written as `.lanes/<slug>`. `lane()` takes `prd.local` (`the-shared-record-describes-only-this-repository/the-record-s-routines-run-in-this-repository`) and replaces `/` with `-`, so the real directory is `.lanes/the-shared-record-describes-only-this-repository-the-record-s-routines-run-in-this-repository`. The obvious guess, the leaf slug, is wrong. A wrong path fails safely: `record.rs::root` canonicalizes and errors, it does not walk up into prd.ctg's record. But the step as written is not copy-runnable. |
| Observable acceptance and baseline evidence | 17 | I extracted the Verify mechanically from spec01 and ran it from the repo root as `env -i PATH=/usr/bin:/bin sh -eu verify.sh`. It exits **1** (`not deleted: .cartridge/memos/routine/quality.md`), and the `git status --short` output of the superproject and prd.ctg is identical before and after. I checked for inert guards: every check is `if …; then …; exit 1; fi` with no `!` or `&&`/`\|\|` guards, no environment variables, no `cd` and no writes. F2 holds in both passes. The lane-like after-state (root and web.ctg from `git archive HEAD`, each submodule's record from its pinned sha, 17 records) gives exit 0. The repo-like after-state (live records) gives exit 0. The mutants go red: `[[improve]]` in memory → 1; `[[self-improve\|y]]` in root → 1; `[[routine/legible.md]]` in prd → 1; memory.ctg removed from the lane → 1 (`unseeded record`); root+memory+prd only (15 < 17) → 1. So the gate cannot pass vacuously on an unseeded lane. −3 (F8): the spec says the memory/prd guard exists because "those two records hold every out-of-footprint link". That is true only in the repo pass. memory.ctg's record is gitignored in memory.ctg (`.cartridge/.gitignore:17 /memos/*`): its pinned tree has only `type/note.md` and `type/type.md`, so in the lane the guard is met by two type memos, and memory's `[[quality]]`/`[[hygiene]]`/`[[legible]]` links and its own copies exist only in the live repo pass. The gate is still sound, because the repo pass runs over the real records, but the stated reason for the guard is wrong for pass 1. −0: an `@`-qualified `[[@root/routine/improve.md]]` is not matched (mutant m6 exit 0). No such link exists and it is not a supported form here, so there is no deduction. |
| Failure, recovery and compatibility | 18 | F3 is fixed: the new description is gated by `register the handle\|prove the gate`. F5 is fixed: both files cite `[[@memo/type/type.md]]`, gated by `(^\|[^/])type/type\.md`. The new-routine body is concrete and runnable here. It names exact `just` recipes from `.cartridge/justfile`, uses PRD lanes (`prd add/claim/collect`) instead of `just lane`, has a copyable `op:"resolve"` payload, and warns about running from inside a lane. Recovery is git, and no stubs are left. A wrong or empty `$lane` fails loudly (`memo cwd must be absolute` / canonicalize error) and never writes to the live record. −2: step 3's filter says memory's `@memory/routine/...` entries are "expected", but from the lane memory's record holds no routines. The live check is the one that would show them. Word it as "any `routine/<deleted>.md` entry from the root record is a failure" so the implementer is not left eyeballing which matches are allowed (same fix area as F8). |
| Reviewer total | 92 / 100 | |

Round-1 findings:

- F1 (blocking): **fixed.** Every `cartridge run memo` in steps 2–3 and in the new-routine body runs from the live root with the absolute lane as payload `cwd`. The lane path is a placeholder (F7 below).
- F2: **fixed.** There is an explicit memory.ctg/prd.ctg seeding guard with a floor of 17. It holds in both passes and turns red on an unseeded lane (reproduced).
- F3: **fixed.** The description is rewritten and gated.
- F4: **fixed.** The Analysis pointer is in place, the pasted Verify is gone, and Acceptance has five boxes. The frontmatter is untouched (`state`/`claim` intact).
- F5: **fixed.** `[[@memo/type/type.md]]` is in both files and gated.
- F6: **fixed.** The landing-pad PRD exists on the root board.

New findings (all non-blocking):

- **F7 — non-blocking. Spell out the lane path.** Replace `.lanes/<slug>` with `.lanes/the-shared-record-describes-only-this-repository-the-record-s-routines-run-in-this-repository`, or say "the directory `prd claim` prints (`lane()` joins `prd.local` with `-`)". Also add `test -d "$lane/.cartridge/memos/routine"` before the first write.
- **F8 — non-blocking. Correct why the seeding guard exists.** State that memory.ctg's record is gitignored apart from `type/`. In the lane pass the guard only proves the submodule was seeded; the out-of-footprint link check is the repo pass over the live records. Fix step 3's "expected entries" wording in the same edit.
- **F9 — non-blocking. Refresh the follow-up.** Cite the landing-pad PRD by its ref instead of "is adding a separate PRD".

Validation (cwd `/Users/feb/dev/cartridge`; scratch `/private/tmp/claude-501/-Users-feb-dev-cartridge/a3492fbd-f726-4514-b5ee-796fd5ea14c1/scratchpad/routines-r2/`):
- `base.sh`: awk-extracts the spec01 Verify to `verify.sh` (29 lines) and runs `env -i PATH=/usr/bin:/bin sh -eu verify.sh`. Result: exit 1, and `before.txt`/`after.txt` are identical (superproject and prd.ctg status).
- `sim.sh`: lane-like after-state gives 0 and repo-like gives 0. Mutants: m1 1, m2 1, m3 1, m4 1, m5 1. m6 (`@root/` qualified) gives 0, which is out of scope. m7 (double-space `just  land`) gives 0, which is trivial prose evasion and does not count.
- Code read: `lifecycle.ts:22-26,105-120`, `records.ts:295`, `record.rs:497-520`, `record.rs:312`, `service.rs:127-140`. I checked git objects at every pin with `cat-file -e`/`ls-tree`. No memo tool, daemon, proxy or reload was invoked. No repo, prd.md, spec or review.md edits were made.

Reviewer identity: fresh reviewer agent, coordinator-5c-5.
User rating: not required under delegation; none supplied.
Result: PASS (92/100, no blocking findings). F7–F9 can be folded in by the implementer or a body-only touch-up. They do not change the footprint or the Verify.
Rounds used / remaining: 2 / 3.

VERDICT: PASS
