Verdict: DONE

**Pass two of `probe-then-spec`, and the build the brief said was already in
the tree was gone.** Pass one built it uncommitted in the orchestrator's
checkout; between that pass and this one it was destroyed. Nothing holds it:
`git log -S'window.__SECTIONS__' --all` finds no commit, no stash carries it,
and a scan of all 1159 loose and packed blobs between 10 KB and 60 KB for the
string finds none. So `attempt-the-build` was entered in full and every spec01
box was re-earned rather than inherited — all seven now cite output from this
pass, taken in the lane at `.pearde/.lanes/one-section-registry`.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | done — PRD, spec01 and pass one's report read; `git status --short` recorded in the checkout, the lane and the board repo before the first edit. The lane was clean at HEAD `1be5d2b`; the checkout's `render.py`/`view.js` held a neighbour's hunks and no trace of the probe's build |
| 2 | capture-the-harness-baseline | done, narrowed — 6 of the board's 98 harnesses spell a footprint path; all six baselined with `PEARDE_ROOT=<lane>`, plus `viewtest.js` on both page shapes and the repo gate. Two atomic defects hit; see **Edits** |
| 3 | attempt-the-build | entered in full (the build was absent, not present) and completed. No back-edge |
| 4 | re-run-the-harnesses | one real regression, caught and repaired inside the route's own rule; every other count back at baseline. No back-edge |
| 5 | write-the-specs | second pass — no spec authored. `## Fails when` applied to the blocks that stand: one box re-aimed to a claim that is true, one box added for the harness this unit had to repair, one footprint entry added, and the `## Verify and Proof` block rewritten from prose into shell that runs |

### Edits

Two atomics need a row; neither file was touched by me.

**`capture-the-harness-baseline`, `## Fails when` — the narrowing recipe does
not run on this board.** Step 2 and two rows of the table spell the subset as
``grep -ln "<path>" $(find <board>/prds -name verify.sh)``. On this board that
command dies: 98 harnesses under slugs 40–60 characters long overflow the
argument list (`File name too long`), and under `ugrep` — the `grep` on this
machine — the truncated invocation prints **every** harness instead of the six
that match, which reads as a correct answer and is not one. Replacement row:

| seen | means | do |
|------|-------|----|
| ``grep -ln "<path>" $(find <board>/prds -name verify.sh)`` prints `File name too long`, or prints nearly every harness on the board | the board's harness paths overflow one argument list, and a `grep` that is `ugrep` reports the truncation as a warning on stderr and answers from the surviving arguments — a subset that looks like the whole answer | never pass the set as arguments. `find <board>/prds -name verify.sh \| sort > <scratch>/all.txt`, then `bash -c 'while read f; do grep -qF -e "<path1>" -e "<path2>" "$f" && echo "$f"; done < <scratch>/all.txt'`. Quote the two counts side by side — `wc -l` of the whole list and of the subset — so a subset that is suspiciously close to the whole is visible before it is trusted |

**`read-the-contract`, `## Fails when` — a second pass whose first pass's
build no longer exists.** The row for a lane repo assumes the checkout still
holds the earlier pass's uncommitted hunks ("copy those files into the lane and
continue there"). It has no row for the case where they are simply gone, and
the brief still says the tree holds them — which sends a worker looking for a
build instead of making one. Replacement row:

| seen | means | do |
|------|-------|----|
| the brief says the probe's uncommitted code is already in the tree, and neither the lane nor the checkout holds it | an uncommitted build between two passes of one route survives only as working-tree bytes; a `reset --hard`, a `stash` that was dropped or a `collect` that parked the tree destroys it with no record | prove it is gone before rebuilding: `git log -S'<a string only the build carries>' --all`, `git stash list` with `git stash show --stat` per entry, and a scan of unreachable blobs (`git cat-file --batch-all-objects --batch-check`, filtered by size, `grep`ed for the string). If all three are empty the build is unrecoverable — enter `attempt-the-build` in full, and say in the report that every box was re-earned rather than inherited. The specs are still the contract; only the code is missing |

