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

## Round 2 — 2026-09-19

Presented revision: `specs/spec01.md` rewritten by analyst-2; `prd.md` unchanged from round 1 in body and frontmatter. Judged against prd.ctg `4e543acc`, the HEAD the analyst built on; `src/lifecycle.ts` is byte-identical at the later HEAD `e27c2f48`, so the judgement carries. The live `src/lifecycle.ts` and `.cartridge/tests/engine.test.ts` still carry another session's uncommitted edits and were never written to.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `0a3a2ea8363f3a3d1b2d01ff812f6df7d255af0ae995f7b6581fe94527387794` |
| Specs | `specs/spec01.md` SHA-256 `3539cc865389fdc016d63842ddfc0424f4c94d546e388cd1dc637300682d29bd` |
| Material contracts/dependencies | `src/lifecycle.ts` at HEAD SHA-256 `177200f02a8cb1c2257c0482f52cafb5ef5e7f160f28ed4835691c4ba9274b11` (live dirty file `e5421d97…eb772`, unchanged since round 1). Analyst artifacts in the gitignored `.state/loop/receipt-survives/`: `reference.patch` SHA-256 `9a09d8c6604e8f788c0bd09e0fbfa0e4925cf32a4644ef8bfa2c3b6255532015`, `receipt-drift.test.ts` SHA-256 `f8bc75570ad35ccc443da47bd3d653fc1110b03754b3931eadd38471a2b8ecb6`. |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The rule is now sound where round 1 was not, and the scope is still one function, one receipt field and one test file. Deduction: the change clears nothing on the live board. Measured on 374 done records, the reference reproduces base's verdicts byte for byte, so the PRD's own evidence case and the parent rollup it names stay blocked on the day this lands (F6). |
| Ownership and reuse | 19 | The check stays inside `completionProblem`, reuses `feet`, `codeRepo`, `git` and the existing `seen` cycle guard, adds no import, and touches one other line in `collect`. The `laneRange` memo is keyed by repository and by the immutable `base..commit` pair. |
| Dependencies and implementable slices | 18 | One spec, no needs. Step 1's rebase instruction is accurate down to the reject: hunks 1 and 2 apply to the live dirty file at offset 68, hunk 3 rejects on context alone because the line above the receipt became `removeLane(code, work.directory)`, and the receipt line itself is identical at live line 245. Step 5's conditional conversion to a `test` block is correct; the live uncommitted `verificationBlocks` does return `kind: 'test'`. |
| Observable acceptance and baseline evidence | 14 | The six tests are named, executed and discriminating: against a round-1 rule rebuilt independently by this reviewer they give 3 pass and 3 fail, with the F1 and F2 tests both showing `Expected: "verified source footprint changed after collection"` and `Received: null`. Deductions: the Design asserts that an evil merge drifts, and no test covers it, and the assertion is false (F5). The corrected timing figures do not reproduce here either (F7). |
| Failure, recovery and compatibility | 13 | F1 and F2 are closed at their root, the recovery sequence is pinned end to end, legacy receipts fail closed, and cycles, uncommitted edits and foreign repositories are all refused. Deduction: a hand edit committed as a merge resolution now passes a check that base refuses, so this revision weakens the integrity gate in one shape while strengthening it in two (F5). |
| Reviewer total | 80 / 100 | |

Findings and concrete revisions:

- **F1 (round 1, resolved).** Closed. In a clone carrying the reference, `a hand commit made before a later lane is not vouched for by that lane` passes; in a clone carrying the round-1 rule rebuilt from the round-1 finding, the same test fails with `Received: null`. The lane range is what closes it.
- **F2 (round 1, resolved).** Closed twice over, as claimed. The container test passes against the reference and fails against the rebuilt round-1 rule. Reading the diff, `other.children.length` and the `/: exit 0\b/` test on the receipt body are independent guards and either one alone refuses a container.
- **F3 (round 1, superseded by F7).** The timing evidence was corrected in the spec but the corrected numbers do not reproduce either.
- **F4 (round 1, resolved).** Verify block 1 now names all six tests, and the gate is real: it exits 1 on base and 1 on the round-1 rule, and 0 on the reference.
- **F5 (blocking, new).** A merge commit that introduces content into a done footprint is accepted with no voucher, so an unreviewed edit is laundered by committing it as a merge resolution. `git log --name-only` prints no file names for a merge commit unless a diff-merges mode is requested, so the log entry for such a merge is a bare `%H` with no files, the inner loop over files never runs, and nothing has to vouch. This falsifies PRD acceptance 2 and the spec's own Remaining limit, which states that an evil merge "is in no lane range, so it drifts".
  - Reproduced in a fixture built on the shipped `receipt-drift.test.ts` scaffolding. After `parent/search` is collected, a side branch and a main commit are merged with `--no-commit --no-ff`, `web/search.txt` is resolved to content neither parent had, and the merge is committed. Base reports `verified source footprint changed after collection`; the reference reports `null`. The probe printed the log output for that range as a single NUL-prefixed sha with no file lines.
  - Fix: add `--diff-merges=dense-combined` to the `git log` invocation. Verified: the evil-merge probe then passes, the six shipped tests stay at 6 pass and 0 fail, and a back-to-back live probe over 376 done records gives verdicts identical to the reference, so the flag costs nothing on real history. Dense-combined is the right mode rather than `-m` or first-parent, because it lists only the paths whose resolution differs from every parent, which is exactly the laundering case; a plain merge of a collected lane lists nothing and does not falsely drift. `collect` integrates with `merge --ff-only`, so no collection ever produces a merge commit and no receipt depends on this.
  - Also correct the Remaining limits paragraph, which currently describes the wrong behaviour, and add the evil merge as a seventh named test in Verify block 1.
