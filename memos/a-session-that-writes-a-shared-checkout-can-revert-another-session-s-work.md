---
memo: a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: workers got worktrees and orchestrator sessions did not, so three sessions shared one checkout and two of them lost work in one afternoon
date: 2026-09-02
---

# a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work

`every-worker-runs-in-its-own-worktree` gave every **worker** a lane. It gave
the **session that dispatches them** nothing. So on 2026-09-02 three
orchestrator sessions — `pearde-ca`, `pearde-60`/`pearde-bf`, and a third
whose pass worker was killed mid-collect — held one working tree between
them, with no ownership, no ledger, and no lock.

Both losses that afternoon were the same shape.

**One.** `collect`'s `unland` ran `git reset --hard` in the shared checkout
and destroyed the entire uncommitted implementation of
`the-machine-is-the-run-verb` — `run.py`, `run.md`, and the `dispatch.py`,
`plan.py`, `index.md`, `README.md` and harness edits with it. Recovery was
attempted against four stashes, 113 unreachable blobs and all 2597 objects in
the store: **nothing was recoverable**. `git mv` had staged a *rename* whose
blob was byte-identical to the original, so it created no new object, and
every content edit after it was unstaged. The work looked protected in
`git status` and existed nowhere git could reach.

**Two.** After the checkout was frozen by agreement and `e5abc5b` had
replaced that `reset --hard` with `git reset --keep`, the tree was reverted
**again** — `pearde-bf`'s 22 uncommitted vault-migration files vanished from
disk while that session had run no git at all. So the fix to `unland` was
real and was not the whole cause; something else reaches the shared checkout.

Three more failures of the same root, none of which lost code but all of
which cost time: a **stale pass file** that reported a landed PRD as still in
flight and nearly caused a second session to edit a live footprint; the
**pass file overwritten twice**, once by a worker and once by `pearde-ca`,
destroying `pearde-bf`'s handover notes; and **four orphaned lane workers**
left running when their parent pass was killed.

## Decision

**A shared working tree is not a place two sessions may both write.** The
worktree rule extends up from the worker to the session:

- **One worktree per `pearde run` session.** A session that dispatches gets
  its own checkout, the way a worker gets its lane. The main checkout stops
  being a place anything runs.
- **A session ledger** records which session holds which worktree, when it
  was taken, and whether that session is still alive.
- **A new session reads the ledger first and reaps what is stale** — a
  worktree whose session is gone is removed, and one whose session is live is
  never touched.
- **No git command that discards uncommitted work may run in a tree the
  running session does not own.** `reset --hard`, `checkout --`, `clean` and
  a real `stash` are all in that set, not just the one that was found.

## Alternatives considered

**Fix `unland` and stop there** — done, as `e5abc5b`, and the tree was
reverted again afterwards. Fixing the one command that was caught leaves
every command that was not.

**A lock file on the checkout** — cheaper, and it serialises sessions instead
of letting them work at once. The whole point of the unlimited-agents
decision (`the-board-assumes-unlimited-agents`) is that work does not queue
behind staffing; a lock reintroduces exactly that at the session layer.

**Tell sessions to commit early** — advice, not a mechanism. It also cannot
work here: a session mid-implementation has nothing coherent to commit, which
is precisely the state both losses happened in.

## Consequences

- `pearde run` grows a setup step and a teardown, and the ledger is state
  that can itself go stale — the reaper is what keeps it honest, and it must
  be safe to run when another session is alive.
- Work in progress stops being visible in the main checkout's `git status`,
  which is a real loss for a person watching the repo, and the reason the
  ledger has to be readable.
- Nothing in this memo protects **uncommitted, unstaged** work inside a
  session's own worktree. That is the residual hole, and it is why the first
  loss was total: the object store is the only thing `reset` cannot reach.
