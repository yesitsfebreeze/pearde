---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "specced"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: scoped-roster-projection
needs: ["@sessions/an-agent-is-one-lookup-from-the-roster/durable-channel-read-cursors"]
commit: "a306370f10b78d94365b7832ce22ce8d10c09487"
---

# Project scoped session activity and watched unread counts

Build a read-only roster from existing sessions, immutable membership and channel snapshots. Include only authorized session metadata and named-channel unread counts, with contributor revisions and observation time. Never read another actor’s transcript or direct mailbox.

## Acceptance

- [x] A20-session fixture stays within row/byte caps, reports omissions, suppresses outside-scope sessions/parent references and rejects copied credentials/identity metadata.
- [x] A child phase change appears without a board post; never-started sessions have an explicit phase and missing activity duration remains unknown.
- [x] Watch/read/ack changes only the requester’s unread progress; roster queries do not acknowledge messages or mutate source snapshots, and unavailable channel data is partial.

## Baseline and review

The parent roster baseline records actual absent SDK operations at423ecd3 and existing harness/Landscape boundaries. This child inherits original roster review rounds1–2; independent round3 review by /root passed 96/100 before implementation. Tests use disposable data. Source implementation is committed at a306370f10b78d94365b7832ce22ce8d10c09487. Detailed proof/recovery is in specs/spec01.md.
