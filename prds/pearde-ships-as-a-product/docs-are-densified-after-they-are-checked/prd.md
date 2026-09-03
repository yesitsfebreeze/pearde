---
state: open
origin: requested
priority: 50
complexity: 0
blast-radius:
needs: the-second-cleanup-pass
---

# docs are densified after they are checked

The remaining dense-rewrite PRDs under `every-document-is-written-in-the-writer-s-prose` need `every-documented-command-exists` before dispatch, so prose is tightened around claims that are true.

At filing time (2026-09-03) that container had no `open` child left to carry the need: every dense-rewrite child is `done` except `templates-personas-and-agents-are-rewritten-dense`, which is `claimed` and in flight, and no command sets `needs:` on another PRD. So the need is recorded here: any dense-rewrite PRD filed or reopened under that container carries `needs: every-documented-command-exists` before it is dispatched, and this PRD is done when that holds for every open child.

## Done means

The container's open children carry that need.

## Needs

`the-second-cleanup-pass` — the container's gate.
