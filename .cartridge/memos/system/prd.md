---
kind: system
description: PRD owns planning, specifications, dependency schedules and work orchestration
order: -40
---

The `prd` cartridge owns planning for this composition. Use its tool to inspect
the central board, prepare specifications, refine sub-PRDs, view the dependency
plan and Gantt, and perform checked work transitions. Project cartridges own
their code; PRD alone knows the mapping from planning records to those repositories.

For continuous work with this host's sub-agents, read
`@prd/routine/run-board.md`. Continue from the persisted board and checkpoint,
rescan after each collected result, and never equate a worker's successful exit
with verified and integrated work. Ratings are agent-owned unless the user changes
that policy. Keep real external blockers visible while working independent leaves.

PRD publishes observed changes on the runtime's `prd` event channel. Memory
provides recalled evidence and retains verified outcomes; PRD files remain the
authority for dependencies, claims and completion. No other cartridge needs
PeaRDe scripts, planning settings, or knowledge of PRD's storage layout.
