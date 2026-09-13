# Map client conversations to cartridge sessions honestly — review

Canonical PRD: [@sessions/improve-sessions-client-mapping](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-sessions-client-mapping](../../../root/reviews/round-1/improve-sessions-client-mapping.md): reviewer 89/100; Revise. Name the authenticated source of external identity and behavior when it is unavailable; do not treat self-declared client metadata as authority.
  Original SHA-256: `f7a40cc9a86d25ddfc7e2d3a0129d8dc731074406c6c3d10e87d1eb7043a44e0`.

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

## Round 3 — 2026-09-13

Independent reviewer: Codex `/root`, implementation by `/root/sessions_mapping`.
Inputs: [review-round-3-inputs.json](review-round-3-inputs.json).

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | One reconnect mapping outcome with explicit shared-profile limitation. |
| Ownership and reuse | 20 | Host configuration supplies authority; sessions owns references and existing creation. |
| Dependencies and slices | 19 | Owner-local native operations; no invented transport authentication. |
| Acceptance and baseline | 19 | Real SDK baseline, reconnect/forgery fixtures and concurrent fresh-process CAS. |
| Failure and compatibility | 19 | Separate bounded index, locked atomic publication, explicit orphan recovery and unchanged transcripts. |

**96/100 — PASS**, no blocking findings, 3/5 rounds used.
Reviewer implementation requirements within the accepted scope: OS lock covers
empty-session creation through index publication; reject target traversal/symlink
escapes; test concurrent fresh processes, not only one-process mutex.
Plan rating is not an implementation test result or user rating.
