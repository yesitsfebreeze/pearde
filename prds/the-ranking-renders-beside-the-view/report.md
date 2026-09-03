Verdict: DONE

Second pass of `probe-then-spec` on this PRD: the analyst's pass built the
code and wrote `specs/spec01.md` from it. This pass ran steps 1, 2 and 4 and
did **not** enter step 3 — `attempt-the-build`'s own first `Fails when` row
covers exactly this shape, and spec01's whole `footprint:` is already dirty in
the lane (`git status --short` names all six files and nothing else). Nothing
in the tree moved this pass; every number below is a measurement, and no flip
is claimed as this pass's.

Lane `/Users/feb/dev/infra/pearde/.pearde/.lanes/the-ranking-renders-beside-the-view`,
branch `lane/the-ranking-renders-beside-the-view`, HEAD `1be5d2b` at the first
command and at the last, cut from that commit and never moved
(`reflog: branch: Created from HEAD`). The orchestrator's checkout sits at
`4a94475`, a different commit, so the two roots have diverged: `1be5d2b`
carries `resources/common.py`, which `4a94475` does not. That is why
`doctor.sh` run against the lane prints
`resources/common.py is on disk with no row in references/files.md` and the
checkout does not — an inherited line that closes on the merge, not this
unit's.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | done — `prd.md`, `specs/spec01.md` and pass one's `report.md` read; no `@`/`@@` in the body; the cited source `docs/content/docs/improvements/health-html-ranking.mdx` is on disk in the checkout (untracked, `?? docs/`); all six `footprint:` paths exist in the lane; `git status --short` recorded before the first command |
| 2 | `capture-the-harness-baseline` | done — pre-edit tree rebuilt in scratch (`git show HEAD:<path>` for each footprint file over an rsync of the lane), harness set = the 8 board harnesses that name a footprint path, plus `viewtest.js`, `index.py check` and `doctor.sh`. Every count taken with `PEARDE_ROOT` naming the tree it measures |
| 3 | `attempt-the-build` | **not entered** — second pass, build already in the tree; see the row above |
| 4 | `re-run-the-harnesses` | done — 7 of 8 board harnesses unchanged, 1 red on a count this contract itself moves (below), `viewtest.js` 49/49 → 50/50, gate unchanged. No back-edge taken |
| 5 | `write-the-specs` | **not authored** — second pass. Its `Fails when` table applied to the blocks that stand: the `## Verify and Proof` block was run the way `collect` runs it (`bash -e -o pipefail -c "$(awk …)"`) and exits **0**; pass one's `## Findings` are carried forward below by name |

### Edits

`re-run-the-harnesses.md`, `## Fails when`, the row `a committed harness
outside your footprint goes red on a count the contract itself moves`. Its
`do` column tells the worker to "put the file in the spec's `footprint:`",
which every worker brief forbids twice over — "Never edit frontmatter, never
touch other PRDs" (@references/parts/workers.md:50, and restated verbatim in
the dispatched brief). Worse, a committed board harness lives at
`prds/<other-prd>/probe/verify.sh`, so the file is inside another PRD's folder
and no implementer may write it at all. As written the row asks for an edit
the same brief refuses, and a worker who obeys it lands outside its scope.
Replacement `do` cell:

> leave it red, quote it beside its baseline, and report the one-line matcher
> change with the file, the line number and the replacement text — do not make
> it. A committed board harness lives in another PRD's folder and a worker's
> footprint may not be widened from inside the run; the orchestrator routes
> the repair, as a spec on the harness's own PRD or as a follow-up unit.

## spec01 — acceptance

- [x] `health.py score <board>` then `mapfile.gantt_payload(...)` returns a
      `"health"` key shaped `{"floor": int, "rows": [...]}` with `score`,
      `file`, `worst` and six `axes` per row. Scored a fresh fixture
      (`4 scored · 4 on the ranking · 0 skipped · 1 under 40 · graph none`),
      then the payload: `box1 shape: int floor= 40 rows= 4` ·
      `box1 every row has score/file/worst + six axes: True`. Same call
      against the live board: `scored: floor= 40 rows= 189`,
      `keys: ['floor','rows']`, `row0 keys: ['axes','file','score','worst']`,
      `axes set: ['branching','fan_in','fan_out','lines','links','longest']`,
      worst-first `[4, 28, 28, 29, 33, 39] sorted: True`.
