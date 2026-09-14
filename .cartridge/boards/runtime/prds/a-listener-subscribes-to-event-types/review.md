# a-listener-subscribes-to-event-types — review

Canonical PRD: [@runtime/a-listener-subscribes-to-event-types](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-listener-subscribes-to-event-types](../../../root/reviews/round-1/a-listener-subscribes-to-event-types.md): reviewer 82/100; Revise. Once-only delivery contradicts drop-on-hang without an acknowledgement/replay protocol; choose delivery semantics and test replay cursor/gap handling.
  Original SHA-256: `3ba9951a739bf40a0b5ad5b393620e6c4407cd02409d0aa9c693ee53377a52e8`.

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

Reconciliation verdict: **REBASE** (largely delivered; remaining gap narrowed). Delivered by the host rewrite (939e7d1, ee7e295, e4cf5e9, c9ef10b): typed `listen` declarations with schema checks (`docs/transport.txt`), per-edge tokens for sender attribution (`src/host/mod.rs:652` `caller`), bounded queues (`src/transport/rpc.rs:47`), hung-listener timeout without blocking (test `a_hung_listener_times_out_and_its_node_keeps_serving`), stream replay with `since` (test `streams_replay_and_then_deliver_live`), restart keeping dependents (test `a_restart_keeps_its_dependents_working`). Not delivered: `src/transport/cartridge.rs:502-535` replays from a bounded in-memory history without signalling a gap and restarts `seq` at 1 per publisher process (source reading; unreproduced). The stale revision's durable journal/ack protocol, absent `runtime.rs`/`service.rs` paths and the `@agent/an-event-declares-its-type` need (agent model-projection authority, not a prerequisite for host channels) no longer fit.
Stale presented revision: `089a9e4d969d8b41eef2fc25f1c3772752f1bdcfdad55f826c7094eb8ea63a57`. Revised revision: `53ef0a03e8554ba91180cc83a54f9b2fdeb52146345e3026c002834bd26de51f`.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 18 | Silent loss on resubscribe is a real correctness gap; scope narrowed to it. -2: restart-seq defect unconfirmed. |
| Ownership and reuse | 19 | Transport crate owns channels; reuses history/join. -1: overlap with document-event-activation declared but not yet removed from that child. |
| Dependencies and slices | 19 | Dead cross-board need dropped with reason. -1: sibling overlap needs coordinator acknowledgement. |
| Acceptance and baseline | 18 | Three observable checks next to an existing test. -2: both defects must be reproduced first. |
| Failure and compatibility | 18 | Clients ignoring `kind: gap` keep working; slow-subscriber disconnect preserved; bounded memory kept. -2: epoch wire change needs a compatibility note for native modules. |
| Reviewer total | 92 / 100 | |

Result: **PASS**. Findings: reproduce before specs; coordinator should strip "overflow reports a gap" from `document-event-activation`. Unresolved blocking findings: none.
Validation: cheap existence checks only — ls/rg over cartridge.ctg (HEAD c9ef10b), tools.ctg (caea5b7) and memory.ctg (c25af4d) source; `just --list` at /Users/feb/dev/cartridge; relative-link resolution over prd.md; `shasum -a 256`. No product gates were run.
Reviewer: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2. Next action: write failing reproductions, then specs.
