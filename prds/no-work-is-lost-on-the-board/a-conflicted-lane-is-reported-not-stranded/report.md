# a-conflicted-lane-is-reported-not-stranded — analyst report

Verdict: SPECCED

The build went through. `resources/board/lanes.py` and
`resources/board/collect.py` in the lane now turn a conflicted rebase into a
`blocked` PRD naming the lane branch and every file git refused to merge, and
the PRD's probe is **21 of 21 green** against that tree and **12 of 21**
against the same tree without the change. Two specs, complexity 12, blast
radius mid.

## What the build did

`lanes.merge` raised a bare `LaneError` on a conflict; `collect.land_lane`
caught every `LaneError` and re-threw it as a `Stop`; `cmd_collect` printed the
`Stop` to stderr and exited 1. Nothing on the board was written — which is why
`board-commands-run-in-the-session-s-tree` and `the-cross-board-parts` sat
`claimed` under workers that were gone.

The change is three moves and no more:

1. `lanes.Conflict(LaneError)` carries `branch`, `onto` and `files`. The file
   list is git's own, carried as data. Re-parsing it back out of the message
   is how the reason drifts from what git said, and the caller writes it into
   `prd.md` verbatim.
2. `land_lane` re-raises `Conflict` and still converts every
   other `LaneError` into a `Stop`. A lane git cannot read is a broken board,
   not a wall a person takes down.
3. `collect.block_conflict` writes `state: blocked`, deletes `claim:`, appends
   a `## Blocked` section and records the transition row. `collect_one` calls
   it from one `except` around `land_lane`.

`## Blocked` was chosen over a new section because @references/parts/view.md
already draws that heading as the wall and `questions.py` already refuses a
`blocked` PRD for not having one. The reason lands where every reader of this
board already looks, and no renderer learns anything new.

`blocked` and not `failed`: this work may be perfect and merely disagree with
what landed while it ran, and `failed` routes to `retry`, which would dispatch
a second worker onto a lane that already holds the answer. `unblock` lands on
`specced`, which is where the PRD was before the collect. The probe checks
that round trip end to end.

Two judgements the build made on purpose, both written into spec01 so an
implementer does not reverse them by accident: `block_conflict` is
unconditional and not behind `--fail`, because without the write the PRD stays
`claimed` with no worker, which is the whole defect; and its `--dry` arm is
unreachable today, because `land_lane` returns before it merges under `--dry`
— kept because it costs nothing if that changes.

## Specs

| spec | goal | complexity | footprint |
|---|---|---|---|
| `spec01.md` | a conflicted lane writes the PRD `blocked` with git's own file list | 8 | `resources/board/lanes.py`, `resources/board/collect.py` |
| `spec02.md` | the written contract says a conflict is reported, not merged by hand | 4 | `references/parts/commits.md`, `references/parts/states.md` |

Union of the footprints — four files, no directory:

- `resources/board/lanes.py`
- `resources/board/collect.py`
- `references/parts/commits.md`
- `references/parts/states.md`

Both specs' verify blocks are green in the lane as this is written. Every
acceptance box in spec01 is a box the probe already fails on a tree without
the change, so none of them is a box that cannot fail.

`complexity: 12` — three functions and one exception class, all additive, on a
path that already had the failure in hand and only threw it away. The PRD's
own frontmatter guessed 15; the build came in a little under it.

`blast-radius: mid` — `land_lane` runs on every collect on every board this
machine watches, so a mistake here is felt everywhere rather than in one
corner. It is not `high` because the change touches nothing destructive: the
lane branch and the checkout are both left exactly where the existing code
already left them, and the worst a bug can do is mis-state a PRD, never lose a
commit.

## Findings

### The sibling holds three of these four files right now

`collect-runs-the-invariants-and-red-refuses` is `claimed`
(`impl-collect-inv-6476`, 12:04) and its specs' footprint already names
`resources/board/collect.py`, `references/parts/commits.md` and
`references/parts/states.md`. This is the `after … (footprint)` case
@references/parts/commits.md describes, not a defect — the plan orders the
pair and whichever lands second rebases onto the first. It is worth saying out
loud that the second of the two will exercise this PRD's own mechanism if the
rebase does not go through cleanly.

### `lane` and `unblock` are not in the board's grammar

`python3 resources/grammar.py show lane` and `… show unblock` both answer "is
not defined on this board", and both words are load-bearing in this contract —
the PRD, the reason text and the acceptance boxes all use them. Reported
rather than invented, per the brief.

### The grammar's `blocked` row goes stale when spec01 lands

