---
complexity: 3
footprint:
  - .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
---

# spec03 — the last harness that only forwarded an exit code now ends on a check

Census J in `the-gate-runs-the-harnesses` reads the last three lines of every
`verify.sh` on the board and demands one that carries the exit code: a bracket
test naming the failure count, `exit 1`, `exit "$fail"`, or
`exit $(( fail != 0 ))`. One harness ended on `RC=$?` / `exit $RC`, which
forwards whatever python left behind and asserts nothing, so the census counted
one short and the row went red.

Its tail now reads `fail=$RC` / `exit $(( fail != 0 ))` — the shape the census
already names, normalising any non-zero to 1.

## What the probe already established

The offender is `scan-parses-the-board-once-and-caches-it-by-mtime`, whose
harness landed with the parse-cache work at `97bf65c`. `git show HEAD:` on that
path still ends on `exit $RC`, and that tail matches none of the census's four
alternatives. **The parent report attributes this row to the graph-probe
harness instead; that attribution is wrong** — `graph-probe-makes-harness-sweep-unaffordable`'s
harness ends on `[ "$FAIL" = 0 ]`, which the census's first alternative reads,
and it has never been the one short. Nothing is owed on the graph-probe side.

The census is discriminating rather than vacuous: a bare `exit $RC` fed to the
same regex does not match, so the row can still fail on the next harness that
forgets. All 46 harnesses on the board now satisfy it.

## Acceptance

- [x] `bash .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh 2>&1 | grep -c '^  FAIL J'` reports 0, and its census note reads `46 harnesses · … · 46 end on a check that sets the exit code`
- [x] `tail -3 .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh` ends on `exit $(( fail != 0 ))`, and the harness still exits 0 on a passing run and non-zero on a failing one
- [x] section C of this PRD's harness passes: every `verify.sh` under `.pearde/prds` satisfies the census regex, the graph-probe harness's own tail satisfies it, and a synthetic `exit $RC` tail does not
- [x] `bash .pearde/prds/graph-probe-makes-harness-sweep-unaffordable/probe/verify.sh` exits 0 unchanged — nothing was edited there

## Verify and Proof

```sh
tail -3 .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
bash .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh; echo "rc=$?"
bash .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh 2>&1 | grep -E '^  (FAIL J|note census)'
bash .pearde/prds/seven-closed-probes-drifted-red/the-fixtures-meet-the-tool/probe/verify.sh
```
