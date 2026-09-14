# Harness builds model context from the shared landscape result — review

Canonical PRD: [@harness/harness-consumes-landscape](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [harness-consumes-landscape](../../../root/reviews/round-1/harness-consumes-landscape.md): reviewer 91/100; Keep. Good authority, transcript, budget and rollback boundaries; reuse the existing compaction evaluation leaves and baseline instead of another corpus.
  Original SHA-256: `9cdc028bb0f5ec3ad80842228362e76c2b093cbdfe96dd05abd116d3f5076bf7`.

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

Reconciliation verdict: **REBASE**. Evidence: decision `.cartridge/memos/decision/the-fabric-lives-in-core.md` (landscape dissolved; evidence contract in core, snapshot served by memo); `memo.ctg/src/context.rs` serves `{op:"context"}`; `proxy.ctg/src/service.rs` already prepares it; `harness.ctg/src/roster.rs` uses `evidence` only for roster; harness ported to transport (harness 68cf9fd, 336f2d1). Pre-revision text (SHA-256 `6f0329999d91cf56cb487114b3a0cfbdd263269a0f9b06886106144495c97b55`, prd.ctg 077e57a2) named five footprint paths that no longer exist (`harness.ctg/main.rs`, `inspection.rs`, `working.rs`, `eval`, `tests`; source is now `src/`, tests `.cartridge/tests/`), relative links resolving to `boards/`, an unqualified root need and the whole landscape quality rollup as prerequisite. Those were blocking.

Revision reviewed: `prd.md` SHA-256 `2e8aa173f820ed542b3c990eafd2b03b2f74d62a3f10211b9100e800c0633432` (working tree, uncommitted). Changes: rebased on memo snapshot and core evidence; footprint to real paths; needs qualified to `@root/memory-document-works-end-to-end` and narrowed to `@landscape/context-quality-is-measured/context-comparison-gate`; fallback to `memo {op:"system"}` made an acceptance item; gate and baseline named.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One outcome (harness adapts the shared snapshot) with explicit exclusions; -2 value deferred behind two open needs. |
| Ownership and reuse | 19 | Harness-only footprint, existing `memo` need, reuses proxy's snapshot path and existing tests; -1 comparison-gate leaf still describes the dissolved library. |
| Dependencies and implementable slices | 17 | Both needs resolve in the root graph, acyclic; -3 both open and the gate leaf itself is stale-after-migration. |
| Observable acceptance and baseline evidence | 18 | Four observable checks, first probe and `just test harness` gate; -2 "same selected rows" equivalence fixture still to be specified. |
| Failure, recovery and compatibility | 18 | Unavailable/timeout fallback, compaction fault cases, no transcript rewrite; -2 no explicit cancellation behaviour for an in-flight snapshot. |
| Reviewer total | 90 / 100 | |

Result: **PASS** (agent score 90, threshold 90).
Findings: rebase complete; the landscape board's comparison-gate leaf must itself be rebased onto core fabric before this leaf becomes ready (coordinator, other board).
Unresolved blocking findings: none.
Validation: existence checks of repo, source, test and doc paths (ls/rg); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke` and `.cartridge/memos/routine/cartridge-development.md` accepts the named owners; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated). 
Rounds used / remaining: 3 / 2.
Next action: wait for both needs; then probe `build_context` vs proxy snapshot.
