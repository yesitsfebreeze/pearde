---
repo: "/Users/feb/dev/cartridge/memory.ctg"
state: open
origin: requested
priority: 40
blast-radius: low
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - src/store/core/src/cold.rs
  - .cartridge/tests/unit/src/store/core/src/lib/tests.rs
---

# A cold re-key chain moves every row with its own vector

`Store::cold_move` (`src/store/core/src/cold.rs:430`) applies the planned moves one at a
time, in key order, inside a single transaction. For each move it reads the vector at
`old`, deletes `old`, and puts the row and vector at `new`. Now take a chain A→B, B→C where
A sorts before B. A's move overwrites B's row and vector first. B's move then reads
`cold_vec[B]`, which by now holds A's vector, and writes it to C beside B's row. C ends up
with B's text and A's vector, while B holds A's row.

The collision guards (`cold_rekey` `:364-384`, `cold_relocate` `:398-420`) only reject
destinations held by a row that is *staying*. A destination whose occupant is itself moving
is allowed, and so are two moves onto the same new id (the second silently replaces the
first). Reachability is not probed. `cold_rekey` mints destinations from
`origin_id(external_id, text)`, so a chain needs a row whose current key is another row's
origin id while it moves on; `cold_relocate` across file renames is the likelier path.

Fix: read every planned row's vector before any write (or order the moves topologically),
and reject duplicate destinations as collisions.

## Acceptance

- [ ] A test builds an A→B, B→C chain through `cold_move` (A sorting first) and fails at 5097a83, because C carries A's vector. After the fix, C has B's vector and B has A's.
- [ ] A test where two rows move onto one new id reports the second as a collision, and both rows survive.
- [ ] The existing `cold_rekey_*` and `cold_relocate_*` tests pass.

## Proof and recovery

First probe whether `cold_relocate` can produce a chain with real rows. If it cannot,
downgrade this to a debug assertion. Already-corrupted rows are not detectable after the
fact without re-embedding, and `memory reembed` rewrites them.
