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
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: landscape-live-owner-context-facade
needs:
- "@memo/landscape-file-kernel-context-facade"
---

# A context provider receives the trusted caller scope

memo already composes every injected `context.<kind>` provider through one collector and deadline ([context.md](../../../../../../memo.ctg/.cartridge/docs/context.md)), but `contribute` and `read` carry only query, limits and reference ([context.rs](../../../../../../memo.ctg/src/context.rs)). A live owner (sessions, pty, router) therefore cannot return only the caller's own metadata. memo owns this shape; live-owner providers remain their owners' work and consume it.

Trigger: a trusted native `context` request from a host session names a provider toggle. Response: the provider call adds a host-derived `scope` (`session`, optional `run`); the model tool and request body cannot supply or override it.

## Acceptance

- [ ] A fixture provider in `context.test.ts` receives the exact trusted session for `contribute` and `read`; a request-body field named `scope` never alters the forwarded value.
- [ ] A missing or disabled provider stays `absent`/`disabled` without activation, and other contributors keep their evidence under the shared deadline.
- [ ] Existing `context.memory`/`context.file` fixtures pass unchanged; a provider ignoring `scope` remains compatible.

## Proof and recovery

First probe where the service `Context` session reaches the context handler in [service.rs](../../../../../../memo.ctg/src/service.rs). Update the provider shape in `.cartridge/docs/context.md`. From /Users/feb/dev/cartridge: `just test memo`, `bun test memo.ctg/.cartridge/tests/integration/context.test.ts`, `just check memo`, `just isolation`. None has run for this plan. Rollback: revert the added field; no durable state changes.

## Dependencies and review

[Review history](review.md): rounds 1–2 inherited from `live-file-context-contributors`; round 3 rebased. Downstream live-owner providers should need this leaf.
