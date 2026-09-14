# a-board-message-is-a-reference-not-a-payload — review

Canonical PRD: [@sessions/a-board-message-is-a-reference-not-a-payload](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [a-board-message-is-a-reference-not-a-payload](../../../root/reviews/round-1/a-board-message-is-a-reference-not-a-payload.md): reviewer 78/100; Revise. A byte cap cannot enforce reference-only content; add structured reference fields, cross-session scope checks and missing/stale-target behavior.
  Original SHA-256: `4fc2aa88bf167806c12b9a1f7e5780510ad78d489b14b58f603cd161581f022e`.

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

Reviewer: agent (independent reviewer, plan refresh pass).
Reconciliation verdict: **REBASE**. Outcome still wanted and not delivered: channel lines accept only `channel, from, ts, seq, message_id, run, text` (`records` in `sessions.ctg/src/channels.rs`). Changed since writing: sessions was ported to the transport protocol; decision `a-cartridge-brings-its-own-surface.md` forbids sessions carrying sibling protocols, so "resolution uses existing scoped read APIs" must mean the reader resolves other owners' targets, not sessions.
Stale revision: `91c4fce85718726c374819d8a5eebcfd711c861473534fed73ca1846ec357908` (start link `../../../main.rs` resolves to `boards/main.rs`, missing; typo owner key; resolution authority ambiguous).
Presented revision: prd.md SHA-256 `9b6e6e6c41a4e1ac343d2c0cded69cb71ad66fccdd1b04be17de7483341dc9d4`. Source inspected at sessions.ctg e9725e8 (ported to transport 0d4310f), memo.ctg 9a1cf99, agent.ctg working tree, cartridge.ctg c9ef10b (dirty working tree), prd.ctg 077e57a2 working tree.
Change: typed optional `references` with four owner-qualified forms; sessions dereferences only session/channel forms; conflict on same `message_id`; legacy compatibility; real start files and tests; caps as settings.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | Small posts pointing into the record. -1: the reporting-bytes measurement from round 1 dropped to guidance. |
| Ownership and reuse | 19 | Reuses channel append/dedup path and settings-based caps. -1: reference caps not yet named as settings keys. |
| Dependencies and slices | 18 | needs the chat leaf (resolves). -2: shares `channels.rs` with chat and log leaves. |
| Acceptance and baseline | 18 | Refusal leaves snapshot bytes unchanged; tests exist to extend. Current gate baseline: `.cartridge/memos/note/release-status.md` records 8 failing sessions workspace tests; the plan requires naming them before judging new failures. -2 for red baseline. |
| Failure and compatibility | 17 | Optional field, legacy lines unchanged. -3: an older binary reading a newer snapshot with references is not addressed (channel-cursors doc says older binaries may refuse). |
| Reviewer total | **91 / 100** | |

Result: **PASS**. Blocking findings: none.
Validation: file existence; `./prd.ctg/prd check` exit 0. Product gates were not run.
User rating: not required under delegation. Rounds used / remaining: 3 / 2.
Next: implement after the chat leaf; land after it in `channels.rs`.
