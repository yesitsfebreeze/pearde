---
repo: /Users/feb/dev/cartridge/agent.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: agent
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: an-event-declares-its-type
---

# an-event-declares-its-type

Register event types through host-owned declarations with a fixed projection authority ceiling. Ordinary events can produce labelled data frames or remain non-projecting; they cannot request system/developer authority. Keep version-1 message projection compatible and expose unknown types as skipped evidence.

## Acceptance

- [ ] All current event types resolve and old sessions project identically under a fixed fixture.
- [ ] An untrusted declared type requesting privileged framing is refused or rendered as attributed data, never elevated.
- [ ] Unknown versions/types remain durable and visible in inspection; adding a safe new type does not require another branch in the generic projector.

## Proof and recovery

Start at [model_loop.rs](../../../model_loop.rs), [run_state.rs](../../../run_state.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test agent` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `an-event-declares-its-type`; maximum five rounds.
