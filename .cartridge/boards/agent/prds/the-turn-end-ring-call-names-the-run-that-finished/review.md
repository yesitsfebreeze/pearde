# @agent/the-turn-end-ring-call-names-the-run-that-finished review history

Plan: `@agent/the-turn-end-ring-call-names-the-run-that-finished`, at `prds/the-turn-end-ring-call-names-the-run-that-finished/prd.md`.
Scope: one observable outcome, a leaf with one spec.
Round limit: 5. Passing threshold: 90/100 for the agent reviewer.
Inherited rounds: none.

## Fast path — 2026-09-19

Coordinator cartridge-d0 (Claude Code session 93137d6c) checked the fast-path conditions in `review-plan.md` against `specs/spec01.md`:

- The PRD has exactly one spec.
- The footprint is two files in one cartridge: `agent.ctg` `src/lib.rs` and `.cartridge/tests/unit/run_state.rs`.
- No `cartridge.json` surface, setting, need or event changes. The change adds two keys to the payload of an existing `harness {op:"ring"}` call. `harness.ctg`'s `ring` already reads those keys as optional and tolerates their absence.
- The Verify section has a `test` block that names the three new tests.

All four conditions hold, so the plan skips the review loop. Rounds used: 0. An independent verifier, never the author, reruns the Verify blocks and reads the diff before collect. If that verifier finds a behavioural gap, or a condition stops holding, this PRD enters review at round 1.
