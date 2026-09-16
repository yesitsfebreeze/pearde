---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: low
workflow: develop-one-cartridge
work-kind: leaf
footprint:
  - src/lib.rs
  - .cartridge/tests/unit/run_state.rs
---

# The turn-end ring call names the run that finished

`Run::finish` (`src/lib.rs` ~592) sends `harness {op:"ring"}` with no subject, so harness cannot tell which run just ended. Send `{op:"ring", session, run}` so harness's failed-turn distillation (`@harness/slim-failed-turn-distillation`) fires live. The call stays fire-and-forget.

This PRD has no `needs`. Harness ignores unknown ring args today, and a ring call without `session`/`run` keeps working after the harness PRD lands, so either PRD can land first.

## Acceptance

- [ ] After a run reaches `completed`, the `harness` ring call it issues carries that run's `session` and `run` ids (`cargo test` unit test in `.cartridge/tests/unit/run_state.rs` over the fake `harness` dispatcher).
- [ ] The same holds for a run that ends `failed`.
- [ ] A ring call that returns an error leaves the run terminal and its `done`/`error` event emitted unchanged (same test file).
- [ ] `cargo clippy --all-targets -- -D warnings` and `cargo fmt --all -- --check` pass in the lane; `just check agent` and `just test agent` pass from `/Users/feb/dev/cartridge` after integration.
