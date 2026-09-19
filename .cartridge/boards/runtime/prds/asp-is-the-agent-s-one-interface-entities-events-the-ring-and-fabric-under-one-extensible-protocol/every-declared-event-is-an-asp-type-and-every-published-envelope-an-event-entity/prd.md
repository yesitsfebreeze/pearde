---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
needs:
  - '@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on'
  - '@runtime/a-listener-subscribes-to-event-types'
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

## Acceptance

- [ ] A named test declares an event in a fixture cartridge. ASP lists it as a
      type, carrying the event's schema.
- [ ] A named test publishes an envelope whose payload names a `file:`, and
      expanding that `file:` returns the `event:` with its edge.
- [ ] The `event:` identity survives a publisher restart, because the epoch is
      part of the key.
- [ ] `cartridge help host` and `cartridge.ctg/docs/transport.txt` describe
      events as ASP entities.
