Verdict: DONE

# one-board-path-resolver-fewer — implementer pass two

## Workflow probe-then-spec

| # | atomic | verdict |
|---|--------|---------|
| 1 | read-the-contract | ok — contract already specced (pass one); second-pass route, step 3 re-measures, step 5 applies the `Fails when` table |
| 2 | capture-the-harness-baseline | ok — gate `every-artifact-lands-inside-the-board.sh` PASS ×7 before any edit; re-run PASS ×7 after the commit |
| 3 | attempt-the-build | ok — probe's uncommitted code stood only as `probe/pass-one.diff` (both trees clean), so the diff was applied to the lane worktree and committed there |
| 4 | re-run-the-harnesses | ok — gate PASS ×7 after; `bash -n` clean on both shell files |
| 5 | write-the-specs | ok — no new spec authored; the three standing specs were implemented against, not written |

No atomic failed; no back-edge taken. No workflow text needed replacing.

### Edits

None — every step's atomic ran as written.

## What landed

`probe/pass-one.diff` applied to lane `lane/one-board-path-resolver-fewer`,
committed as `00d2c0a` — three files, +28/−26:

- `resources/statusline.sh` — board walk now tests `$d/.pearde/settings.md`
  (line 97) before `$d/pearde/settings.md` (line 104); header comment names
  `.pearde/` current, `pearde/` the legacy name read through the compat
  symlink.
- `resources/doctor.sh` — `board_named()` runs `for n in .pearde pearde`;
  three comments flipped to the same direction; the old-layout fix line
  writes `$OFFROOT/.pearde` and `git mv`s to `$OFFROOT/.pearde/prds`; the
  "no board" row says `pearde init creates .pearde/`. The `vault` row
  (`doctor.sh:499`) untouched, out of footprint.
- `references/parts/board.md` — roster reads "written eight times", names
  `doctor.sh` and `statusline.sh`; the four-rule list untouched (collapsing
  it is `legacy-migrations-retire`'s job, per spec03's body).

## Box status

- spec01: 3/3 — verify block quoted in `specs/spec01.md`.
- spec02: 6/6 — verify block quoted in `specs/spec02.md`.
- spec03: 3/3 — verify block quoted in `specs/spec03.md`.

Repo gate: `bash resources/invariants/every-artifact-lands-inside-the-board.sh`
→ PASS ×7, before and after the commit. `bash resources/doctor.sh` on this
repo's board → `board ok · 229 PRDs`.

## The vault row — the finding pass one already named, still standing

`doctor.sh:499` still prescribes `pearde upgrade $PROJ — moves it to
$PROJ/pearde and leaves a .pearde symlink` for a dotted board. Once
`legacy-migrations-retire`'s spec02 lands, `upgrade` will not do that move;
the row is the reverted direction on a row whose fix is a design question
(reads `off` instead of `broken`? points at `--dir`?). Reported, not fixed —
outside this footprint.

## Health floor

Footprint files under the floor — none to leave better inside scope; the
lane's own doctor run shows `knowledge broken` and stale-index rows, all
pre-existing worktree artifacts, none in the footprint, none touched.

## Record

`knowledge.py query` re-run on the contract question: 116 hits, all strong,
no gap enqueued, nothing new learned outside the repo — nothing to
`remember`.