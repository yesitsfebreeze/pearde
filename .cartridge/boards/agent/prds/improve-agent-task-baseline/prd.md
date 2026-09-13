---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: agent
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-agent-task-baseline
footprint:
- /Users/feb/dev/cartridge/agent.ctg/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/run_state.rs
- /Users/feb/dev/cartridge/agent.ctg/context.rs
- /Users/feb/dev/cartridge/agent.ctg/tests/loop.rs
---

# Compare cartridge-native and Codex task outcomes reproducibly

Start with eight immutable disposable tasks: two each for investigation, constrained edit, recovery and multi-step work. Run three repetitions per declared agent/model configuration in alternating order. The decision is whether cartridge-native orchestration adds task value; keep external-product comparisons separate from same-model experiments.

## Acceptance

- [ ] Independent acceptance tests reject a plausible wrong patch and report all constraint violations.
- [ ] Reports retain all 24 outcomes per configuration, unavailable runs, model/config/source revisions, tool calls, token estimates or measured usage and latency.
- [ ] Do not declare a winner unless comparable runs exist; corpus changes produce a new corpus revision and preserve the old report.

## Proof and recovery

Start at [model_loop.rs](../../../model_loop.rs), [run_state.rs](../../../run_state.rs), [context.rs](../../../context.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test agent` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-agent-task-baseline`; maximum five rounds.
