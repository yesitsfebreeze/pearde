# the-exit-flag-tests-race-each-other — review

Canonical PRD: [@memory/the-exit-flag-tests-race-each-other](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-exit-flag-tests-race-each-other](../../../root/reviews/round-1/the-exit-flag-tests-race-each-other.md): reviewer 70/100; Reconcile. The text says the exit flag fix landed; identify the remaining handover test and current test commands instead of reimplementing the completed flag repair.
  Original SHA-256: `4fd17f283d252b81418e083a33e7aa7a9f152f727c96c850963ce61587877242`.

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
Current commands Cargo listing contains 111 unit tests and no exit integration
target, despite the historical file remaining on disk. A disposable child-held
flock probe returns WouldBlock after the parent releases its handle, then acquires
immediately after the child exits. The current no-listener handover fixture is
.cartridge/tests/unit/src/commands/src/commands_serve/watchdog_handover_tests.rs;
its lock is already protected by store_core's bounded inherited-fd retry.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 20 | Restores missing gate and proves the identified handover mechanism. |
| Ownership and reuse | 20 | Reuses the existing exit test and lock patience implementation. |
| Dependencies and slices | 19 | Commands manifest, lock wait seam and owner test only. |
| Acceptance and baseline | 19 | Controlled descriptor lifetime plus two mutation tests and five stable runs. |
| Failure and compatibility | 19 | No global flag reset, no new retry allowance, true holders still refuse. |

**97/100 — PASS**, no blocking findings, 3/5 rounds used. Follow memory's
AGENTS instructions with an isolated worktree and run the full project gates.
