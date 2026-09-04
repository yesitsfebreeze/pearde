---
state: superseded
origin: derived
from: the-board-is-a-real-directory-at-pearde-never-a-symlink
priority: 70
complexity: 0
blast-radius:
---

# two board aliases for one directory fan a run out twice

The user did not ask for this. It was measured on 2026-09-03 at 09:16, when
`/pearde run the-board-is-a-real-directory-at-pearde-never-a-symlink` launched
**two** identical dispatchers against one physical board — pids 47707 and
47729, both `claude --print /pearde run <same prd>` at the same second.
`pearde/.state/run-<prd>.log` records both:

    ─── pearde run 2026-09-03 09:16:15 attempt 1 · @pearde/<prd>
    ─── pearde run 2026-09-03 09:16:15 attempt 1 · @pearde-2/<prd>

**The cause.** `machine.boards()` (`resources/board/machine.py:336`) returns
`os.path.abspath(b["path"])` for every board in the daemon's watch set.
`abspath` normalises a path; it does not resolve a symlink. The daemon watches
both `/Users/feb/dev/infra/pearde/.pearde` and
`/Users/feb/dev/infra/pearde/pearde` — the first is a symlink to the second, so
they are one directory under two names. `serve.py` registered the second as
`pearde-2` because "same key, different path: suffix, never replace"
(`serve.py:558`) sees two different strings. Every fan-out over `boards()`
therefore runs the same board twice.

**Why it is not free.** Two pass workers on one board race every claim, every
lane and every `collect`. The claim ledger is the only mutex, and it does not
cover a `--force`, a second worker dispatched under the same claim id, or two
collects merging into one branch.

## Done means

- `machine.boards()` collapses two watch-set rows that resolve to one
  directory to a single row, keeping the first-registered name.
- The test is `os.path.realpath`, not string equality: a relative symlink, an
  absolute one and a `..`-laden path to the same directory are one board.
- `serve.py register` refuses, or folds, a path already watched under another
  name, instead of suffixing it — `serve.py:558`.
- A fan-out command (`pearde run`, `pearde machine`) over a machine with
  `.pearde` symlinked to `pearde` launches exactly one process per board;
  proved by the run log carrying one `attempt 1` line, not two.
- `pearde doctor` names a duplicate watch-set row.

## Related

`the-board-is-a-real-directory-at-pearde-never-a-symlink` removes the symlink
that produced this instance. It does not fix this defect: any board reached
through a symlink, on any machine, still doubles. Fix the resolution, not the
one layout that exposed it.
