Verdict: SPECCED

## What the build did

Followed `probe-then-spec`. `python3 resources/knowledge.py query` from the
lane found no note on this exact mechanism (only loosely related hits, no
gap worth enqueuing — the record has nothing pointed enough to contradict
or confirm). `python3 resources/workflows.py list` named `probe-then-spec`
as the fit (an open PRD, contract to specs from a build).

Read the contract, then read the code to find the actual "payload service"
and "section registry": `resources/board/render.py`'s `TEMPLATE` `<nav
id="views">` is the tab list every board page shares, `resources/board/
mapfile.py`'s `gantt_payload` is the one payload `/data`, `/board/<name>`
and the merged `all` page all read, and `resources/health.py` already keeps
`ranking.md`, worst first, with the thresholds (`THRESHOLDS`) that decide
which side of the line a number is on.

Built it: `health.py` gains `view_payload(board)` (ranking rows turned into
score/file/worst/axes-with-bands, `None` when unscored); `mapfile.py` adds
one `"health"` key to `gantt_payload`, read fresh per call; `render.py`
gains a `health` nav tab and section; `view.js` gains `PeardeHealth` (a
worst-first table, cells coloured `ok`/`warn`/`danger`/`dim` by threshold
side) and removes the tab on the merged `all` page, the same treatment
`report` already gets there, for the same reason. `view.css` styles the
table off vars already in use. `viewtest.js` — the committed harness
`pearde doctor --harnesses` runs — needed its section count (seven → eight)
and its PRD-order assertion updated; both were. Ran `node viewtest.js
--example` before fixing the assertions (two `FAIL`s, both caused by
adding the tab) and again after — **50/50 passing**, including a genuine
click through the new tab.

Also hand-verified beyond the harness: a fixture board with a real
`ranking.md` (a two-file git repo, `pearde health score`) renders
worst-first with correct `danger`/`warn`/`dim` classes and the under-floor
row bolded; a board with no health record renders `not scored`; and
re-scoring between two payload reads changes the numbers the second read
returns — the existing `/data` poll is the whole "swap-in-place keeps it
current" mechanism, no watcher or second daemon added.

## Findings (not acted on — out of this PRD's footprint)

- `resources/doctor.sh`'s `jstests` row names `resources/board/
  hotreload-test.js` as the second half of that gate; the file does not
  exist anywhere in the tree. Pre-existing, unrelated to this PRD, and
  never reached by `--example`'s own run (that branch only fires when a
  live service is already registered for the board under test).
- `resources/board/all.py`'s merged-page payload does not fold a `health`
  key from its members at all — each member's own `gantt_payload` carries
  one, `all.payload()`'s merge loop just never reads it. A cross-repo
  worst-files view, if ever wanted, is a second unit: the merge would have
  to decide what "worst" means across repos with no shared floor, which
  this PRD's contract never asked for. Spec01 removes the tab there rather
  than leaving it to render `not scored` for the wrong reason.

## Scores

complexity: 14
blast-radius: mid
workflow: probe-then-spec
