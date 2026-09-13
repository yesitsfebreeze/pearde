# Inspect what each compaction retained and removed — review

Canonical PRD: [@harness/improve-harness-compaction-diff](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-harness-compaction-diff](../../../root/reviews/round-1/improve-harness-compaction-diff.md): reviewer 92/100; Keep. Exact covered-prefix identity and no-model inspection are well bounded; preserve prior summary on failure.
  Original SHA-256: `add758653da64abf6e583c03ad3b3058b971eab8bff0cae09c98187cd6ae52c2`.

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
Baseline 2364a432 passes existing harness tests. Extending its real-process
rolling-memory test to require two comparisons fails with “inspection must
retain both compaction comparisons”: write_summary replaces one plain summary.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 20 | Missing comparison reproduced after two actual compactions. |
| Ownership and reuse | 19 | Existing summary buffer and canonical transcript; no parallel journal. |
| Dependencies and slices | 19 | Additive owner-local storage/inspection; existing RPC fixture. |
| Acceptance and baseline | 19 | Exact prefixes/tails, corrected constraint, legacy and altered-source cases. |
| Failure and compatibility | 19 | One history write after success, allowlisted usage, zero-router inspection. |

**96/100 — PASS**, no blocking findings, 3/5 rounds used. Full historical
comparison size grows with the number of summaries, consistent with this
inspector's existing complete-transcript source view; no silent history eviction.
