---
title: "`refuse tree/cmd` — `reset --hard`, `checkout --`, `clean`, a real `stash`, `restore` and `switch --discard-changes` refused in any tree the running session does not own; a tree is owned when the ledger's row for it is this session's, or when it is the worktree this process is itself working in and no other live session holds it; stdlib only and imports nothing from the planner, so @resources/guard.py can call it on every Bash tool call"
type: fileindex
path: resources/board/refuse.py
kind: resource
area: board
ext: py
keywords: [own]
present: true
---

# resources/board/refuse.py

`refuse tree/cmd` — `reset --hard`, `checkout --`, `clean`, a real `stash`, `restore` and `switch --discard-changes` refused in any tree the running session does not own; a tree is owned when the ledger's row for it is this session's, or when it is the worktree this process is itself working in and no other live session holds it; stdlib only and imports nothing from the planner, so @resources/guard.py can call it on every Bash tool call

→ `resources/board/refuse.py` — not a note; Dataview cannot read it, which is why this page exists.

## Keywords

- `@@own` — which tree a session holds, and what may be run in one it does not

## Same scope — `@@own`

- [[.pearde/wiki/index/resources-board-collect-py|resources/board/collect.py]]
- [[.pearde/wiki/index/resources-board-lanes-py|resources/board/lanes.py]]
- [[.pearde/wiki/index/resources-board-session-py|resources/board/session.py]]
- [[.pearde/wiki/index/resources-guard-py|resources/guard.py]]
