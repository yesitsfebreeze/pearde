---
repo: /Users/feb/dev/cartridge/agent.ctg
state: "done"
origin: requested
priority: 50
blast-radius: low
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - src/lib.rs
  - .cartridge/tests/unit/run_state.rs
commit: "a5db86e91b68452f291dda7b0d07868bad74de99"
---

# The turn-end ring call names the run that finished

`Run::finish` (`src/lib.rs` ~592) sends `harness {op:"ring"}` with no subject, so harness cannot tell which run just ended. Send `{op:"ring", session, run}` so harness's failed-turn distillation (`@harness/slim-failed-turn-distillation`) fires live. The call stays fire-and-forget.

This PRD has no `needs`. Harness ignores unknown ring args today, and a ring call without `session`/`run` keeps working after the harness PRD lands, so either PRD can land first.

## Acceptance

- [x] After a run reaches `completed`, the `harness` ring call it issues carries that run's `session` and `run` ids (`cargo test` unit test in `.cartridge/tests/unit/run_state.rs` over the fake `harness` dispatcher).
- [x] The same holds for a run that ends `failed`.
- [x] A ring call that returns an error leaves the run terminal and its `done`/`error` event emitted unchanged (same test file).
- [x] `cargo clippy --all-targets -- -D warnings` and `cargo fmt --all -- --check` pass in the lane; `just check agent` and `just test agent` pass from `/Users/feb/dev/cartridge` after integration.

## Evidence (2026-09-19, coordinator cartridge-d0)

The boxes were ticked on these observations of lane `a5db86e`:

- **Boxes 1 to 3.** An independent verifier (`.state/loop/the-turn-end-ring/verifier-1.md`) ran the spec's `test` block on a `git archive a5db86e` copy under `env -i`. It exited 0 with `24 passed; 0 failed`, and all three named tests were reported `... ok`, in 5 of 5 runs. With `src/lib.rs` restored from `620857d`, the completed and failed ring tests fail with `left: Null right: "s1"`, and the ring-error preservation test still passes.
- **Box 4.** `just check agent` and `just test agent` gate the live submodule, which is still at `620857d`, so they would not execute this change. Instead, the exact commands those recipes run were executed on a `git archive a5db86e` copy under `env -i`: `cargo fmt -p agent -- --check` exited 0; `cargo clippy -p agent --all-targets -- -D warnings` exited 0; `cargo test -p agent --all-targets` exited 0, with `24 passed` for the lib and `13 passed` for `loop`. `cartridge.json` is unchanged, so the composition isolation result is unaffected.