- [x] A board with no `health/ranking.md`: `health key present: True` ·
      `health value: None`.
- [x] `health.py check` and `health.py list` print exactly what they did
      before. Ran both from the pre-edit copy and from the lane against the
      same board: `diff` on each pair is **IDENTICAL** (`check` prints
      `stale: graph 1be5d2b is newer than the ranking's 4a94475 — ...`,
      `list` prints 6 lines, unchanged).
- [x] `node --check resources/board/view.js` → `resources/board/view.js compiles`.
- [x] `node resources/board/viewtest.js --example` → **`50/50 passed`**,
      including `ok    eight section anchors  (got 8)`,
      `ok    the sections are in the PRD's order  (timeline board analytics
      health asks list memos report)` and
      `ok    section "health" is the one shown`.
- [x] The `health` tab on a scored board shows the table. Real Chrome via
      `playwright-core`, fixture scored inside this pass: headers
      `score file lines branching longest "fan out" "fan in" links worst`,
      rows worst first `16, 67, 86, 100` for
      `src/awful.py, src/big.py, src/mid.py, src/small.py`; cell classes seen
      `danger, warn, ok, dim`; first row
      `16 [score] · src/awful.py [file] · 3204 [danger] · 600 [danger] ·
      1202 [danger] · — [dim] · — [dim] · — [dim] · lines, longest [worst]`.
      The under-floor row carries `class="under"` and its score cell computes
      to `font-weight 590`, `color rgb(207, 51, 43)` (`--danger`) against
      `400` / `rgb(16,16,19)` on every other row. Every non-`dim` band cell
      carries its `title` — e.g. `danger|3204|lines 3204 — the line runs 150
      to 1500`; `dim` cells carry `—` as their text, so the colour is never
      the only carrier there either. No page errors.
- [x] The `health` tab on an unscored board shows one line. Rendered text:
      `not scored — pearde health score writes the record this reads`, in the
      `.blank` shape (`blank: true`, `tables: 0`). It is the one line the
      contract asks for, with the command that writes the record appended —
      quoted here because the box says the words `not scored` and the element
      says more than those two words.
- [x] On the merged `all` page, no `health` tab and no `#s-health`:
      `{"virtual":true,"tab":false,"section":false,"reportTab":false,"tabs":
      ["boards","timeline","board","analytics","asks","list","memos"]}`.

`## Verify and Proof`, run in a copy of the lane exactly as `collect` runs it
(`bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec01.md)"`):
**exit 0**, ending `50/50 passed` and `scored: 40 189`. It leaves no tracked
file dirty — `npm i playwright-core` writes only the gitignored
`node_modules`, there is no `package.json` in `resources/board` to move. One
caveat for whoever edits it: the block `cd resources/board` before the Python
heredoc, so `sys.path.insert(0, "resources")` names a directory that does not
exist at that cwd; it works only because `python3 -` puts the cwd on the path
and `plan.py` sits there. Harmless, and true of the block as it stands.

## The contract reddens one committed harness — left red

`prds/one-page-that-says-whats-up/probe/verify.sh`, line 78:

- baseline, pre-edit tree: `31 checks · 26 pass · 5 fail`
- this tree: `31 checks · 25 pass · 6 fail`
- the one added line: `FAIL: the bar is seven anchors that jump, plus boards
  for the merged page`

The matcher is honest and the change is the contract's: it asserts
`grep -cE 'href="#view=[a-z]+" data-v=' resources/board/render.py` equals 8,
and the `health` tab makes it 9 (checkout: 8, lane: 9). Every other FAIL line
that harness prints — `report.md exists`, `report.md carries a dateline`,
`report.md has an '## In work' section`, `report.md has a '## Planned'
section`, `...calling all six draws` — is present in the pre-edit tree too,
and the last three are present in the orchestrator's checkout as well
(`31 checks · 28 pass · 3 fail` there). None of those are this unit's.

