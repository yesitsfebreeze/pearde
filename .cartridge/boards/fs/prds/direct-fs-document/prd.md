---
repo: /Users/feb/dev/cartridge/fs.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: fs
work-kind: leaf
review-round: 3
review-status: superseded-recommend-retire
canonical-scope: capabilities-live-with-their-owners
needs:
- '@mcp/clients-share-document-execution'
---

# A document preserves guarded direct file edits

Document read/edit/write over direct disk storage; preserve its distinct opt-in semantics.

## Acceptance

- [ ] A stale edit refuses without overwriting newer bytes.
- [ ] Read/edit succeeds through the common runner with the intended cwd.
- [ ] A consumer census records why direct FS remains available; migration does not delete it.

## Proof and recovery

Start at [service.rs](../../../service.rs), [files.rs](../../../files.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test fs` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `capabilities-live-with-their-owners`; maximum five rounds.