- **F6 (non-blocking, new).** The conservative legacy semantics are honest but inert, and the spec should say so where the user will read it rather than only in the Design. Measured on the live root board, base and the reference produce byte-identical verdict maps over 374 done records: 343 problems, 65 of them this refusal, and `…/search-returns-ranked-results-each-with-its-source-url` among them in both. The same probe against the round-1 rule clears seven records including that one, which confirms the analyst's 0-of-374 is the migration's real cost and not a rule that fails to fire. A sound partial legacy fallback does exist and this reviewer built it — a receipt without `base:` vouches only for the one commit it records as its own `commit:`, keeping every other guard — and it holds all six tests at 6 pass and 0 fail while clearing four of the 65 live records. It does not clear the PRD's evidence case, because that sibling's lane landed two commits inside `web.ctg` and only the tip is recorded, so the conservative choice is close to forced. Recommendation: keep the conservative rule, and have the coordinator tell the user plainly that landing this does not unblock the rollup named in the PRD's Evidence, which is recovered only by re-collecting the sibling through the six-step sequence the spec pins.
- **F7 (non-blocking, new).** The corrected performance evidence still does not reproduce. Over the live board this reviewer measured base at 15624 ms and 15681 ms and the reference at 11961 ms and 7737 ms, so the reference was faster, not 25 per cent slower; the absolute numbers are dominated by machine load from concurrent sessions. The Verify blocks measured 13 s for block 1 and 29 s and 18 s for block 2, against the spec's claimed 10 s and 9 s. Nothing here is near the engine's 120 s per-block timeout, so this is a claim-quality finding: state these as bounds observed on a loaded machine rather than as measurements, or drop the absolute figures and keep the argument about one memoised `rev-list` per receipt.

Disposition: revise.

Validation. All probes ran in `git clone --local` copies of `prd.ctg` at `4e543acc` under `$TMPDIR/reviewer-receipt-2/`, with `node_modules` copied in and the analyst's `receipt-drift.test.ts` added: `base` (HEAD only), `ref` (HEAD plus `reference.patch`), `r1` (HEAD plus the round-1 rule rebuilt by this reviewer), `r2` (ref plus the legacy-tip fallback) and `r3` (ref plus `--diff-merges=dense-combined`). Nothing was written to the live checkout except this file, and no daemon was started.

- `git apply --check reference.patch` in a clean clone, exit 0; the same against the live dirty `src/lifecycle.ts` in a throwaway repository, exit 1 with hunks 1 and 2 at offset 68 and hunk 3 rejected on context.
- `bun test ./.cartridge/tests/receipt-drift.test.ts`: `ref` exit 0 with 6 pass and 0 fail; `base` exit 1 with 2 pass and 4 fail, the two abuse tests among the passes; `r1` exit 1 with 3 pass and 3 fail, failing exactly the F1 test, the F2 test and the re-collection test.
- Verify blocks extracted with the engine's own `verificationBlocks` (`blocks 2`, no `cd`, no absolute path, no cargo) and run as `env -i PATH="$PATH" HOME="$HOME" sh -eu -c`: `ref` block 1 exit 0 in 13 s and block 2 exit 0 in 29 s and 18 s; `base` block 1 exit 1 in 13 s and block 2 exit 0 in 16 s; `r1` block 1 exit 1. Block 1's name gate works because bun 1.3.14 prints `(pass) <name>` lines when its output is redirected; the log carried all six.
- `bun test ./.cartridge/tests/engine.test.ts ./.cartridge/tests/records.test.ts` in `ref`: 26 pass, 0 fail. `tsc --noEmit` in `ref`: exit 0. The whole suite in `ref`: 88 pass and 4 fail, all four in `statusline.test.ts`, which also gives 0 pass and 4 fail in the `base` clone, so the patch does not cause them.
- Evil-merge probe `merge-probe.test.ts`, written by this reviewer: `base` exit 0 with 1 pass, `ref` exit 1 with `Received: null`, `r3` exit 0 with 1 pass and the six shipped tests still 6 pass and 0 fail.
- Read-only probe over the live root board, importing each build's `src/` and never touching the live files. Base twice: `records=655 done=374 problems=343 drift=65`. Reference twice: identical counts, and `diff` of the two verdict maps exits 0. The rebuilt round-1 rule: `problems=336 drift=58`, clearing seven records including the PRD's evidence case, with none newly problematic. The legacy-tip fallback: `problems=339 drift=61`, clearing four, not including the evidence case. `ref` and `r3` run back to back on one board state: verdict maps identical.

