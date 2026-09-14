# the-agent-spawns-wakes-and-owns-sub-agents — review

Canonical PRD: [@agent/the-agent-spawns-wakes-and-owns-sub-agents](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-agent-spawns-wakes-and-owns-sub-agents](../../../root/reviews/round-1/the-agent-spawns-wakes-and-owns-sub-agents.md): reviewer 82/100; Revise. Define durable wake deduplication, parent-exit policy, concurrency limits and trusted child identities; add crash/replay refusal tests.
  Original SHA-256: `0ece558d3688427cc241d40248e094c89117d1f2142f7d79905afa64275a9726`.

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

Reconciliation verdict: **REBASE**. Outcome still wanted; the agent has no spawn surface (`agent.ctg/src/lib.rs:235`). Changes since the plan: services are now declared events with host outcomes (cartridge.ctg `ee7e295`, `c9ef10b`); each cartridge documents its surface in `.cartridge/help.md` (decision `a-cartridge-brings-its-own-surface`); the sessions parent/mailbox prerequisite is done (`sessions.ctg/src/mailbox.rs:132-175`). The acceptance required a "current PTY lease" but no lease exists in `pty.ctg/src`; the owning leaf `@pty/improve-pty-input-ownership` was not a need. Round-1's owner-routed readback check had been dropped in migration.

Presented revision: prd.md SHA-256 `892b057344f13bd1e8515b16153a56e108fd24b51ae2ece2e274a840eadd6acc` (rebased from `5280a276c29495a41d96e1fc3fa0bcbfbfb35886531c78e9dece10341f2a0304`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | One sub-agent lifecycle outcome with owned shell. −2: spawn/send/wait/peek plus disposal is at the upper bound of one leaf (324 words). |
| Ownership and reuse | 18 | Reuses sessions lineage/mailbox and per-session `Control`; surface documented in help.md per decision. −2: lease semantics owned by pty and not yet specified. |
| Dependencies and slices | 17 | Both needs resolve; PTY lease need added. −3: `@pty/improve-pty-input-ownership` is open and stale-after-migration (its own footprint cites nonexistent `pty.ctg/main.rs`); events-port precondition has no PRD. |
| Observable acceptance and baseline | 19 | Four checks incl. crash-at-most-once, concurrency, forged owner, owner-routed readback. −1: gate cannot build until the port. |
| Failure, recovery and compatibility | 18 | Refused spawn writes nothing; over-limit `declined`; restart exposes unknown without replay. −2: parent disposal policy for still-running children not chosen. |
| Reviewer total | **90 / 100** | |

Findings and concrete revisions: (1) starting-file links resolved to nonexistent `boards/model_loop.rs`/`boards/run_state.rs`; run state now lives in `agent.ctg/src/lib.rs` and `run_state.rs` is a test module under `.cartridge/tests/unit/` — replaced with real paths and a footprint. (2) Added the PTY lease need. (3) Surface rebased to declared events with help.md. (4) Restored owner-routed readback and spawn→wake→report checks from round 1.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (90/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: wait for the PTY ownership leaf and the events port; then probe spawn→wake.
