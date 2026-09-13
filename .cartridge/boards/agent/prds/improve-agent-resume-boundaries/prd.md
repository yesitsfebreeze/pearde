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
canonical-scope: improve-agent-resume-boundaries
needs:
- '@sessions/improve-sessions-recovery'
- '@gitfs/tool-results-interoperate'
footprint:
- /Users/feb/dev/cartridge/agent.ctg/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/run_state.rs
- /Users/feb/dev/cartridge/agent.ctg/context.rs
- /Users/feb/dev/cartridge/agent.ctg/tests/loop.rs
---

# Resume interrupted runs without replaying uncertain mutations

After restart an agent identifies the last durable boundary and either resumes safe work or exposes an uncertain external outcome for reconciliation.

## Acceptance

- [ ] Kill a fixture run before dispatch, during a write, after commit and before result persistence: each restart reports the correct known/unknown state.
- [ ] Completed or uncertain mutations are not automatically repeated; cancellation cannot affect another run.

- [ ] Preserve existing checkpoints and transcripts. Resume only operations whose completion is known; retain uncertain outcomes for reconciliation. Compare loop changes with the fixed fixture corpus before enabling them in a normal profile.

## Proof and recovery

Start at [model_loop.rs](../../../model_loop.rs), [run_state.rs](../../../run_state.rs), [context.rs](../../../context.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test agent` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-agent-resume-boundaries`; maximum five rounds.
