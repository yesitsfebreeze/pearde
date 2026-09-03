---
state: done
origin: requested
priority: 26
complexity: 14
blast-radius: mid
workflow: probe-then-spec
actual: 0.98h
---

# The ranking renders beside the view

*Source: `docs/content/docs/improvements/health-html-ranking.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** health · **Axis:** usability (7 → 8) · **Pulls the score up by
~3 points**

## Why now

The ranking is markdown read raw: every note's frontmatter carries eight
measured numbers (score, lines, branching, nesting, longest, fan_out,
fan_in, links), and a reader decodes them against the thresholds — which
live in the reference, not the output. The view already serves the board's
files at a stable URL with live reload; health renders nothing there, so
the one page a person keeps open about *what resists being worked* is the
one decoded by eye.

## The change

The view gains the ranking: a read-only section rendering
`.pearde/health/ranking.md`'s table — score, file, worst axis — with the
note's numbers shown against their thresholds (the two lines that are the
line, colored by side). Rendered through the same payload service, section
registry row, no second daemon, no new port. Gitignored like every other
view input, and doctor's health row unchanged — the regenerable record
stays the one truth.

## Done when

- `pearde view` on a scored board shows the ranking as a table, worst
  first, each row's numbers beside their thresholds.
- The section renders nothing (one line, `not scored`) on a board with no
  health record — the same shape the now strip's dimmed doors keep.
- The service serves it from the same payload — no second fetch, no
  watcher: the record regenerates and the swap-in-place keeps it current
  within the second the page already promises.

## Fails when

- The section reads health notes *at render* per request — a 60-file board
  is 60 reads per paint. Guard: the payload is the ranking file's parsed
  table only; notes are fetched on click, the way the prose section opens
  the plan.

## What stays out

No re-scoring on view, no write affordance — the record is regenerable by
its one command, and the view stays a renderer, never an author.

## Report

spec01: exit 0
resources/board/view.js compiles

up to date, audited 2 packages in 682ms

found 0 vulnerabilities
  ok    no page error
  ok    Lit is bound, offline
  ok    the payload is on window, enriched
  ok    live refresh hook wired
  ok    live apply hook wired
  ok    hold hook still wired
  ok    the toolbar built
  ok    eight section anchors  (got 8)
  ok    the canvas is sized
  ok    the gantt drew  (1125 draw ops)
  ok    the frontier column built
  ok    the frontier is a component
  ok    it renders into light DOM
  ok    its rows are doors  (5 doors)
  ok    the stats bar has numbers
  ok    the inspector exists
  ok    the sections are in the PRD's order  (timeline board analytics health asks list memos report)
  ok    exactly one section is visible on load  (timeline)
  ok    every section drew on first load, no click
  ok    the timeline's legend drew
  ok    the state panel holds the doors, the prose and the vision line
  ok    the plan's footer strip is inside the plan's section
  ok    the focus tab is too
  ok    at 390px the page does not scroll sideways  (body 390 vs client 390 — div#spacer)
  ok    N opens the new-PRD modal with its editor toolbar
  ok    the theme switch pins a theme and a cycle releases it  (system → dark → system)
  ok    section "timeline" is the one shown
  ok    section "board" is the one shown
  ok    the board view fits the viewport
  ok    section "analytics" is the one shown
  ok    section "health" is the one shown
  ok    section "asks" is the one shown
  ok    no ask card failed to read its PRD  (0 of 1)
  ok    no card renders a pass with no options  (0 of 1 cards carry picks)
  ok    a parsed pass has no bulk submit  (0 cards)
  ok    every question carries its own reopen
  ok    an unaskable card says so instead of dumping the body  (0 cards)
  ok    every open question has its own submit
  ok    an answered question has left the inbox
  ok    the answered panel built  (0 answered)
  ok    the answered panel is in date order  (0 out of order)
  ok    a board's own passes are answerable  (0 read-only pass(es))
  ok    an answered question can be taken back  (0 of 0)
  ok    section "list" is the one shown
  ok    section "memos" is the one shown
  ok    section "report" is the one shown
  ok    a resize behind the plan does not squash the plot  (default · spacer 1156 vs plot 757)
  ok    zooming out stops at the whole track  (−25 → 1105, fit all → 1105, plot 1097)
  ok    fit all puts every row on the screen  (world 273, plot 847)
  ok    the plan does not animate its way to width on load  (1 step(s) over 91 frames · 1381/2110 → 1381/2110)

50/50 passed
scored: 40 189
