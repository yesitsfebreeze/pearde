---
state: done        # open|analyzing|refine|question|specced|claimed|blocked|done|failed
origin: requested  # requested = the user asked | derived = the board found it
# from:            # derived only — the PRD whose work surfaced this one
priority: 85        # higher first
complexity: 34      # analyst, at spec time — 1-100. THE WEIGHT the board schedules by
blast-radius:      # analyst, at spec time — high|mid|low. What breaks if this is wrong
repo:              # the sub-repo the code lands in; delete if n/a
# workflow:        # OPTIONAL — how this kind of job is done: a slug in
#                  #   .pearde/workflows/. @references/workflow.md.
#                  #   Absent = the brief alone, as before workflows
time:              # OPTIONAL. See @references/parts/order.md
  est:             # the weight, only when complexity is absent. Not a duration
  actual: 2.85h
  # claim: <worker> <started>   # orchestrator-only, present while a worker holds this PRD
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
     or counting above `specs-above` (both in .pearde/settings.md, default 40 and
     6) make the analyst's verdict REFINE, and `pearde refine` lands the split
     under `## Children` here — the contract above it stays as written.

     A derived PRD states, in the body, which requested PRD it would otherwise
     get wrong. If it cannot, it is filed `state: deferred` — and if fixing it
     would change only how loudly the board notices, it is a memo, not a PRD.
     See @references/parts/derived.md. -->

# Every probe harness is re-aimed at the pearde layout

When this is done, every harness under `.pearde/prds/**` runs from any
directory and measures the code repo, not the board. The board moved from
`<repo>/prds/` to `<repo>/.pearde/`, and every harness written before that move
finds its repo root by counting `..` from its own path — a count that is now
short by exactly one segment, the `.pearde/` the move inserted. Until this
lands no harness on this board can be trusted: an implementer who runs one
reads red that says nothing about the code they changed, and the board's own
`harnesses` gate — `resources/doctor.sh:634`, `HLIST=$(find "$BOARD" -name
verify.sh …)` — runs all of them, so the gate reports the migration forever
instead of reporting the work.

The measurement. There are 38 shell files under `.pearde/prds/**`. Thirty-three
derive a root with a `cd "…/../.." && pwd` and every one of them is short by
one: a top-level probe at `.pearde/prds/<name>/probe/` needs four `..` and
spells three — `.pearde/prds/an-unknown-flag-refuses/probe/verify.sh:10`,
`.pearde/prds/a-parked-prd-comes-back/probe/verify.sh:6`,
`.pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh:10`; a child probe at
`.pearde/prds/<parent>/<child>/probe/` needs five and spells four —
`.pearde/prds/the-board-runs-itself/collect-is-a-command/probe/verify.sh:10`,
`.pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh:14`,
`.pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh:7`,
`.pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh:7`.
Run today, `bash .pearde/prds/a-parked-prd-comes-back/probe/verify.sh` prints
`44 checks · 4 pass · 40 fail` under a first error of `grep:
/Users/feb/dev/infra/pearde/.pearde/references/parts/handles.md: No such file
or directory` — the root landed on the board. Two files are already right and
are the models to copy: `.pearde/prds/nothing-left-open/the-line-tells-the-truth/probe/verify.sh:11`
counts five, and `.pearde/prds/nothing-left-open/a-quoted-walk-is-data/probe/verify.sh:8-9`
walks up to the nearest ancestor holding `resources/guard.py`, so no depth is
encoded at all. Four more do not count `..` and each is wrong its own way:
`.pearde/prds/init-writes-a-board-on-the-pearde-layout/probe/check.sh:15` hardcodes
the absolute `BOARD_PY=/Users/feb/dev/infra/pearde/resources/board`;
`.pearde/prds/one-page-that-says-whats-up/probe/verify.sh:9` `cd`s three levels
and then reads `resources/…` relatively;
`.pearde/prds/workflows-on-the-board/workflow-seed/probe/verify.sh:10-14` `cd`s
four levels, sets `ROOT=$PWD` and then `BOARD=$ROOT/prds`;
`.pearde/prds/collect-commits-the-code-repo-not-the-board-repo-twice/probe/build_fixture.sh:4`
takes its root as `$1` and is only as right as its caller.

