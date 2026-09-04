# every-run-session-works-in-a-worktree-of-its-own — analyst

Verdict: REFINE

workflow: probe-then-spec · persona: engineer · lane:
`pearde/.lanes/every-run-session-works-in-a-worktree-of-its-own`

The build went through the ledger, the liveness test and the reaper — that
half stands green in a clean room and its code is uncommitted in the lane.
It then hit a layer the contract does not mention and cannot be built around
inside one PRD: **no board command takes the session's tree as the code
repo**, so a session worktree changes nothing until that resolution learns
the session. That is a second contract, and with the refuse rule it is a
third. Three children, footprints disjoint, both later ones consuming the
first.

## What the build stood up

`resources/board/sessions.py` (new, uncommitted in the lane, 260 lines):

- `whoami()` — the session's id, pid and socket from the environment.
- `alive(pid, sock)` — the conservative test, both signals or neither.
- `take(board, repo)` — a worktree at `<board>/.sessions/<id>` on
  `session/<id>`, the board sparse-excluded exactly as `lanes.create` does
  it, idempotent on the path, and a row written to the ledger.
- `rows()` / `reap(board, repo, apply)` — the ledger read back with a
  live/gone verdict per row, and the removal, which snapshots first.
- `owns(board, tree)` — the predicate the refuse rule needs.
- `snapshot(tree)` — the object-store save, at reap only.

The probe is `prds/every-run-session-works-in-a-worktree-of-its-own/probe/verify.sh`.
It builds a two-session clean room and runs the PRD's own `## Verify`:

```
1 · take       two sessions, two trees · the ledger names both · the board is
               not copied into a session tree
2 ·            each holds uncommitted work on the same file, different content
3 · owns       a session owns its own tree and neither of the other two
4 · reap       both alive — nothing touched
5 · reap       bravo killed: its tree gone, alpha's tree byte-identical, its
               row off the ledger
6 ·            the tracked edit AND the untracked file are both recoverable
verify: green
```

## Findings

### The mechanism the memo names would not have saved the loss it was written for

Measured, git 2.55: **`git stash create` silently ignores `-u`.** It returns
a sha and builds a two-parent commit from HEAD and the index; the untracked
files are not in it and no error is printed.

```
git stash create -u   → 75cd62e…, parents: HEAD, index            (2)  new.py absent
git stash push   -u   → refs/stash, parents: HEAD, index, untracked (3)  new.py present
```

`a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work`
names `git stash create` + `stash store` as "the one mechanism that would
have saved either loss". Loss one was `run.py` — a **new** file. `create`
would have returned a sha, `store` would have written a ref, the reap would
have reported a snapshot, and `run.py` would still have been gone. The
probe's first run failed on exactly this box.

The fix the build took: `git stash push -u` at reap. It mutates the working
tree, which is why it is not usable anywhere else — but at reap the tree is
removed by the next command, so the price is zero. `create` + `store` stays
as the fallback for the case `push` refuses. Box 6 is green after it.

The memo is a decision record and this analysis does not edit it. The child
that owns the reaper carries the corrected mechanism, and the correction is
worth a memo of the orchestrator's own.

### No board command resolves the session's tree

`collect.repo_of` is the only answer to "where does this PRD's code live",
and **it takes neither a cwd nor a session**. On a board that is its own
worktree — which this one is — it returns `repo_root(dirname(board))`:

```
board             /Users/feb/dev/infra/pearde/pearde
board_root==board True
repo_of resolves  /Users/feb/dev/infra/pearde      ← the main checkout, always
```

So `collect`'s merge, `lanes.create`'s base, the verify block and the gate
all run in the main checkout no matter which session invoked them. Giving a
session a worktree is inert until this changes, and changing it reaches
`collect.py`, `plan.py` and `dispatch.py` — a footprint that has nothing to
do with the ledger's. This is the split.

Downstream of it, and undecided: once a session commits on `session/<id>`,
**main never advances**. Fork 5 of the PRD is real and structural, not a
preference — it is that child's first question, and `wt step push`
("fast-forward target to current branch") is the one piece of worktrunk that
bears on it.

### The board is still one shared tree, and this PRD does not fix that

`pearde/` is itself a linked worktree of this repo, on branch `pearde`
(`git worktree list`: `.pearde  51fa0bd [pearde]`). Every session writes
`.state/pass.md`, the parse cache, `transitions.jsonl` and every `prd.md`
into that one tree. The memo records the pass file being **overwritten
twice**, destroying a session's handover notes — that failure is on the board
side, and the contract here covers the code tree only. It is a finding, not a
child: widening the contract is the user's call, not initiative.

### Fork 1 — worktrunk and pi, surveyed before anything was designed

`worktrunk` 0.72.0 is on the machine as `wt`. Read-only survey:

| asked | answer |
|---|---|
| a ledger of its own? | no — `wt list --format json` is `git worktree list` plus dirty-state and remote fields; the rest is git config and `.git/wt/logs/` |
| reaps stale worktrees? | `wt step prune` removes only worktrees **merged into the default branch**, `--min-age 1d`. Not a liveness reaper |
| a session or an owning process? | no. `wt remove --reap` kills processes whose **cwd** is under the tree — a heuristic, escaped by anything that `cd`s away |
| snapshots before removing? | **no.** `--force` deletes a dirty tree outright; background removal renames into `.git/wt/trash/` and `rm -rf`s it |
| where trees go | `{{repo_path}}/../{{repo}}.{{branch}}`, configurable in `~/.config/worktrunk/config.toml` |

