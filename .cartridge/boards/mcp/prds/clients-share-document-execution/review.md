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

## Round 3 — 2026-09-14

Reconciliation verdict: **CURRENT**. Evidence: roll-up names no architecture-bound paths; decision `the-tool-contract-is-a-memo.md` keeps the outcome; `@runtime/one-runner-executes-documents` still open, so nothing is delivered; all four needs resolve (children and `@agent/agent-document-client`, `@proxy/proxy-document-client` open, stale-after-migration). Compatible with `a-cartridge-brings-its-own-surface.md` provided clients reach the runner only by declared need.
Revision reviewed: `prd.md` SHA-256 `9f705c42a0315375db1811a41ff0819a97396d211392c0b07d2369b5469f80a9` (prd.ctg 077e57a2, pre-revision).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | -3 round-1 findings (freeze schema/collision rule; stage one-shot parity before lifecycle modes) not reflected. |
| Ownership and reuse | 19 | -1 surface-decision constraint not stated. |
| Dependencies and implementable slices | 18 | Needs resolve; -2 staging (contract first) implicit only. |
| Observable acceptance and baseline evidence | 15 | "work together" is not observable; no gates for three clients. |
| Failure, recovery and compatibility | 15 | No rule for contract change after adoption or leaf exhaustion. |
| Reviewer total | 84 / 100 | |

Result: **FAIL**.
Findings: Staging and schema-freeze findings absent; no shared-fixture parity check or gates; no contract-change rule.
Unresolved blocking findings: none (below threshold only).
Validation: existence checks of child PRDs and cited commits (ls, git log); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke`; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: one bounded revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **CURRENT** (unchanged from round 3).
Revision reviewed: `prd.md` SHA-256 `5fabb1002a70efbbc59aed14826b2cc4e696dc0a3d611041fe26eb135d570a6a` (working tree, uncommitted). Change: staged contract-then-clients plan; lifecycle modes refused; declared-need constraint; shared-fixture parity acceptance; `just test agent|mcp|proxy` and `just smoke mcp` gates; stale-on-contract-change and exhaustion rules.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Staging explicit; -2 value blocked behind root memory-document proof. |
| Ownership and reuse | 19 | Owner boards per client, declared-need rule; -1 none. |
| Dependencies and implementable slices | 18 | Needs resolve; -2 all children still stale-after-migration and unreviewed in this pass here. |
| Observable acceptance and baseline evidence | 18 | Parity over shared fixtures, gates with cwd; -2 fixtures do not exist yet. |
| Failure, recovery and compatibility | 18 | Contract-change staleness, exhaustion; -2 no rollback for a client that adopted early. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of child PRDs and cited commits (ls, git log); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke`; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 4 / 1.
Next action: implement open leaves; this parent closes only on its integration acceptance.
