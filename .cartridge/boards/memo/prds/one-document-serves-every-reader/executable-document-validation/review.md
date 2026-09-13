# Invalid executable documents refuse before launch — review

Canonical PRD: [@memo/one-document-serves-every-reader/executable-document-validation](prd.md). Reviewer: `/root` (self-review).
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

Independent reviewer `/root`: **95/100 PASS**, no blocking findings;3/5 rounds used.
[Input digests](review-round-3-inputs.json) bind the actual native/Just baseline and
conservative cartridge-just/v1 spec. Additional parser-edge-probes.json records
mixed-indentation and contextual identifier behavior.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Invalid executable docs yield no descriptor or process starts. |
| Ownership and reuse | 20 | Existing one-snapshot metadata/fence parser; separate execution authority. |
| Dependencies and slices | 18 | Pinned conservative syntax needs explicit future upgrade/runner enforcement. |
| Acceptance and baseline | 19 | Actual Just1.58.0/native probes, immutable LF/CRLF and SDK sentinel proof. |
| Failure and compatibility | 19 | Located failures, bounded extraction/argv/base, unchanged raw views. |

Reviewer labels were problem19, architecture20, boundaries19, proof19,
feasibility18, mapped above. This agent score is not a user rating or measured
product quality. Preserve shell-body opacity and launch_authorized:false; make no
safety claims. Source remains held until facade/type/initialize/parent receipts
finish. No implementation or product gate result is claimed here.

## Implementation evidence — 2026-09-13

Source `3251566e6c92439e4a32c5ce8b734e55726801ee` passes77 memo tests and public check,63 actual validation SDK assertions and80 context compatibility assertions. Frozen LF/CRLF sources retain exact committed manifests and original identity/projection fixtures are unchanged. The native sentinel confirms no Just invocation during valid or invalid validation; actual parser conformance runs only in tests. The expanded56-case native/parser probe found Unicode whitespace overacceptance in Rust splitting; spaces/tabs-only syntax and unit regressions fix it, with the original mismatch retained. All36 accepted cases now parse in Just1.58.0. A Clippy test byte-slice warning was also corrected. See [proof](proof.json).

The shell-body and launch authority boundaries remain unchanged. Coordinator must refresh identity/projection and any dependent facade receipt; this worker did not collect shared board state.
