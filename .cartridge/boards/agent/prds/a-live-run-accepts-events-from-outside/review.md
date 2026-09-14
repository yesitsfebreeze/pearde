# a-live-run-accepts-events-from-outside — review

Canonical PRD: [@agent/a-live-run-accepts-events-from-outside](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-live-run-accepts-events-from-outside](../../../root/reviews/round-1/a-live-run-accepts-events-from-outside.md): reviewer 83/100; Revise. Define authenticated sender identity, durable acceptance, queue bounds and the live-to-idle race so acknowledged posts cannot disappear.
  Original SHA-256: `d652c083b5975ff12947929313bbdf1455d27114ba2d76645f699acc5623d9df`.

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

Reconciliation verdict: **REBASE**. The outcome is still wanted, but the old contract (a host-authenticated `post` op into a new inbox) predates the host rewrite: senders are now authenticated per edge and payloads schema-checked by the host (cartridge.ctg `ee7e295`, `c9ef10b`, `docs/transport.txt`), and a sessions mailbox with authenticated actors and message-ID dedupe is delivered (`@sessions/sub-agent-sessions-record-parent-and-mailbox`, state done; `sessions.ctg/src/mailbox.rs:132`). Nothing in agent source posts today (`agent.ctg/src/lib.rs:235`). Not delivered.

Presented revision: prd.md SHA-256 `fb66166e1df080c5f97b716d52b1cf6ab2b904952d4c808c482d39585dbbfbeb` (rebased from `62094aeba7f2982e47838b5d5140fa8e67973f8cf4fe8e66a88f4da62e24358e`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | One outcome (posts reach a working run at whole boundaries), idle-session durability kept. −1: 308 words, slightly above the 300 aim. |
| Ownership and reuse | 18 | Reuses host edge authentication, schema checks and the done sessions mailbox instead of a second inbox. −2: durable acceptance spans agent and sessions; drain cursor semantics still to be probed. |
| Dependencies and slices | 17 | Both needs resolve (one done, one open); mailbox prerequisite now explicit. −3: `@agent/an-event-declares-its-type` is failing review; the events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | Four behavioral checks incl. crash replay, idle race, refusal; baseline cites source lines; gates exist. −2: baseline is source reading, not a fixture run; gate cannot build until the port. |
| Failure, recovery and compatibility | 18 | Declined-before-write, checkpoint-conflict retry from mailbox cursor, v1 transcripts readable. −2: idle-transition race strategy not chosen. |
| Reviewer total | **90 / 100** | |

Findings and concrete revisions: (1) starting-file links resolved to nonexistent `boards/model_loop.rs`/`run_state.rs`; `run_state.rs` is now a test module (`agent.ctg/.cartridge/tests/unit/run_state.rs`) — replaced with real paths and a footprint. (2) Post surface rebased to a declared, listened event with host outcomes (`answered`/`declined`). (3) Mailbox need added. (4) Restored the round-1 checks for single journal landing and tool-group integrity.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API ("provide, call, the Rust SDK crate and wire.ts are gone") and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (90/100).
Unresolved blocking findings: none.
Rounds used / remaining: 3 / 2.
Next action: coordinator adds the agent events-port prerequisite; then probe the post fixture and write specs.
