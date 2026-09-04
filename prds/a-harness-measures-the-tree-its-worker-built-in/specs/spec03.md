---
complexity: 6
footprint:
  - resources/doctor.sh
  - .pearde/workflows/capture-the-harness-baseline.md
  - .pearde/workflows/re-run-the-harnesses.md
  - references/parts/workers.md
---

# spec03 — the runner names the tree, and the worker is told to

Specs 01 and 02 give every harness a root it will take from whoever runs it.
This spec is the other half: something has to name one, and a worker has to
know it can.

`resources/doctor.sh` is the only runner of the set. Its sweep launches each
harness as `PEARDE_HARNESSES=1 bash "$h"` and hands it no tree at all. It now
resolves one before the launch loop and exports it per harness — honouring an
already-set `PEARDE_ROOT`, so `PEARDE_ROOT=<lane> bash resources/doctor.sh
--harnesses <board>` is how a worker measures its own lane against the
orchestrator's board of harnesses, and a plain run is unchanged.

The two atomics a worker follows when it touches harnesses — `capture-the-harness-baseline`
and `re-run-the-harnesses` — say to find the board and run what it holds, and
say nothing about which tree those harnesses will read. Each gains the line: a
worker building in a lane names its lane, or the baseline it records and the
re-run it compares against are both the orchestrator's checkout and the
comparison is empty. `references/parts/workers.md` carries the same in one
sentence, where the worker blocks already describe the lane as `<repo>`.

`capture-the-harness-baseline`'s `## Fails when` already holds a row for the
scratch-root-with-a-symlinked-`.pearde` trick. That row stays and is now
answerable: the reason to reach for the trick was that no other way existed to
point a board harness at a lane.

**Already standing (this analyst's uncommitted pass one):** the `doctor.sh`
edit is in the lane worktree, uncommitted, and both sweeps have been run
through it — see spec05. No documentation is written yet.

## Acceptance

- [x] `resources/doctor.sh` resolves the tree once before the launch loop and exports it to each harness; the launch line carries `PEARDE_ROOT="$HROOT"`.
- [x] An already-set `PEARDE_ROOT` wins: `PEARDE_ROOT=/tmp/x bash resources/doctor.sh --harnesses <board>` runs the harnesses with `PEARDE_ROOT=/tmp/x`, not with the board's repo.
- [x] With `PEARDE_ROOT` unset, the resolved value is the board's own repo — the directory `$BOARD/..` resolves to — and the sweep's failure set is unchanged from before the edit.
- [x] The job cap is untouched: `the-harness-sweep-is-capped-so-a-red-is-a-real-red` still passes, both of its `doctor.sh` matchers included.
- [x] `capture-the-harness-baseline.md` and `re-run-the-harnesses.md` each name `PEARDE_ROOT` and say a worker in a lane sets it to the lane.
- [x] `references/parts/workers.md` says the same once, and names no other new variable.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
N=0
grep -n 'PEARDE_ROOT' resources/doctor.sh                  # the resolve and the export
grep -qF 'HROOT="${PEARDE_ROOT:-' resources/doctor.sh || { echo "no already-set-wins resolve"; N=$((N+1)); }
grep -qF 'PEARDE_ROOT="$HROOT"' resources/doctor.sh || { echo "the launch line carries no root"; N=$((N+1)); }
for f in .pearde/workflows/capture-the-harness-baseline.md \
         .pearde/workflows/re-run-the-harnesses.md \
         references/parts/workers.md; do
  grep -qF 'PEARDE_ROOT' "$f" || { echo "does not name PEARDE_ROOT: $f"; N=$((N+1)); }
done
# An already-set root wins, measured rather than read: a board of one harness
# that prints the root it was handed, swept twice.
D=$(mktemp -d); trap 'rm -rf "$D"' EXIT
mkdir -p "$D/proj/.pearde/prds/one/probe"
printf 'name: rootfix\nlanguage: English\n' > "$D/proj/.pearde/settings.md"
# it exits 1 on purpose: doctor prints a harness's own last line only when the
# harness went red, and that line is the whole measurement here.
printf '#!/usr/bin/env bash\nPASS=0; FAIL=1\n[ "$((PASS + FAIL))" = 1 ]\necho "root=${PEARDE_ROOT:-<none>}"\nexit 1\n' \
  > "$D/proj/.pearde/prds/one/probe/verify.sh"
set_out=$(PEARDE_ROOT=/tmp/named-by-the-runner bash resources/doctor.sh --harnesses "$D/proj" 2>&1) || true
unset_out=$(env -u PEARDE_ROOT bash resources/doctor.sh --harnesses "$D/proj" 2>&1) || true
[ -n "$set_out" ] && [ -n "$unset_out" ]
printf '%s\n' "$set_out"   | grep -F 'root=' | tail -1
printf '%s\n' "$unset_out" | grep -F 'root=' | tail -1
printf '%s\n' "$set_out" | grep -qF 'root=/tmp/named-by-the-runner' \
  || { echo "an already-set PEARDE_ROOT did not reach the harness"; N=$((N+1)); }
printf '%s\n' "$unset_out" | grep -qF "root=$D/proj" \
  || { echo "with none set, the root is not the board's own repo"; N=$((N+1)); }
# the cap harness, captured: it is not in this spec's footprint, so it prints
# beside the block and does not decide it.
cap=$(bash .pearde/prds/the-harness-sweep-is-capped-so-a-red-is-a-real-red/probe/verify.sh </dev/null 2>&1) || true
printf '%s\n' "$cap" | tail -1
echo "spec03: $N offending"
[ "$N" = 0 ]
```
