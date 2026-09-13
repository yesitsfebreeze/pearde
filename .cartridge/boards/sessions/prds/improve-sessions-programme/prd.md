---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-sessions-programme
needs:
- '@sessions/improve-sessions-client-mapping'
- '@sessions/improve-sessions-retention'
- '@sessions/improve-sessions-recovery'
commit: "2a6a863cf1af0876072f8879050274cfa650a785"
---

# Sessions improvement plan

Coordinate the three linked owner outcomes at one integrated source revision. The [baseline](baseline.json) shows retention collected at `b772c6e`, while mapping and recovery receipts require refresh after their shared source changed. This rollup adds executable combined verification and no source implementation.

## Acceptance

- [x] Each linked leaf passes its own review and observable acceptance.
- [x] Record tested mitigations and remaining limitations at the integrated revisions.

## Work items

- [Map client conversations to cartridge sessions honestly](../improve-sessions-client-mapping/prd.md)
- [Preview and apply safe session retention](../improve-sessions-retention/prd.md)
- [Explain session damage and narrowly repair eligible snapshots](../improve-sessions-recovery/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-sessions-programme`; maximum five rounds.

Reverification at965108d9 after mailbox integration. Add the new transitive source module to verification coverage; behavioral acceptance is unchanged.

Reverification: attributed report at2a6a863 adds native main dispatch; bind src/observations.rs as transitive source, retaining previous acceptance and executable gates.
