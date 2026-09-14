# A document invokes validated memo writes — review

Canonical PRD: [@memo/memo-write-document](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [capabilities-live-with-their-owners](../../../root/reviews/round-1/capabilities-live-with-their-owners.md): reviewer 84/100; Split. Create independently claimable owner migrations; connect shell work to PTY input ownership and preserve direct-FS parity before retirement.
  Original SHA-256: `990147ebe7129477ba49047e365acf0292465529cb96a5c5c1d6b91b6ddc58e6`.

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

## Round 3 — 2026-09-14 (reconciliation)

Reconciliation verdict: **SUPERSEDED**.

Reviewed revision: prd.md SHA-256 `e37d91d88ce7db066a3fe72d12dad9f7ee64c2ae7c009dace2d0afb723221a39` (frontmatter afterwards set to review-round 3 / superseded-recommend-retire; body unchanged). Source revisions: memo.ctg 9a1cf99; cartridge.ctg c9ef10b; prd.ctg 077e57a2 (dirty tree).

Owner evidence: validated atomic memo writes with `expected_revision` are native on `tool.memo` and the native service (`memo.ctg/src/service.rs` 112-134; tests `memo.ctg/.cartridge/tests/integration/tests.rs` `a_refused_write_leaves_the_memo_on_disk_untouched`, `concurrent_record_writers_preserve_revision_conflicts`). memo's `document` op reads `cartridge-document/v1` but grants no launch authority (`memo.ctg/.cartridge/docs/documents.md`). Links in this PRD still resolved; the premise did not.

Program-level evidence (shared by the owner-document leaves): the host was rewritten on the transport protocol (cartridge.ctg 939e7d1, ee7e295 "Events are the interface", c9ef10b) and every client now executes the same injected `tool.*` keys (`agent.ctg/src/main.rs` 19-26, `mcp.ctg/src/service.rs` 36-38/74, `proxy.ctg/src/service.rs` 42-43/122). Decision `.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md` (2026-09-14, decided_by user) puts each cartridge's surface and `.cartridge/help.md` in its own directory, rebuilt by `cartridge help`; decision `the-tool-contract-is-a-memo.md` keeps Rust cartridges serving what a memo cannot express. No owner ships a `.cartridge/documents/` tool document, and the shared runner (`@runtime/one-runner-executes-documents`) and `@mcp/clients-share-document-execution` remain open and stale.
Additional staleness: none in paths (memo `src/` links resolve); `needs` targets the mcp rollup rather than its contract leaf.
Disposition: retire recommendation (coordinator/user). Do not delete; `state:` unchanged. If an executable wrapper is still wanted, it belongs to the open root work memo `.cartridge/memos/work/a-tool-is-declared-by-its-memo.md`, not to this owner leaf.
No score recorded (superseded verdicts need none).
Validation: ls/rg existence checks, `git log` of the owner and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required. User feedback: none supplied.
Result: SUPERSEDED — recommend retire. Unresolved blocking findings: none for this leaf; the program parents need the same reconciliation.
Rounds used / remaining: 3 / 2.
Next action: coordinator confirms retirement or reopens under the tool-memo work.
