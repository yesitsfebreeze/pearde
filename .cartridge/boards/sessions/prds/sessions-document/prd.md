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
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: capabilities-live-with-their-owners
---

# Sessions declares a bounded read-only inspection surface of its own

The earlier plan exposed session inspection through a shared client document runner (`@mcp/clients-share-document-execution`). No such runner exists in current mcp, agent or proxy source; under root decision `a-cartridge-brings-its-own-surface.md` a cartridge declares its own surface and marks read-only operations with `reads` (as memo, memory, fs and docs do). Sessions exposes `list`, `get`, `diagnostics`, `recovery` and `roster` on its host-trusted `sessions` service, but `list` returns every session unpaged (`sessions_inner` in `sessions.ctg/src/main.rs`) and sessions provides no `tool.*` descriptor.

## Acceptance

- [ ] `list` accepts `limit` and an opaque `cursor`, returns exact IDs, `total` and `more`, and a cursor from a changed store is refused as stale rather than skipping or repeating sessions.
- [ ] `get` distinguishes `missing`, `corrupt` (with the diagnostics path) and `unavailable` (unreadable or unsafe file); no inspection call mutates a snapshot, journal or buffer, proven by byte hashes before and after.
- [ ] `sessions.ctg/.cartridge/help.md` documents paging and these outcomes, and an unpaged legacy `list` call keeps its current response shape.

## Proof and recovery

Start: `sessions.ctg/src/main.rs`, `sessions.ctg/src/recovery.rs`, `sessions.ctg/.cartridge/help.md`, tests `sessions.ctg/.cartridge/tests/unit/main/tests.rs`. First record the `just test sessions` baseline (release-status lists 8 failing sessions tests). Gates from /Users/feb/dev/cartridge: `just test sessions`, `just check sessions` (not run). Excluded: an agent tool binding and its `reads` declaration (owned by `the-agents-chat-through-one-tool`) and history content beyond metadata. Rollback: paging is opt-in; reverting restores the unpaged response.

## Dependencies and review

No hard prerequisites; the dropped mcp need is recorded in [review history](review.md). Rounds inherited from `capabilities-live-with-their-owners`, maximum five.
