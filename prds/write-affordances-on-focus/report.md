Verdict: DONE

# write-affordances-on-focus — report (pass two, implementer)

Workflow followed: `probe-then-spec`, second pass. Lane
`/Users/feb/dev/infra/pearde/.pearde/.lanes/write-affordances-on-focus`,
branch `lane/write-affordances-on-focus`.

**11 of 11 acceptance boxes in `specs/spec01.md` are ticked, each against
output quoted below.** Two files changed, both in footprint:
`resources/board/view.js` (+34/-3), `resources/board/view.css` (+21/-3).

## The headline: pass one's build was gone

The spec opens "**All of it already stands in the tree, uncommitted**" and
the brief repeats it. It did not. The lane was clean and the checkout's
`resources/board/view.js` carried only a neighbour's uncommitted hunks (the
`waiting on you` -> `questions` rename); `view.css` was untouched since
09:46, before pass one ran. Pass one's own report names the cause without
knowing it hit: a concurrent `collect` reset the checkout at ~17:50, three
minutes after the spec was written, and stash entries at 17:50/17:51 say so
in their messages ("safety net vs collect reset --hard").

Searched before rebuilding, all empty:

```
git log --all --oneline -S"tabindex" -- resources/board/view.js   -> (nothing)
git stash list -> 5 entries; none has tabindex in view.js
git fsck --lost-found -> 479 objects; grepped every blob for
  "open to move or edit", 'tabindex="0"', ".card:focus-visible" -> no hit
```

So this pass rebuilt both files from the spec's `## What already stands`,
which was complete enough to do it from. Every box is ticked against a
command run on the rebuild, not inherited.

## What now stands

- **`view.js` — `PeardeBoard.card()`.** `tabindex="0"`, `role="button"` and
  `aria-label` = `"<title> — open to move or edit, currently <state>"`, each
  bound `this.served ? … : nothing` so the read-only `all` page's copy
  renders none of them. `nothing` is now imported from `lit` (line 1) — it is
  the sentinel that *removes* an attribute; `undefined` would render the
  string. A `@keydown` handler opens the drawer on Enter/Space, guarded on
  `e.target === e.currentTarget` (the nested `start` button keeps its own
  native activation), `preventDefault`ed so Space does not scroll and
  `stopPropagation`ed so the window handler's `Enter` (view.js:2408) does not
  also open the timeline's selection.
- **`view.js` — `#dstate`.** The drawer's state `<select>` — the move menu
  the PRD asks for — carries `aria-label="state — writes this PRD's state"`.
- **`view.css` — `.card:hover,.card:focus-visible`.** The lift a hover gives
  is now the lift a focus gives; the ring comes from the global
  `:focus-visible` rule at view.css:150.
- **`view.css` — `#answered .areopen`.** `visibility:hidden` -> `opacity:0`.
  `visibility:hidden` removes an element from the tab order, and this
  button's only ancestor is a plain `.adone` div with nothing else focusable
  in it, so no sequence of Tab presses could ever have reached it — the
  reopen write was pointer-only end to end. Revealed on `.adone:hover`, on
  `:focus`, and unconditionally under `@media (hover:none)`.

### Two deviations from the spec's prose, both deliberate

1. **`:focus`, not `:focus-visible`, on `.areopen`.** Under
   `:focus-visible` the reveal rides Chrome's last-input-modality heuristic
   and the probe's own box read `opacity: 0`. A pointer that focuses this
   button is already hovering it, so there is nothing to withhold. The card
   keeps `:focus-visible`, where a mouse-down would otherwise leave the lift
   stuck on.
2. **No `transition` on that opacity.** The first build had one; it made the
   probe's synchronous `getComputedStyle` after `.focus()` read the
   interpolated `0` rather than the target `1`. Removed — which also
   restores the instantness `visibility:hidden` had.

The spec's claim that `(hover:none)` is "the same breakpoint `#vrail`
already uses two hundred lines up" is off twice: `#vrail` uses
`@media (hover:hover)` at view.css:443, ~820 lines up. `(hover:none)` is its
complement — a new query, not a reused one. Corrected in the spec.