`grammar.md` defines `blocked` as "the work is done and a box waits on
something named. Live work, counted, carrying `needs:`". After this PRD a
conflicted lane is `blocked` while carrying no `needs:` and while waiting on a
person rather than on a named PRD. spec02 corrects the same claim where it
appears in `references/parts/states.md`; the grammar row is a board file under
another skill's rules, so it is named here rather than edited or specced.

### `states.md` said `blocked` is set by the orchestrator only

Now `collect` sets it too. spec02 fixes that row. Noted separately because it
is the kind of claim that reads as merely stale and is in fact the reason a
reader would not think to look for a `blocked` PRD after a red collect.

### `resources/install.sh --check` prints `usage: dirname string [...]`

Running it in the lane emits a `dirname` usage error and reports three agent
files "missing" at a path beginning `/agents/` — an empty root joined into an
absolute path, because `CLAUDE_CONFIG_DIR` is unset in a worker's shell. It
predates this PRD and is outside the footprint, so it is named here and not
touched.

## Harnesses

`resources/board/mapfile.py check` is silent. Every board harness whose script
names `collect.py` or `lanes.py` was run twice — `PEARDE_ROOT` at the lane and
at the orchestrator's checkout — and every one printed the identical count
either way, so nothing in this change moves a committed harness:

| harness | lane | checkout |
|---|---|---|
| `a-lane-s-wiki-is-a-stub-…` | 19 · 18 pass · 1 fail | 19 · 18 pass · 1 fail |
| `a-verify-block-must-not-destroy-the-checkout-it-runs-in` | 24 passed, 0 failed | 24 passed, 0 failed |
| `board-rel-is-a-third-wrong-board-path-resolution` | 0 failed | 0 failed |
| `collect-must-not-reset-the-checkout-it-did-not-write` | 31 · 31 · 0 | 31 · 31 · 0 |
| `collect-resolves-a-board-path-two-ways-and-both-are-wrong` | 7 · 7 · 0 | 7 · 7 · 0 |
| `collect-stages-a-shared-file-whole` | 32 passed, 0 failed | 32 passed, 0 failed |
| `filing-refuses-a-file-it-does-not-hold` | 52 · 52 · 0 | 52 · 52 · 0 |
| `collect-runs-the-invariants-and-red-refuses` | 12 FAIL | 12 FAIL |
| `nothing-left-open/the-line-tells-the-truth` | 85 · 81 · 4 | 85 · 81 · 4 |
| `post-report-crashes-a-collect-…` | 75 · 75 · 0 | 75 · 75 · 0 |
| `every-module-finds-its-siblings-by-one-rule` | 3 passed, 20 failed | 3 passed, 20 failed |
| `the-board-runs-itself/collect-is-a-command` | 133 · 133 · 0 | 133 · 133 · 0 |
| `hunks-land-where-they-came-from` | 47 · 47 · 0 | 47 · 47 · 0 |
| `the-brief-names-the-verdict-line-collect-requires` | 15 ok · 0 FAIL | 15 ok · 0 FAIL |
| `the-collect-and-brief-harnesses-are-carried-across-the-layou` | 7 · 7 · 0 | 7 · 7 · 0 |
| `the-tool-keeps-its-word/collect-keeps-its-word` | 101 · 101 · 0 | 101 · 101 · 0 |
| `the-verify-guard-parses-git-s-own-output-before-it-trusts-it` | 46 passed, 0 failed | 46 passed, 0 failed |
| `workflows-on-the-board/workflow-improve` | 62/71 pass | 62/71 pass |

The reds in that table are pre-existing and belong to other PRDs: the sibling's
own probe is red because the sibling is mid-implementation, and
`every-module-finds-its-siblings-by-one-rule` and `the-line-tells-the-truth`
are red identically on both trees, as is `workflow-improve` at 62 of 71. All
eighteen were measured on both trees and not one count moved.

## Housekeeping

- `python3 resources/knowledge.py query` on the contract returned 90 hits, all
  90 strong, over 90 notes on record. No gap, so nothing was enqueued to
  `.pearde/wiki/pending/` by this pass.
- Nothing was learned outside this repo, so nothing was written back with
  `knowledge.py remember`.
- The probe under `.pearde/prds/` resolves its root by walking up to `.pearde`
  and taking its parent, which in a lane pass is the orchestrator's checkout
  and not the lane. Both spec verify blocks therefore set `PEARDE_ROOT="$PWD"`,
  which is correct in a lane and correct after landing.
- The probe and both specs are left uncommitted in the lane, together with the
  four footprint files, for the implementer to continue.

## Scores

complexity: 12
blast-radius: mid
workflow: probe-then-spec
