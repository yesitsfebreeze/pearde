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


# Listener replay plan review, round 4

Plan: `@runtime/a-listener-subscribes-to-event-types`. Reviewer: `/root/listener_reviewer`, independent of the analyst. Claim: `coordinator-codex-2`. Review date: 2026-09-19. Result: **FAIL, 85/100**. Disposition: revise before implementation. Three inherited rounds were present; this substantive review uses round 4 of 5 and leaves one round. No user rating was supplied or required.

## Presented inputs

The implementation repository HEAD is `8da102215640bedf9b11d4f3325abec34bf639a2`. The working source is dirty, including foreign trace work. Digests below bind the actual working files, not just HEAD. Paths are relative to `/Users/feb/dev/cartridge`.

| Input | SHA-256 |
| --- | --- |
| `prd.ctg/.cartridge/boards/runtime/prds/a-listener-subscribes-to-event-types/prd.md` | `c40031555c15bb434781618afdda070ca8b2a32e1990461428ddd6b8dfafec0e` |
| `prd.ctg/.cartridge/boards/runtime/prds/a-listener-subscribes-to-event-types/review.md` | `85b0afe0b9b32cf500f7784d0b5ab83eac08c92fe11ae812e349d02189813ce6` |
| `prd.ctg/.cartridge/boards/runtime/prds/a-listener-subscribes-to-event-types/specs/spec01.md` | `fce7db80e3969b9c0c3f3ffa26b7b66cee59a6a31893c10bec3f59ec80029fd7` |
| `prd.ctg/.cartridge/boards/runtime/.state/loop/a-listener-subscribes-to-event-types/analyst-1.md` | `90cfde999c0ed6c0262f710bcf0c7640c440d9d8c559efaf3fa8b273e1445584` |
| `cartridge.ctg/src/transport/cartridge.rs` | `1b8ce1e6de04cf95ccd716310081cdd504793dfb473e0c707be16abefe2118d1` |
| `cartridge.ctg/src/transport/rpc.rs` | `02ac29262dc7dfb1d27610ddbda5f17ec3d247d360ca3d582e203b47f4558ab9` |
| `cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs` | `3bac988054d468da5ce6684b3747c937b59119444672a806559dc86a94e8639f` |
| `cartridge.ctg/docs/transport.txt` | `8a257d0114ec1db55a6d5ad6c2da6832ced2936f877795fcbf0458b9c9320298` |
| `cartridge.ctg/README.md` | `04b0c387f6b5b5c2e5dd5bc8054f6cc3325d273e8d66808052c07b5559f44b36` |
| `cartridge.ctg/.cartridge/help.md` | `9ac645a5e2e3a7b7b52d7d6dd98419a3e577e97f330ad7f37e9419f799f85c04` |

## Scores

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Silent truncation and restart cursor loss are reproduced through the public RPC boundary. The bounded-memory outcome is coherent. The current PRD still says neither defect is reproduced and cites obsolete gates. |
| Ownership and reuse | 19 | Runtime transport owns the channel and watcher. The approved five-file footprint includes all required public documentation. Shared dirty source and documentation require preserving the integrated baseline. |
| Dependencies and implementable slices | 16 | One implementation slice and no false event-type dependency. The proposed queue reservation is insufficient for the actual shared Peer, so its mechanism and possibly footprint need revision. |
| Observable acceptance and baseline evidence | 17 | Seven named acceptance items cover restart, exact gaps, ordinary replay and slow readers. Existing baseline evidence is honest. Tests do not yet require occupied/shared RPC queues or cursor continuity after an enqueue failure. |
| Failure, recovery and compatibility | 14 | Epoch-aware cursors and current-generation numeric semantics are sensible. The proposed queue capacity arithmetic and successful-enqueue-only cursor rule do not yet prevent silent loss in the cases below. |
| Reviewer total | 85 / 100 | Two unresolved behavioral blockers remain. |

## Blocking findings and precise revisions

### B1. Reducing history to QUEUE minus three does not reserve shared queue capacity

`rpc.rs:135–148` closes a Peer when its outgoing queue is full. `cartridge.rs:641–653` reuses one client Peer for a publisher, while the subscribe handler at `866–881` performs synchronous replay and replies before its next incoming receive. No yield is guaranteed between ready subscribe requests. Two queued subscriptions to full channels on the same Peer can therefore enqueue their replays back-to-back on a current-thread runtime before the writer drains. The second replay overflows even when the remote subscriber drains promptly. Already queued replies or live frames consume the same purported three reserved slots; concurrent publication after `join` releases its lock can do so too. A history bound is not a reservation against other producers.

