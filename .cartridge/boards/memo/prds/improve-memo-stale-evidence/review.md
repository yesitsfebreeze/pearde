# Distinguish stale source references from current guidance — review

Canonical PRD: [@memo/improve-memo-stale-evidence](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-memo-stale-evidence](../../../root/reviews/round-1/improve-memo-stale-evidence.md): reviewer 90/100; Keep. Clear changed-target and historical-evidence rules; reuse the ranking corpus and retain caller-reported attribution.
  Original SHA-256: `cb9f99eb93ef792b30ae3fa7d8ec3245f4c981e0da6fc84680e0fd119f29272c`.

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

## Round 3 — 2026-09-13

Reviewer: Codex `/root`, self-review under session delegation policy.
Inputs: [review-round-3-inputs.json](review-round-3-inputs.json).
Baseline: the 45-test memo suite passes, including a source whose digest changes
and a missing target whose descriptor stays readable. Inspection of usage.rs
shows missing search hits contain only path/error and changed targets return a
new digest without a recorded comparison. An optional explicit baseline makes
comparison meaningful; unrecorded targets cannot be called unchanged. Preserve
legacy response fields, exact-read errors and observational attribution.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Explain missing/changed references without declaring historical guidance obsolete. |
| Ownership and reuse | 20 | Existing resource identity, hash limits and discovery problems reused. |
| Dependencies and slices | 19 | Three memo files, no additional journal or source mutation. |
| Acceptance and baseline | 19 | Changed/renamed file fixture, descriptor and journal immutability, malformed digests. |
| Failure and compatibility | 19 | Optional baseline, additive fields, exact missing behavior and caller attribution preserved. |

**96/100 — PASS**, no blocking findings, 3/5 rounds used. Matching bytes do not
establish current guidance. Use direct-checkout collection for sibling Cargo paths.

Validation: `just test memo` passes all 48 tests. New fixtures check unrecorded,
matching, changed and renamed/missing sources; preserve descriptor text and
revision; reject malformed baselines; retain exact missing errors and explicit
caller-report attribution. A current routine and completed work are separately
retrieved without changing either record. Existing source-boundary, symlink,
cancellation and journal tests remain green. Checkbox changes record proof only.
