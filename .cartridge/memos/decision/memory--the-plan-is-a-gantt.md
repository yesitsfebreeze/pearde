---
kind: decision
date: 2026-09-06
status: superseded
description: typed `estimate:`, `actual:`, `claim:`, `due:` and `needs:` lines place a live work part in time, and git's two stamps place a done one
read_when: "adding a front matter key to a work part, or asking where a part sits in time"
---

# the-plan-is-a-gantt

Raised by the user 2026-09-06: every part categorised, sorted by category
and by time, and its timing read off the front matter — done, not done,
claimed, needs a spec.

This records a superseded design. Current planning is owned by the native PRD cartridge; source cartridges no longer provide a scheduler or planning loop.

## Decision

**The `plan` operation is `~/dev/infra/pearde/resources/board/schedule.py`
over `kind: work` parts.**

- **Five optional front matter lines carry the timing, and each has a
  type.** `estimate:` and `actual:` are durations (`30m`, `4h`, `2d`, bare
  hours) — pearde's `est` and `actual`; `claim: <who> <YYYY-MM-DD HH:MM>`
  is pearde's own claim line; `due:` is a date or date-time; `needs:` is
  its `needs:` as wikilinks. A `subwork:` child is an implicit need of its
  parent, as a pearde child is. No new kind, no new state word: `status:`
  keeps `open | blocked | done`.
- **The grammar lives once, in the work-field table**, run over every work
  part in the record by `tests/memos_fields.rs`, so a value that does not
  parse fails `cargo test` by name rather than scheduling at the average and
  looking estimated ([[gates-are-tests]]). The user's line: "we need
  estimated times and length and all that as types".
- **Six bands, in pressure order** — `spec` (open, no `## Check`), `blocked`,
  `claimed`, `ready` (nothing it needs is open), `later`, `done`. The band
  is derived on every read, never stored.
- **Time comes from two places.** A done part is placed `actual:` long
  ending at its latest commit, or from git's first commit of it to its
  latest — `part list` answers `created`, `modified` and `check` per row,
  one `git log` per root. A live part is simulated from now with unlimited
  hands, so the schedule is the critical path itself; a claim starts when it
  was claimed and keeps what is left of its estimate, never less than a
  twentieth. Eight hours of work is one day of axis.
- **Unestimated parts take the board's average**, as pearde's do; a parent
  with a live child weighs nothing and folds when they are done.
- **The vision is the one work part at the lowest level** — [[@prd/work/memory--the-vision.md]],
  level 1, its `subwork:` the terminals — and the axis is pearde's: a part's
  depth is the longest chain from it up to the vision, and a part no chain
  carries there is off the axis. The plan's header reads the vision's
  sentence, the hours to it, what is in flight and by whom, and **next**:
  the ready parts deepest on the axis, then by what they unblock.
- **The record's category axis is `kind`,** in the order work, question,
  decision, research, insight, knowledge, documentation, routine — the
  actionable kinds first — newest inside each. A work row shows its band, a
  decision its status.

## Why

Pearde's calendar is a discrete-event simulation with a worker cap, a
footprint-clash pass and three wall numbers; the port keeps the forward pass
over `needs`, the backward pass for slack, the container rule and the claim
burn-down, and drops the cap (pearde itself never binds the board's
`workers:` without an explicit ask), footprints (a part names no files) and
the parked state (the record has none). One sentence of the user's decides
the shape: "we should always have a clear overview of what's happening in the
workspace, the plan, and what's next" — so the header is the overview and
the vision is written down as the goal the axis measures against.

Against the field — every 2026 agent orchestrator ships a kanban and none a
gantt, and time rides on cards as relative age — the gantt stays because the
user asked for timing. The claim lease and heartbeat (Hermes kanban), the
`ready` label meaning "has acceptance criteria" (the `## Check` rule here)
and the assignee-plus-status atomic claim (Beads) are the three conventions
the survey found stable; all three are in.

Git stamps over a `done:` date because nothing writes one, and a stamp a
person must remember to write is a stamp the record will not carry
(`a-conditional-mechanism-under-an-absolute-claim`). The first commit
under-reads a part imported in one commit — every part the fold brought in
was "born" 2026-09-05 15:32 — and the latest commit over-reads a part touched
by a rename; both are what git knows, and both are right the day after.

## Consequences

- `part list` answers three more fields; a root that is not a git repository
  answers mtime for both stamps and the axis still holds.
- A work part with a `claim:` line is in flight whatever its `status:` says.
  Nothing yet writes or expires the line — a claim older than a session is
  the next question, and the lease the survey found is the likely answer.
- Every open part with no `needs:` is on the critical chain at once, so a
  board that has written no `needs:` reads as every ready part critical. The
  chain means something the day the first `needs:` line is written; the axis
  already means something, because `subwork:` is a need and the vision names
  its terminals — 42 of the 51 live parts are on it today.
- Two parts sharing the lowest level is no vision: the header says so and
  every part is off the axis until one of them is lifted.
- The `spec` band is empty on this record today: every work part carries a
  `## Check`. It is the band a drill leaves a part in.