Revise step 6 to specify actual bounded replay admission/draining coordinated with the shared outgoing queue. State how replay, its gap, subscribe notification, reply and subsequent live frames stay ordered without holding the channel lock across an await or waiting inside `publish_kind`. Genuine downstream saturation must still disconnect; a healthy peer must not be deterministically disconnected simply because two replay requests are already ready. Do not solve this by replacing a full required replay with an invented retention gap, increasing a fixed spare-slot constant, or introducing an unbounded buffer. A bounded replay pump or another concrete capacity-aware mechanism is acceptable if its ownership, cancellation and ordering are described. Amend the footprint if that design requires `rpc.rs`.

Add named tests for two full-history channel subscriptions on one Peer, and replay with pre-existing control/live frames queued on that Peer. Run the deterministic cases on a current-thread runtime, receive the complete replay and RPC replies, then prove live delivery. Keep the original full-retention test and actual slow-peer disconnect proof. These are source-established counterexamples to the proposed mechanism; I did not claim to execute a proposed implementation.

### B2. Successful enqueue is not enough to make a cursor safe after a failed enqueue

`cartridge.rs:687–697` closes the Peer when the watcher queue is full but continues the incoming loop. The RPC incoming receiver may still contain notifications. If envelope N fails to enqueue, the callback then drains a slot, and envelope N+1 successfully enqueues, the current pump advances its cursor past N. The proposed step 5 preserves this possibility: it requires advancing only on successful enqueue, but says nothing about stopping advancement after the first loss. Reconnect can then request after N+1 and silently omit N even though N is retained.

Specify that the saved cursor represents a contiguous accepted prefix within its epoch. After the first watcher enqueue failure, later buffered notifications for that subscription must not advance it past the missing envelope before recovery. Stopping forwarding on the failed connection and reconnecting from the last accepted cursor is one possible implementation; account for all watchers sharing that connection. Avoid regressing delivery to an independent draining subscriber or blocking the publisher.

Add a deterministic test that blocks a callback, fills its queue, induces a failed enqueue, releases callback capacity while later incoming envelopes remain, then reconnects. Prove that the failed sequence is replayed before later accepted data, or is covered by an exact retention gap if deliberately evicted. Merely observing a disconnect/reconnect and eventual latest data does not prove this property.

## Accepted decisions and integration requirements

The additive `StreamCursor { epoch, seq }` and `subscribe_from` path satisfy publisher-restart recovery provided the actual SDK watcher automatically sends the pair, as the spec requires. The existing numeric API remains useful for positions in a known current generation; it cannot identify a former generation, and documentation must say so. This is not permission to leave existing automatic reconnect numeric-only. The host-replacement and second-reconnect tests correctly prevent that narrower substitute. A restart gap must identify the changed epoch without fabricating a numeric missing range across generations. Recovery of discarded previous-generation memory is outside the explicit bounded-memory contract.

The inclusive retention range, subscriber-local gap, checked arithmetic and replay-before-live ordering are specified clearly. The test matrix includes smaller, equal and larger sequence values after restart and an initially empty generation. Subscribe replies must not regress a cursor already advanced by replay. Reading the existing test reveals that `streams_replay_and_then_deliver_live` exercises live Lua delivery, not saved-cursor replay; keep it as a compatibility regression, and rely on the new direct replay tests for replay evidence.

The five-path authored footprint is now present in PRD frontmatter, so the draft's preapproval sentence is historical editorial residue rather than an unresolved authorization request. Preserve foreign trace edits in `State`, construction, `publish_kind` and request handling, and foreign ASP/launch documentation edits in README and help. The source and documentation hashes above capture that baseline. Do not commit the unrelated hunks as listener work. A clean lane must start from a coordinator-integrated baseline; the source file now references dirty trace infrastructure outside this leaf's footprint.

The overlap with `document-event-activation` has already been reconciled: its current PRD delegates gap and restart cursor shape to this leaf, and its round-3 review explicitly drops its duplicate overflow requirement. Do not spend another round re-resolving that historical overlap. Update the current leaf's body in place to replace unreproduced claims and obsolete `just` gates with the observed evidence and current task gates, and correct its stale inherited-round prose. Preserve frontmatter ownership and history.

