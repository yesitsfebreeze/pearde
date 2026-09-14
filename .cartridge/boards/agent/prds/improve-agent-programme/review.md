# Agent loop improvement plan — review

Canonical PRD: [@agent/improve-agent-programme](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-agent-programme](../../../root/reviews/round-1/improve-agent-programme.md): reviewer 90/100; Keep. Valid roll-up of value measurement, resume and attribution; do not dispatch the parent as additional implementation.
  Original SHA-256: `f9e92ebf54b3dc2cead0147fb83b3ff36355bf32a8e314e91a8079d34c0b88b3`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 20 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 20 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 18 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: Parent reduced to linked scope and integration acceptance; only leaves are implementation work.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14 (reconciliation and rebase)

Reconciliation verdict: **REBASE**. The roll-up goal stands and all three children resolve (`@agent/improve-agent-task-baseline`, `-resume-boundaries`, `-decision-attribution`), each rebased in this pass. Frontmatter carried `capability-capability-owner`; the parent had no integration gate and lost its round-1 reconciliation pointers.

Presented revision: prd.md SHA-256 `0eaa3474b400460bc154ef814547d8bad1bafef965edc57684cca59741ed2169` (rebased from `c2cafd02a4bbfbe83ec8976556d1eef5647aedc78339bc5661f4a4a1bace3d7f`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Parent only: outcome, children, integration gate. −1: no measurable programme-level success criterion beyond child acceptance. |
| Ownership and reuse | 19 | Typo key fixed; shared `lib.rs`/`run_state.rs` footprint and landing order stated. −1: reconciliation with active root memo `agents-query-the-tool-graph` is a pointer, not a resolution. |
| Dependencies and slices | 18 | Qualified needs resolve; graph acyclic. −2: events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | Integration check at one revision with named gates. −2: gates cannot build until the port. |
| Failure, recovery and compatibility | 18 | Limitations recorded at integrated revisions. −2: rollback between sequentially landed children unstated. |
| Reviewer total | **92 / 100** | |

Findings and concrete revisions: (1) fixed `capability-capability-owner`. (2) Added integration gate and shared-footprint landing order. (3) Restored round-1 reconciliation pointers.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (92/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: children proceed after the events port.
