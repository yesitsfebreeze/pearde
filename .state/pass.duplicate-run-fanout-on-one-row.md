# pass · four dispatchers raced one row, 2026-09-03 11:56-11:59

Kept under its own name so a `pass.md` rewrite by any of the racing siblings
cannot clobber it. This is the acceptance case of
`no-work-is-lost-on-the-board/the-board-locks-by-realpath` firing in
production, against a board where that PRD's mechanism is written but **not
landed** — it sits uncommitted in the lane as `resources/board/dispatch.py`
and `resources/board/serve.py`.

## What happened

`.state/run-no-work-is-lost-on-the-board_the-board-locks-by-realpath.log`
holds **four** `pearde run … attempt 1` lines for the *same* PRD inside 46
seconds: 11:56:40, 11:56:43, 11:57:15, 11:57:26. Nothing refused any of them.

Each spawned a pass worker with a byte-identical prompt:

```
Work the board at /Users/feb/dev/infra/pearde.
Resume from .pearde/.state/pass.md.
Scope: no-work-is-lost-on-the-board/the-board-locks-by-realpath.
```

Four parent session uuids carry that prompt — `e061fba4` (09:56:49Z),
`7ede1630` (09:56:53Z), `0474dcda` (09:57:20Z), `72816902` (09:57:34Z) — and
`ps` showed three `claude --print … /pearde run <same row>` processes still
running at 11:59, beside the interactive orchestrator `s9856` (pid 9856, up
51m), which is alive and still collecting its own 11:43 batch.

Four sessions were taken for one row: `s89740`, `s90646`, `s7022`, plus
`s9856`. Four worktrees, four branches, one board.

## Why nothing stopped it

These are not two *spellings* of one path — they are the same spelling four
times. The PRD's contract covers it anyway: identity by `os.path.realpath`,
and *the second registration of a path whose realpath is already held names
the first holder and refuses*. There is no lock on this board yet, so the
second, third and fourth registrations all took.

`serve.json` is written per registration; a claim records only
`claim: <name> <timestamp>` in the PRD frontmatter and **names no process**,
so no sibling can tell a live claim from an orphan one — that is the separate
row `the-board-reclaims-dead-work-by-itself/a-claim-names-the-process-that-holds-it`,
and it is what makes this race silent instead of loud.

## What kept it from becoming lost work, this once

Session `7ede1630` won the claim at 11:57 and dispatched the one implementer,
`agent-ae6439a54de4db4d6`, on `--worker impl-lock-realpath`. Verified alive at
11:59:36: 89 lines, growing, zero
`grep -acE '"(text|content)":"(API Error|Claude AI usage limit reached)'`.

The three losing pass workers each have to decide not to dispatch a second
implementer. `pearde claim` refuses a held claim — but **a worker whose own
claim name matches briefs itself without refusal**, and `impl-lock-realpath`
is the name every one of them would reach for. The guard against two
implementers on one lane worktree is currently four independent windows each
choosing to stand down. This pass (`s7022`) stood down.

## The two writers nobody arbitrates

- **`.state/pass.md`** — every pass worker is told to rewrite it *whole* at
  every transition. Four of them on one board is last-writer-wins over the
  board's only memory.
- **the lane** `.lanes/no-work-is-lost-on-the-board-the-board-locks-by-realpath`
  — one worktree, one branch, and any second implementer writes into it under
  the first.

## What a person has to settle

Kill the duplicate `pearde run` processes, leave `s9856` and the one live
implementer. Then land the realpath lock, because until it is committed every
`pearde run` on this machine can fan out again — and the row that fixes it is
the row that was fanned out.

## The winner died too, at 12:00:16

The stand-down above was correct and still cost the row its worker.
`agent-ae6439a54de4db4d6` grew to 116 lines and stopped at **12:00:16** —
the moment its dispatcher exited. Two minutes later it had not moved, while
five of `s9856`'s workers wrote at 11:59:54, 12:01:56, 12:02:12 and 12:02:27.
A frozen transcript beside live controls is the measurement; `ps` on the
`claude --print … /pearde run` processes is what named the cause.

That is the top rule of `pass.md` — *a worker dies with the window that holds
it* — measured a third time, and the first time the killing window was a
**duplicate dispatcher exiting normally** rather than a return or a Ctrl+C.
The fan-out does not merely waste windows: the loser windows exit, and if one
of them owns the claim, its worker goes with it.

## It is not one row

At 12:02, `ps` showed `pearde run` dispatchers live on four different rows,
and **two of them on the same row** — `copy-lint-ledger-drift/pattern-6`,
pids 16406 and 93146, five and a half minutes apart. The fan-out is board-wide
and reproducing on its own.

## What this window did

- Committed the orphaned lane work as `6560ab9` — 176 insertions across
  `resources/board/dispatch.py` and `resources/board/serve.py`, the realpath
  lock as the analyst's build left it. It had been sitting uncommitted since
  the probe-then-spec build, one `sweep --apply` from being dropped.
- Re-dispatched `impl-lock-realpath` once, on Opus, against the orphaned
  claim, and held the turn on it.

## The measurement worth keeping

`claim: <name> <timestamp>` names no process, so an orphaned claim and a live
one are indistinguishable from the outside. Every check that mattered here had
to be made against transcript mtime and `ps` — outside the board entirely.
Until a claim names its holder, the board cannot tell a working row from a
dead one, and each of four windows has to re-derive it by hand.

## A sibling already handed back BLOCKED on this row

`.state/run-no-work-is-lost-on-the-board_the-board-locks-by-realpath.log`
ends with another of the four windows returning `BLOCKED` and *"Stopping. No
dispatch until both settled."* It asked a person for two calls: kill three of
the four duplicate processes, and decide whether `pearde run` may dispatch per
row with no lock. Its own note: *"that decision is what this PRD builds —
irony noted, it raced itself."*

Its read was one step stale — it believed **two** implementers shared the
claim and the lane. They never overlapped: the first was already dead when
this window checked, and the lane was clean. Two of the four dispatchers have
since exited on their own, so its call 1 has mostly settled itself; only
`s7022` is left on this row, with one live implementer under it.

That is worth keeping as its own lesson: **four windows reading one board
produce four partly-wrong accounts of it**, each true at the second it was
taken. The board has no way to reconcile them, and `pass.md` — the one file
that would — is the file they all overwrite.

## It is still spreading

At 12:05, `ps` showed **four** `pearde run` dispatchers on
`the-board-is-a-real-directory-at-pearde-never-a-symlink/init-and-upgrade-write-the-dotted-board`
(its own log carries four `attempt 1` headers, the last at 12:03:37), beside
single dispatchers on `api-docs-link-dead`, `big/second` and
`every-board-path-citation-resolves-on-a-fresh-clone`. Whatever is invoking
`pearde run` is doing it several times per row, and moved on to a new row
after this one.

## And the account has a ceiling

`.state/run-the-session-rebase-rollback-asks-refuse-before-it-resets.log` ends
`You've hit your session limit · resets 1:50pm (Europe/Berlin)`. Some of the
quiet windows above did not stand down or die — they were never served. Any
count of "live workers" taken this hour is a floor, not a total.