The second breakage rides with the first: a board is no longer a `prds/`
directory. `resources/board/plan.py:60` sets `BOARD_DIR = ".pearde"` and
`find_board` (`plan.py:78-92`) refuses anything else with `no .pearde/ board at
<x>` (`plan.py:85`), so the 19 files that pass `--board "$D/prds"` are refused
before a single assertion runs. `plan.py cmd_example` (`plan.py:2390`,
`shutil.copytree(EXAMPLE, dest…)` at `:2415`) now copies the example board *to*
`<dir>`, so `<dir>` is the board — `bash
.pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh` exits 2 with `no
example board` from its `example "$D/ex"` at `:27-28`, and
`.pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh:11`
still reads its fixture source from `$ROOT/resources/board/example/prds` when
`resources/board/example/` itself now holds `memos/ prds/ README.md
settings.md workflows/` and is the board.

Constraints. This is a re-aiming, not a rewrite: no assertion is added, removed
or weakened, and every harness's own denominator stays exactly where it is —
`collect-keeps-its-word` 101, `collect-is-a-command` 133,
`specced-is-a-command` 90, `transitions-are-commands` 74,
`an-unknown-flag-refuses` 196, `a-parked-prd-comes-back` 44. Nothing under
`resources/` is edited here. `resources/statusline.sh:78-81` still walks up
looking for `$d/prds` and sets `BOARD="$d/prds"` — that is a real defect and it
is **not** this PRD's: `every-document-names-the-path-the-board-is-on` (open,
priority 75) names `resources/*.sh` in its scope and explicitly excludes the
Python under `resources/board/`. Likewise `plan.py example` writing no
`.state/` belongs to `state-dir-belongs-to-the-board` (open, priority 85); a
harness that needs the directory may `mkdir -p` it as a marked workaround, as
`the-line-tells-the-truth`'s already does, but must not fix it here. Prefer the
`a-quoted-walk-is-data` walk-up over a longer `..` chain wherever a harness is
touched, so the next layout move costs nothing.

Pointers. `.pearde/prds/nothing-left-open/the-line-tells-the-truth/` is
`state: blocked` on this PRD by name in its `needs:`, with 24 of 31 acceptance
boxes closed and 7 open; its `report.md` is the field measurement of this
breakage and should be read first. Five of those boxes are exactly the
harnesses this contract must re-aim, named in its specs:
`the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh` to 101/101 and
`the-board-runs-itself/collect-is-a-command/probe/verify.sh` to 133/133
(`specs/spec01.md:51-52`);
`the-board-runs-itself/specced-is-a-command/probe/verify.sh` to 90/90 and
`the-board-runs-itself/transitions-are-commands/probe/verify.sh` passing `the
line opens with the transition` (`specs/spec03.md:56-57`); and
`an-unknown-flag-refuses/probe/verify.sh` to 196/196 (`specs/spec04.md:59`).
Those five are the core of this job and land first. Its two other open boxes
are not this PRD's to close and should not be counted as such: the statusline
box (`specs/spec03.md:54`) waits on `resources/statusline.sh`, and the `git
diff HEAD --` box (`specs/spec03.md:58`) is unclosable as written because the
rename it inspects was committed in `7b88100`.

## Acceptance sketch, for the analyst

- Every shell file under `.pearde/prds/**` that derives a repo root resolves it
  to `/Users/feb/dev/infra/pearde` when invoked by absolute path from `/`, and
  no file hardcodes an absolute machine path.
- The five harnesses `collect-keeps-its-word`, `collect-is-a-command`,
  `specced-is-a-command`, `transitions-are-commands` and
  `an-unknown-flag-refuses` each print their own full denominator with zero
  failures, at the counts 101, 133, 90, 74 and 196.
- `grep -rn -- '--board [^ ]*prds' .pearde/prds --include='*.sh'` returns
  nothing, and no harness passes a `prds` directory to `plan.py`, `specs.py`,
  `transitions.py`, `collect.py` or `serve.py` as a board.
- `bash .pearde/prds/a-parked-prd-comes-back/probe/verify.sh` and `bash
  .pearde/prds/the-gate-runs-the-harnesses/probe/verify.sh` both run to a
  count line instead of dying on a missing path or `no example board`.
- `git diff` over `.pearde/prds/**` holds only path and root-derivation hunks:
  the number of `check`/`t`/`ok` call sites in each harness is unchanged, and
  no file under `resources/` is modified.

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