Reviewer identity: reviewer-receipt-2 (independent review sub-agent, Opus 5).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (80/100).
Unresolved blocking findings: F5.
Rounds used / remaining: 2 / 3.
Next action: make one bounded revision. Add `--diff-merges=dense-combined` to the `git log` in the Design, add a seventh named test for the evil merge to the test file and to Verify block 1, and rewrite the Remaining limits paragraph that currently claims an evil merge drifts. Soften the absolute timing figures to observed bounds, and surface to the user that landing this does not unblock the rollup the PRD's Evidence names. Then request round 3.

## Round 3 — 2026-09-19

Presented revision: `specs/spec01.md` revised by analyst-2, bounded to F5, F6 and
the timing claims; `prd.md` unchanged in body and frontmatter since round 1.
Judged against prd.ctg HEAD `4fb90e79`. The analyst built on `4e543acc`;
`src/lifecycle.ts` is byte-identical at both, so the judgement carries. The live
`src/lifecycle.ts` and `.cartridge/tests/engine.test.ts` still carry another
session's uncommitted edits and were never written to.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `0a3a2ea8363f3a3d1b2d01ff812f6df7d255af0ae995f7b6581fe94527387794` (unchanged from round 2) |
| Specs | `specs/spec01.md` SHA-256 `1792c542668b887f7ee65d2acb40905d7999c97dec94d392304d92df43bface4` |
| Material contracts/dependencies | `src/lifecycle.ts` at HEAD SHA-256 `177200f02a8cb1c2257c0482f52cafb5ef5e7f160f28ed4835691c4ba9274b11` (live dirty file `e5421d97…eb772`, unchanged since round 1). Analyst artifacts in the gitignored `.state/loop/receipt-survives/`: `reference.patch` SHA-256 `1f95a0decab6e70f9345d7d0992b22bde83683fceb14c30d69fb520893d751b0`, `receipt-drift.test.ts` SHA-256 `0869941b6de9f0a15b7c31690f6230f6e75481d09682753a1aefa14391ab4018`. bun 1.3.14, git 2.55.0. |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | The rule is sound and the scope is still one function, one receipt field and one test file. Deduction: it clears nothing. Over the live root board at 689 records and 381 done, base and the reference produce byte-identical verdict maps, and the PRD's own evidence case still reports the refusal, so the rollup the PRD names stays blocked on the day this lands (F6, now recorded in the Design as the analyst was asked to do). |
| Ownership and reuse | 19 | Unchanged from round 2 and still accurate: the check stays inside `completionProblem`, reuses `feet`, `codeRepo`, `git` and the `seen` cycle guard, adds no import, and touches one other line in `collect`. This round's change is one flag on an existing spawn; the patch is still 34 added and 2 removed lines. |
| Dependencies and implementable slices | 18 | One spec, no needs. Step 1's rebase guidance is still exact: `src/lifecycle.ts` is byte-identical at `4e543acc` and at today's HEAD `4fb90e79`, so the described offsets and the one rejecting hunk still describe the tree the implementer will meet. |
| Observable acceptance and baseline evidence | 13 | The seven tests are named and genuinely discriminating: the reference gives 7 pass and 0 fail, the same reference with `--diff-merges=dense-combined` removed gives 6 pass and 1 fail with the evil-merge test failing at its final assertion on `Received: null`, and base gives 2 pass and 5 fail. Deduction: the Verify block that publishes those seven tests cannot pass on a correct implementation (F8), and one of the tests exceeds bun's default per-test timeout on this machine (F9), so the plan's own proof does not hold even though the tests behind it do. |
| Failure, recovery and compatibility | 17 | F5 is closed at its root and the flag was probed beyond the fixture: an ordinary merge of disjoint files names nothing, a conflict resolved by taking one parent's content names nothing, a clean octopus names nothing, and a hand-built evil octopus does name the file, so the octopus case the analyst left unverified is covered. The rule is also strictly weaker than base — `changed` is by construction the set of paths whose content differs from the receipt, and base refuses whenever that set is non-empty — so the flag cannot make a healthy record refuse. Deduction held for F9's flakiness rather than for the rule. |
| Reviewer total | 83 / 100 | |

Findings and concrete revisions:

- **F5 (round 2, resolved).** Closed by the flag alone, reproduced exactly as the
  analyst reported. In three clones of HEAD `4fb90e79` carrying the same test
  file — `base`, `ref` (the reference patch) and `noflag` (the reference patch
  with only `'--diff-merges=dense-combined', ` deleted, `diff` confirming the two
  builds differ in that one line) — `bun test ./.cartridge/tests/receipt-drift.test.ts`
  gives `ref` exit 0 with 7 pass and 0 fail, `noflag` exit 1 with 6 pass and 1
  fail, and `base` exit 1 with 2 pass and 5 fail. The single `noflag` failure is
  `an evil merge that resolves a footprint path to new content still drifts`,
  failing at line 141 with `Expected: "verified source footprint changed after
  collection"` and `Received: null`, which is the drift assertion and not an
  accident of the fixture. The fixture's own guard on line 140,
  `rev-list --merges -1 HEAD` equal to `rev-parse HEAD`, passes in that run, so a
  merge commit really was constructed.