## What was built

`render.py` carries one `SECTIONS` list — `id`, `title`, `nav_attrs`,
`nav_extra`, `band`, `folds`, `only`, `host`, `on`, `summary`, `body` — and
`_nav_html()` / `_sections_html()` generate the header bar and the
`<section data-view=…>` wrappers from it. **The generated markup is
byte-identical to the hand-written template it replaces**: `diff` of
`TEMPLATE` before the edit against `TEMPLATE` with both generators substituted
after it is empty. That is the proof the PRD's "no visual change" asked for,
and it is stronger than the pass counts.

The registry rides across as `window.__SECTIONS__` beside `window.__PAYLOAD__`.
It is substituted **before** `view.js` is inlined, because `view.js` names
`window.__SECTIONS__` in its own source and a token replaced after the inlining
would rewrite the script that reads it — the same trap the renderer already hit
once with `__PAYLOAD__`, which is why the tokens are `__NAVBAR__` and
`__SECTIONBODY__` and not `__SECTIONS__`.

`view.js` drops a section and its tab together by `only` against the page's own
`virtual` flag, in one loop over the registry, where two blocks each named
`"report"` or `"boards"` by id; the merged page's landing section is
`DEFAULT_VIRTUAL`, the first row marked `only: "virtual"`, where
`setView("boards")` was typed.

`viewtest.js` reads the same rows for its expected order, its landing section,
its per-section `host` selector and its anchor count, replacing a two-variant
`ORDER` array, a hard-coded six-selector host list and a hard-coded seven.

`folds` is load-bearing, not decoration: `_sections_html()` writes the
`<details class="fold">` and its `<summary>` from the field, so flipping a row
changes the page. The fold rule is a field now, which is the PRD's own words.

## Numbers, baseline → after

Every harness run with `PEARDE_ROOT=<lane>` in both directions, and with a
`playwright-core` driver found at `NODE_PATH=/Users/feb/gstack/node_modules`.

| harness | before the first edit | after |
|---|---|---|
| `one-section-registry/probe/verify.sh` | `2/6 passed, 3 skipped` (`AttributeError: module 'render' has no attribute 'SECTIONS'`) | **`10/10 passed, 0 skipped`** |
| `viewtest.js --example` | `49/49 passed` | `49/49 passed` |
| `viewtest.js` on a merged (`all`) page | `50/50 passed` | `50/50 passed` |
| `one-page-that-says-whats-up/probe/verify.sh` | `31 checks · 26 pass · 5 fail` | `31 checks · 26 pass · 5 fail` (went to 8 fail mid-run; repaired — below) |
| `an-example-board/probe/verify.sh` | `37 checks · 36 pass · 1 fail · 1 skipped` | identical, like-for-like |
| `resources-are-organised-by-responsibility/probe` | `probe: 11 passed, 9 failed` | unchanged |
| `…/every-module-finds-its-siblings-by-one-rule` | `probe: 22 passed, 1 failed` | unchanged |
| `the-documented-board-matches-the-code/probe` | `FAIL README's .gitignore count is not ten` | unchanged |
| `python3 resources/index.py check` | 3 lines, exit 1 | byte-identical, exit 1 |
| `bash resources/doctor.sh` | exit 1 | every row identical but three, none mine — below |

The two `viewtest.js` check sets are identical before and after down to the
label: `diff` of the two runs' check lines names exactly two renamed checks
(`seven section anchors` → `one section anchor per registry row`, `the sections
are in the PRD's order` → `…in the registry's order`) and nothing else.

The five failures left in `one-page-that-says-whats-up` and the reds in the
other four harnesses are all inherited, recorded **before the first edit**.
Four of the five are `.pearde/report.md` assertions that cannot pass in a lane,
which carries no board of its own.

