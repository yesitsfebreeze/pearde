---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: the-swarm-talks-on-a-board
---

# the-swarm-talks-on-a-board

Coordinate the linked owner outcomes and record their combined evidence; claim a leaf for implementation. Channels, cursors and the roster already exist in `sessions.ctg/src`; the open leaves add the agent tool and post event, typed references, and the ordered replay.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance.
- [ ] At one pinned sessions revision, a two-actor fixture posts with references, restarts the sessions node mid-exchange, and replays the exchange from `follow` with no lost or duplicated line.
- [ ] An actor presenting another actor's `from`, or a reference outside its scope, is refused during that run, and the refusal appears in neither actor's unread lines.
- [ ] Remaining limitations are recorded at that revision, including that coalescing wake bursts into one run is a harness listener's outcome, not this parent's.

## Work items

- [an-agent-is-one-lookup-from-the-roster](../an-agent-is-one-lookup-from-the-roster/prd.md)
- [the-agents-chat-through-one-tool](../the-agents-chat-through-one-tool/prd.md)
- [a-board-message-is-a-reference-not-a-payload](../a-board-message-is-a-reference-not-a-payload/prd.md)
- [the-board-log-replays-who-did-what](../the-board-log-replays-who-did-what/prd.md)

## Integration gate

From /Users/feb/dev/cartridge: `just test sessions` against the baseline recorded by the first leaf (release-status lists 8 failing sessions tests), plus the two-actor fixture added to `sessions.ctg/.cartridge/tests/integration/`; neither has run for this plan.

## Review

[Review history](review.md); rounds inherited, maximum five.

## From the retired work memo

Folded 2026-09-15 from `work/the-swarm-talks-on-a-board.md` (status open). The PRD state above is authoritative.

> A message board with channels, a roster, a terse referencing protocol and a followable log, so many agents share one context cheaply

### Outcome

Agents and sub-agents coordinate on a message board instead of in each other's
prompts. Channels carry short lines; a roster answers who is doing what in one
lookup; messages carry references into the shared record rather than copies of
it; and one ordered log replays who did what. The result is a planning force with
many tools and a small context: an agent's per-turn cost is a bounded roster
block plus the lines it has not read, not the history of everyone else.

This is the coordination half of [sub-agents-share-the-terminal](../../../agent/prds/sub-agents-share-the-terminal/prd.md): that memo
owns spawning, ownership of the visible shell and the panel that shows children;
this one owns how they talk. The visible shell stays the owner's, and a board
post is never an execution path.

| Work | Estimate |
| --- | --- |
| [the-board-is-channels-of-lines](../the-board-is-channels-of-lines/prd.md) | 1d |
| [an-agent-is-one-lookup-from-the-roster](../an-agent-is-one-lookup-from-the-roster/prd.md) | 1d |
| [the-agents-chat-through-one-tool](../the-agents-chat-through-one-tool/prd.md) | 2d |
| [a-board-message-is-a-reference-not-a-payload](../a-board-message-is-a-reference-not-a-payload/prd.md) | 1d |
| [the-board-log-replays-who-did-what](../the-board-log-replays-who-did-what/prd.md) | 2d |

### Check

- [ ] Every child is done: a `tool.memo` list of kind `work` shows each memo
      named in this memo's `subwork` with `status: done`.
- [ ] `just test` carries a swarm probe in which one planner and two workers
      complete a task through the board alone: the probe asserts the planner
      read no worker transcript and that every handoff line carries a reference.
- [ ] The same probe replays its log through `follow` as an ordered story naming
      each actor, and records the planner's rendered prompt size with two and
      with eight workers, both within the configured roster and unread caps.
- [ ] With the board cartridge removed from the profile, that probe's tool-list
      assertion shows no `board`, a record index shows no board memos, and a
      composed prompt shows no roster block.

### Approach

Observed 2026-09-12, reading `builtin/sessions/main.rs`. More exists than the
board needs to invent. A session already records a `parent` at `create` and
carries agent state including `phase`, which the store guards during a run
(`:505`, `:541`); `list` returns every session (`:503`); and a durable mailbox is
already implemented — `send{id,from,text}` appends a JSON line to the target
session's `mailbox` buffer and notifies with that session as the event target,
`mailbox{id}` reads it back (`:666`, `:682`). The tool surface is a glob, so a
cartridge providing `tool.board` reaches the agent and MCP with no second
registration (`.zirkle/default/init.lua`, `.zirkle/mcp/init.lua`). The harness
already renders bounded live blocks from a service named by config
(`builtin/harness/README.md:136`).

What is missing: a channel name that is not a session id, a sequence number, a
read cursor, one roster projection, a protocol the tool enforces, and one
ordering across sessions.

### Spec

The board is a cartridge over the sessions store, not a new store and not an
external service. Two decisions follow from that, stated here so the children can
assume them.

The board is local. An existing chat product would give a human UI for free, but
it would put auth, network latency, rate limits and a third party between agents
that share a machine, and it cannot hold the ordering that
[the-board-log-replays-who-did-what](../the-board-log-replays-who-did-what/prd.md) needs. So the substrate is `sessions`, and
a bridge that mirrors a channel into an external chat for human reading is a
separate, optional cartridge — worth building when watching matters more than
coordinating, and not before.

Terseness is enforced, not requested. The line cap in
[the-board-is-channels-of-lines](../the-board-is-channels-of-lines/prd.md) and the reference forms in
[a-board-message-is-a-reference-not-a-payload](../a-board-message-is-a-reference-not-a-payload/prd.md) are what make the protocol hold;
the routine memo the board cartridge ships teaches the rest. A rule that lives
only in a prompt is a rule the next prompt rewrite loses.

Order of work is channels, then roster, then the tool, then the protocol, then the
log. The first two are cheap and independently useful — a roster over today's
mailbox already answers who is doing what.
