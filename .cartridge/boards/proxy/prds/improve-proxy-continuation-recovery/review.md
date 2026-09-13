# Make continuation lifetime and restart recovery explicit — review

Canonical PRD: [@proxy/improve-proxy-continuation-recovery](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-proxy-continuation-recovery](../../../root/reviews/round-1/improve-proxy-continuation-recovery.md): reviewer 91/100; Keep. Good expired/restart/wrong-client cases; keep persistence conditional on demonstrated need and preserve full-input recovery.
  Original SHA-256: `5e7e9badbcece8bf3a6e0d31eec6138ab657d0069be3889b246c0979bdbda3d1`.

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

Independent reviewer: `/root`; implementing agent: `/root/proxy_continuation`.
Reviewed inputs: [round-3 digests](review-round-3-inputs.json), [specification](specs/spec01.md), [disposable baseline](baseline-inputs.json).

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | One observable continuation recovery boundary; durable history explicitly excluded. |
| Ownership and reuse | 19 | Proxy owns synthetic IDs, reuses authenticated frontend and actual router route contract. |
| Dependencies and slices | 19 | Existing router route pin available; bounded optional distinct principals require frontend wiring. |
| Acceptance and baseline | 19 | Source-identical disposable probe confirms wrong-selector mapping and indistinguishable restart/expiry. |
| Failure and compatibility | 19 | TTL/capacity bounds, fail-closed route evidence, trusted scopes, no replay and honest shared-key limitation. |

**95/100 — PASS.** No blocking findings. Reviewer requires principal ownership checks before revealing live/tombstone model mismatch or expiry, final-round route evidence (including hidden tool rounds), and 4 KiB bounds before metadata allocation/retention. These implement the reviewed contract. Ratings concern the plan, not product quality; implementation gates remain pending. Rounds used: 3/5.

Implementation: source `0c9d4e9bd2bb7fef98dd1bc2f593f314b7a090e2`; [proof](implementation-proof.json). Public proxy tests (25) and check passed for final product code. One final test assertion was added afterward; coordinator must run the committed-source gate against the integrated router before collection. State/review markers and acceptance checks changed after round-3 review without modifying the reviewed contract.
