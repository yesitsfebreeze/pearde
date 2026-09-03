---
state: open
origin: requested
priority: 75
complexity: 40
blast-radius:
needs: the-second-cleanup-pass
---

# core and dev are two trees

`resources/core/` holds what a user's board runs — plan, transitions, specs, collect, brief, orphans, questions, init, serve, render, view, advisors, common, doctor, statusline, install, update. `resources/dev/` holds what only this repo uses — session, lanes, refuse, shared, machine, dispatch, ramp, scout data, the harness runner, the invariants for this machine. The install links core only; `pearde.py` forwards to both when dev exists.

## Done means

A fresh install elsewhere has no `resources/dev` path reachable, and every `pearde` command a board needs works.

## Needs

`the-second-cleanup-pass` — the container's gate.
