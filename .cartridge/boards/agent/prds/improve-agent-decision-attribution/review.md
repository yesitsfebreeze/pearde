# Trace tool dispatch to exact context and route configuration — review

Canonical PRD: [@agent/improve-agent-decision-attribution](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-agent-decision-attribution](../../../root/reviews/round-1/improve-agent-decision-attribution.md): reviewer 91/100; Keep. Good reference-based attribution and negative cases; include fallback and reload identity in the fixture without retaining full prompts.
  Original SHA-256: `9903b9e3ba6ccf96d16d8829d63b408c07a4eddc7b56101854582971e58b37ae`.

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

Reconciliation verdict: **REBASE**. Outcome still wanted and partly present: `descriptor_revision` digests (`agent.ctg/src/model_loop.rs:17`, `agent.ctg/src/lib.rs:466`) reach memo observations only with `record_usage` on (`agent.ctg/src/lib.rs:811`); `context:last` keeps one overwritten request (`agent.ctg/src/context.rs`). Not delivered. Frontmatter key was `capability-capability-owner` and the footprint named four nonexistent paths (`agent.ctg/model_loop.rs`, `run_state.rs`, `context.rs`, `tests/loop.rs`). Policy no longer holds a tool catalog (decision `a-cartridge-brings-its-own-surface`); dispatch outcomes are now host outcomes (`c9ef10b`). All three needs are done.

Presented revision: prd.md SHA-256 `65d774da2bd242ad886f05c551175c349a7995071b70b3559d255768a723eca5` (rebased from `58c020445ead238069765236abe195ca234b52ccab31d850cbb0f6a9549abf63`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One inspection outcome; digests and references only. −1: "reload" identity depends on how the ported agent reloads. |
| Ownership and reuse | 19 | Agent joins what declared needs return; reuses descriptor digests and context snapshot; records policy's decision, not rules. −1: typo key fixed but provider identity source not yet confirmed in router output. |
| Dependencies and slices | 18 | All needs resolve and are done. −2: events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | Four checks incl. fallback/reload (round-1 note restored) and host outcome kinds; baseline cites lines. −2: gate cannot build until the port. |
| Failure, recovery and compatibility | 18 | Unavailable references recorded, never inferred; attribution never fails dispatch; old transcripts load. −2: storage bound for per-dispatch references unstated. |
| Reviewer total | **92 / 100** | |

Findings and concrete revisions: (1) starting-file links resolved to nonexistent `boards/model_loop.rs`/`boards/run_state.rs`; run state now lives in `agent.ctg/src/lib.rs` and `run_state.rs` is a test module under `.cartridge/tests/unit/` — replaced with real paths and a footprint. (2) Fixed `capability-capability-owner` to `capability-owner` (value unchanged). (3) Moved the compatibility prose out of acceptance into a testable check. (4) Added fallback/reload attribution from round 1.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased). Partial delivery noted above; not DELIVERED.
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (92/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: after the events port, write the two-round probe and specs.
