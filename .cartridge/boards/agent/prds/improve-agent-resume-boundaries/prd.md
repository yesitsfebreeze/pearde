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
canonical-scope: improve-agent-resume-boundaries
footprint:
- /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
- /Users/feb/dev/cartridge/agent.ctg/src/model_loop.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
- /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/integration/loop.rs
needs:
- "@sessions/improve-sessions-recovery"
- "@gitfs/tool-results-interoperate"
- "@root/improve-tool-result-contract"
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

## From the retired work memo

Folded 2026-09-15 from `work/improve-agent-resume-boundaries.md` (status open). The PRD state above is authoritative.

### Outcome

After restart an agent identifies the last durable boundary and either resumes safe work or exposes an uncertain external outcome for reconciliation.

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
- [ ] Kill a fixture run before dispatch, during a write, after commit and before result persistence: each restart reports the correct known/unknown state.
- [ ] Completed or uncertain mutations are not automatically repeated; cancellation cannot affect another run.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. This is a large slice: use that bounded probe to split implementation into smaller child outcomes if more than one independent state transition or migration is required.
2. Audit existing checkpoints and cancellation tests first. Add invocation status/correlation and idempotency where backends support it; never infer that cancellation undid a completed mutation.
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

Priority P1; scope size L (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-sessions-recovery](../../../sessions/prds/improve-sessions-recovery/prd.md), [improve-tool-result-contract](../../../root/prds/improve-tool-result-contract/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
