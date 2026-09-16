# @gitfs/gitfs-is-back-in-the-composition review history

Plan: `@gitfs/gitfs-is-back-in-the-composition`,
`prd.ctg/.cartridge/boards/gitfs/prds/gitfs-is-back-in-the-composition/prd.md`.
Scope: one observable outcome — the composition is clean after the user retired
`gitfs.ctg`. Executable leaf, no children.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none. `analyst-1.md`/`spec01.md` in `.state/loop/` are a
superseded draft for the superproject retirement work and were not reviewed.

Use the shared [review method](../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-16

Presented revision: superproject HEAD `65a18101385425053c827b4b0976e59075568440`
(`Advance planning: … live-attaches-to-the-daemon-instead-of-spawning-its-own collected`).
PRD state `analyzing`, claim `coordinator-cartridge-1b-3`, `repo:
"/Users/feb/dev/cartridge"`, `footprint: [".gitmodules", ".cartridge/init.lua"]`.
Dirty at review time (all outside this footprint): `.cartridge/memos/**` (14
modified), plus untracked `CLAUDE.md`, `PROMPT*.md`, `.obsidian/`, `.yolo-test/`,
`.cartridge/*.log`, `.cartridge/memos/system/isolation.md`.
`git status --porcelain -- .gitmodules .cartridge/init.lua` → empty, exit 0.

| Input | Content digest (SHA-256) |
| --- | --- |
| Plan | `prds/gitfs-is-back-in-the-composition/prd.md` — `7d60020a8df8db3392c0a72aff83479be598f08bfe3e0f4fd61ce3388dd6d44c` |
| Specs | `specs/spec01.md` — `40636d286656ae1cc8b9b5c82ce4d55d0e5cce6bd87346cd3c4179b810139797` |
| Verify block 1 (as the engine extracts it) | `69a53c3883a73dfaab6829e6b79471dc5a3a76d692c76731d89274ee938133c8` |
| Verify block 2 | `b57f8d5d45b571d90cfdbbf64d928248c17ff9f7b181f6b72b5524a5e77ff5f6` |
| Verify block 3 | `bc848256d752bb5d49319c7bf52a329e873aaa157c27747c4237b75d49c8327b` |
| Engine contract | `prd.ctg/src/lifecycle.ts` — `177200f02a8cb1c2257c0482f52cafb5ef5e7f160f28ed4835691c4ba9274b11` |
| Engine contract | `prd.ctg/src/planner.ts` — `fd60f4c7603e212279d47bf1bc37a30e7f2b28d2865b9cc3cbb175317807fcfe` |
| Host contract | `cartridge.ctg/src/cli/manual.rs` — `f5de0acfa5fa3e475000497c25bfabb0e4b8f7089b0f375f7034c22c2d5251b0` |
| Host contract | `cartridge.ctg/src/host/plan.rs` — `7bc8813ccd05cd93e19f4a09c155c56432a82bfa4cddda28c23f961940c7de21` |
| Asserted state | `.gitmodules` — `e3a822d1ed9dbfa3dbd231b8fa1a9af637fb52a070529a67143b8af6ded09842` |
| Asserted state | `.cartridge/init.lua` — `04f905784ea628a4a1bb56cd25f4ba25bd1b9bba6ab67fa587001179a5a28b0d` |
| Asserted state | `fs.ctg/cartridge.json` — `1d7e1a4aa6fd63fe751a6f4285be492a661205ca2587480b1f5148f3bbf5331d` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Premise inversion verified independently, not taken from the analyst: `git log -1 9a84e46` → `Stefan Hoevelmanns <shadowhvlmnns@gmail.com>`, 2026-09-16 13:17 +0200, "Drop the gitfs submodule, absorbed into fs"; `git merge-base --is-ancestor 9a84e46 HEAD` exit 0; `git show --stat 9a84e46` → `.gitmodules` −3, `gitfs.ctg` −1 (the gitlink). The user answered his own question in code, so rewriting Outcome/Acceptance to "the composition is clean" is the only honest reading — keeping "gitfs is back" would have required re-adding a submodule the user had just deleted. **Verification-only is honest.** I swept the tree myself rather than trusting the report: `grep -rIn 'gitfs\.ctg'` excluding `.git`, `target`, `node_modules` and `/boards/` returns exactly one file, `prd.ctg/.cartridge/reports/record-migration/manifest.json`, a provenance record. Every other surviving `gitfs` string is the *tool* name (`.gitignore:41` fs's store, `policy.ctg/.cartridge/docs/policy.md:10,19`, `sessions.ctg/src/change_record.rs:162` `refs/gitfs/`). No live work is being waved through. −1: the PRD title still reads "gitfs is back in the composition" while its Outcome says the opposite; the slug is identity and frontmatter is out of bounds, so this is residual rather than fixable, but a board reader sees a title meaning the inverse of the row. |
| Ownership and reuse | 19 | The `repo` retarget is not a preference, it is required, and I proved the analyst's argument is *understated*. `feet()` resolves each foot against `codeRepo(prd)` (`planner.ts:5-9`) and `collect` maps it with `path.relative(code, f)` (`lifecycle.ts:129,144,152,173`). With the old pair, `path.relative('/Users/feb/dev/cartridge/fs.ctg', '/Users/feb/dev/cartridge/.cartridge/config.lua')` = `../.cartridge/config.lua`; I ran the exact call `assertFootprint` makes — `git -C fs.ctg diff --name-only --no-renames -z $H $H -- ../.cartridge/config.lua` → **exit 128**, `fatal: … is outside repository`. `assertFootprint` checks `diff.exitCode` and throws `could not validate committed source footprint`, so the previous pair would have aborted collection at the first line of `collect`, before any verification. The retarget is a bug fix. Both rejected inventions **agreed**: (a) the migration manifest is provenance — rewriting it would falsify where records came from, and it is the only live-tree `gitfs.ctg` string left; (b) a bun test asserting "0 not enabled" would be a superproject-state assertion living in a submodule's suite, and the invariant is false in general — `cartridge help` from `/tmp` prints `0 cartridges enabled, 9 installed and not enabled`, empirical proof that install-without-enable is a supported state. The `gitfs` board alias, the `gitfs`/`ship` policy rows and `fs.store_dir = ".cartridge/gitfs"` are correctly left alone. −1: `boards/gitfs/settings.md` still defaults `repo` to `.../fs.ctg`, and nothing in the board record says this PRD had to override it; the next row on this board inherits the same unusable default. |
| Dependencies and implementable slices | 18 | The no-lane derivation is correct and I tested the failure mode instead of reasoning about it. `claim` from `specced` creates the lane worktree (`lifecycle.ts:220-223`, `git worktree add -b lane/gitfs-<slug>`); `collect` then sets `tree = lane` (`lifecycle.ts:130`). I built a faithful lane simulacrum in the scratchpad — real `.gitmodules` and `.cartridge/init.lua`, all 18 submodule directories present and empty — and ran the blocks there: block 1 exit **1** (`is in no trusted project`), block 2 exit **1** (`test -f fs.ctg/cartridge.json`). So a mis-claim fails loudly rather than passing vacuously, which is better than the spec claims. Landing path confirmed: state is `analyzing`, `collect` accepts `claimed` or `specced` (`lifecycle.ts:112`), and the lane is created only by `claim` — so `prd specced` → `prd collect`, never `prd claim`. −2: the spec states the prohibition but not the recovery. If a lane is created anyway, the worktree and the `lane/gitfs-gitfs-is-back-in-the-composition` branch both survive the failed collection and `claim` then refuses with `pre-existing lane must be inspected before claim`; the spec's own landing instruction should carry `git worktree remove … && git branch -D lane/…` beside it. |
| Observable acceptance and baseline evidence | 19 | Every figure re-measured, none taken on trust. `.gitmodules`: 18 stanzas, `git config -f .gitmodules --get-regexp '^submodule\..*\.path$'` names no gitfs. `git ls-files --stage -- gitfs.ctg` → 0 lines. `ls -d gitfs.ctg` → exit 1, absent. `.cartridge/init.lua`: 19 `{ id = … }` entries, no gitfs. `cartridge help` (cwd repo root) → `19 cartridges enabled, 0 installed and not enabled`. `cartridge ledger` → one row per key, `fs.ctg  (fs)`. On disk, `./fs.ctg/cartridge.json` is the only manifest naming `"tool.gitfs"` or `"tool.ship"`, and I confirmed the block's glob is not under-reaching: `find . -maxdepth 3 -name cartridge.json` outside `.git`/`target` returns nothing the `./*.ctg/` + `./*.ctg/*/` pair misses. `cartridge status` → `cartridges active: 19`. Live write→read→ls succeeded on `refs/gitfs/18d5ca53d7f604a8-13`. The spec's three acceptance boxes map 1:1 onto the PRD's three. −1: both blocks *print* their counts (`19 cartridges enabled`, `cartridges active: 19`) but gate only the invariants, so a silently shrunken composition would still pass all three boxes. Recording the number in the receipt is a defensible trade against a brittle hard-coded 19; noted rather than demanded. |
| Failure, recovery and compatibility | 18 | **The guards are real, and I went past the analyst's four probes to eight.** Reproduced as reported: regressed scratch tree (`gitfs.ctg/` + gitfs stanza + gitfs `init.lua` entry) → block 1 exit **1** (`gitfs.ctg is still installed under the cartridge root`); stub `CARTRIDGE_BIN` ledger with two owners per key → block 2 exit **1**; stub status carrying `"state":"failed"` → block 3 exit **1** (`a cartridge of the running host is not active`); empty tree → blocks 1, 2 and 3 all exit **1** on their `test -f`/first command, not vacuously. Added by me, each isolating one guard: stanza-only regression → **1** (`.gitmodules still registers gitfs.ctg`); `init.lua`-entry-only regression → **1** (`.cartridge/init.lua still composes a gitfs cartridge`); stub help printing `1 installed and not enabled` → **1**; `CARTRIDGE_BIN=/nonexistent` → **1**. Structural checks pass: `grep -n '^\s*!\|if !\|&& !\|cd \|CARGO_TARGET_DIR\|\.\./'` over all three extracted blocks matches **nothing** — no `!`-prefixed guard for POSIX `set -e` to swallow, no `cd`, no cargo, no `../sibling` path; every file read is preceded by `test -f`/`test -e`. **The `cartridge help` exit tolerance is acceptable here**, and not on the spec's say-so: `print_overview` returns `broken.len()`, the number of enabled modules shipping no `.cartridge/help.md` (`manual.rs:345-355`), a quantity orthogonal to every claim this PRD makes — and the overview line is printed *before* that count is computed, so the status cannot carry composition information. `|| true` therefore hides only the separately-filed defect, and I proved it opens no hole: the block still exits 1 on a missing binary, on a wrong count, and from the wrong cwd (`/tmp` → `0 cartridges enabled, 9 installed and not enabled`, which fails the `, 0 installed and not enabled$` anchor). One immaterial correction to `analyst-2.md` row 5: `cartridge help` from `/tmp` exits **1** here, not 0; the conclusion it supports is unaffected. **The cargo substitution is sound and strictly better than what it replaced**: the box claims the *composed* host, which `cargo test --lib` in `fs.ctg` would not exercise, and building in the live checkout would hot-restart cartridges other sessions are using. It leaves the worktree untouched as claimed — after block 3, `ls .cartridge/gitfs-composition-probe.txt` → absent, and `git status --porcelain --untracked-files=all -- .gitmodules .cartridge/init.lua .cartridge/gitfs-composition-probe.txt` → empty, so pass 2's `source footprint changed during integrated verification` cannot fire. Confirmed that a duplicate-key clash is genuinely observable: `plan::catalogue` records the clash (`plan.rs:244-264`), the slot becomes `State::Failed` (`host/mod.rs:355-358`) and `status()` maps over *all* slots (`host/mod.rs:215-224`), so a clashed cartridge appears with `"state":"failed"` rather than vanishing. −2: (a) the spec asserts the two footprint paths "are exactly what would have to change for the outcome to become false again" — an overclaim; boxes 2 and 3 can become false through `fs.ctg/cartridge.json` or the running host, neither of which *can* sit in a superproject footprint (a path inside a submodule is a gitlink to the superproject's git). The choice is right; the justification should say "the two paths that can be footprinted", not "exactly what would have to change". (b) Block 3 is non-hermetic by construction — it needs the live daemon answering — so the receipt is not reproducible from a clean checkout. Acknowledged in Remaining risk and unavoidable given the claim, but it is a real bound on the evidence. |
| Reviewer total | **93** / 100 | >= 90 and no blocking finding. |

Findings and concrete revisions:

1. *(non-blocking, recommend)* The no-lane instruction states the prohibition but
   not the recovery. Add to spec Steps 1: if a lane was created, `git worktree
   remove prd.ctg/.cartridge/boards/gitfs/.lanes/gitfs-is-back-in-the-composition`
   and `git branch -D lane/gitfs-gitfs-is-back-in-the-composition` before retrying,
   because `claim` otherwise refuses with `pre-existing lane must be inspected
   before claim` (`lifecycle.ts:221`). Evidence: lane simulacrum, blocks 1 and 2
   both exit 1.
2. *(non-blocking, recommend)* Soften the footprint justification in spec01
   "Why repo, footprint and 'no lane' must change": `.gitmodules` and
   `.cartridge/init.lua` are the two paths that *can* carry this claim in a
   superproject footprint, not the complete set of inputs whose change would
   falsify the outcome. Acceptance boxes 2 and 3 also depend on
   `fs.ctg/cartridge.json` and on the running host, which are unfootprintable
   from here. The verify blocks still check all three boxes regardless, which is
   why this is prose, not a gate.
3. *(non-blocking, note for the coordinator)* Landing procedure, not spec
   content: the PRD is `analyzing` with open `- [ ]` boxes in both `prd.md` and
   `specs/spec01.md`. `collect` throws `collect: open acceptance boxes remain`
   (`lifecycle.ts:113`, `records.ts:345`) and `collect requires claimed or
   specced work` (`lifecycle.ts:115`). Path: tick all six boxes, `prd specced`,
   then `prd collect` — never `prd claim`. The done sibling
   `@root/…/agent-runs-key-per-attached-instance-not-per-process` carries `[x]`
   boxes at collect and its spec Steps likewise do not restate this, so the
   omission matches board practice; recorded because this row has no worker and
   nobody else will tick them.
4. *(non-blocking, note)* `boards/gitfs/settings.md` keeps `repo:
   /Users/feb/dev/cartridge/fs.ctg`. Correct as the owner alias, but it is the
   unusable default this PRD had to override; a one-line comment there would
   stop the next gitfs row repeating the mistake.
5. *(correction to the analyst record, immaterial)* `analyst-2.md` commands
   table row 5 reports `cartridge help` from `/tmp` exiting 0; measured exit is
   1. The finding it supports — that the global-home fallback reports `0
   enabled, 9 installed and not enabled` and so the block must run inside the
   project — holds and is what the block's `grep` anchor enforces.

Disposition: **keep**. Verification-only is honest and the slice gates something
real: eight failure probes show every guard fires independently, and the two
footprint paths are precisely the ones a gitfs regression would touch.

Validation (all cwd `/Users/feb/dev/cartridge` unless noted; no `prd` transition,
no commit, no `git add`, no daemon start/stop/replace/reload, no cargo):

| # | command | cwd | exit | note |
| --- | --- | --- | ---: | --- |
| 1 | `git rev-parse HEAD`; `git log -1 9a84e46`; `git merge-base --is-ancestor 9a84e46 HEAD`; `git show --stat 9a84e46` | repo | 0 | user-authored, ancestor, drops stanza + gitlink |
| 2 | `git status --porcelain -- .gitmodules .cartridge/init.lua` (before blocks) | repo | 0 | empty |
| 3 | block 1, `sh -eu -c "$(cat block1.sh)" </dev/null` | repo | **0** | `19 cartridges enabled, 0 installed and not enabled`; <1 s of 120 s |
| 4 | block 2, same form | repo | **0** | one owner per key; `./fs.ctg/cartridge.json` only manifest; <1 s |
| 5 | block 3, same form | repo | **0** | `cartridges active: 19`; write/read/ls on `refs/gitfs/18d5ca53d7f604a8-13`; <1 s |
| 6 | `git status --porcelain -- .gitmodules .cartridge/init.lua` (after blocks) | repo | 0 | empty; `ls .cartridge/gitfs-composition-probe.txt` → absent |
| 7 | block 1 in regressed scratch tree (`gitfs.ctg/` + stanza + entry) | scratch | **1** | `gitfs.ctg is still installed under the cartridge root` |
| 8 | block 1 in stanza-only scratch tree | scratch | **1** | `.gitmodules still registers gitfs.ctg` |
| 9 | block 1 in `init.lua`-entry-only scratch tree | scratch | **1** | `.cartridge/init.lua still composes a gitfs cartridge` |
| 10 | block 1 with stub `CARTRIDGE_BIN` printing `1 installed and not enabled` | scratch | **1** | count gate fires |
| 11 | block 1 with `CARTRIDGE_BIN=/nonexistent/cartridge` | scratch | **1** | `|| true` opens no hole |
| 12 | block 2 with stub ledger listing two owners per key | scratch | **1** | owner count 2 ≠ 1 |
| 13 | block 3 with stub status `"state":"failed"` | scratch | **1** | `a cartridge of the running host is not active` |
| 14 | blocks 1, 2, 3 in an empty git tree | scratch | **1, 1, 1** | fail on `test -f` / first command, not vacuously |
| 15 | blocks 1, 2 in a lane simulacrum (real `.gitmodules` + `init.lua`, 18 empty submodule dirs) | scratch | **1, 1** | `is in no trusted project`; `test -f fs.ctg/cartridge.json` |
| 16 | `cartridge help` | repo | **1** | `host` ships no help page; overview line correct |
| 17 | `cartridge help` | `/tmp` | **1** | `0 cartridges enabled, 9 installed and not enabled` — fails the block's anchor |
| 18 | `git -C fs.ctg diff --name-only --no-renames -z $H $H -- ../.cartridge/config.lua` | `fs.ctg` | **128** | proves the old `repo`/`footprint` pair aborts `assertFootprint` |
| 19 | `git -C fs.ctg status --porcelain=v1 -z -uall -- ../.cartridge/config.lua` | `fs.ctg` | — | `fatal: … is outside repository` |
| 20 | `grep -n '^\s*!\|if !\|&& !\|cd \|CARGO_TARGET_DIR\|\.\./'` over the three extracted blocks | scratch | 1 | no match: no `!` guard, no `cd`, no cargo, no sibling path |
| 21 | `grep -rIn 'gitfs\.ctg'` excluding `.git`/`target`/`node_modules`/`/boards/` | repo | 0 | one file: `reports/record-migration/manifest.json` |
| 22 | `find . -maxdepth 3 -name cartridge.json` outside `.git`/`target` | repo | 0 | nothing escapes block 2's glob |

Blocks were extracted with the engine's own rule (split on `^##\s`, keep
`Verify|Verification|Proof` sections, take `^```(sh|bash|shell)` fences —
`lifecycle.ts:36-39`) and run as `sh -eu -c <block>` with `</dev/null`, matching
`lifecycle.ts:44`. All three finish in under one second against the 120 s limit.

Reviewer identity: independent reviewer agent (coordinator cartridge-1b).
User rating: not supplied; delegated per the 2026-09-13 instruction "i dont rate, you do".
User feedback/provenance: the user's decision is commit `9a84e46` (option (b)),
which this review verified against the reviewed revision rather than restating.
Result: **PASS (93/100)**.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed to landing. Tick the six acceptance boxes in `prd.md` and
`specs/spec01.md`, `prd specced`, then `prd collect` from `specced` with **no
lane** and the daemon up. Findings 1, 2 and 4 are optional polish and do not
require another round; applying 1 or 2 changes `spec01.md`, which makes this
rating stale and costs round 2, so apply them only if the coordinator wants them.
