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
canonical-scope: improve-sessions-recovery
footprint:
- /Users/feb/dev/cartridge/sessions.ctg/main.rs
- /Users/feb/dev/cartridge/sessions.ctg/README.md
---

# Explain session damage and narrowly repair eligible snapshots

A read-only recovery report distinguishes missing, legacy, corrupt and incomplete-run records with safe next steps.

## Acceptance

- [ ] Fixtures for missing, legacy-empty, corrupt and uncertain-run states produce distinct diagnoses; inspection changes no files.
- [ ] Only eligible legacy-empty snapshots can be repaired, backups are preserved, and a repeated repair cannot overwrite an existing backup or transcript.

- [ ] Keep old snapshots readable; any migration preserves original bytes and uses atomic revision-checked writes. Retention requires an explicit reviewed candidate set. Reverting code must not delete or reinterpret an uncertain external effect.

## Proof and recovery

Start at [main.rs](../../../main.rs), [README.md](../../../README.md).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-sessions-recovery`; maximum five rounds.
