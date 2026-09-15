---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1h"
description: "the WorktreeCreate hook opens an isolated agent's lane as directory `agent-<id>` with branch `worktree-agent-<id>`, and `lane-rm` assumes the two spellings are one, so it dies on `fatal: Not a valid object name` and no agent lane can ever be closed by name"
---

# lane-rm cannot address an agent worktree

`lane` (`justfile:243-247`) creates the branch and the directory under one
name, and `lane-rm` (`justfile:270-273`) spends that name three times — as a
commit-ish for `git merge-base --is-ancestor`, as a path under
`.claude/worktrees/`, and as a branch for `git branch -d`. The `WorktreeCreate`
hook that gives an isolated agent its lane does not follow that rule:

```
.claude/worktrees/agent-a1428197a9059983d   d5319c10 [worktree-agent-a1428197a9059983d]
.claude/worktrees/agent-a85691e7482ae3921   6c202439 [worktree-agent-a85691e7482ae3921]
```

So `lane-rm agent-a1428197a9059983d` fails on its first line with
`fatal: Not a valid object name`, and `lane-rm worktree-agent-a1428197a9059983d`
would fail on its second, at a path that does not exist. Measured 2026-09-08 by
[landed-lanes-are-never-closed](../landed-lanes-are-never-closed/prd.md), which left both worktrees standing for this
reason. They are also dirty and would have been refused anyway, so nothing was
lost — but no agent lane can be closed by name at all, and the hook opens one
per isolated agent.

## Do

Resolve the branch from the worktree instead of assuming it: `lane-rm` reads
the checked-out branch with `git -C .claude/worktrees/{{name}} rev-parse
--abbrev-ref HEAD` and uses that for the ancestry test and the delete, keeping
the path as the one name the caller gives. That covers both spellings without
teaching the recipe the hook's prefix.

## Acceptance
`just lane-rm agent-<id>` on a clean agent worktree whose HEAD is an ancestor of
`main` removes the worktree and deletes `worktree-agent-<id>`; `just lane-rm
<name>` on an ordinary lane still behaves exactly as before; a dirty worktree of
either shape is still refused. `just memos-check` green.

Landed 2026-09-08: `lane-rm` is a bash recipe that reads the branch with
`git -C .claude/worktrees/{{name}} rev-parse --abbrev-ref HEAD` and spends it on
the ancestry test and the delete, keeping the caller's name as the path only
(`justfile:270-276`). Checked on throwaway worktrees of both shapes: an
agent-shaped `agent-<id>`/`worktree-agent-<id>` pair closes, an ordinary lane
still closes, and a dirty or unlanded worktree of either shape is still refused.