- **F6 (round 2, resolved as a recording obligation).** The Design now states the
  cost plainly and this reviewer's measurement agrees with its direction while
  its absolute figures have already moved with the board: over
  `prd.ctg/.cartridge/boards/root` today the probe reads 689 records, 381 done,
  353 problems and 75 reporting this refusal, against the spec's recorded 657,
  376, 344 and 66. `diff` of the base and reference verdict maps exits 0 with no
  record changing verdict, and
  `…/search-returns-ranked-results-each-with-its-source-url` reports
  `verified source footprint changed after collection` on both. The census
  numbers in the spec are dated evidence rather than a claim about today, so this
  is not a finding; a reader should know the board moves under them.
- **F7 (round 2, partially resolved).** The softened wording is better than the
  round-2 figures, but the specific claim that "the two builds are inside each
  other's spread" does not reproduce here. Three alternating read-only runs over
  the live board give base 5502, 5896 and 7104 ms and the reference 11228, 8481
  and 8659 ms, so base's slowest run is faster than the reference's fastest and
  the reference is consistently 1.2 to 2.0 times base. Non-blocking, and the
  absolute cost is still a few seconds over a whole board. Revision: say that the
  reference costs up to about twice base over a whole board, a few seconds either
  way, rather than that the two are inside each other's spread.
- **F8 (blocking, new).** Verify block 1 cannot pass on a correct implementation,
  so the plan's published proof fails `collect` for the implementer. The block
  gates on `grep -Fq "(pass) $named"` for each of the seven tests, and bun 1.3.14
  prints no per-test line at all for a passing test when its output is not a
  terminal. Every block-1 run in this review exited 1 on the reference: three
  runs under `env -i PATH HOME` and three under the full environment, six of six.
  One of those full-environment runs reported `7 pass` and `0 fail` and the block
  still exited 1, with zero `(pass)` lines in its log. Reduced to a two-line
  probe: a file of two passing tests, redirected to a file, prints `2 pass` and
  `0 fail` and no per-test line; adding one failing test prints only the `(fail)`
  line, still none for the two that pass. Across this review's logs the `(pass)`
  line count is 0 for the reference's all-pass run, 0 for base's 2-pass run and 0
  for `noflag`'s 6-pass run; the single log that carried six `(pass)` lines is one
  that also reported an unhandled error and a killed dangling process, which is
  how round 2 and the analyst can both have observed the gate passing. The gate is
  therefore not merely wrong, it is nondeterministic, and it discriminates
  nothing: it exits 1 on the reference, on base and on the unflagged build alike.
  - Verified remedy: `bun test ./.cartridge/tests/receipt-drift.test.ts --timeout 30000 --reporter=junit --reporter-outfile=<file>`
    exits 0 on the reference, and the XML carries `<testcase name="…">` for each
    of the seven names together with `failures="0"`. I ran that command and read
    that output. What I did **not** verify is a rewritten Verify block built
    around it end to end, nor that it exits 1 on base and on `noflag`; treat the
    rewritten block as unverified until its author runs it against all three
    builds. Revision: replace the `(pass)` name gate with a gate over the JUnit
    report — each of the seven names present as a `testcase`, and `failures="0"` —
    or, if the engine committed at claim time executes `test` blocks, take step
    5's conditional conversion and let the engine's own report carry the names.
    Either way the new block must be shown to exit 0 on the reference and 1 on
    base before it is published.
- **F9 (non-blocking, new).** The first test exceeds bun's default 5000 ms
  per-test timeout on this machine, so the file is flaky independently of F8.
  `a later collected sibling inside the footprint leaves the receipt verified and
  the parent collects` — the heaviest test, since it also collects the parent —
  took 6511, 6729, 6896 and 6113 ms under `env -i` and 5903 and 6637 ms under the
  full environment, and bun reports `this test timed out after 5000ms` in each.
  It passed at 1428 ms in an unconstrained run, so the margin is real but thin.
  Revision: pass `--timeout 30000` to `bun test` in Verify block 1, or give that
  test an explicit timeout. Verified only to the extent that the run with
  `--timeout 30000` above passed all seven.

Disposition: revise.

Validation. All probes ran in `git clone --local` copies of `prd.ctg` at
`4fb90e79` under `$TMPDIR/reviewer-receipt-3/`, with `node_modules` copied in and
the analyst's `receipt-drift.test.ts` added: `base` (HEAD only), `ref` (HEAD plus
`reference.patch`) and `noflag` (`ref` minus the flag). Every command ran under
`env -u CARTRIDGE_YOLO`. Nothing was written to the live checkout except this
file, and no daemon was started.

- `git apply reference.patch` in a clean clone of HEAD, exit 0. `diff` of
  `ref/src/lifecycle.ts` against `noflag/src/lifecycle.ts`: one line, the flag.
- `bun test ./.cartridge/tests/receipt-drift.test.ts`: `ref` exit 0, 7 pass, 0
  fail; `noflag` exit 1, 6 pass, 1 fail, the evil-merge test with `Received:
  null` at line 141; `base` exit 1, 2 pass, 5 fail.
- Verify blocks extracted from the published spec with the engine's own
  `verificationBlocks` (`blocks 2`), and checked to contain no `cd`, no absolute
  path and no cargo. Block 1: `ref` exit 1 six times out of six (three under
  `env -i PATH HOME`, 23 to 32 s; three under the full environment, 19 to 26 s);
  `base` exit 1; `noflag` exit 1. Block 2: exit 0 everywhere, in 23 s on `ref`,
  23 s on `base` and 29 s on `noflag`, well inside the 120 s limit.
