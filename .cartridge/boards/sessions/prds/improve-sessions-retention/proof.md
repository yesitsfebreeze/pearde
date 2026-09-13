# Verified safe session retention

Source: `b772c6ee4f1ad476995c8c8c07cd02ed2be264fa`. [Exact source/consumer inputs and commands](proof-inputs.json).

- Sessions: **41 native tests passed**, including all 32 previous mapping/recovery/checkpoint/persistence cases.
- Public sessions check/build passed; public harness build and **41 tests passed**. Existing concurrent harness changes were preserved and their source digests recorded.
- Native process integration: **7 tests, 83 assertions passed**. Actual sessions and harness SDK subprocesses exercise ordinary successful ring eviction and the race where the turn becomes running during committed memory ingest. The latter preserves the exact post-activity snapshot and reports the deletion refusal.
- Interruption matrix covers durable plan, backup, unlink-before-journal-update and post-unlink directory sync uncertainty; explicit resume retains exact backups, never expands its candidate set and preserves same-ID replacements, including identical bytes.
- Stale previews/protection revisions, pins, registered/parent/mapping references, busy apply/resume locks, malformed journal/partial backup, oversized snapshots and symlink/traversal evidence fail safely. Notifications name newly completed deletions and do not repeat on completed resume.

Only disposable fixtures were deleted. Summary output and committed memory ingest
are synthetic integration providers; no live model or user session store was used.

Review remains round 3, **95/100** by independent coordinator `/root`. The verify
command was expanded to build/inject the actual harness binary for the already
reviewed harness compatibility acceptance; no acceptance criterion, owner boundary
or failure behavior was relaxed. The final source adds ordinary delete notifications
for successful retention changes, preserving the existing sessions event contract.

Coordinator must collect this PRD, then refresh client-mapping and recovery
receipts because the shared source footprint changed.
