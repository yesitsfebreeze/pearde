# The `all` board

Every board this machine watches, on one page.

```sh
pearde view                       # register this board, as always
open http://127.0.0.1:8443/board/all
```

`all` is not a board. Nothing of it is on disk: no `.pearde/`, no
`settings.md`, no PRD of its own, no plan file, no watch entry. It is one
render over every board the live service is watching, built fresh on each
request out of those boards' own payloads and thrown away again. Registering a
board is the whole of joining it — **the watch set is the configuration**, and
there is no file naming what it merges.

**It is a display, not a plan.** Nothing writes back through it. `/edit`,
`/new`, `/report` and `/run` answer `409` when the board named is `all`, and
the page offers no door that would call them: no `＋ PRD`, no save, no drag
between columns, no answer box. Every row is addressed `@<board>/<rel>`, so
the one thing a click can do is take the reader to the board that owns it.

A pass is rendered here as what it asks — the fork, the three answers as a
marked list with the recommended one filled — and carries no radio, no
own-answer box, no submit, and no `reopen` on the answered panel beside it. A
disabled control is indistinguishable from a live one: the reader picks,
nothing moves, and the page reads as broken rather than as read-only. In the
cards and in the inspector alike the foot is the door — *answered on its own
board*. `viewtest.js` pointed at `/board/all` asserts it.

**It is not a master board.** The two answer different questions and neither
replaces the other:

| | master (@references/parts/master.md) | `all` |
|---|---|---|
| what it is | a board — its own PRDs, memos, commits | a page |
| what names the set | `members:` in its `settings.md` | whatever is registered |
| what it computes | one merged schedule and one critical path across the members | nothing. Each board's own plan, laid side by side |
| who works it | one orchestrator, dispatching across the group | nobody. It is read |
| where a PRD is written | the member's own `prd.md` | nowhere — the door is the board |

A master board appears on `all` like any other board, showing its own PRDs —
the ones spanning members. Its members appear as themselves, because
registering a master registers every member as a board in its own right.

## What it merges

@resources/board/all.py, one function per line of this list:

- **Each board's own PRDs.** A master's payload also carries its members', and
  those members are registered boards, so counting both would print every
  member PRD twice. A row carrying a `board` is dropped there and picked up
  from the member itself. The rule and the promise are the same sentence:
  `all` shows the boards the daemon watches, and a member nobody watches is
  not one of them.
- **Addresses**, qualified `@<board key>/<rel>` — the master board's own form,
  which the view already groups, colours and folds by. The key is the
  `/board/<key>` key, so every row on this page names the page it came from.
- **`needs` inside a board**, qualified with it. One pointing across a board
  boundary is dropped: `all` draws no edge it did not compute, and the one
  place such an edge is real is the master that declared it.
- **The counts, the burn-down and the transitions**, summed. One row a day per
  board becomes one row a day.
- **The memos**, slugged `@<board>/<slug>`, and **the answers**, both fanned
  out over every board.
- **Search** (⌘K) runs the same walk over every board and the scores compete
  in one list — one box for the whole machine. A hit's path carries its board,
  because two boards both have a `settings.md`.

Nothing else is merged, and two things are deliberately absent:

- **No report.** A report is one board's state written for a person
  (@references/skills/pearde-report.md). Several boards have several, and
  picking one would be a lie about the rest. The `report` tab is not on this
  page and `/report?board=all` answers `null`.
- **No real hours.** Weight prints as tuned hours off a fit made per board
  (@references/parts/order.md), and two fits cannot both be the axis. Boards
  that agree keep theirs; boards that disagree print raw weight units, which
  is the one number that means the same thing on every board here.

## What it draws

The same page, with one section added and one taken away.

| # | section | on `all` |
|---|---------|----------|
| — | **boards** | new, and what the page opens on: one card per board — its name, its purpose, the spread of its states, and the counts as doors |
| 2 | **timeline** | every board's rows on one axis, each board's chain laid from the same zero. Group by board is one click; a board is a branch in `tree` |
| 3 | **board** | kanban over the lot. Cards carry their board's chip; drag is off |
| 5 | **asks** | every question on the machine, in one wall, rendered as its own pass and disabled — read here, answered on its board |
| 8 | **report** | absent |

A board's card carries four doors: the name goes to that board's own page,
`to collect` to the timeline's collect filter, `waiting on you` and `in flight`
to the list filtered to that board and that band. A board that will not read
says so in its own row rather than taking the page down with it.

## The mechanics

- The key `all` is reserved. A real board that would key that way is suffixed
  `-board` by `register()` — the page is not a board's to take.
- `/` redirects to `all` when more than one board is registered, to the one
  board when there is one, and to a master when one is registered — a master
  carries a merged plan, which is more than a display.
- `/wait?board=all` sleeps like any board's: every bump on a real board bumps
  `all` too, and so does a board joining or leaving the watch set. A page open
  on `all` moves within about a second of a file changing on any of them.
- `/sync` with `board: all` forces a pass on every board it draws.
- `all` has no `view.user.css` or `view.user.js`. Those belong to a board, and
  this page is over all of them.

```sh
python3 @resources/board/all.py <board>…          # the dashboard, as text
python3 @resources/board/all.py --json <board>…   # the merged payload
```

The text form is the same rows the page draws, for a check that has no
browser. `node @resources/board/viewtest.js http://127.0.0.1:8443/board/all`
is the page's own gate — it reads `virtual` off the payload and asserts the
merged page's shape, the dashboard's rows, and that no door on it writes.
