---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-sessions-client-mapping
footprint: ["src/roster.rs","src/channels.rs","src/mailbox.rs","src/main.rs","src/mapping.rs",".cartridge/tests/unit/main/mapping_tests.rs",".cartridge/tests/integration/mapping.test.ts",".cartridge/docs/client-mapping.md","src/observations.rs","Cargo.toml","src/lib.rs","src/change_record.rs","src/changes.rs",".cartridge/tests/unit/main/change_records_tests.rs","src/context.rs",".cartridge/tests/unit/main/context_tests.rs",".cartridge/tests/integration/context.test.ts"]
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
---

# Map client conversations to cartridge sessions honestly

Only a host-authenticated connection identity plus an explicitly supplied external conversation identifier can create a durable mapping. Treat arbitrary clientInfo/name fields as untrusted description. If authenticated identity or conversation ID is absent, use a clearly labelled connection scope and retain no invented cross-reconnect identity.

## Acceptance

- [x] The same authenticated client/workspace/external ID resolves its own mapping after reconnect.
- [x] Another authenticated client, workspace or profile cannot reuse it by copying metadata; missing IDs remain connection-scoped.
- [x] Legacy session files remain readable and mapping writes use revision-checked atomic persistence without rewriting transcripts.

## Proof and recovery

Owner contracts: `sessions.ctg/src/main.rs` and the native SDK host configuration boundary. Baseline at source `4dd8518e2f9fb1bf63f191acffe3777d4eec3b5c`: the real SDK process returns `unknown sessions op mapping`; see [inputs](baseline-inputs.json) and [log](baseline.log).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-sessions-client-mapping`; maximum five rounds.

Reverify unchanged acceptance after the next integrated owner feature; earlier
181adb20 receipt retained. No contract relaxation.

Reverification at965108d9 after mailbox integration. Add the new transitive source module to verification coverage; behavioral acceptance is unchanged.

Reverification: attributed report at2a6a863 adds native main dispatch; bind src/observations.rs as transitive source, retaining previous acceptance and executable gates.

Named channel registration revalidation at 423ecd32: source footprint includes registered channels and its shared mailbox codec; acceptance and behavior gates remain unchanged.

## From the retired work memo

Folded 2026-09-15 from `work/improve-sessions-client-mapping.md` (status open). The PRD state above is authoritative.

### Outcome

A session reports its client identity and correlation scope without pretending connection-scoped IDs are Codex conversation IDs.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [sub-agent-sessions-record-parent-and-mailbox](../sub-agent-sessions-record-parent-and-mailbox/prd.md), [the-board-is-channels-of-lines](../the-board-is-channels-of-lines/prd.md).

### Footprint

Sessions; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `sessions.ctg/main.rs`
- `sessions.ctg/README.md`
- `mcp.ctg/service.rs`
- `agent.ctg/run_state.rs`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] Reconnect with the same trusted external identity and workspace retrieves the intended mapping; another client/workspace cannot inherit it.
- [ ] A client providing no conversation ID is labelled connection-scoped and never assigned a fabricated Codex identity.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Determine what trusted MCP/client metadata actually exists. Store explicit external mappings when available, otherwise label connection scope. Preserve backward compatibility and isolate identities across clients/workspaces; coordinate with active board persistence work.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test sessions
just check sessions
just test mcp
```


### Compatibility and recovery

Keep old snapshots readable; any migration preserves original bytes and uses atomic revision-checked writes. Retention requires an explicit reviewed candidate set. Reverting code must not delete or reinterpret an uncertain external effect.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
