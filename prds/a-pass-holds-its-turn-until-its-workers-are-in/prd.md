---
state: claimed
origin: derived
from: the-board-is-a-real-directory-at-pearde-never-a-symlink
priority: 90
complexity: 11
blast-radius: mid
workflow: probe-then-spec
claim: impl-nova2-a-pass-holds 2026-09-03 21:40
---


# a pass holds its turn until its workers are in

`references/parts/loop.md` and `references/parts/dispatch.md` never say that a background worker does not outlive the pass window that dispatched it. Only `references/parts/workers.md` says anything nearby, and it says something weaker — check the worker is alive *before the turn ends*. A pass can pass that check, hand back `MORE`, and kill every worker it just verified.

**Measured 2026-09-03.** The pass that ended 09:59 dispatched six workers in its last turn and returned. Their subagent transcripts under `~/.claude/projects/<slug>/<uuid>/subagents/` stop between 10:02 and 10:10, hold no `API Error`, and no process of theirs survived; five wrote no specs. Seventy-five minutes and five analysts bought nothing. The next pass found five PRDs `analyzing` over empty `specs/` directories and had to sweep and re-dispatch every one, and `sweep --apply` dropped 44 uncommitted paths across their four lanes — whatever they had built before they died.

The consequence for requested work is direct: every PRD dispatched in a pass's final turn is burned, and the board reads the corpse as live work for a full `claim-ttl` before anything notices. The four PRDs under `the-board-is-a-real-directory-at-pearde-never-a-symlink` — the container the user asked for by name — were the ones burned.

What must not change: the liveness check itself, and the ceiling handover. A pass that has genuinely reached `context-budget` still hands back `MORE`; the rule is about workers it dispatched and did not wait for, not about how long a window may live.

## Done means

- [ ] `references/parts/loop.md` states that a pass holds its turn until every worker it dispatched has returned or is measurably dead, and that handing back `MORE` with workers in flight burns them.
- [ ] `references/parts/dispatch.md` says the same from the dispatcher's side: a pass worker's return ends its children.
- [ ] The verdict table names holding as the response to workers in flight, so a status line like "waiting on workers" is not reachable as a return.
- [ ] `references/parts/workers.md`'s liveness paragraph points at the hold rule rather than reading as if the check alone were sufficient.
- [ ] A harness asserts the rule appears in both `loop.md` and `dispatch.md`, and fails if either loses it.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 20:59 — claim impl-pass-holds-6476 2026-09-03 12:04, silent 8.5h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/a-pass-holds-its-turn-until-its-workers-are-in`, whose worktree this sweep removed — the branch is kept.
