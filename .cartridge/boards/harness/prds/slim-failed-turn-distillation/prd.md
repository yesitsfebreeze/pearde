---
state: "analyzing"
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/harness.ctg"
work-kind: leaf
canonical-scope: slim-failed-turn-distillation
claim: "coordinator-c4-5 2026-09-16T08:17:28.370Z"
---

# A failed turn leaves one retrievable line behind

When the context window moves past a turn, the turn is gone. That is right for a successful turn — its durable record is whatever was written down deliberately — and wrong for a failed one, because the next attempt at the same thing has no way to learn that it already failed and how.

At turn end, distil each failed tool-using turn into one line: the tools it called and its closing statement, stored so it is retrievable after the window has moved. Successful turns leave nothing; a per-turn tool log for work that worked is noise, and this is a retention rule, not a second transcript.

## Acceptance

- [ ] A named run with at least one `tool_finished` record that failed (a tool result with `error:true`, or a `run_finished` phase of `failed`) is ingested exactly once into the configured memory bank. The ingested text is one line, `slim failed turn <session> <run>: <tools> -> <closing statement>`, and the bank's `query` returns it.
- [ ] A named run whose tools all succeeded stores nothing.
- [ ] A named run with no `tool_finished` record stores nothing, whether it failed or not.
- [ ] If the bank refuses or cannot be reached, the ring call still returns Ok with its sweep keys, carries the failure under `slim.error` and writes it to stderr.
- [ ] The declared boolean setting `slim` (default true) turns distillation off: `slim = false` stores nothing. An empty `memory` also stores nothing, and a ring call without `session`/`run` returns the same reply as today.
- [ ] `cargo test --test slim`, `cargo clippy --all-targets -- -D warnings` and `cargo fmt --all -- --check` pass in the lane. After integration, `just test harness` and `just check harness` pass from `/Users/feb/dev/cartridge`.

The hook is harness's turn-end call, `{op:"ring", session, run}`. The live trigger, agent naming the finished run on that call, comes from `@agent/the-turn-end-ring-call-names-the-run-that-finished`. That PRD has no `needs` in either direction, because harness ignores unknown ring args today and an unnamed ring call behaves as before, so either can land first. Every box above is proved offline by `cargo test --test slim`, which calls the named ring directly.

## Proof and recovery

Mechanism from `/Users/feb/dev/pi/packages/coding-agent/src/core/slim/` (71 lines at survey, verified present) — a pure end-of-turn hook that fails open when its store is absent. Upstream writes to its own external knowledge tool; here the store is `memory.ctg`.

Reconcile at implementation with `@harness/safe-transcript-compaction` and `@harness/improve-harness-compaction-diff`, which own the rest of the compaction surface: this is the retention half and must not duplicate what compaction already drops or keeps.

Gates, cwd `/Users/feb/dev/cartridge`: `just test harness`, `just check harness`. Not run for this plan.
