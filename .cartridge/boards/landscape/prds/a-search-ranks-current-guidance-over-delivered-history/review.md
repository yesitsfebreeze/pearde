# a-search-ranks-current-guidance-over-delivered-history — review

Canonical PRD: [@landscape/a-search-ranks-current-guidance-over-delivered-history](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-search-ranks-current-guidance-over-delivered-history](../../../root/reviews/round-1/a-search-ranks-current-guidance-over-delivered-history.md): reviewer 87/100; Revise. Keep measured current-guidance queries, but add explicit history-intent and paraphrase fixtures; never universally suppress done work when history is the requested answer.
  Original SHA-256: `cd5a1abe53dabf63e62c5d3f75d38fcf4da426107f9f1867186ca50dadb6959b`.

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

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **REBASE**. The target `landscape.ctg/src/{lib,surface}.rs` no longer exists (root commit bc2c190 dropped the submodule; decision `.cartridge/memos/decision/the-fabric-lives-in-core.md`). Verified against source rather than the direction digest: core no longer holds the fabric either (cartridge.ctg 939e7d1 deleted `src/graph.rs`, `fabric.rs`, `evidence.rs`); the ranker is `memo.ctg/src/fabric_graph.rs::search` and the evidence crate is `memo.ctg/evidence` (8d6a803). Outcome still wanted: `search` has no lifecycle input and `Node` carries no `status`.
Stale revision: `5adca59559b4ccfbb9193b6e8c62ce7af700aad9c00299c503d6a0b61fb32dc9` (repo cartridge.ctg; start links resolve to a missing repository; gate `just test landscape` hits `Unknown owner` in `.cartridge/memos/routine/cartridge-development.md`).
Presented revision: prd.md SHA-256 `864b4bdcfa7143e07fefcdfe1d741e1f26fdce7496002adbe3dfc9e8a2dbd81b`. Source inspected at memo.ctg 9a1cf99, memory.ctg c25af4d, sessions.ctg e9725e8, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: repo and owner moved to memo; start files, fixture queries and `just test memo`/`just check memo` named; explicit `intent` (default `current`) replaces an unspecified intent heuristic; rollback and statusless-node compatibility stated.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Measured defect (work memo, 2026-09-12) with both repository-gate queries named; STOP-list tuning excluded. -1: resolve ordering left out without a linked follow-up. |
| Ownership and reuse | 19 | memo owns `fabric_graph.rs`; reuses `usage.rs` status/superseded vocabulary; no new store. -1: board is still `landscape` until rehomed. |
| Dependencies and slices | 19 | No hard prerequisites; one file footprint plus `graph.rs`. -1: `graph.rs` is shared with the usage-ranked leaf. |
| Acceptance and baseline | 18 | Three observable checks incl. invalid intent; unit test file exists. -2: expected top-five fixture must be built; baseline order not yet recorded in-repo. |
| Failure and compatibility | 17 | Derived-only rollback, statusless nodes compatible. -3: no statement on announce rows from other cartridges declaring conflicting `status` values. |
| Reviewer total | **92 / 100** | |

Result: **PASS**. Blocking findings: none. Non-blocking: rehome to the memo board; coordinate `graph.rs` edits with a-usage-ranked-tool-graph.
Validation: path existence checks for every named file; `just` recipe case list read; `./prd.ctg/prd check` (cwd /Users/feb/dev/cartridge) exit 0, no problems. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: rehome to memo board, then add the two failing unit cases.
