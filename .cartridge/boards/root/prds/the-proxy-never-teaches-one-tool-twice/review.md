# @root/the-proxy-never-teaches-one-tool-twice review history

Plan: `@root/the-proxy-never-teaches-one-tool-twice`, `prd.ctg/.cartridge/boards/root/prds/the-proxy-never-teaches-one-tool-twice/prd.md`.
Scope: executable leaf — one observable outcome (each cartridge tool reaches the
model exactly once; a caller's namespaced copy replaces the injection). The work
is already landed; `specs/spec01.md` exists to reprove the five ticked
acceptance boxes from observed evidence rather than a previous session's word.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: records repo `/Users/feb/dev/cartridge` at `120037d`, moving
to `76c3b8b` during the round (other sessions committing). Source repo for the
footprint is the `proxy.ctg` submodule, at `132f458` with 9 modified + 1
untracked path when the round began; those paths were committed by their owner
as `04b64eb` during the round, so the tree every measurement below ran against
is now exactly `proxy.ctg` HEAD `04b64eb`, which the superproject gitlink pins.
The spec's stated base `0692c18` is two commits behind that; the skip logic at
`src/service.rs:629-639` is unchanged across all three.

| Input | Content digest |
| --- | --- |
| Plan | `prds/the-proxy-never-teaches-one-tool-twice/prd.md` — SHA-256 `032999e8666aaaebd8bcb813e40c537ec4ca172701d8383247f121b9765a6026` |
| Specs | `specs/spec01.md` — SHA-256 `b8fbdf8508dcba92ff01289af2325066ce2752b4047b86ae026610af09e2c112` |
| Material contracts/dependencies | `prd.ctg/src/lifecycle.ts` (collect/verify: `:39-49`, `:125`, `:164-171`, `:225`); `proxy.ctg/src/service.rs` @ working tree (`:589-600`, `:629-639`, `:647`, `:759`, `:809`, `:823`, `:864`, `:899`, `:908`); `proxy.ctg/.cartridge/tests/unit/tests.rs:318-410`; `proxy.ctg/.cartridge/docs/README.md:52-58` |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Right purpose and nothing more: no new behaviour, no new repo files, footprint is exactly the three paths the PRD already owns, and every block reruns a claim instead of restating it. Deducted for leaving the record it certifies internally inconsistent — the PRD still says "51 tests" while the spec asserts a floor of 55 and the tree runs 57. |
| Ownership and reuse | 16 | Reuses the shipped test, the shipped suite and the shipped README paragraph; touches nothing in the footprint; keeps the repo clean by patching an out-of-tree copy. Deducted because the copy-and-patch machinery only exists to honour the *analyst's* read-only constraint: an implementer may edit `.cartridge/tests/unit/tests.rs`, which is already in the footprint, so the two missing assertions belong there and block 2 could collapse into a plain `cargo test`. |
| Dependencies and implementable slices | 16 | The load-bearing "collect without a lane" decision is correct and I re-derived it: `lifecycle.ts:125` picks the lane as `tree` when it exists, `:225` makes a lane by plain `git worktree add` on the superproject (submodules empty), and `:164` only reruns pass 2 in `repo` when `candidate !== initialHead`, which a lane where nothing can change never reaches. Both blocks exit 1 with the intended message in an empty `proxy.ctg/` (observed) instead of passing vacuously. Deducted for a stale base: the spec says the submodule HEAD is `0692c18`; it is `132f458`, which is also the gitlink the receipt will pin, and the spec names it nowhere. |
| Observable acceptance and baseline evidence | 13 | The blocks have real teeth where they reach — I re-derived control A (skip disabled → the named test FAILS on the duplicate-name assertion) and control C for *both* inserted assertions (each inversion FAILS, so both are reached and evaluated), the anchor check is robust (reworded anchor → block 2 exits 1, no silent no-op), and the inserted absences are non-vacuous because `granted_dispatches_land_in_the_observation_journal_with_caller_and_turn` proves the same fixture records exactly two `memo`/`observe` calls and a `policy` round when a dispatch does happen. Deducted heavily for finding B1: a mutation that drops `ends_with` — so any caller tool name longer than `cartridge__<name>` suppresses that injection — passes all 57 tests and both blocks, leaving acceptance box 1's second half ("tools without a namespaced caller copy are still injected") with no check that fails when it is false. |
| Failure, recovery and compatibility | 15 | Refusing loudly in an empty submodule rather than skipping politely is the right trade and is verified; no block writes inside the footprint; the temp copy is removed; the cold cost from an empty `CARGO_TARGET_DIR` is 17 s against the engine's 120 s cap; the test floor (`>= 55`, `0 failed`) survives sibling sessions adding tests. Deducted because block 1 makes this record hostage to a whole suite in a tree carrying ten dirty paths owned by nobody on this board, and the receipt records no identity for the tree it actually tested. |
| Reviewer total | 77 / 100 | Strong on the hard parts (lane analysis, anchor robustness, negative controls); fails on the one thing the spec exists for — one of the five ticks is still unproven. |

Findings and concrete revisions:

- **B1 (blocking) — box 1's "still injected" half has no teeth.** Replacing
  `.any(|caller| caller.len() > public.len() && caller.ends_with(&public))`
  with `.any(|caller| caller.len() > public.len())` makes every cartridge tool
  disappear for any caller that ships a longer tool name (a real MCP client's
  `mcp__linear__create_issue`), and the full suite still reports
  `57 passed; 0 failed`, so both blocks pass. The fixture has exactly one
  injectable tool and the test replaces the caller's tool list with the
  namespaced copy, so nothing observes a descriptor surviving the filter.
  Remedy, proven here: an unrelated namespaced caller tool must leave the
  injection in place — with `body["tools"]` set to
  `mcp__cartridge__read` only, assert the forwarded list still contains
  `cartridge__memo`. That test passes on the shipped code and FAILS under the
  mutation above (both runs observed). Put it in
  `.cartridge/tests/unit/tests.rs` (in the footprint) rather than in another
  awk patch, and add a PRD-box-1 acceptance clause naming it.
- **B2 (blocking) — the record's own count is false.** Acceptance box 5 says
  "the proxy unit suite passes (51 tests)"; the suite the collection will run
  reports 57, and the spec's box 1 asserts a floor of 55. Asked whether the box
  needs rewording: **yes.** Keep the floor in the block (an exact number breaks
  the moment a sibling session adds a test) and reword the PRD box to the
  measured shape, e.g. "the proxy unit suite passes with no failures (57 at
  `132f458`; the spec pins a floor of 55 because sibling sessions add tests)".
  Collecting a tick whose parenthetical is measurably wrong is exactly the
  "previous session's word" this spec exists to replace.