Verify blocks comply with the supplied engine facts: repo-relative commands, isolated `CARGO_TARGET_DIR`, exact named tests, no absolute checkout switch and no source writes. Their lane and integrated execution must both be preserved. Full compilation may require prebuild outside the 120-second collection blocks, as already stated.

## Validation and next action

I ran `./task prompt` first, then task discovery. I consulted ASP before code lookup, read the review workflow and templates, Rust router/concurrency skills, and the prove-it-works principle. I inspected the PRD, spec, review history, analyst report, actual transport/watcher/RPC implementation, existing tests, node subscription call, dirty diffs and input hashes. Commands were read-only except writing this report. All started commands completed; no background work remains. Initial `./task cartridge` was an invalid recipe; direct `cartridge call asp` succeeded. Searches for historical `src/core` paths confirmed those paths are absent; the actual Lua entry is `src/node/mod.rs`.

I read `/tmp/listener-probe.log` and `/tmp/listener-baseline.log`: the analyst's public probe observed 1024 replay data frames, no gap and a closed subscribe reply; its fresh-publisher numeric-cursor probe observed no data; the existing stream baseline test passed. I did not rerun product gates or claim the future tests pass. These logs plus the source explain the baseline failures; implementation must supply permanent regressions and full verification.

Next action: the coordinator records round 4, makes one coherent revision addressing B1 and B2 with their regression requirements and any necessary footprint change, then requests the fifth independent review. Do not implement or reset the review allowance before that gate.


# Listener replay plan review, round 5

Plan: `@runtime/a-listener-subscribes-to-event-types`. Reviewer: `/root/listener_reviewer5`, a fresh independent reviewer who did not author this revision. Date: 2026-09-19. Result: **PASS, 94/100**. Disposition: keep and proceed to implementation. Four historical rounds remain consumed; this review uses round 5 of 5. No user rating was supplied or required.

## Presented revision and bindings

The implementation base is cartridge.ctg commit `8da102215640bedf9b11d4f3325abec34bf639a2`. The published PRD and spec have the same six-path footprint, including `src/transport/rpc.rs`. The PRD remains `state: "analyzing"` with claim `coordinator-codex-2 2026-09-19T17:28:07.199Z`. Its inherited review frontmatter is historical, not evidence that this candidate had already passed. This report does not change any planning record or transition.

The following SHA-256 values bind the actual inspected working inputs. Paths are relative to `/Users/feb/dev/cartridge`.

| Input | SHA-256 |
| --- | --- |
| `prd.ctg/.cartridge/boards/runtime/prds/a-listener-subscribes-to-event-types/prd.md` | `86d44c58931e242ea57f28316b7e35c2ad4a2c5d370157d45f09419f3db6262f` |
| `prd.ctg/.cartridge/boards/runtime/prds/a-listener-subscribes-to-event-types/specs/spec01.md` | `4d8c73ded408c85554f75793f61697546fa0449324781b4eb13047654f645f62` |
| `prd.ctg/.cartridge/boards/runtime/prds/a-listener-subscribes-to-event-types/review.md` | `bc4cac139eb17e92d37bb1b297c870bf3e21609de43b379f3ebc333939241b9c` |
| `prd.ctg/.cartridge/boards/runtime/.state/loop/a-listener-subscribes-to-event-types/analyst-codex-revision-5.md` | `65d2cb65f18fd393aab242b9bcf36497f8b00c53ebd272c6598ee3914a4f8eb2` |
| `cartridge.ctg/src/transport/cartridge.rs` | `1b8ce1e6de04cf95ccd716310081cdd504793dfb473e0c707be16abefe2118d1` |
| `cartridge.ctg/src/transport/rpc.rs` | `02ac29262dc7dfb1d27610ddbda5f17ec3d247d360ca3d582e203b47f4558ab9` |
| `cartridge.ctg/.cartridge/tests/unit/src/tests/host.rs` | `3bac988054d468da5ce6684b3747c937b59119444672a806559dc86a94e8639f` |
| `cartridge.ctg/docs/transport.txt` | `8a257d0114ec1db55a6d5ad6c2da6832ced2936f877795fcbf0458b9c9320298` |
| `cartridge.ctg/README.md` | `04b0c387f6b5b5c2e5dd5bc8054f6cc3325d273e8d66808052c07b5559f44b36` |
| `cartridge.ctg/.cartridge/help.md` | `9ac645a5e2e3a7b7b52d7d6dd98419a3e577e97f330ad7f37e9419f799f85c04` |
| `cartridge.ctg/Cargo.toml` | `4508a9b67ec1332782746ac225a9e9c9e86bf45c1b7bfa6a5fc8070d1aecc600` |
| `cartridge.ctg/Cargo.lock` | `896732590aaae296f2ce57ab3de945d3800e9bf36d3a62636feadfaa4343045b` |
| `prd.ctg/.cartridge/templates/spec.md` | `0350746f33dde5398bf620c7982e5fe3c8163ff2e0c4879436631393704020ad` |
| `prd.ctg/.cartridge/workflows/review-plan.md` | `1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9` |

