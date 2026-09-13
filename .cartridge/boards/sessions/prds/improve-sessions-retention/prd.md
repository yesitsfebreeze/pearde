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
footprint:
- src/roster.rs
- src/main.rs
- src/mapping.rs
- src/retention.rs
- .cartridge/tests/unit/main/retention_tests.rs
- .cartridge/tests/integration/retention.test.ts
- .cartridge/docs/retention.md
commit: "a306370f10b78d94365b7832ce22ce8d10c09487"
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
