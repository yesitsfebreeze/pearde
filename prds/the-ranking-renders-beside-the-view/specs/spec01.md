---
complexity: 14
workflow: probe-then-spec
footprint:
  - resources/health.py
  - resources/board/mapfile.py
  - resources/board/render.py
  - resources/board/view.js
  - resources/board/view.css
  - resources/board/viewtest.js
---

# spec01 — the view gains a `health` tab: the ranking, worst first, each number beside its line

**All of it already stands in the tree, uncommitted.** The implementer's job
is to read it, run the probe below, and tick each box against what it
prints.

## What already stands

- **`resources/health.py`** gains `_cell_num` (a ranking-table cell back to
  a number or `None`), `axis_band(axis, kind)` (the `(lo, hi)` pair
  `THRESHOLDS` already keeps, at the file's own kind), and
  `view_payload(board)`: `read_ranking(board)`'s rows turned into
  `{"floor": int, "rows": [{"score", "file", "worst": [...], "axes": {axis:
  {"value", "band"}}}]}` for the six axes `ranking.md`'s own columns carry
  (`lines`, `branching`, `longest`, `fan_out`, `fan_in`, `links` — nesting is
  not a ranking column and stays off this payload, on the note a click
  fetches). Returns `None` when there is no `ranking.md` yet.
  `read_ranking`'s rows also carry the six raw numbers now, `_cell_num`-
  parsed; `check()` and `list_ranking()` read the same dict and are
  unaffected — they used only `score`, `file` and `why`, both still present.
- **`resources/board/mapfile.py`** imports `health as healthlib` and
  `gantt_payload` gains one key, `"health": healthlib.view_payload(board)`
  — read fresh off disk on every call, the same file `pearde health list`
  reads, no cache of its own. `render.enrich()` copies the payload dict
  unchanged, so the key survives to both the embedded first paint
  (`/board/<name>`) and the polled `/data` swap-in-place.
- **`resources/board/render.py`**'s `TEMPLATE` gains a nav entry
  (`<a data-v="health">health</a>`, between `analytics` and `asks`) and
  `<section data-view="health" id="s-health"><pearde-health
  id="health"></pearde-health></section>`.
- **`resources/board/view.js`** gains `PeardeHealth`, a `LitElement` reading
  `DATA.health`: a table, worst score first (the payload is already sorted
  that way), one row per file — score, file, the six axis values, worst
  axes — and `drawHealth()`, wired into `drawAll()`. A `None` payload
  renders the `.blank` shape every other empty section already uses:
  `not scored`. Each axis cell is coloured by which side of its band the
  value sits on — `ok` at or under the low line, `danger` at or over the
  high line, `warn` between, `dim` when the file's kind never measured that
  axis — the same three-word vocabulary `#list`'s state dots already spend,
  named in a `title` attribute too so the colour is never the only carrier.
  A row under the floor bolds and reddens its score cell. On the merged
  `all` page the tab and section are **removed**, not hidden — the same
  treatment `report` already gets there, for the same reason: health is one
  repo's own record, and a table of files across several repos would not
  share a scale.
- **`resources/board/view.css`** gains `#health` rules mirroring `#list`'s
  existing table chrome, plus `.ok`/`.warn`/`.danger`/`.dim` cell colours
  off the vars every other section already uses.
- **`resources/board/viewtest.js`**, the committed harness `pearde doctor
  --harnesses` runs (`jstests` row): the section-anchor count moved from
  seven to eight, and the PRD-order assertion for the non-virtual page now
  reads `timeline board analytics health asks list memos report`. Both are
  updated to match; the virtual (`all`) page's expected order is unchanged,
  since `health` is removed there.

Verified against a fixture board scored inside this pass (`pearde health
score`, a two-file git repo): worst-first ordering, `danger`/`warn`/`dim`
cell classes, and the under-floor row all render as designed. Verified
against a fresh board with no `.pearde/health/` at all: the section renders
the one line `not scored`. Verified that a rescore between two payload
reads changes the numbers the second read returns, with no reload and no
second daemon — the existing `/data` poll is the whole mechanism.

## What is left to finish

Nothing to build. Land the six files as they stand.

## Findings for whoever reads this next (not acted on here — out of footprint)

- `resources/doctor.sh`'s `jstests` row also runs `hotreload-test.js` when a
  live service is registered for the board under test; that file does not
  exist anywhere in this tree (`find resources -iname '*hotreload*'` is
  empty). Pre-existing, unrelated to this PRD — the `jstests` row only
  reaches that branch when a service is already up and serving the board by
  name, which `--example`'s own run never triggers, so this PRD's own
  verify below never exercises it either.
- The merged (`all`) page's payload (`resources/board/all.py`) does not
  merge a `health` key at all — each member board's own `gantt_payload`
  carries one, but `all.payload()`'s loop never reads `p.get("health")`.
  Showing a cross-repo worst-files view there, if ever wanted, is a second
  unit: the merge has to decide what "worst" means across repos that do not
  share a floor, which this PRD's contract never asked for.

## Acceptance

- [ ] `python3 resources/health.py score <board>` then a Python call to
      `mapfile.gantt_payload(board, ...)` returns a `"health"` key shaped
      `{"floor": int, "rows": [...]}`, each row carrying `score`, `file`,
      `worst` and `axes` for all six axes.
- [ ] The same call against a board with no `.pearde/health/ranking.md`
      returns `"health": None`.
- [ ] `resources/health.py check` and `resources/health.py list` print
      exactly what they did before this spec — `read_ranking`'s extra keys
      change nothing either reads.
- [ ] `node --check resources/board/view.js` — compiles.
- [ ] `node resources/board/viewtest.js --example` — 50/50, including
      `eight section anchors`, the PRD-order line naming `health`, and
      `section "health" is the one shown`.
- [ ] Opening the `health` tab on a scored board shows a table, worst score
      first, each axis cell classed `ok`/`warn`/`danger`/`dim` by its own
      band.
- [ ] Opening the `health` tab on an unscored board shows the one line
      `not scored`.
- [ ] On the merged `all` page, no `health` tab and no `#s-health` exist in
      the DOM.

## Verify and Proof

```sh
# from the repo root (or the lane's own copy)
node --check resources/board/view.js && echo "resources/board/view.js compiles"
cd resources/board && npm i playwright-core   # once, if not already present
node viewtest.js --example

# the payload, both states
python3 - <<'PY'
import sys, tempfile, subprocess, os
sys.path.insert(0, "resources"); sys.path.insert(0, "resources/board")
import plan as planlib
board = "/Users/feb/dev/infra/pearde/.pearde"   # any scored board
p = planlib.gantt_payload(board, planlib.scan(board), planlib.load_map(board)[0],
                          planlib.board_settings(board))
assert p["health"] and p["health"]["rows"], "expected a scored health payload"
print("scored:", p["health"]["floor"], len(p["health"]["rows"]))
PY
```