- Two-line bun probe establishing F8: two passing tests redirected to a file give
  exit 0, `2 pass`, `0 fail` and no `(pass)` line; adding a failing test gives
  exit 1 and only the `(fail)` line.
- `bun test … --timeout 30000 --reporter=junit --reporter-outfile=…` on `ref`:
  exit 0, 7 pass, 0 fail, and the XML carries all seven `testcase` names with
  `failures="0"`.
- Git-level probe of `--diff-merges=dense-combined --format=%x00%H --name-only`:
  a merge of two branches touching disjoint files names no path; an automatic
  merge of two disjoint hunks in one file names that file, and the result differs
  from both parents; a conflict resolved by taking one parent's content names no
  path; a clean octopus names no path; a hand-built three-parent commit whose
  tree differs from all three parents names the file. The octopus case the
  analyst listed as unverified is therefore covered.
- Read-only probe over the live root board, importing each build's `src/` and
  never touching the live files: base `records=689 done=381 problems=353
  drift=75` in 5502 ms; reference identical counts in 11228 ms; `noflag`
  identical counts in 7916 ms; `diff` of the verdict maps exits 0 for base
  against reference and for reference against `noflag`. Two further alternating
  pairs: base 5896 and 7104 ms, reference 8481 and 8659 ms. The board moved under
  the runs (problems 353 to 354, drift 75 to 76) because another session was
  committing.
- Reading the diff, the range the log walks is guaranteed sound: an earlier guard
  in `completionProblem`, `merge-base --is-ancestor commit HEAD`, already returns
  `receipt is not integrated in code repository`, so `commit..HEAD` can never
  miss a difference caused by a rollback or a sideways checkout. That was the one
  soundness hole this reviewer looked for beyond the fixture and it is closed
  upstream of the new code.
- Not verified by this reviewer: a superproject gitlink bump, a submodule lane, a
  receipt carrying an abbreviated hash, a voucher on a board outside the scanned
  graph, any real `collect` or state transition against a live board, and the
  rewritten Verify block proposed under F8.

Reviewer identity: reviewer-receipt-3 (independent review sub-agent, Opus 5).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (83/100).
Unresolved blocking findings: F8.
Rounds used / remaining: 3 / 2.
Next action: make one bounded revision to Verify block 1 only. Replace the
`(pass)` name gate with a JUnit-report gate over the same seven names plus
`failures="0"`, or convert to a `test` block if the engine committed at claim
time executes one, and add `--timeout 30000`. Show the rewritten block exiting 0
on the reference and 1 on base before publishing it. Change nothing else: the
rule, the flag and the seven tests are settled. Then request round 4.

## Round 4 — 2026-09-19

Presented revision: `specs/spec01.md` revised by analyst-2, bounded to the gate;
`prd.md` unchanged in body and frontmatter since round 1. Judged against prd.ctg
HEAD `ce911ede`. The analyst built on `bdf0370c`; `src/lifecycle.ts` is
byte-identical at both and at the round-2 and round-3 HEADs, so every earlier
round's evidence still describes this code. The live `src/lifecycle.ts` and
`.cartridge/tests/engine.test.ts` still carry another session's uncommitted
edits and were never written to. The analyst's `reference.patch` and
`receipt-drift.test.ts` are byte-identical to round 3's, which confirms the
claim that the rule is untouched and only the gate changed.

| Input | Content digest |
| --- | --- |
| Plan | `prd.md` SHA-256 `0a3a2ea8363f3a3d1b2d01ff812f6df7d255af0ae995f7b6581fe94527387794` (unchanged since round 2) |
| Specs | `specs/spec01.md` SHA-256 `8cc94cee878e5d21d41315998fc87531e5bd7942f8cc54ec80e7a162bcbf66b6` |
| Material contracts/dependencies | `src/lifecycle.ts` at HEAD SHA-256 `177200f02a8cb1c2257c0482f52cafb5ef5e7f160f28ed4835691c4ba9274b11`. Analyst artifacts in the gitignored `.state/loop/receipt-survives/`: `reference.patch` SHA-256 `1f95a0decab6e70f9345d7d0992b22bde83683fceb14c30d69fb520893d751b0`, `receipt-drift.test.ts` SHA-256 `0869941b6de9f0a15b7c31690f6230f6e75481d09682753a1aefa14391ab4018`, both unchanged from round 3. bun 1.3.14, git 2.55.0. Machine load average 27.8 on 10 cores throughout. |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 16 | Unchanged and still accurate. The rule is settled and the scope is one function, one receipt field and one test file. Deduction unchanged: it clears nothing. Over the live root board at 717 records and 398 done, base and the reference produce byte-identical verdict maps, `diff` exiting 0, and the PRD's own evidence case still reports the refusal on both. |
| Ownership and reuse | 19 | Unchanged from rounds 2 and 3. The check stays inside `completionProblem`, reuses `feet`, `codeRepo`, `git` and the `seen` cycle guard, adds no import, and touches one other line in `collect`. This round changed no source at all. |
| Dependencies and implementable slices | 18 | One spec, no needs. `src/lifecycle.ts` is byte-identical at `4e543acc`, `bdf0370c` and today's `ce911ede`, so step 1's rebase offsets still describe the tree the implementer will meet. Step 5's reading of the engine is correct: the committed `verificationBlocks` still matches only `sh`, `bash` and `shell`, so the blocks are right to build the JUnit report themselves. |
| Observable acceptance and baseline evidence | 13 | The seven tests are genuinely discriminating and I reproduced the direction of the analyst's table exactly: block 1 exits 0 on the reference, 1 on base with 2 pass and 5 fail, and 1 on the build without `--diff-merges=dense-combined` with 6 pass and 1 fail, the single failure being the evil-merge test with `Received: null` at line 141. Deductions: the rewritten block still cannot be relied on to pass a correct implementation, failing one reference run in four here (F10), and the Design's steady-state cost bound is wrong by two to three orders of magnitude (F11). |
| Failure, recovery and compatibility | 15 | The rule is strictly weaker than base and I re-confirmed it by measurement rather than by argument: byte-identical verdict maps over 717 records. Two items round 3 left unverified are now closed in the plan's favour — a gitlink bump is named by both of the rule's probes, so the Design's claim about submodules holds, and no done record on the live board has an unresolvable `repo:`, so the new cross-record `codeRepo(other)` call does not turn a verdict into an exception today. Deductions: the 120-second block margin is thinner than the analyst's own figures suggested (F10), and the voucher loop's cost is unbounded in the shape the board is heading for (F11). |
| Reviewer total | 81 / 100 | |