Three `doctor` rows moved and none is this unit's: `statusline` gained `*3`
(this lane's three modified files — the row carries a dirty count and every
live session moves it), `knowledge` went `broken` → `ok` (a sibling relinked
the graph mid-run; a rise is not mine to claim), and `harnesses` went 98 → 100.
The two new harnesses are `the-lifecycle-contract-and-purge-reclaims-it/probe`
and `the-promotion-rule/probe`, landed by a parallel session after my baseline;
neither names a footprint path, and a harness with no baseline cannot regress.

## The one real regression, and its repair

`one-page-that-says-whats-up/probe/verify.sh` went `26 pass · 5 fail` →
`23 pass · 8 fail`, and a fourth of its checks started passing for the wrong
reason. All four read the hand-typed markup out of `render.py`'s **source** —
which is exactly what this PRD replaces with a generator:

- `the plan toolbar is inside its own section` — `s.index('<section data-view="timeline"')` on the source, now a `ValueError`
- `the bar is seven anchors that jump, plus boards for the merged page` — `grep -cE 'href="#view=[a-z]+" data-v='` over the source, now 0
- `every anchor has the view it names` — two source regex sets, now both empty
- `the three archives fold, and only those` — `grep -c 'details class="fold"'` over the source; this one still printed 3 and still *passed*, but two of its three matches were my own new comments. A check passing by coincidence is worse than one failing honestly, so it is counted with the others.

`re-run-the-harnesses`' `## Fails when` names this case — *a committed harness
outside your footprint goes red on a count the contract itself moves* — and its
instruction is to put the file in the spec's `footprint:` with the matcher
change as that spec's work. Done: the harness is in spec01's footprint, and all
four matchers now read the page `render.py` **writes** (`TEMPLATE` with both
generators substituted) instead of the source it used to be typed in. Same
rules, one level later, no browser needed.

Not weakened — each was re-run against the mutation it exists to catch, and
each failed:

```
--- A: a fourth folding row ---        FAIL: the three archives fold, and only those
--- B: a stray hand-written anchor --- FAIL: the bar is seven anchors that jump, plus boards for the merged page
                                       FAIL: every anchor has the view it names
--- C: the toolbar leaves timeline --- FAIL: the plan toolbar is inside its own section
```

`render.py` was restored byte-identical after each mutation, from a
`trap … EXIT INT TERM` — pass one's own hard-won lesson, carried forward.

## The merge will conflict in `render.py`, and here is the resolution

The orchestrator's checkout holds a neighbour's uncommitted rename in
`render.py`: `asks` → `questions` on the nav anchor, and
`<h2 class="sect">waiting on you</h2>` → `<h2 class="sect">questions</h2>` in
the asks section. Both land on lines this build moves into `SECTIONS`.

Proved rather than guessed, per `re-run-the-harnesses`' adjacent-hunk row:
`git clone --shared` of the checkout, the neighbour's working copy committed
there, then `git apply --3way` of this lane's diff —

```
Applied patch to 'resources/board/render.py' with conflicts.
Applied patch to 'resources/board/view.js' cleanly.
Applied patch to 'resources/board/viewtest.js' cleanly.
```

`view.js` and `viewtest.js` merge clean; `render.py` conflicts twice. The
resolution is two edits on the `asks` row of `SECTIONS` — `"title":
"questions"` and `<h2 class="sect">questions</h2>` in its `body` — and it was
carried out in that scratch tree, where the resolved file renders a page
**byte-identical** to the neighbour's own. The lane must not carry the hunk
itself: the checkout already holds it and it would land twice.

`git status --short` at the end: the lane holds `resources/board/render.py`,
`view.js`, `viewtest.js`; the board repo holds
`prds/one-page-that-says-whats-up/probe/verify.sh`,
`prds/one-section-registry/specs/spec01.md` and the untracked
`prds/one-section-registry/prd.md`. Nothing else, in either root.

