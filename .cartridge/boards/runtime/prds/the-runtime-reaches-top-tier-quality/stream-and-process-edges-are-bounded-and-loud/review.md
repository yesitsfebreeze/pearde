# Stream and process edges are bounded and loud — review

Plan: `@runtime/the-runtime-reaches-top-tier-quality/stream-and-process-edges-are-bounded-and-loud` (`prd.md`).
Scope: one leaf. Every queue has a bound, and every drop is visible.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: 1, from parent `@runtime/the-runtime-reaches-top-tier-quality` (round 1, 84 FAIL).

Use the shared [review method](../../../../../workflows/review-plan.md). Append rounds; never overwrite.

## Round 2 — 2026-09-14

Reconciliation verdict: **SUPERSEDED**.

Reviewer: agent (independent reviewer, plan refresh pass). Presented revision: `prd.md` SHA-256 `635a035b49702b2f96157521ae5f8510a4f6809ab20dd272d88c2c986ba285d1` (frontmatter only; prior text `9337ea174601daa7d609330c58d97745a733af31cf0484fbcd69e032e2d50ad6`).
Composition:
- root `24aa2be` (dirty);
- cartridge.ctg `main` `e8a4da3`;
- `ws/cartridge.ctg` `transport-design` `ba198f4`;
- prd.ctg `077e57a2`, dirty.

Evidence:

- **Deleted targets.** Every file and mechanism the PRD names was deleted by the transport rewrite `939e7d1`: `src/stream.rs` (history `try_send`, the byte counter, the slow-subscriber rule), `src/sdk.rs`, `src/process.rs` (`Child::drop`), the `Arc`-pointer identity in `src/cartridge.rs`, and `src/settings.rs:514`.
- **Streams.** They now live in `transport/cartridge.rs` as a `VecDeque` capped at `HISTORY = 1024`, with sequence numbers. A subscriber too slow for a notification is disconnected and resubscribes from its last sequence (`publish_kind` / `join`).
- **Process identity.** It is the host `generation: u64`.
- **Children.** A node is spawned with `kill_on_drop(true)`, its stdin is a lifeline, and a monitor task waits or kills within `shutdown_timeout` (`host/process.rs`).

The "bounded and loud" rule for queues was re-specified by `c9ef10b`. The `rpc.rs` module doc says both queues are bounded and that a full outgoing queue closes the connection. That commit exists **only on local unpushed `main`**. On `origin/main` / `transport-design` `ba198f4`, `src/transport/rpc.rs:175,185` still use `mpsc::unbounded_channel`. Landing it is the job of `the-in-flight-rewrite-lands-in-reviewable-commits`, which names the bounded queues as a part that must survive.

Residual gap, for the parent's next audit: replay from a `since` older than `HISTORY` gives no explicit gap marker; the client sees only a jump in sequence numbers.

Result: no score (verdict round). Status: `superseded-recommend-retire`. Do not change `state:`.
Unresolved blocking findings: none.
Validation (read-only):
- `ls src` on both lines;
- `rg 'try_send|unbounded|HISTORY|saturating|Arc::as_ptr'` on both lines;
- reads of `src/transport/rpc.rs:1-20,160-180` (`e8a4da3`), `src/transport/cartridge.rs:495-545` and `src/host/process.rs:20-158`;
- `shasum -a 256`.

Rounds used / remaining: 2 / 3.
Next action: retire once the landing leaf carries the bounded queues to `origin/main`.