Findings and concrete revisions:

- **F8 (round 3, resolved in direction, not in reliability — see F10).** The
  census no longer depends on stdout and the block now discriminates. Reproduced
  at HEAD `ce911ede` in three clones: `ref4` exits 0 with 7 pass and 0 fail,
  `base4` exits 1 with 2 pass and 5 fail, `noflag4` exits 1 with 6 pass and 1
  fail. The `tests="7" failures="0" skipped="0"` gate and the seven
  `<testcase name="…">` greps all fire as intended.
- **F9 (round 3, resolved as far as a per-test timeout can resolve it).**
  `--timeout 30000` is on both invocations. It is not enough on this machine; see
  F10.
- **Round-3 diagnosis versus round-4 diagnosis.** The evidence supports the
  analyst, not round 3. In four block-1 runs on the reference and one each on
  base and `noflag`, bun printed a `(pass) <name>` line for every passing test,
  in every run, including runs whose output was a plain file — six of six. The
  observed mechanism of failure was the timeout, exactly as the analyst reports:
  the failing reference run shows
  `(fail) a later collected sibling inside the footprint leaves the receipt verified and the parent collects [33532.13ms]`
  followed by `^ this test timed out after 30000ms.` Round 3's attribution to a
  missing `(pass)` line is therefore not reproducible here either, and the spec
  is right to record the timeout as the mechanism while keeping the
  stdout-independent census on the strength of the project's recorded trap. The
  rewritten gate is correct for the reason the spec now gives; that reason is
  just not sufficient, which is F10.
