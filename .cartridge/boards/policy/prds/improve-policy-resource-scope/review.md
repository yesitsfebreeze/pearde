# Constrain granted file operations to declared resources — review

Canonical PRD: [@policy/improve-policy-resource-scope](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-policy-resource-scope](../../../root/reviews/round-1/improve-policy-resource-scope.md): reviewer 88/100; Revise. Bind validation to the resource actually opened so symlink swaps cannot race authorization; define supported operations and opaque-shell refusal separately.
  Original SHA-256: `a131cac2559534b395307ff242bb0e8fd53ba7977c257dac3a96f35011b39bfa`.

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

## Round 3 — 2026-09-14 (reconciliation)

Reconciliation verdict: **CONFLICT**.

Reviewed revision: prd.md SHA-256 `06f7235fbf507fb6784bced20fd3f7b8cf6863b76c51b519de078890518c80b5` (frontmatter afterwards set to review-round 3 / needs-decision; body unchanged). Source revisions: policy.ctg 6c91708, fs.ctg b69bce0, gitfs.ctg ebcb3d6, cartridge.ctg c9ef10b, prd.ctg 077e57a2 (dirty tree).

Still wanted: a granted file operation cannot write outside its authorized root, including a symlink swapped between preview and open. Not delivered: `fs.ctg/src/files.rs` `resolve` canonicalizes a path string and later opens it (the insufficient pattern this PRD names); per-cartridge OS grants exist (`cartridge.ctg/src/sandbox.rs`, commit 66df558) but fs grants `write: ["/"]` (`fs.ctg/cartridge.json` 189-197), so they do not scope a call.

Conflict: the plan puts a file-operation target schema and a backend binding contract in policy with footprint `policy.ctg/init.lua` and `cartridge.json`. Decision `.cartridge/memos/decision/a-cartridge-brings-its-own-surface.md` (2026-09-14, decided_by user) says "the policy knows no tool", per-tool rules are the composition's `config.lua`, and no cartridge carries a sibling's protocol; `policy.ctg/init.lua` now only evaluates configured decisions and opens no file. Policy therefore cannot bind the opened handle, and a policy-defined file-target schema is tool knowledge in policy.

Alternatives for the user:
- A (recommended): each mutating owner confines itself. fs and gitfs declare their own root settings and open through handle-relative/no-follow operations, failing closed where the platform cannot bind. This leaf is retired and replaced by owner leaves in the fs and gitfs boards; policy stays tool-agnostic.
- B: policy returns a composition-configured resource scope (`config.lua` data, like `operations`) in its decision, and fs/gitfs declare a need on policy and enforce the returned scope at open. Keeps a central grant, but adds a policy-to-backend contract that must be justified against the decision.
- C: rely on host sandbox grants narrowed per composition (per-cartridge, not per-call or per-session). Cheapest; does not meet the per-grant preview/revision acceptance.
Additional findings: starting-file links resolve; `needs` `@policy/improve-policy-operation-rules` is done; `just test policy` exists (routine `policy.ctg/.cartridge/memos/routine/policy-tests.md`). The Linux sandbox is not implemented yet (`sandbox.rs` header), relevant to C.
No score recorded: a material user decision blocks revision. Validation: file reads, rg, git show; no product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required. User feedback: none supplied.
Result: needs decision. Unresolved blocking findings: owner of path confinement (A/B/C).
Rounds used / remaining: 3 / 2.
Next action: user chooses A, B or C; then revise (A: coordinator creates fs/gitfs leaves and retires this one).
