Verdict: DONE

# A check for the reading list — implementer report

Second pass on `probe-then-spec`. The probe's build was already in the lane;
this pass measured it against `spec01`'s six boxes, found two defects that
made box 1 false, fixed both in the footprint, extended the probe to catch
them, and repaired one acceptance check that could not fail. All six boxes
are ticked with output quoted below.

## Boxes

All 6 of spec01 closed. Every tick was taken as its check ran.

| box | evidence |
|---|---|
| bare row fails, names the row, does not modify the file | `ok bare row fails (exit 1)` · `ok non-GitHub bare row named by its link text` · `ok failing run left the content alone` · `ok failing run left the mode alone (644)` |
| exits 0 with mappings, marks archived rows in place | `ok archived+active mix exits 0` · `ok archived row marked in place` · `ok active row left alone` · `ok marking run kept the list's mode (644)` · real list: `reading: 17 repo(s) checked against state, 0 marked stale`, exit 0 |
| second run idempotent, no re-lookup | `ok second run is idempotent` |
| snapshot resolves without a network call | `ok snapshot-first guard held — no network call` (stubbed `gh` logs any call, log absent) |
| `doctor.sh` gains no scout row | `grep -n 'scout' resources/doctor.sh` — no output; doctor's only `scout` string is the pre-existing `pearde-scout` skill name on the `skills` row, identical before and after |
| README names the verb | four-layers overview line 10, `### scout.sh reading` section, and the `## Layout` command table row for `scout.sh` (this pass added the table row — see Findings) |

`## Verify and Proof` block, run verbatim from the repo root the way `collect`
runs it (`bash -e -o pipefail`, cwd = code repo): **exit 0**, `verify: all
checks passed` (10 checks), `grep -c 'reading' resources/scout/README.md` → `11`.

## Findings

Two defects in the probe's build. Both were inside `cmd_reading`, both made
acceptance box 1 false, and neither was visible to the probe as written.

**1 — a non-GitHub row killed the whole run, silently.** `scout.sh` runs under
`set -euo pipefail`, and the repo name is parsed with

```sh
repo=$(printf '%s' "$line" | grep -oE 'github\.com/[^)]+' | head -1 | sed 's#github\.com/##')
```

A row that links anywhere but GitHub makes `grep` exit 1; under `pipefail` the
assignment fails and `-e` aborts the function mid-file — no output at all, and
an exit status a caller cannot tell from a bare-row failure. Today's
`reading-list.md` is 17/17 GitHub rows, so the branch had never been reached;
adding one off-GitHub fixture row reproduced it immediately (whole run printed
nothing, exit 1). Fixed with `|| true` on the pipeline: no match here is a
normal row, not an error.

**2 — every run made `reading-list.md` mode 0600.** The write-back was
`mv "$tmp" "$list"`, and `$tmp` is a `mktemp` file — so the list took the temp
file's 0600 mode and inode on *every* run, including a run that changed
nothing and a run that failed on a bare row. Box 1 contracts "without
modifying the file". Git does not track the mode below the executable bit, so
nothing on the board would ever have reported it. It had already fired: the
lane's `resources/scout/reading-list.md` was `-rw-------` against `644` for
every sibling file, from the probe's own rehearsal. Fixed to write back only
when a row was actually marked, through `cat "$tmp" > "$list"`, which keeps
the list's own mode and inode. The lane's file was `chmod 644`'d back to match
its siblings — a mode restore, no content write, on a file outside the
footprint; named here rather than left.

**3 — a bare row with no GitHub link went unnamed.** Box 1 says "names every
row"; the bare-row message printed the parsed `owner/repo`, which is empty for
such a row, so it named a blank line. Added a fallback to the row's link text.

