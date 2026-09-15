---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 80
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: rollup
review-round: 3
review-status: failed
canonical-scope: documents-own-live-processes
needs:
- '@runtime/documents-own-live-processes/document-sidecar-lifecycle'
- '@runtime/documents-own-live-processes/document-event-activation'
---

# Sidecars, event tools, and reload have explicit lifetimes

Processes a cartridge starts belong to the node generation that started them. So do its event subscriptions. None of them outlive it. In the current base, these are helper programs from `cartridge.spawn` ([node.rs](../../../../../../cartridge.ctg/src/node.rs)), channel subscriptions ([transport/cartridge.rs](../../../../../../cartridge.ctg/src/transport/cartridge.rs)), and replacement in `replace_locked`/`stop_slot` with a generation guard ([host/mod.rs](../../../../../../cartridge.ctg/src/host/mod.rs)). This parent only coordinates; claim a leaf.

## Acceptance

- [ ] Each linked leaf is rebased onto these paths, has revision-bound proof and passes its own review.
- [ ] At the same pinned revisions, `just test runtime` (cwd `/Users/feb/dev/cartridge`) passes and the included outcomes work together.

## Work items

- [A sidecar belongs to one ready owner generation](document-sidecar-lifecycle/prd.md). Its refusal-at-planning overlap is owned by [extension-loader-plugin-tree](../extension-loader-plugin-tree/prd.md).
- [Event activation resumes from a durable cursor](document-event-activation/prd.md). Its channel-gap overlap is owned by [a-listener-subscribes-to-event-types](../a-listener-subscribes-to-event-types/prd.md).

## Review

[Review](review.md). Inherits round 1 from `documents-own-live-processes`; at most five rounds.
