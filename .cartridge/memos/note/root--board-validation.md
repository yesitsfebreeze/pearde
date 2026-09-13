---
kind: note
memo: board-validation
status: decided
subject: Development board validation and limits
description: Evidence for the authored recursive development plans and explicit integration gaps
date: 2026-09-13
---

# Board validation

The root and child boards are planning artifacts. All 16 PRDs remain open; no implementation acceptance boxes or completed work are claimed.

`just board-check` passes the installed Pearde memo, workflow and grammar validators and scans 16 PRDs across 17 declared members. `just board-plan` uses that engine's ordered scan because its current `plan <path>` parser treats the path as a group. These commands do not launch a development pass.

The additional validation probe uses Pearde's real registry and dependency resolver to check every dependency and detect cycles. It also checks authored Markdown links, each child entry memo, native type declaration presence, and shared workflow/grammar resolution from all child settings. Its temporary reproduction script is `/tmp/check-cartridge-board.py`; it depends on the installed engine source location, not a new project planner implementation.

Observed result: 17 members, 16 open PRDs, 28 resolved dependency edges, no cycles, 120 initial authored files with valid local Markdown links, 17 child entry memos, and 34 passing child workflow/grammar checks.

The reference engine source is `/Users/feb/dev/infra/pearde`, revision `ae2d5b4075564a3c4c069a6d2b347ab406c749fc`. Full native Pearde transition parity, automatic template installation, all-kind memo bridging, and arbitrary-depth Landscape discovery are acceptance gates in the open plans. Native memo validation of all legacy child records is not claimed by the configured Pearde note view.

Memory's authored board was committed in its required isolated worktree and fast-forwarded into its local main branch as `057c971`. Its ignore rules share only the new development memo/type declarations while retaining the existing ignore behavior for other memory-local memos. The remaining planning changes are local working-tree files. Nothing was pushed.

See the [assessment](../../boards/root/CARTRIDGE-ASSESSMENT.md) for the earlier 294 passing component tests, the reproduced MCP result-envelope failure and limits on retrieval, live-provider and full-system coverage. This documentation pass does not rerun or extend those implementation claims.
