---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
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
- [ ] From memory.ctg, `cargo nextest run --workspace` reports 0 failed.

## Verify

```sh
test -x ../cartridge.ctg/target/release/cartridge
cargo nextest run -p memory --test cartridge
```

Split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 (analyst-2). It inherits the parent's used review rounds: none.
