# Readable projections hydrate bounded linked prose — review

Canonical PRD: [@memo/one-document-serves-every-reader/document-projections](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [one-document-serves-every-reader](../../../../root/reviews/round-1/one-document-serves-every-reader.md): reviewer 89/100; Revise. Pin a dialect version and freeze parser/read fixtures before downstream work; specify revision binding for linked prose and executable imports.
  Original SHA-256: `da288972051eab3cebe4a12d8f555bc390b0ce629d164dede840929a14155a47`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-13

Independent reviewer: `/root`. [Input digests](review-round-3-inputs.json) bind
the actual native SDK baseline at5345aaaa and the concrete projection contract.
The baseline retains literal links/no derived revision and projects explicit
private content.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Exact linked prose projections with separate execution validation. |
| Ownership and reuse | 19 | Existing canonical source owner/parser and immutable snapshots. |
| Dependencies and slices | 19 | Collected identity prerequisite and separate derived closure. |
| Acceptance and baseline | 20 | Actual native baseline; explicit bounds, privacy and source-binding cases. |
| Failure and compatibility | 19 | Private redaction, literal code, bounded truncation and no side effects. |

**96/100 — PASS**, no blocking findings;3/5 rounds used. The reviewer's
labels were scope19, architecture19, verification20, failure19, traceability19;
the table maps those scores to the workflow dimensions. This is an agent plan
score, not a user rating or product measurement. Ensure malformed private
frontmatter never leaks metadata through diagnostics and add a sentinel fixture.

## Implementation evidence — 2026-09-13

Source `76800a23d90202645a2eca7d4ee5dcdca3951998` implements the reviewed contract. Public test reports72 passing tests and check passes; native SDK proof retains six actual replies. Eight projection fixtures cover snapshot reuse after source/alias changes, exact owner/section diagnostics, every bound, code literals and private metadata/body/digest exclusion. Final inspection found and fixed private expected_revision conflict leakage before commit; the privacy test covers this ordering. Both frozen fixture manifests match exact working/index bytes; existing identity fixtures are untouched. See [proof](proof.json). Coordinator must refresh the overlapping identity receipt before collection.
