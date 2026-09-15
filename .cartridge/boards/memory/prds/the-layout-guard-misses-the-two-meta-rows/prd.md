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

# the layout guard pins `StoredMemory` and `ColdRow` and nothing else, so a field added to `GraphMeta` or `EmbedStamp` — both persisted through the same versioned encoder — changes the on-disk layout without moving a checksum

## Do

`src/store_core/src/tests/layout_guard.rs` exists because `FORMAT_VERSION`
"only identifies a layout if every layout change bumps it", and its header
records the time that broke: `f60fbce` added `Entity.trust_tier` without
touching `store_core`, leaving two incompatible layouts both calling themselves
version 10. It pins a bincode checksum over a fixture of each persisted row
type — two of them:

```
STORED_MEMORY_LAYOUT   sample_stored_memory()
COLD_ROW_LAYOUT      sample_cold_row()
```

Its nesting is careful and worth not re-deriving. `StoredVec` is pinned through
`entity_vecs` because `mk_entity` gives a non-empty `vec![0.0; 8]`;
`StoredTemporal` is pinned through `ColdRow.temporal`, which is a value rather
than a map and so encodes even at `default()`; and
`the_fixtures_actually_encode_something` guards against a fixture that encodes
to nothing. `temporal` and `reason_vecs` are empty inside `sample_stored_memory`,
which would have left their value types unpinned — those two other paths are
what covers them.

Two persisted types have no fixture at all. `GraphMeta { replica_id,
quant_mode }` is written at `lib.rs:686-692` and `EmbedStamp { model, dim }` at
`:573-578`, both through the same `encode` → `encode_at(FORMAT_VERSION, ..)`
that stamps every row. Add a field to either and the bytes on disk change shape
while both checksums hold — the version-10 ambiguity the file was written to
prevent, in the two rows that gate an open rather than carry content.

Add `sample_graph_meta()` and `sample_embed_stamp()` with their constants,
next to the two that exist. `GraphMeta` is private to `store_core`, so the
fixture belongs in that module either way.

**Done 2026-09-06.** `sample_graph_meta()` and `sample_embed_stamp()` sit beside
the two fixtures that existed, with `GRAPH_META_LAYOUT = 0x45dc_5d0f_17e5_158d`
and `EMBED_STAMP_LAYOUT = 0x2301_880b_08b6_9ef0`. Both constants were read off a
deliberately-wrong pin rather than computed by hand: set to zero, run, take the
number the failure prints. A checksum written from a calculation is a second
implementation of the encoder.

**Both guards were watched failing.** Adding a `probe_field: u8` to `GraphMeta`
moves its checksum and fails the new test with the `WHAT_TO_DO` message;
removing the field restores it. That is the only way to know the fixture is
covering the type rather than encoding something incidental — the same question
`the_fixtures_actually_encode_something` asks of the two older ones.

The compiler made the probe more informative than intended: adding the field
first failed to *build*, at the one construction site in `lib.rs:688`. So for
`GraphMeta` there are two independent alarms — the layout guard and the
initializer — where `EmbedStamp`, constructed in more places and read back from
disk, relies on the guard alone.

## Acceptance
Four layout tests, and adding a field to `GraphMeta` or to `EmbedStamp` fails
one of them with the `WHAT_TO_DO` message. `just test` green. All hold: seven
layout tests where there were five, the `GraphMeta` failure observed and
reverted, suite 1,253 passed.
