# Agent, MCP, and proxy share discovery and execution behavior — review

Canonical PRD: [@mcp/clients-share-document-execution](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [clients-share-document-execution](../../../root/reviews/round-1/clients-share-document-execution.md): reviewer 87/100; Revise. Freeze the public query/read/execute schema and legacy-name collision rule; explicitly stage one-shot client parity separately from later lifecycle modes.
  Original SHA-256: `477b9dbaa76fb4c625623164c619b6a2cdc7a5b3d8c6b4cd3ad2af717abe6755`.
- [an-mcp-server-carries-the-tools](../../../root/reviews/round-1/an-mcp-server-carries-the-tools.md): reviewer 78/100; Reconcile. MCP is already present; compare remaining real-client/cancellation evidence against current mcp.ctg and the shared-client PRD instead of creating another server.
  Original SHA-256: `dd6b262a720b6ce0f5f9d6f37bc626fb42102f0656122d28f44ebf0f0f0678fe`.
- [zirkles-tools-serve-any-agent](../../../root/reviews/round-1/zirkles-tools-serve-any-agent.md): reviewer 80/100; Reconcile. Both transports now exist; identify remaining CLI/context/cancellation gaps in current clients and roll them into shared document execution.
  Original SHA-256: `35ea9c0afe2bcb4fd809abe508cc371f35dd12ce24f15ab27131080ecb470fe3`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 20 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 20 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: Parent reduced to linked scope and integration acceptance; only leaves are implementation work.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.
