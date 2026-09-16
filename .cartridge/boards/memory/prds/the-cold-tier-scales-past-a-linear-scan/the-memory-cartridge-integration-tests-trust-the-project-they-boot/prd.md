---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "open"
origin: requested
priority: 60
blast-radius: low
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - .cartridge/tests/integration/cartridge.rs
---

# The memory cartridge integration tests trust the project they boot

`memory::cartridge` (`.cartridge/tests/integration/cartridge.rs`) boots the real base
(`../cartridge.ctg/target/release/cartridge`) over a fresh tempdir project whose
`.cartridge/init.lua` and `cartridges/memory/*` were never trusted. The base's trust
check (`cartridge.ctg/src/trust/mod.rs:140`) refuses with `is in no trusted project;
review it, then run cartridge trust ...`, so three tests fail on every machine. The
failure predates the cold-tier work (recorded in `the-floor-names-the-weak-hits-it-cut`
and in both cold-tier passes) and keeps `just test` red for every memory PRD.

Fix inside the fixture only: give `Base::boot` its own `CARTRIDGE_HOME` (a tempdir;
read at `trust/mod.rs:20`), run `cartridge trust` on the temp project before `daemon`,
and pass the same env to `cli`. No base change, no trust record outside the tempdir.

## Acceptance

- [ ] `cargo nextest run -p memory --test cartridge` exits 0 with the base built.
- [ ] Every base command the fixture spawns carries the tempdir `CARTRIDGE_HOME`; the user's trust record is unchanged by a test run.
- [ ] The stale `no active listener` assertion matches the base's current answer (`` `memory` is not provided ``, cartridge.ctg `src/host/mod.rs:769`), so all 3 `memory::cartridge` tests pass.

## Verify

```sh
test -x ../cartridge.ctg/target/release/cartridge
cargo nextest run -p memory --test cartridge
```

Split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 (analyst-2). It inherits the parent's used review rounds: none.

## Planning note

2026-09-16, coordinator cartridge-c4, from analyst-1. With this fix the workspace still has one failure outside this footprint: `memory::spill_transparency a_spilled_graph_answers_the_same_queries_as_one_that_never_spilled` (recall@10 0.8370 < 0.84). That is filed as its own PRD, and the parent keeps the workspace gate. A full workspace run takes about 3 min, which doesn't fit a Verify block.
