---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-agent-task-baseline
footprint:
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/eval
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/integration/loop.rs
---

# Compare cartridge-native and Codex task outcomes reproducibly

Decide whether cartridge-native orchestration adds task value. A versioned corpus of eight immutable disposable tasks — two each for investigation, constrained edit, recovery and multi-step work — is scored by independent acceptance tests. Product comparison (cartridge against Codex) and same-model experiments are separate reports.

## Acceptance

- [ ] Offline, with a scripted model, every task's acceptance test rejects a plausible wrong patch and reports all constraint violations, inside `just test agent` with no network or credentials.
- [ ] An opt-in run executes three repetitions per declared agent/model configuration in alternating order and reports all 24 outcomes, unavailable runs, model/config/source revisions, tool calls, measured or estimated tokens and latency.
- [ ] No winner is declared without comparable completed runs on both sides.
- [ ] Changing a task creates a new corpus revision; earlier reports stay readable against theirs.

## Proof and recovery

Baseline (agent `fad6d3b`): no corpus, evaluation runner or Codex adapter exists in the composed tree. Reuse the scripted HTTP fake (`agent.ctg/.cartridge/tests/unit/http_fake.rs`) and the `loop` integration harness that boots a host with disposable directories (`agent.ctg/.cartridge/tests/integration/loop.rs`). Create the corpus under `agent.ctg/.cartridge/tests/eval/`, per the decision keeping tests in `.cartridge/tests/`, and run the offline check from the existing `loop` target.

Precondition without a PRD: agent and its `loop` harness still target the host API removed in cartridge `ee7e295`; no agent gate builds until the agent is ported to declared events.

The live comparison needs model credentials and spend: run it only with explicit user authorization at execution time, never in a gate. Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run for this plan. Failure: a crashed or unavailable run is reported as such, never dropped or silently retried.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
