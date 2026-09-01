# round — ⌘K search palette for the board view

Not a board round. A direct feature request from the user, worked in
`resources/board/`. No PRD, no state transitions. This file exists only to
hand the remaining verification to a fresh window.

## What was asked (four messages, in order)

1. "Command K shortcut where we can search all PRDs, states, memos, and
   everything via grep so we can list where we have a hit, navigate to it,
   and then when we press Enter we jump to that integration. Full search over
   everything, including the wiki on the board page"
2. "i want ctrl+k to search.. not just k — k does nothing right now, also
   restart the daemon"
3. "also allow grep and fuzzy search with the best matches first"
4. "also add a searchbar"
5. "in the search overlay we need to be able to filter by type — so if you
   only want to search for workflows, we can click Workflows only, like a
   multi-select, to be able to filter by kind or type"

All five are BUILT. Only the last one's browser probe has not been run.

## Established

- Three files carry the whole feature: `resources/board/serve.py` (the
  endpoint + ranking), `resources/board/view.js` (the palette),
  `resources/board/view.css` (its styles), plus one button in
  `resources/board/render.py`.
- The daemon re-execs on `PY_SOURCES` (serve/render/plan/edit/transitions.py)
  within ~2s of a save; `view.js`/`view.css` are served by stamp and need no
  restart. **`render.py` changes DO need the re-exec** — the shell is built
  in Python.
- The daemon's watch thread had been dead since 2026-08-31 (`is_board_dir`
  NameError caught mid-edit, traceback in `/private/tmp/pearde-serve.log`).
  Restarted; it is healthy now, pid varies. Restarted three times this
  session, most recently after the `kinds` filter landed.
- `viewtest.js` needs `NODE_PATH=/Users/feb/gstack/node_modules`.
- Boards on this machine: pearde, dotfiles, model, infra, shared, manola,
  racer-mi. Only pearde and dotfiles have content to search.

## Decided

- **Search is server-side, ranked there, rendered in the order it arrives.**
  The page never re-ranks. `GET /search?board=<b>&q=<text>[&kinds=<a,b>]`.
- **Three match modes, one box.** `re:<pat>` or `/<pat>` → regex (grep);
  anything else → literal substring per line, plus a fuzzy pass over file
  names only (never bodies — fuzzy over every line of a board is noise).
- **Two hard score tiers that cannot meet.** `LITERAL = 1000` floor for any
  literal/regex hit; fuzzy is banded `1..FUZZY_MAX (99)`. `KIND_RANK` (max
  60) only ever orders *within* a tier. Worst literal 1010 > best fuzzy 159.
  A fuzzy guess must never outrank a fact.
- **Fuzzy takes an initialism, refuses a scatter.** The span guard is waived
  when at least half the matched letters are word starts — otherwise
  `abcdef` over "alpha bravo charlie delta echo foxtrot" would be refused,
  which is the one abbreviation everybody types. Needles under 3 chars are
  refused outright. Brevity breaks ties (shorter name = better guess).
- **The `kinds` filter is applied on the daemon, before the 300-hit cap.**
  This is load-bearing, not a preference: `q=board` finds 24 workflow hits
  behind 4,400 others — filtering a truncated list in the page would make
  them unreachable. `counts` in the response always covers every kind found,
  filter or no filter, so the chips keep saying what is there.
- **`README.md` is excluded from the walk** — it is an index of links, so it
  matched everything and drowned the real hits.
- **Jump by kind:** prd/spec → inspector (`go({prd: rel})`); memo → memos
  view, scrolled to and flashed; anything the vault holds (wiki, workflow,
  report, settings, vision, graphify notes) → `obsidian://open?vault=<id>&
  file=<path>`, vault id looked up in Obsidian's own register by exact path
  (same lookup `statusline.sh` does).
- **`window.open(uri)`, not `location.href`** — headless Chrome silently
  no-ops an external scheme via `location.href`; `window.open` fires it.
  This is also how the probe detects the jump (a popup event with an empty
  URL).
- **Keys:** ⌘K / ctrl-K opens from anywhere *including out of another input*
  (bound above the INPUT/TEXTAREA guard — that placement is the whole point
  of a palette). Shift-K also opens. Lowercase `k` still walks rows,
  untouched.

## Edits made (all on disk, all syntax-checked)

`resources/board/serve.py`
- `vault_uri()` — obsidian URI for one note, by exact-path vault lookup.
- `KIND_RANK`, `LITERAL`, `FUZZY_MAX`, `score_line()`, `fuzzy()` — the
  ranker, sitting just above `board_json()`.
- `GET /search` — the walk, the three modes, `kinds` filter, `counts`.
- `/search` added to the `ROUTES` tuple and to the module docstring's API list.
- `cmd_selfcheck()` + `serve.py selfcheck` verb — asserts the tier
  separation and the fuzzy accept/refuse set. **11 checks, all passing.**

`resources/board/view.js`
- ⌘K/ctrl-K binding above the input guard; `K` in the plain-key block.
- The `ksBuild/ksShow/ksClose/ksRun/ksMark/ksDraw/ksJump` block plus
  `ksKindsDraw()`, after `drawMemos()`.
- `ksKinds` Set + `ksCounts` + `KIND_ORDER`; ⌥←/→ steps the filter.
- `$("ksopen").onclick` next to `$("newprd").onclick`.

`resources/board/view.css` — the `#ks` overlay, `.ks-chip` row, `#ksopen`
searchbar, `.memo.flash`. All from existing tokens; no new hue (the sheet's
rule 2/3).

`resources/board/render.py` — `#ksopen` button in `#titlebar .right`.

## Verified (all green)

- `serve.py selfcheck` — 11/11.
- `viewtest.js` against the served board — 45/45.
- `viewtest.js --example` — 45/45.
- Palette probe, 16 checks: searchbar opens it, ⌘K, ctrl-K, ⌘K from inside
  another input, hits render, literal-above-fuzzy ordering, best hit is a
  PRD/memo not a graph note, hint counts, `/regex` and `re:` modes, bad
  pattern reports itself, misspelling finds by name, match lit in the line.
- Jump probe, 7 checks: arrows, Enter, prd→inspector, memo→memos+flash,
  wiki→vault popup, lowercase `k` still walks rows.

## Owed — the one thing left

Run the kind-filter probe and fix whatever it finds:

    node /private/tmp/claude-501/-Users-feb-dev-infra-pearde/ca1fce64-00b3-49a3-81db-b0e74645a5d5/scratchpad/kskinds.js

It is written and unrun (the window hit its ceiling as it was invoked). 14
checks: chips render one per kind found with counts, `all` lit by default,
click filters, chip lights, `all` darkens, counts still name every kind,
hint says the filter is on, a second kind ADDS (multi-select), clicking a lit
chip turns it off, a rare kind survives the cap, `all` clears, the filter
survives close+reopen, an empty filtered result explains itself and offers
the way back, ⌥→ steps from the keyboard.

The server half of that probe is already confirmed by hand:
`q=board` → counts `{board:2075, spec:1203, prd:1151, wiki:450, memo:121,
workflow:24, report:1}`; `&kinds=workflow` → 24 hits, all workflow, counts
still full; `&kinds=memo,wiki` → 571 hits, exactly those two kinds. So any
failure is in the page, not the endpoint.

Then re-run the three regression suites above (they were green before the
chips landed) and report to the user.

Scratch probes live in that same scratchpad dir: `ks.js` (palette),
`ksjump.js` (jumps), `kskinds.js` (filter), `fz.py` (superseded by
`serve.py selfcheck`).

## Asked

Nothing outstanding with the user.