## Acceptance — 11/11, with output

Probe, run as the spec's block runs it, from `resources/board`:

```
  ok    unserved render: board has cards  (8)
  ok    unserved render: no card is tabbable (bullet 3 — `all` gains nothing)  (0)
  ok    served render: a card is now tabbable  (big)
  ok    Tab walkthrough reaches the served card
  ok    the card's aria-label names the write
        (big — a parent whose work is in its children — open to move or edit, currently open)
  ok    the focused card matches :focus-visible
  ok    Enter opened the drawer
  ok    Enter did not write `state:` — a focus walkthrough ends with the board
        unchanged  (open -> open)
  ok    reopen is focusable at all (the old `visibility:hidden` bug)
  ok    reopen starts de-emphasised (opacity 0)  (0)
  ok    focusing it reveals it the way hover does (opacity 1)  (1)
  ok    no page error  ()

probe: all checks passed
```

`probe/extra-affordances.js` — new this pass, for the three boxes
`keyboard-affordances.js` does not reach:

```
  ok    every served card carries role=button  (8/8)
  ok    every served card carries tabindex=0  (8/8)
  ok    every served card's aria-label names title and state  (8/8)
  ok    #dstate carries an aria-label naming the write
        (state — writes this PRD's state)
  ok    #dstate is the move menu — it lists every state  (9)
  ok    the touch context really has no hover
  ok    with a pointer, reopen starts hidden  (0)
  ok    under (hover:none) reopen is plainly visible  (1)

extra: all checks passed
```

Code gate: `node --check resources/board/view.js` -> `view.js compiles`,
exit 0. `node resources/board/viewtest.js --example` -> `49/49 passed`,
exit 0, equal to baseline.

## The spec's `## Verify and Proof` block was rewritten

It could not have run under `collect`, which executes it
`bash -e -o pipefail -c` with cwd = the PRD's `repo:` root:

- `cd resources/board && npm i playwright-core` hits the network on every
  collect and dirties the tree the collect then reads. Dropped — it is
  one-time machine setup, and `viewtest.js` already exits 2 with that
  instruction when the driver is missing.
- `node ../../.pearde/prds/…` dies in a lane, which has no `.pearde`. The
  board is now found through the checkout the lane is a worktree of:
  `CO="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"`,
  correct from either root.
- Added grep assertions on both footprint files, so the block goes red the
  moment the work is reverted regardless of what a browser can say — and one
  `if grep -q '…visibility:hidden'; then exit 1; fi` asserting the old bug is
  absent. No literal total is asserted anywhere; `viewtest`'s exit code is
  the gate, so a later PRD adding a 50th check cannot redden this spec.

Run as `collect` will:

```
awk '/^```sh/{f=1;next} /^```/{f=0} f' specs/spec01.md > block.sh
cd <lane> && bash -e -o pipefail -c "$(cat block.sh)"   -> exit 0
```

And proved it can fail — `@media (hover:none)` mutated to `(hover:xnone)` in
the lane's `view.css`, block re-run -> **exit 1**; restored from a scratch
copy outside the repo, `cmp` clean. (The footprint file is uncommitted, so
the restore could not be a `git checkout`.)

## Harness baseline and re-run

Taken before the first edit; the board's own repo is a worktree, so both
roots were recorded. Board harnesses: 98 `verify.sh` under `.pearde/prds`,
of which two name a footprint path.

| harness | baseline (before the first edit) | after |
|---|---|---|
| `the-documented-board-matches-the-code/probe/verify.sh` (does **not** honour `PEARDE_ROOT` — measures the checkout, never the lane) | exit 1, 11 FAIL | exit 1, 11 FAIL — `diff` of the FAIL lines: identical |
| `one-page-that-says-whats-up/probe/verify.sh`, `PEARDE_ROOT=<lane>` | `31 checks · 26 pass · 5 fail` | `31 checks · 26 pass · 5 fail` — FAIL lines identical |
| `python3 resources/index.py check` (lane) | exit 1, 3 lines | exit 1, 3 lines, identical |
| `bash resources/doctor.sh` (lane) | exit 1; broken: index, claims, vault, origin, memos, knowledge, questions | same seven, same text |

