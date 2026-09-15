---
kind: work
description: "Compare cartridge-native and Codex task outcomes reproducibly"
status: open
priority: P2
size: M
uses:
  - usage: "[[read-usage]]"
    when: ["compare cartridge-native and codex task outcomes reproducibly", "implementing agent cartridge improvements"]
---

# Compare cartridge-native and Codex task outcomes reproducibly

## Outcome

A small evaluation compares completed coding tasks under equivalent repository fixtures and declared tool/model conditions.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [agents-query-the-tool-graph](../../prds/agents-query-the-tool-graph/prd.md), [the-agent-spawns-wakes-and-owns-sub-agents](../../../agent/prds/the-agent-spawns-wakes-and-owns-sub-agents/prd.md).

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
- [ ] Offline harness runs fixed fixture agents against identical initial trees and catches a wrong patch despite plausible prose.
- [ ] The opt-in comparison report names models, configuration, revisions and all failures; no speed/quality winner is claimed without actual comparable runs.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Create a versioned task corpus for read-only investigation, constrained edit, recovery and multi-step work. Score acceptance tests, constraint violations, tool calls, latency and tokens; separate product comparison from same-model experiments and record unavailable conditions honestly.
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

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
