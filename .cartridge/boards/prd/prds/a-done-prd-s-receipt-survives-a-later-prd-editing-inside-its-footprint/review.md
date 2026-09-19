# @prd/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint review history

Plan: `@prd/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint`, at `prd.ctg/.cartridge/boards/prd/prds/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint/prd.md`.
Scope: one observable outcome. A done leaf's receipt survives a later, separately collected PRD that edits inside its footprint, and an unreviewed edit still drifts. This is an executable leaf with one spec.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md).

## Round 1 — 2026-09-19

Presented revision: prd.ctg HEAD `ee4d910f`. The PRD directory is untracked. Live `src/lifecycle.ts`, `.cartridge/tests/engine.test.ts` and `.cartridge/templates/spec.md` carry another session's uncommitted edits, and the spec was judged against HEAD.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `666fb11a2ce0787e4c4728215781122fccbbaedfb4e0b661b92d165d52b8461d` |
| Specs | `specs/spec01.md` SHA-256 `1c6d870674fa3b9d0d6f11b4866bdfd397cdd2ff539c28e2ed3fbcdf5f8b4234` |
| Material contracts/dependencies | `src/lifecycle.ts` at HEAD SHA-256 `177200f02a8cb1c2257c0482f52cafb5ef5e7f160f28ed4835691c4ba9274b11` (live dirty file `e5421d97…eb772`). `src/planner.ts` SHA-256 `fd60f4c7…fcfe`. Analyst reference `scratchpad/reference.patch` and `scratchpad/receipt-drift.test.ts`. |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | The problem is real and reproduced. The live search child and its parent rollup are blocked by a legitimate sibling collection. The scope is one function and one test file. Deduction: the acceptance promises more soundness than the rule delivers (see F1). |
| Ownership and reuse | 18 | The check stays in `completionProblem` and reuses `feet`, `git` and the existing `seen` cycle guard. It adds no import. The hunk applies cleanly over the live uncommitted edits (`git apply --check`, offset 68 lines, no conflict). |
| Dependencies and implementable slices | 16 | This is one spec with no needs. Deduction: a sound fix for F1 probably needs `collect` to record the lane base in `collection.md`. That changes the spec's footprint region and conflicts textually with the live hunk at HEAD line 175. |
| Observable acceptance and baseline evidence | 13 | The reference turns the three named tests green, and base fails them. Deductions: acceptance bullet 2 is false as written (F1, F2) and no test covers either abuse case. The timing claim does not reproduce (F3). The base count is misstated: base gives 1 pass and 2 fail, not 1 pass and 1 fail. |
| Failure, recovery and compatibility | 12 | A stale voucher, a voucher that does not match bytes, an uncommitted edit, a deleted path and cycles are all handled. Two ways to launder a hand edit remain (F1, F2). This is the integrity check the engine depends on. |
| Reviewer total | 77 / 100 | |

Findings and concrete revisions:

- **F1 (blocking).** A hand commit that lands before a later PRD's lane is excused. The rule vouches for every byte at the later receipt, including commits that landed before that lane's base. The Design's claim that whatever those commits wrote is the content at the receipt overlooks commits from before the lane.
  - Reproduced in the fixture `…/reviewer-receipt-1/abuse.test.ts`, test 1. After `search` is done, a hand commit edits `web/search.txt`. A new leaf `broad` (footprint `web`, proof `true`) is then claimed and collected, and its lane writes only `web/broad.txt`.
  - Base: `parent/search` still reports `verified source footprint changed after collection`.
  - Reference: `parent/search` reports `null`.
  - This contradicts spec acceptance 2 and PRD acceptance 2 ("An uncollected or hand-made commit … still reports").
  - Fix: record the lane base (`initialHead`) in each new `collection.md`. A voucher then counts only when the file changed within `base..commit`, and its content at `base` is itself reviewed relative to the earlier receipt; apply this recursively. For legacy receipts that have no base, choose between two options. (a) Stay conservative. The evidence case then clears only after its sibling is recollected. (b) Accept byte equality for legacy receipts. That needs a reworded acceptance approved by the user, because the PRD's acceptance is `origin: requested`. Add a named test for whichever option is chosen.
- **F2 (blocking).** A container launders a hand commit and verifies nothing. `feet()` includes a parent's own `footprint`, and a container's receipt is `container: every child done` at the HEAD at the time it was collected.
  - Reproduced in `abuse.test.ts`, test 2. A hand commit edits `web/search.txt`. An unrelated container `q` (footprint `web`) has one child `q/c` (footprint `lib`). Collecting `q/c` and then `q` exits 0.
  - Reference: `parent/search` reports `null`. Base: it drifts.
  - Fix: a record with children, or a receipt without `: exit 0` evidence, never vouches. Add a named test.
  - In the live data every voucher is a leaf (see the instrumented probe below), so this hole is latent but open.
- **F3 (non-blocking).** The performance evidence does not reproduce. On a copy of the live records, `completionProblem` over 374 done records took 3.6 s on base and 10.2 s on the reference, measured twice each. That is a 2.8x slowdown, not 19.6 s against 20.4 s. The absolute cost is acceptable, so correct the evidence.
- **F4 (non-blocking).** The Verify blocks gate by grepping named passes, which is correct at HEAD because `test` blocks are not committed yet. When the F1 and F2 tests are added, name them in block 1. If the live `test`-block edits land first, move to a `test` block.

Disposition: revise.

Validation. Each Verify block ran as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c` in `git clone --local` copies at `…/scratchpad/reviewer-receipt-1/{base,ref}`, with `node_modules` copied in:

- Base plus the new test file: block 1 exited 1 in 8 s, with 1 pass and 2 fail. Block 2 exited 0 in 23 s.
- Reference: block 1 exited 0 in 9 s, with 3 pass and 0 fail. Block 2 exited 0 in 9 s, with 26 pass and 0 fail. `tsc --noEmit` exited 0.
- Abuse fixture `abuse.test.ts`, with three tests:
  - Base: exit 0, 3 pass.
  - Reference: exit 1, 1 pass and 2 fail. Both failures show `Received: null` at the final drift assertion, lines 50 and 58. The control test (an uncommitted edit over a sibling's path still drifts) passes.
- Live-records copy `…/reviewer-receipt-1/live`, read-only probe `probe.ts` over the root board (645 records, 374 done):
  - Problems fell from 341 to 334.
  - No record that was clean on base became problematic.
  - Seven records cleared, including `…/search-returns-ranked-results-each-with-its-source-url`, `…/web-ctg-exists-…`, `@gitfs/gitfs-is-back-in-the-composition` and four others.
  - The instrumented run `reflog/` shows every voucher is a leaf.
- `git apply --check` of the reference patch on the live dirty `src/lifecycle.ts` succeeded.

Reviewer identity: reviewer-receipt-1 (independent review sub-agent, Opus 5).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (77/100).
Unresolved blocking findings: F1, F2.
Rounds used / remaining: 1 / 4.
Next action: make one bounded revision. Exclude containers from vouching (F2). Either bind vouchers to the lane range through a recorded base, or obtain the user's decision on the weaker semantics for legacy receipts (F1). Add named tests for both cases and correct the timing evidence. Then request round 2.
