# report — the doctor checks the path a board is on

**DONE** · 1 spec · 5/5 acceptance boxes ticked, each re-run personally.

## What was on disk when I started

Pass one (the probe's uncommitted work) had already rewritten the `board` row
in `resources/doctor.sh`: the walk looks for `$d/.pearde` instead of a literal
`$d/prds`, `BOARD` is the `.pearde/` root, `PRDS` is `$BOARD/prds`, the
git-toplevel comparison is gone, and the old-layout fallback names
`.pearde/prds` as the destination. The analyst had pre-ticked nothing — all
five boxes were open. I re-ran all five against disk.

`git diff resources/doctor.sh` is confined to the board row and nothing else,
so there was no other work in this file to build on or preserve.

## The one thing that did not hold — and was fixed

Acceptance box 3 passes as written (the `fix:` line names
`git mv <found-prds> <root>/.pearde/prds`), but the PRD's own done-when is
stronger: the fix line must name *a command that would actually repair* a
project on the old layout. It did not. Pasted verbatim into a real git repo:

```
fatal: renaming 'prds' failed: No such file or directory
git mv rc=128
```

`git mv` refuses a destination whose parent directory does not exist, and on a
repo with no `.pearde/` the parent is exactly what is missing. The fix line was
a fix line that fails when you paste it.

Changed at `resources/doctor.sh:299` — the fix now leads with the mkdir:

```
fix "mkdir -p $OFFROOT/.pearde && git mv $(echo "$OFF" | head -1) $OFFROOT/.pearde/prds — …"
```

Re-tested by extracting the emitted fix line from doctor's own output and
`eval`-ing it verbatim in the fixture repo: `rc=0`, `prds/` moved under
`.pearde/`, and doctor re-run on the repaired fixture moves off "no .pearde/
board" to `1 PRDs · no settings.md` — a different and correct complaint, and
one the fix line's own prose already tells the person to handle (it names
`settings.md` among the siblings that move alongside).

This is the only line I wrote this round. Everything else was verification.

## Box by box, with output

**Box 1 — `board` row ok against `.pearde/prds` on this repo, not some other
`prds/`.** Holds.

```
  board       ok      /Users/feb/dev/infra/pearde/.pearde/prds · 68 PRDs · language English
```

This is a real test, not a tautology: `/Users/feb/dev/infra/prds` exists one
level up (the master board), and it is exactly what the old walk would have
found and reported `ok` instead. The row now names the right directory.

**Box 2 — the `board` row alone never sets `BROKEN` when it reads `ok`.**
Holds. `row()` at `resources/doctor.sh:51` is
`[ "$2" = broken ] && BROKEN=1; return 0`, and the ok branch (line 314) passes
the literal `ok`. Executed against the real definition:

```
BROKEN after ok row = 0
BROKEN after off row = 0
BROKEN after broken row = 1
```

The trailing `return 0` matters under `set -uo pipefail` — without it the
failed test would be the function's exit status.

**Box 3 — old-layout fixture reports broken, fix names the destination.**
Holds (after the correction above).

```
  board       broken  no .pearde/ board · found …/old-layout/prds  on the old layout
                      fix: mkdir -p …/old-layout/.pearde && git mv …/old-layout/prds …/old-layout/.pearde/prds — …
```

**Box 4 — `.pearde/prds/` fixture reports ok, count matches.** Holds. Doctor
said `2 PRDs`; a direct `rglob('prd.md')` over the same directory said `2`.
On this repo: doctor `68`, rglob `68`.

**Box 5 — no board at all still reports off.** Holds, unchanged.

```
  board       off     no board — pearde init creates .pearde/
                      fix: python3 …/resources/pearde.py init [<dir>] — a board, asking nothing
```

## The spec's Verify and Proof block

Run verbatim, all five greps matched, block ended `VERIFY_OK`. `bash -n
resources/doctor.sh` → `SYNTAX_OK`.

## The gate

Full `bash resources/doctor.sh /Users/feb/dev/infra/pearde`, 0.8s, exit 1.
The exit is not mine. Red rows: `skills` (no `.md` under `skills/` — the
files live in `references/skills/` after the rename), `guard`, `origin`
(3 derived PRDs with no `from:`). All pre-existing and named in my brief as
out of scope. My row is green. The `workflows` row, red at 66 problems when
my brief was written, now reads `5 workflows · 13 atomics · the library checks
out` — another worker closed it this round.

Via the real entry point, `python3 resources/pearde.py doctor <repo>`:
`board ok /Users/feb/dev/infra/pearde/.pearde/prds · 71 PRDs · language
English` (the board grew mid-round; the count tracks it).

## Defect found, not fixed — out of my footprint

`bash resources/doctor.sh .` — a **relative** board path — hangs. Not slow:
it did not finish in 6m40s, against 0.8s for the same run with an absolute
path. Partial output shows it dies in the `guard` row, immediately after
`statusline` and *before* the `board` row, so the board row is not implicated
and neither is anything I touched. The `guard` row is already reported broken
on the absolute path, so this is likely the same defect wearing a second face.
Worth its own PRD: a doctor that hangs on `doctor .` is the same class of
failure this PRD was written about — the tool that tells you what is wrong
being the thing that is wrong.

Nothing was learned outside this repo, so nothing was written to knowledge.
Nothing committed.
