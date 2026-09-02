# round — new-PRD modal as a writing surface + default framing, done

Pass 3 of the board-UI redesign (handed over at the context ceiling; passes
1–2 in round.board-layout.md). Not a board round: no PRDs claimed, no
commits, serve.py untouched. Files touched: render.py, view.css, view.js,
viewtest.js.

## Established
- The "super high" write-it button: the modal's action row was an inline
  flex div in render.py's TEMPLATE, and `#newbox input{width:100%}` in
  view.css hit #nparent inside that nowrap row — it demanded the full card
  width, flex-shrink crushed both buttons to min-content, and "write it"
  broke into a two-line tower at EVERY width (no real breakpoint; the
  shrink math just always lost). Reproduced in before-modal-{wide,narrow}
  .png in the scratchpad.
- The page's one markdown renderer is `md()` in view.js (~line 3869), used
  by the report view; `inline()` above it gives `code` + **bold**. lit-core
  exports `render` — imported as `litRender` for the preview pane.

## Decided
- Default framing is always now→vision (coordinator relay of a user ask):
  removed the mostly-landed heuristic in fitDefault() (view.js ~1797) that
  framed the whole track once the frontier passed mid-track. `from = now`,
  DECISION comment rewritten in place: the default frames the question; the
  whole track is what "fit" (f) is for; history is one pan-left away.
- md() grew fences + checkboxes in that one shared place (list items became
  {box,s} objects) — the report view gets both for free. No second renderer.
- Editor floor: #nsplit min-height clamp(320px,52vh,620px) so a tall window
  gets a tall writing surface without the card overflowing 86vh.

## Edits
- render.py TEMPLATE (~564): modal rebuilt — h3, #ntitle, #ntools toolbar
  (#mdbold #mdcode #mdhead #mdlist #mdbox + #npseg seg with #npedit/#npshow),
  #nsplit (#nbody + #npreview), #nfoot (#nprio #nparent #ncancel #ncreate).
  All inline styles dropped. Original ids all kept.
- view.css overlay block (~1052): card2 width min(940px,94vw), flex column,
  max-height 86vh; overlay padding 7vh 3vw 24px; #ntools ghost buttons in
  the #tcontrols footer-strip idiom; #nsplit grid 1fr (rows minmax(0,1fr)),
  two columns + inline preview at min-width:920px, seg-toggled panes below
  (#newbox.preview swaps them, guarded to max-width:919.98px so a stale
  class can't hide #nbody on a wide card); #npreview .prose type scale;
  shared .prose pre / li.chk styles; #nfoot flex-wrap with #nprio 90px,
  #nparent flex:1, #ncancel margin-left:auto (actions wrap right as a pair,
  primary never strands).
- view.js: import render as litRender (line 1); fitDefault from=now
  (~1800); Escape closes #newbox from inside its fields (~2196) and heads
  the main Escape chain (~2224); md() fences+checkboxes (~3869); editor
  block after $("ncreate").onclick (~4185): nPreviewDraw/nMode/nWrap/nLines,
  toolbar wired via bind() (SIG-threaded for re-import), mousedown
  preventDefault so buttons keep the caret, ⌘B bold, Tab = two spaces,
  input → live preview; $("newprd").onclick resets to edit mode + draws.
- viewtest.js (~236): one new check — N opens #newbox and #ntools #mdbold
  exists — pressed and Escaped before the view-click loop so the overlay
  can't intercept it.

## Verified
- Gate: 46/46 on http://127.0.0.1:8443/board/dotfiles (was 45/45 + the new
  check). node --check clean on both js files; render.py parses.
- Screenshots (scratchpad): modal-wide-light/dark.png 1512×920 (split
  editor+preview, one-row footer, primary intact), modal-narrow-light.png +
  modal-narrow-preview.png 640×844 (seg toggle, footer wraps whole, button
  never strands), modal-final-light.png (52vh editor). Preview exercised a
  PRD-shaped body: ## headings, - [ ]/- [x] boxes, a code fence, **bold**,
  `code`.
- Functional probe (probe.js): toolbar bold wraps the selection, ⌘B wraps,
  Tab inserts two spaces and keeps focus in #nbody, ☐ prefixes the line,
  preview populated, Escape closes.
- Framing: frame-default.png — dotfiles (mostly landed) opens on now→vision
  (axis 0→+3h, three bars); frame-after-d.png — f then d returns the
  identical frame.

## Addendum — theme switch + functionality audit (user mid-task ask)
- User: "no light/dark switch; check every functionality is present."
- Finding: the CSS was fully three-state theme-aware (data-theme stamps at
  view.css 71/99/133…) but NO code ever set the stamp and no toggle ever
  existed, in HEAD either — only the OS preference applied. Genuine gap,
  not a redesign casualty.
- Built: #themetog in #titlebar .right (render.py ~437), between search and
  + PRD. Three states — ◐ system / ☀︎ pinned light / ☾ pinned dark — first
  click pins the OPPOSITE of what shows (a person reaching for it wants a
  flip), full cycle returns to system. Stored under localStorage
  "pearde-theme"; a head classic script (render.py ~404) stamps before
  first paint so a pinned page never flashes. view.js themeSet (~196, in
  the tokens section next to the matchMedia listener) re-stamps, re-reads
  tokens, clears inkCache, redraws canvas+mini+all — same path as an OS
  flip. #themetog ghost-button style at view.css ~226.
- Audit method + result: extracted all 96 $("id") refs from view.js and
  checked the live page — 82 present statically, the 14 "missing" all
  dynamically built (drawer internals at openDrawer ~2659+, ⌘K palette at
  ksShow ~3496), confirmed by opening each. Functional probe: ⌘K palette
  opens+hits, drawer via j/Enter with dstate/dprio/dnote/dnoteadd, state
  panel (s), focus panel (l, 272px↔0), names (t), filters c/r/x latch,
  v flips vision/dates, board picker (b), / focuses filter. Zero page
  errors. Nothing else is missing.
- Gate: 47/47 (added: theme switch pins and a cycle releases).
- CONCURRENT WRITER: another session is editing view.js in this checkout
  (asks view — .qreopen button, wireQuestions(…, reopen), takeRecommended
  removed). My theme block landed beside it cleanly; node --check clean
  and the gate green WITH their in-flight changes. One writer per file
  from here — view.js edits done for this pass.

## Owed
- Nothing on this pass. Working tree still uncommitted on purpose (branch
  carries unrelated uncommitted work).
- Snapshot note: viewtest --check snapshots of the report view will differ
  if a report ever uses fences/checkboxes — md() honestly changed; re-snap
  when that trips.
