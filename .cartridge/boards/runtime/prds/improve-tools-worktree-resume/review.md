# Recover interrupted worktree creation safely — review

Canonical PRD: [@runtime/improve-tools-worktree-resume](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-tools-worktree-resume](../../../root/reviews/round-1/improve-tools-worktree-resume.md): reviewer 90/100; Keep. Strong fault injection after each owned step and refusal of unrelated paths; carry the operation ledger into the surviving package.
  Original SHA-256: `764e07ab84df12e9ed6e7b656c39438d91d6b99f81c8d829ae50b3f3546f7474`.

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

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `7b4e804525314f9f92cbd566263a37488e5bb298ef063057ac1e9172e540bcc8`.

Reconciliation verdict: **REBASE**. The footprint `cartridge.ctg/scripts/workspace.py` and `repositories.json` no longer exists. Worktree creation is `lane()` in `tools.ctg/src/service.rs` (decision `tui-and-tools-are-cartridges`). Existing tests in `tools.ctg/.cartridge/tests/integration/lane.test.ts` already cover refusal of unsafe names and existing paths, and re-provisioning. Revision: rewritten against `lane()`; two concrete gaps are named from source reading; `needs: @runtime/improve-tools-preflight` is removed because it is not a hard prerequisite, only a shared file; fixture repair is step one.

Source findings (read, not reproduced): (a) the worktree loop calls `PathBuf::from(path).canonicalize()?` for every registered worktree, so a registration whose directory is gone fails every lane operation; (b) with a leftover `work/<name>` branch and no worktree, `git worktree add -b` fails and there is no attach/resume path.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | One recovery outcome with concrete current gaps; −1: the gaps are not yet reproduced. |
| Ownership and reuse | 18 | Correct function, test file and gate; −2: the board is runtime while the owner is tools. |
| Dependencies and slices | 19 | Dependency-free now; the shared-footprint serial landing is stated; −1: the dropped need changes the programme graph order (still acyclic). |
| Acceptance and baseline | 18 | Three observable checks tied to injected interruptions; −2: fixture launch validity unknown until step one. |
| Failure and compatibility | 19 | No automatic prune, refusal by name, rollback boundary; −1: branch-with-extra-commits reuse semantics need a spec detail. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Blocking findings: none.
Validation: `rg`/`sed` of `tools.ctg/src/service.rs` `lane()`, `lane.test.ts` cases, `ls cartridge.ctg/builtin` (absent), and the `just test tools` recipe in `cartridge-development.md`. No product gates were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: run `just test tools`, record the baseline, then reproduce gaps (a) and (b).