**4 — box 5's check could not fail.** The block's last line was
`grep -n 'scout' resources/doctor.sh || true   # empty: still not a doctor row`.
The `|| true` makes it exit 0 whatever it finds: a doctor row could land and
the block would still pass. Rewritten as
`if grep -q 'scout' resources/doctor.sh; then echo '...'; exit 1; fi` — the
`!`-prefix form is not used, per `write-the-specs`' own row on `set -e` and
inverted status. Mutation-tested: with `# row: scout` appended to a scratch
copy of `doctor.sh`, the line prints and exits 1.

Carried forward from the analyst's pass, unchanged and still true: the repo
full name must come from the URL rather than the link text
(`[cargo-mutants](.../sourcefrog/cargo-mutants)`), and an unresolvable repo is
left unmarked rather than called stale.

### Defects outside this scope, not fixed

- `prds/every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh`
  exits **2** before and after this pass: it `cd`s to a hard-coded lane
  (`/Users/feb/dev/infra/pearde/pearde/.lanes/every-document-…`) that no
  longer exists. It reads `resources/scout/README.md`, so it is in this
  footprint's harness set and can measure nothing. Recorded as failing before
  the first edit; not this PRD's to repair.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | pass — PRD, `spec01.md`, `probe/verify.sh` read; `git status --short` recorded in both roots before the first edit |
| 2 | capture-the-harness-baseline | pass — see Baseline |
| 3 | attempt-the-build | pass — second pass, so this re-measured the standing build rather than authoring one; two defects found and fixed in place in the footprint file, per the atomic's rule that a guard has no meaning outside the function it lives in |
| 4 | re-run-the-harnesses | pass — no harness went green-to-red; the only moved numbers are board census counts a sibling session moved |
| 5 | write-the-specs | pass — second pass, so its `Fails when` table was applied to the blocks that already stand; row "a check that cannot fail" fired, finding 4 |

No back-edge was taken. No workflow file was edited.

### Edits

None. No atomic on this route named a wrong command, a stale path, a check
that cannot fail, or a shape its `## Fails when` does not list.

## Baseline

Taken before the first edit, and re-taken after.

| gate | before | after |
|---|---|---|
| `python3 resources/index.py check` (lane) | exit 1, 3 lines | exit 1, same 3 lines, byte-identical |
| `python3 resources/index.py check` (checkout) | exit 0, no output | not re-run — no edit landed in the checkout |
| `bash resources/doctor.sh` (lane) | exit 1 | exit 1, same rows |
| `python3 resources/memos.py check` (lane) | exit 1, memos missing `tags:` | unchanged, no `scout` line |
| prose-density harness | exit 2 (`cd` to a missing lane) | exit 2, identical |

The lane's three index lines — `resources/common.py` with no row in
`references/files.md`, and `hotreload-test.js` referenced twice but absent —
are the lane's older `HEAD`, name nothing under `resources/scout/`, and are
unchanged. Doctor differs from its own baseline only on census rows the live
board moved under this run: `223 → 224 PRDs`, `93 → 96 harnesses`,
`110/179 61% → 110/180 62%`. None names a footprint path; a sibling session
filed those, per `capture-the-harness-baseline`'s row on parallel workers
moving the baseline.

The `## Verify and Proof` block needs a board at `.pearde/`, and the lane has
none. It was run through a temporary `<lane>/.pearde` symlink to the live
board (both spellings are gitignored), and the symlink was **removed** after
the run so the lane is handed back in the state it was received. `collect`
runs the block with the code repo as cwd after landing the lane, where
`.pearde/` exists, so it needs no scaffolding there.

## Tree

Lane `lane/a-check-for-the-reading-list`, `git status --short`:

```
 M resources/scout/README.md
 M resources/scout/scout.sh
```

Exactly the spec's footprint, and the same two paths that were dirty when this
pass started — nothing else in the lane moved. On the board,
`prds/a-check-for-the-reading-list/` is untracked in full; the six other dirty
`spec01.md` files under `prds/` are other sessions' and were not touched.

## Health

The brief names no footprint file under the health floor, and `health.py show`
has no note for either footprint path. `cmd_reading` grew by 12 lines, all
comment or guard; nothing was split.
