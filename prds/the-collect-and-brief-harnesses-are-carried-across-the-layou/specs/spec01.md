---
complexity: 8
footprint:
  - .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh
---

# spec01 — the three collect/brief harnesses measure the pearde layout

The three suites the parent report measured red across the layout rename —
`collect-keeps-its-word` (33 pass · 68 fail on arrival), `collect-is-a-command`
(32 pass · 101 fail) and `brief-is-printed` (41/104) — build their fixture
boards at
`<dir>/.pearde`, pass `--board <dir>/.pearde` to `collect.py`/`brief.py`
/`plan.py`/`specs.py`/`transitions.py`, resolve their own root by walk-up to
the nearest ancestor holding `resources/guard.py` (or a correct `..` count),
and each prints its own full denominator with zero failures.

What already stands, measured on disk 2026-08-31 after the 878d164/2a3c69a
re-aim wall and the `collect-defaults-to-the-boards-enclosing-repo` repo fix
(55bff9c, 0849795): all three suites are green from the code repo root AND by
absolute path from `/` —

- `collect-keeps-its-word` 101 checks · 101 pass · 0 fail
- `collect-is-a-command` 133 checks · 133 pass · 0 fail
- `brief-is-printed` verify: 104/104 checks pass

The arrival-denominator rule holds: no assertion was added, removed or
weakened by the carry; each suite's own count line is its denominator. One
standing exception is deliberate and stays: `collect-keeps-its-word` line 40,
`run_old`, passes `"$D/.pearde/prds"` to a pinned pre-move `collect.py` copy —
it drives the pearde-shaped board with the old code, which is that harness's
back-compatibility assertion, not a stale path.

What is left, if anything moves: no code. The unit is the proof. An
implementer re-runs the verify block, compares each printed count against the
denominator above, and ticks what passes. A count that comes back short is a
finding: whoever moved the measured file between the analyst's run and this
one owns the delta — do not back-edge the harness to restore a number, and do
not close a box whose output you did not personally quote.

## Acceptance

- [x] `bash .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh`, run from the code repo root, prints `101 checks · 101 pass · 0 fail` as its last line
- [x] `bash .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh`, run from the code repo root, prints `133 checks · 133 pass · 0 fail` as its last line
- [x] `bash .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh`, run from the code repo root, prints `verify: 104/104 checks pass` as its last line
- [x] Each of the three suites, invoked by absolute path from `/`, prints the same count line it printed from the repo root — none derives a root that only works from one directory, and none hardcodes a machine path
- [x] No line in any of the three files hands a bare `<dir>/prds` board to `collect.py`, `brief.py`, `plan.py`, `specs.py` or `transitions.py` — the only `--board …prds` mention board-wide in these three is `run_old`'s documented `.pearde/prds` exception
- [x] Each of the three files derives its root without counting segments of a hardcoded depth that breaks on a nested-board move — a walk-up to `resources/guard.py` (`a-quoted-walk-is-data`'s model), or a `..` count that resolves to the code repo from `/`

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
suite() { local n; n=$(bash "$1" </dev/null 2>&1 | tail -1); echo "$2: $n"; }
suite .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh collect-keeps-its-word
suite .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh collect-is-a-command
suite .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh brief-is-printed
bash /Users/feb/dev/infra/pearde/.pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh </dev/null 2>&1 | tail -1
bash /Users/feb/dev/infra/pearde/.pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh </dev/null 2>&1 | tail -1
bash /Users/feb/dev/infra/pearde/.pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh </dev/null 2>&1 | tail -1
grep -E -- '--board [^ ]*prds' .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh || true
grep -ln '/Users/feb' .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh .pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh || true
echo "spec01: three suites, counts quoted above by name"
```