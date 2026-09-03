---
state: done
origin: requested
priority: 90
complexity: 38
blast-radius: mid
workflow: probe-then-spec
---

# a worker survives the window that launched it

Measured twice on 2026-09-03. Six workers died when their pass returned. Then
eighteen workers, every one verified alive and growing at 11:14, **all stopped
at 11:18:04 to the second** when the user interrupted a tool call in the pass
window. No API error in any transcript. The window's end ended every child it
held, and `sweep --apply` at 11:10 dropped 44 uncommitted paths across four
lanes — whatever they had built before they died.

The sibling `a-pass-holds-its-turn-until-its-workers-are-in` (p90, already
specced) makes the pass hold its turn, which stops a pass from dropping its own
children **on a normal return**. It does not survive a user Ctrl+C, which is
what actually happened at 11:18:04, and it cannot: holding a turn is a
discipline, not a lifetime.

The user is explicit that killing workers by hand should be survivable.

When this is done, a worker's work is recoverable after its launching window
dies — whether by detaching the worker from the window, by re-attaching it from
the session ledger, or by committing its lane continuously so a death costs the
verdict and not the build. Say in the report which of those the tree can
actually support and what each costs; the cheapest honest answer may be the
third.

**Distinct from the p90 sibling**, which this does not replace: that one keeps
a well-behaved pass from killing its own workers, this one keeps a
badly-ended one from destroying their work.

## Answers

**Q1** *(answered 2026-09-03)* — Which of the three recovery levers does the
tree support, and what does each cost?

Detaching is already built for dispatched workers — `dispatch.launch` spawns
with `start_new_session=True`, and the probe replays the window's interrupt
(SIGINT to the foreground group) to show the attached child dying while the
detached one keeps writing. It costs nothing; it is also not a lever pearde
holds over the eighteen workers that died, because those were harness
subagents of the pass window, launched by the Agent tool, and no flag pearde
can set changes how a harness reaps its own children. The session ledger
(`session.py`) reaps dead sessions by snapshotting their worktrees into
`refs/pearde/reaped/`, but lanes are not session worktrees and a swept lane
gets no snapshot — re-attach for a worker means the lane branch, and the lane
branch only holds what a commit put there. So the third lever is the honest
one, and it was already half-built: `lanes.commit_all` existed with zero
callers. The build wired it into all three edges pearde owns — the sweep
before it drops, a `pearde checkpoint <prd>` command for a pass or a person,
and the dispatcher's poll loop on a timer.

<!-- for the board: the-verdict-names-the-lever -->

## Blocked

**2026-09-03 18:34 — the lane will not rebase**

`lane/the-board-reclaims-dead-work-by-itself-a-worker-survives-the-window-that-launched-it` does not land on `session/s98669`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/the-board-reclaims-dead-work-by-itself-a-worker-survives-the-window-that-launched-it` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-board-reclaims-dead-work-by-itself/a-worker-survives-the-window-that-launched-it`.

## Report

spec01: exit 0
sweep-checkpoint: ok
checkpoint-command: ok

spec02: exit 0
dispatcher-checkpoint: ok
