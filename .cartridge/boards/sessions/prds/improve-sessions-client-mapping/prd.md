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
footprint:
- src/roster.rs
- src/main.rs
- src/mapping.rs
- .cartridge/tests/unit/main/mapping_tests.rs
- .cartridge/tests/integration/mapping.test.ts
- .cartridge/docs/client-mapping.md
commit: "a306370f10b78d94365b7832ce22ce8d10c09487"
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
