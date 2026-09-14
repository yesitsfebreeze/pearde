# macos-policy — macOS commands enforce manifest capabilities through sandbox-exec with verified runtime exceptions and real allowed/denied operation tests. — review

Canonical PRD: [@runtime/macos-policy](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [macos-policy](../../../root/reviews/round-1/macos-policy.md): reviewer 91/100; Keep. Concrete granted/denied resource tests and explicit network limitations; refresh source paths and invoke real wall tests on the identified supported macOS environment.
  Original SHA-256: `6cab72debd36239e5298bd4efca79caffd0640b2d1c86b0ba26c37b124284d7c`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 18 | Resolved hard dependencies and child links; external prerequisites require recorded owner handoff. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **93/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `0a061b731d1bc6dfdca584c2f752369af29a8fa5958dcc39671cb3d58af07a93`.

Reconciliation verdict: **REBASE** (partially delivered). `src/sandbox.rs` ships the sandbox-exec profile: `(deny default)`, canonical path spellings, `literal()` escaping, all-or-nothing net documented, sockets and semaphores. One real-child test exists (`the_synchronous_command_enforces_the_empty_grant`); the other tests assert profile text. The old starting files and command-adapter link are gone. Revision: the outcome is narrowed to the missing behavioral proofs and exception justification, and the known-red smoke baseline is recorded (release-status note).

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Converts text-only tests into real enforcement proof; −1: the implicit-allowance audit may be sizeable. |
| Ownership and reuse | 19 | Existing `wall_fixture` pattern and test file; −1: none beyond board-level. |
| Dependencies and slices | 19 | No needs; macOS-only; −1: shares `sandbox.rs` with linux-policy and launch-authority. |
| Acceptance and baseline | 18 | Concrete allow/deny operations; −2: no baseline run; TCP connect fixture target unspecified. |
| Failure and compatibility | 18 | Removal of allowances is gated on the smoke baseline; −2: the smoke baseline is already red, which weakens that guard. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Blocking findings: none. This is not DELIVERED: the behavioral proof it requires does not exist.
Validation: reading of `src/sandbox.rs` and `.cartridge/tests/unit/src/sandbox/tests.rs`, and `.cartridge/memos/note/release-status.md`. No product gates were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: add real-child allow/deny cases.
