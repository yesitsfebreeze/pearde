# @root/the-shared-record-describes-only-this-repository/the-vision-memo-states-today-s-composition review history

Plan: @root/the-shared-record-describes-only-this-repository/the-vision-memo-states-today-s-composition (prd.md, specs/spec01.md).
Scope: leaf.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: none (split 2026-09-19 with none used).

# the-shared-record-describes-only-this-repository/the-vision-memo-states-today-s-composition review history

Plan: root board, leaf PRD `the-shared-record-describes-only-this-repository/the-vision-memo-states-today-s-composition`.
Scope: one observable outcome — the "Where the composition actually stands" section of `system/vision.md` re-measured and re-dated.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none (split from `@root/the-shared-record-describes-only-this-repository` on 2026-09-19 with no rounds used before the split).

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.

## Round 1 — 2026-09-19

Presented revision: repo HEAD `c84b3a4126224af211de08f2e45fe06e705a5e99`, dirty checkout (target file and routine both clean/untracked at base).

| Input | Content digest |
| --- | --- |
| Plan | `prds/the-shared-record-describes-only-this-repository/the-vision-memo-states-today-s-composition/prd.md` sha256 `c5998c88c95ca7a3e5f892fcad9cb4d63597f37d5c7d369b37d2a308d6747634` |
| Specs | `specs/spec01.md` sha256 `1bf73cf03e6f52768982ef45eef05ee25ee47c4ca743f34fee332a4fe9bbb5d8` |
| Analyst evidence | `.state/loop/the-vision-memo-states-today-s-composition/analyst-1.md` sha256 `09f066db6762ce660c5a69e2052021f0a05d527f6155358d0f6d6178633eb6c5` |
| Target at base | `.cartridge/memos/system/vision.md` sha256 `79eb89fde901cf39d5cf3a69520d215cbc053d83111b0971385ce52b232f7235` (matches the analyst's recorded base revision) |
| Dependency routine | `.cartridge/memos/routine/check-cartridge-isolation.md` sha256 `23f76eb5e6e4bdd409c6fb6e6eeb3650e5a9c9a5f7e3268d28c0cfc7c26c7a0a` |
| Cross-owner dependency | `prds/the-isolation-gate-reads-the-composition-profile/prd.md` — state `open` (not yet landed) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Single observable outcome (re-date and re-measure one vision-memo section), footprint is exactly one file, and the PRD correctly excludes the out-of-scope overclaim at vision.md:162 ("Isolation of code already holds"), leaving it for the isolation-gate PRD as analyst-1.md notes. -1 for scope-adjacent noise: the Outcome sentence "It shares `system/vision.md` with `the-isolation-gate-reads-the-composition-profile`" is not actually true of the declared footprints (see Ownership finding below). |
| Ownership and reuse | 18 | Reuses the existing memo tool write path (read → splice → write with `expected_revision`), no new files, no new abstractions. -2 for a footprint/ownership mismatch: `the-isolation-gate-reads-the-composition-profile/prd.md` declares footprint `.cartridge/memos/routine/check-cartridge-isolation.md` only, not `system/vision.md`, even though its own acceptance #4 requires it to edit vision.md too. Only this PRD declares vision.md in its footprint, so the "land one after the other" sequencing this PRD's Outcome asserts is not engine-enforced from the other side. Non-blocking: the spec's Verify already tolerates either landing order (confirmed by mutation testing below), so nothing breaks either way; this is a planning-hygiene gap in the sibling PRD, not in the one under review. |
| Dependencies and implementable slices | 19 | Both `needs` entries (`the-record-s-routines-run-in-this-repository`, `every-link-in-the-record-resolves-and-a-test-says-so`) are already collected (repo log: `03228f3`, `e6c2a8f`). The remaining soft dependency, the isolation-gate PRD, is still `open`; the spec's conditional Verify clause correctly handles both "still open" and "landed" cases (verified). Single spec, single file, directly implementable. -1 for the same footprint-sequencing softness noted above. |
| Observable acceptance and baseline evidence | 20 | Independently re-measured every claim in analyst-1.md's probe table against today's tree from repo root, `env -u CARTRIDGE_YOLO`: `just audit` → 18 of 18 pass, soft findings match (memory.ctg 6, memo.ctg 2, prd.ctg 1 stray root entries); `just isolation` → "Isolation passed for 18 cartridges."; `.cartridge/init.lua` → 18 `id =` path entries, no `live-record`/`live-mcp`; all 19 `*.ctg` (cartridge.ctg included) have `README.md` and `.cartridge/help.md`; `memory.ctg` 40,778 source lines, median of the 18 audited cartridges = (2700+2795)/2 = 2747.5 ≈ "near 2,750"; `git -C prd.ctg ls-files` = 4507 (4403 under `.cartridge/boards`, ≈97.7%, consistent with "about 4,500 ... nearly all board records"); `check-cartridge-isolation.md:52` still reads `cartridge.ctg/.cartridge/init.lua`, line 59 builds `owner[k]` only from `m.provide`, and `grep -l '"provide"' */cartridge.json` returns 0 manifests — the key check is confirmed inert. `just test layout`: 2 pass / 1 fail, the failure is `recorded memory source and SDK build from a recursive composition snapshot` (ENOENT `builtin/memory`), unrelated to this section's claims; the drafted section correctly omits it. Every number in the drafted section matches today's re-measurement. |
| Failure, recovery and compatibility | 19 | The memo-tool write procedure is sound: shell cwd is the live root, the JSON `cwd` is the absolute lane path, `.text`/`.revision` are read first, the whole body is written with `expected_revision` (optimistic concurrency), and the memo write validates links on save. Description frontmatter (194/200 chars) is untouched by a body-only splice. Verify-block correctness independently re-tested on a scratch fixture (`/private/tmp/.../scratchpad/vision-r1/`, `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`, no live-checkout edits): base tree → exit 1 `measurement date 2026-09-16 predates the sibling children`; drafted section (today's date) → exit 0 `vision-section-ok`; mutant stale date → exit 1; mutant gate bullet trimmed while routine still reads the host profile → exit 1 `the isolation gate still reads the host profile and the section no longer says so`; mutant heading renamed (empty section) → exit 1 `section missing or thin: 0 bullets` (no vacuous pass); mutant reintroducing a `live-record` line → exit 1; mutant with the routine fixed and the bullet updated to drop the host-profile mention → exit 0. No inert guards: both `grep` checks use `if grep ...; then exit 1; fi` (non-negated), not `! grep`, and there is no `a && b` used to gate a failure. The block reads only tracked files and writes nothing, so it is safe to run twice (lane, then repo) unmodified; it uses no cargo, so `CARGO_TARGET_DIR` is not applicable. -1 because the exact-count claims (`prd.ctg` file count, per-cartridge line counts) will drift day to day; the section already hedges with "about 4,500" but "40,778" and "2,750" are precise enough that a future re-measurement a few days later could read differently without re-triggering the gate (the Verify only checks for a fresh date and named commands, not exact-number staleness) — acceptable given the section states it must be re-measured "on the day it is written," but worth a reviewer note for whoever re-runs this after today. |
| Reviewer total | 95 / 100 | |

Findings and concrete revisions:
- Non-blocking — Ownership/sequencing: `prds/the-isolation-gate-reads-the-composition-profile/prd.md` footprint does not list `system/vision.md`, so this PRD's Outcome claim that the two "share `system/vision.md` ... so the two land one after the other" is not engine-enforced. Fix (not authorized in this review's scope): when that sibling PRD is next revised, add `system/vision.md` to its footprint, or soften this PRD's Outcome sentence to describe the overlap as advisory. No action needed now — the spec's Verify block already produces the correct result under either landing order (independently confirmed by mutation test).
- Non-blocking — informational: exact numeric claims (`40,778` source lines, `2,750` median, `4,505`/`4,507` files) will go stale within days; the section is explicitly framed as "re-measured on the day it is written" and the Verify gates the date, not the numbers, so this is inherent to the design and not something to fix in this round.

Disposition: keep.
Validation: `env -u CARTRIDGE_YOLO just audit` (exit 0, 18/18 hard checks pass), `env -u CARTRIDGE_YOLO just isolation` (exit 0, "Isolation passed for 18 cartridges."), `env -u CARTRIDGE_YOLO just test layout` (2 pass / 1 fail, unrelated ENOENT), `grep -n 'id = ' .cartridge/init.lua` (18 entries), `test -f README.md .cartridge/help.md` per `*.ctg` (19/19), `grep -l '"provide"' */cartridge.json` (0), all run from `/Users/feb/dev/cartridge` cwd, foreground. Verify-block reproduction run under `/private/tmp/claude-501/-Users-feb-dev-cartridge/a3492fbd-f726-4514-b5ee-796fd5ea14c1/scratchpad/vision-r1/{base,drafted,mutA,mutB2,mutC,mutD,mutE}` with `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`; live checkout untouched, no edits, no commits, no prd transitions, no daemon actions.
Reviewer identity: fresh reviewer agent, coordinator-5c-15.
User rating: not required under delegation; none supplied.
User feedback/provenance: none.
Result: PASS.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed to implementation (write the drafted section through the memo tool per spec01.md's "How to write it").

VERDICT: PASS
