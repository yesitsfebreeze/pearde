# Event activation resumes from a durable cursor — review

Canonical PRD: [@runtime/documents-own-live-processes/document-event-activation](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [documents-own-live-processes](../../../../root/reviews/round-1/documents-own-live-processes.md): reviewer 85/100; Split. Separate sidecar lifetime from event activation; settle event acknowledgement/deduplication and handoff of exclusive listeners or writers before implementation.
  Original SHA-256: `75f4d40c468a29f7c36d7ca8c32ca4d4111e67422c49c65aa3986eb3b1101404`.

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
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14

Reviewer: agent (independent reviewer, plan refresh pass). No user score was supplied or invented.

Reconciliation verdict: **REBASE**. Aligned with the parent's round-3 REBASE.
- Event subscriptions are channels on the transport route: `cartridge.subscribe` (`src/node.rs`) into `Ctx::subscribe` and the connection loop in `src/transport/cartridge.rs` (ws/cartridge.ctg `transport-design` `ba198f4`).
- As the coordinator directed, "queue overflow reports a gap and recoverable journal cursor" is dropped; `@runtime/a-listener-subscribes-to-event-types` owns the gap envelope and restart `seq`. That leaf also settles "there is no durable journal", so the "durable cursor" title is replaced.
- The need on `document-command-result` (CONFLICT in this pass) is replaced by a hard need on the listener leaf, whose cursor wire format `since` must follow.

Source findings, reading only:
- A repeated subscribe on one connection replaces the prior entry (`if let Some(at) = subscriptions.iter().position(...)` then `leave`), and a closed connection leaves every subscription. The "reload produces no duplicate subscriptions" theme therefore already exists in source but is untested; it is kept as regression proof, not new work.
- The Lua bridge always passes `since: None`, so a replaced subscriber cannot resume. That is the new behavior.

Stale presented revision: `cca059bc915076ba8052a81963aa7bd69763cc5af85214304977d065e876a42c`. Revised revision: `prd.md` SHA-256 `79f028b8483021d48ba29a87f271e66a6d97e3667b9443f2c729d4e7ac2d1597`.

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 18 | Envelopes silently lost across a subscriber restart are a correctness gap; scope is one optional argument plus two regression proofs. -2: the value depends on subscribers persisting their own cursor. |
| Ownership and reuse | 19 | The base owns the bridge and channels; the leaf reuses `join` replay and history. -1: the overlap with the listener leaf needs coordinated landing. |
| Dependencies and implementable slices | 18 | One hard need, which resolves (passed round 3) and is acyclic. -2: the shared footprint `src/transport/cartridge.rs` and the need's unsettled epoch shape can block specs. |
| Observable acceptance and baseline evidence | 18 | Three checks next to `streams_replay_and_then_deliver_live`; which checks must fail first is stated. -2: the regression claims are source reading. |
| Failure, recovery and compatibility | 18 | Omitting `since` is today's behavior; no durable journal is claimed; rollback named. -2: the answer for a `since` from an older publisher epoch is delegated to the need. |
| Reviewer total | 91 / 100 | |

Result: **PASS**. Word count 299 with frontmatter (`wc -w`; leaf bound 150–300).
Findings: the regression tests may pass immediately; record that as evidence, not as new behavior.
Unresolved blocking findings: none.
Validation (read-only): source reading on ws/cartridge.ctg branch `transport-design` `ba198f4` (`src/node.rs` `spawn`/`Spawned`/reader task/`request`/`kill`, global `subscribe`; `src/transport/cartridge.rs` `join`/`leave`/`subscribe`, connection loop subscribe/unsubscribe/disconnect; `src/host/mod.rs` `stop_slot`/`replace_locked`); existence of the named tests in `.cartridge/tests/unit/src/tests/host.rs`; main cartridge.ctg `e8a4da3` carries the same files; needs resolution under `boards/<owner>/prds/<slug>/prd.md` (`@runtime/launch-authority`, `@runtime/extension-loader-plugin-tree`, `@runtime/a-listener-subscribes-to-event-types` exist, passed round 3); root `.cartridge/justfile` `test`/`check` and the `runtime` routing in `.cartridge/memos/routine/cartridge-development.md`; `wc -w`; `shasum -a 256`. No product gates were run.
User rating: not required under delegation; none supplied.
Rounds used / remaining: 3 / 2.
Next action: after the listener leaf fixes the cursor shape, write the failing `since` test.