The file is another PRD's, so this pass did not touch it. The repair is one
line, and its own comment block above it needs the same re-aim:

```
t "the bar is eight anchors that jump, plus boards for the merged page" "test $(grep -cE 'href=\"#view=[a-z]+\" data-v=' $R) -eq 9 && grep -q 'data-v=\"boards\"' $R && grep -q '#views a\[data-v=\"boards\"\]' $V"
```

The rule the check asserts does not move: `render.py` writes nine anchors and
each page boots down to eight — a board's own page drops `boards`, the merged
page drops `health`. The comment above line 78 should say so, since it
currently explains only the `boards` half.

## Harness set, baseline → re-run

Every count taken with `PEARDE_ROOT` naming the tree measured; the pre-edit
tree is the lane with the six footprint files restored from `HEAD`.

| harness | pre-edit | lane |
|---|---|---|
| `viewtest.js --example` | `49/49 passed` | `50/50 passed` |
| `one-page-that-says-whats-up` | `31 checks · 26 pass · 5 fail` | `31 checks · 25 pass · 6 fail` |
| `one-graph-writer` | `8 checks · 3 pass · 5 fail` | same |
| `one-section-registry` | `2/6 passed, 3 skipped` | same |
| `files-score-their-health-…` | `37 checks · 36 pass · 1 fail` | same |
| `resources-are-organised-by-responsibility` | `probe: 11 passed, 9 failed` | same |
| `…/every-module-finds-its-siblings-by-one-rule` | `probe: 22 passed, 1 failed` | same |
| `the-board-runs-itself/an-example-board` | `37 checks · 36 pass · 1 fail · 1 skipped` | same |
| `…/the-documented-board-matches-the-code` | `FAIL README's .gitignore count is not ten` | same |

Every red in that table except the one line named above was red **before the
first edit**. The `viewtest.js` count rose by one because this unit added the
section: the suite runs one `section "<name>" is the one shown` check per
section, and `health` is the eighth. No pre-existing check in it moved.

Repo gate, both trees: `python3 resources/index.py check` prints the same two
lines in the pre-edit copy and in the lane — `references/files.md lists
@resources/board/hotreload-test.js — not on disk` and `@@view names
@resources/board/hotreload-test.js — not on disk`. `bash resources/doctor.sh`
on the lane exits 1 on `index` (3 problems), `claims` (6 drifted names),
`vault`, `origin` and `memos` (43 problems) — none names a footprint path, all
inherited. `jstests` reads `off` because `--harnesses` was not passed; the row
it would run is `viewtest.js --example`, run directly above at 50/50.

## Findings — carried forward from pass one, still true, still out of footprint

- `resources/doctor.sh`'s `jstests` row names `resources/board/hotreload-test.js`
  and the file exists nowhere in the tree. Confirmed again this pass: it is
  also the whole of `index.py check`'s red, in both the pre-edit tree and the
  lane. Pre-existing, unrelated to this PRD, and never reached by `--example`.
- `resources/board/all.py`'s merged payload folds no `health` key from its
  members — confirmed this pass: `all.payload([...])` returns
  `health key in merged payload: False`. spec01 removes the tab on that page
  rather than letting it render `not scored` for the wrong reason. A
  cross-repo worst-files view is a second unit; the merge would have to decide
  what "worst" means across repos with no shared floor.

## Findings new to this pass

- The brief's health-floor block says `none under the floor` for this
  footprint, and two footprint files are under it: `resources/board/view.css`
  at **4** and `resources/board/view.js` at **39**, floor **40**, both on
  `lines` (`pearde health list` names them). `prd.md` carries no `footprint:`
  key — only `specs/spec01.md` does — so the block appears to read the PRD's
  frontmatter rather than the union of its specs' footprints, and reports an
  empty set whenever a PRD's footprint lives only in its specs. Worth a look
  by whoever owns that block.
- Nothing was moved for those two files: both fail on `lines` alone, this
  contract necessarily adds lines to each (19 to `view.css`, 75 to `view.js`),
  and the only repair is a split — a defect outside this spec's scope,
  reported here rather than done.

## Scores

complexity: 14
blast-radius: mid
workflow: probe-then-spec
