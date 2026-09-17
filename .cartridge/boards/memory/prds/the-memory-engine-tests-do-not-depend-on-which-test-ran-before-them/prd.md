---
state: "done"
origin: requested
priority: 65
repo: "/Users/feb/dev/cartridge/memory.ctg"
footprint:
- "src/util/src/lifecycle.rs"
- ".cartridge/tests/unit/src/cartridge/engine_test.rs"
commit: "47864de00b8b07a6418268fdd18632da0e6acc05"
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

- [x] `cargo test -p memory_cartridge --lib` exits 0 from a clean checkout of
      this repo, with no test skipped or ignored to achieve it.
- [x] Reordering or reversing the engine tests does not change the result.
- [x] A test that exercises `drain`/`dispose` still asserts the shutdown
      refusal it was written for.

## Planning note

2026-09-16, coordinator cartridge-1b. Filed separately rather than folded into
the memory-runs-once PRD: it predates that work, it is in a different area
(`util::lifecycle`, not the writer lock), and that PRD's spec deliberately works
around it by ending with `drop(owner)` instead of `drain(…)` and by naming the
single test in its Verify block. Fixing it here removes that workaround's reason
to exist.

## Further evidence (2026-09-17, coordinator cartridge-fa)

Observed while landing `@memory/a-spilled-graph-answers-the-same-queries-as-one-that-never-spilled`, which shares no file with this PRD. `just test memory` fails at
`memory_cartridge --lib engine_tests::health_overtakes_blocked_ingestion_and_dispose_drains_it`,
which panics `Elapsed(())` at `engine_test.rs:137` — 20 passed, 1 failed.

The spilled-graph implementer ablated it rather than assuming: it restored both
of its own changed files to their HEAD content with `git show HEAD:<path>`,
re-ran `cargo test -p memory_cartridge --lib`, and got an identical failure,
then restored its work from a backup. The same test passes when run in
isolation. So the failure is order- and timing-dependent under the parallel
suite, which is exactly the outcome this PRD names, and it is reproducible
today rather than historically.
