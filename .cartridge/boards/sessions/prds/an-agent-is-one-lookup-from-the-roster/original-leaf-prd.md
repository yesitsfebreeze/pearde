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
canonical-scope: an-agent-is-one-lookup-from-the-roster
---

# an-agent-is-one-lookup-from-the-roster

Build a scoped read projection over sessions and durable channel cursors. Identify the source revisions and observation time of each contributor; unavailable state is partial rather than a falsely atomic global snapshot. Supply the bounded prompt projection through Landscape/harness.

## Acceptance

- [ ] A 20-session fixture stays within configured row/byte caps and reports omitted rows and unread counts.
- [ ] Only authorized sessions/channels appear; copying another client's metadata cannot reveal its roster.
- [ ] Reading advances only the requesting session's cursor, concurrent posts are not skipped, and a child phase change appears on a fresh query without a board post.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

External evidence prerequisites: [the-board-is-channels-of-lines](../../../../memos/work/root--the-board-is-channels-of-lines.md). Resolve their current completion and source revision before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `an-agent-is-one-lookup-from-the-roster`; maximum five rounds.
