---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: reflex-reports-attributed-tool-outcomes
---

# reflex-reports-attributed-tool-outcomes

Use the existing execution/session observation boundary as the owner of tool-use attribution. Classify actor and activity origin, attempt versus completion, outcome, duration and size; retain unknown historical fields. Landscape can consume the evidence, but memory does not host a second Reflex service.

## Acceptance

- [ ] A mixed fixture of agent calls, UI reads, polling, discovery and cancelled work produces distinct correctly attributed observations.
- [ ] Old rows retain unknown status/time rather than gaining invented success or billing; source/descriptor changes identify stale verdicts.
- [ ] Default telemetry excludes sensitive arguments/bodies, has bounded retention and cannot turn observation failure into tool failure.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `reflex-reports-attributed-tool-outcomes`; maximum five rounds.
