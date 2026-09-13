# the-memory-workspace-is-tracked-not-patched — review

Canonical PRD: [@runtime/the-memory-workspace-is-tracked-not-patched](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-memory-workspace-is-tracked-not-patched](../../../root/reviews/round-1/the-memory-workspace-is-tracked-not-patched.md): reviewer 35/100; Retire proposal. Current memory is a separate tracked submodule; do not execute the obsolete instruction to remove its .git or import its source into the runtime repository.
  Original SHA-256: `95dace7797c079783a5767e5a5732ea68ad5d08e80378be7bfa66f3975f26025`.

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
Baseline [fresh-build evidence](baseline-build.json): composed revision
`aae108998c35e217a557fb9a2637bc1b4b47fa79` recursively initialized 22 submodules,
retained memory `318c8f71347f63cc3296945aada8373029f8f372`, resolved the SDK to the
sibling checkout, and built memory_cartridge in 31.13 seconds through the public
build recipe with locked dependencies and the cartridge feature. The temporary
clone was removed; the existing repository, worktrees and stores were untouched.
The metadata path compares equal after canonicalizing macOS /var and /private/var.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Replaces obsolete import assumptions with a reproduced fresh build. |
| Ownership and reuse | 20 | Runtime verification only; memory history and ownership unchanged. |
| Dependencies and slices | 19 | Local Git object sources, recorded gitlinks and current public recipe. |
| Acceptance and baseline | 20 | Fresh recursive checkout and adapter binary already observed; retain a repeatable gate. |
| Failure and compatibility | 19 | Fixture-only configuration/output/cleanup; assert original registrations unchanged. |

**97/100 — PASS**, no blocking findings, 3/5 rounds used. No production relocation
is needed. Add the regression proof and collect it using the current recipe.

Validation: the maintained full Bun proof recursively initialized all 22 pinned
submodules, built memory_cartridge, and checked the source/worktree registrations
remained unchanged (93 assertions, 32.83 seconds). The runtime test
`recorded_memory_layout_uses_the_separate_submodule` passed and is included by
`just test runtime`; it verifies layout/metadata without repeating the full build.
Collection reruns both declared proof commands. No migration or bootstrap source
change was necessary. Checkbox changes record these observations only.
