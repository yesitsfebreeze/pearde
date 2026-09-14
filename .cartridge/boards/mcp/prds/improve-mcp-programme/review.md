# MCP bridge improvement plan — review

Canonical PRD: [@mcp/improve-mcp-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-mcp-programme](../../../root/reviews/round-1/improve-mcp-programme.md): reviewer 88/100; Reconcile. Connect common executor migration and shared readiness schema to the three leaves so transport diagnostics are not rebuilt twice.
  Original SHA-256: `9ec9d25645193f20c136acef9127a7164c3ea003caeb6e1fc7e033455ebf511e`.

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

Reconciliation verdict: **CURRENT**. Evidence: roll-up names no architecture-bound paths; `@mcp/improve-mcp-approval-route` done (mcp f5a7405), `@mcp/improve-mcp-refresh-catalog` done (29b20b2), `@mcp/improve-mcp-tool-readiness` open (rebased round 3); mcp on transport (834b9d9).
Revision reviewed: `prd.md` SHA-256 `a407240e232397590f6df57bb4c4cb61ec4d259096d0e9a04456084ccd8a6b84` (prd.ctg 077e57a2, pre-revision).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | -2 done children not reflected. |
| Ownership and reuse | 19 | -1 round-1 "shared readiness schema / no duplicate diagnostics" not carried. |
| Dependencies and implementable slices | 19 | Needs resolve, acyclic; -1 no ready item named. |
| Observable acceptance and baseline evidence | 15 | No integration gate; release-status smoke failure (`memo inactive`) unaddressed. |
| Failure, recovery and compatibility | 15 | No exhaustion or integration-failure rule. |
| Reviewer total | 86 / 100 | |

Result: **FAIL**.
Findings: Missing integration gate and smoke; no failure rule; done children not reflected.
Unresolved blocking findings: none (below threshold only).
Validation: existence checks of child PRDs and cited commits (ls, git log); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke`; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: one bounded revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **CURRENT** (unchanged from round 3).
Revision reviewed: `prd.md` SHA-256 `f8375b65cfb1b6f225c482b1edf43ee4c34b370ec06a71de05577c36c7b8c824` (working tree, uncommitted). Change: done children noted; `just test mcp` and `just smoke mcp` at a pinned revision with named failures; reuse of registry/policy inspection stated; exhaustion rule.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | -1 limitations list open-ended. |
| Ownership and reuse | 19 | Reuse stated; -1 none. |
| Dependencies and implementable slices | 19 | Needs resolve; readiness leaf ready; -1 none. |
| Observable acceptance and baseline evidence | 18 | Test and smoke gates with cwd; -2 closing with named failures allowed. |
| Failure, recovery and compatibility | 18 | Exhaustion rule; -2 no rollback note. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of child PRDs and cited commits (ls, git log); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke`; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 4 / 1.
Next action: implement open leaves; this parent closes only on its integration acceptance.
