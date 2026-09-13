---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "specced"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 1
review-status: passed
canonical-scope: the-board-is-channels-of-lines
needs: ["@sessions/sub-agent-sessions-record-parent-and-mailbox"]
commit: "a306370f10b78d94365b7832ce22ce8d10c09487"
---

# Durable scoped channels over the mailbox line primitive

Provide named append-only channels with ordered bounded reads and a catalogue in sessions. Reuse the authenticated mailbox authority and line codec/append rules; `session:<id>` addresses the existing recipient mailbox without migration or duplicate storage. Other channel names are shared only inside the host-provisioned actor scope. This canonical delta preserves the [historical active source and claim](../../../../memos/work/root--the-board-is-channels-of-lines.md) verbatim; it does not reclaim or certify that historical worker's work.

## Acceptance

- [x] Actual SDK concurrent posts assign distinct per-channel sequences, retry by message ID is idempotent, and channel lines/catalogue survive restart.
- [x] Forged senders/scopes, unauthorized direct reads, unsafe names/paths, oversized text and full/corrupt stores are refused without changing accepted data.
- [x] Ordered reads and catalogue obey row/byte limits with explicit remaining counts; cursors beyond the end return empty, and legacy send/mailbox lines are visible through the direct-channel alias without rewriting snapshots.
- [x] Pre-publication failures preserve earlier bytes; uncertain post-publication failures expose uncertainty and retries reconcile by ID. Notifications follow accepted publication only.

[Measured baseline](baseline.json): the current real SDK rejects post/read/channels, while direct authenticated mailboxes already persist ordered lines. Existing native and SDK mailbox tests remain compatibility gates. Single active writer is the existing snapshot contract. Durable read acknowledgements, watcher/wake routing, roster prompts and a global cross-channel causal journal remain their separate existing PRDs; this leaf exposes no execution or approval authority.

## Review

No scored review for the historical active memo was found in the round-1 inventory; it was explicitly excluded as active. First concrete delta review is pending, with any discovered prior rounds to be inherited before proceeding.
