---
name: pearde
description: Work the PRD board at .pearde/prds/ in the repo root as a product orchestrator — one session that scans the board, keeps PRDs specced ahead via analyst workers, dispatches implementer workers on specced PRDs, relays questions to the user, records decisions as memos, and prints progress + time-remaining on every PRD state change. Also merges several projects' boards into one master board that plans across them. Use for "/pearde", "/pearde status", "/pearde once", "/pearde run <name>", "/pearde memo <subject>", "/pearde plan", "/pearde master <path>", "/pearde view", "work the board", "run the prds", "plan the board", "plan over several projects".
---

**You are the dispatcher, not the pass.** A worked board fills a window, and a
window is billed on every turn after it. The pass therefore runs in a worker
whose window is thrown away on return, and this session keeps one line per
pass.

Read @references/parts/dispatch.md — short, the whole of your job, and the
only file you open. `/pearde`, `once`, `run <prd>` and the plain ask are that
file, start to finish:

```
Dispatch pearde-pass: "Work the board at <repo>. Resume from .pearde/.state/pass.md."
```

Two asks are answered here instead, each one call and changing nothing:

```bash
python3 @resources/pearde.py scan      # status
python3 @resources/pearde.py doctor    # is this wired
```

A memo, a drill, the view, a master board: each is its own skill, tabled in
@references/parts/handles.md. Read @README.md only for an ask about the board
itself rather than about working it.
