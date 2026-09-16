---
complexity: medium
footprint:
  - src/store/core/src/lib.rs
  - src/store/core/src/cold.rs
  - .cartridge/tests/unit/src/store/core/src/lib/tests.rs
---

# spec01 — cold_seq, the cold_since set and its floor

Base: memory.ctg 5097a83.

## Steps

1. **lib.rs.** Add `COLD_SINCE_DB = "cold_since"`, open it in `Store::open`, and raise
   `MAX_DBS` to 6 (`:36`). Add the meta keys `cold_seq` and `cold_since_floor` (u64; absent
   reads as 0). Add `pub enum ColdOp { Put, Delete }`, with each entry encoded as `(op u8, seq u64 LE)`.
2. **cold.rs, the writers.** Add a private
   `record_cold(&self, txn, puts: &[&str], deletes: &[&str])`. It reads `cold_seq` inside
   `txn`, writes `seq + 1`, and puts each entry with that seq. Call it in `import_snapshot`
   (`:148`), `cold_spill` (`:175`) and `cold_put_all` (`:310`). In `cold_move` (`:430`), record
   delete(old) and put(new) for each planned move. Every call happens before the existing
   `commit`.
3. **cold.rs, the readers and the clear.**
   - `cold_seq() -> u64` and `cold_since_floor() -> u64`.
   - `cold_since_build() -> Vec<(String, ColdOp, u64)>`, sorted by id.
   - `cold_since_len()` and `cold_len()`, both from the LMDB stat (O(1)).
   - `cold_snapshot_vectors(visit: impl FnMut(&str, &[f32])) -> Result<u64>`: one read
     transaction that reads `cold_seq` and then scans `cold_vec`.
   - `clear_cold_since_build(s)`: one write transaction that deletes entries with
     `seq <= s` and sets the floor to `max(floor, s)`.
4. **Tests** in lib/tests.rs, with exact names:
   - `cold_since_build_names_every_writer`: one scenario per writer (`cold_spill`,
     `cold_put_all`, `cold_rekey`, `cold_relocate`, `import_snapshot`). Drop the `Store`,
     reopen it, and assert the exact (id, op) set and rising seq.
   - `cold_since_build_write_during_a_build_survives_the_clear`: spill a and b, then take
     `S = cold_snapshot_vectors(..)`. Spill b again and spill a new c, then
     `clear_cold_since_build(S)`. The set is exactly {b, c}, both with seq > S, and a is gone.
   - `cold_since_build_floor_persists_across_open`: `clear(S)`, drop and reopen, and the
     floor is S. `clear(S - 1)` leaves the floor at S.

## Acceptance

- [ ] `cold_since_build_names_every_writer` passes.
- [ ] `cold_since_build_write_during_a_build_survives_the_clear` passes.
- [ ] `cold_since_build_floor_persists_across_open` passes.
- [ ] The existing `cold_rekey_*` and `cold_relocate_*` tests still pass (same block).
- [ ] The block exits non-zero at 5097a83 ("no tests to run").

## Verify

The reviewer measured this block at 14 s cold and 1 s warm (kache). The coordinator warms it
with `--no-run`.

```sh
export CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/cold-index-verify
cargo nextest run --no-tests=fail -p store_core -E 'test(/::cold_since_build_names_every_writer$/) or test(/::cold_since_build_write_during_a_build_survives_the_clear$/) or test(/::cold_since_build_floor_persists_across_open$/) or test(/::cold_rekey_/) or test(/::cold_relocate_/)'
```
