# Compare cartridge-native and Codex task outcomes reproducibly — review

Canonical PRD: [@agent/improve-agent-task-baseline](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [improve-agent-task-baseline](../../../root/reviews/round-1/improve-agent-task-baseline.md): reviewer 89/100; Revise. Freeze task count, repeated-run protocol and the decision the comparison will inform before evaluating; product comparison and same-model comparison remain separate.
  Original SHA-256: `5119c64692ee668fa9d3f7148c95d2969d5951d5a5885bc495688fef909af070`.

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

Reconciliation verdict: **REBASE**. The evaluation outcome is architecture-neutral and still wanted; nothing like it exists (no corpus, runner or Codex adapter in the composed tree). The plan's footprint and starting files pointed at loop sources that no longer exist at those paths and are not where an evaluation corpus belongs; the offline/live split from round 1 was lost; frontmatter key was `capability-capability-owner`. Tests now belong in `.cartridge/tests/` (decision `cartridge-repositories-keep-records-and-executable-memos`).

Presented revision: prd.md SHA-256 `ecf029b59e2b23a20965da766d79d896fad9bbc86423af9d060db55dee4603f2` (rebased from `7f2759437790e488f0ab7c6096e550dc628a93a0726b7728d09e6a145c4c1552`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | States the decision it informs, frozen corpus size and protocol; product vs same-model reports separate. −2: 301 words; eight tasks may not be enough to decide, which the plan does not acknowledge. |
| Ownership and reuse | 18 | Reuses `http_fake.rs` and the `loop` integration harness; corpus under `.cartridge/tests/eval/`. −2: agent owning a cross-product benchmark is a judgement call; Codex adapter owner unnamed. |
| Dependencies and slices | 18 | No hard needs. −2: the `loop` harness boots the host through the removed API; events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | Offline check inside `just test agent`; opt-in report contents enumerated; no-winner rule; corpus revisioning. −2: gate cannot build until the port. |
| Failure, recovery and compatibility | 18 | Crashed/unavailable runs reported; live spend needs explicit user authorization and stays out of gates. −2: credential isolation for the live run not specified. |
| Reviewer total | **90 / 100** | |

Findings and concrete revisions: (1) footprint moved from nonexistent loop paths to the corpus and `loop` test. (2) Fixed `capability-capability-owner`. (3) Restored the round-1 offline/opt-in separation and made live-model spend an explicit execution-time authorization.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (90/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: after the events port, build the offline wrong-patch fixture first.
