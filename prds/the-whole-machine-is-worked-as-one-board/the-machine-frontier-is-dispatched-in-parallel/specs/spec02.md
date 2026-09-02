---
complexity: 8
footprint:
  - resources/board/dispatch.py
---

# spec02 — a launch is not a worker: the liveness test that frees the slot

A dispatcher that counts `Popen` returning counts workers that never existed.
The model gateway is what actually bounds this machine, and a 402 or a 429
arrives as a process that starts, prints an error and exits — so the slot is
given away and the row is reported as worked. This unit makes a slot cost a
*live* worker: a launch grace window, a scan of the run log, one re-dispatch,
and a named death.

## What already stands

`Job.poll` in the probe, and the two fixture cases that prove it: `dead` (a
stand-in that prints `API Error: 402 {"error":"credit balance"}` and exits 1 —
named, re-dispatched exactly once, then reported dead, and never counted as
worked) and `instant` (a stand-in that exits 0 immediately — dead, with the
reason naming the grace window). Recorded as `[[260902-b296]]`.

## What is left

Nothing but the move with spec01. `GRACE` stays env-tunable
(`PEARDE_LAUNCH_GRACE`, default 2.0) because the harness needs it short and the
real thing needs it long.

## Design notes

- **Both tests are needed, and neither alone.** A worker that dies at second 30
  passes the grace check at second 2, so the log scan is what catches it. A
  worker that logged a 429 it retried and recovered from is alive, so the log
  scan is only ever consulted on a process that has already exited. Order in
  `poll`: exited? → log matches `DEAD_PAT`? → non-zero exit? → exited 0 inside
  the grace window? → otherwise `ok`.
- **`DEAD_PAT`** covers `API Error`, `credit balance`, `insufficient quota`,
  `402`, `429`, `rate limit`, case-insensitively. This is the same test
  @references/agents/pearde-pass.md already gives the pass worker for its own
  subagents ("its transcript file must exist and hold no `API Error`"), applied
  one level up.
- **One re-dispatch, then named.** `RETRIES = 1`, matching the pass worker's
  own rule: a dead worker is re-dispatched once on the same terms; a second
  death is reported with the error text and never retried again.
- **The dead row is not silently dropped.** It ends in the `dead` list, its
  address and reason printed, and the command exits non-zero when the list is
  non-empty — a run that dispatched nothing living must not read as success.

## Acceptance

- [x] A launched process that exits with an error line matching `DEAD_PAT` is reported `DEAD <addr> · dead: <the matching line>`, and the line is quoted, not paraphrased
- [x] A launched process that exits 0 inside the grace window is dead, with a reason naming the window and the elapsed time
- [x] A launched process that exits non-zero with no matching line is dead, with its exit code
- [x] A process still running is never judged — `poll` returns `(False, None)` and the slot stays taken
- [x] A dead row is re-dispatched exactly once, and its second death is recorded in `dead` with the error text
- [x] A dead worker's slot is freed for the next queued row in the same fill, and the dead row is never counted in the dispatched total
- [x] `PEARDE_LAUNCH_GRACE` overrides the 2.0 s default
- [x] The command exits non-zero when anything is in the `dead` list

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
set -e -o pipefail
# the liveness cases, against the shipped resources/board/dispatch.py
python3 .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/fixture.py dead instant alive
# the two tests, the retry and the grace, are in the file that ships
grep -q '^GRACE = float(os.environ.get("PEARDE_LAUNCH_GRACE"' resources/board/dispatch.py
grep -q '^RETRIES = 1' resources/board/dispatch.py
grep -q 'return 1 if dead else 0' resources/board/dispatch.py
# PEARDE_LAUNCH_GRACE overrides the 2.0 s default, read at import
g=$(PEARDE_LAUNCH_GRACE=7.5 python3 -c \
  "import sys; sys.path.insert(0, 'resources/board'); import dispatch; print(dispatch.GRACE)")
[ "$g" = "7.5" ]
g=$(python3 -c "import sys; sys.path.insert(0, 'resources/board'); import dispatch; print(dispatch.GRACE)")
[ "$g" = "2.0" ]
```
