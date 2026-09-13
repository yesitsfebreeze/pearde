---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 3
review-status: "passed"
needs:
- '@sessions/improve-sessions-client-mapping'
commit: "92240c6ba415f53b2d17971aea185536a6f517bc"
---

# Retain bounded, reported file-change evidence per session

Give direct and overlay producers one Sessions-owned record schema and a durable
read API. Current `touch` only inserts a path into `Session.files`; measured FS
and GitFS changes cannot retain actor, operation, storage target or revisions.
This leaf owns storage and validation, not filesystem mutation or authentication.

Keep existing `touch`, `files`, transcript, agent revision and mapping behavior.
New records are optional when loading old snapshots. Actor fields are reported
invocation coordinates; they grant no session access, client identity or GitFS
ownership. Native Sessions remains behind its existing trusted host boundary.

## Acceptance

- [x] Strict shared DTO rejects unknown fields, invalid revisions/targets and actor/session mismatch; rerecording one publication is idempotent while distinct publications remain distinct.
- [x] Bounded atomic append persists records across restart; prepublication failure preserves old state and uncertain publication remains explicit.
- [x] Revision-bound pages expose exact retained records without file reads or mutation; legacy touched paths remain readable without invented attribution.
- [x] Public Sessions tests/check and native persistence/capacity/legacy fixtures pass; current roster, mailbox, mapping and transcript behavior remains compatible.

Reuse the existing per-session transaction/gate and atomic snapshot publisher.
Never silently evict records, create sessions, retry mutations or repair snapshots.
Inherit the original provenance requirement's two used review rounds.