All of the above were red **before the first edit** and are not this unit's.
Three doctor rows moved and none is mine:

- `statusline … *2` — the tree's dirty-file count, which is my two footprint
  files. The atomic names this row as nobody's finding.
- ``health … stale, `pearde health score` refreshes it`` — the health record
  is an mtime cache and any edit to a scored file stales it. Not
  refreshed: `.pearde/health/` is shared with every other live session and
  is outside my footprint.
- `harnesses 98 -> 99` — a sibling landed
  `the-lifecycle-contract-and-purge-reclaims-it/probe/verify.sh` at 18:26.
  A neighbour's landing, not mine.

## The merge

The lane's base (`1be5d2b`) already carries the checkout's last committed
`view.js` (`b1d3f5d`), and `git diff 1be5d2b 379bc17 -- resources/board/view.{js,css}`
is empty — the lane's copies are HEAD's plus mine. The checkout's
**uncommitted** `view.js` hunks are a neighbour's (`waiting on you` ->
`questions`). Tested: all 12 of those hunks `git apply --check` cleanly onto
the lane's `view.js` (offsets only, no conflict), so the two passes can land
in either order without a resolution. Nothing of the neighbour's was carried
into the lane.

## Health floor

The brief's floor block reads `none under the floor` — but that is a lane
artefact. `python3 resources/health.py list resources/board/view.{js,css}`
**in the checkout** prints:

```
  4  resources/board/view.css  lines
 39  resources/board/view.js  lines, branching
```

Both are under the floor of 40, and the brief could not see it because
`.pearde/health/` is keyed on checkout paths and holds no note for a lane
path (`health show` in the lane: `no note for …/.lanes/…/view.js`). Reported
below as a defect in the brief composer.

Nothing could move inside this spec's scope. Both files score low on
`lines` — `view.js` is 225 KB, `view.css` 78 KB — and the only repair is a
split, which is a defect outside scope, reported and not done. This unit
added ~30 lines to each; the alternative was to leave the write affordances
pointer-only.

## Findings

Carried forward from pass one's report, still true, still unfixed:

- **The source doc's "+ to open a PRD" claim is stale.** `#newprd`
  (`render.py:404`) is a plain always-visible `<button>`, never hover-gated,
  already keyboard-operable.
- **The ask view's submit and picks are not hover-gated either** —
  `display:none` toggles on `.qq.answered`, not on hover. Already fine.
- **`#answered .adone` is a `<div data-go=…>`, not a button**, so it is not
  Tab-reachable at all. Confirmed still true this pass (view.js:3737). It is
  a *read* affordance (it navigates, it writes nothing), so it is outside
  this PRD's "every write affordance" contract — for whoever owns
  read-navigation reachability.
- **`knowledge.py query` read a miss as 103 strong hits** and enqueued no
  pending gap.
- **`__dirname` in a script under `.pearde/prds/*/probe/` resolves through a
  lane's `.pearde` symlink back onto the orchestrator's checkout.** The two
  probes here resolve from `process.cwd()` instead; the general fix belongs
  to the parked PRD on a lane missing its own `.pearde`.

New this pass:

- **A `collect` can destroy an uncommitted probe build with no record
  anywhere.** This is the second time this PRD has paid for it and the first
  time it was total: pass one's work existed only in the checkout's working
  tree, a concurrent collect reset it, and it was in no commit, no stash and
  no dangling object. The board's only trace was a stash *message* on
  unrelated work. Cost this pass a full rebuild. Whatever owns
  `collect`'s reset should snapshot every dirty footprint of every `claimed`
  PRD, not only the PRD it is collecting.
- **The brief's health-floor block is blind on a lane.** It resolves
  footprint paths against the lane, `.pearde/health/` has no note for a lane
  path, and the block therefore prints `none under the floor` for a footprint
  whose files both score under it. It should resolve against the checkout
  the lane is a worktree of — the same `--git-common-dir` trick this spec's
  verify block now uses.
