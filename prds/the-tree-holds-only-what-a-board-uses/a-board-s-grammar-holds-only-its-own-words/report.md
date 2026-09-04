# a-board-s-grammar-holds-only-its-own-words — analyst report

Verdict: SPECCED

workflow: `probe-then-spec` — the library file fits as written: an open PRD, a
build first, specs from what the build stood up. No new route is named.

The build went through. A board's `grammar.md` is its own words only,
`references/grammar-board.md` holds pearde's once, `grammar.py` merges the two
on every read, `pearde upgrade` trims a board that carries the old copy, and
the map and the documents name the file. Sixteen probe checks are green, the
repo gate is back at baseline, and `doctor`'s `grammar` row reads the same 183
terms it read before the change. Two specs, `specs/spec01.md` and
`specs/spec02.md`, sum `complexity` 22 over two units.

## What the build passed through

- The contract's own measure: a fresh board's `grammar.md` is **19 lines** and
  `grammar show prd` still answers — from the shipped file, through
  `merged()`.
- The install's symlink shape. `grammar.py` resolves the shipped file the way
  `init` already resolved the template: `dirname(dirname(abspath(__file__)))`,
  which under `<skills>/<skill>/resources/grammar.py` is the skill folder, and
  `references` there is a symlink to the repo. Proved in a fixture, probe step 9.
- The split of verbs. `list`, `show`, `brief` and `undefined` read the merge;
  `check`, `add` and `stale` stay on the board's file — a shared row is not one
  board's to break, to define twice, or to be told is unused. `check` does gain
  one line: a missing or malformed `references/grammar-board.md` is reported as
  an incomplete install, naming that file rather than the board.
- The migration. `trim` drops a group only when the shipped file holds every
  one of its rows verbatim, so an edited row keeps its whole group and the
  report names the row that kept it. Idempotent. `cmd_upgrade` calls it on the
  branch where `plant_grammar` found a file already there.

## The defect the first pass shipped, and the check that now catches it

`merged()` popped, from each table, every spelling the other table held. The
two tables are not exclusive — a word can carry a group row *and* a collision
row, which is the format working: the group row says what it means here, the
collision row says what it is not. Seventeen words on this board do:
`state`, `pass`, `run`, `claim`, `done`, `gate`, `report`, `route`, `weight`,
`blocked`, `parked`, `container`, `complexity`, `floor`, `group`, `sweep`,
`vault`. Each vanished from both tables. `grammar list` printed 149 rows where
it had printed 183, and `doctor` reported the loss as a healthy `ok`.

The `mine` filter already drops the shipped copy of anything the board
respells, in either table, so the two pop loops bought nothing and cost 34
rows. They are gone. Probe step 10 is the regression: the merged count before
a trim and after it must be one number, and that number must be 183.

## Gates

- `python3 resources/index.py check` — four lines, every one of them also at
  baseline in the main worktree: `resources/common.py` with no manifest row,
  `references/files.md` and `@@view` naming `@resources/board/hotreload-test.js`
  which is not on disk, and `references/parts/commits.md` citing a memo that is
  not there. All pre-existing, none in this footprint. The one line this build
  added — `references/grammar-board.md` with no row — is closed.
- `bash resources/doctor.sh` — diffed row for row against the main worktree. No
  `broken` row that was not broken before. The only content difference was
  `grammar 183 → 149`, which is the defect above; it now reads 183 again. The
  remaining diffs are `$DIR` paths and counts other sessions moved while this
  pass ran (`vision` 44→48, `harnesses` 78→82, one more knowledge note).
- Harnesses. The full 82-harness sweep was launched and had produced nothing
  after twenty minutes — the machine is running some thirty `doctor.sh`
  processes for other sessions. Two targeted harnesses stood in:
  `the-documented-board-matches-the-code/probe/verify.sh` prints the identical
  eight failures under the lane and under main, and
  `every-module-finds-its-siblings-by-one-rule/probe/verify.sh` fails on a
  `pearde_path` module that exists in neither tree. Both pre-existing.

## Findings outside this contract

- **`resources/common.py` has no manifest row.** Pre-existing, reported by
  `index.py check` at baseline. Not fixed here — it belongs to whichever PRD
  owns the module layout.
- **`doctor` counted a silent vocabulary loss as `ok`.** The `grammar` row
  prints a term count and reads `grammar.py check` for problems, and a merge
  that drops 34 rows is neither. The row is honest about what it measures; the
  point is that a count nobody compares is not a check. Named here, not fixed —
  the board's own `grammar.md` trim in spec02 is the one place it matters, and
  spec02's last box pins the number.
- **The knowledge record had no note on this question** (90 hits, 88 strong,
  none on point). No gap file was enqueued; nothing was learned outside this
  tree, so nothing was written back.
- No word in the contract was missing from the vocabulary.

## Specs, weight and footprint

- `specs/spec01.md` — the shipped file and the merge on every read. complexity 12.
- `specs/spec02.md` — the trim, `pearde upgrade`, the map and the documents. complexity 10.

`complexity: 24` — one parser, one merge and one guarded migration, all of it
Python stdlib against a format this repo already owns; the weight is in the
merge's edge cases, not in the volume.
`blast-radius: mid` — `grammar.py` is read by `doctor` on every board on the
machine and every board's `grammar.md` changes shape, but nothing outside the
vocabulary layer moves and no other module imports it.

Union of the footprints, ten files: `references/grammar-board.md`,
`resources/grammar.py`, `references/templates/grammar.md`,
`resources/board/init.py`, `resources/pearde.py`,
`references/parts/grammar.md`, `references/skills/pearde-grammar.md`,
`references/grammar.md`, `references/files.md`, `index.md`.

## Scores

complexity: 24
blast-radius: mid
workflow: probe-then-spec
