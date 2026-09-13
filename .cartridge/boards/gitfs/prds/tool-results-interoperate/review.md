# Every currently exposed tool completes through its real consumers — review

Canonical PRD: [@gitfs/tool-results-interoperate](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [tool-results-interoperate](../../../root/reviews/round-1/tool-results-interoperate.md): reviewer 83/100; Merge. Unify with improve-tool-result-contract and choose one normalization owner; distinguish rejected request input from a malformed result discovered after effects.
  Original SHA-256: `7522d3a132a405f17ba19663b0ad8800b1809ac5187c0fe1662a56b228a300d7`.
- [improve-tool-result-contract](../../../root/reviews/round-1/improve-tool-result-contract.md): reviewer 86/100; Merge. Merge with tool-results-interoperate; choose SDK normalization or producer normalization explicitly and reject double serialization with real-consumer tests.
  Original SHA-256: `a9dc4428c5fe61d5f1b3ba034e2c4eec30233d472d46670aaadcc1a5ba42266a`.

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

Reviewer: Codex `/root`, self-review under session delegation policy.
Inputs: [review-round-3-inputs.json](review-round-3-inputs.json).
Controlled direct-runtime probe on a temporary Git repository returned
`content:{content:"{\"literal\":true}",found:true,...},error:false` from
GitFS read. Both producer `ok` helpers return objects directly; actual MCP/proxy
consumers require string content and reject this envelope. StoreConfig.at also
runs before operation parsing and creates its directory on malformed input.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 20 | Reproduced interoperability failure at a shared prerequisite. |
| Ownership and reuse | 19 | Producer-boundary serialization and validation; consumers retain their protocol. |
| Dependencies and slices | 19 | Owner files and shared real-consumer fixture; no model/provider dependency. |
| Acceptance and baseline | 19 | Actual SDK/MCP/proxy read/scan, literal JSON string, malformed-effect counter. |
| Failure and compatibility | 19 | Pre-backend validation, ordinary-error envelope, no malformed-result replay, existing identity fixtures. |

**96/100 — PASS**, no blocking findings, 3/5 rounds used. Use the clean GitFS
checkout for collection so sibling Cargo workspace dependencies remain valid.
