# round — board layout redesign (godesign) + color follow-through, done

User ask 1 (layout, done): viewport-dominant Gantt, slide-in state panel
(left tab) and focus panel (right tab), controls contextual to their
elements instead of a header bar.

User ask 2 (color pass, done): collect is green everywhere (analytics tile
included), Gantt titles carry the state color with a legibility floor, and
on master boards each bar's first ~10% is the member board's identity hue.

## Established
- Shell HTML: resources/board/render.py TEMPLATE. Styles: view.css. Logic:
  view.js (ids only — DOM placement free). Gate: viewtest.js.
- Live daemon on 127.0.0.1:8443 re-execs on render.py save; view.js/css hot.
- Screenshot loop: /private/tmp/claude-501/-Users-feb-dev-infra-pearde/089068fb-58a8-489d-ba52-f62d595aa1f5/scratchpad/shot.js
  usage: node shot.js <url> <out.png> <w> <h> [light|dark] ["click:#id;js:...;key:X"]
  NOTE: actions split on ";" — injected js may not contain semicolons; for
  bigger injections see master-shot.js in the same dir, which mutates
  pearde.data in place (hydrate() makes it circular — never JSON-clone it)
  and calls pearde.apply. A live seq bump can overwrite an injection.

## Done — layout pass (see git diff; verified after2*.png)
1. render.py TEMPLATE: aside#state + #statetab (badge #staten); #landtog
   right edge tab (badge #focusn); #rowtools HUD in #frame; #tcontrols is
   the chart card footer; h2 "the plan" removed.
2. view.css: .edgetab styles, #state drawer, footer strip, #rowtools glass,
   #frame radius, #stage margin, narrow/media rules.
3. view.js: setStatePanel + key "s", Esc chain, #staten/#focusn badges.
4. viewtest.js: statePanel + focusTab checks.

## Done — handover verification (this worker)
- after2-narrow/after2-names were sound except the axis-end pills at 390px:
  - view.js drawHeader ("the two tags" block, ~line 936): pills shed their
    suffix below 560px plot width ("vision · 3.2h", "now"), and the now tag
    skips drawing when it would sit under the vision tag (tag() now returns
    its span, ~line 1124).
- view.css #rowtools: padding 2px 6px (wider blur pad, hides tick peek).
- Verified: after3-narrow.png, after4-narrow-dates.png, after3-names.png.

## Done — color pass (this worker)
1. Collect is green everywhere:
   - view.js tile() takes a class ("hot"/"got"); "to collect" tile passes
     "got"; view.css .tile.got .v{color:var(--ok)} (~line 835).
   - canvas ✓ collect glyph in the name column: T.accent → T.ok (~line 1012).
   - tooltip "✓ collect" key: class "k got"; #tip .got in view.css (~1095).
2. Gantt titles in the state color: nameInk(t) (view.js ~line 171) —
   colOf(t), but graphite-ramp fills with alpha < .45 (open/refine/
   analyzing/done) fall back to T.ink2; hues (question/blocked/failed/
   claimed/collect-green) pass through. Used in the name-column draw and in
   labels() floats; inside-the-pill labels keep inkOn(fill).
3. Board identity hue (master boards): boardHue(name) + onMaster() beside
   nameInk (~line 181) — deterministic hsl(hash 55% 45%), with the DECISION
   comment (owner-directed hue-on-category override, scoped to member
   identity). drawBar gained o.lead: a 10%-width cap (clamp 6..22px)
   clipped to the bar's rounded rect, drawn before part ghosting (~line
   745); the task drawBar call passes lead when onMaster() && t.board
   (~line 930). Group-by-board headers get an 8px swatch before the label
   (name-column branch ~line 1000); kanban board chips get an inset
   box-shadow in the hue (~line 3025).

## Verified (color pass)
- master-plan-light/dark.png (simulated master via master-shot.js): lead
  caps read in both themes, state fills/ghosting/crit outlines unchanged,
  collect titles green, claimed purple, graphite floor holds.
- collect-tile.png: "to collect 3" green in analytics.
- color-analytics{,-dark}.png, color-names{,-dark}.png: real boards, both
  themes, clean.
- Gate: 45/45 on http://127.0.0.1:8443/board/dotfiles; node --check clean.
- Not visually exercised (single-board daemon; GROUPS.board registers only
  at module boot on a real master): the group-header swatch and the chip
  tint — code-reviewed only. First look at a real master board should
  glance at group-by-board and the kanban chips.

## Owed
- Nothing on these two passes. Working tree left uncommitted on purpose
  (branch carries unrelated uncommitted work); serve.py untouched.
