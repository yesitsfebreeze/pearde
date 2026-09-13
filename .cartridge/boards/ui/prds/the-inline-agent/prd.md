---
repo: /Users/feb/dev/cartridge/ui.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: ui
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: the-inline-agent
needs:
- '@ui/the-gutter-is-the-boundary'
- '@ui/the-gutter-shows-both-sides'
- '@ui/the-panel-switches-to-a-sub-agent'
- '@ui/improve-ui-terminal-owner'
---

# the-inline-agent

Track the linked current outcomes as a finite scope snapshot. Historical framework and product proposals remain source history.

## Acceptance

- [ ] Each included leaf has its own current acceptance and owner.
- [ ] Close this snapshot only against observed child evidence; later enhancements get separate work items.

## Work items

- [the-gutter-is-the-boundary](../the-gutter-is-the-boundary/prd.md)
- [the-gutter-shows-both-sides](../the-gutter-shows-both-sides/prd.md)
- [the-panel-switches-to-a-sub-agent](../the-panel-switches-to-a-sub-agent/prd.md)
- [Display shared terminal ownership and cwd](../improve-ui-terminal-owner/prd.md)

## Review

[Round 2 agent review](review.md). Inherits round 1 from `the-inline-agent`; maximum five rounds.
