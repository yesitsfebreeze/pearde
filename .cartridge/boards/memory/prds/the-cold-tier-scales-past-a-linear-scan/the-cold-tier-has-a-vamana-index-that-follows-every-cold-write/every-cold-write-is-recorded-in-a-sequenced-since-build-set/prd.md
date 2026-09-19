---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "specced"
origin: requested
priority: 60
blast-radius: mid
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - src/store/core/src/lib.rs
  - src/store/core/src/cold.rs
  - .cartridge/tests/unit/src/store/core/src/lib/tests.rs
---

# Every cold write is recorded in a sequenced since-build set

## Outcome

A cold index needs to know which rows changed since it was built, across processes.
Every cold writer bumps a persisted `cold_seq` in its own LMDB write transaction and records
`id -> (put|delete, seq)` in a new `cold_since` table; the last write to an id wins. The
writers are `import_snapshot`, `cold_spill`, `cold_put_all`, and `cold_move`, which serves
`cold_rekey` and `cold_relocate`. LMDB serialises writers across processes, so the sequence
is atomic.

A builder reads `cold_seq` in the same read transaction as its vector scan. Then
`clear_cold_since_build(S)` removes only entries with `seq <= S` and, in the same
transaction, raises a persisted floor `cold_since_floor` to S. Writes during a build keep
their entries, and a reader can tell that an index older than the floor is no longer
backed by the set.

`MAX_DBS` goes from 5 to 6 (`lib.rs:36`). `compact_dir` opens with it, while `read_graph`
opens through `health::open_readonly` with `max_dbs(32)` (`health.rs:22`), so both old and
new binaries still open the store.

Cost accepted: until `@memory/.../cold-index-builder` lands, nothing reads or clears the
set. It stays bounded by the distinct cold ids ever written.

## Acceptance

- [ ] After each of the five writers, a reopened store (first handle dropped) reads a since-build set naming exactly the ids put and deleted, with rising `seq`.
- [ ] A write that commits while the build's scan transaction is open (from another thread) keeps its entry after `clear_cold_since_build(S)`; entries at or below S are gone.
- [ ] The floor persists across `Store::open` and never moves down.

## Proof and recovery

The tests are named in specs/spec01.md. The Verify `test` block fails at 3432b13: its
command runs only the 8 existing `cold_rekey_*`/`cold_relocate_*` tests and exits 0, but
none of the three named tests is reported passed. An older binary ignores the table. Deleting the table only forces the next build to be
a full one. This leaf inherits 2 used review rounds from `the-cold-tier-has-a-vamana-index-that-follows-every-cold-write`.

## Failure

No work was attempted. Coordinator session cartridge-cc
(`coordinator-41b7-7`) claimed this row at 2026-09-19T14:15Z, which created its
lane, and the session was then asked by its user to finish and stop before an
implementer was ever dispatched. The lane holds no commits and nothing was
written to `memory.ctg`.

This is a clean release, not a defect. The spec is sound and reviewed: it
passed round 4 at 91 with no blocking findings, after round 3 failed at 79 and
the author revised. Its Verify is an engine `test` block naming three new
tests, confirmed failing at base through the engine's own `passedTests`, and
its target dir is `${CARGO_TARGET_DIR:-$PWD/target/since-build-set-verify}`.
The next coordinator should `retry` this row and dispatch an implementer
against that spec unchanged.

One out-of-footprint defect was found by cartridge-5c while reviewing this row,
and it is recorded here because it has no PRD of its own yet: `cold_move`
loses data on an A→B then B→C chain — the row lands at C carrying B's contents
and A's vector — and `cold_rekey` produces exactly that order when A sorts
before B. That deserves its own memory PRD.
