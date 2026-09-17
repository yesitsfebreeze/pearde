# @memory/the-memory-engine-tests-do-not-depend-on-which-test-ran-before-them review history

Plan: @memory/the-memory-engine-tests-do-not-depend-on-which-test-ran-before-them, prd.ctg/.cartridge/boards/memory/prds/the-memory-engine-tests-do-not-depend-on-which-test-ran-before-them.
Scope: one observable outcome — `cargo test -p memory_cartridge --lib` passes from a clean checkout regardless of test order or thread count, with the shutdown-refusal assertion preserved.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../workflows/review-plan.md) in the root board.
When copying this template, resolve that link relative to the actual owner board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results. This review record
does not replace the work item's Pearde or memo implementation status.

## Round 1 — 2026-09-17

Presented revision: PRD db858cfb4c3b68c37f607f85d76c840e6e09e817422d8065a6ba1eec1f9e0974; memory.ctg source HEAD 1351865eb0e787cf819456aaa201c18eacf74406; spec01 published from analyst-1 with the validated attempt diff `attempt-engine-test-serialize-and-relatch.diff`.

| Input | Content digest |
| --- | --- |
| Plan | prd.md db858cfb... (bound revision) |
| Specs | specs/spec01.md, reviewed at the presented revision with the attempt diff applied against base 1351865 |
| Material contracts/dependencies | src/cartridge/src/lib.rs, src/commands/src/memory.rs, src/util/src/lifecycle.rs, src/llm/src/llm.rs, .cartridge/tests/unit/src/cartridge/engine_test.rs at 1351865 |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One concrete outcome (order-independent engine suite from a clean checkout) with the PRD's own failure evidence reproduced at base (101 parallel, 101 serial, both signatures named). |
| Ownership and reuse | 19 | Only engine_test.rs changes; reuses the existing test protocol (`shutting_down_for_tests()` + `ShutdownForTests::drop`) that other test files already use rather than inventing new lifecycle API. |
| Dependencies and implementable slices | 19 | Single-file validated diff, no footprint change, no Cargo.toml touch; the attempt diff applies cleanly at the bound base and at live HEAD (no named file moved). |
| Observable acceptance and baseline evidence | 19 | Red/green bracket observed: three suite shapes red at 1351865, all green with the fix, five consecutive full-suite runs green; 21-test census pin verified correct. |
| Failure, recovery and compatibility | 18 | The relatch cannot be blocked from outside the four serialized engine tests; the Elapsed(()) write-preferring-lock account is inferred rather than runtime-traced, but the fix removes both failure pathways. |
| Reviewer total | 94/100 | PASS |

Findings and concrete revisions: non-blocking — the spec's "ten other test files" count is actually six write-protocol callers plus one read-side user; the footprint names `lifecycle.rs` though it needs no change; the Elapsed(()) mechanism account is inferred (flagged, and the fix removes the pathway). No blocking findings.
Disposition: keep.
Validation: independent reviewer verified all spec line citations exact at the bound revision and the attempt diff's clean application; full report at prd.ctg/.cartridge/boards/memory/.state/loop/the-memory-engine-tests-do-not-depend-on-which-test-ran-before-them/reviewer-1.md.
Reviewer identity: background reviewer agent (reviewer-1), dispatched by coordinator cartridge-8e.
User rating: not required under delegation; not supplied.
User feedback/provenance: none this round.
Result: PASS.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed — run `prd specced` and dispatch the implementer in a lane.