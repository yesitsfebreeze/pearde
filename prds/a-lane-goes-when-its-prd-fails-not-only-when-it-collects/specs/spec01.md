---
complexity: 14
footprint:
  - resources/board/transitions.py
  - resources/board/lanes.py
---

# spec01 — `release <prd> failed` drops the lane like `sweep` does

`cmd_release` in `resources/board/transitions.py` only called
`transition(...)` — a PRD moved to `failed` that way kept its worktree and
branch standing forever, unlike the silent-reclaim path inside `cmd_sweep`,
which already calls `drop_lane` on the same edge. This unit makes the two
paths agree, and adds the second half R1 asks for: the `lane/<slug>` branch
goes too, but only when `## Failure` says this run is not to be retried and
only when the drop actually carried the lane's work onto that branch.

What stands, on `lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects`:

- `lanes.delete_branch(board, repo, slug, force=True)` — deletes
  `lane/<slug>` and **returns the sha it pointed at**; `None` when there was
  no such branch, `LaneError` the way git raises. The sha is returned
  because deleting the ref takes that branch's reflog with it: the
  checkpoint `drop_lane` just made is then reachable only through
  `git fsck --lost-found`, and the caller prints the sha so the drop stays
  recoverable.
- `transitions.not_to_be_retried(prd)` — `True` when the PRD's `## Failure`
  section matches `NO_RETRY_RE` (`not (to )?be retried`, case-insensitive).
- `cmd_release`: on `to == "failed"` and not `--dry`, calls
  `drop_lane(board, rel, who="release")` unconditionally — worktree gone,
  checkpoint-committed if dirty, branch kept, exactly `sweep`'s behaviour.
  Then, when `not_to_be_retried` is true **and** the drop kept the work,
  `lanes.delete_branch` and a line naming the tip and why. When the drop did
  **not** keep the work it says so and keeps the branch.
- `drop_lane` returns `sha is not None or not left` instead of a bare
  `True`: `False` now also means "paths went uncommitted because the
  checkpoint failed". That is the only signal a caller about to delete the
  branch can read — the branch is then the one place the work is *not*, and
  deleting it destroys the last copy. No existing caller reads the return,
  so `sweep` is byte-identical.
- `drop_lane` takes `who=` (default `"sweep"`) so its progress lines and its
  checkpoint commit message name the edge that dropped the lane, not `sweep`
  when `release` did it.
- `drop_lane`'s docstring (R2): names `release <prd> failed` beside `sweep`
  as the two edges that drop a lane, and says why the branch rule differs —
  a state nobody is about to keep writing in is what makes the worktree safe
  to take, and only `## Failure`'s own words say the branch itself is not
  needed either.

The probe is `probe/verify.sh` (renamed from `probe.sh`, which the board's
harness sweep — `find prds -name verify.sh` — could never see) and takes its
tree the way every other harness on this board does: `PEARDE_ROOT` when the
runner names one, the board's own repo otherwise. It no longer names an
absolute lane path that stops existing the moment this PRD collects.

## Acceptance

- [x] On a probe board: claim → release failed with a `## Failure` saying
      not to be retried → `git worktree list` shows no lane and `git
      branch` no `lane/<slug>`.
- [x] Same without the marker → worktree gone, branch kept.
- [x] `release <prd> failed --dry` leaves the worktree, the branch and the
      state untouched (no write happens on a dry run).
- [x] `drop_lane`'s docstring names `release <prd> failed` as the second
      edge that drops a lane, and says why the branch rule differs.
- [x] The deletion line names the sha the branch pointed at, so the
      checkpoint is recoverable through `git fsck` after the reflog goes.
- [x] A drop whose checkpoint could not take keeps the branch **despite**
      the marker, and says why.

## Verify and Proof

```sh
B=.pearde; [ -d "$B/prds" ] || B=pearde
bash "$B/prds/a-lane-goes-when-its-prd-fails-not-only-when-it-collects/probe/verify.sh"
```

Run 2026-09-04 from the merged tree (`git clone --shared --branch
lane/<slug>`, board symlinked in), block exit 0:

```text
PASS: case 1: lane cut before release
release: case-one lane removed · branch lane/case-one kept
release: case-one branch lane/case-one deleted at 949c0589f141 — `## Failure` says no retry; the checkpoint is reachable through `git fsck --lost-found` until gc
PASS: case 1: worktree gone
PASS: case 1: the deletion names the tip it dropped
PASS: case 1: branch deleted
release: case-two lane removed · branch lane/case-two kept
PASS: case 2: worktree gone
PASS: case 2: branch kept
PASS: case 3: --dry keeps the worktree
PASS: case 3: --dry keeps the branch
PASS: case 3: --dry keeps the state
PASS: case 4: drop_lane's docstring names `release <prd> failed`
release: case-five checkpoint failed — error: gpg failed to sign the data:
release: case-five lane removed · branch lane/case-five kept · 1 uncommitted path(s) dropped
release: case-five branch lane/case-five kept despite `## Failure` — the drop did not take the lane's work with it, and the branch is all there is left
PASS: case 5: worktree gone
PASS: case 5: a failed checkpoint keeps the branch
PASS: case 5: and says why
13 checks · 13 pass · 0 fail
```

Every check was shown to be able to fail: four mutations of
`resources/board/transitions.py` (backed up outside the repo, restored,
`cmp` identical) — dropping the `--dry` guard reddened case 3 (2 fail),
`if False:` on the whole block reddened cases 1 and 2 (3 fail), reverting
the docstring reddened case 4 (1 fail), and forcing `kept = True` reddened
case 5 (2 fail).
