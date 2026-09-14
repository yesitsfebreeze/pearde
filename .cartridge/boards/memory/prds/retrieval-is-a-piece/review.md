# retrieval-is-a-piece — review

Canonical PRD: [@memory/retrieval-is-a-piece](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [retrieval-is-a-piece](../../../root/reviews/round-1/retrieval-is-a-piece.md): reviewer 72/100; Reconcile. Current retrieval/piece crate exists; compare shipped ABI and reload tests with the old twelve-function migration, then specify only the demonstrated residual gap.
  Original SHA-256: `fababf43af05594484e46d3c9f8217bcce01de3dfc8921421f713fad439e2fc1`.
- [every-compute-crate-is-a-piece](../../../root/reviews/round-1/every-compute-crate-is-a-piece.md): reviewer 74/100; Reconcile. Current retrieval/piece already exists; review retained hygiene/retrieval evidence and remaining hot-reload gap before treating this umbrella as new implementation.
  Original SHA-256: `66f82e47b3b7b750dbdacb8592a8d5190ada18d2aa981087959cd5f33be1d484`.

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

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.
Reconciliation verdict: **REBASE — the hot swap is delivered (`src/retrieval/src/lib.rs` hot_lib_reloader; `.cartridge/tests/integration/retrieval-reload.test.ts` proves score change under same PID and restore), so round-2 acceptance 1 was already met. The remaining gap is a pre-use compatibility check (none exists). Memory decision `crates-are-hot-pieces` governs.**

Presented revision: `prd.md` SHA-256 `4435b6303e91ad9ab07f0188eaaaca72a0c3b201f04570c37ac59b0697c33e51`. Rebased in this round (prior text `964787ff260c2f3e5f4a14afaf85a5c1c96503e3fc268619ed2021d26942b7dc`).
Source inspected: memory.ctg `c25af4d` (main), root `24aa2be`, prd.ctg `077e57a2` plus working tree.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Prevents a crashing/incorrect swap in a live daemon. -2: dev-loop only impact. |
| Ownership and reuse | 19 | Reuses piece-build install and reload test. -1. |
| Dependencies and implementable slices | 17 | -3: veto feasibility in hot_lib_reloader unprobed; fallback stated. |
| Observable acceptance and baseline evidence | 19 | Compatible, incompatible and visibility checks with commands. -1. |
| Failure, recovery and compatibility | 18 | Previous implementation keeps serving; static build unaffected. -2: a dylib already mapped cannot be unloaded if the runtime check fires late. |
| Reviewer total | 91/100 | |

Agent score: **91/100 — PASS**.
Findings: Delivered half recorded; narrowed to compatibility stamp.
Blocking findings: none.
Validation: Existence checks only: cited source/test/doc paths exist (`ls`), `needs` targets and local links resolve (script over frontmatter and markdown links), memory.ctg `just --list` shows `check`, `test`, `e2e`, `all`, `eval-mature`, `eval-replay`, `test-reload`. Leaf body word count checked. No product gates were run.
Rounds used / remaining: 3 / 2.
Next: Probe reload hooks.
