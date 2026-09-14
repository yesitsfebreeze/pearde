# Proxy tool calls retain the shared execution outcome — review

Canonical PRD: [@proxy/proxy-document-client](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [clients-share-document-execution](../../../root/reviews/round-1/clients-share-document-execution.md): reviewer 87/100; Revise. Freeze the public query/read/execute schema and legacy-name collision rule; explicitly stage one-shot client parity separately from later lifecycle modes.
  Original SHA-256: `477b9dbaa76fb4c625623164c619b6a2cdc7a5b3d8c6b4cd3ad2af717abe6755`.

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

Reviewed revision: prd.md SHA-256 `07ab38f5152740b270a0f1d1ad38101994cd0c0f6867a9b0174d4aa9147cbda0` (frontmatter afterwards set to review-round 3 / superseded-recommend-retire; body unchanged). Source revisions: proxy.ctg fb93074; cartridge.ctg c9ef10b; prd.ctg 077e57a2 (dirty tree).

Owner evidence: proxy executes the profile's `tool.*` keys directly (`proxy.ctg/src/service.rs` 42-43, 122; `proxy.ctg/src/main.rs` 212-219) and already proves the acceptance themes natively: `interrupted_stream_reports_error_without_success_replay_or_tools`, `deadline_and_dropped_request_cancel_the_exact_active_tool`, `caller_tools_are_returned_and_mixed_batches_are_deferred_without_execution` (`proxy.ctg/.cartridge/tests/unit/tests.rs`). The "common runner" it was to adopt no longer exists as a planned surface. Cross-client result parity (agent/mcp/proxy shared fixtures), if still wanted, is an mcp-board question. Release note: proxy smoke still times out (implementation).

Program-level evidence (shared by the owner-document leaves): the host was rewritten on the transport protocol (cartridge.ctg 939e7d1, ee7e295 "Events are the interface", c9ef10b) and every client now executes the same injected `tool.*` keys (`agent.ctg/src/main.rs` 19-26, `mcp.ctg/src/service.rs` 36-38/74, `proxy.ctg/src/service.rs` 42-43/122). Decision `.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md` (2026-09-14, decided_by user) puts each cartridge's surface and `.cartridge/help.md` in its own directory, rebuilt by `cartridge help`; decision `the-tool-contract-is-a-memo.md` keeps Rust cartridges serving what a memo cannot express. No owner ships a `.cartridge/documents/` tool document, and the shared runner (`@runtime/one-runner-executes-documents`) and `@mcp/clients-share-document-execution` remain open and stale.
Additional staleness: starting-file links resolved against the old owner-local board location; the files now live under `src/`.
Disposition: retire recommendation (coordinator/user). Do not delete; `state:` unchanged. If an executable wrapper is still wanted, it belongs to the open root work memo `.cartridge/memos/work/a-tool-is-declared-by-its-memo.md`, not to this owner leaf.
No score recorded (superseded verdicts need none).
Validation: ls/rg existence checks, `git log` of the owner and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required. User feedback: none supplied.
Result: SUPERSEDED — recommend retire. Unresolved blocking findings: none for this leaf; the program parents need the same reconciliation.
Rounds used / remaining: 3 / 2.
Next action: coordinator confirms retirement or reopens under the tool-memo work.
