# per cartridge versioned test runner — review

Canonical PRD: [@runtime/per-cartridge-versioned-test-runner](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [per-cartridge-versioned-test-runner](../../../root/reviews/round-1/per-cartridge-versioned-test-runner.md): reviewer 58/100; Rewrite. Version-only evidence becomes stale when code changes without a bump; key validity by source, dependencies, recipe, toolchain and relevant configuration digests.
  Original SHA-256: `d2e540da2df7c8c7ea778b2584ff9b131b4a66d0a4281dbf268f2b14b19d745d`.

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

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `069bee2e74bc4356cbb2c5db2c8a3f5f0cd701e7f160023c9ead9504e63418ab`.

Reconciliation verdict: **REBASE**. Not delivered: no evidence cache exists (`rg` for evidence/digest in `.cartridge/tools/memo-run` and cartridge.ctg `src` finds none; `cartridge verify` runs selftests without recording). The old starting files `src/runtime.rs`/`src/service.rs` are gone. Gates now live in the root composition routine `.cartridge/memos/routine/cartridge-development.md`, and cartridge.ctg is "the base, not a composition" (`b1494bb`). Revision: `repo` moved to the composition root; key inputs named concretely; evidence under ignored `.cartridge/empirical/`; test file creation and test-entry extension stated. Already delivered and retained as a regression: per-worktree targets (the `_cargo` recipe sets `CARGO_TARGET_DIR` for git worktrees).

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | Stale-evidence detection without running; −2: the original user trigger (a version bump) was replaced by digest keys in round 1; the version is retained as descriptive. |
| Ownership and reuse | 17 | Reuses the root routine and memo-run; −3: runtime board vs composition owner; the routine files are currently uncommitted in the root checkout. |
| Dependencies and slices | 19 | No needs; one leaf; −1: dependent-owner staleness needs the owner graph (`cartridge.json` needs). |
| Acceptance and baseline | 18 | Three observable checks plus a test file; −2: no baseline. |
| Failure and compatibility | 18 | A failure never masks a success; deleting evidence resets safely; −2: concurrent runs writing the same evidence file are not addressed. |
| Reviewer total | 90 / 100 | |

Result: **PASS**. Blocking findings: none. Findings: rehome to the root board (coordinator); specify atomic evidence writes in the spec.
Validation: reading of `cartridge-development.md` and `memo-run`, `ls .cartridge/tests/integration`, `.gitignore` for `/.cartridge/empirical/`, `git ls-files` (routine and justfile untracked). No product gates were run.
User rating: not required. Rounds used / remaining: 3 / 2.
Next: commit the root routine files, then write the fixture test.
