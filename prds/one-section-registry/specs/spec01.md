---
complexity: 18
footprint:
  - resources/board/render.py
  - resources/board/view.js
  - resources/board/viewtest.js
  - .pearde/prds/one-page-that-says-whats-up/probe/verify.sh
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

- [x] `render.py`'s `SECTIONS` list is the only place a section's id is
      declared for render.py's own markup — `_nav_html()` and
      `_sections_html()` build the bar and the section wrappers from it, and
      with the `SECTIONS` block cut out of the file the only remaining
      `data-v=`, `data-view=` and `#view=` in it are the two format strings
      inside those two generators and one line of the registry's own comment.
      No `<a>` and no `<section>` is typed by hand anywhere. Four section
      *words* do remain outside the list and none of them declares a section:
      `p["board"]` (a payload key), `aria-label="boards"` on the board picker,
      `title="list"` on a mode button, and one `data-go='{"view":"report"}'`
      door into the report section, which `view.js` removes beside that
      section on a merged page.
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
- [x] `prds/one-page-that-says-whats-up/probe/verify.sh` is back at its
      pre-edit count. Four of its checks greped the hand-typed markup out of
      `render.py`'s **source** — the anchor count, the anchor/section id sets,
      the toolbar's place inside the timeline section, and the count of
      folding archives — which the generator removes from that source. Each is
      re-aimed at the page `render.py` writes (`TEMPLATE` with `_nav_html()`
      and `_sections_html()` substituted), asserting the same rule one level
      later, and each still fails on the mutation it exists to catch: a fourth
      `folds: True` row, a hand-written `<a href="#view=ghost">` put back into
      `TEMPLATE`, and `#tcontrols` moved out of the timeline section.

## Verify and Proof

```sh
# the tree under test: the lane its worker built in when one is named, the
# code repo otherwise — and the board beside it, which is where the harnesses
# live. Both resolve from either root, so this block runs the same way by hand
# and under `collect`.
ROOT="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"
if [ -d "$ROOT/.pearde/prds" ]; then BOARD="$ROOT/.pearde"; else BOARD="$(cd "$ROOT/../.." && pwd)"; fi

# this unit's own harness. With a playwright-core driver on NODE_PATH it
# prints `10/10 passed, 0 skipped`; without one the three viewtest-dependent
# checks report `skip`, not `FAIL`, and the remaining seven — the registry and
# render checks, which need no browser — still have to pass. Its own last line
# is `[ "$fail" -eq 0 ]`, so its exit is the assertion and no total is nailed
# down here.
PEARDE_ROOT="$ROOT" bash "$BOARD/prds/one-section-registry/probe/verify.sh"

# the harness this spec re-aims, back at its own pre-edit count: the four
# source-greps that the generator obsoleted now read the generated page. Its
# other failures are inherited (a lane carries no `.pearde/report.md`), so
# this gates on the four names, not on the harness's total.
out="$(PEARDE_ROOT="$ROOT" bash "$BOARD/prds/one-page-that-says-whats-up/probe/verify.sh" 2>&1 || true)"
printf '%s\n' "$out" | tail -1
if printf '%s\n' "$out" | grep -E '^FAIL: (the plan toolbar is inside|the bar is seven anchors|every anchor has the view|the three archives fold)'; then exit 1; fi
```
