---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-sessions-retention
footprint: ["src/roster.rs","src/channels.rs","src/mailbox.rs","src/main.rs","src/mapping.rs","src/retention.rs",".cartridge/tests/unit/main/retention_tests.rs",".cartridge/tests/integration/retention.test.ts",".cartridge/docs/retention.md","src/observations.rs","Cargo.toml","src/lib.rs","src/change_record.rs","src/changes.rs",".cartridge/tests/unit/main/change_records_tests.rs","src/context.rs",".cartridge/tests/unit/main/context_tests.rs",".cartridge/tests/integration/context.test.ts"]
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
needs:
- "@sessions/improve-sessions-client-mapping"
---

# Preview and apply safe session retention

Remove external-client mapping as a hard dependency. Retention relies on canonical session IDs, live-run/approval state, explicit pins and registered references. Preview returns eligible IDs/revisions and reasons; apply rechecks pins under the store's mutation boundary and journals each deletion step for crash recovery.

## Acceptance

- [x] An active, pinned, approval-waiting or referenced session is never eligible; totals distinguish bytes and record counts.
- [x] Becoming active or referenced after preview refuses deletion at apply without touching the transcript.
- [x] An interrupted cleanup resumes only its recorded eligible deletions and preserves all retained sessions and backup evidence.

## Proof and recovery

Baseline at sessions `181adb20248c6fdb718823919438939de55bdefc`: a real disposable SDK fixture reports unknown retention preview and allows generic deletion of a running session; [requests/results](baseline.json). Existing harness ring filters activity before distillation, then calls generic sessions delete, leaving a state-change race.

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-sessions-retention`; maximum five rounds.

Reverification at965108d9 after mailbox integration. Add the new transitive source module to verification coverage; behavioral acceptance is unchanged.

Reverification: attributed report at2a6a863 adds native main dispatch; bind src/observations.rs as transitive source, retaining previous acceptance and executable gates.

Named channel registration revalidation at 423ecd32: source footprint includes registered channels and its shared mailbox codec; acceptance and behavior gates remain unchanged.

## From the retired work memo

Folded 2026-09-15 from `work/improve-sessions-retention.md` (status open). The PRD state above is authoritative.

### Outcome

An operator can inspect stored session sizes/ages and eligible cleanup candidates before deleting closed unpinned sessions.

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
- [ ] A mixed fixture reports byte/count/age totals, preserves pinned and running sessions and deletes only reviewed eligible IDs.
- [ ] A session becoming active after preview invalidates deletion; interrupted cleanup is resumable and does not damage retained transcripts.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Define retention separately from harness ring distillation; reuse lifecycle state, pin active/approval-waiting/referenced work and guard against a state change between preview and apply. Preserve prior defaults until configured.
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

Priority P2; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
Ready after [improve-sessions-client-mapping](../improve-sessions-client-mapping/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
