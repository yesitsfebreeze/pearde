---
complexity: 9
workflow: probe-then-spec
footprint:
  - resources/board/view.js
  - resources/board/view.css
---

# spec01 — a kanban card is keyboard-reachable, and the answered panel's reopen button is not only findable by hovering

**All of it already stands in the tree, uncommitted.** The implementer's job
is to read it, run the probe, and tick each box against what it printed.

## What already stands

- **The kanban card** (`resources/board/view.js`, `PeardeBoard.card()`) now
  carries `tabindex="0"`, `role="button"` and an `aria-label` naming the
  write ("… — open to move or edit, currently <state>") whenever
  `this.served` — the same flag already gating `draggable` and the `.start`
  button on this element, so the read-only `all` page's copy of this
  component renders none of it and gains no new stop a Tab reaches. A
  `@keydown` handler opens the drawer on Enter/Space (checked against
  `e.target === e.currentTarget` so the nested `.start` button's own native
  Enter/Space does not also fire it, and `stopPropagation`ed so the window's
  global `Enter` shortcut for the timeline's own selection does not also
  fire). `view.css` adds `.card:focus-visible` mirroring the visual lift
  `.card:hover` already gives — the global `:focus-visible{outline:…}` rule
  (view.css:150) already supplies the ring; this only matches the card's own
  shape to it.
- Drag has no keyboard equivalent of its own and needs none: activating the
  now-focusable card opens the same drawer a click already does, and that
  drawer already carries a real `<select id="dstate">` (`view.js:2881`,
  pre-existing) listing every state — the "move menu" the PRD's `## The
  change` asks for. It now carries `aria-label="state — writes this PRD's
  state"` so it names itself to a reader who lands on it directly, not only
  one who read down from the `<h4>state</h4>` beside it.
- **The answered panel's `reopen` button** (`#answered .areopen`,
  `view.css`) used `visibility:hidden` before `:hover` — but a hidden
  element cannot receive focus, and its only ancestor, `.adone`, is a plain
  `<div>` with nothing else inside it that could ever gain focus first and
  trigger a `:focus-within` reveal. No sequence of Tab presses could ever
  have reached this button; `:hover`-only and `:focus`-only were both dead
  ends built the same way. The fix swaps `visibility` for `opacity` (which
  does not remove an element from the tab order) and reveals it on
  `:focus-visible` as well as `:hover`, plus `@media (hover:none)` for touch
  — the same breakpoint `#vrail` already uses two hundred lines up, not a
  second one.
- The static, unserved render (the shape the read-only `all` page shares)
  was directly compared against the same page with `served` forced true —
  the unserved copy has zero tabbable cards; only the served one does.

## What is left to finish

Nothing to build. Land the two files as they stand and keep
`.pearde/prds/write-affordances-on-focus/probe/keyboard-affordances.js` as
the regression check — it is pass one's own evidence, not throwaway.

## Findings for whoever reads this next (not acted on here — out of footprint)

- The PRD's own source doc names "＋ to open a PRD" as a third hover-gated
  affordance. It is not: `#newprd` (`render.py:404`) is a plain, always-
  visible `<button>`, never hover-gated in `view.css`, and was already fully
  keyboard-operable before this PRD. The doc's claim is stale or was never
  quite accurate; nothing here changes it.
- The ask view's own submit (`.qq .qsend`, the picks and the own-answer
  textarea) is likewise never hover-gated — `display:none` toggles it on
  `.qq.answered`, not on hover. Also already fine.
- `.adone` (the settled-answer row that opens a PRD) is a `<div
  data-go=…>`, not a button — its own comment even calls it "the door to
  that PRD" — so it is not Tab-reachable at all. This is a *read* affordance
  (it navigates, it writes nothing), so it sits outside this PRD's "every
  write affordance" contract; flagged for whoever owns read-navigation
  reachability next.
- Running this PRD's own probe cost most of a build cycle to a harness bug
  worth naming for the board generally: this lane has no `.pearde` of its
  own (the parked PRD on a lane missing the symlink), so the analyst working
  it symlinked `.pearde` onto the orchestrator's own board to reach the PRD
  contract at all. Any later script under `.pearde/prds/*/probe/` that
  builds its own paths from `__dirname` then resolves — silently, via that
  symlink — back onto the orchestrator's checkout, not the lane, because
  Node resolves `__dirname` against the real path. The probe here works
  around it by resolving from `process.cwd()` instead and documents the
  trap in its own header; the general fix belongs to the parked PRD, not
  here.

## Acceptance

- [ ] On the unserved (read-only) render, no `.card` carries a `tabindex`
      attribute — the `all` page's copy of this component gains nothing.
- [ ] Once `served` is true, every `.card` carries `tabindex="0"`,
      `role="button"` and an `aria-label` containing the PRD's title and its
      current state.
- [ ] A Tab walkthrough from the top of the page reaches a served card.
- [ ] The focused card matches `:focus-visible` (a real, visible focus
      indicator, not only a property flag).
- [ ] Pressing Enter on a focused card opens the drawer.
- [ ] Pressing Enter on a focused card does **not** change which column
      (state) the card is in — the guard from the PRD's `## Fails when`.
- [ ] `#dstate` inside the drawer carries an `aria-label` naming the write.
- [ ] `#answered .areopen` can receive focus via `.focus()` even before any
      hover or click — the old `visibility:hidden` bug, reproduced with a
      markup fixture since the example board ships no answered question.
- [ ] `#answered .areopen` is visually de-emphasised (`opacity:0`) until
      hovered or focused, and plainly visible under `(hover:none)`.
- [ ] `node --check resources/board/view.js` — compiles.
- [ ] `node resources/board/viewtest.js --example` — the committed harness,
      49/49, no new failure.

## Verify and Proof

```sh
# from the repo root (or the lane's own copy)
node --check resources/board/view.js && echo "resources/board/view.js compiles"
node resources/board/viewtest.js --example
cd resources/board && npm i playwright-core   # once, if not already present
node ../../.pearde/prds/write-affordances-on-focus/probe/keyboard-affordances.js
```
