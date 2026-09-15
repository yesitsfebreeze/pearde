---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 3
review-status: delivered-pending-verification
canonical-scope: one-search-covers-the-record-and-memory
---

# one-search-covers-the-record-and-memory

Use landscape-composes-system-context as the canonical implementation and retain this record as memory-contributor acceptance. Memory stays optional and owns exact fact retrieval; metadata-only candidates are query-bounded before body hydration.

## Acceptance

- [ ] A memory-only phrase and a memo/tool phrase produce correctly attributed hits from one query.
- [ ] Returned memory IDs read back exactly through the surviving memory adapter; missing/deleted facts are explicit, not replaced by a semantic requery.
- [ ] Disabled memory yields useful remaining results; configured unavailable memory yields named partial status within the deadline and no second writer.

## Proof and recovery

Start at [lib.rs](../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `one-search-covers-the-record-and-memory`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `work/one-search-covers-the-record-and-memory.md` (status open, estimate 4h). The PRD state above is authoritative.

> One ranked search answers what exists across the record and the memory store, instead of a tool per store

### Outcome

One query returns the best matches across everything the system remembers: the
record's memos, the tools and cartridges the landscape already graphs, and the
memory store's facts. A caller asks once, with a situation in its own words, and
does not choose a store first.

The memory store keeps its own tool for writing and for reads that are about
memory as memory (ingest, entity lookup); what goes away is having to know which
of two searches to ask in order to find out that something exists.

Scope is retrieval. Merging the two stores is explicitly not the outcome: the
record stays the record, memory stays memory, and the graph stays derived from
both rather than becoming a third copy.

### Check

- [ ] `tool.memo {"op":"landscape","query":"<a phrase only a memory fact
      matches>"}` returns that fact as a hit, with its kind naming the memory
      store and a reference the caller can read it back by.
- [ ] The same call still returns memo, tool and cartridge hits for phrases they
      match, ranked against the memory hits by the same score and observed use.
- [ ] A profile without the memory cartridge answers the same query with the
      record and tool hits and no error — memory is an optional contributor, not
      a dependency of the search.
- [ ] Memory hits carry no content the caller did not ask for: the hit is a
      description and a reference, and reading the fact is a second call.
- [ ] `just check` and `just test` pass.

### Approach

Observed 2026-09-12. [the-memory-bank-is-wired-into-the-surface](../../../root/prds/the-memory-bank-is-wired-into-the-surface/prd.md) is done, so
`memory` and `memory-tool` are composed and `tool.memory` exists — but the
landscape graphs cartridges, tools and memos only
(`builtin/landscape/src/surface.rs`), so the two stores are two separate
searches and a caller has to guess which one holds what it needs.

The shape already fits: `Node` carries `kind`, `key`, `description`, `when` and
`tags`, and `compose` takes its sources as flat JSON rows, so memory
contributes rows the same way the record does. `builtin/memo`'s `landscape` op is
where they meet; it already describes every injected `tool.*` key, so reaching
the memory store is an existing dependency rather than a new one.

Two things to settle while building: memory rows are potentially many, so the
graph needs a bound (the record's scan is already capped — see
`MAX_MEMOS`/`MAX_RECORD_BYTES`), and a memory hit's `key` must be a reference
`tool.memory` accepts, so a hit leads to a read without the caller constructing
a query. Sits under the same ranking the resolver's observation journal feeds, so
a memory fact that gets used outranks one that never does.

Related: [agents-query-the-tool-graph](../../../root/prds/agents-query-the-tool-graph/prd.md) is the caller's side of this (active,
owned elsewhere) — this memo is what it has to search.