## The spec block now runs

Pass one's `## Verify and Proof` block was prose — a bare
`bash prds/one-section-registry/probe/verify.sh` plus comments, relative to the
board, which `collect` runs from the code repo where that path does not exist.
It is now shell that resolves both roots from `PEARDE_ROOT` or `git rev-parse
--path-format=absolute --git-common-dir`, runs this unit's harness (whose own
last line is `[ "$fail" -eq 0 ]`, so no total is nailed down), and gates the
repaired harness on its four check **names** rather than on its total, which
carries inherited reds. Run the way `collect` will —
`bash -e -o pipefail` over the `awk`-extracted block — it exits **0**.

## Findings (carried forward from pass one, and this pass's own)

Pass one's findings, still open and still not this PRD's to fix:

- **The crash-safety lesson for `attempt-the-build`'s own atomic.** A footprint
  mutation left live across a kill — the specific trigger being an outer
  harness timeout during a multi-browser-launch probe — is not in that
  atomic's fails-table. `verify.sh` carries the `trap`; the atomic does not
  carry the row. Still owed to whoever next edits that file.
- **Two pre-existing `index.py check` lines**, unrelated to this footprint and
  unchanged across both passes: `resources/common.py is on disk with no row in
  references/files.md`, and `references/files.md lists
  @resources/board/hotreload-test.js — not on disk` (which a third line
  repeats through `@@view`).

This pass's own, none of them fixed:

- **`the-board-runs-itself/an-example-board/probe/verify.sh` carries three
  stale hard-coded totals**, invisible without a driver and red with one:
  it wants `35/35 passed` and `47/47 passed` from `viewtest.js` and 12 snapshot
  files. The pre-edit lane already printed `49/49` — measured at baseline,
  before the first edit — so all three were stale before this PRD existed. With
  a driver that harness reads `43 checks · 39 pass · 4 fail`; run the way the
  baseline was taken, without one, it is `36 pass · 1 fail` before and after.
  A literal total of another harness's count is the wall
  `write-the-specs`' fails-table warns about, and it is owed to that PRD.
- **A route collision worth a line in one of the two files.**
  `probe-then-spec`'s "Use when" says a second-pass step 5 applies its
  `## Fails when` table "without authoring a spec"; `re-run-the-harnesses`
  instructs a second-pass worker to add a file to `footprint:` and a matcher
  change as that spec's work. Both were followed here — the footprint entry and
  one box were added, no spec was authored — but the two sentences read as
  opposed, and a worker who reads only the route will leave a committed harness
  red. Not edited: the brief forbids editing the workflow files.
- Nothing was learned from outside this repo. `knowledge.py remember` was not
  called and `.pearde/wiki/pending/` is untouched, which is the honest answer
  rather than an omission.
- No file in the footprint is under the health floor; the brief named none and
  none appeared.

## Boxes

All seven of spec01's acceptance boxes are `[x]`, each ticked as it closed and
each citing output from **this** pass. Two were edited rather than merely
ticked:

- **Box 1 re-aimed.** It claimed nothing else in `render.py` spells any of the
  eight section ids. That is not true and was not true after the build: four
  occurrences remain and none of them declares a section — `p["board"]` (a
  payload key), `aria-label="boards"` on the board picker, `title="list"` on a
  mode button, and one `data-go='{"view":"report"}'` door. The box now asserts
  what is both true and checkable: with the `SECTIONS` block cut out of the
  file, the only remaining `data-v=`, `data-view=` and `#view=` are the two
  format strings inside the two generators and one line of the registry's own
  comment — measured, 1, 1 and 2 — so no `<a>` and no `<section>` is typed by
  hand anywhere, and the four survivors are named in the box.
- **Box 7 added**, for the `one-page-that-says-whats-up` harness this unit had
  to repair, with its falsifiability proof.
