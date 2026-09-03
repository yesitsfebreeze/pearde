---
complexity: 18
footprint:
  - resources/board/render.py
  - resources/board/view.js
  - resources/board/viewtest.js
---

# spec01 — one section registry drives the bar, the sections and the tests

**Already built, in the footprint files, uncommitted.** `render.py` gains a
`SECTIONS` list — id, nav title, the band of the enriched payload it reads,
`folds:`, `only:` (`None`/`"virtual"`/`"real"`, which of the two page shapes
shows it) and `host:` (the CSS selector proving it drew). `_nav_html()` and
`_sections_html()` generate the header bar's `<a>` tags and the
`<section data-view=…>` wrappers from that one list — replacing two
hand-written HTML blocks that had to be edited together and nothing checked
that they were. The registry is also embedded as `window.__SECTIONS__`
alongside `window.__PAYLOAD__`, the same hand-off pattern already used for
the enriched payload.

`view.js` reads `window.__SECTIONS__` to decide, on a merged (`all`) page,
which tab and section to drop for the other page shape — replacing a block
that named `"report"`/`"boards"` by id — and to pick the merged page's
landing section (`defaultVirtual`), replacing the hard-coded `setView("boards")`.

`viewtest.js` derives its expected section order, its default landing
section, its "every section drew" check and its nav/section count check from
`window.__SECTIONS__`, replacing a hand-written `ORDER` array (two variants,
real and virtual), a hard-coded host-selector list and a hard-coded "seven".

No markup a person sees changed: the rendered `<a>`/`<section>` elements
carry the same attributes and content as before, generated rather than
typed, confirmed byte-for-byte behaviourally by `viewtest.js` passing
unchanged (49/49 on the example board, 50/50 on a merged page built the same
way `all.py`/`serve.py` build one).

## Acceptance

- [x] `python3 resources/board/render.py`'s `SECTIONS` list is the only place
      a section's id is declared for render.py's own markup — `_nav_html()`
      and `_sections_html()` build the bar and the section wrappers from it,
      and nothing else in `render.py` spells `"boards"`, `"timeline"`,
      `"board"`, `"analytics"`, `"asks"`, `"list"`, `"memos"` or `"report"`
      outside that list.
- [x] `grep -c '<section data-view=' <a rendered page>` equals
      `len(render.SECTIONS)`, and so does the nav bar's `<a href="#view=`
      count — proven in `prds/one-section-registry/probe/verify.sh`, §1.
- [x] Adding one row to `SECTIONS` — no edit anywhere else — raises both of
      those counts by one on the next render, and `viewtest.js`'s "every
      section drew on first load, no click" check fails on the added row
      (an un-rendered stub host) until something draws into the selector its
      row names — proven in `verify.sh`, §2 and §3 (`viewtest.js`'s own run
      against a stubbed `render.py`, `FAIL every section drew on first load,
      no click — empty frames: stub`).
- [x] ⌘1–7 and `#view=` routing still come from the bar's own `<a>` elements
      (`view.js`'s existing `setView`/keydown handlers, unchanged) — since
      those elements are now generated from the registry, the keyboard map
      and the URL fragments are provably the same table as the bar, not a
      separately maintained one.
- [x] `all`'s merged page still shows `boards` and hides `report`, and a
      single board's own page still shows `report` and hides `boards` — both
      now decided by `view.js` reading `SECTIONS[].only` against the page's
      own `virtual` flag, rather than two blocks each naming a section by
      id. `viewtest.js` against a merged page still shows 50/50, including
      "the merged page offers no door that writes" and "the merged page
      draws a row per board".
- [x] `node resources/board/viewtest.js --example` passes with no change in
      count from before this PRD's build (49/49, matching the pre-edit
      baseline taken on this same tree before any file here was touched).

## Verify and Proof

```sh
bash prds/one-section-registry/probe/verify.sh
# with a playwright-core driver reachable (NODE_PATH=<dir with playwright-core>):
#   10/10 passed, 0 skipped
# without one, the three viewtest-dependent checks report `skip`, not `FAIL`,
# and the remaining 7 (the registry/render checks that need no browser) still
# have to pass.
```
