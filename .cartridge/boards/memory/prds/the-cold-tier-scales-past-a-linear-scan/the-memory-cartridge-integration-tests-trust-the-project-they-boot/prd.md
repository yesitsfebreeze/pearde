---
repo: /Users/feb/dev/cartridge/memory.ctg
state: "specced"
origin: requested
priority: 60
blast-radius: low
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - .cartridge/tests/integration/cartridge.rs
---

# The memory cartridge integration tests trust the project they boot

`memory::cartridge` (`.cartridge/tests/integration/cartridge.rs`) boots the real base over a
fresh tempdir project whose files were never trusted. memory.ctg `f2319c5` already gives
`Base::boot` its own `CARTRIDGE_HOME`, runs `cartridge trust` before `daemon`, and asserts
`` `memory` is not provided `` (measured 2026-09-19 at 3432b13: `env -u CARTRIDGE_YOLO cargo
nextest run -p memory --test cartridge` exits 0, 3 passed). What remains: every base command
the fixture spawns still inherits `CARTRIDGE_YOLO`, which `just launch claude --yolo` exports and
which makes the base serve an untrusted project (`cartridge.ctg/src/trust/mod.rs:94`). Under it
the fixture would pass whether or not trust works, so the tests prove nothing on these machines.

Fix inside the fixture only: one `base_command(home)` helper sets `CARTRIDGE_HOME` and removes
`CARTRIDGE_YOLO` (precedent `src/hub/src/lib.rs:121`), and a new test sets YOLO itself and proves
`base_command` does not pass it on. No base change, no trust record outside the tempdir.

## Acceptance

- [ ] `an_inherited_yolo_does_not_trust_a_project_the_fixture_never_trusted` passes, and so do the 3 existing `memory::cartridge` tests.
- [ ] The new test fails when `.env_remove("CARTRIDGE_YOLO")` is removed from `base_command`.
- [ ] A run leaves `~/.cartridge` untouched.

## Verify

```sh
test -x "${CARTRIDGE_BIN:-../cartridge.ctg/target/release/cartridge}"
```

```test
run: CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$PWD/target/integration-trust-verify}" cargo nextest run -p memory --test cartridge
pass: an_inherited_yolo_does_not_trust_a_project_the_fixture_never_trusted
pass: status_tool_and_context_answer_without_opening_the_store
pass: a_bad_configuration_fails_the_cartridge_before_it_listens
pass: ingest_query_tool_and_context_reach_one_store_through_the_base
```

Split from `@memory/the-cold-tier-scales-past-a-linear-scan` on 2026-09-16 (analyst-2). It inherits the parent's used review rounds: none.

## Planning note

2026-09-16, coordinator cartridge-c4, from analyst-1. With this fix the workspace still has one failure outside this footprint: `memory::spill_transparency a_spilled_graph_answers_the_same_queries_as_one_that_never_spilled` (recall@10 0.8370 < 0.84). That is filed as its own PRD, and the parent keeps the workspace gate. A full workspace run takes about 3 min, which doesn't fit a Verify block.
