# the-agents-chat-through-one-tool — review

Canonical PRD: [@sessions/the-agents-chat-through-one-tool](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [the-agents-chat-through-one-tool](../../../root/reviews/round-1/the-agents-chat-through-one-tool.md): reviewer 80/100; Reconcile. The older tool.board wrapper conflicts with document-owned capability migration; retain sessions storage and define authorized posts, wake coalescing and replay recovery.
  Original SHA-256: `554426cba7cb85bce9162acdb1b07ae5ef7af91896609c708b99e30cd4b7f4ff`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 18 | Resolved hard dependencies and child links; external prerequisites require recorded owner handoff. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **93/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **REBASE**. Partly delivered: channel ops, durable per-actor watches, receipts and acks exist (`sessions.ctg/src/channels.rs`, `sessions.ctg/.cartridge/docs/channel-cursors.md`, tests `channel_cursor_tests.rs`, `channel-cursors.test.ts`); prerequisite memo `the-board-is-channels-of-lines` is still `active` in the record but delivered in source. Changed: no `tool.board` exists to "retain"; sessions provides no `tool.*`; the host is event-based (transport, `cartridge.ctg/docs/transport.txt`); decision `a-cartridge-brings-its-own-surface.md` means sessions ships its own tool and reaches a waker only by an event. Wake coalescing into one run is a listener (harness) outcome, not sessions'.
Stale revision: `0e497f928e622e75ef3afa47971303d1b7b51f76d44390e19cdf0ca75263a3c3` (dead start link; retained a non-existent binding; re-planned delivered cursor/restart behavior).
Presented revision: prd.md SHA-256 `12c079d2252afb1ba00e671ca156421b5cf5909b82e0acf6312a88fe9fde391b`. Source inspected at sessions.ctg e9725e8 (ported to transport 0d4310f), memo.ctg 9a1cf99, agent.ctg working tree, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: scope reduced to the undelivered gap: one sessions tool with `reads`, host-supplied token, one post event per accepted post, disable behavior; credential probe with stop condition; wake coalescing excluded.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 17 | Makes delivered channels usable by models. -3: user-visible wake coalescing moved out and needs a harness owner. |
| Ownership and reuse | 19 | Maps to existing ops; `reads` pattern from `agent.ctg/src/model_loop.rs`. -1: tool key name not fixed. |
| Dependencies and slices | 18 | Roster need is done. -2: credential-to-actor binding on transport is unproven (probe with stop condition). |
| Acceptance and baseline | 18 | Forged token/from refusal, idempotent retry emits nothing, restart and disable byte-identity. Current gate baseline: `.cartridge/memos/note/release-status.md` records 8 failing sessions workspace tests; the plan requires naming them before judging new failures. -2. |
| Failure and compatibility | 18 | Removal leaves stored channels untouched. -2: event delivery failure (no listener, bounded queue full) outcome unspecified. |
| Reviewer total | **90 / 100** | |

Result: **PASS**. Blocking findings: none. Coordinator: create or assign a harness leaf "a burst of post events wakes one run".
Validation: file existence; `rg` for `tool.board`, wake/coalesce code (none); `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: run the credential probe first.
