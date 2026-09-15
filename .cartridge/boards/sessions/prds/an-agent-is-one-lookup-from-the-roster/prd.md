---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: an-agent-is-one-lookup-from-the-roster
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
needs:
- "@harness/scoped-roster-context-contributor"
- "@sessions/the-board-is-channels-of-lines"
---

# an-agent-is-one-lookup-from-the-roster

Build a scoped read projection over sessions and durable channel cursors. Identify the source revisions and observation time of each contributor; unavailable state is partial rather than a falsely atomic global snapshot. Supply the bounded prompt projection through Landscape/harness.

## Acceptance

- [x] A 20-session fixture stays within configured row/byte caps and reports omitted rows and unread counts.
- [x] Only authorized sessions/channels appear; copying another client's metadata cannot reveal its roster.
- [x] Reading advances only the requesting session's cursor, concurrent posts are not skipped, and a child phase change appears on a fresh query without a board post.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [the-board-is-channels-of-lines](../../../../memos/work/root--the-board-is-channels-of-lines.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `an-agent-is-one-lookup-from-the-roster`; maximum five rounds.

## Owner split

The [durable named-channel cursor child](durable-channel-read-cursors/prd.md) supplies authenticated delivery progress; the [scoped roster child](scoped-roster-projection/prd.md) reads existing session/channel metadata; the [harness adapter](../../../harness/prds/scoped-roster-context-contributor/prd.md) renders it through the existing Landscape collector. Original acceptance above and rounds1–2 remain unchanged; [pre-split leaf](original-leaf-prd.md) preserves the prior contract. Missing activity duration remains unknown. This parent requires actual composed prompt evidence and all dependency receipts.

## From the retired work memo

Folded 2026-09-15 from `work/an-agent-is-one-lookup-from-the-roster.md` (status open, estimate 1d). The PRD state above is authoritative.

> One call, and one rendered block, tell an agent every live session, what it is doing and what it has not read

### Outcome

Who is doing what is a lookup, not a conversation. One `roster` call returns
every live session with its id, name, parent, phase, what it is doing now, how
long it has been at it, the channels it watches, and its last posted line. The
same roster is rendered into the system prompt as one bounded block, so an agent
starts a run already knowing the shape of the swarm without asking, and asks
only to refresh.

The roster is a projection of state the sessions store already keeps. Nothing
about it requires reading another agent's transcript.

### Check

- [ ] `roster` returns one row per live session with id, parent, phase, current
      activity, age and last line; a session that has never run shows a phase
      rather than an absent field.
- [ ] The rendered roster block appears in a composed system prompt, is blank
      when no board service is configured, and stays under its configured size
      cap with twenty live sessions.
- [ ] A child's phase change is visible in the next `roster` call without any
      post to a channel.
- [ ] The block names each session's unread count per watched channel, and the
      count drops after that session reads.
- [ ] Two agents calling `roster` concurrently get consistent rows, and neither
      call blocks a running turn.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. `sessions list` already returns every session, and `create`
records `parent` while `update{agent}` merges agent state including `phase`,
which the store guards against conflicting changes during a run
(`builtin/sessions/main.rs:503`, `:505`, `:541`). So parent, phase and activity
exist; what does not exist is a single projection of them plus the board's unread
counts, and a way for that projection to reach the model without a tool call. The
harness already renders exactly this kind of block: `environment` and `terminal`
are placeholders filled from a service named by `harness.<name>` config, blank
when unset (`builtin/harness/README.md:136`).

### Spec

`roster` is a read-only op on the board service, computed from the sessions store
and the channel index: no new state, so it cannot disagree with what the store
says. Rows are ordered parent-first, then by age, so the tree reads top down.

The prompt block follows the existing pattern exactly: a `swarm` placeholder
filled from the service named by `harness.board`, blank in a profile that has no
board, capped in size and escaped like the other rendered values. A profile that
wants the roster in the prompt names the service; a profile that does not gets
the cost of nothing. That keeps the "dynamic list of context" a bounded render of
live state rather than a growing transcript.

Cap before render: the block carries at most N rows and one line each, with a
count of what was omitted. An agent that needs more calls `roster` — the block is
the cheap default, not the complete answer.
