---
repo: /Users/feb/dev/cartridge
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
superseded-by: "@root/the-repository-drives-itself"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: rollup
review-round: 4
review-status: passed
canonical-scope: the-vision
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

## From the retired work memo

Folded 2026-09-15 from `work/the-vision.md` (status open). The PRD state above is authoritative.

> zirkle is a terminal wrapper with an inline agent, composed from replaceable cartridges

### Outcome

zirkle wraps the user's own terminal with an agent, composed from replaceable
cartridges. The shell survives UI replacement. The agent expresses intent,
retrieves environment-specific memos, acts through one visible `shell`, and
validates what happened from readback. `memo` supplies knowledge and routines.

The current surface follows [[the-agent-surface-preserves-the-visible-shell]]:
only the latest tool in the bottom area, no empty-tool message, main and dynamic
status, Ctrl+G composer and Ctrl+F full transcript. Agent output remains separate
from nvim and other foreground programs. Small working context crystallizes
goals, evidence, decisions and their effects; details stay retrievable.
The agent can discover, debug and extend its program as specified by
[[the-agent-can-diagnose-and-extend-its-runtime]].

[the-terminal-is-drawn-from-pty](../the-terminal-is-drawn-from-pty/prd.md) preserves this surface while moving the grid
and input encoding into `pty`. Gutter indicators and sub-agent collaboration
remain independent goals. Core composition/transport and product cartridges
follow [[core-composes-and-the-cli-selects-services]].

This continues [coding-agent-vision](../coding-agent-vision/prd.md). A request belongs when it improves the
user's terminal, the agent working visibly within it, or replaceable composition.
Attach it under the child that owns its outcome, or add a bounded new child.

### Check

- [ ] All currently required children listed in `subwork` are done with recorded evidence.
- [ ] `core/tests/test_shell.py` proves shell lifetime, resizing, interactive editor passage, composer access, separate transcript replies and cancellation.
- [ ] UI checks prove the latest-tool footer is empty before a call, paints tool readback, keeps dynamic status and clears covered composer glyphs.
- [ ] Grid migration preserves the footer/transcript contract and the editor's size and cursor across view changes.
- [ ] A composed-record scan finds every open work memo reachable from this vision and no missing prerequisites or dependency cycle.
- [ ] [runtime-stays-small-and-provable](../../../runtime/prds/runtime-stays-small-and-provable/prd.md) delivers the bounded audit, debug and extension improvements.

### Approach

[the-wrapped-shell](../the-wrapped-shell/prd.md) and [the-inline-agent](../../../ui/prds/the-inline-agent/prd.md) preserve the interaction contract;
[the-record-feeds-the-agent](../the-record-feeds-the-agent/prd.md) supplies knowledge; [cartridges-compose-live](../cartridges-compose-live/prd.md)
provides replaceability; [models-reach-the-agent](../models-reach-the-agent/prd.md) supplies models;
[the-work-can-be-proven](../the-work-can-be-proven/prd.md) owns the delivery gates.

This is a standing open vision. Current unchecked criteria are continuing
obligations, not a claim that today's gate failed. Dated results belong in child
memos and checkpoints. The former checked reply-into-scrollback assertion and
fixed count of 43 work memos described an earlier surface/board; they are not
current acceptance evidence. See the superseded decisions for that history.
