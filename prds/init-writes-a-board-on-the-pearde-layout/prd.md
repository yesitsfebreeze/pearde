---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 80        # higher first
complexity: 10      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   prds/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 0.36h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
commit: c7d674b
---
<!-- Ordering reads three axes and no clock: dependency (needs + footprint),
     vision importance (priority), and complexity/blast-radius. Add your own
     keys freely, at any nesting. Nothing outside state, origin, from,
     priority, complexity, blast-radius, claim, repo, workflow, needs and
     footprint is read, and nothing you add is ever dropped.
       needs:     — PRD dir names this one depends on. A hard gate in `plan`
       footprint: — paths this PRD touches. The overlap check
       workflow:  — the route a worker is handed, expanded into its brief

     One sitting is the limit: specs summing `complexity` above `split-above`
     or counting above `specs-above` (both in prds/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# init writes a board on the .pearde layout

`pearde init` writes a board that already has the `.pearde/` shape: PRD
directories under `.pearde/prds/`, and `memos/`, `wiki/`, `workflows/`,
`.state/` as their siblings. A board created by `init` today is malformed —
`scan` finds no PRDs in it, because the example PRDs land one level too high.

The board layout was moved from `prds/` at the repo root to a `.pearde/`
directory beside `.obsidian/`:

    <project>/.pearde/
        prds/        PRD directories
        memos/  wiki/  workflows/
        settings.md  vision.md
        .state/      plan.json history.jsonl transitions.jsonl round.md view.html

`resources/board/init.py` was carried across that move only halfway. Its
`write_board()` (around line 109) still `copytree`s `resources/board/example/prds`
into the board root, so the example PRD directories land at `.pearde/<name>/`
where `scan` no longer looks, and `settings.md` and `vision.md` may land in the
wrong place with them. The first command to run is a listing of
`resources/board/example` two levels deep — the fix depends on how that tree is
shaped on disk.

Two shapes will do it, and either is acceptable:

  - restructure `resources/board/example` on disk to mirror the board layout,
    and keep the single `copytree`; or
  - keep the example tree as it is and split the copy — `settings.md` and
    `vision.md` to the board root, the PRD directories into `prds/`.

Whichever is chosen, `write_board()` must also create the five directories a
board has even when empty: `prds/`, `memos/`, `wiki/`, `workflows/`, `.state/`.

Done when a board created by `init` in an empty directory passes
`python3 resources/board/plan.py scan` and that scan reports the example PRDs
by the names they have in the example tree — not prefixed by `prds/`.

Not in scope: the rest of `init.py`, which was already moved to the new layout
(the `board = os.path.join(d, ".pearde")` line, the `IGNORED` tuple, the
api-key path, the docstrings). Do not re-do those. Do not add dual-path
support for the old `prds/` root — the decision on record is a single layout
and a one-off migration, not a compatibility shim.

Pointers: `resources/board/init.py`, `resources/board/plan.py`
(`find_board`, `BOARD_DIR`, `STATE_DIR`, `PRDS_DIR`, `prds_dir`, `state_dir`),
`resources/board/example/`.

<!-- Three more headings exist, and none of them is a slot to copy down. Each
     is a claim about the state of this PRD, so an empty copy of it is a false
     one: an empty `## Questions` stops the board on nothing, an empty
     `## Answers` reads as answered, an empty `## Failure` reads as a failed
     attempt. Write the heading when it has content; until then it is absent,
     which is the honest state. @resources/questions.py reports the empty
     ones, and `doctor`'s `questions` row runs it. -->

<!-- `## Questions` — analyst-only, when blocked on the user: one round in the
     format of drill.md — `### Q1: <title>`, the fork in two sentences ending
     in "?", then exactly three prepared answers, each a complete decision,
     one `(recommended)`. Only real forks the user must settle (naming, scope,
     cost) — never facts a worker could look up, never the PRD restated. A PRD
     parked on the user with no such round never says what it is asking.
     Written in plain words for the person who asked, never for the board — no
     backtick, no path, no PRD name, no board word, 60 words in the fork and 25
     in an answer: the table in @references/drill.md is the whole rule, and
     @resources/questions.py refuses a round that breaks it. -->

<!-- `## Answers` — orchestrator-only (or the view), written after asking the
     user: `**Q1** — <the picked answer verbatim, or the user's own words>`,
     numbers matching the round above it. Analysts read these before speccing.
     An `## Answers` with no `## Questions` above it answers nothing. -->

<!-- `## Failure` — implementer-only, after a FAILED attempt: what broke, what
     was tried. `retry` moves this into the body as history and reopens the
     PRD. -->

## Report

spec01: exit 0
PASS - example board lands under prds/, scan sees it unprefixed, the five empty dirs are made on a plain init
