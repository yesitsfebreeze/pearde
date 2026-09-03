---
state: done
origin: requested
priority: 45
complexity: 9
blast-radius: mid
workflow: probe-then-spec
actual: 0.14h
commit: ccd21c6 a267e4a
---

# Write affordances on focus

*Source: `docs/content/docs/improvements/view-write-affordances.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** view · **Axis:** usability (6 → 7) · **Pulls the score up by
~3 points**

## Why now

The board view writes through affordances: drag a card to write `state:`,
＋ to open a PRD, the ask cards' submit to answer a question. All three are
hover-revealed — a keyboard or touch reader, or anyone who does not happen
to rest the pointer, sees a read-only page and concludes the view is one.
The view's contract is "how a person reads *and works* the board"; the
working half is currently undocumented by the interface itself.

## The change

Focus reveals the affordance: a card or panel receiving keyboard focus
shows the same handles a hover shows, and the handles carry a visible
`aria-label` naming the write ("move to in-review", "answer this ask").
Drag stays pointer-only — keyboard gets an equivalent move menu on the same
handles, the way the asks view already offers picks and an own-answer box.

## Done when

- Tabbing through the board view reaches every write affordance without a
  pointer, and each announces what it writes.
- The touch path opens the same handles a pointer hover does — one
  breakpoint, no second rule.
- The read-only `all` page gains nothing: it is read-only end to end, and
  this page must not give it a write affordance to grey out.

## Fails when

- The keyboard path writes on focus rather than on activate — a Tab becomes
  a state move. Guard: handles activate on Enter/Space, like every other
  button; the check is a focus walkthrough that ends with the board
  unchanged.

## What stays out

No new write route, no undo. The writes go through the same endpoints the
drags use today; only their visibility moves.

## Blocked

**2026-09-03 18:46 — the lane will not rebase**

`lane/write-affordances-on-focus` does not land on `session/s34612`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/write-affordances-on-focus` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock write-affordances-on-focus`.

## Report

spec01: exit 0
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
  ok    unserved render: board has cards  (8)
  ok    unserved render: no card is tabbable (bullet 3 — `all` gains nothing)  (0)
  ok    served render: a card is now tabbable  (big)
  ok    Tab walkthrough reaches the served card
  ok    the card's aria-label names the write  (big — a parent whose work is in its children — open to move or edit, currently open)
  ok    the focused card matches :focus-visible
  ok    Enter opened the drawer
  ok    Enter did not write `state:` — a focus walkthrough ends with the board unchanged  (open → open)
  ok    reopen is focusable at all (the old `visibility:hidden` bug)
  ok    reopen starts de-emphasised (opacity 0)  (0)
  ok    focusing it reveals it the way hover does (opacity 1)  (1)
  ok    no page error  ()

probe: all checks passed
  ok    every served card carries role=button  (8/8)
  ok    every served card carries tabindex=0  (8/8)
  ok    every served card's aria-label names title and state  (8/8)
  ok    #dstate carries an aria-label naming the write  (state — writes this PRD's state)
  ok    #dstate is the move menu — it lists every state  (9)
  ok    the touch context really has no hover
  ok    with a pointer, reopen starts hidden  (0)
  ok    under (hover:none) reopen is plainly visible  (1)

extra: all checks passed