- **F10 (blocking, new; F8's family).** The published proof still fails on a
  correct implementation, now intermittently rather than always, and the block as
  a whole has too little headroom against the engine's hard limit. Four runs of
  block 1 on the reference, each `env -i PATH HOME`, `sh -eu -c`, in the build's
  own checkout, gave exit 1 at 90 s, then exit 0 at 71 s, 89 s and 61 s. The
  failing run is not a different rule or a different build: it is the same `ref4`
  tree that passed three times. Its first test took 33532 ms against the block's
  own `--timeout 30000`, and bun's teardown of the timed-out test then produced a
  second, cascading symptom — `# Unhandled error between tests` reporting
  `parent/cites: source is not an existing Git repository — git failed: fatal: cannot change to '/private/tmp/prd-drift-Myx7vU/code'`,
  which is `afterEach` removing the fixture root while the timed-out test's
  `execute('collect', …)` was still running. So one slow test both fails itself
  and poisons the report. Separately, the engine kills a block at
  `timeout: 120_000` (`src/lifecycle.ts` line 45 at HEAD) and runs each block
  twice, once in the lane and once in `repo`. Block 1 on the reference measured
  61 to 90 s here against that 120 s, and block 1 on base measured 155 s, over it.
  The margin is roughly 30 to 60 s on a machine at load 28, and the plan has two
  independent ways to lose: a single test over 30 s, or the block over 120 s.
  - Revision, bounded and not touching the rule: stop running all seven fixture
    collections in one block. Split Verify block 1 into two blocks that select
    disjoint subsets with `bun test -t`, each writing its own JUnit report and
    each gating on its own subset of names and on `failures="0"`, with the
    `tests="…"` count adjusted per block. That halves both the wall time per
    block and the number of collections competing for the machine, and it costs
    nothing in coverage because the seven names are still all gated. Raising
    `--timeout` alone does not help: it trades a per-test failure for a
    block-timeout failure at 120 s.
  - Whichever shape is chosen, show it exiting 0 on the reference in at least
    four consecutive runs, and 1 on base and on `noflag`, before publishing it.
    Two rounds have now been spent on this gate; a third should not be.
- **F11 (blocking, new).** The Design's steady-state cost bound is wrong, and the
  cost it hides is severe. The spec states that once every receipt carries a
  `base:`, "the added cost is bounded by one memoised `rev-list` per receipt,
  measured at 4.2 ms per spawn on the superproject, so under 1.6 s for a whole
  board once per process". That accounts only for `laneRange`, which is the one
  thing in the new code that is memoised. Reading the reference, `vouches` runs
  per candidate and per `(commit, file)` pair, and before `laneRange` is ever
  consulted it calls `codeRepo(other)` and then `feet(other)`, each of which
  spawns `git rev-parse --show-toplevel` through `repoRoot`; if a candidate
  survives that it calls `completionProblem(other, graph, seen)`, which is not
  memoised at all and is re-entered for the same `other` on every pair and for
  every record of a board sweep.
  - Measured on the live root board with the reference build: `codeRepo` 5.28 ms,
    `feet` 5.53 ms and `completionProblem` 28.00 ms per record, over a 40-record
    sample. The board holds 717 records, 398 done, 390 done leaves, 175 receipts
    of which 0 carry a `base:` today and 163 already satisfy every other voucher
    guard. 83 records report this refusal, and the `git log` the rule runs for
    them yields 1232 `(commit, file)` pairs, the largest single record
    contributing 81.
  - Today all of that is free, because every candidate is rejected by the missing
    40-hex `base:` before any Git work — which is exactly why no round has seen
    it. In steady state each pair scans the graph until a voucher matches, paying
    about 10.8 ms of Git spawns per candidate examined, so a pair costs up to
    390 × 10.8 ms ≈ 4.2 s and the board's 1232 pairs cost minutes to tens of
    minutes per sweep, not 1.6 s. `verifiedStatus` runs this for every record, so
    `prd plan` and `prd status` pay it.
  - Revision, cheap and local: test `laneRange(code, base, tip).has(sha)` — which
    is memoised and spawns nothing after the first call per receipt — before
    `codeRepo(other)` and `feet(other)`, so the two Git spawns run only for the
    handful of candidates whose lane actually contains the commit. Additionally
    memoise `completionProblem` per record for the life of a sweep, or state
    plainly that it is not memoised and what that costs. Either way, replace the
    "under 1.6 s for a whole board" sentence: it is arithmetic over the wrong
    term and the spec should not publish it as a bound.
- **F12 (non-blocking, closed in the plan's favour).** A gitlink bump behaves like
  any other changed path, so the Design's submodule paragraph is correct. In a
  purpose-built superproject, `git diff --name-only <base> -- web.ctg` prints
  `web.ctg`, and
  `git log --full-history --no-renames --diff-merges=dense-combined --format=%x00%H --name-only <base>..HEAD -- web.ctg`
  prints the bumping commit followed by `web.ctg`. Nothing to revise; recorded so
  the next reader need not re-derive it.
- **F13 (non-blocking, closed in the plan's favour).** The new code calls
  `codeRepo(other)` for records other than the one being judged, so a single done
  record naming a repository that no longer exists would turn an unrelated
  record's verdict into a thrown exception during a single-record `collect`. On
  the live board this does not bite: of 398 done records, 0 have an unresolvable
  `repo:`, and the full sweep threw 0 times on both builds. Worth knowing given
  this repository's history of submodule renames and drops, but not a finding
  against this plan.
- **F7 (round 2, resolved).** The softened wording matches what I see. Over the
  live board the reference swept 717 records in 9068 ms against base's 17297 ms —
  the reference was faster in my pair, the reverse of round 3's direction, which
  is what "under load the difference disappears into a spread" predicts. The
  spec's framing is now honest about this. Note that this figure measures the
  inert migration, not steady state; see F11.

Disposition: revise.

Validation. All probes ran in `git clone --local` copies of `prd.ctg` at HEAD
`ce911ede` under `$TMPDIR/reviewer-receipt-4/`, with `node_modules` copied in and
the analyst's `receipt-drift.test.ts` added: `base4` (HEAD only), `ref4` (HEAD
plus `reference.patch`) and `noflag4` (`ref4` with only
`'--diff-merges=dense-combined', ` deleted, `diff` confirming the builds differ in
that one line). Every command ran under `env -u CARTRIDGE_YOLO`. Nothing was
written to the live checkout except this file, no daemon was started, and the
scratch directory was removed afterwards.

- Verify blocks extracted from the published spec with the committed
  `verificationBlocks`: `blocks 2`, and a grep for `cd `, `/Users/` and `cargo`
  over both blocks found none.
- Block 1, run as the engine does (`sh -eu -c` on the extracted string) under
  `env -i PATH HOME`, in each build's checkout: `ref4` exit 1 in 90 s, then exit 0
  in 71 s, 89 s and 61 s; `base4` exit 1 in 155 s with 2 pass and 5 fail;
  `noflag4` exit 1 in 107 s with 6 pass and 1 fail, the evil-merge test with
  `Expected: "verified source footprint changed after collection"` and
  `Received: null` at line 141.
- The failing `ref4` run's log: 6 pass, 1 fail, 1 error;
  `(fail) a later collected sibling … [33532.13ms]` with
  `^ this test timed out after 30000ms.`, and an `Unhandled error between tests`
  naming the removed fixture root.
- Read-only probe over the live root board, importing each build's `src/` and
  writing nothing: `ref4` `scanMs=261 sweepMs=9068 records=717 done=398
  problems=681 drift=83 threw=0`; `base4` identical counts at `sweepMs=17297`;
  `diff` of the two verdict maps exits 0. `doneRecordsWithUnresolvableRepo=0`.
  `receipts=175 withBase=0 doneLeafReceiptsWithExit0=163`.
  `driftRecords=83 pairsTotal=1232 maxPairs=81 graphSize=717`.
- Per-candidate cost probe on the live board with the reference build, 40-record
  sample: `codeRepo=5.28ms feet=5.53ms completionProblem=28.00ms`,
  `doneLeaves=390`.
- Gitlink probe in a purpose-built superproject and submodule: both the rule's
  `git diff --name-only` and its `git log … --diff-merges=dense-combined
  --name-only` name the submodule path for a gitlink bump.
- Not verified by this reviewer: a submodule lane, an abbreviated-hash receipt, a
  voucher on a board outside the scanned graph, any real `collect` or state
  transition against a live board, and a direct measurement of steady state with
  receipts actually carrying `base:` — F11's figure is a measured per-candidate
  cost multiplied by a measured candidate and pair count, not an end-to-end
  timing.

Reviewer identity: reviewer-receipt-4 (independent review sub-agent, Opus 5).
User rating: not supplied.
User feedback/provenance: none for this revision.
Result: FAIL (81/100).
Unresolved blocking findings: F10, F11.
Rounds used / remaining: 4 / 1.
Next action: one round remains and it cannot honestly close both findings. F10 is
closable in it: splitting Verify block 1 into two `bun test -t` blocks is a
bounded edit to the spec's Verify section, touches no source, and can be shown
passing four times on the reference and failing on base and `noflag` within the
round. F11 is not, because its remedy — reordering the `laneRange` test ahead of
`codeRepo(other)` and `feet(other)`, and memoising the recursive
`completionProblem` — changes the rule's own code, which would re-open the
reference, the seven tests and every measurement rounds 2 to 4 rest on, in the
last available round and with no round left to review the result. Recommended
disposition: spend round 5 on F10 alone and on correcting the Design's
steady-state sentence to say that the cost is not bounded by `laneRange` and is
unmeasured, then take F11 to the user as its own PRD against the same function,
alongside the lane-branch defect the spec already carries in Remaining limits. If
the user would rather not land a rule whose cost grows as receipts accumulate
`base:`, this PRD should go to them now rather than consume its last round.

## Round 5 — 2026-09-19 — explicit re-verification

Independent reviewer: /root. Result: PASS, 91/100. Scope 19, ownership 19, boundaries 18, acceptance 18, recovery 17. No blocking plan findings.

- prd.md: SHA-256 `31cc876a206df0c97043f67dc714a39211e69fe20cb195da0430563385a08838`.
- specs/spec01.md: SHA-256 `a65536f050e2cbfd995f921f3d81dd2e418be06ede61eb4621bbc36db98f51ae`.

The reviewer read the full current contract, canonical record, four predecessor
rounds and lifecycle source. Explicit committed-target verification plus immutable
receipt history avoids prior automatic-voucher risks. Lane fast-forward may still
refuse dirty README/help overlap; preserve that refusal and require scoped
integration reconciliation, never silently include dirty tails. Parent rollups
must distinguish committed and workspace evidence. Named tests must actually run
within the existing 120-second block budget. A separately reviewed and verified
necessary source baseline must precede specced and implementation claim.

Rounds used / remaining: 5 / 0. Substantive revisions require escalation; no
review-history reset. User authorization: “Authorize the minimal lifecycle
prerequisite fix.” No implementation has occurred at this review.

## Extra-round authorization — 2026-09-19

The user authorized one additional review round, round 6, for the bounded
verification amendment. This does not reset or discard rounds 1–5. The amendment
adds frozen dependency setup and separates clean-candidate fixture/migration
checks from the unchanged full live-dataset records audit. No source behavior,
source footprint or named regression was removed. Round 6 remains pending.

## Round 6 — 2026-09-19 — authorized verification amendment

Independent reviewer: /root. Result: PASS, 92/100. Scope 19, ownership 19,
boundaries 18, acceptance 19, recovery 17. No blocking findings. The reviewer
read the full amended contract; the user explicitly authorized this sixth round.
Rounds used / remaining: 6 / 0. Prior rounds and their decisions remain intact.

- prd.md SHA-256: `dbf628d312f4cff8108babb82e6c70b62702cd9e8a91a5c7eaeb528f335236bb`.
- specs/spec01.md SHA-256: `8bbfa1fb0df0fa64bec8bb1275cac673463f2ceb725811866ac35d50daace6cb`.

The independently executed current named regression suite passed all eight
tests and 87 assertions in 34.60 seconds. Log:
`/tmp/memory-stack-lifecycle-independent.log`. Canonical live-record validation
with matching code hashes, pinned dataset evidence and final code checks remains
required before collection. Source is frozen during those checks. This round
approves the bounded verification-data amendment; it does not claim the committed
global board dataset is complete or authorize unrelated record changes.
