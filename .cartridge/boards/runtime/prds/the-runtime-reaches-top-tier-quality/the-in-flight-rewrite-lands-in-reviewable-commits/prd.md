---
state: open
origin: requested
priority: 70
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
review-round: 2
review-status: passed
---

# The in-flight rewrite lands in reviewable commits

## Outcome

`cartridge.ctg` has one line of history that every sibling leaf diffs against. The 2026-09-14 working tree landed as `b4d553f`, but the host rewrite now runs on two diverged lines from merge base `b02b200`:

- Local `main` (`e8a4da3`) has two unpushed commits: `c9ef10b` (declared sends, per-edge tokens, outcomes, deadlines, bounded queues, yielding Lua bridge) and `e8a4da3` (trust).
- `origin/main` = `transport-design` (`ba198f4`, worktree `/Users/feb/dev/cartridge-worktrees/ws/cartridge.ctg`) has nine commits `main` lacks, including coroutine listeners (`29dbff6`) and unbounded queues in `src/transport/rpc.rs`.

Sixteen files changed on both lines. This leaf reconciles them without redesigning either.

## Acceptance

- [ ] In `cartridge.ctg`, `git rev-list --left-right --count main...origin/main` prints `0	0` and `git status --porcelain` is empty.
- [ ] Origin's listener model (`29dbff6`, `8a59b5f`, `ba198f4`) is kept. The bounded queues, declared sends, per-edge tokens, outcomes and deadlines from `c9ef10b`, and the trust from `e8a4da3`, survive. Any dropped part is named in the commit message.
- [ ] Each landed commit passes `just check runtime` and `just test runtime` (cwd `/Users/feb/dev/cartridge`). No commit mixes a rename with a behavior change.
- [ ] The porting branches under `cartridge-worktrees/ws/` build against the reconciled head, or `coordination/PORTING.md` names the new base.

## Proof and recovery

1. Probe from `cartridge.ctg`: `git log --oneline main...origin/main`, then the overlap `comm -12` of `git diff --name-only b02b200 main` and `git diff --name-only b02b200 origin/main`. Record the file list.
2. Rebase on a disposable branch: `git switch -c reconcile e8a4da3 && git rebase origin/main`. Never force-push `origin/main`.
3. If two yielding bridges cannot be merged without a design choice, keep origin's and record the question in a memo.

`main` keeps the unpushed commits until `reconcile` passes the gates. The coordinator moves the root gitlink (now `d2a761e`) afterwards.

## Review

[Review history](review.md): round 2/5 (1 inherited from the parent).
