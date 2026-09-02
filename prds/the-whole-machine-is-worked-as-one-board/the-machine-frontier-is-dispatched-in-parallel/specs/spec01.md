---
complexity: 13
footprint:
  - resources/board/dispatch.py
  - resources/board/machine.py
---

# spec01 — `pearde machine dispatch`, the frontier run down to nothing

`resources/board/dispatch.py` takes the frontier `machine.py` already computes
and runs it: a rolling pool of launched pass workers, `slots()` wide, each row
started the moment a slot is free and nothing in flight clashes with its
real-path footprint. `machine.py` gains one verb and loses nothing — its
default mode stays the read-only one whose harness row asserts *"it moved
nothing in this repo"*.

## What already stands

`.pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/dispatch.py`
is this file, working, and it imports the shipped `machine.py` rather than
copying it — `boards`, `slots`, `real_feet`, `frontier`, `waves`, `clash` and
`progress` are used as they landed in `fde172f`/`f986510` and no arithmetic is
re-derived. Its harness (`probe/verify.sh`) is 16 of 16, including a fixture
that builds two boards in two repos whose footprints are one inode through a
symlink and proves they never overlap, and a control with no symlink that
proves they do.

Launching goes through `serve.load_adapters` and `serve.adapter_bin` — the same
adapter set and the same `PEARDE_ADAPTER_BIN` override the view's Start button
uses — into the same log file `/run` writes, `<board>/.state/run-<rel>.log`.
Proven against the shipped `adapters/claude.json`: the binary received
`--print --dangerously-skip-permissions "/pearde run one"`.

## What is left

Move the probe to `resources/board/dispatch.py`, replacing the
`PEARDE_ROOT`-rooted `sys.path` bootstrap with the file's own directory the way
`machine.py` does it. Add the verb to `machine.py`: `dispatch` in `main`, one
line, importing `dispatch` lazily so the read path costs nothing. Nothing else
in `machine.py` changes.

## Design notes

- **Waves are the plan; the pool is the plan run.** A queued row starts on
  three conditions at once — a free machine-wide slot, its own board's
  `workers:` cap not reached, and no in-flight footprint clash. Checking the
  in-flight set rather than a precomputed wave gives the same guarantee (never
  two writers on one real path) without a barrier: wave 2's first row starts
  when wave 1's clashing row is in, not when wave 1's slowest is.
- **A board's own `workers:` is read, never written.** Fork 3 of the parent
  PRD: the machine-wide count is a dispatch-time override (`--workers`), and
  `0` on a board is unlimited, so it is read through `plan.plan_workers` and
  a falsy value means no per-board cap.
- **The order is printed before anything moves** — contract step 4 of the
  parent. `machine.text` is called first, unchanged.

## Acceptance

- [x] `resources/board/dispatch.py` exists, imports `machine`, `plan`, `serve` and `transitions` from its own directory, and defines no second copy of `clash`, `frontier`, `slots` or `progress`
- [x] `pearde machine dispatch` runs from a directory with no board above the cwd and exits 0 when nothing died
- [x] `pearde machine` with no verb still prints and moves nothing — the sibling harness stays 18 of 18
- [x] The full order, its waves and the slot reading are printed before the first launch line
- [x] `--dry` prints one `would <addr> · <prompt> in <cwd>` per row it would launch and starts no process
- [x] Two rows on different boards whose footprints `realpath` to one file never run at the same time; two rows with unrelated footprints do
- [x] A row is never started while its board already has its own `workers:` many in flight, and `workers: 0` imposes no per-board cap
- [x] `--workers N` overrides the load-derived count and says so in the reading; without it the count is `machine.slots()`
- [x] `--once` fills the pool once and returns; `--deadline S` stops filling after S seconds and names what is still in flight
- [x] Launching uses `serve.load_adapters` and `serve.adapter_bin`, honours `PEARDE_ADAPTER_BIN`, and appends to `<board>/.state/run-<rel>.log`
- [x] With two or more adapters configured and none named, it refuses with the list rather than picking one

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
set -e -o pipefail
# the probe harness, now aimed at the shipped file: 18 rows, the fixtures
# among them, and every one of them prints
bash .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel/probe/verify.sh
python3 -c "import ast; ast.parse(open('resources/board/dispatch.py').read())"
for m in "import machine as mach" "import plan as planlib" \
         "import serve as servelib" "import transitions as trans"; do
  grep -q "^$m" resources/board/dispatch.py
done
# no second copy of the read path's arithmetic
n=$({ grep -cE '^def (clash|frontier|slots|progress)\(' resources/board/dispatch.py || true; })
[ "$n" = 0 ]
# the verb is machine.py's, imported lazily
grep -q 'import dispatch as dispatchlib' resources/board/machine.py
grep -q 'argv\[0\] == "dispatch"' resources/board/machine.py
# index.py check is repo-wide: printed, and allowed to decide nothing but the
# lines that name this spec's own footprint
idx=$(python3 resources/index.py check 2>&1 || true)
[ -n "$idx" ] || idx="(index.py check printed nothing)"
printf '%s\n' "$idx"
if printf '%s\n' "$idx" | grep -qE 'resources/board/(dispatch|machine)\.py'; then
  echo "FAIL index.py check names a file this spec owns"; exit 1
fi
```
