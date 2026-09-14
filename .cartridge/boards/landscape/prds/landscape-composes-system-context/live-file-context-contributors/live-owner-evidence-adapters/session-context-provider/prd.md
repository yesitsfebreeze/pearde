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
canonical-scope: landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters/session-context-provider
needs:
- "@memo/landscape-live-owner-context-facade"
- "@sessions/context-session-metadata"
footprint:
- /Users/feb/dev/cartridge/sessions.ctg/cartridge.json
- /Users/feb/dev/cartridge/sessions.ctg/init.lua
- /Users/feb/dev/cartridge/sessions.ctg/src/context.rs
- /Users/feb/dev/cartridge/sessions.ctg/.cartridge/tests/integration/context.test.ts
---

# Sessions answers context with scoped session metadata

sessions already has a read-only metadata observation (`src/context.rs`, operation `context_metadata`: id, parent, revision, phase and timestamps, with no transcript, mailbox body or agent payload). Today it is reachable only through the `sessions` event with a mailbox `access_token`. This leaf makes sessions define and listen to `context.session`, answering memo's `contribute` and `read` shapes (`memo.ctg/.cartridge/docs/context.md`) for the trusted `scope` that memo forwards.

## Acceptance

- [ ] A memo `context` prepare naming `session` returns rows with `reference.kind: session` for the scoped session and its in-scope parent only, carrying exactly the `context_metadata` allowlist.
- [ ] Readback is `available` while the row is unchanged and `changed` after the session's revision moves. An unknown or out-of-scope id, or a request without `scope`, is `unavailable`, and no session state or cursor changes.
- [ ] With sessions removed from the composition, `session` is `absent` and the other contributors keep their rows.

## Proof and recovery

Probe first: how sessions can trust the forwarded `scope` from memo's per-edge sender identity without a mailbox token. Record the answer before specs. Extend `.cartridge/tests/integration/context.test.ts`. Gates, cwd `/Users/feb/dev/cartridge`: `just test sessions`, `just check sessions`, `just isolation`. Not run. Rollback: remove the event; `context_metadata` stays unchanged.

## Dependencies and review

Needs the trusted scope from memo and the delivered metadata operation. Rounds 1–2 are inherited; this leaf was created by the round-3 split ([review](review.md)).
