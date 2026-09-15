---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# `space` becomes a field on the entity — a declaring part lands in `behaviour`, undistilled, unvectored, unrecalled and beyond the tick's reach

## Do

`Entity` gains `pub space: String` beside `claim_kind` in
`src/base/src/base_types.rs`, empty for everything memory writes today.
`FORMAT_VERSION` moves 12 to 13 in `src/store_core/src/lib.rs` and the v12
layout is snapshotted into `src/store_core/src/legacy.rs` the way v11 is —
that file's header already names the steps for the 13 bump.

`split_front_matter` (`src/ingest/src/ingest_worker.rs`) reads the part's
`kind:` already; the watcher sink (`src/ingest/src/ingest_file_watcher.rs`)
derives `space` from it — `behaviour` for a declaring kind, empty otherwise —
and threads it beside `claim_kind` through `DirectJob` and `worker.submit`,
the same wire [kind-is-a-field](../kind-is-a-field/prd.md) cut.

A behaviour job skips distill and embed: frontmatter and edges, no vector,
no statements. With no vector it cannot be a seed, so recall never reaches
it; the query path filters it out of lexical hits by space.

`src/base/src/base_retention.rs` is the one place removal is decided
(`tests/removal_policy.rs` fails the suite when a second copy appears): a
behaviour row is not collectable by the tick and carries no TTL, while an
operator naming the row may still forget it — authority stays monotone, the
invariant that file exists to hold.

## Acceptance
A test in the ingest crate: a `kind: routine` part through the watcher sink
lands with `space == "behaviour"`, an empty vector and no statements; the
same store answers `query` for its text with nothing; `is_cold_victim`
refuses the row while `forget` by id accepts it. The format-version checksum
test passes at 13.

Landed: `Entity.space` beside `claim_kind`, `FORMAT_VERSION` 12 -> 13 with the
v12 layout frozen in `legacy.rs` and its mirrors pinned in `legacy_test.rs`.
`space` is derived in `ingest_worker::job()` — the one gate every producer
already passes for the confidence clamp — rather than threaded through
`DirectJob` and `submit`: it is a pure function of `claim_kind`, which both
legs already carry, so the wire this item planned to widen needed no change
and the durable leg gets the same answer for free. A behaviour job clears its
TTL there, skips the embed and the chunk split, and lands its body in one
context chunk with no statements — and `entity_document` is the statements, so
the lexical index is fed nothing and a search for the body's own words answers
nothing without a filter on the query path. `base_retention::may_remove` gains
one arm under `Automatic` alone, so the tick cannot reclaim a declaration while
`forget` by id still takes it.

The check runs as
`ingest_file_watcher_test::a_declaring_part_lands_in_the_behaviour_space_and_out_of_memory`,
against a dead embedder: a row that arrives at all is one that spent no embed.
