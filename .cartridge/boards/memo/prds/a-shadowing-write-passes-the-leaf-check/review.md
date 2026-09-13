# a-shadowing-write-passes-the-leaf-check — review

Canonical PRD: [@memo/a-shadowing-write-passes-the-leaf-check](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-shadowing-write-passes-the-leaf-check](../../../root/reviews/round-1/a-shadowing-write-passes-the-leaf-check.md): reviewer 88/100; Revise. Add non-shadowable duplicate and owner-qualified read fixtures; reconcile leaf shadowing with the new canonical hierarchical identity before changing validation.
  Original SHA-256: `3ded4544bd9ed9360fee05ea137e5756ac5837ee151805bf3058427d92b3a0ff`.

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

## Round 3 — current behavior and missing merged-write proof

Reviewer: Codex self-review. The 48-test baseline passes and current namespace
validation already separates local uniqueness from owner-qualified identity.
The older defect is not reproduced. Existing tests write the local shadow without
supplying shipped records; the new fixture closes that proof gap and ties stale
revision, duplicate-leaf and owner-write refusals to the same merged view.

Value/scope 19; ownership/reuse 20; dependencies/slices 19; acceptance/baseline 20;
failure/compatibility 20. **98/100 — PASS for the plan**, no blocking finding.
The existing canonical parser is the authority; no global duplicate relaxation
or cross-owner source mutation is proposed. Inputs bound in
review-round-3-inputs.json. Three rounds used, two remain.
