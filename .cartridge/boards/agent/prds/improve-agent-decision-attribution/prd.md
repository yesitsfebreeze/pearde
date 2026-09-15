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
canonical-scope: improve-agent-decision-attribution
needs:
- '@router/improve-router-route-explanation'
- '@policy/improve-policy-explain'
- '@harness/improve-harness-compaction-diff'
footprint:
- /Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
- /Users/feb/dev/cartridge/agent.ctg/src/context.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/context_tests.rs
---

# Trace tool dispatch to exact context and route configuration

Run inspection links each tool dispatch to the assembled request revision, the tool descriptor revision, provider and model, and the policy decision, by digest and reference rather than copied prompts. Router, policy and harness explanations (all done) supply the references; the agent records and joins what its declared needs return.

## Acceptance

- [ ] Two model rounds with changed context and changed descriptors resolve to different, correct revisions in inspection.
- [ ] A provider fallback or cartridge reload between rounds is attributed to the round it affected.
- [ ] A policy-refused call and a dispatch ending `failed`, `timed_out` or `unavailable` each have an attributable record with no credential and no fabricated reasoning.
- [ ] Transcripts written before the change still load, recover and project unchanged.

## Proof and recovery

Baseline (agent `fad6d3b`): `descriptor_revision` hashes each descriptor (`agent.ctg/src/model_loop.rs:17`) into `tool_revisions` (`agent.ctg/src/lib.rs:466`), but it reaches only memo observations and only with `record_usage` on (`agent.ctg/src/lib.rs:811`). `context:last` keeps just the latest assembled request (`agent.ctg/src/context.rs`); `tool_started` carries no model, request digest or policy decision (`agent.ctg/src/lib.rs:632-662`). Record a request digest on `model_turn_started` and references on `tool_started`; store no prompt copies. Policy rules now come from the composition's `config.lua`; record the decision policy returns, not a rule catalog.

Precondition without a PRD: agent still targets the host API removed in cartridge `ee7e295` (`agent.ctg/src/main.rs:14,33,42`); no agent gate builds until it is ported to declared events.

First probe: a failing two-round test in `run_state.rs` whose descriptors differ. Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run for this plan. Failure: an unavailable reference is recorded `unavailable`, never inferred; attribution failure never fails the dispatch.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).

## From the retired work memo

Folded 2026-09-15 from `work/improve-agent-decision-attribution.md` (status open). The PRD state above is authoritative.

### Outcome

A run inspection links each tool dispatch to assembled request revision, descriptor revision, provider/model and policy decision.

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
- [ ] Two rounds with changed context/provider descriptors resolve to different correct revisions in inspection.
- [ ] A rejected call and a failed dispatch have attributable records without storing credentials or fabricated private reasoning.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Reuse harness context:last and existing session journals. Store hashes and references with bounded telemetry rather than duplicate prompts; preserve attribution when a provider falls back or a cartridge reloads.
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
Ready after [improve-router-route-explanation](../../../router/prds/improve-router-route-explanation/prd.md), [improve-policy-explain](../../../policy/prds/improve-policy-explain/prd.md), [improve-harness-compaction-diff](../../../harness/prds/improve-harness-compaction-diff/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
