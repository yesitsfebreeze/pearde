# the-run-is-a-stream-of-typed-events — review

Canonical PRD: [@agent/the-run-is-a-stream-of-typed-events](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-run-is-a-stream-of-typed-events](../../../root/reviews/round-1/the-run-is-a-stream-of-typed-events.md): reviewer 81/100; Revise. Settle sender authority, acceptance durability, replay and cancel/preempt precedence across children; reconcile the parent's separate-signal rule with the child's proposed shared watch.
  Original SHA-256: `f28fe54314433ac5292c441412a2ec84ef8c6e625fb0620eac39850fa790bed4`.

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

Reconciliation verdict: **REBASE**. The goal stands, but much of its substrate moved into the host: declared events with schemas, per-edge sender tokens, per-listener outcomes with deadlines, bounded queues and channels with replay `since` (cartridge.ctg `ee7e295`, `c9ef10b`, `docs/transport.txt`). The runtime child `@runtime/a-listener-subscribes-to-event-types` may be largely delivered by host streams and still cites nonexistent `cartridge.ctg/src/runtime.rs`/`service.rs`. Round 1's separate-signal finding is resolved in the priority leaf.

Presented revision: prd.md SHA-256 `f07a62f9cd27a750b7271ecc0eb106d55b597e8639f612eb58cc7eb5b904ad3f` (rebased from `9ec9f7bcc3d4d7796ff991c8da52f0e041fb628faa1ecbcc1da0b29361a7f282`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Parent only; host substrate named so children do not rebuild it. −1: the typed-journal half depends on a harness counterpart. |
| Ownership and reuse | 18 | Reuses host events/channels; children agent-owned except the runtime listener. −2: listener leaf ownership vs host streams unreconciled. |
| Dependencies and slices | 17 | All needs resolve; landing order stated; acyclic (runtime listener needs `@agent/an-event-declares-its-type`, the stall leaf no longer needs the listener). −3: `an-event-declares-its-type` failed review; listener leaf stale; events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | One end-to-end check covering post, priority, stall, typed journal and cancel precedence; gates exist. −2: gates cannot build until the port. |
| Failure, recovery and compatibility | 18 | Cancel precedence preserved; limitations recorded. −2: no roll-up rollback boundary if a child lands and a sibling fails. |
| Reviewer total | **90 / 100** | |

Findings and concrete revisions: (1) integration check, landing order and gate added. (2) Host substrate cited; listener child flagged for reconciliation.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Disposition: keep (rebased). Coordinator: reconcile `@runtime/a-listener-subscribes-to-event-types` against host streams (possible DELIVERED/REBASE).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **PASS** (90/100).
Unresolved blocking findings: none for the parent.
Rounds used / remaining: 3 / 2.
Next action: children proceed in the stated order.
