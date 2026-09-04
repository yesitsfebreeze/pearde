---
state: done
origin: requested
priority: 65
complexity: 4
blast-radius: mid
workflow: probe-then-spec
actual: 0.32h
---

# a collect closes the claim dir it measured against

The `.pearde/.claims/<rel>/` baseline that `claim` snapshots is never
removed by anything. Measured 2026-09-03: 103 claim dirs on this board,
42 MB, of which 88 `diff` files over 200 KB hold 31 MB — nearly all for
PRDs `done` for days, whose `diff`/`untracked`/`gate` record no reader will
read again. The growth is unbounded: one dir per claim ever taken, each
holding a full `git diff HEAD` of the tree at claim time, and
`collect.snapshot` only ever adds.

When this is done: `collect`, on the transition that closes a PRD out of
`claimed` — `done`, `failed`, `blocked`, any terminal the collect itself
writes — removes that PRD's claim dir after the commit lands. The baseline
has done its whole job by then: step 3 measured the worker's edits against
it, the commit is on the branch, and the only reader that ever re-reads a
baseline is a claim, which writes a fresh one (`snapshot` re-records and
already deletes a stale `.repo` side rather than inherit it). A PRD that
comes back — `retry`, `unblock`, a re-claim after `release` — snapshots
anew; nothing reads a closed PRD's baseline.

Must not change: the riders file (`.claims/riders`) and `collect.owe` —
those are live queues, not baselines; `snapshot`'s two-repo record; the
`blocked` state's meaning (a blocked PRD's dir dies only when a collect
closes it, not when it is parked — `sweep` and `release` leave it, so a
worker that re-claims finds no stale baseline lying about what was dirty).
A `--dry` collect removes nothing.

Pointers: `resources/board/collect.py` (`claims_dir`, `snapshot`,
`baseline`, the collect close path), `resources/board/transitions.py`
(`drop_lane` — the sweep's counterpart for worktrees), the
`the-lifecycle-contract-and-purge-reclaims-it` PRD, whose five leftover
classes this is not a sixth of: the dir dies at the transition that used
it, not in a later sweep.

## Report

spec01: exit 0
('done', True, 0, False) PASS
('failed', True, 1, False) PASS
('blocked', True, 1, False) PASS
('container', True, 0, False) PASS
('dry', True, 0, True) PASS
('transitions untouched', True) PASS
PASS
