# Resume interrupted runs without replaying uncertain mutations — review

Canonical PRD: [@agent/improve-agent-resume-boundaries](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-agent-resume-boundaries](../../../root/reviews/round-1/improve-agent-resume-boundaries.md): reviewer 92/100; Keep. Strong crash-boundary and unknown-effect tests; use existing checkpoint vocabulary and do not infer rollback from cancellation.
  Original SHA-256: `b264b2a947726a7d2915117e98e20fcce2a9685ee7b033f9a758d6bb20318db7`.

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

## Round 3 — 2026-09-14 (reconciliation and rebase)

Reconciliation verdict: **REBASE**. Outcome still wanted and partly present: `Agent::recover` already closes every unfinished run `interrupted` with `interrupted-outcome-unknown` and never replays (`agent.ctg/src/lib.rs:213-231`; tests `run_state.rs:453,493`), but it does not distinguish never-started calls (no `tool_started` checkpoint, `agent.ctg/src/lib.rs:662`) or backend-confirmed completion. Since agent `936df03` a reload is a stop and start, so every reload takes this path — the outcome matters more. Frontmatter key was `capability-capability-owner`; footprint named four nonexistent paths. Both needs are done.

Presented revision: prd.md SHA-256 `fc99cfc16cde6169ac3b1989d20bf89ceb8ee3ef27c5ad3b4c928889c77444d4` (rebased from `9e6f65aca64c0f126a6f154328f94ed4dbaa1ff79baf0b73f56908a104eddf45`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Classification at restart/reload with a bounded default (no automatic continuation). −1: scope L; split point stated but not taken. |
| Ownership and reuse | 19 | Extends existing recovery and its two tests; backend status from the done gitfs tool-result leaf. −1: which backends report call status is unprobed. |
| Dependencies and slices | 18 | Needs resolve and are done. −2: events-port precondition has no PRD. |
| Observable acceptance and baseline | 19 | Three kill-point outcomes defined per point, cross-session isolation, legacy recovery unchanged. −1: gate cannot build until the port. |
| Failure, recovery and compatibility | 18 | Ambiguity defaults to unknown; recovery error leaves the record untouched and a new start possible. −2: cancellation of an in-progress recovery unstated. |
| Reviewer total | **93 / 100** | |

Findings and concrete revisions: (1) starting-file links resolved to nonexistent `boards/model_loop.rs`/`boards/run_state.rs`; run state now lives in `agent.ctg/src/lib.rs` and `run_state.rs` is a test module under `.cartridge/tests/unit/` — replaced with real paths and a footprint. (2) Fixed `capability-capability-owner`. (3) Defined known/unknown per kill point and removed the undefined "resumes safe work" in favour of a stated default. (4) Moved compatibility prose into a check.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased). Partial delivery noted; not DELIVERED.
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (93/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: after the events port, run the kill-point probe and split if needed.
