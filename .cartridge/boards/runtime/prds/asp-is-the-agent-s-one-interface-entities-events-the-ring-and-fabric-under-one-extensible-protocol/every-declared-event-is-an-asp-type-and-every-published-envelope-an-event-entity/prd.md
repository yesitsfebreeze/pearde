---
state: "deferred"
superseded-by: "@root/the-event-ring-keeps-every-event-forever-by-rolling-it-into-day-week-month-and-year-tiers-under-asp"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
  - '@runtime/a-listener-subscribes-to-event-types'
  - '@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/an-event-declaration-carries-a-host-validated-frame-and-a-cartridge-can-read-its-own-declared-events'
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp
  - /Users/feb/dev/cartridge/cartridge.ctg/src/transport/cartridge.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/transport.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp
---

# every declared event is an ASP type and every published envelope an event entity

## Outcome

Every event a cartridge declares in `cartridge.json` is an ASP type, and
every envelope the host publishes is an `event:` entity (host-owned, keyed by
channel, epoch and sequence). Each carries edges to the entities its payload
names: the agent that raised it and the target it acted on. The event system
and ASP describe one world. An agent can follow an event into the entity it
touched, or ask an entity which events touched it.

## Start at

- `cartridge.ctg/src/transport/cartridge.rs:474-486`: `publish_kind`, the
  single point every `publish` and `notify` passes through. The ASP tap goes
  here.
- `cartridge.ctg/src/transport/cartridge.rs:23` and `:152-199`: the
  in-memory `HISTORY = 1024` and the `seq` that starts again at 1 on restart.
  `@runtime/a-listener-subscribes-to-event-types` adds the epoch this PRD
  keys on.
- `cartridge.ctg/src/loader/document.rs:7-50`: the `Cartridge` and `Event`
  manifest structs, both `deny_unknown_fields`.
- `cartridge.ctg/docs/transport.txt`: event semantics.

## Decision (2026-09-19, ASP coordinator): superseded by the ring

Box 1 (a declared event is an ASP type carrying its schema) was delivered by
`the-base-contributes-tools-cartridges-and-event-types-to-asp` (cartridge.ctg
a2c5962): `asp types` lists every declared event with its owner and schema.
Boxes 2 and 3 (`event:` entities tapped at publish, keyed with the epoch)
need the same node-to-host tap the durable ring needs, because
`publish_kind` runs in each node, not in the host. The ring row
`@root/the-event-ring-keeps-every-event-forever-by-rolling-it-into-day-week-month-and-year-tiers-under-asp`
owns that tap and the `event:` scheme, so this row is deferred in its favour.

## Acceptance

- [ ] A named test declares an event in a fixture cartridge. ASP lists it as a
      type, carrying the event's schema.
- [ ] A named test publishes an envelope whose payload names a `file:`, and
      expanding that `file:` returns the `event:` with its edge.
- [ ] The `event:` identity survives a publisher restart, because the epoch is
      part of the key.
- [ ] `cartridge help host` and `cartridge.ctg/docs/transport.txt` describe
      events as ASP entities.