- N1 — "Base and dependencies" states the submodule HEAD is `0692c18`. It was
  `132f458` when the round began (one README-only commit; all three footprint
  paths byte-identical) and is `04b64eb` now, the sibling session having
  committed the paths the spec calls "dirty". Name the current commit and say it
  is the gitlink the superproject HEAD pins; also drop or restate the paragraph
  about ten dirty paths, which no longer describes the tree.
- N2 — the receipt will name the superproject HEAD while the blocks compile a
  dirty working tree whose identity is recorded nowhere. Add
  `git -C proxy.ctg rev-parse HEAD` and
  `git -C proxy.ctg status --porcelain -- src .cartridge` to block 1 so the
  evidence says which tree it ran against.
- N3 — the laziest correct plan is smaller: move the two absence assertions
  (and B1's test) into `.cartridge/tests/unit/tests.rs`, which the PRD already
  owns, and block 2's temp dir, `cp`, `ln -s ../memo.ctg` and awk patch all
  disappear into block 1's `cargo test`. The out-of-tree copy exists only
  because the analyst was forbidden to edit; the implementer is not.
- N4 — the spec says "collect without a lane" but not how a lane appears:
  `prd claim` on a `specced` PRD creates one (`lifecycle.ts:225`). Say
  explicitly: collect straight from `specced`, do not claim.
- N5 — the non-vacuity of block 2's two absences rests on a neighbouring test
  (`granted_dispatches_land_in_the_observation_journal_with_caller_and_turn`,
  `tests.rs:318`) that block 1 runs as part of the suite. Name it; a reader
  cannot otherwise tell the absences are not trivially true.
- N6 — block 1's whole-suite `0 failed` means an unrelated red test in another
  session's dirty work blocks this collection. Acceptable (box 5 demands the
  suite) but the recovery belongs in the spec: rerun once the sibling's tree is
  green; nothing here can be fixed by this PRD's owner.

Disposition: revise (keep the spec's structure; it is close).

Validation (all foreground, `sh -eu -c`, `CARGO_TARGET_DIR` in private scratch):

| cwd | command | result |
| --- | --- | --- |
| `/Users/feb/dev/cartridge` | spec block 1 verbatim, empty target dir | exit 0, `57 passed; 0 failed`, 17 s cold |
| `/Users/feb/dev/cartridge` | spec block 2 verbatim | exit 0, `1 passed; 0 failed`, 4 s |
| empty `proxy.ctg/` dir | spec block 1 / block 2 | exit 1 / exit 1, "collect this PRD without a lane" |
| scratch copy | control A: skip condition `false && …` | named test FAILED (`the namespaced copy must replace the injected one`) |
| scratch copy | control C: invert inserted `policy` absence | test FAILED |
| scratch copy | control C: invert inserted `observe` absence | test FAILED |
| scratch copy | control D: anchor comment reworded | block 2 exit 1 (no silent no-op) |
| scratch copy | control E: drop `ends_with` from the skip condition | **full suite `57 passed; 0 failed`** — B1 |
| scratch copy | proposed `an_unrelated_namespaced_caller_tool_does_not_suppress_injection` | passes shipped code, FAILS under control E |
| `/Users/feb/dev/cartridge` | `git status --porcelain -- proxy.ctg/src/service.rs …` | exit 0, empty (submodule invisible to the superproject scan) |

Reviewer identity: `reviewer-1 (round 1)`, independent of the analyst that wrote the spec.
User rating: not required under delegation; none supplied.
User feedback/provenance: none for this revision.
Result: FAIL (77/100).
Unresolved blocking findings: B1 (box 1's "still injected" half survives a
passing mutation), B2 (acceptance box 5's "51 tests" is false; reword it).
Rounds used / remaining: 1 / 4.
Next action: bounded revision — add the discriminating check for B1 (preferably
in `tests.rs`), reword box 5, correct the base to `132f458`, then re-review.
