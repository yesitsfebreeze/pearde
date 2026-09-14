---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: the-agents-chat-through-one-tool
needs:
- '@sessions/an-agent-is-one-lookup-from-the-roster'
---

# Agents reach channels through one sessions tool and posts are announced as events

Channel storage is delivered: `post`, `read`, `channels`, `channel_watch`, `channel_read`, `channel_ack`, `channel_unwatch` and `roster` exist on the `sessions` service with durable per-actor cursors and receipts (`sessions.ctg/src/channels.rs`, `sessions.ctg/.cartridge/docs/channel-cursors.md`). No `tool.board` exists and sessions provides no `tool.*` key, so a model cannot use them. Under root decision `a-cartridge-brings-its-own-surface.md` sessions ships that tool itself and reaches wakers only by an event; posts are data and never grant approval.

## Acceptance

- [ ] Sessions provides one tool whose descriptor lists these operations, declares the read-only ones under `reads`, and maps each call to the existing op; the host supplies `access_token` outside model-visible arguments, and a model-supplied token or `from` for another actor is refused.
- [ ] Each newly accepted post emits one declared event carrying scope, channel, `seq` and `from` only; an idempotent retry with the same `message_id` emits none.
- [ ] After restart, watches and unread lines are unchanged; with the sessions cartridge disabled the tool and event are absent while channel files remain byte-identical.

## Proof and recovery

Start: `sessions.ctg/src/main.rs`, `sessions.ctg/cartridge.json`, `sessions.ctg/init.lua`, reference descriptors in `memo.ctg/src/service.rs` and `agent.ctg/src/model_loop.rs` (`reads`). First probe how a transport node learns the calling actor's credential; if no host path exists, stop and record the question. Record the `just test sessions` baseline (8 failing per release-status). Gates from /Users/feb/dev/cartridge: `just test sessions`, `just check sessions` (not run). Excluded: coalescing wake bursts into one run, which belongs to the listening harness. Rollback: remove the tool and event; stored channels are untouched.

## Dependencies and review

Needs the scoped roster (done). Prerequisite memo `the-board-is-channels-of-lines` is delivered in source. [Review history](review.md); rounds inherited, maximum five.
