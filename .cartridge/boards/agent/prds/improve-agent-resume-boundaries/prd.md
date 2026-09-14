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
canonical-scope: improve-agent-resume-boundaries
needs:
- '@sessions/improve-sessions-recovery'
- '@gitfs/tool-results-interoperate'
footprint:
- /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
- /Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/integration/loop.rs
---

# Resume interrupted runs without replaying uncertain mutations

After a restart or reload the agent classifies every unfinished call at its last durable boundary: not started, completed, or unknown. The next start continues from that boundary with those outcomes in context; a call that may have taken effect is never repeated automatically. Automatic continuation without a new start is out of scope.

## Acceptance

- [ ] Kill a fixture run before dispatch, during a write, and after the tool commits but before its result persists: restart reports not started, unknown, and completed when the backend confirms that call ID (otherwise unknown).
- [ ] Completed and unknown mutations are never repeated; the next start on that session proceeds, and recovering one session never touches another session's run.
- [ ] Transcripts written before the change recover exactly as today: interrupted, outcome unknown.

## Proof and recovery

Baseline (agent `fad6d3b`): `Agent::recover` finishes every unfinished run `interrupted` and closes each pending call with `interrupted-outcome-unknown` (`agent.ctg/src/lib.rs:213-231`, `agent.ctg/src/model_loop.rs:60`). A call with no `tool_started` checkpoint never started (`agent.ctg/src/lib.rs:662`), yet is reported unknown. Since the transport port a reload is a stop and a start, so every reload takes this path (agent `936df03`). Extend `restart_marks_unfinished_run_interrupted_without_replay_and_allows_a_new_start` and `recovery_closes_persisted_unresolved_tool_calls_without_replay` (`.cartridge/tests/unit/run_state.rs:453,493`). Scope L: after the first probe, split backend status queries from classification if both need changes.

Precondition without a PRD: agent still targets the host API removed in cartridge `ee7e295` (`agent.ctg/src/main.rs:14,42`); no agent gate builds until it is ported to declared events.

Gates, cwd `/Users/feb/dev/cartridge`: `just test agent`, `just check agent`. Not run for this plan. Failure: any ambiguity classifies as unknown; a recovery error leaves the session record untouched and a new start possible.

## Review

[Review history](review.md): round 3 of 5 (rounds 1–2 inherited).
