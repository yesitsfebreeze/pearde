---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters
needs:
- "@landscape/landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters/session-context-provider"
- "@landscape/landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters/terminal-context-provider"
- "@landscape/landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters/route-context-provider"
---

# Live owners answer context with scoped metadata

Roll-up only; claim a leaf. By decision `a-cartridge-brings-its-own-surface`, memo carries no other cartridge's protocol: a live owner offers evidence by defining and listening to its own `context.<kind>` event, as fs does with `context.file` and memory with `context.memory`. The earlier shared "live-owner adapter" is therefore split into one provider per owner. Each provider consumes the trusted caller scope from `@memo/landscape-live-owner-context-facade` and reuses the owner's delivered or specced metadata operation.

## Acceptance

- [ ] Each provider leaf is done with revision-bound proof and a passed review.
- [ ] At pinned memo, sessions, pty and router revisions, one `context` prepare naming `session`, `terminal` and `route` returns rows for exactly the caller's scope, with distinct owner and kind references, under one shared deadline.
- [ ] A provider that times out or is removed reports `timeout` or `absent` for its own kind only. No payload, credential or connection state appears in any row.

## Work items

- [Sessions answers context with scoped session metadata](session-context-provider/prd.md)
- [Pty answers context with terminal lifecycle metadata](terminal-context-provider/prd.md)
- [Router answers context with redacted route explanations](route-context-provider/prd.md)

## Integration gate

From `/Users/feb/dev/cartridge`: `just test memo`, `just test sessions`, `just test pty`, `just test router`, and `bun test memo.ctg/.cartridge/tests/integration/context.test.ts`. None has run for this plan.

## Review

[Review history](review.md). Rounds 1–2 are inherited through `live-file-context-contributors`; round 3 split this item. Each leaf may rehome to its owner's board.
