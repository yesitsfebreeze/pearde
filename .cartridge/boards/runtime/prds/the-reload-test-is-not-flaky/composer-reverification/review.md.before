# the-reload-test-is-not-flaky — review

Canonical PRD: [@runtime/the-reload-test-is-not-flaky](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-reload-test-is-not-flaky](../../../root/reviews/round-1/the-reload-test-is-not-flaky.md): reviewer 88/100; Revise. Twenty green reruns are supporting evidence only; require a controlled reproduction of the race and explicit synchronization that proves the old ordering fails.
  Original SHA-256: `5f09e1bebd11580ab761ef9e9cb3501d210e4c2d929a92c3df758a84fa7859c1`.

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

Reviewer: Codex `/root`, self-review (delegation unavailable under session policy).
Exact inputs: [review-round-3-inputs.json](review-round-3-inputs.json).
Source HEAD: `5fb52a4b458dbec89e405e0f1b06e5a850740bd8`.

Baseline: `just test runtime tests::reload -- --nocapture` passed all eight
selected tests. In an isolated lane, making the initial nested provider depend
on withheld `build_ready` forced the unchanged old assertion to fail after its
60 ms delay: `cargo test --lib tests::reload::a_nested_node_is_swapped_and_its_dependent_follows -- --exact`
exited 101 with `attempt to call a nil value`. This is an initial generation
readiness race, not a compiler artifact failure. The same fixture will publish
that dependency and await the exact fiber; a timeout only bounds failure.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Reproduced the flaky startup assumption in the named test. |
| Ownership and reuse | 20 | One runtime test file; uses existing fiber lifecycle contract. |
| Dependencies and slices | 19 | No external prerequisites; isolated lane and explicit footprint. |
| Acceptance and baseline | 19 | Controlled failing probe, generation assertions, current gate, 20 binary repeats. |
| Failure and compatibility | 19 | Failed candidate stays unpublished; exact Active state and subsequent recovery checked. |

Agent score: **96/100 — PASS**. No blocking findings. Rounds used: 3/5.
Implementation and successful proof are still pending at review time.

## Round 4 — 2026-09-13

Reviewer: Codex `/root`, self-review. Inputs: [review-round-4-inputs.json](review-round-4-inputs.json).
The lane gate exposed a pre-existing runner issue: `MEMO_OWNER_ROOT=${memo_file%%/.cartridge/*}`
selects prd.ctg for lanes nested under its `.cartridge/boards`. The updated spec
runs the identical Cargo selection in the lane and requires the actual public
`just test runtime tests::reload` entry point during integrated verification.
Both stages repeat the unchanged binary twenty times. No acceptance was removed.
Scores: value 19, ownership 20, dependencies 19, observable proof 19, recovery 19.
**96/100 — PASS**, no blocking findings, 4/5 rounds used. Runner repair is a
separate owner-local outcome; it is not hidden by a claimed public lane success.

Validation after implementation: all eight selected reload tests passed in the
isolated lane; twenty invocations of the same built test executable passed.
Acceptance checkbox changes record observed results and do not alter the reviewed
contract. Collection must rerun the declared proof after integration, including
the public development entry point. The generation helper rejects failed/retired
fibers rather than treating settlement alone as success.
