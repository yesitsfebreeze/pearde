---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# one embed lane means a read waits for the whole write backlog — a query embed queued behind an intake drain of 2,268 jobs never returns, so reads need the front of the lane

Landed: the embed lane grew a second end. `EmbedLane` (`src/llm/src/llm.rs`)
holds the one-permit semaphore beside a `watch<usize>` of reads waiting;
`Client::embed` joins the front, `embed_bulk` and `embed_batch` join the back
and hand the slot back when a read arrives while they queued, so a batch in
flight is never preempted. The write sites say which side they are on by the
name they call: `ingest_worker.rs:746`,
`src/commands/src/commands_focus.rs:59` and
`src/commands/src/commands_unnamed.rs:62` now call `embed_bulk`, and `embed_batch` is a write path by definition — its only
callers are `ingest_worker.rs:717` and `commands_reembed.rs:120,159`. The
query paths keep `embed` and get the front for free.
`a_read_takes_the_front_of_the_embed_lane` (`src/llm/src/tests/llm_test.rs`)
is the mechanism's proof: six bulk embeds queued on a 100 ms-per-request
server, a read issued 150 ms in, served 3rd or sooner — 7th of 7 when the
priority is removed. The `Check` below is a live measurement and still wants a
daemon running this binary against a non-empty intake; none is running here.

## Do

[embeds-go-through-one-lane](../embeds-go-through-one-lane/prd.md) gives memory the only queue for a one-slot
embedding server. A queue in arrival order is the wrong order: a `query` embeds
one short text and a caller is waiting for it, while the intake drain embeds
thousands of chunks that nobody is waiting for. Measured 2026-09-06, the
backlog was 2,268 intake jobs draining at 5.7 a minute — a read that lands
behind it is not slow, it is gone, and that is what an agent session saw as
`query` timing out at 120 s on a single word.

Give the lane two priorities and let the read take the front: the query embeds
(`commands_query.rs:80,129,289`, `server.rs:526`) ask for the lane ahead of the
ingest and admin embeds (`ingest_worker.rs:694,723`,
`src/commands/src/commands_focus.rs:59`,
`src/commands/src/commands_unnamed.rs:62`, `commands_reembed.rs:120,159`). A batch already in
flight is not preempted — the write path keeps its throughput between reads —
so the bound a read sees is one batch, not one backlog.

## Acceptance
With the intake drain running against a non-empty intake, twenty `query` calls
answer with a worst case under 5 s, and the drain's own rate over the same
window falls by less than a fifth.
