# The sandbox — review

Canonical PRD: [@runtime/the-sandbox](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-sandbox](../../../root/reviews/round-1/the-sandbox.md): reviewer 82/100; Reconcile. Update the opening absolute-grant promise to agree with the accepted coarse network semantics; roll up real platform and launch-path proof from children.
  Original SHA-256: `12988bc00ed715e34b1eafb00c2e722a75c77078505d02abd68de9c227cd2121`.

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

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `3a006fa4dc6de024f526c222d234fe2d68ecac7460407acf6eecc2a0af0f1244`.

Reconciliation verdict: **REBASE**. All three children targeted pre-rewrite files. On the transport host the grant in `cartridge.json` is the single policy input and `src/sandbox.rs` the single wall (macOS profile shipped; Linux refuses). Round 1's "absolute-grant promise vs coarse network" point is reconciled: the snapshot now states the platform limit. Revision: current-state paragraph, pinned integration gate, shared footprint; the launch-authority link text was updated to its rebased title. All three children were rebased and passed round 3 in this pass.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | A finite snapshot with a current state; −2: Linux closure has no date or runner certainty. |
| Ownership and reuse | 19 | Single runtime module; −1: `src/cli/host.rs` launch remains an intentionally excluded route. |
| Dependencies and slices | 18 | Three resolving needs, acyclic; −2: launch-authority acceptance 2 waits on the linux-policy runner. |
| Acceptance and baseline | 18 | A pinned-revision gate on both platforms; −2: no baseline. |
| Failure and compatibility | 18 | Refusal-not-fallback is retained in the children; −2: no roll-up-level rollback beyond child boundaries. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Blocking findings: none.
Validation: needs resolution and children review status, reading of `src/sandbox.rs`/`sandbox_linux.rs`. No product gates were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: macos-policy is dependency-free; linux-policy starts with the runner probe.
