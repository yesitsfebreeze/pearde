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
canonical-scope: durable-channel-read-cursors
needs: ["@sessions/the-board-is-channels-of-lines"]
commit: "a306370f10b78d94365b7832ce22ce8d10c09487"
---

# Durable watched-channel delivery cursors

Give each authenticated actor a bounded durable set of watched named channels and explicit read receipts. Keep channel read observational; acknowledge only a batch actually delivered to that actor. Reuse the existing scope snapshot, mailbox credential authority and publication boundary.

## Acceptance

- [x] Watch/read/ack survive SDK restart; only the authenticated actor changes its watched channels/cursor, and copied metadata cannot grant access.
- [x] Concurrent posts are not acknowledged by an earlier receipt; stale receipts conflict and uncertain acknowledgement is reconciled without skipping undelivered lines.
- [x] Bounds and all publication faults preserve accepted channel lines; legacy scope snapshots remain readable and direct mailbox behavior is unchanged.

## Baseline and review

The parent roster baseline records actual absent SDK operations at423ecd3 and existing harness/Landscape boundaries. This child inherits original roster review rounds1–2; independent round3 review is pending. Tests use disposable data, and no source implementation is authorized before review. Detailed proof/recovery is in specs/spec01.md.
