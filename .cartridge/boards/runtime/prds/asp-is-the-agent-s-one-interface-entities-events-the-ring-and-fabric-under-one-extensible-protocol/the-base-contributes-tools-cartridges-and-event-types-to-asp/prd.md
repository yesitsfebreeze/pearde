---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/rank.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/plan.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp.rs
commit: "a2c59624f710afb0cef2278534c55ba5199e2a9f"
---

# the base contributes tools cartridges and event types to asp

## Outcome

The base is an ASP provider for what only it knows in full. It contributes
`cartridge:<id>` for every loaded cartridge, `tool:<name>` for every
`tool.<name>` event, and a `provides` edge between them, and its search finds
a tool by name and description. `types` lists every declared event with its
owner, description and schema.

This is the first part of moving the fabric into ASP. The fabric learned about
tools because memo and prd each announced `kind: tool` nodes on
`graph.announce`. The base already holds every tool event in its catalogue, so
no cartridge has to announce one. It is also the first acceptance item of
`every-declared-event-is-an-asp-type-and-every-published-envelope-an-event-entity`:
a declared event is an ASP type that carries its schema.

## Acceptance

- [x] A named test declares a tool event in a fixture cartridge. `types` lists
      the event with its owner and schema, expanding `tool:` and `cartridge:`
      returns both nodes and the `provides` edge attributed to `host`, and a
      search by the tool's description finds it.
- [x] `docs/asp.txt` says what the base contributes.
