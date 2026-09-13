# Make headless operation authorization usable and truthful — review

Canonical PRD: [@mcp/improve-mcp-approval-route](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-mcp-approval-route](../../../root/reviews/round-1/improve-mcp-approval-route.md): reviewer 92/100; Keep. Preserves headless refusal and tests forged approval context; document the actual operator route under the same policy revision.
  Original SHA-256: `bd365bd8dc6a7bb7e0d9fd8dc1192bdba8c43e903a5a1cdcaf0b836d7af1c977`.

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

## Round 3 — Optional operation inspection and refusal diagnostics

Reviewer `/root` self-review; input digests in review-round-3-inputs.json.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Baseline proves missing inspection; one headless authorization outcome. |
| Ownership and reuse | 20 | Reuses completed policy.explain and current exposed-tool registry. |
| Dependencies and slices | 19 | Policy prerequisites are done; MCP owns optional presentation only. |
| Acceptance and baseline | 19 | Real stdio profile, forged-authority negatives and replacement mismatch. |
| Failure and compatibility | 19 | Diagnostic failure cannot turn refusal into dispatch; old clients unchanged. |

**96/100 — PASS**. No blockers. The extension is explicitly optional; configuration
does not create an interactive approver. Same-revision checks bind explanation to
a refusal; inspection itself is only a current observation and never a grant.
Rounds used: 3/5. Product tests remain pending.

Protocol reference: [MCP 2025-06-18 schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-06-18/schema.ts)
and [metadata keys](https://modelcontextprotocol.io/specification/2025-06-18/basic).
Experimental capabilities and a non-reserved metadata key carry this extension.

Proof spelling correction: Bun requires the explicit `./.cartridge/` path to treat the hidden test directory as a path. This changes only command resolution, not the fixture or accepted behavior.
