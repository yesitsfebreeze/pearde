---
state: done
origin: requested
priority: 90
blast-radius: high
complexity: 0
actual: 22.17h
commit: 4e311b8
---

# every run session works in a worktree of its own

The worktree rule extends up from the worker to the session that dispatches
it. A `pearde run` session takes a checkout of its own; a ledger records who
holds what; a new session reads that ledger first and reaps what is stale.
The main checkout stops being a place anything runs.

Why, in full, with both losses and the three near-misses:
`pearde/memos/a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work.md`.
Do not re-derive the reasoning — it is settled. This PRD is the mechanism.

## The user's words, 2026-09-02

*"record the gap and fix it. we need to have one worktree per `pearde run`
session i think. then when we start a new session we check the session ledger
and clean up stale worktrees. we can also use worktrunk for that. if you look
in pi we have a lot of neat tools there"*

## The contract

| part | what it must do |
|---|---|
| **take** | a `pearde run` session gets a worktree of its own before it dispatches anything. The main checkout is never where a session works |
| **ledger** | which session holds which worktree, when it was taken, and how to tell whether that session is still alive |
| **reap** | a new session reads the ledger first and removes worktrees whose session is gone. A worktree whose session is **live** is never touched |
| **refuse** | no command that discards uncommitted work runs in a tree the running session does not own — `reset --hard`, `checkout --`, `clean`, and a real `stash`, not only the one that was caught |

## Forks the drill must settle — every one needs the user

1. **`worktrunk`, and the rest of `pi`.** The user named `worktrunk` as a
   candidate for this and said `pi` holds a lot of neat tools. **Survey it
   before designing anything** — this PRD must not reinvent a tool that is
   already on the machine and already trusted. Report what `worktrunk` does,
   whether it owns the ledger and the reaping or only the worktree, and what
   else in `pi` is relevant. This is the first job, ahead of any code.
2. **Where the ledger lives.** A machine-local file, the board, or `git
   worktree list` read as the ledger itself. Note the standing invariant this
   repo keeps: *the watch set is the whole configuration* and no registry of
   boards is written (`references/parts/run.md`). A session ledger is a
   registry — so either it is genuinely different in kind, or that invariant
   moves, and which one is the user's call.
3. **How liveness is decided.** A pid, a socket under `/tmp/cc-socks/`, a
   heartbeat, or a TTL like `claim-ttl`. Reaping a worktree whose session is
   merely idle would destroy exactly the work this PRD exists to protect, so
   the false-positive cost is total and the test must be conservative.
4. **What happens to uncommitted work at reap time.** `git stash create` +
   `stash store` before removal puts it in the object store where `reset`
   cannot reach it — that is the one mechanism that would have saved either
   loss. Decide whether reaping snapshots unconditionally.
5. **How a session's work gets back to main.** Merge per session the way
   `collect` merges a lane, or leave it to the person. Interacts with one
   commit per PRD on the transition that lands it.

## What must not change

- **One commit per PRD, on the transition that lands it**, and the
  orchestrator is the only committer (`references/parts/commits.md`).
- **`pearde <cmd>` stays the whole shell surface** (`references/install.md`).
- **Lanes keep working as they are.** `resources/board/lanes.py` gives each
  worker its worktree under the board; this PRD is the layer above it and
  must not fold the two together without saying so.
- **The reaper must be safe to run while other sessions are alive.** It is
  the one part that deletes, and it runs at every session start.

## Verify

Two sessions, started in either order, each holding uncommitted edits to the
same file: neither can revert the other's tree, and a `collect` in one leaves
the other's working tree byte-identical. Then kill one without cleanup and
start a third: the dead session's worktree is reaped, its uncommitted work is
in the object store, and the live session's worktree is untouched.

## Children

| child | contract | needs |
|---|---|---|
| `a-session-ledger-names-who-holds-what-and-reaps-what-is-gone` | pearde session take/list/reap/owns` stands: every run session gets a worktree of its own under the board, a ledger names who holds which and how to tell it is alive, and a reaper removes a dead session's tree only after stashing everything it left, untracked files included | — |
| `board-commands-run-in-the-session-s-tree-not-the-checkout` | every board command resolves the running session's worktree as the code repo instead of the board's parent, and a session's commits reach the branch a person reads | a-session-ledger-names-who-holds-what-and-reaps-what-is-gone |
| `no-destructive-git-runs-in-a-tree-the-session-does-not-own` | reset --hard`, `checkout --`, `clean` and a real `stash` are refused in any tree the running session does not own — in the board's own code and in a session's own shell | a-session-ledger-names-who-holds-what-and-reaps-what-is-gone |

## Report

container: every child done — pearde collect closes it

children: every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone, every-run-session-works-in-a-worktree-of-its-own/board-commands-run-in-the-session-s-tree-not-the-checkout, every-run-session-works-in-a-worktree-of-its-own/no-destructive-git-runs-in-a-tree-the-session-does-not-own
