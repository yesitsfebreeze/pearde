---
state: open
origin: requested
priority: 65
repo: "/Users/feb/dev/cartridge/memory.ctg"
footprint:
- "src/util/src/lifecycle.rs"
- ".cartridge/tests/unit/src/cartridge/engine_test.rs"
---

# the memory engine tests do not depend on which test ran before them

## Outcome

`cargo test -p memory_cartridge --lib` passes from a clean checkout. No test
leaves process-wide state that makes a later test fail, so the suite's result
does not depend on test order or thread count.

## Evidence

Found 2026-09-16 by the analyst of
`@root/one-daemon-.../memory-runs-once-in-the-daemon-and-attached-instances-never-hit-the-writer-lock`,
while establishing a baseline for that PRD's regression test.

`cargo test -p memory_cartridge --lib` is **already red at HEAD** (`5097a83`):
19 passed / 1 failed at baseline, and 20 / 1 with that PRD's new test — the same
single failure either way, so it is pre-existing and not caused by that work.

Cause: `drain`/`dispose` sets the process-wide `SHUTTING_DOWN`
(`src/util/src/lifecycle.rs:30`). Whichever engine test runs after
`health_overtakes_blocked_ingestion_and_dispose_drains_it` then fails with
"shutting down: the daemon refused this request". Observed with the default
harness and with `--test-threads=1`.

## Acceptance

- [ ] `cargo test -p memory_cartridge --lib` exits 0 from a clean checkout of
      this repo, with no test skipped or ignored to achieve it.
- [ ] Reordering or reversing the engine tests does not change the result.
- [ ] A test that exercises `drain`/`dispose` still asserts the shutdown
      refusal it was written for.

## Planning note

2026-09-16, coordinator cartridge-1b. Filed separately rather than folded into
the memory-runs-once PRD: it predates that work, it is in a different area
(`util::lifecycle`, not the writer lock), and that PRD's spec deliberately works
around it by ending with `drop(owner)` instead of `drain(…)` and by naming the
single test in its Verify block. Fixing it here removes that workaround's reason
to exist.
