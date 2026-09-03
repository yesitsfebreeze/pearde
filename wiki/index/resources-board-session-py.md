---
title: "`session take/list/reap/land/owns` — one git worktree per RUN SESSION, the layer above lanes, and the module every board command asks before it names a code repo: `instead_of` answers the session's tree, or the repo it was handed when no session holds one, so `collect.repo_of` and `plan.prd_repo` both end here. `<board>/.sessions/<id>` on `session/<id>`, a ledger at `<board>/.state/sessions.json` keyed on pid and start time, a reaper that commits everything a dead session left (untracked included) to `refs/pearde/reaped/<id>` before it removes the tree — alive and unknown are both never reaped — and `land`, rebase then fast-forward, putting the session's commits on the branch the checkout is on"
type: fileindex
path: resources/board/session.py
kind: resource
area: board
ext: py
keywords: [handles, own]
present: true
---

# resources/board/session.py

`session take/list/reap/land/owns` — one git worktree per RUN SESSION, the layer above lanes, and the module every board command asks before it names a code repo: `instead_of` answers the session's tree, or the repo it was handed when no session holds one, so `collect.repo_of` and `plan.prd_repo` both end here. `<board>/.sessions/<id>` on `session/<id>`, a ledger at `<board>/.state/sessions.json` keyed on pid and start time, a reaper that commits everything a dead session left (untracked included) to `refs/pearde/reaped/<id>` before it removes the tree — alive and unknown are both never reaped — and `land`, rebase then fast-forward, putting the session's commits on the branch the checkout is on

→ `resources/board/session.py` — not a note; Dataview cannot read it, which is why this page exists.

## Keywords

- `@@handles` — every command the board answers to
- `@@own` — which tree a session holds, and what may be run in one it does not

## Same scope — `@@handles`

- [[.pearde/wiki/index/references-drill-md|references/drill.md]]
- [[.pearde/wiki/index/references-parts-handles-md|references/parts/handles.md]]
- [[.pearde/wiki/index/references-parts-loop-md|references/parts/loop.md]]
- [[.pearde/wiki/index/resources-board-brief-py|resources/board/brief.py]]
- [[.pearde/wiki/index/resources-board-orphans-py|resources/board/orphans.py]]
- [[.pearde/wiki/index/resources-board-transitions-py|resources/board/transitions.py]]
- [[.pearde/wiki/index/resources-pearde-py|resources/pearde.py]]

## Same scope — `@@own`

- [[.pearde/wiki/index/resources-board-collect-py|resources/board/collect.py]]
- [[.pearde/wiki/index/resources-board-lanes-py|resources/board/lanes.py]]
- [[.pearde/wiki/index/resources-board-refuse-py|resources/board/refuse.py]]
- [[.pearde/wiki/index/resources-guard-py|resources/guard.py]]
