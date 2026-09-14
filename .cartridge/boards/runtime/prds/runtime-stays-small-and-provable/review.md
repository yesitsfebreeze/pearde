# A small, provable terminal runtime — review

Canonical PRD: [@runtime/runtime-stays-small-and-provable](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [runtime-stays-small-and-provable](../../../root/reviews/round-1/runtime-stays-small-and-provable.md): reviewer 83/100; Reconcile. Recompute child status and current integration gaps; retain finite release criteria and remove obsolete paths and uncalibrated duration estimates.
  Original SHA-256: `29b1fe998c5558723bdca1dd2d52b8221417e9a9d059ea989b7a0c04fed3daa7`.

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

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `11a3225c7c57a6c2eea063d547e398e3b585a96208526c7e3b79a676ca397aeb`.

Reconciliation verdict: **REBASE**. The "small" audit moved to the newer roll-up `the-runtime-reaches-top-tier-quality` (2026-09-14), which also needs the CI leaf. The done child `the-reload-test-is-not-flaky` was proven before the transport rewrite (`939e7d1`); reload is now `Host::replace`/`reconcile` (`src/host/socket.rs:301`), with `a_restart_keeps_its_dependents_working` in `tests/host.rs`. Revision: this parent now holds the "provable" half, links the sibling roll-up as context, and requires the reload regression to be re-proven at the integrated revision.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | A clear split from the sibling roll-up; −2: the title still says "small". |
| Ownership and reuse | 18 | Needs resolve across runtime/agent boards; −2: overlap with the sibling roll-up on the CI leaf. |
| Dependencies and slices | 16 | Acyclic; −4: `ci-proves-the-supported-terminal-matrix` is `needs-decision` in this pass and `debug-mode-correlates-a-terminal-turn` is still stale. |
| Acceptance and baseline | 18 | Re-proof requirement for delivered evidence; −2: no baseline. |
| Failure and compatibility | 18 | Reopen path stated; −2: no integration rollback. |
| Reviewer total | 88 / 100 | |

Result: **FAIL**.
Blocking findings: none in the text itself. The score fails because a hard child awaits a user decision (CI). Re-review once the CI leaf resolves.
Validation: needs resolution with state/review-status of children; `rg reload` in host sources and tests. No product gates were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: resolve the CI decision; consider merging this roll-up into the sibling at the coordinator's discretion.
