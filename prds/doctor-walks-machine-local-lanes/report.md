Verdict: DONE

# doctor-walks-machine-local-lanes — implementer, pass two

spec01: 6 of 6 boxes ticked, each against quoted probe output.
`bash .pearde/prds/doctor-walks-machine-local-lanes/probe/verify.sh` → `0 failure(s)`,
11 checks over 3 cases. Live board: `lanes  broken  6 of 45 lane(s) cannot find the board`.

Pass one built `lanes.check`/`lanes.relink` and the `doctor.sh` row and left
them uncommitted in this lane. This pass re-measured them, found and closed
one hole, and added the two probe cases that were missing.

## What this pass changed

- `resources/doctor.sh` — the `lanes` row now takes `LRC=$?` on the
  `python3 -c` capture and reddens on a non-zero exit, before it greps.
  Without it the row read `ok` with a lane count whenever `lanes.check`
  raised: the traceback went into `$LPROB`, `grep -c ': no link to the
  board'` counted 0, and 0 took the `ok` branch. This is the `health`
  row's own pattern (`HRC=$?`, six sections above) — the `lanes` row was
  the only board-scoped row deriving its verdict from a grep alone.
  Filed as knowledge `[[260904-a336]]`.
- `probe/verify.sh` — two cases the harness could not fail without.
  Case 2 now clears the blocking file and asserts the `ok` half of box 4
  (`2 lanes, every one finds the board`), which nothing exercised before.
  New case 3 `chmod 000`s the fixture's `.lanes/` and asserts the row is
  `broken`, not `ok` — the check for the guard above.
- `specs/spec01.md` — boxes ticked with their output, plus a sixth box for
  the guard's behaviour. Adding a box to a spec I was dispatched to
  implement is the one liberty this pass took; leaving new behaviour
  unspecced looked worse than the edit.

`resources/board/lanes.py` is unchanged from pass one — `check` and
`relink` hold under all three fixture cases and against the 45 real lanes.

## Not done, out of footprint

`references/parts/doctor.md` does not name the new row, so
`the-documented-board-matches-the-code` prints
`doctor.md is missing rows: briefs guard jstests knowledge lanes plugins vault vision`
— eight names where it printed seven before this row existed. The other
seven predate this PRD; that harness has been red on this check for a
while. The file is outside `footprint:`, so this is reported, not fixed.
The row to append to that table, matching its neighbours:

| `lanes`      | no `.lanes/` on the board              | a machine-local lane whose top level holds no path resolving to the live board |

`doctor --fix` was **not** run against the live board this pass. Six real
lanes are named and repairable, but relinking another session's lane
mid-round is not this PRD's call — the fixture proves the repair, and
`pearde doctor --fix` is one command for whoever wants it.

## Gate and harnesses

Baselines taken against `git clone --shared` of this lane at its own HEAD
`d8b509c`, with the live board symlinked in, `PEARDE_ROOT` set — the route
`capture-the-harness-baseline` prescribes for an uncommitted lane build.

| check | pre | post | reading |
|---|---|---|---|
| `index.py check` | 27 lines | 27 lines, byte-identical | pre-existing, none mine |
| `doctor.sh .pearde` | see rows below | no new `broken` row but `lanes` | `lanes` is this PRD's row, reporting a true state |
| `upgrade-leaves-the-memo-index-stale` | 17 pass · 22 fail | 17 · 22 | pre-existing |
| `resources-are-organised-by-responsibility` | 11 · 9 | 12 · 8 | better; the flip is `package.json`, absent in a clone |
| `the-skill-tree-is-guarded` | 36 · 5 | 40 · 1 | better; the clone has no live `.claude/settings.json` |
| `the-doctor-completes-without-a-home` | 9 · 3 | 9 · 3 | pre-existing |
| `workflow-seed` | 67 · 13 | 67 · 13 | pre-existing |
| `ramp-is-a-doctor-row-not-a-gate` | red | red, one count higher | see `__pycache__` below |
| `the-documented-board-matches-the-code` | red, 7 rows missing | red, 8 rows missing | the row above; out of footprint |
| `vision-is-first-class` | 46/52 | 46/52 | pre-existing |
| `a-lane-s-wiki-is-a-stub-…` | — | exit 0 | green, the only other harness naming `lanes.py` |

Narrowed set, and how: 24 of 103 harnesses spell `resources/doctor.sh`; a
full sweep does not finish and 21 of the 24 honour `PEARDE_ROOT`. Narrowed
again to the ten that assert on doctor's *row set* — the only thing a new
row can break — plus the one naming `lanes.py`. A sweep was not run.

Pre-existing `broken` doctor rows, none in this footprint: `index` (27),
`claims` (3 drifted names), `origin`, `memos`, `workflows`, `knowledge`.
`guard`, `vault` and `plugins` read `off` from a lane because their paths
resolve to `<lane>/../.claude` — lane scoping, not a defect.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | `prd.md` is still the placeholder template; `specs/spec01.md` carries the whole contract. Read it and pass one's report instead. No fork left open. |
| 2 | `capture-the-harness-baseline` | done via `git clone --shared` + board symlink + `PEARDE_ROOT`. One shape the table does not list — below. |
| 3 | `attempt-the-build` | second pass: the blocks stood, re-measured, one hole found and closed. |
| 4 | `re-run-the-harnesses` | eleven harnesses, table above. Nothing went green to red. |
| 5 | `write-the-specs` | second pass: `Fails when` applied to the standing blocks, boxes ticked, no spec authored. |

### Edits

`capture-the-harness-baseline`, `## Fails when` — one row to add:

| a `git clone --shared` pre-tree scores *better* than the lane on a harness that counts matches under a source directory, and the extra matches are in files neither tree edited | the lane has `resources/**/__pycache__/*.pyc` from every `python3 -c` the build ran, and the clone has none — a `grep -r` count reads the byte-compiled copy of the same source twice | measured here: `ramp-is-a-doctor-row-not-a-gate` reads `no file under resources/ still reads happiness: — got 9` in the clone and `got 13` in the lane on identical tracked bytes. Compare `git ls-files`-scoped counts, or `find … -name __pycache__ -prune`, and never read a count difference sourced only in build byproducts as a regression |

`capture-the-harness-baseline`, row 141 — its prescribed command is refused
in this environment. `bash -c "for f in …; done; exit 0"` is blocked by the
tool's safety net (`shell execution source cannot be verified safely`) the
moment the loop body is a variable. Replacement text for that row's **do**:
run the harnesses as separate literal commands in one call, each
redirecting to its own file and echoing `$?` — `bash <path> >/tmp/hN.txt
2>&1; echo "hN=$?"` repeated. It costs one line per harness and reads the
exit code the loop was there to collect.

Not an atomic, but the brief's own first command: `pearde brief …` is
`command not found` in a worker shell on this machine — nothing installs a
`pearde` binary on `PATH`. `python3 resources/pearde.py brief …` from the
repo root is what runs.

## Scores

complexity: 12
blast-radius: low
workflow: probe-then-spec
