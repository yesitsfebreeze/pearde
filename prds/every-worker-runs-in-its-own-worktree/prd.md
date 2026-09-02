---
state: done
origin: requested
priority: 0
complexity: 39
blast-radius: high
workflow: probe-then-spec
actual: 0.65h
---

# Every worker runs in its own worktree

Every analyst and implementer works in a git worktree of its own, on a branch `lane/<prd-slug>`, never in the checkout the orchestrator holds. When this is done: `pearde claim` creates the worktree and the brief names it as `<repo>`; a probe's uncommitted code lives in that worktree and survives the verdict there; `collect` merges the lane into the checkout's branch, runs the verify blocks and the gate on the merged tree, and a merge conflict is a red collect naming the file, never a silent stage; the footprint clash gate on `claimed` PRDs stays as the scheduler's edge but no longer refuses a claim — two PRDs on one file are serialized by the plan and resolved at the merge; `sweep` removes the worktree of a claim it releases. Why: the board now assumes unlimited agents (memo `the-board-assumes-unlimited-agents`), and the one serializer that decision leaves standing is a single working tree — unlimited analysts probing one repo collide on files no footprint names yet, and the `CONTENDING` hunk-splitting in `collect.py` exists only because one tree holds every PRD's dirt. Must not change: one commit per PRD on the transition that lands it; the orchestrator is the only committer; `plan.py` already reads `lane/` branches as work on this machine, so the branch name is fixed. Pointers: `resources/board/collect.py` (`snapshot`, `CONTENDING`, step 3), `resources/board/transitions.py` (`cmd_claim`, `cmd_sweep`), `resources/board/brief.py` (`<repo>`), `references/parts/commits.md`.

## Report

spec01: exit 0


spec02: exit 0


spec03: exit 0


spec04: exit 0


spec05: exit 0
