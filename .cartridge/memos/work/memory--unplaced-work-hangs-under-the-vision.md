---
kind: work
level: 10
status: done
estimate: 2h
description: the `plan` operation gives a work memo no chain reaches the vision from axis depth 1 under the vision and counts it as `unplaced` in the header, so a task written anywhere competes for `next` from the moment it exists
read_when: "touching the plan's axis, or asking why a new task is never next"
---

# unplaced-work-hangs-under-the-vision

## Do

In `src/rpc/src/plan.rs`: where `depth()` answers `None` for a task the
vision's chains do not reach, answer `Some(1)` instead and mark the task
`unplaced: true`; the header gains `unplaced: <count>`; a task that is the
vision itself or done stays as it is. Update the crate doc at the top of
`plan.rs` and [[@prd/decision/memory--the-plan-is-a-gantt.md]]'s sentence on the axis with one line
naming this rule.

## Check

`cargo test -p rpc plan` passes with the existing axis tests amended: the
test at `plan.rs:740` that asserted `axis: null` for a task without a chain
asserts `axis: 1` and `unplaced: true`, and a new assertion shows that task
appearing in `next` ahead of a placed task shallower than it. `memory plan`
on the project record prints an `unplaced` count in the header.

**Done for the plan.rs core.** The axis assignment maps an unreached live
memo to depth `Some(1)` with `unplaced: true` — a task written anywhere
competes for `next` from the moment it exists — while the vision (depth 0)
and a done memo keep the depth the chains answer. The header and
`progress` carry `unplaced` counts, folding the `unplanned`/`off_axis`/
`off-axis` naming cbe62715 added into the memo's contract; the crate doc
names the rule.
