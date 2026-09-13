---
kind: work
description: "Preview and apply safe session retention"
status: open
priority: P2
size: M
needs:
  - "[[@prd/work/root--improve-sessions-client-mapping.md]]"
uses:
  - usage: "[[read-usage]]"
    when: ["preview and apply safe session retention", "implementing sessions cartridge improvements"]
---

# Preview and apply safe session retention

## Outcome

An operator can inspect stored session sizes/ages and eligible cleanup candidates before deleting closed unpinned sessions.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [[@prd/work/root--sub-agent-sessions-record-parent-and-mailbox.md]], [[@prd/work/root--the-board-is-channels-of-lines.md]].

## Footprint

Sessions; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `sessions.ctg/main.rs`
- `sessions.ctg/README.md`
- `mcp.ctg/service.rs`
- `agent.ctg/run_state.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

## Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] A mixed fixture reports byte/count/age totals, preserves pinned and running sessions and deletes only reviewed eligible IDs.
- [ ] A session becoming active after preview invalidates deletion; interrupted cleanup is resumable and does not damage retained transcripts.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Define retention separately from harness ring distillation; reuse lifecycle state, pin active/approval-waiting/referenced work and guard against a state change between preview and apply. Preserve prior defaults until configured.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

## Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test sessions
just check sessions
just test mcp
```


## Compatibility and recovery

Keep old snapshots readable; any migration preserves original bytes and uses atomic revision-checked writes. Retention requires an explicit reviewed candidate set. Reverting code must not delete or reinterpret an uncertain external effect.

## Handoff

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [[@prd/work/root--improve-sessions-client-mapping.md]] are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
