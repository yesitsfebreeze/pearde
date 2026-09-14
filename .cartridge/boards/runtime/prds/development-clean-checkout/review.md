# Development documents work from a clean checkout — review

Canonical PRD: [@runtime/development-clean-checkout](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [development-tooling-has-one-home](../../../root/reviews/round-1/development-tooling-has-one-home.md): reviewer 84/100; Split. Separate package relocation, reproducible bundles and gate integration; reconcile existing preflight/provenance/resume leaves before retiring their owner.
  Original SHA-256: `29135b4eab7d6a5fdbaebd508f564c219de7f5df9a20a2920a848d1edd39d9d9`.

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

Reconciliation verdict: **REBASE**. Paths `cartridge.ctg/src/runtime.rs`/`service.rs` are absent. The needs on `runtime-development-package` (moving tooling under the base, contradicting `tui-and-tools-are-cartridges` and b1494bb), preflight, provenance and worktree-resume are independent outcomes, not prerequisites; no shim exists to retire. The clean-checkout outcome stays wanted and a concrete defect exists: `tools.ctg/cartridge.json` (and every other `*.ctg/cartridge.json`) `commands` call `just --justfile ../cartridge.ctg/justfile build|check|test|process|verify <owner>`, while `cartridge.ctg/justfile` has only `build *args`, `test *args`, `check`, `fmt`. The existing root `.cartridge/tests/integration/source-layout.test.ts` already builds a temporary recursive clone. Tracked developer-home paths outside records: none found (`git ls-files | xargs rg /Users/feb` hits only root memo history).
Stale presented revision: `563823bc38e594b7283192eb3196fde2a67fb470b0e7531799f9db9c6f11dcae`. Revised revision: `4b9e3a6bf466fcdf32644f126df9de34e241da7c48e127c81f182b8d35e1b7f9`.
Change: repo → composed root; needs removed; shrinking baseline so the gate stays green while owners fix manifests.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | Documented commands that actually run from a clone; one check. -2: does not itself fix manifests. |
| Ownership and reuse | 17 | Extends existing root layout test. -3: root test under @runtime board with canonical alias to the @tools rollup; manifest fixes belong to each owner (decision a-cartridge-brings-its-own-surface). |
| Dependencies and slices | 19 | No hard needs, reasons recorded. -1: per-owner follow-ups not yet tracked. |
| Acceptance and baseline | 18 | Resolution, shrink-only baseline, home-path scan. -2: baseline list not yet captured. |
| Failure and compatibility | 18 | Gate stays green on land; rollback deletes check; host never runs commands. -2: `just --summary` misses recipes with parameters in odd forms. |
| Reviewer total | 90 / 100 | |

Result: **PASS**. Unresolved blocking findings: none. Coordinator: create or assign per-owner manifest-command fixes; @tools rollup `development-tooling-has-one-home` still needs `@runtime/runtime-development-package`, which conflicts with current decisions.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: run the check, record the baseline.
