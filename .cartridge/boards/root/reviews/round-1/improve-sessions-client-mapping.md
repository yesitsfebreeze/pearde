---
kind: work
description: "Map client conversations to cartridge sessions honestly"
status: open
priority: P1
size: M
uses:
  - usage: "[[read-usage]]"
    when: ["map client conversations to cartridge sessions honestly", "implementing sessions cartridge improvements"]
---

# Map client conversations to cartridge sessions honestly

## Outcome

A session reports its client identity and correlation scope without pretending connection-scoped IDs are Codex conversation IDs.

## Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [sub-agent-sessions-record-parent-and-mailbox](../../../sessions/prds/sub-agent-sessions-record-parent-and-mailbox/prd.md), [the-board-is-channels-of-lines](../../../sessions/prds/the-board-is-channels-of-lines/prd.md).

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
- [ ] Reconnect with the same trusted external identity and workspace retrieves the intended mapping; another client/workspace cannot inherit it.
- [ ] A client providing no conversation ID is labelled connection-scoped and never assigned a fabricated Codex identity.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

## Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Determine what trusted MCP/client metadata actually exists. Store explicit external mappings when available, otherwise label connection scope. Preserve backward compatibility and isolate identities across clients/workspaces; coordinate with active board persistence work.
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

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
