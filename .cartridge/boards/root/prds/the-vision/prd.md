---
repo: /Users/feb/dev/cartridge
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: the-vision
needs:
- the-composed-system-proves-the-plan
- cartridge-improvement-programme
---

# The current release snapshot closes only on observed child evidence

Roll-up only: the vision's finite snapshot is the composed-system release gate plus the improvement programme. Historical framework and product proposals remain source history; later enhancements get separate work items.

## Acceptance

- [ ] Both linked items are `done` with their own recorded gate evidence at one set of submodule SHAs.
- [ ] A child that fails, exhausts its rounds or is retired keeps this snapshot open, with the gap named in Result.

## Work items

- [The composed system passes the complete workflow and retires redundant wrappers](../the-composed-system-proves-the-plan/prd.md)
- [Cartridge improvement programme](../cartridge-improvement-programme/prd.md)

## Integration and recovery

The integration gate is the composed-system item's: `just check`, `just test`, `just smoke`, `just verify` and `just isolation` from `/Users/feb/dev/cartridge`. It is not repeated here and has not run for this plan. Both children currently fail review on needs held by other boards (the dissolved landscape board, superseded or dropped owners), so this snapshot cannot close yet. Nothing is implemented or rolled back at this level.

## Review

[Review history](review.md). Inherits round 1 from `the-vision`; 4 of 5 used.
