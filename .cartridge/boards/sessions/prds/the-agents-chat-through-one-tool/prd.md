---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: the-agents-chat-through-one-tool
needs:
- '@sessions/an-agent-is-one-lookup-from-the-roster'
---

# the-agents-chat-through-one-tool

Keep channel/inbox state in sessions and express the board capability through the common owner document/executor path. Retain an existing tool.board compatibility binding only while consumers need it. A post is authenticated data and cannot directly execute or grant approval.

## Acceptance

- [ ] Idle wake bursts coalesce to one run with durable unread IDs; a restart neither loses accepted posts nor starts duplicate runs.
- [ ] Cross-scope posts and forged senders are refused; bounded text/typed references and queue limits are checked before append.
- [ ] Read/watch/unwatch survive restart with explicit cursor gaps; disabling the owner removes exposure/subscriptions while preserving durable channel data.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [the-board-is-channels-of-lines](../../../../memos/work/root--the-board-is-channels-of-lines.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-agents-chat-through-one-tool`; maximum five rounds.
