---
name: pearde
description: Work the PRD board at prds/ in the repo root as a product orchestrator — one session that scans the board, keeps PRDs specced ahead via analyst workers, dispatches implementer workers on specced PRDs, relays questions to the user, records decisions as memos, and prints progress + time-remaining on every PRD state change. Also merges several projects' boards into one master board that plans across them. Use for "/pearde", "/pearde status", "/pearde once", "/pearde run <name>", "/pearde memo <subject>", "/pearde plan", "/pearde master <path>", "/pearde view", "work the board", "run the prds", "plan the board", "plan over several projects".
---

**You are the dispatcher, not the pass.** Working the board fills a window,
and a window is billed on every turn that follows it. So the pass runs in a
worker whose window is thrown away when it returns, and this session keeps one
line per pass.

Read @references/parts/dispatch.md — it is short, it is the whole of your job,
and it is the only file you open.

Working the board — `/pearde`, `once`, `run <prd>`, or the plain ask — is
that file, start to finish:

```
Dispatch pearde-pass: "Work the board at <repo>. Resume from .pearde/.state/pass.md."
```

Two things are answered here instead, because each is one call and changes
nothing:

```bash
python3 @resources/pearde.py scan      # status
python3 @resources/pearde.py doctor    # is this wired
```

Everything else — a memo, a drill, the view, a master board — is its own
skill, and @references/parts/handles.md is the table. Read @README.md only
when the ask is about the board itself rather than about working it.
