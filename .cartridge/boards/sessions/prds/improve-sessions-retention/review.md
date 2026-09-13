# Preview and apply safe session retention — review

Canonical PRD: [@sessions/improve-sessions-retention](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-sessions-retention](../../../root/reviews/round-1/improve-sessions-retention.md): reviewer 88/100; Revise. Define the authoritative pin/reference set and crash-safe deletion journal; avoid a dependency on external client mapping unless deletion actually needs it.
  Original SHA-256: `1659ad9e8f8d085e4597dbc0d9b615bc7b97067f3ba86b206c29bc0cb2cc0726`.

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

Independent reviewer: Codex `/root`; implementer `/root/sessions_mapping`.
Inputs: [review-round-3-inputs.json](review-round-3-inputs.json).

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 20 | Native baseline exposes active-delete gap; one guarded retention outcome. |
| Ownership and reuse | 19 | Sessions guard protects existing harness cleanup; references are owner metadata. |
| Dependencies and slices | 18 | Journal/barrier/index lock ordering requires careful concurrency tests. |
| Acceptance and baseline | 19 | Exact SDK baseline and targeted stale-preview/interruption cases. |
| Failure and compatibility | 19 | Backups precede unlink; resumes preserve changed/protected/replacement sessions. |

**95/100 — PASS**, no blocking findings, 3/5 rounds used.
Reviewer requirements within this scope: serialize concurrent apply/resume on each
journal; distinguish deleted originals from later same-ID replacements; reject
traversal/symlink paths; test post-unlink/pre-journal update and directory-sync
uncertainty. Cross-process transcript writers retain the documented single-writer
contract. This is an agent plan rating, not product validation or a user rating.

### Round 3 verification binding

The verification shell command now builds and supplies HARNESS_BINARY to the
actual SDK test for the existing harness compatibility acceptance. This expands
its concrete proof command without changing the reviewed outcome, scope or failure
boundary. Final checklist/proof metadata and input digests are recorded in
[proof-inputs.json](proof-inputs.json); no review round was reset or criterion relaxed.
