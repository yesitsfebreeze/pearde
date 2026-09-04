Verdict: DONE

# a-collect-stages-a-deleted-footprint-path-as-a-deletion — engineer report (pass two, implementer)

workflow: probe-then-spec · second pass — the specs stand; step 3 re-measured, step 5 applied its `Fails when` table to the blocks that stood. Pass one's `## Findings` are carried below by name.

## What this pass did

- **Continued the uncommitted build.** Both fixes were in the working tree
  at dispatch (staged, then twice lost to a sibling session's stash
  round-trip — see Collisions): `land_lane` staging the standing
  intersection (`collect.py:2120-2122`) and the `sort_paths` hold-it guard
  reading history (`collect.py:1789-1796`). Re-applied both hunks from the
  sibling's stash when they vanished; the tree at end of run holds them as
  uncommitted edits to `resources/board/collect.py` only.
- **Found and fixed a second shape the specs did not cover.** A lane whose
  implementer STAGED a deletion but did not commit it (porcelain `D ` in
  column 1) holds that path in `standing`, and `git add -A -- <that path>`
  is fatal the same way a committed deletion is — gone from index AND
  worktree matches no pathspec. Measured on the real
  `the-template-twins-fold-into-the-reference` lane, which holds exactly
  this shape: its seven `.doc.md` deletions stand staged, uncommitted.
  The staging set now drops paths absent from the lane's index and
  worktree (`collect.py:2125-2132`); the merge's own commit carries the
  removal. New probe `probe/staged.py` + new spec01 box, both run.
- Recorded the measured fact:
  `python3 resources/knowledge.py remember "a staged deletion is still an
  unmatchable pathspec"` → `sources/260903-4b04.md`, provenance measured
  on pearde (three fixture shapes + the real lane).

## Verify and Proof — every command, verbatim, output quoted

`python3 .pearde/prds/…/probe/reproduce.py` (spec01) → exit 0:
```
delete=True: landed. the collect's commits carry:
  D	resources/install.sh
  M	resources/keep.txt
delete=False: landed. the collect's commits carry:
  M	resources/install.sh
PASS: the delete shape lands with the deletion staged, the modify shape lands unchanged, outside dirt stays outside
```
`python3 .pearde/prds/…/probe/staged.py` (spec01, new box) → exit 0:
```
lane porcelain: 'D  resources/gone.txt\n M resources/keep.txt\n'
LANDED. range: 'D\tresources/gone.txt\nM\tresources/keep.txt\n'
PASS
```
`python3 .pearde/prds/…/probe/verify.py` (spec02) → exit 0:
```
gone shape: 0 ['state: done'] carries: D	resources/install.sh | M	resources/keep.txt
nonexistent shape refused, as it must be: Stop … footprint resources/never/was.sh is in no repo that holds it — looked for
PASS
```
Ran twice each — the second runs landed mid-session when a sibling's
stash round-trip had silently reverted `collect.py`; the first pass-one
run had measured the fixed file. All six runs exit 0 on the fixed tree.

## The repo's own gate — red, on inherited rows only

- `index.py check` exit 1: 13 problems, every line names `docs/*`,
  `resources/board/obsidian_register.py` or `references/files.md` rows —
  none names `resources/board/collect.py`.
- `memos.py check` exit 0.
- `doctor.sh` exit 1: `index` (the rows above), `claims` 3 drifted names
  (`references/parts/handles.md:74`, `resources/board/mapfile.py:206`),
  `vault` (the dot-segment layout — a `pearde upgrade` decision, not a
  file fix), `workflows` run-counter behind (81 sections / 77 runs).
- `knowledge.py relink` run this pass; `knowledge` row now `ok` (116
  notes, graph in sync). Pass one left it broken on `260903-a796`.

Every red row names files outside this PRD's footprint. A split or repair
of any of them is a defect outside scope, reported here, not done.

## Acceptance box 3 — the two held PRDs

Not run, and measured as far as a worker can without taking the
orchestrator's transition on a shared checkout (memo
`no-destructive-git-runs-in-a-tree-the-session-does-not-own`):
- `collect every-task-is-a-verb-under-one-skill/the-skills-fold-into-one-index --dry` →
  `spec01 exit 1`: its spec01 verify runs `test ! -e references/skills`
  against the CHECKOUT, which still holds `references/skills/` — the lane
  is 0 commits ahead and holds the build as standing dirt, so the merged
  tree cannot exist until the lane lands, and the lane cannot land while
  the collect's own verify refuses. It also holds a staged
  `D resources/install.sh` — the shape spec01's new guard now stages
  around.
- `collect the-tree-holds-only-what-a-board-uses/the-template-twins-fold-into-the-reference --dry` →
  `spec01 exit 1`: `doc.md twins on disk: 7` — same shape, plus `main
  moved under the lane` on 5 footprint paths.
- The dry runs also parked 700+ `docs/node_modules/**` files aside and
  reported `stash pop conflict; resolve by hand` — the shared checkout's
  foreign dirt is what makes a live collect from a worker unsafe, which
  is why box 3 stays with the orchestrator: collect this PRD, then
  collect the two. The mechanism both boxes need is measured (all three
  probes, including the exact staged-deletion shape both lanes hold).

## Findings (pass one's carried forward, plus new)

- (pass one) `references/parts/workers.md` said the fix is `git add -A`;
  the record says `-A` cannot match a gone pathspec at all. Stands.
- (pass one) `specced` checker's "verify block names no path under the
  footprint" warning is a false positive for probe-shaped verify blocks.
  Still stands — this pass did not widen it.
- (new) **A staged deletion is a third unmatchable shape.** spec01's
  measured facts covered committed deletions and worktree deletions; the
  template-twins lane holds the third. Fixed in this pass's hunk, probed
  by `probe/staged.py`, recorded as `sources/260903-4b04.md`.
- (new) **A session's `collect` verify parked the whole shared checkout's
  foreign dirt in `stash@{0}` and the pop failed** — that is how this
  pass found the fix reverted twice. `collect-aside/` under `.git`
  holds `docs/node_modules/**`. Someone must drop or restore
  `stash@{0}` (`nova2: foreign stash-apply leftover parked back`) and
  the three older snapshot stashes deliberately, on a quiet board.
- (new) `probe/reproduce.py`'s fixture committed its deletion, so it
  could not see the staged shape; `staged.py` covers it. The PRD's box 3
  cannot be closed by any worker: it names a live collect of two other
  PRDs.

## Health floor

Footprint under the health floor: `resources/board/collect.py`, 6 files
under 40 lines board-wide per `doctor health` — none in this footprint.
Nothing to leave better inside scope; the guard comment at
`collect.py:2112-2119` now names all three deletion shapes.

## Scores

complexity: 6
blast-radius: high
workflow: probe-then-spec

Blast-radius: every PRD lands through `land_lane` and `sort_paths`. The
staging set was narrowed (dropping unmatchable gone paths), never widened;
the guard's never-existed refusal is measured both ways.