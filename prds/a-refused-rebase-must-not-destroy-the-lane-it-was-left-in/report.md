Verdict: DONE

# a refused rebase must not destroy the lane it was left in

## What stands

`spec01` — 3 of 3 boxes closed. `resources/board/lanes.py`'s `merge()` now
runs `git reset --hard <was>` in the lane worktree only inside the branch
where `git rebase --abort` returned `0`. A rebase that never got under way —
`git rebase` refusing outright on the dirty tree `land_lane` leaves on paths
outside the footprint — no longer reaches the reset, so the lane keeps its
uncommitted work and the raised `LaneError` describes a tree that is still
there. A genuine mid-rebase conflict is unchanged.

The guard is built **in place in the footprint file**, not staged under
`probe/` — a branch has no meaning outside the function it lives in. It
stands in this PRD's lane worktree
(`pearde/.lanes/a-refused-rebase-must-not-destroy-the-lane-it-was-left-in/resources/board/lanes.py`),
which is where `collect` merges it from; the orchestrator's checkout still
holds the unguarded file, as it should before the merge.

This pass also finished the two items the analyst left: the probe's
temporary `echo "testing: ..."` line is gone, and the probe now takes its
tree from `PEARDE_ROOT` when the runner names one — a lane worktree carries
no board, so the old four-levels-up walk always landed in the checkout and
would have measured a tree holding none of the work.

## Boxes

| box | how it was closed |
|-----|-------------------|
| `merge()` resets only inside the `abort == 0` branch | read at `lanes.py:189-198` in the lane: `aborted = git(wt, "rebase", "--abort", check=False)` then `if aborted.returncode == 0:` with the reset indented under it. Sole `reset` in the file (`grep -n reset resources/board/lanes.py` → one line) |
| the probe prints `PASS` for both cases against the repo's own `lanes.py`, no `LANES_PY` | `PEARDE_ROOT=<lane> bash …/probe/reproduce.sh` → exit 0, `2 cases · 2 pass · 0 fail`. Same on the post-merge tree (checkout's `resources/` with the lane's `lanes.py` overlaid): exit 0, `2 cases · 2 pass · 0 fail`. Against the unmerged checkout it is red — exit 1, `FAIL: the lane's uncommitted dirt was destroyed` — which is the check proving it can fail |
| a genuine mid-rebase conflict still lands back on the pre-rebase tip | case 2, `PASS: branch/tree restored to the pre-rebase tip`, in all three runs including the one against the unguarded file — the behaviour is untouched by the change |

## Verify block

Rewritten, then run the way `collect` runs it —
`bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec01.md)"`:

- on the merged tree: **exit 0**, printing `lanes.py:192` / `lanes.py:193`
  and `2 cases · 2 pass · 0 fail`.
- with one footprint file mutated (the guard reverted to the unconditional
  `rebase --abort` + `reset --hard` pair): **exit 1**. Restored by `cp` from
  a scratch dir outside the repo and proved back with `cmp` (exit 0);
  re-run after the restore: exit 0.
- the mutation above proves the counter is wired. The behavioural half is
  the block's last line run against the unguarded `resources/board/lanes.py`
  that is still in the checkout: exit 1 on `FAIL: the lane's uncommitted
  dirt was destroyed`.
- `pearde specced … --check --as impl-lane-rebase` → `ok · complexity 8 ·
  footprint resources/board/lanes.py`, one expected warn (3 of 3 boxes
  ticked — this pass ticked them).

Two defects in the block as it stood were repaired under step 5's
`Fails when` table, which the second pass applies to blocks that already
stand:

- it named `prds/…/probe/reproduce.sh`, a path that does not resolve from
  the root `collect` runs a spec block in. `collect.py:1336` runs each block
  with `cwd = repo_of(prd, …)`, which for this board is the checkout
  `/Users/feb/dev/infra/pearde`, not the board — so the path is
  `pearde/prds/…`. As written the block died on the first command with
  every box ticked.
- the probe's assertions were `grep -q … && echo PASS || echo FAIL`, which
  exits 0 whichever branch runs. The probe now keeps a tally, prints
  `N cases · P pass · F fail`, and ends on `[ "$FAILED" = 0 ]` — a floor,
  not a locked total.

## Harness baseline and re-run

Taken before the first edit of this run, both roots named.

| harness | root | baseline | re-run |
|---------|------|----------|--------|
| `prds/collect-must-not-reset-the-checkout-it-did-not-write/probe/verify.sh` | checkout | `31 checks · 31 pass · 0 fail`, exit 0 | identical |
| same | `PEARDE_ROOT=<lane>` | `31 checks · 23 pass · 8 fail`, exit 1 | identical |
| `python3 resources/index.py check` | checkout | exit 1, 3 lines | identical |
| `python3 resources/index.py check` | lane | exit 1, 2 lines | identical |
| `python3 resources/memos.py check` | checkout | exit 0 | identical |
| `bash resources/doctor.sh` | checkout | exit 1, `health broken` | exit 1, `health broken` |
| `find pearde/prds -name verify.sh \| wc -l` | checkout | 61 | 61 |

