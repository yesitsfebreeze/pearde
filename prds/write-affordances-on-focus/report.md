Verdict: SPECCED

# write-affordances-on-focus — report

Workflow followed: `probe-then-spec`.

## What was built (pass one, left uncommitted in the lane)

- `resources/board/view.js`: `PeardeBoard.card()` — the kanban card is now
  `tabindex="0"`, `role="button"`, and carries an `aria-label` naming the
  write, gated on `this.served` (the same flag already gating `draggable`
  and the `.start` button). Enter/Space on the card opens the drawer, which
  already carries a real `<select id="dstate">` listing every state — the
  "move menu" the PRD's `## The change` asks for; it now has its own
  `aria-label` too.
- `resources/board/view.css`: `.card:focus-visible` mirrors `.card:hover`'s
  lift. `#answered .areopen` (the reopen-a-settled-answer button) switched
  from `visibility:hidden` to `opacity:0`, revealed on `:hover`,
  `:focus-visible`, and `(hover:none)` — the same breakpoint `#vrail`
  already uses.
- Both changes verified against a real Chrome via
  `.pearde/prds/write-affordances-on-focus/probe/keyboard-affordances.js`
  (left in the tree, not a committed harness) and against the existing
  `viewtest.js --example` (49/49, no regression) and `node --check`.

## An incident worth flagging

While reviewing my own spec I ran `python3 resources/pearde.py specced
write-affordances-on-focus` to see what it would say — I had taken it for a
read-only check. It is not: it validated the spec, wrote `complexity: 9`,
`workflow: probe-then-spec` into `prd.md`'s frontmatter, set `state:
specced`, and released the `an-write-affordances-on` claim, all before this
report existed. It is the same function `collect.py` calls internally on a
SPECCED verdict, so the values it wrote match this report's own `## Scores`
below — but the transition happened ahead of `collect` reading a verdict,
which is not the order this board's contract describes. `blast-radius` was
not touched (I passed no `--blast`) and is still blank, as it was in the
PRD's original frontmatter before I touched anything. Flagging this so
whoever reads the board next knows the state already moved and the claim is
already free, rather than being surprised by either.

## Findings (not acted on — outside this PRD's footprint)

- The source doc names "＋ to open a PRD" as a hover-gated affordance. It is
  not, and never was in the code: `#newprd` (`render.py:404`) is a plain,
  always-visible `<button>`, already fully keyboard-operable. The doc's
  claim is stale.
- The ask view's own submit and picks are likewise never hover-gated —
  already fine, contrary to the doc's grouping of it with the other two.
- `#answered .adone` (the row that opens a settled answer's PRD) is a
  `<div data-go=…>`, not a button, so it is not Tab-reachable — but that is
  a *read* affordance (navigation), not a write, so it sits outside this
  PRD's "every write affordance" contract.
- `resources/knowledge.py query` on this PRD's contract returned no
  relevant hits (only unrelated high-scoring matches from other topics) but
  did not auto-enqueue a pending gap — the tool read it as 103 "strong"
  hits rather than a miss. Not a question of my own to ask; noted since the
  brief says a gap should show up in `.pearde/wiki/pending/` and none did.
- `__dirname`-relative paths in a script under `.pearde/prds/*/probe/`
  resolve, in a lane, through the compatibility symlink back onto the
  *orchestrator's* checkout, not the lane — cost most of a build cycle
  before the probe was rewritten to resolve from `process.cwd()` instead.
  Detailed in spec01's own findings section; the general fix belongs to the
  parked PRD on a lane missing its own `.pearde`, not here.

## Specs

- `specs/spec01.md` — the whole build above, one implementable unit,
  complexity 9, footprint `resources/board/view.js`,
  `resources/board/view.css`.

## Scores

complexity: 9
blast-radius: mid
workflow: probe-then-spec
