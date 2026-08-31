# report — doctor finds the guard the way the scan does

**DONE** · 1/1 spec · 3/3 acceptance boxes re-run and closed · gate 3/3 green ·
`doctor` exit 0, 0 `broken` rows.

## What changed

Nothing new. The fix was already in the tree from the probe and I confirmed it
is the whole of the change: `resources/doctor.sh`'s guard row walks for
`$d/.pearde` instead of a literal old-layout directory, with the same
dirname-fixpoint break the `board` row below it already had. Net diff against
the round's start: unchanged, 8 insertions / 3 deletions in that one hunk. My
own edit is confined to this PRD's `specs/spec01.md` — the `## Verify and
Proof` block, hardened (see below).

## The three boxes, re-run

I re-ran each box myself rather than trusting the tick.

**Box 1 — the walk matches `board_of` and `find_board`.** `resources/guard.py`
and `resources/board/plan.py` both hold `BOARD_DIR = ".pearde"` and both climb
to the nearest ancestor holding it, breaking on the dirname fixpoint.
`doctor.sh` now makes the identical test in two places — the guard row and the
`board` row.

**Box 2 — absolute `$START`, with the hijacker still on disk.**
`/Users/feb/dev/infra/prds` (another project's old-layout board, a level above
this repo) is present, so this is a live test of the bug, not a hypothetical
one. A replay of the pre-fix walk in Python settles on
`/Users/feb/dev/infra/.claude/settings.json` — the wrong project's file. The
current walk gives:

```
  guard       ok      wired in /Users/feb/dev/infra/pearde/.claude/settings.json · MAX_THINKING_TOKENS=8000 · skill tree guarded
```

**Box 3 — relative `$START`.** `bash resources/doctor.sh .` terminates (run
under a 120 s watchdog; it returns in seconds) and reports
`guard ok · wired in ./.claude/settings.json`. Without the fixpoint break,
`dirname .` is `.` forever.

## The check can still fail

The orchestrator asked for proof the row is not green regardless of the truth.
Three negative controls, each restoring state in a `finally`:

1. **Pre-fix walk put back, same disk state** — the row flips to
   `guard broken  …/resources/guard.py does not refuse a hand-walked board`,
   the exact symptom the PRD describes. Restoring the fix flips it back to
   `ok`. This is the decisive one: only the walk changed.
2. **The hook genuinely unwired** — `.claude/settings.json` moved aside, then
   put back with its `hooks` block stripped. Both give
   `guard off  not wired in …/.claude/settings.json`. The file was restored
   byte-identical (sha256 `4fd37d83aa745f55…` before and after).
   Note the vocabulary: an unwired-but-findable hook is `off`, not `broken` —
   `broken` is reserved for a guard that is wired and does not refuse. Neither
   is `ok`, which is what the box is asserting.
3. **The verify block itself** — run against the pre-fix code it exits 1
   (`WALK_MISMATCH n=1`), and the row-matching arm exits 1 on a fabricated
   `broken` row. The block is falsifiable at both its assertions.

## The verify block was rewritten

The block as specced ended on `grep … && echo A || echo B`, which under
`bash -e -o pipefail` risks a SIGPIPE-driven false FAIL and, worse, exits 0
whichever branch it takes — `collect` reads the last exit code, so a failing
run would have been collected as green. The replacement captures `doctor` into
a variable with `|| true`, matches with `case` rather than a pipeline, exits 1
on any failure, and ends on an explicit `echo VERIFY_DONE`.

One trap surfaced while proving this out and is worth recording, because it
does not show up when a block is run by hand. Box 3's hang watchdog was
`( sleep 120; kill -9 $p ) &`, and killing that subshell does not kill the
`sleep` it spawned. The orphan inherited the block's stdout, so under
`collect` — which captures output through a pipe — the block did its work in
under two seconds and then sat for the full 120 s waiting on a pipe an
orphaned `sleep` still held open. Run from a terminal it looked instant. The
watchdog is now `>/dev/null 2>&1 </dev/null` and killed with `-9`, so no
descendant holds the pipe. Measured through a captured pipe: exit 0 in 1.6 s
on the current tree, exit 1 (`WALK_MISMATCH n=1`) on the pre-fix tree.

## The gate

`python3 resources/index.py check` → 0. `python3 resources/memos.py check` → 0.
`bash resources/doctor.sh /Users/feb/dev/infra/pearde` → 0, closing with
"every part this repo owns checks out". No row reports `broken`. Three report
`off`, all of them absences rather than faults: `plan` (no plan on record),
`harnesses` and `jstests` (both opt-in, not run).

## Defect outside this scope — `PBOARD`, confirmed, not fixed

The analyst's report is right. `resources/doctor.sh:594` expands `$PBOARD` in
the `view` row, and `PBOARD` is assigned nowhere in the file — it is the only
occurrence of the name. Under `set -u` that aborts the row. It is invisible on
an absolute `$START` only because `||` short-circuits: the preceding
`grep -qF "\"$BOARD\""` matches the registered absolute path, so the `PBOARD`
operand is never evaluated. On a relative `$START` the registered path does not
match `./.pearde`, the second operand is reached, and the run prints
`resources/doctor.sh: line 594: PBOARD: unbound variable`, reports
`view broken  the service is up but this board is not registered`, and exits 1.
So `doctor` exits non-zero on any relative path. Left alone, as briefed.
