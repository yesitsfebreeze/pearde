---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: sessions
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-sessions-retention
footprint:
- /Users/feb/dev/cartridge/sessions.ctg/main.rs
- /Users/feb/dev/cartridge/sessions.ctg/README.md
---

# Preview and apply safe session retention

Remove external-client mapping as a hard dependency. Retention relies on canonical session IDs, live-run/approval state, explicit pins and registered references. Preview returns eligible IDs/revisions and reasons; apply rechecks pins under the store's mutation boundary and journals each deletion step for crash recovery.

## Acceptance

- [ ] An active, pinned, approval-waiting or referenced session is never eligible; totals distinguish bytes and record counts.
- [ ] Becoming active or referenced after preview refuses deletion at apply without touching the transcript.
- [ ] An interrupted cleanup resumes only its recorded eligible deletions and preserves all retained sessions and backup evidence.

## Proof and recovery

Start at [main.rs](../../../main.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-sessions-retention`; maximum five rounds.
