---
kind: work
description: "Resume interrupted runs without replaying uncertain mutations"
status: open
priority: P1
size: L
needs:
  - "[[@prd/work/root--improve-sessions-recovery.md]]"
  - "[[@prd/work/root--improve-tool-result-contract.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["resume interrupted runs without replaying uncertain mutations", "implementing agent cartridge improvements"]
---

# Resume interrupted runs without replaying uncertain mutations

## Outcome

After restart an agent identifies the last durable boundary and either resumes safe work or exposes an uncertain external outcome for reconciliation.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [[@prd/work/root--agents-query-the-tool-graph.md]], [[@prd/work/root--the-agent-spawns-wakes-and-owns-sub-agents.md]].

## Footprint

Agent loop; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `agent.ctg/model_loop.rs`
- `agent.ctg/run_state.rs`
- `agent.ctg/context.rs`
- `agent.ctg/tests/loop.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Kill a fixture run before dispatch, during a write, after commit and before result persistence: each restart reports the correct known/unknown state.
- [ ] Completed or uncertain mutations are not automatically repeated; cancellation cannot affect another run.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. This is a large slice: use that bounded probe to split implementation into smaller child outcomes if more than one independent state transition or migration is required.
2. Audit existing checkpoints and cancellation tests first. Add invocation status/correlation and idempotency where backends support it; never infer that cancellation undid a completed mutation.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test agent
just check agent
```


## Compatibility and recovery

Preserve existing checkpoints and transcripts. Resume only operations whose completion is known; retain uncertain outcomes for reconciliation. Compare loop changes with the fixed fixture corpus before enabling them in a normal profile.

## Handoff

Priority P1; scope size L (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-sessions-recovery.md]], [[@prd/work/root--improve-tool-result-contract.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
