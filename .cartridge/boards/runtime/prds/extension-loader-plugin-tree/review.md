# extension-loader-plugin-tree — review

Canonical PRD: [@runtime/extension-loader-plugin-tree](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [extension-loader-plugin-tree](../../../root/reviews/round-1/extension-loader-plugin-tree.md): reviewer 28/100; Rehome. Use the existing cartridge loader owner; the plan's dispose-then-mount path cannot retain an old active generation on failure without an explicit transactional handoff.
  Original SHA-256: `18c0fcb34f87ed0ab98cb3789b088864d31bd25d247aace169095a47cda13031`.

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

Reconciliation verdict: **REBASE**. Fiber/plugin-tree loader replaced by host slots (939e7d1). Gap confirmed by source reading: `src/host/mod.rs:494-534` `replace_locked` calls `stop_slot` before inspecting the plan result, catalogue refusals (`rewire`, mod.rs:316-345) apply only to stopped slots, and `reconcile` (mod.rs:260-275) stops entries whose new plan is refused. Idempotent reconcile of unchanged entries is delivered (mod.rs:284). The stale revision's memory/plugin-catalog clauses and absent paths are obsolete.
Stale presented revision: `73444e0e6104254ce240e1d09b3aec10218d22275740372e238ce3eb74804784`. Revised revision: `262c85e93855f427be68f97adf0ecd4d0f59a60a830dc9b48061b5a234120f13`.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | A bad manifest edit no longer takes down a working node; bounded to planning refusal. -1: start-failure handoff explicitly deferred. |
| Ownership and reuse | 19 | Host owns replacement; reuses plan/unmatched/catalogue. -1: overlap with document-sidecar-lifecycle. |
| Dependencies and slices | 19 | No needs; overlap ownership declared. -1: child PRD still carries the overlapping clause. |
| Acceptance and baseline | 19 | Four observable checks next to named existing tests. -1: no failing test recorded yet. |
| Failure and compatibility | 18 | Old generation keeps serving; refusal visible in status/lifecycle; rollback named. -2: exclusive-socket start failure remains a known outage. |
| Reviewer total | 94 / 100 | |

Result: **PASS**. Unresolved blocking findings: none.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: failing test for replace with an unreadable document.
