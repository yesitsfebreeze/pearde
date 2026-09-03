Verdict: SPECCED

## What the build found

The seven (eight on `all`) sections were already toggled generically by
`view.js`'s `setView()` off `data-view`/`data-v`, and folds were already
opened generically off `details.fold` presence — the part of the PRD's
complaint that was *not* true any more. What was still true: `render.py`'s
`TEMPLATE` hand-wrote the header bar's seven `<a>` tags and the seven
`<section data-view=…>` wrappers as two separate HTML blocks that had to
move together with no check that they did, `view.js` named `"report"` and
`"boards"` by id in two blocks to decide what a merged (`all`) page drops,
and `viewtest.js` carried a hand-written `ORDER` array (two variants) and a
hard-coded "seven section anchors" count — three places a ninth section
would have needed a second and third edit, none of them checked against
each other.

**Built:** `render.py` now carries one `SECTIONS` list — id, nav title, the
payload band it reads, `folds:`, `only:` (which page shape shows it) and
`host:` (the selector proving it drew) — and generates both the nav bar and
the section wrappers from it, plus embeds it as `window.__SECTIONS__`.
`view.js` reads that table to decide the merged page's tab/section drop and
its landing section, instead of naming ids. `viewtest.js` derives its
expected order, its landing section, its first-paint host check and its
nav/section count check from the same table.

Confirmed on the example board: `viewtest.js --example` 49/49 (unchanged
from the pre-edit baseline, also 49/49), a merged page built the way
`all.py`/`serve.py` build one 50/50 (unchanged in shape from what the old
hard-coded logic produced — `report` dropped, `boards` shown, no door that
writes). Adding one stub row to `SECTIONS` — no other edit — raised both the
nav-anchor and section count from 8 to 9 and made `viewtest.js`'s "every
section drew on first load, no click" check fail on the stub until
something draws into the selector its own row names; this is
`prds/one-section-registry/probe/verify.sh`'s whole demonstration (10/10
with a `playwright-core` driver on `NODE_PATH`, 7/7 of the driver-free
checks without one).

The rendered markup is unchanged behaviourally — same attributes, same
content, generated rather than typed — which the identical pass counts
before and after are the proof of; the diff is structure only, per the
PRD's own "what stays out".

## Findings (not specced, not fixed)

- **A crash-safety lesson for `attempt-the-build`'s own atomic.** Building
  the stub-row demonstration meant swapping `render.py` for a mutated copy,
  rendering, and swapping back — a plain sequential `cp original → mutate →
  cp back` with no trap. The very first full run of `verify.sh` was killed
  mid-window by this session's own 2-minute default command timeout (three
  serial Chrome launches ran long), landing between the swap-in and the
  swap-back, and left this lane's real `resources/board/render.py` holding
  the stub row — read by every subsequent `import render` in this lane until
  it was noticed and hand-restored. `verify.sh` now takes a clean copy
  before the first mutation and restores it from a `trap … EXIT INT TERM`,
  not only a sequential `cp`. `@resources/workflows.py show attempt-the-build`'s
  own fails-table already has a similar row for a *reachable* mutation
  measuring itself; this is the same family (a footprint mutation left live
  across a kill) but the specific trigger — an outer harness timeout during
  a multi-browser-launch probe — is not in that table. Left for whoever
  next edits that atomic; not a file this PRD's footprint owns.
- **Two pre-existing `index.py check` lines, unrelated to this footprint,
  seen before and after this build with no change:** `resources/common.py is
  on disk with no row in references/files.md` and `references/files.md
  lists @resources/board/hotreload-test.js — not on disk`. Neither names a
  file this PRD touched or moved; not this PRD's to fix.
- No gap was found that `knowledge.py query` would have answered or that
  needed a fact from outside this repo — nothing was written to
  `.pearde/wiki/pending/` and nothing was `remember`ed.

## Specs

- `specs/spec01.md` — the registry, the generated bar/sections, and the
  registry-driven `view.js`/`viewtest.js` reads. complexity 18. Already
  built; every acceptance box is checked and cites the harness that proves
  it.

Footprint (union): `resources/board/render.py`, `resources/board/view.js`,
`resources/board/viewtest.js`.

**complexity: 18** — one cohesive change already built and verified across
three files that already existed; nothing left undefined.
**blast-radius: mid** — `render.py`/`view.js`/`viewtest.js` are the one
rendering path every board's page (and `all`'s merged page) goes through, so
a mistake here is felt everywhere, but the change is structure-only and the
before/after pass counts (49/49, 50/50) are the proof nothing moved.

## Scores

complexity: 18
blast-radius: mid
workflow: probe-then-spec
