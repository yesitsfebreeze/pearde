# A descendant edit refreshes only its derived rows — review

Canonical PRD: [@landscape/recursive-development-graph/recursive-source-refresh](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [recursive-development-graph](../../../../root/reviews/round-1/recursive-development-graph.md): reviewer 91/100; Keep. Strong identity, traversal and inactive-source checks; turn depth/count/byte bounds and cursor invalidation into explicit fixture parameters during analysis.
  Original SHA-256: `7c6fda62b070e70f1ce2276761ad99be78c275d6c4b87a0762184791c893534b`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.

Reconciliation verdict: **DELIVERED**. Aligned with the parent's REBASE to owner memo. The outcome exists in memo's native source search on the route taken (memo.ctg `83bf1ad`, identical on main and ws branch `transport`).
- **No derived rows to go stale.** Search derives nothing durable: every query re-runs the census and owner indexes (`src/sources/search.rs`, `src/source_search.rs`), and the integration test asserts no `.cartridge/.state` is created.
- **Acceptance 1 (edited child facts appear on the next fresh query).** `.cartridge/tests/integration/source-search.test.ts` edits `plugin/.cartridge/documents/same.jd` (CHILDBERYL -> NEWQUARTZ); the next query returns exactly one NEWQUARTZ hit, and the earlier result object is unchanged.
- **Acceptance 2 (a moved or removed source invalidates its stale reference explicitly).** Exact readback of the old reference returns `changed`. `read_until` (`src/sources/search.rs`) returns `Changed` when the owner's census `source_revision` moved (an edit, move or removal changes it) and `Unavailable` when the owner row is gone. A forged or merged path reference is `malformed`, and a wrong owner is `invalid_reference`.
- **Acceptance 3 (no provider restarts, records never copied or deleted).** Search only reads through owner indexes and never starts providers. The test compares a byte snapshot of the whole fixture tree before and after, including symlinks.

Change: frontmatter only. `repo` `cartridge.ctg` -> `memo.ctg`, `capability-owner` `landscape` -> `memo` (matching the parent's rebase), review-round, review-status. The body is unchanged.
Presented revision: `prd.md` SHA-256 `c2cc6d43593a3ed9669f8427fab9d4122970c3cd870301a49547d7bfd8da3104`. Before: `e8cf898895a4e8261c4588eed2af87ab0e0582326b2e812ecdec440f0a766430`.

Agent score: not scored (delivered-pending-verification).
Findings: (1) The body still cites `landscape.ctg/src/lib.rs`, `surface.rs` and `just test landscape`, which no longer exist. Verify with `just test memo` and `bun test memo.ctg/.cartridge/tests/integration/source-search.test.ts` instead. (2) No test reads a reference after the source file is *deleted*. The `Unavailable`/`Changed` branches come from source reading; a one-line deletion case in the existing test would close this. (3) The need `recursive-root-search` is `specced`, not done. The refresh behavior exists independently of its three-level fixture. The coordinator should close this leaf only with or after that proof. `state:` is untouched.
Unresolved blocking findings: none.
Validation (read-only): reads of `src/sources/search.rs` (`read_until`, `Status`) and `.cartridge/tests/integration/source-search.test.ts` at memo.ctg `83bf1ad`; `git log` on memo.ctg and ws/memo.ctg; needs resolution; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: coordinator runs the two memo gates above and closes after `recursive-root-search`.
