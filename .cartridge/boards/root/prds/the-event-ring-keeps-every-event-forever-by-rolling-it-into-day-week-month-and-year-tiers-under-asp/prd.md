---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
needs:
- "@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on"
- "@runtime/a-listener-subscribes-to-event-types"
---

# the event ring keeps every event forever by rolling it into day week month and year tiers under ASP

## Outcome

Every event any agent raises in this project stays reachable through ASP for
as long as the project exists, at a cost that stays bounded. The newest
events sit in a live ring of fixed size (1024 entries). When an entry falls
out of the ring, it is folded into the current day's tier. A finished day is
compacted into its week, a week into its month, and a month into its year. An
agent asks ASP for `event:` or `ring:` entities and gets the same answer shape
from every tier. Only the resolution changes as the tier gets older: single
events in the live ring, aggregated rows in the tiers.

## Context

The user's words (2026-09-19): "even if we do a history of 1024, it rolls over
into the day, into the week, into the month, into the year, so we get a
compacted list of every event session, backwards compatible." And: "pretty
much everything can live below the ASP. That means also the event stream and
the context ring."

Today the host keeps `HISTORY = 1024` envelopes per event kind, in memory
only (`cartridge.ctg/src/transport/cartridge.rs`). The count restarts at 1
when a publisher restarts, and nothing survives past the ring.
`@runtime/a-listener-subscribes-to-event-types` owns the gap envelope and the
per-generation epoch, and this PRD builds on both.

## Concept

- **Entry.** A ring entry names `agent → action → entity id → revision`, plus
  the event kind and time. It never carries a payload. The entity id is an
  ASP id such as `symbol:src/a.rs#main`, so following an entry is one ASP
  `expand`.
- **Tiers.** live (1024 entries) → day → week → month → year. A tier row
  aggregates by `(agent, action, entity id)`. It keeps the count, the first
  and last sequence and time, and the first and last revision, so an old row
  still says who did what to which entity and when.
- **Durable.** The tiers are written to disk under the project's state
  directory, so a daemon restart loses nothing but the live entries that were
  not yet folded.
- **Backwards compatible.** Every tier file carries a format version. A reader
  accepts every version it ever wrote, and compaction never rewrites an older
  tier into a newer format.
- **Under ASP.** The ring is an ASP provider for `event:` and `ring:` and
  contributes `touched` edges from `agent:` to the entities an event names.
  Asking ASP about a file therefore also returns who touched it recently and
  how often, with nothing extra to call.
- **Indexed by entity.** Each tier keeps an index from entity id to its rows,
  so "what happened to this entity" is answered without scanning the tier.

## Decision (2026-09-19, coordinator-b0)

cartridge-1f, the ASP owner, handed this row to cartridge-b0. The pre-draft
spec is `proposals/spec01-draft.md`, read at cartridge.ctg `d04ab33`.

- `publish_kind` runs in each node, not in the host (`src/node/mod.rs:114`),
  so the tap forwards the id fields of a published event to the host over the
  node's existing host connection, through one new host-socket method `ring`.
  The host takes the publisher from the node's token. Only `notify` and
  `publish` reach the ring.
- This row defines both `event:` and `ring:` as host-owned schemes. One row,
  not split.
- Counts go on the row nodes, not on the edges, so the ASP protocol does not
  change.
- A frozen `format: 1` fixture is the older-format test until a format 2
  exists.
- The epoch stays in the row key.
- No purge operation: deleting `.cartridge/.state/ring/` is the purge.
- The ring keeps no payload, only well-formed ids.
- The lane is cut after `@runtime/a-native-cartridge-s-outbound-call-does-not-block-its-own-node`
  and `@runtime/a-listener-subscribes-to-event-types` are collected. Both are
  cartridge-b0's since cartridge-cc closed, and both edit
  `src/transport/cartridge.rs`.
- Rollout needs `cartridge daemon --replace` with a clear from every running
  session. No manifest changes, so no trust step.

## Acceptance

- [ ] A named executed test publishes more than 1024 events, then asks ASP for
      the oldest one. The event is answered from the day tier as an aggregate
      row naming its agent, action, entity and revision range.
- [ ] A named executed test compacts a finished day into its week, and the week
      into its month. The same ASP query returns the same row shape at each
      tier.
- [ ] A named executed test restarts the daemon and asks for an event that had
      already been folded into a tier. The event is still answered.
- [ ] A named executed test reads a tier file written in an older format
      version, fixed in the test tree, and gets the same answer shape.
- [ ] A named executed test asks ASP to expand a `file:` entity and receives the
      ring's `touched` edges with counts, next to what the other providers
      contribute.
- [ ] Disk use is bounded and measured: a test records the tier size for 100k
      events over a synthetic year.
