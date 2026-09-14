# Preview workspace-tool effects before execution — review

Canonical PRD: [@runtime/improve-tools-preflight](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-tools-preflight](../../../root/reviews/round-1/improve-tools-preflight.md): reviewer 89/100; Rehome. Keep read-only preview and apply revalidation; settle the surviving development-package home so migration does not duplicate the operation planner.
  Original SHA-256: `63c10efb1d5123dcaaef683759423f5d1fa201d45ed7ced762a51e8e5a093d8d`.

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

Reconciliation verdict: **REBASE**. `scripts/workspace.py` and `repositories.json` no longer exist; the operations are the tools cartridge's `dispatch` (`tools.ctg/src/service.rs:652`: bundle, lane, land, lane-rm), ported 9b7d7dc. The stale revision's "surviving runtime development package" home contradicts decision `tui-and-tools-are-cartridges` and cartridge.ctg b1494bb ("the base, not a composition"). Preview mode is absent (every op mutates directly). Frontmatter key typo `capability-capability-owner` corrected to `capability-owner` (value unchanged).
Stale presented revision: `d96307c195ad4501ee6acef22ecea9c024841b999786abb8443a92087a950523`. Revised revision: `0d40f6958fd96d07b8312ac17057c512c1a58a6277a8337122c7733e2bd0c2e8`.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 17 | Useful for agents driving destructive repository ops; one outcome. -3: moderate value, no reported incident. |
| Ownership and reuse | 18 | tools.ctg owns the ops; preview reuses each op's checks, no second executor. -2: @runtime board placement historical. |
| Dependencies and slices | 19 | No hard needs; shared file with two siblings named. -1: landing order unset. |
| Acceptance and baseline | 19 | Byte-identity, missing prerequisite, stale expect, compatibility. -1: snapshot fixture still to be written. |
| Failure and compatibility | 19 | Stale digest refuses before effects; requests without new fields unchanged. -1: digest scope for bundle (build inputs) left open. |
| Reviewer total | 92 / 100 | |

Result: **PASS**. Unresolved blocking findings: none. Coordinator: rehome to @tools when convenient.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: fixture snapshot, then specs.
