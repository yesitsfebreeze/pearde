# Ship bundles with source and dependency provenance — review

Canonical PRD: [@runtime/improve-tools-bundle-provenance](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-tools-bundle-provenance](../../../root/reviews/round-1/improve-tools-bundle-provenance.md): reviewer 88/100; Rehome. Keep the deterministic provenance contract, but bind implementation ownership to the runtime development-package migration.
  Original SHA-256: `4f414937a0fbbee8d9cf79629c41e128a8c7d0ea85f13d5c65da14b85c9c81c3`.

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

Reconciliation verdict: **REBASE**. Bundling is `bundle`/`package` in `tools.ctg/src/service.rs:300-413`; `scripts/workspace.py`/`repositories.json` are gone; the "runtime-owned development package" and old-shim equivalence clauses contradict decision `tui-and-tools-are-cartridges` and b1494bb. Partially delivered: staged temporary publish with rename, and missing-binary refusal before publication (test `packaging_refuses_missing_rust_binaries_but_accepts_lua_only`). Absent: any provenance record. The `@runtime/improve-tools-preflight` need was not a hard prerequisite and is dropped (shared footprint noted). Frontmatter key typo corrected (value unchanged).
Stale presented revision: `77f969b5ff0f77b5bb51932f4ba3ab6296cbaba5ed39187875b1a4621a2bb808`. Revised revision: `8b5b1edd62508bb11ccab026b0c52c850d75e70aaf3a5d760270fd22a24830a4`.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 17 | Traceable bundles; delivered parts removed from scope. -3: no stated consumer of the record yet. |
| Ownership and reuse | 18 | tools.ctg; extends existing staging. -2: @runtime board placement historical. |
| Dependencies and slices | 19 | No hard needs; shared file named. -1: landing order unset. |
| Acceptance and baseline | 19 | Determinism, per-digest sensitivity, secret exclusion with existing test entry. -1: git fixture to build. |
| Failure and compatibility | 18 | Probe failure keeps previous dist; bundles load without the file. -2: dirty-diff digest of large binary diffs unbounded. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: extend package test with a git fixture.