- **`specced` is not a read-only check.** Pass one's report already flagged
  this; the state it wrote is still what the board reads. No action needed
  now, but the row is still open.

## Knowledge written back

`python3 resources/knowledge.py remember` ->
`sources/260903-9b84.md` · `[[260903-9b84]]` — *Chromium flips (hover:none)
only under mobile emulation, not via setEmulatedMedia*. Measured both ways
on this machine; a CDP `Emulation.setEmulatedMedia` `hover: none` feature
leaves `matchMedia("(hover:none)").matches` false, while
`newContext({isMobile:true, hasTouch:true})` flips it. One source, so
`remember` and not `conclude`.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | pass. PRD, `specs/spec01.md`, pass one's `report.md`, the probe, and `git status --short` in **both** roots (the lane clean, the checkout carrying 16 modified paths across other sessions) recorded before the first edit. The row "the `repo:` root is a worktree under `<board>/.lanes/`…" fired and was followed: the checkout's `view.js` hunks were read, found to be a neighbour's, and left there. |
| 2 | `capture-the-harness-baseline` | pass. Two board harnesses named a footprint path; one does not honour `PEARDE_ROOT` and is recorded as measuring the checkout. Repo gate recorded with exit codes. Table above. |
| 3 | `attempt-the-build` | pass, but **not** as the "second pass, nothing to build" row expects — the build was gone and had to be redone. Built in place in the footprint files, which is what the atomic's step 2 prescribes for an edit to an existing file. |
| 4 | `re-run-the-harnesses` | pass. Every count equal to baseline; three doctor rows moved and each is accounted for above. No back-edge taken. |
| 5 | `write-the-specs` | pass, second-pass form: no spec authored. The `## Fails when` table was applied to the block that already stood — three rows fired (board-wide/networked command, a block that reads `.pearde/…` from a lane, no literal total) and the block was rewritten and proved both ways. The "the report path already holds a previous pass's report" row fired: pass one's `## Findings` are carried forward by name above. |

No back-edge was taken at any step.

### Edits

**`attempt-the-build` — `## Fails when`.** The row beginning "the brief says
the probe's code is uncommitted, and `git status --short` is clean" resolves
to two causes, a sibling's commit or the lane's own `land_lane`, and its
remedy assumes the work is somewhere. It has no third branch for the work
being **destroyed**, which is what happened here. Add after that row:

| seen | means | do |
|------|-------|----|
| `git log --all -S<a token from the build>`, `git stash list` and `git fsck --lost-found` all come back empty on a footprint the brief says is built | a concurrent `collect` reset the checkout while the build was uncommitted; nothing on the board records it, and the spec's "already stands in the tree" is now a description rather than a fact | search all three before concluding it, then **rebuild from the spec's own `## What already stands`** — a spec written off a real build is normally complete enough to redo it. Take every box against the rebuild, tick none as inherited, and rewrite the spec's "what is left" section so the next reader is not told a third time that it already stands |

**`capture-the-harness-baseline` — `## Fails when`.** The `statusline` row
("that row carries the tree's dirty-file count, which every live session
moves") names one such row. Two more move for the same reason and are not
listed. Replace that row with:

| seen | means | do |
|------|-------|----|
| `doctor` at step 4 differs from step 2 only on `statusline`, `health` or `harnesses` | none of the three measures a rule: `statusline` carries the tree's dirty-file count, which your own edits move; `health` reports its record stale the moment any scored file's mtime changes; `harnesses` counts `verify.sh` under the board, which any sibling landing a probe increments | compare doctor's rows without those three. Where `harnesses` moved, `find <board>/prds -name verify.sh -newermt <baseline time>` names the sibling that added one — a count that rose there is a neighbour's landing, never yours. Do not run `health score` to clear the stale marker: `.pearde/health/` is shared with every live session and is outside your footprint |

## Scores

complexity: 9
blast-radius: mid
workflow: probe-then-spec
