---
state: open
origin: requested
priority: 80
complexity: 0
blast-radius:
---

# a lane is removed when its prd collects

Nothing removes a lane when its PRD collects, so the board leaks one git
worktree per completed PRD.

Measured 2026-09-03: `git worktree list` reports **54** worktrees on this repo
and `.pearde/.lanes/` holds **49** directories; 26 of those lanes belong to
PRDs whose state is already `done`.

`laneslib.git(repo, "worktree", "prune")` only drops registrations whose
directory has already vanished, so it never touches a lane that is merely
finished. `session.py`'s reap cleans **sessions**, not lanes. The sibling
`no-work-is-lost-on-the-board/a-conflicted-lane-is-reported-not-stranded`
covers what happens to a lane that *conflicts* — not to one that succeeded.

When this is done, a successful collect removes the lane it merged, the
registration goes with the directory, and a run of the board over many PRDs
does not grow the worktree list without bound. Removal happens only after the
merge is committed and only for a lane holding nothing uncommitted — this must
not become a second way to lose work.

Report how many of the 26 existing stale lanes the change would clean, and
whether cleaning the backlog is this PRD's job or a one-off command.
