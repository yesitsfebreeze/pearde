# a-cartridge-installs-from-its-source — review

Canonical PRD: [@runtime/a-cartridge-installs-from-its-source](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-cartridge-installs-from-its-source](../../../root/reviews/round-1/a-cartridge-installs-from-its-source.md): reviewer 86/100; Revise. Good pin-specific approval; define atomic concurrent cache/lockfile updates, immutable approved trees and failed-fetch cleanup before adding an installer cartridge.
  Original SHA-256: `8c18c94d1aa30987dc01d3e53db241294d6103506ae866d97f16a801ef4e237a`.

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

Reconciliation verdict: **REBASE**. The installer now exists in the base: `cartridge setup`/`doctor` (cartridge.ctg commit b02b200, `src/cli/setup.rs:349` `install` runs an unpinned `git clone` into `<root>/<name>`, records no commit, leaves a partial folder on failure). The stale revision named absent `src/runtime.rs`/`src/service.rs`, "hello/demand activation" vocabulary from the retired loader, and an external memo prerequisite (`root--a-cartridge-declares-what-it-needs`) whose manifest-only declarations are delivered by `needs`/`listen` in `src/loader/document.rs`.
Stale presented revision: `418cf44e7bf9ca0d43b7b825ad60ba161ec0784d7ffd8a652be49ed8e4e4358d`. Revised revision (this round): `1840a00bf1ba56f200f9e33f82aa28f6daa56d4b982c97e267abdd440e8e8221`.
Change: rebased onto `setup.rs` with a recommended lock-file default and stop condition; dropped the dead prerequisite and transitive-approval clause (nested cartridges arrive inside their tree); starting test entry `.cartridge/tests/unit/src/cli/setup.rs` exists.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | One observable outcome (reproducible repository install). -2: lock format is a recommended default, not yet probed against other readers. |
| Ownership and reuse | 19 | Base installer owns it (b02b200); reuses `install`/`write`/`doctor`. -1: doctor/plan boundary for drift refusal left to implementation. |
| Dependencies and slices | 19 | No hard needs; previous memo prerequisite verified delivered in document.rs. -1: no shared-footprint note with other setup work. |
| Acceptance and baseline | 18 | Four unchecked observable checks with fixture location. -2: partial-folder defect inferred from source, not yet reproduced. |
| Failure and compatibility | 18 | Failed clone, unchanged lock, read-only doctor, folder installs and lockless profiles covered. -2: two concurrent setups not addressed. |
| Reviewer total | 92 / 100 | |

Result: **PASS**. Findings: reproduce the partial-folder case before specs; decide concurrency only if setup becomes non-interactive. Unresolved blocking findings: none.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: probe the fixture, write specs, implement.
