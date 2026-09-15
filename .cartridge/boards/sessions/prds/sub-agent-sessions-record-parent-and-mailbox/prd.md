---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: sub-agent-sessions-record-parent-and-mailbox
footprint: ["src/roster.rs","src/channels.rs","src/main.rs","src/mailbox.rs",".cartridge/tests/unit/main/mailbox_tests.rs",".cartridge/tests/integration/mailbox.test.ts",".cartridge/docs/mailbox.md","src/observations.rs","Cargo.toml","src/lib.rs","src/change_record.rs","src/changes.rs",".cartridge/tests/unit/main/change_records_tests.rs","src/context.rs",".cartridge/tests/unit/main/context_tests.rs",".cartridge/tests/integration/context.test.ts"]
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
---

# sub-agent-sessions-record-parent-and-mailbox

First verify the already-described parent/mailbox implementation. The remaining contract is authenticated sender/recipient scope, durable message identity, bounded ordered reads and restart-safe cursor handling; reuse current snapshots rather than introducing a second inbox.

## Acceptance

- [x] Creating a child records its parent and survives restart; forged parent or out-of-scope recipient is refused before writing.
- [x] A retry with the same message ID cannot append a second logical message, and concurrent messages retain distinct monotonic sequence positions.
- [x] Missing-session writes change nothing; current and legacy snapshots read correctly and unread cursors never acknowledge undelivered messages.

## Proof and recovery

Real SDK [baseline](baseline.json), source `b772c6e`: parent/mailbox behavior already works, but repeating message_id appends twice, messages have no sequence and bounded mailbox_read is absent. A parent string alone supplies no authenticated scope. Named/public channels remain a separate historical prerequisite; [mapping analysis](channel-prerequisite-analysis.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `sub-agent-sessions-record-parent-and-mailbox`; maximum five rounds.

Reverification: attributed report at2a6a863 adds native main dispatch; bind src/observations.rs as transitive source, retaining previous acceptance and executable gates.

Named channel registration revalidation at 423ecd32: source footprint includes registered channels and its shared mailbox codec; acceptance and behavior gates remain unchanged.

## From the retired work memo

Folded 2026-09-15 from `work/sub-agent-sessions-record-parent-and-mailbox.md` (status open). The PRD state above is authoritative.

> A sub-agent session records its parent, and messages travel through a durable mailbox on the sessions cartridge

### Outcome

A sub-agent is a session with `parent` recorded on it. `sessions create{parent}`
records the parent on the created session; `sessions get`/`list` expose it and
it survives restart. Messages to a session travel through a mailbox on the
sessions cartridge: `sessions send{id,from,text}` appends one message line to
the target session's mailbox buffer, notifies, and persists; `sessions
mailbox{id}` lists the messages back in order. The composer and the agent call
the same ops, so a message to an idle agent parks in the mailbox for the next
run; waking that agent is the agent cartridge's contract, not this one.

### Check

- [ ] `sessions create{parent}` records the parent on the session; `get`/`list`
      return it and the session's snapshot file contains it.
- [ ] `sessions send{id,from,text}` appends one message and `sessions
      mailbox{id}` lists messages back in order with `from`, `to` and `text`.
- [ ] Reloading the store returns the same parent and mailbox messages.
- [ ] `sessions send` to a missing session is refused without changing the store.
