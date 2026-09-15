---
repo: /Users/feb/dev/cartridge/agent.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-agent-task-baseline.md` (status open). The PRD state above is authoritative.

### Outcome

A small evaluation compares completed coding tasks under equivalent repository fixtures and declared tool/model conditions.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [agents-query-the-tool-graph](../../../root/prds/agents-query-the-tool-graph/prd.md), [the-agent-spawns-wakes-and-owns-sub-agents](../the-agent-spawns-wakes-and-owns-sub-agents/prd.md).

### Footprint

Agent loop; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `agent.ctg/model_loop.rs`
- `agent.ctg/run_state.rs`
- `agent.ctg/context.rs`
- `agent.ctg/tests/loop.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Offline harness runs fixed fixture agents against identical initial trees and catches a wrong patch despite plausible prose.
- [ ] The opt-in comparison report names models, configuration, revisions and all failures; no speed/quality winner is claimed without actual comparable runs.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Create a versioned task corpus for read-only investigation, constrained edit, recovery and multi-step work. Score acceptance tests, constraint violations, tool calls, latency and tokens; separate product comparison from same-model experiments and record unavailable conditions honestly.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test agent
just check agent
```


### Compatibility and recovery

Preserve existing checkpoints and transcripts. Resume only operations whose completion is known; retain uncertain outcomes for reconciliation. Compare loop changes with the fixed fixture corpus before enabling them in a normal profile.

### Handoff

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
