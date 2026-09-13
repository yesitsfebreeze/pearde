# Refresh a live client's tool catalog after replacement — review

Canonical PRD: [@mcp/improve-mcp-refresh-catalog](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-mcp-refresh-catalog](../../../root/reviews/round-1/improve-mcp-refresh-catalog.md): reviewer 90/100; Keep. Re-list fallback and rejected-reload behavior are explicit; pin negotiated notification behavior in fixtures.
  Original SHA-256: `fb5ec421efa107b82e898f43c65f653801c213e6f179a095c843ef83250ff974`.

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

## Round 3 — Coherent discovery and a live client

Reviewer `/root` self-review. Inputs: review-round-3-inputs.json.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Deterministic baseline exposes mixed descriptor generations. |
| Ownership and reuse | 20 | Existing version queries, registry and composition; no transport fork. |
| Dependencies and slices | 19 | Four MCP paths; existing policy/wire tests retained. |
| Acceptance and baseline | 19 | Causal descriptor race plus one real initialized stdio client and failed replacement. |
| Failure and compatibility | 19 | Three attempts, no partial publication, older-runtime fallback and truthful notification capability. |

**96/100 — PASS**. No blockers. This is coherent discovery, not an atomic lock
across discovery and all future calls; providers continue to validate inputs.
Rounds used: 3/5. Product gates remain pending.

## Round 4 — Correlated runtime failure dependency

Self-review **96/100 — PASS** (19/20/19/19/19). Actual live-client testing
found a dropped stdio response when the provider is temporarily absent. The
new runtime leaf owns that two-file repair and inherits four used rounds. MCP
collection waits for it. Catalog design remains unchanged. No blockers; inputs
in review-round-4-inputs.json. Rounds used: 4/5.

## Reverification after optional policy diagnostics

MCP service and shared tests changed for @mcp/improve-mcp-approval-route. The catalog contract and discovery behavior are unchanged; default initialization remains the same and the optional diagnostic capability is separately discoverable. Archive the prior receipt and rerun the full 15-test owner gate, including the initialized live catalog replacement fixture. No additional substantive catalog plan revision.
