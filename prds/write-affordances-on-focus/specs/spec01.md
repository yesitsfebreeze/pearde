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

**Pass one's build did not survive.** "Already stands in the tree" was true
when this was written and was gone by the time an implementer read it: a
concurrent `collect` reset the checkout at ~17:50, and the hunks were in no
commit, no stash and no dangling blob (`git fsck --lost-found` searched for
`open to move or edit`, `tabindex="0"` and `.card:focus-visible`; nothing).
Pass two rebuilt both files from the description above, which was complete
enough to do it from — read this section as the record of what was rebuilt,
not as a claim that nothing was.

Two details of that description were off, and the rebuild follows the file:
`#vrail` uses `@media (hover:hover)` (view.css:443), not `(hover:none)`, and
it is ~820 lines up, not two hundred — `(hover:none)` is its complement, a
new query rather than a reused one. And `#answered .areopen` reveals on
`:focus`, not `:focus-visible`: a pointer that focuses this button is
already hovering it, so there is nothing to withhold, and a programmatic
focus must reveal it too — under `:focus-visible` alone the reveal depends
on Chrome's last-input-modality heuristic and the probe's own box reads 0.
The card keeps `:focus-visible`, where a mouse-down would otherwise leave
the lift stuck on.

Keep both files under `probe/` as the regression check — they are pass one's
and pass two's own evidence, not throwaway.
`keyboard-affordances.js` is pass one's; `extra-affordances.js` covers the
three boxes it does not reach (`role="button"` on every served card,
`#dstate`'s `aria-label`, and the `(hover:none)` reveal, which needs
Chromium's mobile emulation — an `Emulation.setEmulatedMedia` `hover`
feature alone does not flip `matchMedia("(hover:none)")`, measured).

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

- [x] On the unserved (read-only) render, no `.card` carries a `tabindex`
      attribute — the `all` page's copy of this component gains nothing.
- [x] Once `served` is true, every `.card` carries `tabindex="0"`,
      `role="button"` and an `aria-label` containing the PRD's title and its
      current state.
- [x] A Tab walkthrough from the top of the page reaches a served card.
- [x] The focused card matches `:focus-visible` (a real, visible focus
      indicator, not only a property flag).
- [x] Pressing Enter on a focused card opens the drawer.
- [x] Pressing Enter on a focused card does **not** change which column
      (state) the card is in — the guard from the PRD's `## Fails when`.
- [x] `#dstate` inside the drawer carries an `aria-label` naming the write.
- [x] `#answered .areopen` can receive focus via `.focus()` even before any
      hover or click — the old `visibility:hidden` bug, reproduced with a
      markup fixture since the example board ships no answered question.
- [x] `#answered .areopen` is visually de-emphasised (`opacity:0`) until
      hovered or focused, and plainly visible under `(hover:none)`.
- [x] `node --check resources/board/view.js` — compiles.
- [x] `node resources/board/viewtest.js --example` — the committed harness,
      49/49, no new failure.

## Verify and Proof

```sh
# `collect` runs this from the PRD's `repo:` root — the checkout, or the lane
# that is a worktree of it. Both need `playwright-core` in resources/board and
# a Chrome on the machine: `npm i playwright-core` there is one-time setup,
# not a gate, so it is not run here — an install inside a verify block hits
# the network on every collect and dirties the tree the collect then reads.
node --check resources/board/view.js

# the committed harness. Its exit code is the gate, never a literal total: a
# later PRD adding a check must not redden this spec.
node resources/board/viewtest.js --example

# the affordances themselves, in the two footprint files. These go red the
# moment the work is reverted, whatever a browser is or is not able to say.
grep -q 'tabindex=${this.served ? "0" : nothing}' resources/board/view.js
grep -q 'role=${this.served ? "button" : nothing}' resources/board/view.js
grep -q 'open to move or edit, currently' resources/board/view.js
grep -q 'aria-label="state — writes this PRD' resources/board/view.js
grep -q '^.card:hover,.card:focus-visible{' resources/board/view.css
grep -q 'cursor:pointer;opacity:0}' resources/board/view.css
grep -q '@media (hover:none){#answered .areopen{opacity:1}}' resources/board/view.css
# the bug this unit fixed, asserted as absent rather than as a count
if grep -q '#answered .areopen{.*visibility:hidden' resources/board/view.css; then exit 1; fi

# the browser probes: pass one's own evidence, kept as the regression check.
# A lane has no board of its own, so the board is found through the checkout
# the lane is a worktree of — `--git-common-dir` is that root from either.
CO="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
PROBE="$CO/.pearde/prds/write-affordances-on-focus/probe"
( cd resources/board && node "$PROBE/keyboard-affordances.js" )
( cd resources/board && node "$PROBE/extra-affordances.js" )
```
