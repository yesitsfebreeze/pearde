---
complexity: medium
footprint:
  - src/store/core/src/lib.rs
  - src/store/core/src/cold.rs
  - .cartridge/tests/unit/src/store/core/src/lib/tests.rs
---

# spec01 — cold_seq, the cold_since set and its floor

Base: memory.ctg 3432b13. The footprint is unchanged since 5097a83.

## Steps

1. **lib.rs.** Add `COLD_SINCE_DB = "cold_since"`, open it in `Store::open`, and raise
   `MAX_DBS` to 6 (`:36`). Add the meta keys `COLD_SEQ_KEY = "cold_seq"` and
   `COLD_SINCE_FLOOR_KEY = "cold_since_floor"`. Add `pub enum ColdOp { Put, Delete }`.
   - Encoding. Both meta values are a raw 8-byte `u64` LE with no version byte, read and
     written directly through `self.meta` (a `Database<Str, Bytes>`), not through
     `Store::get`/`put`'s versioned `encode`. An absent key reads as 0. Any other length
     is a `StoreError` decode error, never 0. Each `cold_since` value is 9 bytes: an op
     byte (`0` Put, `1` Delete) followed by the seq as `u64` LE. Nothing iterates `meta`
     (checked with `rg` at 3432b13), so `rewrite_meta` and `note_version` stay unchanged.
2. **cold.rs, the writers.** Add a private
   `record_cold(&self, txn: &mut RwTxn, touched: &[&str])`. It runs after the writer's
   last put or delete and before the existing `commit`. If `touched` is empty, it returns
   without bumping anything, so `cold_put_all(&[])` from compact and a `cold_move` with no
   planned moves leave `cold_seq` unchanged. Otherwise it reads `cold_seq` inside `txn`,
   writes `seq + 1`, and, for each distinct id, derives the op from the id's final state
   in the same transaction (`self.cold.get(txn, id)?.is_some()` gives `Put`, and absence
   gives `Delete`). It then puts `(op, seq + 1)`, overwriting any older entry, so the
   last write wins. Deriving the op from the final state makes a `cold_move` chain
   correct in either plan order: after A→B then B→C, B is absent and recorded as
   `Delete`; after B→C then A→B, B is present and recorded as `Put`. Chains can occur,
   because `cold_rekey`/`cold_relocate` check collisions only against `staying` rows
   (`cold.rs:382,415`), and a row that is itself moving is not staying.
   Call sites: `import_snapshot` (`:148`, the imported cold ids), `cold_spill` (`:175`),
   `cold_put_all` (`:310`), and `cold_move` (`:430`, every `old` and `new`). Make
   `cold_move` and `ColdRow::of` `pub(crate)` so the unit test can drive both chain orders
   directly. A real rekey chain needs a stale id that equals another row's origin id,
   which no existing fixture produces.
3. **cold.rs, the readers and the clear.**
   - `cold_seq() -> u64` and `cold_since_floor() -> u64`.
   - `cold_since_build() -> Vec<(String, ColdOp, u64)>`, sorted by id.
   - `cold_since_len()` and `cold_len()`, both from the LMDB stat (O(1)). The sibling
     `the-cold-tier-has-a-vamana-index-that-the-tick-keeps-current` uses them in its
     rebuild trigger (its spec01 `:44-46`), and its footprint does not include store_core,
     so they land here. They are asserted in `cold_since_build_names_every_writer`.
   - `cold_snapshot_vectors(visit: impl FnMut(&str, &[f32])) -> Result<u64>`: one read
     transaction that reads `cold_seq` and then scans `cold_vec`. It is kept because the
     sibling builds from it (its spec01 `:32`). It does not duplicate the scan: extract the
     loop in `cold_visit_vectors` (`:224`) into a private
     `visit_vectors_in(&self, txn: &RoTxn, visit)`, and call it from both functions.
     `cold_visit_vectors`'s signature is unchanged, so `retrieval_query.rs:777` and its
     test caller are not touched.
   - `clear_cold_since_build(s)`: one write transaction that deletes entries with
     `seq <= s` and sets the floor to `max(floor, s)`.