I also inspected the committed cartridge source, not just its dirty working version. At the named base commit, `src/transport/cartridge.rs` has SHA-256 `d74dd9fd975fdf8633c9f3e65c45b121984fb3147a9639bcb755ac0381561e8c`, `README.md` has `adccc26100a67dec964583d1967e2c84d2a021c9e35397f45130e57d703a9a8e`, and `.cartridge/help.md` has `a5761f5d3c3eb5a9d16cadb5df2fde1b6ef0ee67e115b281ff85a3c354a4efc4`. The other three footprint files have the same committed and working hashes listed above. Foreign trace and documentation edits are integration constraints, not planning blockers.

## Scores

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The public probe demonstrates truncated replay without a gap and lost restart replay. The revision preserves the bounded-memory outcome and current-generation numeric compatibility. The repair necessarily changes subscription scheduling as well as cursor shape. |
| Ownership and reuse | 19 | Runtime transport owns both relevant queues, Request reply ownership, and the watcher. The footprint includes these mechanisms and all three required documentation surfaces. Integration still requires careful separation from foreign trace hunks. |
| Dependencies and implementable slices | 18 | The six paths cover the implementation, production-path test seam, and public contract. Dedicated stream admission, atomic snapshot/tail handoff, one startup per Peer and explicit task ownership form an implementable design. The cancellation and replacement state machine is substantial and needs disciplined implementation review. |
| Observable acceptance and baseline evidence | 19 | Named tests now exercise both shared-Peer counterexamples, the enqueue hole with exact reconnect cursor, restart matrices, bounded shutdown and the receive-pump fence. Existing logs establish the two original baseline defects. The old stream test only proves live delivery; the new production-path regressions must establish actual replay. |
| Failure, recovery and compatibility | 19 | Contiguous accepted cursors, connection-wide stop, late-reply exclusion, bounded retry, finite admission waits, task reaping and two distinct teardown fences address the identified failure modes. Shutdown sink writes and local replacement ordering remain important implementation proof obligations. |
| Reviewer total | 94 / 100 | No unresolved blocking finding. |

## Resolution of the previous blockers

**B1 is resolved in the plan.** The current `Inner::push` closes on a full shared ordinary queue, and ready subscription handlers can execute without writer progress. The revision no longer reserves fictitious spare slots by reducing HISTORY. A separate finite stream queue and awaited admission allow a full replay to yield to the same writer that drains it. Fair alternation preserves ordinary traffic progress. Serial startup acknowledgement limits captured startup history to one snapshot per Peer while already established pumps continue draining. The publisher only uses nonblocking tail sends under the channel lock. Genuine tail saturation still closes the affected Peer; the plan does not fabricate a retention gap to avoid replaying retained frames.

The history snapshot, tail registration and sequenced subscribe control share a single channel-lock boundary. That prevents a live envelope from overtaking replay or obtaining a sequence earlier than the startup control after the snapshot. Sending gap, replay, subscribe control and reply through the same FIFO lane preserves the necessary per-subscription order. Interleaving distinct channels is explicitly allowed. The two current-thread tests require all retained frames and both replies, and the occupied-queue test forces actual waiting before releasing the writer. These tests would detect the old spare-capacity assumption.

