---
complexity: 8
footprint:
  - .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
---

# spec01 — the parse-cache harness counts work, not milliseconds

The cache harness ended in a stopwatch: `warm < cold` and `warm < 40 ms`,
measured with `time.perf_counter` inside a sweep that runs four harnesses at
once. What the cache actually promises is not a duration — it is that a warm
parse opens no file. This unit is that assertion, and the removal of every
clock from the file.

## What stands from the probe

The rewrite is in the tree, uncommitted, and green. The stopwatch block at the
end of
`.pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh`
is replaced by a Python block that wraps `builtins.open`, walks the fixture
board three times, and reports integers:

```
ok   a cold walk reads every file once (14)
ok   a warm walk reads nothing (0)
ok   one changed mtime costs exactly one re-read (1)
ok   the check can fail: without the cache the walk reads every file (14)
```

The last line is the tripwire: it runs the same walk through
`plan._parse_prd_uncached`, so a run in which the counter is broken and every
count comes back zero fails on its own account.

The fixture board is the one the file already builds in a tempdir, so the
numbers do not move when the real board grows, and the real board is never
written to.

**The measurement that justifies it.** Six runs of the old file under 64
spinners, on an unchanged tree, on 2026-09-02: two red. `FAIL: warm walk+parse
54.2 ms above the 40 ms bar` on a run whose cold/warm pair was 161.9 ms ->
54.2 ms — a cache doing its job, on a busy box. Idle, the same file reads 11.5
ms -> 5.3 ms.

**The flip.**
`.pearde/prds/two-self-tests-fail-on-timing-not-on-code/probe/flip-scan.sh`
builds three trees from `git archive HEAD`, drops the same harness into each,
and runs it:

| tree | what is broken in `plan.py` | harness |
|---|---|---|
| `good` | nothing | exit 0 |
| `never` | `e = _PCACHE.get(apath)` -> `e = None`, so the store never hits | exit 1, warm walk reads 14 |
| `stale` | `e.get("mtime") == st.st_mtime_ns` -> `True`, so mtime is ignored | exit 1, the changed file is served stale |

## What is left

Run the two commands below and read the counts. Nothing to write unless a
count moved — and a moved count is a change in `plan.py`, which is what this
harness now says.

## Acceptance

- [x] `bash .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh` exits 0 and prints `ok   a warm walk reads nothing (0)`
- [x] the same file holds no wall-clock assertion — no `perf_counter`, no `ms above the`, no `warm >= cold`
- [x] `bash .pearde/prds/two-self-tests-fail-on-timing-not-on-code/probe/flip-scan.sh` exits 0: green on `good`, red on `never` and on `stale`
- [x] the harness leaves the real board unwritten — its whole fixture is under `mktemp -d`, and `git status --porcelain .pearde` is unchanged across a run

## Verify and Proof

```sh
H=.pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
OUT="$(bash "$H")"
printf '%s\n' "$OUT"
bash .pearde/prds/two-self-tests-fail-on-timing-not-on-code/probe/flip-scan.sh
CLOCK="$( { grep -cE 'perf_counter|ms above the|warm >= cold' "$H" || true; } )"
[ "$CLOCK" = 0 ] && [ -n "$(printf '%s\n' "$OUT" | grep '^ok   a warm walk reads nothing (0)$')" ]
```
