---
complexity: 9
footprint:
  - resources/board/dispatch.py
---

# spec01 — one dispatcher per physical board, and the refusal says whose

`pearde run` takes an advisory `flock` on `<board>/.state/run.lock` for every
distinct physical board it is about to move, before it reads or prints
anything, and releases it however the process ends. A second dispatcher on a
board already held refuses with the holder's pid and prints no order it is not
going to work.

**What already stands** (committed on the lane, all six probe claims green as
of the second analyst pass 2026-09-03 21:34):
`Held`, `BoardLock`, `lock_boards` and the `try/finally` around the pool in
`main`. `flock` and not a pidfile, so nothing is ever stale to reap; the lock
file lives inside the board, so it is realpath-keyed by construction — one
physical directory has one `.state/` however it was spelled. `lock_boards`
dedupes `entries` by realpath so a caller handing one tree twice cannot
deadlock against itself, and refuses one board by name while still taking the
rest, so `pearde run all` moves every board that is free. All three "left"
items below are DONE and measured: the parser is built once in `main` and
`_dispatch_main(a, …)` takes the namespace; the empty-entry-set case was a
real bug in the standing code — the held-board filter ran before the empty
check and turned "everything held" into an empty set answered with rc 0 and a
0-board order (probe claim C rc=0) — and is fixed by testing `not locks and
entries` before the filter; the refusal names the physical board
unconditionally.

**What is left**: nothing in this spec. Verify the boxes against the lane and
return DONE.

## Acceptance

- [x] `dispatch.main` builds the argument parser exactly once; `grep -c "ArgumentParser" resources/board/dispatch.py` is `1` — measured `1`
- [x] `dispatch.main([], entries=[])` prints something and does not exit 1 in silence — probe claim F: `rc=0`, printed the empty frontier (`0 of 0 board(s) … dispatched 0 · refused 0 · dead 0`)
- [x] `dispatch.main` still takes the lock before `runlib.frontier` is called, and releases every lock in a `finally` — read: `lock_boards(entries)` at `main()` precedes `_dispatch_main` (which calls `runlib.frontier`), and `for lk in locks: lk.release()` sits in the `finally`
- [x] A second `pearde run` on a board already being dispatched exits non-zero, says `already being dispatched`, names the first dispatcher's pid, and prints no `would ` line and no `dispatched N` line — probe claim C: `rc=1`, `is already being dispatched by pid 77037`, no order printed
- [x] The refusal names the physical board — `one physical board at <realpath>` — whether or not the two callers spelled it differently — probe claim E: refusal carries `— one physical board at …/proj/pearde`
- [x] A `pearde run` started after the first dispatcher exits is taken, not refused: the kernel dropped the lock, and nothing reaps a stale pid — probe claim D: `dispatched 1 · refused 0 · dead 0`
- [x] One board of several being held does not stop the rest: the held board is named on stderr, added to `skipped`, and the others are still dispatched — direct check: `d.main(["--dry"], entries=[("b1",b1),("b2",b2)])` with b1 held → `rc=0`, stderr `b1 — … is already being dispatched by pid 47496`, stdout `skipped b1 — already being dispatched`, b2 on the frontier
- [x] `python3 resources/index.py check` prints no line naming `dispatch.py` (its four pre-existing lines about `common.py`, `hotreload-test.js` and `commits.md` are not this spec's) — grep over the gate's output is empty

## Verify and Proof

```sh
cd "$PEARDE_LANE"
python3 -c "import ast,sys; ast.parse(open('resources/board/dispatch.py').read())"
test "$(grep -c 'ArgumentParser' resources/board/dispatch.py)" = 1
python3 .pearde/prds/no-work-is-lost-on-the-board/the-board-locks-by-realpath/probe/probe.py --skill "$PWD"
python3 resources/memos.py verify
python3 resources/index.py check 2>&1 | grep dispatch.py && exit 1 || true
```
