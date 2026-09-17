# @memory/a-retention-probe-measures-the-half-life-of-a-stored-fact-per-claim-kind review history

Plan: @memory/a-retention-probe-measures-the-half-life-of-a-stored-fact-per-claim-kind, prd.ctg/.cartridge/boards/memory/prds/a-retention-probe-measures-the-half-life-of-a-stored-fact-per-claim-kind.
Scope: one runnable retention eval (`just eval-retention`) on the mature fixture, plus a dated RESULTS.md section.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer; user-delegated ratings.
Inherited rounds: none.

Use the shared [review method](../../workflows/review-plan.md) in the root board.
Replace placeholders with observed evidence; a blank score is pending, not zero.
Append rounds and feedback without overwriting prior results.

## Round 1 — 2026-09-17

Presented revision: PRD e266de07e89d38446e6cabf51ee99aa1801e73d7b12614721149ac396c2a2685 (analyzing, claim coordinator-ea-3); memory.ctg source HEAD 1351865eb0e787cf819456aaa201c18eacf74406; specs/spec01.md published from analyst-1 (verdict SPECCED).

| Input | Content digest |
| --- | --- |
| Plan | prd.md e266de07e89d38446e6cabf51ee99aa1801e73d7b12614721149ac396c2a2685 |
| Specs | specs/spec01.md (published; digest not recomputed this round — reviewed at the revision presented to the reviewer) |
| Material contracts/dependencies | memory.ctg f808262-era checkout at HEAD 1351865e (src/graph/src/heat.rs, src/tick/src/tick_stigmergy.rs, src/base/src/base_retention.rs, .cartridge/tests/integration/bench/*) |

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Concrete unmeasured retention question on the existing mature fixture, limited to one runnable eval and one dated RESULTS.md decision section. |
| Ownership and reuse | 18 | Owned by memory.ctg; reuses memory-bench, common write_report/cache plumbing, GraphGnn, retrieval::query::query, tick::tick_stigmergy::run_gc, with minor uncertainty on how much replay internals must be exposed or copied. |
| Dependencies and implementable slices | 18 | Names base HEAD, dirty-checkout constraint, expected crate deps, files to change, stepwise path; the retention runner is one mid-sized slice rather than several independently landable slices. |
| Observable acceptance and baseline evidence | 18 | Requires rows for all built-in claim kinds plus unlabelled, both retrieval variants, rank-at-10/tier cells, cache repeatability, RESULTS.md provenance; analyst's mature-fixture smoke test (exit 0) is baseline evidence; collect-time proof does not itself prove the real non-fake report contents. |
| Failure, recovery and compatibility | 18 | Runs without a daemon, --fake-llm only for plumbing, isolated CARGO_TARGET_DIR, no footprint writes in Verify, preserves unrelated dirty work, exercises production GC spill policy; recovery guidance implicit through cache refusal/reuse and temporary report dirs. |
| Reviewer total | 91/100 | PASS |

Findings and concrete revisions: non-blocking — (1) the span grid and unrelated-document count are left to the implementer; acceptable because the spec requires them fixed before measurement and recorded in RESULTS.md; the implementer must choose them before observing real scores. (2) The Verify block checks fake-LLM determinism and report shape; the dated RESULTS.md acceptance still depends on a real cached eval run that is not encoded as a collect-time gate.
Disposition: keep.
Validation: independent reviewer agent read the PRD, published spec01.md and memory.ctg source at HEAD 1351865e; full report at prd.ctg/.cartridge/boards/memory/.state/loop/a-retention-probe-measures-the-half-life-of-a-stored-fact-per-claim-kind/reviewer-1.md.
Reviewer identity: background reviewer agent (reviewer-1), dispatched by coordinator cartridge-8e.
User rating: not required under delegation; not supplied.
User feedback/provenance: none this round.
Result: PASS.
Unresolved blocking findings: none.
Rounds used / remaining: 1 / 4.
Next action: proceed — run `prd specced` and dispatch the implementer.