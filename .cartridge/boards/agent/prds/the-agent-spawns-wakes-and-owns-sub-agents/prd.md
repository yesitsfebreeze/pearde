---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: the-agent-spawns-wakes-and-owns-sub-agents
needs:
- '@sessions/sub-agent-sessions-record-parent-and-mailbox'
---

# the-agent-spawns-wakes-and-owns-sub-agents

Persist child identity, parent, launch intent and inbox wake cursor before acknowledging spawn/send. Coalesce wakes per idle generation and bound active children by configuration. Parent disposal stops admission and reports/reconciles owned children under the documented lifecycle policy; it never kills unrelated processes.

## Acceptance

- [ ] Crash around spawn acknowledgement or wake scheduling produces at most one live run per child generation, with replayable inbox evidence.
- [ ] A forged owner/session or execution request without a current PTY lease is refused before shell input.
- [ ] Two children finish concurrently with attributed reports; parent restart exposes unfinished/unknown work without automatic mutation replay.

## Proof and recovery

Start at [model_loop.rs](../../../model_loop.rs), [run_state.rs](../../../run_state.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test agent` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-agent-spawns-wakes-and-owns-sub-agents`; maximum five rounds.
