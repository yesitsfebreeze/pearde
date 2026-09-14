# an ancestry test cannot tell a live lane from an abandoned one — review

Canonical PRD: [@runtime/an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one](../../../root/reviews/round-1/an-ancestry-test-cannot-tell-a-live-lane-from-an-abandoned-one.md): reviewer 55/100; Rewrite. A stale mtime/reflog does not prove an idle lane abandoned; use explicit ownership/release evidence in runtime tooling and test a long-idle live owner.
  Original SHA-256: `8bf04edc22f0be871d7d4f891337fc0d073a1e1e4ba72c39dbb526baa73f44ca`.

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

Reconciliation verdict: **REBASE**. The lane tooling moved out of the root justfile into the tools cartridge (`tools.ctg/src/service.rs:503-650`, ported 9b7d7dc/caea5b7; decision `tui-and-tools-are-cartridges`). The defect still exists: `lane-rm` authorises by `merge-base --is-ancestor` (service.rs:597) plus clean/unlocked checks, which a seconds-old clean lane passes. Decision `the-trunk-checkout-is-a-landing-pad` requires ownership established explicitly, not by mtime. The stale revision named absent `cartridge.ctg/src/runtime.rs`/`service.rs` and `just test runtime`.
Stale presented revision: `c1776985259a31fc8b4499e4325a9c08bd1482fba2706f85cea4e1dc16cfe11a`. Revised revision: `fa2b0d64a8094d1f5fded40e804ce49e0229973b3bb234e74b36b6863de82de7`.
Change: repo → tools.ctg; release marker default; existing `lane.test.ts` entry point; gates `just test tools`/`just check tools` (resolve via root `.cartridge/justfile` → cartridge-development routine, which also runs lane.test.ts).

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Prevents deleting a live session's worktree; one outcome. -1: no automatic sweep exists today, so the risk is scripted/agent use. |
| Ownership and reuse | 17 | Implementation in tools.ctg reusing existing checks. -3: board placement under @runtime while code is tools-owned (coordinator rehome to @tools). |
| Dependencies and slices | 19 | No hard needs; shared `lane` footprint with preflight/worktree-resume named. -1: landing order not fixed. |
| Acceptance and baseline | 19 | Four checks including the existing landed-lane case. -1: failing fresh-lane case not yet recorded. |
| Failure and compatibility | 19 | Pre-existing lanes refused safely with a named recovery op; markers die with the worktree. -1: marker corruption not addressed. |
| Reviewer total | 93 / 100 | |

Result: **PASS**. Unresolved blocking findings: none. Finding for coordinator: rehome to the tools board.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: add failing fresh-lane test, then implement.
