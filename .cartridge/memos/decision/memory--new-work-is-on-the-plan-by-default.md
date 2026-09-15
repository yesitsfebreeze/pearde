---
kind: decision
date: 2026-09-08
status: superseded
description: superseded — new work was once on the plan the moment it existed, wherever it lived, with an unplaced item hanging under the vision until a planning move placed it; the whole loop from vision to parallel execution ran through operations and routines, with the CLI only a shell over them
read_when: "asking why existence counts as placement, how intake reaches the plan, or why the CLI is only a shell over the operations"
---

# new-work-is-on-the-plan-by-default

Superseded 2026-09-15: the `work` memo kind is retired. A PRD under its board's
`prds/` directory is the only work record, and `prd scan` is the plan.

## Decision

**Existence is placement.** The `plan` operation read every item the record
held, `intake/` included, so a task written anywhere was on the board on the
next scan. An item no `subwork:` or `needs:` chain carried
to [the-vision](../../boards/root/prds/the-vision/prd.md) is not off the plan: the plan hangs it directly under the
vision at axis depth 1 and counts it in the header as `unplaced`, so it
competes for `next` like any other ready part instead of sorting last as
axis-less. Placing it under a terminal — a `subwork:` line on the parent, or
a `needs:` line on it — is a planning move [[@prd/routine/root--drill.md]] makes, and
until it is made the memo is worked where it stands.

**The loop is pearde's, over the record.** A vision is one level-1 item
whose `subwork:` are the terminals ([the-vision](../../boards/root/prds/the-vision/prd.md)); the drill splits a
terminal into questions and level-10 children; the pass reads the board
with `plan`, answers the `asking` band, specs the `spec` band, and dispatches
every `ready` memo in parallel lanes, one agent each
([[@prd/decision/memory--the-pearde-workflow-is-the-work-record.md]], [[@prd/routine/run-board.md]], [[@prd/routine/run-board.md]]).

**Operations and routines, not the CLI.** Every move of the loop is a memory
operation an agent calls through the tool surface — `plan` for the read,
`memo write` for the front matter edit that claims, places or closes,
`routine_<leaf>` for the procedure — and `memory plan`, `memory memo` are shells
over the same operations for a person at a terminal. A routine is reached
through its skill, which calls the operation ([[new-routine]]).

## Why

The user, 2026-09-08: "tasks and intake stuff that we put into the work
needs to be planned into the plan by default. The idea is the same as in
PRD: we describe a vision of what we want the product to be, then we plan
dynamically to move as fast as possible in parallel towards this plan. And
all of this should be able to be done via routines and commands rather than
a CLI command."

Most of the loop already stands: the seven bands, the scan, the pass and the
vision landed this week. What contradicted the default was the axis:
`plan.rs` answers `axis: null` for a part no chain reaches the vision from,
and `next` sorts by axis depth, so an intake task nobody linked was visible
but never next — planned in the sense of listed, not in the sense of moving.
Hanging it under the vision is the smallest rule that makes writing a task
the same act as planning it. The operation surface exists too; what breaks
"via commands" today is not a missing operation but the MCP server that does
not answer `initialize` ([memory-mcp-never-answers-initialize](../../boards/memory/prds/memory-mcp-never-answers-initialize/prd.md)), which is
why every skill currently falls back to `just memo <leaf>`.

## Consequences

- [unplaced-work-hangs-under-the-vision](../../boards/memory/prds/unplaced-work-hangs-under-the-vision/prd.md) changes `plan.rs`; until it lands,
  a new task is placed by hand with one `needs:` line.
- [memory-mcp-never-answers-initialize](../../boards/memory/prds/memory-mcp-never-answers-initialize/prd.md) is on the critical path of "via
  commands": every routine's primary path is `mcp__memory__routine_<leaf>`.
- A memo that stays `unplaced` through a pass is a question for the drill,
  not a defect in the memo.
- [build-the-composition-pillar](../../boards/memory/prds/build-the-composition-pillar/prd.md) is placed as a terminal of the vision by
  this decision's rule, not left beside it.
