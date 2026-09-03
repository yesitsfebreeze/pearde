---
complexity: 16
footprint:
  - resources/board/plan.py
  - resources/board/boards.py
  - resources/board/prdfile.py
  - resources/board/repos.py
  - resources/board/registry.py
  - resources/board/silence.py
  - resources/board/needs.py
  - resources/board/vision.py
  - resources/board/schedule.py
  - resources/board/mapfile.py
---

# spec01 — one file becomes ten, each named for what it is responsible for

`resources/board/plan.py` was 3242 lines and twelve banner sections. It is now
ten modules beside each other in `resources/board/`, none over 700 lines, each
named for one thing:

| module | responsible for | lines |
|---|---|---|
| `boards.py` | where a board is on disk, and how a new one is made | 470 |
| `prdfile.py` | one PRD file: frontmatter, boxes, typed numbers, questions | 537 |
| `repos.py` | the git tree under a board, and the lanes cut off it | 134 |
| `registry.py` | the PRDs a board holds and the boards a master merges | 260 |
| `silence.py` | whether a held PRD is still moving | 163 |
| `needs.py` | what a PRD waits on before it may run | 140 |
| `vision.py` | the axis `prds/vision.md` declares, and depth along it | 215 |
| `schedule.py` | what may run now, and in what order | 519 |
| `mapfile.py` | the plan on disk, the journals, the payload the view reads | 488 |
| `plan.py` | the command line, and the module every caller imports | 644 |

**What stands.** The cut is in the tree, uncommitted, produced by
`probe/cut.py` — the split is a table of line ranges over the file plus a
generated import header, so it is re-runnable from a clean checkout and
reviewable as a table rather than as a 3000-line diff. `probe/plan.py.orig`
is the file as it was. Sections A, B and C of `probe/verify.sh` are green:
every module is under 700 lines, every one of the 151 top-level names the
single file carried is still reachable as `plan.<name>` — 148 by value and the
three rebound parse-cache globals through `plan.prdfile` — `pearde help` reports
no module failing to import, and `scan`, `plan`, `status`, `members`,
`calibrate`, `reconcile`, `vision --check` and `example` all exit 0 against
the real board.

Three things the build had to solve, and did:

- **`needs` and `schedule` would have imported each other.** `compute_plan`
  reads `axis_depth`, and `cmd_vision` calls `compute_plan`. The axis is
  `vision.py`, the CLI command that prints it stays in `plan.py`, and the
  cycle is gone. The import order is the `ORDER` list in `probe/cut.py`, and a
  module may only name one before it.
- **The parse cache's three globals are rebound at run time.**
  `_PCACHE`, `_PCACHE_LOADED` and `_PCACHE_DIRTY` live in `prdfile.py`;
  `registry.scan` reads `prdfile._PCACHE_DIRTY` through the module, because a
  `from prdfile import _PCACHE_DIRTY` would bind the value it had at import.
  These three are the only names `plan.py` does not re-export by value — it
  carries `import prdfile` instead, so a caller outside the package still
  reaches them the only way a rebound global can be reached. The parse-cache
  harness does exactly that; spec03 is where it is re-pointed.
- **`cmd_example` printed its own `__file__`.** Moved into `boards.py` it
  printed `python3 …/boards.py scan <dir>` — a command that exists and does
  something else. It now names `plan.py` explicitly.

- **A cut expressed as line numbers is pinned to one revision.** It has been
  re-based onto a moved `plan.py` twice. `1880990` grew a 139-line
  board-discovery pass; `39c0cab..31620bb` added `NotABoard`, `state_dir`'s
  husk guard and `session_tree`, 43 lines more. Each time the lane's own
  harnesses stayed green and the rebase conflicted in `plan.py`. The
  resolution is a re-cut, not a merge — every boundary mapped through a
  `difflib` diff of `probe/plan.py.orig` against the new file, `plan.py.orig`
  refreshed to the new base, and `cut.py`'s own `uncovered` guard proving the
  table still covers every non-blank line. Every hunk both times landed whole
  inside one range — the board-discovery pass and the husk guard in `boards`,
  `session_tree` in `silence`, the `__main__` wrapper in `plan` — so no range
  crossed a module boundary. `cut.py` now also refuses an input whose length
  is not the base's: cutting the already-cut 644-line `plan.py` a second time
  produced ten stubs and collapsed every count, with nothing in the harness
  saying so. `cmd_calibrate`'s sentence and `cmd_example`'s `__file__` are
  both rewritten inside `cut.py` rather than by hand, so a re-cut from a
  clean checkout carries them.

**What is left.** Nothing in this spec. spec02 gives the nine new files their
rows in the map and corrects the five sentences in the prose that name the old
one; spec03 re-points the four harnesses that read `plan.py` by name rather
than through its interface.

## Acceptance

- [x] `resources/board/` holds `boards.py`, `prdfile.py`, `repos.py`,
  `registry.py`, `silence.py`, `needs.py`, `vision.py`, `schedule.py` and
  `mapfile.py` beside `plan.py`, and none of the ten is over 700 lines
- [x] every top-level name the single `plan.py` carried, except the three
  rebound parse-cache globals, is still reachable as `plan.<name>` — the
  check reads `probe/plan.py.orig` with `ast` and compares against the
  imported module, so it cannot pass by a name being spelled twice
- [x] `python3 resources/pearde.py help` exits 0 and prints no line matching
  `failed to import`
- [x] `plan.py scan`, `plan`, `status`, `members`, `calibrate`, `reconcile`,
  `vision --check` each exit 0 against the board, and `plan.py example <dir>`
  writes a board and prints a next command naming `plan.py`
- [x] `pearde calibrate` names `mapfile.py` as `TUNE`'s home, and the string
  `hard-coded in plan.py` is gone from `resources/board/`
- [x] no module in the cut imports a module later than itself in the order
  `boards, prdfile, repos, registry, silence, needs, vision, schedule,
  mapfile, plan` — `python3 -c "import plan"` from `resources/board` raises no
  `ImportError` about a partially initialized module

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
for m in resources/board/boards.py resources/board/prdfile.py \
         resources/board/repos.py resources/board/registry.py \
         resources/board/silence.py resources/board/needs.py \
         resources/board/vision.py resources/board/schedule.py \
         resources/board/mapfile.py resources/board/plan.py; do
  n=$(wc -l < "$m" | tr -d ' '); echo "$m $n"; test "$n" -le 700 || exit 1
done
if grep -rn 'hard-coded in plan.py' resources/board/plan.py; then exit 1; fi
# the probe exits non-zero on any FAIL, and under pipefail that status becomes
# the pipeline's — masking a grep that DID match, so the guard never fires and
# a broken cut reads green. Capture the output and read it, never pipe it.
out=$(PEARDE_ROOT="$PWD" bash .pearde/prds/resources-are-organised-by-responsibility/the-largest-module-is-cut-by-responsibility/probe/verify.sh 2>&1) && rc=0 || rc=$?
[ -n "$out" ]
printf '%s\n' "$out" | tail -1
if printf '%s\n' "$out" | grep -E '^  FAIL [ABC] '; then exit 1; fi
python3 resources/pearde.py help > /dev/null
```