In `~/dev/pi`, the two relevant files are
`packages/coding-agent/src/core/crew/presence.ts` — file-per-session
presence, 30s heartbeat, 120s stale, `peers()` unlinks what has gone quiet:
the liveness/reap primitive almost as-is — and
`packages/coding-agent/src/core/session-ledger.ts` — a JSON ledger of
`{sessionId, cwd, pid, tty, startedAt}` with upsert and trim. Neither pi nor
worktrunk ties a worktree's lifetime to a session's liveness; pi's crew
spawns into a caller-supplied cwd and never calls `git worktree`. **Nothing
on the machine hands this feature over**; the glue is pearde's to write.
Reusing `wt` for the worktree operations buys nothing `lanes.py` does not
already do, and costs a binary dependency the install does not have — so the
build used `git worktree` directly, as `lanes.py` does.

### Forks 2 and 3 closed by the build, not by asking

**Fork 3, liveness.** The environment answers it outright. Every Claude Code
session carries `CLAUDE_PID`, `CLAUDE_CODE_SESSION_ID` and
`CLAUDE_CODE_MESSAGING_SOCKET=/tmp/cc-socks/<pid>.sock`, and the socket is
unlinked when the process goes (`/tmp/cc-socks/` held six socks for six live
sessions while this ran). `alive()` requires the pid **and** the socket: a
pid alone is reused, a socket alone survives a hard kill. A grace window on
top covers a tree taken seconds ago. The probe's boxes 4 and 5 are that test
passing, and failing on purpose. No TTL, no heartbeat, no new daemon.

**Fork 2, where the ledger lives.** `<board>/.state/sessions.json`, beside
`serve.json` — machine-local, gitignored, one file per board. The standing
invariant is that no registry of **boards** is written; this is a registry of
the **sessions on one board**, written by the board it describes and read by
nobody else. Different in kind, and nothing moves. The build went through it
without a decision the user has to make.

### Defects outside this scope, not fixed

`python3 resources/index.py check` in the lane, pre-existing, before this
run's file was added:

```
references/skills/pearde-machine.md is on disk with no row in references/files.md
references/language.md references @references/personas/writer.md — not on disk
resources/board/edit.py references @questions.py — not on disk
```

`.lanes/` holds 17 worktrees, several cut off commits four ahead of HEAD and
left by sessions that are gone — the same accumulation this PRD's reaper
addresses, one layer down. Not this PRD's contract.

### Knowledge

`knowledge.py query` returned 0 hits, 0 notes on record; the gap enqueued as
`.pearde/wiki/pending/260902-5962.md`. Nothing learned here came from off this
machine except the worktrunk and pi survey, which is a fact about this machine
rather than about the world — `remember` would file a local observation as a
source. It is recorded above instead.

### Grammar

No word in the contract was undefined. One word this analysis needed and the
grammar does not hold: **session tree** — the worktree an orchestrator session
holds, as against a **lane**, the worktree a worker holds. The two need
distinguishing in every file the children touch, and the child that writes
`references/parts/sessions.md` should coin it.

## The split

Three children. `sessions.py` is one file and cannot be cut across siblings,
so the ledger, the liveness test, the reaper and `owns()` are one child — the
one that is already built. The other two are the layers that consume it, and
their footprints touch nothing of each other's.

- **the ledger child** owns `resources/board/sessions.py`,
  `references/parts/sessions.md`, `references/files.md`, `index.md`. It is
  the only child that adds a file, so it is the only one with manifest rows;
  siblings must not touch either map file.
- **the resolution child** owns `resources/board/collect.py`,
  `resources/board/plan.py`, `resources/board/dispatch.py`,
  `references/parts/loop.md`, `references/parts/dispatch.md`. It carries
  fork 5 and will very likely ask it.
- **the refuse child** owns `resources/board/lanes.py`, `resources/guard.py`,
  `references/parts/guard.md`.

The union of the three: `resources/board/sessions.py`,
`resources/board/collect.py`, `resources/board/plan.py`,
`resources/board/dispatch.py`, `resources/board/lanes.py`,
`resources/guard.py`, `references/parts/sessions.md`,
`references/parts/loop.md`, `references/parts/dispatch.md`,
`references/parts/guard.md`, `references/files.md`, `index.md`.

Why not one PRD: the ledger alone is around 15 of complexity and is done; the
resolution layer reaches four modules the ledger never opens and holds an
unanswered fork; the refuse rule is a predicate wired into a guard and every
destructive call site. Summed they are well past the board's ceiling of 40,
and the three share no file.

## Split

| child | contract | needs |
|---|---|---|
| a-session-ledger-names-who-holds-what-and-reaps-what-is-gone | `pearde session take/list/reap/owns` stands: every run session gets a worktree of its own under the board, a ledger names who holds which and how to tell it is alive, and a reaper removes a dead session's tree only after stashing everything it left, untracked files included | — |
| board-commands-run-in-the-session-s-tree-not-the-checkout | every board command resolves the running session's worktree as the code repo instead of the board's parent, and a session's commits reach the branch a person reads | a-session-ledger-names-who-holds-what-and-reaps-what-is-gone |
| no-destructive-git-runs-in-a-tree-the-session-does-not-own | `reset --hard`, `checkout --`, `clean` and a real `stash` are refused in any tree the running session does not own — in the board's own code and in a session's own shell | a-session-ledger-names-who-holds-what-and-reaps-what-is-gone |
