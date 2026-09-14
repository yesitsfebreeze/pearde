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