**B2 is resolved in the plan.** Current `pump` closes on `Full` and continues receiving; `fetch_max` can consequently skip a failed frame when callback space later becomes available. The revision stops that entire old connection pump at the first failure and drops its incoming receiver before replacement. Accepted callback contents remain queued, but no later old-connection envelope can advance any affected watcher. Recovery uses each watcher's synchronized epoch/sequence prefix. The named regression requires observing the outgoing request at N-1, then N before later data, and includes both a second watcher on the failed Peer and an independent healthy Peer. Its eviction variant requires a precise gap instead of merely eventual latest-data delivery. The observation seam cannot decide failure or alter queue capacity, so it does not supply the property it claims to test.

## Ordering, cancellation and finite bounds

The revision correctly distinguishes a writer barrier from receiver progress. `rpc::dispatch` resolves replies directly through pending oneshots, while notifications await delivery through `incoming`. An unsubscribe reply therefore cannot prove that the SDK pump has consumed preceding notifications. The explicit internal fence and watcher tombstone cover that boundary. The implementation must apply that rule before installing a replacement watcher, including direct duplicate subscription, as required by the replacement contract; merely adding the publisher-side barrier is insufficient.

The concrete memory bound is HISTORY plus at most two startup envelopes for one starting subscription per Peer; QUEUE tail frames plus one pending admission per active subscription; two QUEUE outgoing lanes and one writer frame per Peer. Existing channel history, incoming queues and callback queues remain bounded at their existing cardinalities. Total storage still scales with subscriptions and channels, exactly as acknowledged; the plan does not falsely claim a new global byte or subscription-count limit.

Cancellation consumes or disarms Request ownership before an admission future can be dropped, preventing its existing Drop implementation from sending a second reply through the ordinary queue. The connection owns and reaps subscription tasks. The plan honestly defers a queued unsubscribe until startup finishes or fails rather than assuming the serial handler can receive it concurrently. Peer closure and host stop interrupt startup and admission waits. Bounded admission timeouts and retry backoff prevent infinite capacity waiting or recovery spinning.

Implementation review must verify the existing writer's `writer.send(frame).await` and close/drain awaits are included in the stated shutdown budget. Selecting cancellation only outside those awaits would not satisfy the published requirement. This is a concrete verification of an existing explicit requirement, not a request to change this plan. Likewise, the required cancellation test must include the receive-pump fence case specified in its preceding mechanism section. Existing RPC tests cover ordinary replies, dropped Request errors and close propagation; they do not independently establish bounded flush against a permanently blocked writer. The newly required blocked-admission/host-stop regression must provide that evidence.

## Validation and limits

I ran `./task prompt` first, then `./task task` for this review, read PROMPT.md, the review method/templates, canonical PRD/spec/history and revision report, and used the Rust router and concurrency skills plus the prove-it-works principle. ASP search identified the current Peer source before targeted code lookup. JEV returned a completed fallback assessment (`ebd9061a-3ebf-4cde-bf54-2e889f491580`, timeout within 7905 ms), with no selected evidence or validated decision, so I gathered evidence directly.

Read-only shell commands inspected HEAD, the actual working and committed transport source, Request Drop/reply, writer/reader dispatch, watcher and reconnect paths, host fixtures, RPC tests, documentation claims, manifest and diff statistics. All completed with exit 0. Python computed the SHA-256 bindings, confirmed 13 exact `pass:` requirements across the two test blocks and four cargo invocations, and printed the unchanged PRD state/claim. I read the existing `/tmp/listener-probe.log`: full retention produced 1024 data frames beginning at sequence 77, no gap and a closed subscribe reply; the restart probe produced zero data. `/tmp/listener-baseline.log` records the existing stream test passing. I did not rerun those product tests or claim that the future implementation tests pass.

Verify commands are relative to the selected cartridge repository, initialize an isolated CARGO_TARGET_DIR, require exact named tests and do not write source-footprint files. They preserve both lane and integrated execution. Prebuilding outside the 120-second collection window is explicitly allowed. No substantive plan revision is requested by this review.

Unresolved blocking findings: **none**. Rounds used / remaining: **5 / 0**. Next action: the coordinator records this revision-bound PASS and proceeds through the normal specced/implementation gate. Implement against the named clean host base; integrate listener hunks while preserving foreign work; independently verify the full published acceptance and gates before collection. A later substantive plan change cannot silently reuse this score or reset the five-round allowance.

Only this report was written. No source, PRD, spec, canonical review, frontmatter, transition or commit was changed. All started processes have finished; no background command remains.
