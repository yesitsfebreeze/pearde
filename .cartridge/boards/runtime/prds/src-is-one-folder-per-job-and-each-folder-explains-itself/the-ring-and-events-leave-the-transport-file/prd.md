---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
blast-radius: high
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/transport
  - /Users/feb/dev/cartridge/cartridge.ctg/src/ring
  - /Users/feb/dev/cartridge/cartridge.ctg/src/events
  - /Users/feb/dev/cartridge/cartridge.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/transport.txt
---

# the ring and events leave the transport file

## Outcome

`src/transport/cartridge.rs` is 1023 lines and three jobs. It splits by job, and `src/transport` keeps only bytes on the wire (`typed.rs`, `rpc.rs`).

- `src/ring`: `Channel` (`seq`, `history`, `subscribers`), `HISTORY`, `Watcher`, `publish`, `publish_kind`, `join`, `subscribe`, `unsubscribe`. The ring becomes its own type that the event context owns, instead of a map inside `State`.
- `src/events`: `Directory`, `EventEntry`, `Address`, `Accept`, `Outcome`, `Prepared`, `validate`, `on`, `on_dispose`, `emit`, `bail`, `gather`, `ask`, `notify`, the `send` funnel, and the connection side: `Ctx`, `State`, `serve`, `listen`, `Access`, `Refused`, the client map.

No folder is named fabric; ASP is the fabric. What is left of the file after the ring leaves is the event transport that `ASP.md` calls "Events = communication".

## Acceptance

- [ ] `src/transport/cartridge.rs` does not exist. `src/transport` holds `typed.rs`, `rpc.rs` and their tests only.
- [ ] `src/ring` depends on `transport` and on nothing in `events`; `src/events` depends on `ring` and `transport`. Neither direction is reversed.
- [ ] The tests in `src/transport/tests/cartridge.rs` move with the code they test, and the stream tests (`streams_replay_and_then_deliver_live` among them) keep passing.
- [ ] Every caller names the new paths; nothing re-exports `transport::cartridge`.
- [ ] `@runtime/a-listener-subscribes-to-event-types`, the ring and event-entity PRDs under the ASP rollup, and the "Where the code is" table in `ASP.md` name the new files in their footprints and anchors, in the same change.
- [ ] `docs/transport.txt` describes transport only, and the event semantics it held are in a document named for events.
- [ ] `src/ring/README.md`, `src/events/README.md` and `src/transport/README.md` exist in the shape the parent's README child defines.
- [ ] `just test runtime` runs the same test names as before and all pass; `just check runtime` and `just isolation` report nothing.

## Proof and recovery

Lines 280-395 and 590-1010 of the file were not read when this was filed, so whether `serve` and the access checks separate cleanly from `Ctx` is unverified; the analyst settles that first. No behaviour change is intended: the one structural edit is giving the ring its own type. Land this before the PRDs named above are claimed, because they edit the same lines. Gates, cwd `/Users/feb/dev/cartridge`: `just test runtime`, `just check runtime`, `just isolation`. Not run.
