# a lane's build can hand back a sibling's binary — review

Canonical PRD: [@runtime/a-lanes-build-can-hand-back-a-siblings-binary](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-lanes-build-can-hand-back-a-siblings-binary](../../../root/reviews/round-1/a-lanes-build-can-hand-back-a-siblings-binary.md): reviewer 78/100; Rehome. Strong measured cache contamination, but host lane automation is excluded by current WORK_ITEMS.md; give it a runtime/tools owner and verify two divergent binaries.
  Original SHA-256: `557d654bd9bb8943ad9a23290b00adbff178819b829a7d13a90b0a3c2738b5b1`.

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

Reviewer: Codex `/root`, self-review under session delegation policy. Inputs:
[review-round-3-inputs.json](review-round-3-inputs.json). Historical wrapper
contamination evidence is retained above; no new observation is attributed to it.
Current probe: two new behavior tests fail on the original runner. Nested memo
execution picks the first `.cartridge` ancestor, and the resulting build reports
`manifest path .../Cargo.toml does not exist`. The development routine also
inherits both compiler wrappers and the caller's shared target without checking
whether it is running in a worktree. The safe path will isolate those settings;
the opt-in comparison records the actual installed wrapper without changing it.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Own binaries are an executable board prerequisite; nested lane failure reproduced. |
| Ownership and reuse | 20 | Three runtime-owned files; public recipe remains the build path. |
| Dependencies and slices | 19 | Disposable Git worktrees and dependency-free Rust fixture; no model/network dependency. |
| Acceptance and baseline | 19 | Execute binaries, retain digests/source/timing, hostile inherited settings checked. |
| Failure and compatibility | 19 | Disable wrappers locally when broad correctness is unproven; preserve ordinary checkout configuration. |

**96/100 — PASS**, no blocking findings, 3/5 rounds used. Small-fixture wrapper
success is not proof of correctness for the historical dependency workspace.

Validation: four Bun tests pass, including two real Git worktrees with distinct
committed source, cold/warm executable output checks, and inherited target plus
both wrappers deliberately set to hostile shared settings. Nested memo owner,
argument preservation, malformed memo refusal and failure propagation pass.

`CARTRIDGE_COMPARE_WRAPPER=/Users/feb/.cargo/bin/kache bun test ./.cartridge/tests/integration/memo-run.test.ts`
passed with kache 0.16.0 and rustc 1.98.0 on aarch64-apple-darwin. The dependency-free
fixture did not reproduce historical kache contamination: all eight measured
outputs were correct. [Raw comparison](wrapper-comparison.json) retains source
commits/trees/digests, executable digests, platform and timings. Safe public cold
builds took 576–613 ms, warm 374–486 ms; direct wrapper cold 523–558 ms, warm
191–234 ms. These include different command paths and are not an isolated wrapper
speed estimate. Global configuration was not modified. Since this fixture cannot
prove kache's cache keys for the historical workspace, worktree builds disable
both wrappers locally. Checkbox changes record proof without changing acceptance.