No other board harness reads the footprint: `grep -ln
'resources/board/lanes\.py\|lanes\.merge\|import lanes'` over all 61 names
only the row above. The four harnesses that enumerate the board
(`grep -l 'find.*verify\.sh'`) read `verify.sh` files; this PRD's probe is
`reproduce.sh` and its footprint is outside the board, so they read nothing
of mine — the count 61 is unchanged either way.

Doctor's only moved rows are `board 120 → 121 PRDs`, `memos 32 → 33`,
`vision 14 → 15 off`, `origin 223 → 224` and the `statusline` count. None
names my footprint; a sibling session landed a PRD and a memo mid-run. The
`health` row was `broken` **before the first edit** — two rankings naming
files no longer tracked, and a ranking older than the graph. It is a
finding, not mine.

## Findings

1. **Sixty harnesses cannot find the board by its own name.** The shared
   header walks up until `basename == .pearde`; the board is `pearde/`
   since 92e318c, so the walk runs off to `/` and `ROOT` becomes `/`. The
   set only works through the legacy `.pearde` symlink. Measured on
   `prds/collect-must-not-reset-the-checkout-it-did-not-write/probe/verify.sh`:
   `31 pass · 0 fail` invoked as `.pearde/prds/…`, `11 pass · 20 fail`
   invoked as `pearde/prds/…` — the same file, the same tree. Every
   harness-sweep number on this board is currently a property of which
   spelling the sweeper used. Owed to whichever PRD owns the sweep, not to
   this one.
2. **66 spec files run a verify-block command on a bare `prds/…` path.**
   `collect` runs spec blocks with `cwd` = the code checkout (`collect.py`,
   `repo_of`), where the board is `pearde/`. Those blocks die on their first
   command with every box already ticked — the same defect this PRD's own
   block carried. `grep -rl '^\(bash\|python3\) prds/' pearde/prds
   --include='spec*.md' | wc -l` → 66.
3. **The lane is two commits behind the checkout** (lane base `3587817`,
   checkout `3664de0`). The parent PRD's harness is 8/31 red under
   `PEARDE_ROOT=<lane>` purely because the lane's
   `resources/board/collect.py` predates `e5abc5b`, which is that PRD's own
   landing. Every one of those reds closes on the merge; none is a live
   finding, and nothing was added in the lane to silence them.
4. `resources/index.py check` is red in both roots before the first edit —
   `references/skills/pearde-machine.md` with no row in
   `references/files.md`, `@references/personas/writer.md` and
   `@questions.py` not on disk. None in this footprint. The
   `personas/writer.md` line is in the checkout only, so it arrived after
   the lane was cut.

## Workflow probe-then-spec

| step | atomic | outcome |
|------|--------|---------|
| 1 | `read-the-contract` | pass. `prd.md` body is still the untouched template — the contract is carried entirely by `specs/spec01.md` and the analyst's `report.md`. Footprint `resources/board/lanes.py` opened in both roots; `git status --short` recorded in checkout (clean), lane (` M resources/board/lanes.py`) and board before the first edit |
| 2 | `capture-the-harness-baseline` | pass. Set and counts in the table above, both roots |
| 3 | `attempt-the-build` | pass, as the route's second pass. The guard already stood from the analyst's build; this pass finished the two items the spec named as left and repaired the probe's exit. Nothing was rebuilt to have something to do, and no red-to-green on `lanes.py` is claimed for this pass |
| 4 | `re-run-the-harnesses` | pass. Every count equal to its baseline |
| 5 | `write-the-specs` | pass, as the second pass: no spec authored, the `Fails when` table applied to the block that already stood (two rows fired — the unrunnable path and the `&&…\|\|` shape) and the boxes ticked as they closed |

No back-edge was taken.

### Edits

Two rows the atomics do not cover, offered as replacement text.

**`capture-the-harness-baseline`, `## Fails when` — a new row.** The
existing lane row assumes the harness walks up from `$0`; this board's
harnesses walk up looking for a directory *named* `.pearde`, and the board
has been renamed:

> | a harness walks up for a directory named `.pearde` and the board is on
> another name | the board was unhidden and the walk runs off to `/`, so
> `ROOT` becomes `/` and every count the harness prints is a property of
> which spelling invoked it | run the same harness through both spellings
> before recording anything — a set that reads differently through a
> symlink and through the real path has no baseline yet, and the
> difference is the finding |

**`write-the-specs`, `## Fails when` — a new row.** The section says to run
the block the way `collect` runs it, but never says from *where*, and the
relative path is the half that breaks:

> | every command in the block passes from the board, and the block dies on
> its first line under `collect` | `collect` runs a spec block with `cwd` =
> `repo_of(prd, …)` — the **code checkout**, not the board — so a path
> written `prds/<prd>/…` names nothing and a path written
> `<board>/prds/<prd>/…` is the one that resolves | spell every board path
> in a block from the checkout root, and run the block with `cd
> <checkout>` before quoting its exit. `awk`-ing the block out and running
> it from the PRD's own directory proves nothing about the exit `collect`
> will see |

## Knowledge

Nothing was learned outside this repo, so there was nothing to `remember`.
The analyst's pass already recorded the query gap at
`pending/260902-47af.md`.

## Scores

complexity: 8
blast-radius: mid
workflow: probe-then-spec
