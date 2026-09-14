# Harness improvement plan — review

Canonical PRD: [@harness/improve-harness-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-harness-programme](../../../root/reviews/round-1/improve-harness-programme.md): reviewer 90/100; Keep. Reuse the existing compaction corpus across this parent and Landscape quality work; child evidence remains authoritative.
  Original SHA-256: `bed1c74c960217c87091c04ea1945ff0e83400bf954fcb359079103107da8d1e`.

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

Reconciliation verdict: **CURRENT**. Evidence: roll-up names no architecture-bound paths; needs resolve: `@harness/improve-harness-token-accounting` done (harness ca7eeab), `@harness/improve-harness-compaction-diff` done (a282c87), `@harness/improve-harness-quality-eval` open (rebased round 3).
Revision reviewed: `prd.md` SHA-256 `b902d5a60227b52c65de337e754d0ca07f379d9f71fe3521bf46b6af88e42989` (prd.ctg 077e57a2, pre-revision).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Short roll-up; -2 does not say two of three leaves are done. |
| Ownership and reuse | 19 | Harness board, children same board; -1 corpus reuse from round 1 not stated. |
| Dependencies and implementable slices | 19 | Three needs resolve, acyclic; -1 no ready item named. |
| Observable acceptance and baseline evidence | 15 | No integration gate command or cwd; "record mitigations" is not observable. |
| Failure, recovery and compatibility | 15 | No behaviour when a leaf exhausts review or fails at integration. |
| Reviewer total | 86 / 100 | |

Result: **FAIL**.
Findings: Missing integration gate; no failure/exhaustion rule; done children not reflected.
Unresolved blocking findings: none (below threshold only).
Validation: existence checks of child PRDs and cited commits (ls, git log); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke`; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 3 / 2.
Next action: one bounded revision.

## Round 4 — 2026-09-14

Reconciliation verdict: **CURRENT** (unchanged from round 3).
Revision reviewed: `prd.md` SHA-256 `9bf3ec1fa5edef8f5ceb0ee3c8e6407d7fda3e828afffe124373a3e36cf2bf32` (working tree, uncommitted). Change: done children and commits noted; integration gate `just test harness` at a pinned revision with named failures; limitation record; exhaustion rule.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | States remaining work; -1 limitations list is open-ended. |
| Ownership and reuse | 19 | Reuse of existing corpus explicit; -1 none further. |
| Dependencies and implementable slices | 19 | Needs resolve; one open leaf is ready; -1 none. |
| Observable acceptance and baseline evidence | 18 | Concrete gate with cwd; -2 "or named failures" permits closing with known failures. |
| Failure, recovery and compatibility | 18 | Exhaustion keeps parent open; -2 no rollback note for a regressing leaf. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: existence checks of child PRDs and cited commits (ls, git log); `./prd check` (cwd `/Users/feb/dev/cartridge/prd.ctg`, root graph) exit 0 with 228 records and no problems (needs resolve, no cycle); `just --list` (cwd `/Users/feb/dev/cartridge`) shows `test`/`smoke`; relative links checked. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not requested (delegated).
Rounds used / remaining: 4 / 1.
Next action: implement open leaves; this parent closes only on its integration acceptance.
