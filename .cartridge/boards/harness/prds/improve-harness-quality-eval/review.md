# Measure multi-round context quality with real task outcomes — review

Canonical PRD: [@harness/improve-harness-quality-eval](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-harness-quality-eval](../../../root/reviews/round-1/improve-harness-quality-eval.md): reviewer 91/100; Keep. Good adversarial and three-round replay coverage; share the long-horizon corpus and keep live-model results distinct from offline gates.
  Original SHA-256: `16da9d3db4fa4bbf2679b61865bd044d685d06b7b0bebe615e20490dce7ab4bc`.
- [long-horizon-recall-benchmark](../../../root/reviews/round-1/long-horizon-recall-benchmark.md): reviewer 82/100; Merge. Merge corpus ownership with harness quality evaluation; freeze dataset/license, per-ability metrics, abstention scoring and model/fixture distinction before runs.
  Original SHA-256: `57458fd6c5de067e9eda2ff13e286cf0138607079be1c99f05f1fda7828a0c6c`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 19 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reconciliation verdict: **REBASE**. Evidence: `eval/eval_compaction.py` deleted in harness 2364a43 ("Keep cartridge records, routines and tests under .cartridge") under decision `cartridge-repositories-keep-records-and-executable-memos` (no Python); corpus retained at `harness.ctg/.cartridge/tests/eval/corpus` (journals v1–v3, `facts.json`, `summaries/manifest.json` with good rounds 1–3 and four adversarial classes) but no test references it (rg); `src/compaction.rs` `comparisons` delivered by `@harness/improve-harness-compaction-diff` (done, a282c87). Pre-revision text (SHA-256 `0d415ffb73210ca4e820e5ffc1d96aef8112aeb9dae45ed7fd1845ffb2029376`) had all five footprint paths missing, broken links, a recovery statement formatted as acceptance, and did not carry the inherited long-horizon findings (licence, per-ability metrics, abstention). Blocking.

Revision reviewed: `prd.md` SHA-256 `8b4f48665bcae1d7bb77457a1cefe825ed59dc4b80ecb41387f32c2a13373a34` (working tree). Changes: baseline stated; offline Rust test over the existing corpus in the existing compaction unit entry point; broken-checker negative; abstention/unknown and licence; opt-in live report with task-outcome replay; real footprint and gate.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Restores a missing check over an existing corpus; -1 live task-success scoring rubric still to be defined. |
| Ownership and reuse | 19 | Harness-owned, reuses corpus and `compaction::comparisons`; -1 `inspection.rs` in footprint may be unnecessary. |
| Dependencies and implementable slices | 19 | Only need done; ready; -1 offline and live parts could split if the live report grows. |
| Observable acceptance and baseline evidence | 18 | Per-class expectations from the manifest, negative control, baseline command; -2 licence source for the corpus unknown until probed. |
| Failure, recovery and compatibility | 18 | Additive, live run excluded from gate, bounded budget; -2 no statement on live-run cancellation/partial report. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of repo, source, test and doc paths (ls/rg); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke` and `.cartridge/memos/routine/cartridge-development.md` accepts the named owners; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: ready to claim; record `just test harness` baseline first.
