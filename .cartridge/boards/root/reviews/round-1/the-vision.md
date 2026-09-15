---
kind: work
description: "zirkle is a terminal wrapper with an inline agent, composed from replaceable cartridges"
status: open
subwork:
  - "[runtime-stays-small-and-provable](../../../runtime/prds/runtime-stays-small-and-provable/prd.md)"
  - "[the-wrapped-shell](../../prds/the-wrapped-shell/prd.md)"
  - "[the-inline-agent](../../../ui/prds/the-inline-agent/prd.md)"
  - "[the-record-feeds-the-agent](../../prds/the-record-feeds-the-agent/prd.md)"
  - "[cartridges-compose-live](../../prds/cartridges-compose-live/prd.md)"
  - "[models-reach-the-agent](../../prds/models-reach-the-agent/prd.md)"
  - "[the-work-can-be-proven](../../prds/the-work-can-be-proven/prd.md)"
  - "[the-terminal-is-drawn-from-pty](../../prds/the-terminal-is-drawn-from-pty/prd.md)"
  - "[the-gutter-is-the-boundary](../../../ui/prds/the-gutter-is-the-boundary/prd.md)"
  - "[sub-agents-share-the-terminal](../../../agent/prds/sub-agents-share-the-terminal/prd.md)"
  - "[zirkles-tools-serve-any-agent](../../prds/zirkles-tools-serve-any-agent/prd.md)"
  - "[cartridges-compose-recursively](../../../runtime/prds/cartridges-compose-recursively/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["Deciding what zirkle is for, whether a request belongs on the board, or which child work a new memo attaches under"]
---

# the-vision

## Outcome

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

[the-terminal-is-drawn-from-pty](../../prds/the-terminal-is-drawn-from-pty/prd.md) preserves this surface while moving the grid
and input encoding into `pty`. Gutter indicators and sub-agent collaboration
remain independent goals. Core composition/transport and product cartridges
follow [[core-composes-and-the-cli-selects-services]].

This continues [coding-agent-vision](../../prds/coding-agent-vision/prd.md). A request belongs when it improves the
user's terminal, the agent working visibly within it, or replaceable composition.
Attach it under the child that owns its outcome, or add a bounded new child.

## Check

- [ ] All currently required children listed in `subwork` are done with recorded evidence.
- [ ] `core/tests/test_shell.py` proves shell lifetime, resizing, interactive editor passage, composer access, separate transcript replies and cancellation.
- [ ] UI checks prove the latest-tool footer is empty before a call, paints tool readback, keeps dynamic status and clears covered composer glyphs.
- [ ] Grid migration preserves the footer/transcript contract and the editor's size and cursor across view changes.
- [ ] A composed-record scan finds every open work memo reachable from this vision and no missing prerequisites or dependency cycle.
- [ ] [runtime-stays-small-and-provable](../../../runtime/prds/runtime-stays-small-and-provable/prd.md) delivers the bounded audit, debug and extension improvements.

## Approach

[the-wrapped-shell](../../prds/the-wrapped-shell/prd.md) and [the-inline-agent](../../../ui/prds/the-inline-agent/prd.md) preserve the interaction contract;
[the-record-feeds-the-agent](../../prds/the-record-feeds-the-agent/prd.md) supplies knowledge; [cartridges-compose-live](../../prds/cartridges-compose-live/prd.md)
provides replaceability; [models-reach-the-agent](../../prds/models-reach-the-agent/prd.md) supplies models;
[the-work-can-be-proven](../../prds/the-work-can-be-proven/prd.md) owns the delivery gates.

This is a standing open vision. Current unchecked criteria are continuing
obligations, not a claim that today's gate failed. Dated results belong in child
memos and checkpoints. The former checked reply-into-scrollback assertion and
fixed count of 43 work memos described an earlier surface/board; they are not
current acceptance evidence. See the superseded decisions for that history.