4. **Tests** in lib/tests.rs, with exact names:
   - `cold_since_build_names_every_writer`: one scenario per writer, each on a fresh store:
     `cold_spill`, `cold_put_all`, `cold_rekey`, `cold_relocate` (the fixtures from
     `cold_rekey_moves_the_row_and_its_vector_and_leaves_nothing_behind` and
     `cold_relocate_moves_a_parked_file_row_and_leaves_the_rest`), and `import_snapshot`
     (`&HashMap::new()`, one cold entity, replica `"r"`, `QuantizationMode::None`,
     `EmbedStamp { model: "m".into(), dim }`). Each scenario drops the `Store`, reopens
     it, and asserts the exact (id, op) set, a rising seq, and `cold_since_len()` and
     `cold_len()`. Add two chain scenarios through `cold_move`, one per order: spill A and
     B, then `cold_move([(A,B), (B,C)])` records A Delete, B Delete, C Put, and
     `cold_move([(B,C), (A,B)])` records A Delete, B Put, C Put. Finally,
     `cold_put_all(&[])` leaves `cold_seq` unchanged.
   - `cold_since_build_write_during_a_build_survives_the_clear`: spill a and b. Then call
     `S = s.cold_snapshot_vectors(|..| ..)`. On its first visit, the callback runs
     `std::thread::scope(|t| t.spawn(|| { s.cold_spill(&b2)?; s.cold_spill(&c) }).join())`.
     This commits a write transaction on another thread while the scan's read transaction
     is open. Then call `clear_cold_since_build(S)`. The set is exactly {b, c}, both with
     seq > S, and a is gone. An implementation that reads `cold_seq` after the scan, in a
     separate transaction, returns an S that covers b2 and c, clears them, and fails
     this test.
   - `cold_since_build_floor_persists_across_open`: `clear(S)`, drop and reopen, and the
     floor is S. `clear(S - 1)` leaves the floor at S.

## Acceptance

- [ ] `cold_since_build_names_every_writer` passes, including both `cold_move` chain orders.
- [ ] `cold_since_build_write_during_a_build_survives_the_clear` passes, with the write committed from another thread inside the scan callback.
- [ ] `cold_since_build_floor_persists_across_open` passes.
- [ ] The existing `cold_rekey_*` and `cold_relocate_*` tests still pass. They run in the same `run:` command, so any failure makes it exit non-zero.
- [ ] At 3432b13 the block fails. The command exits 0 after running only the 8 existing `cold_rekey_*`/`cold_relocate_*` tests, and collect rejects the block because none of the three `pass:` names is reported. Measured with an isolated target; see `.state/loop/since-build-set/revision-3.md`.

## Verify

The coordinator warms the target with `--no-run` before collect.

```test
run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/since-build-set-verify}" cargo nextest run --no-tests=fail -p store_core -E 'test(/::cold_since_build_/) or test(/::cold_rekey_/) or test(/::cold_relocate_/)'
pass: cold_since_build_names_every_writer
pass: cold_since_build_write_during_a_build_survives_the_clear
pass: cold_since_build_floor_persists_across_open
```

## Review notes carried into implementation (round 4, clarification only)

- `cold_since_build()` iterates the `cold_since` table directly and never through `scan_with`/`get_with`:
  each value starts with its op byte (0 or 1), and `note_version` (`lib.rs:483`) would read that as an
  old format and report the store stale permanently. The `note_version` comment names `cold_since`
  next to `cold_vec` as a table whose values carry no version byte.
- The writer test's "rising seq" means: within one store, each non-empty batch's recorded seq is
  strictly greater than the previous batch's; each writer scenario starts from a fresh store at seq 1.
- The lane pass and the repo pass resolve `$PWD` to different target dirs, so each builds cold; a cold
  build measured 7 s (with the user's kache wrapper) against the 120 s limit.
- Out of scope, reported to the memory owner as a follow-up: `cold_move` already loses data on an
  A→B then B→C chain (pre-existing; `cold_rekey` produces this order when A sorts before B). This
  plan's chain test records the op per final row state and does not fix the move itself.

