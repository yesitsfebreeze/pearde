---
kind: work
description: "zirkle is a terminal wrapper with an inline agent, composed from replaceable cartridges"
status: open
subwork:
  - "[[@prd/work/root--runtime-stays-small-and-provable.md]]"
  - "[[@prd/work/root--the-wrapped-shell.md]]"
  - "[[@prd/work/root--the-inline-agent.md]]"
  - "[[@prd/work/root--the-record-feeds-the-agent.md]]"
  - "[[@prd/work/root--cartridges-compose-live.md]]"
  - "[[@prd/work/root--models-reach-the-agent.md]]"
  - "[[@prd/work/root--the-work-can-be-proven.md]]"
  - "[[@prd/work/root--the-terminal-is-drawn-from-pty.md]]"
  - "[[@prd/work/root--the-gutter-is-the-boundary.md]]"
  - "[[@prd/work/root--sub-agents-share-the-terminal.md]]"
  - "[[@prd/work/root--zirkles-tools-serve-any-agent.md]]"
  - "[[@prd/work/root--cartridges-compose-recursively.md]]"
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

[[@prd/work/root--the-terminal-is-drawn-from-pty.md]] preserves this surface while moving the grid
and input encoding into `pty`. Gutter indicators and sub-agent collaboration
remain independent goals. Core composition/transport and product cartridges
follow [[core-composes-and-the-cli-selects-services]].

This continues [[@prd/work/root--coding-agent-vision.md]]. A request belongs when it improves the
user's terminal, the agent working visibly within it, or replaceable composition.
Attach it under the child that owns its outcome, or add a bounded new child.

## Check

- [ ] All currently required children listed in `subwork` are done with recorded evidence.
- [ ] `core/tests/test_shell.py` proves shell lifetime, resizing, interactive editor passage, composer access, separate transcript replies and cancellation.
- [ ] UI checks prove the latest-tool footer is empty before a call, paints tool readback, keeps dynamic status and clears covered composer glyphs.
- [ ] Grid migration preserves the footer/transcript contract and the editor's size and cursor across view changes.
- [ ] A composed-record scan finds every open work memo reachable from this vision and no missing prerequisites or dependency cycle.
- [ ] [[@prd/work/root--runtime-stays-small-and-provable.md]] delivers the bounded audit, debug and extension improvements.

## Approach

[[@prd/work/root--the-wrapped-shell.md]] and [[@prd/work/root--the-inline-agent.md]] preserve the interaction contract;
[[@prd/work/root--the-record-feeds-the-agent.md]] supplies knowledge; [[@prd/work/root--cartridges-compose-live.md]]
provides replaceability; [[@prd/work/root--models-reach-the-agent.md]] supplies models;
[[@prd/work/root--the-work-can-be-proven.md]] owns the delivery gates.

This is a standing open vision. Current unchecked criteria are continuing
obligations, not a claim that today's gate failed. Dated results belong in child
memos and checkpoints. The former checked reply-into-scrollback assertion and
fixed count of 43 work memos described an earlier surface/board; they are not
current acceptance evidence. See the superseded decisions for that history.
