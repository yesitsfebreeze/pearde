---
complexity: 8
footprint:
  - resources/board/serve.py
---

# spec01 — `.state/ask.md` bumps the board like any other write

The daemon's `digest()` walk excludes every directory starting with `.`
(`dirs[:] = [d for d in dirs if not d.startswith(".")]`), so `.state/ask.md`
— the file a fork lands in — was never part of what "changed" means to the
watch loop. A fork written mid-pass sat unseen by every `/wait` long-poller
(`pearde view wait`, and the board page's own live-reload) until some
unrelated tracked `.md` file happened to change, which in practice meant the
pass's own return line, minutes to tens of minutes later. This is already
built and verified: `ask_digest(path)` stats `<board>/.state/ask.md`
independently of `digest()`, `Board.ask_stamp` holds its last value, and the
watch loop's per-tick check (`resources/board/serve.py`, inside `watch()`,
run for every board on every tick regardless of which of the other branches
fired) calls `bump(b)` the moment that stamp moves — the same primitive
`lane_digest` already rides for a landed lane, not a fresh `mirror()`. No
new CLI, no hold timer, no batching logic: `POLL_S = 1.0`'s existing
one-second sweep is the whole wake, per the PRD's own answer.

Verified directly: the existing `probe/p1-signal.sh` flips "ask.md written"
from `quiet` to `BUMP`, and a live `/wait?board=...&seq=...` call issued
before the write returns within ~2s of `.state/ask.md` being written (the
one-second poll plus its own settle), not at any pass boundary. `pearde
view wait` — the dispatcher's own park after `DRAINED`, `references/parts/
dispatch.md` line 44 — reads this same `/wait` and needs no change to pick
the wake up.

## Acceptance

- [x] `ask_digest(path)` exists in `resources/board/serve.py`, stats
      `<board>/.state/ask.md` and returns `None` when the file is absent
      (mirrors `lane_digest`'s `OSError` handling — a missing file is not
      an error state). `grep -n 'def ask_digest' resources/board/serve.py`
      → `442:def ask_digest(path):`; its body is
      `p = os.path.join(path, planlib.STATE_DIR, "ask.md")` then
      `try: return os.stat(p).st_mtime_ns / except OSError: return None`.
- [x] `Board.__init__` holds `self.ask_stamp` alongside `self.digest` and
      `self.refs`. Line 295, immediately under
      `self.digest = None       # of the .md files — what "changed" means`.
- [x] `watch()`'s per-board loop checks `ask_digest(b.path)` against
      `b.ask_stamp` on every tick — independent of whether the `digest()` or
      `plan_digest()` branches fired that tick — and calls `bump(b)`, never
      `mirror(b)`, when it moved. Lines 796-803: the block sits at the body
      indent of `for b in boards():`, after the `if / elif / else` chain
      closes, and its only call is `bump(b)`.
- [x] `probe/p1-signal.sh`, run against this tree, prints `BUMP` (not
      `quiet`) for the `ask.md written` step:
      `ask.md written             3 -> 4   BUMP`, with all three
      `control (nothing)` rows `quiet` and `## Questions in prd.md`
      still `4 -> 5   BUMP` — the path `digest()` already watched did not
      regress.
- [x] A direct `/wait?board=<name>&seq=<n>` call parked before `.state/
      ask.md` is written returns within a few seconds of the write, not
      after a `.md` file `digest()` already tracked changes. Parked at
      seq 3, the file written at t+2.0s, the call returned at **2.18s**
      with `{"seq": 4, ...}` — `## Manual /wait check` in `report.md`.

## Verify and Proof

```sh
python3 -m py_compile resources/board/serve.py
out=$(bash .pearde/prds/the-board-reclaims-dead-work-by-itself/a-fork-reaches-the-user-when-it-is-written/probe/p1-signal.sh 2>&1)
printf '%s\n' "$out"
printf '%s\n' "$out" | grep -qE '^ask\.md written +[0-9]+ -> [0-9]+ +BUMP$'
[ "$(printf '%s\n' "$out" | grep -cE '^control \(nothing\) +[0-9]+ -> [0-9]+ +quiet$')" = 3 ]
```

The block now asserts rather than prints: the earlier version ran the probe
and took its exit, which is the exit of a `serve.py forget` that succeeds
whatever the rows said, so no row could redden it. It also no longer needs
`SKILL=` passed in — the probe's default named a lane that was never cut,
and now walks up from its own directory to the checkout holding
`resources/pearde.py`.

Run on this tree, collect-style
(`bash -e -o pipefail`): exit **0**, rows
`control (nothing) 3 -> 3 quiet`, `ask.md written 3 -> 4 BUMP`,
`control (nothing) 4 -> 4 quiet`, `## Questions in prd.md 4 -> 5 BUMP`,
`control (nothing) 5 -> 5 quiet`. The block is known to fail on a tree
without this change, measured rather than argued: the checkout was reverted
under this run by a neighbouring session (`## The tree was wiped mid-run` in
`report.md`), the same probe printed `ask.md written 3 -> 3 quiet`, and the
`grep -qE` above has no line to match there. A direct `/wait` call, parked
before the write, returned in 2.18s in this run — logged in the report under
`## Manual /wait check`.
