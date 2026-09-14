# a-usage-ranked-tool-graph — review

Canonical PRD: [@landscape/a-usage-ranked-tool-graph-serves-the-best-way](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-usage-ranked-tool-graph-serves-the-best-way](../../../root/reviews/round-1/a-usage-ranked-tool-graph-serves-the-best-way.md): reviewer 80/100; Reconcile. Check already-delivered children and retain Landscape as the ranking owner; do not introduce the older proposed separate ranking database again.
  Original SHA-256: `d5e8990205383a80dacd227155115bfd42026f14b89297696e1393e0ebd340be`.

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
Reconciliation verdict: **REBASE**. The older plan targeted `landscape.ctg` and, through its children, a `builtin/toolgraph` ranking crate. Both are gone: decisions `the-fabric-owns-the-graph.md` and `the-fabric-lives-in-core.md`; cartridge.ctg 939e7d1 then removed core's fabric, leaving the single ranker in `memo.ctg/src/fabric_graph.rs` (`search`, `counts_from_journal`, `grown`) served by the memo `fabric` op (`memo.ctg/src/service.rs`). Children status: tool-graph-engine, resolver-runs-on-engine and dispatch-and-routines are `done` in the root record but the resolver move was reverted by the dissolution (`usage.rs` does not call the fabric ranker); agents-query-the-tool-graph is `active` with an owner.
Stale revision: `300d60122240e4e81f478ea1cc10a1f9eb2d3e442aca251b33d768575f5bffc6` (dead start links, dead gate `just test landscape`, repo cartridge.ctg).
Presented revision: prd.md SHA-256 `d3b6849f771a70ea9f9f52d26769fb01957ad68051870469562ed9ddcc47671e`. Source inspected at memo.ctg 9a1cf99, memory.ctg c25af4d, sessions.ctg e9725e8, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: owner memo; four children mapped by name; real-consumer proof through `tool.memo` fabric + observe; resolve/fabric boundary default stated; active claim preserved.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 17 | Reconciles a user request (2026-09-12) with the delivered fabric. -3: first acceptance is an analysis artifact rather than product behavior. |
| Ownership and reuse | 19 | Single ranker reused; no service/store. -1: board alias still landscape. |
| Dependencies and slices | 18 | No hard needs; active sibling claim respected. -2: shares `graph.rs`/`fabric_graph.rs` with the search-ranking leaf. |
| Acceptance and baseline | 18 | Consumer-level observation proof and malformed-journal case (`counts_from_journal` skips bad lines). -2: the shared-standing default changes resolve behavior and needs a before/after fixture. |
| Failure and compatibility | 18 | Derived-only rollback; journal preserved. -2: no compatibility note for `ranking_version` consumers of resolve. |
| Reviewer total | **90 / 100** | |

Result: **PASS**. Blocking findings: none. Non-blocking: decide with the resolve owner whether shared standing bumps `ranking_version`.
Validation: file existence, root/prd record statuses of the four children, `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: rehome to memo board; write the reconciliation note first.
