---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
---

# The unit suite runs offline in under a minute

## Outcome

`cargo test` in `cartridge.ctg` needs Rust and Git only, touches nothing outside the repository, passes on a fresh clone with no network, and finishes in under one minute on the development machine. Today it takes 124 seconds and one test fails because it depends on the sibling checkout.

## Findings to close

- `.cartridge/tests/unit/src/tests/folders.rs:132` `recorded_memory_layout_uses_the_separate_submodule` shells out to `bun test`, which clones the parent repository and runs `git submodule update --init --recursive` with a 660-second budget. It is the failing test on 2026-09-14. It is an integration gate and belongs in `just smoke` or CI, not `cargo test`.
- `.cartridge/tests/unit/src/tests/mod.rs` `settle()` is a fixed 60 ms sleep, self-marked as a flake risk; the reload PRD that was collected replaced one such sleep with a generation boundary and the same pattern applies here.
- Test files sit outside `src/` behind `#[path = "../.cartridge/..."]` in eleven modules, with four different depth conventions: `unit/src/tests/*.rs`, `unit/src/<module>/tests.rs`, `unit/<file>.rs`, `unit/service/version_tests.rs`. Pick one.
- `cargo test` runs `bun` for one test and the `just test runtime` recipe runs a second Bun suite afterwards; two toolchains for one crate's tests.

## Acceptance

- [ ] `cargo test` passes on a clean clone with the network disabled and no sibling repository present.
- [ ] Wall time under 60 seconds; the slowest ten tests are listed in the PRD's collection receipt.
- [ ] The submodule layout check runs from `just smoke` and CI only.
- [ ] `settle()` is gone; tests await an observable lifecycle event.
- [ ] One layout convention for out-of-tree tests, documented in `docs/development.txt`, or the tests move to `src/**/tests.rs` and `tests/` per Cargo convention. The PRD's specification must say which and why.
