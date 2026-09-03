---
state: open
origin: requested
priority: 65
complexity: 30
blast-radius:
needs: the-doctor-refuses-drift
---

# the daemon caches one payload per board

`serve.py` drops POST /sync, the /timeline proxy prefix, `reap`/stranded/orphan hygiene, self-restart on source change, the adapter plug-in directory (`PEARDE_ADAPTER_BIN` is the one knob) and `selfcheck`. `Board` gets `payload()/prds()/memos()/answers()/writable` and `AllBoard` implements it so no route branches on `is_all()`. `watch()` stats `plan.json` and caches members per `settings.md` mtime.

## Done means

Every GET/POST the page uses answers the same JSON; `pearde view status/stop/wait/forget` unchanged; `/board/all` loads with one scan per board.

## Needs

`one-primitive-one-definition` and `every-documented-command-exists` — both children of `the-doctor-refuses-drift`; the frontmatter `needs:` names that container, which is done exactly when both are.
