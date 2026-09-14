# one-search-covers-the-record-and-memory — review

Canonical PRD: [@landscape/one-search-covers-the-record-and-memory](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [one-search-covers-the-record-and-memory](../../../root/reviews/round-1/one-search-covers-the-record-and-memory.md): reviewer 82/100; Merge. Merge into Landscape composition; preserve optional memory, query-bounded candidates and exact readback instead of a second search integration.
  Original SHA-256: `94daf1594bf776d21dd7bb447836adc3ee6abdaf48575da35dfb04260f19771a`.

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
Reconciliation verdict: **DELIVERED** (pending verification). The PRD designates itself memory-contributor acceptance under landscape-composes-system-context; that scope exists in current source and tests:
- A memory-only fact and a document fact from one `context` prepare with attribution and exact readback, no requery: `memo.ctg/.cartridge/tests/integration/context.test.ts` ("native shared context and exact readback retain attribution…"); `memory.ctg/.cartridge/tests/unit/src/cartridge/source.rs` (`memory_fact_joins_shared_context_and_exact_readback_without_requery`).
- Missing/changed references explicit, never re-queried: `exact_missing_changed_prefix_and_invalid_references_never_requery`; context.test.ts `changed`/`invalid_reference` cases.
- Disabled/absent/unavailable/timeout memory keeps other results within the deadline: `unavailable_malformed_empty_and_inactive_memory_preserve_other_sources`, `deadline_drops_pending_read_without_starting_later_hydration`; context.test.ts "optional states and a delayed read…".
- Provider: `memory.ctg/src/source.rs` (`context.memory`), consumer `memo.ctg/src/context.rs`. Sibling PRDs @landscape/landscape-composes-system-context/memory-context-contributor and @memo/landscape-context-facade are `done`.
Residual not covered (outside this PRD's canonical scope): tool hits appear in the `fabric` op, not the `context` op, so "memo/tool phrase" is met for documents and kernel only.
Reviewed revision: `8bef1a42cbe5009026febf07a9b1463f149f4cccab894a9e710675e2a7b10d64`; after frontmatter-only update (review-round, review-status) `11b26820f2ebe2fb6d184e9cdff79069ca83fe5e662ff65c3e658f45b71b3f60`, no semantic change. Stale body links to `landscape.ctg` and gate `just test landscape` were left unrevised because the item is delivered. Source inspected at memo.ctg 9a1cf99, memory.ctg c25af4d, sessions.ctg e9725e8, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Score: not scored (delivered). Result: delivered-pending-verification; `state:` unchanged.
Verification to run before marking done, from /Users/feb/dev/cartridge: `just test memory`, `just test memo`, `bun test memo.ctg/.cartridge/tests/integration/context.test.ts`. None were run in this pass.
Rounds used / remaining: 3 / 2.
