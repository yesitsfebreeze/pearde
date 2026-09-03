---
atomic: capture-the-harness-baseline
subject: record what every committed harness prints before the tree is touched
date: 2026-08-28
updated: 2026-09-02
runs: 82
tags:
  - atomic
---

# capture-the-harness-baseline — the numbers as they were before you

## Do

1. Locate the board root first — it is the `.pearde/` at or above the
   `repo:` root, and it is often **not** the repo. Then
   `find <board>/prds -name verify.sh | sort` for board harnesses, and
   separately identify the *code* gate the PRD's own `verify:` key names.
   On a board inside a code repo these are two different harness sets and
   only the second usually reads the footprint.
   A fixed glob list aborts on the first depth that
   has no match, and under a shell with `nomatch` it prints nothing at all.
   Then name the tree the set is to measure. Most board harnesses take their
   root from `PEARDE_ROOT` and fall back to the board's own repo, which is
   always the orchestrator's checkout — so a worker building in a lane runs
   `PEARDE_ROOT=<lane> bash resources/doctor.sh --harnesses <board>`, or
   exports `PEARDE_ROOT=<lane>` before running one by hand. Not all of them
   do. `grep -L PEARDE_ROOT $(find <board>/prds -name verify.sh)` names the
   ones that do not, and every count from those is the checkout's however you
   invoke them — record them as measuring another tree, and never claim a flip
   on one. Without it the baseline you record and the re-run you compare it
   against are both the checkout's, the lane's build is invisible to every
   number, and the comparison is empty.
2. Run each one that reads a path in your `footprint:` — grep each harness
   for the footprint paths spelled from the repo root (`references/settings.md`,
   not `settings.md`: a bare board filename matches every fixture that writes
   one) — each one whose PRD is named in `needs:`, and each one that runs
   `git status` or `git diff` at the repo root, because that reads every
   footprint. Record the exact count it prints, verbatim, and `git status
   --short` beside it: the untracked files a root-level check sees are the
   only way to tell your drop from a neighbour's later. Save each harness's
   whole output to a scratch file, not only its count — when a count moves you
   need the FAIL line, and the machine may sleep before you can re-run it. Write them under a subdirectory named for this run — the scratch directory is shared across sessions, and a bare `grep FAIL <scratch>/*` sweeps another worker's outputs in with yours. Record the mtime and `git diff -U0 | grep -c '^@@'` of every file outside your footprint that a spec says it stands on — a predicate in a sibling's file moves during the run, and the number beside each run is the only way to say which plan.py a count was taken against. A harness that **enumerates** the board — `find … -name verify.sh`, a glob over `prds/`, a census — reads every footprint that is itself a file it enumerates, and spells none of their paths. Grep will not find it. Add every harness matching `grep -l 'find.*verify\.sh' $(find prds -name verify.sh)` to the baseline set whenever any footprint path lies under the board.
3. Record the repo's own gate the same way — **its exit code as well as its
   lines**. The gate is whatever the PRD's `verify:` key names, or the
   repo's documented one (`just all` here, `python3 resources/index.py check`
   + `bash resources/doctor.sh` on a pearde board). Do not assume the pearde
   pair exists; check before running. The lines they print now, plus any line the contract itself
   adds (a new doctor row, a new file the map will name), are the lines you are
   allowed to still see at the end; name each added one in the report.
4. A harness that is already failing is recorded as failing before your first
   edit. It is a finding, not yours to fix.

## Done when

- Each harness that touches a footprint path has a recorded count, quoted.
- The recording happened before any file *this run* writes — `git status
  --short` at this point lists nothing you added in this session.
- **Resuming a killed run, or taking a second pass at a footprint another
  worker already built:** if the earlier build is **uncommitted**, the
  pre-edit tree is still on disk and the baseline is recoverable — do not
  inherit it. `git clone --no-hardlinks` recovers the pre-edit tree
  only where the harnesses are tracked **in the repo you cloned**. Before
  concluding they are not, check the board's **own** history: a board at
  `.pearde/` is normally a separate repo or a **linked worktree**, so the
  parent repo ignoring that path says nothing about whether the board's
  files are tracked. `git -C <board> rev-parse --show-toplevel`, `git
  worktree list` and `git -C <board> ls-tree -r --name-only HEAD` answer it.
  Measured on this board: the parent's `.gitignore` ignores `.pearde/` and
  the board's own `HEAD` still holds 49 harnesses, so `git -C <board> show
  HEAD:<path>` returns them and a real pre-edit baseline was always
  available. Only where the board's own history genuinely lacks a file do
  you copy the working tree to scratch and restore your own footprint files
  from `HEAD` there — that reverts your build and keeps every neighbour's,
  **but only where no neighbour has hunks in a file of yours. Check first:
  `git diff -U0 -- <footprint path>` and read the hunks. Where a file is
  shared, restoring it from `HEAD` reverts their work as well and the copy
  is not a baseline for anything that reads it — say so, and fall back to
  comparing the two copies row by row for the rows your own hunks touch,
  which is the comparison the control copy makes honest** —
  then run a control copy with nothing reverted: a harness that reads the
  repo's own git history fails in any copy, and only the control tells that
  apart from a regression. Only when the earlier build was **committed** is there no
  pre-edit baseline: then record the tree as it stands, cite the earlier
  worker's numbers, and say in the report that the baseline is inherited. A
  number honestly labelled inherited is worth something; a number that
  could have been re-taken and was not is worth less than it looks.
  Where the earlier pass **published its counts** and the harnesses are
  deterministic, a cheaper and safer confirmation is to re-run the same set
  on the built tree and show every count equal to the published one: a
  matching set confirms the inherited baseline without a window in which the
  tree is half-reverted. Say in the report that the baseline is inherited and
  confirmed, and name the pass it came from. Revert only when the counts
  disagree or none were published.
- Any pre-existing failure is written down with the words "before the first
  edit" beside it.

> A count published by the previous pass of this same route is the count as of
> the moment it was taken, not as of that pass's final tree — a pass that
> re-writes a probe after running the census publishes a stale number in good
> faith. Before calling a difference a regression, compare the **mtime** of the
> harness and of every file it reads against the timestamp of the pass that
> published the count. Where the harness has not moved and a file it reads was
> written after the count was taken, the difference is inside the earlier pass,
> and it is neither a landing nor yours.

## Fails when

| seen | means | do |
|------|-------|----|
| the baseline `git status --short` list is *shorter* at step 5 than at step 2, and a footprint path you never staged is now clean | a sibling session committed while you ran; those paths are theirs, landed | `git log --oneline` for the new HEAD and `git log -1 -- <your footprint path>`; if your path's last commit predates your run, your hunks are intact and uncommitted. Record the new HEAD in the report — a shrinking dirty list is another session finishing, not your edits vanishing |
| `index.py check` or `doctor` prints lines at step 4 that were not there at step 2 and name files outside your footprint | parallel workers moved the baseline under you | count as yours only the lines naming your footprint; quote the rest beside the baseline as inherited |
| `no matches found` or `No such file or directory` from the listing | a glob names a depth this board has no harness at | list with `find prds -name verify.sh` — it prints what exists and exits 0 |
| the listing is empty on a board that has harnesses | the shell aborted the whole command on the first empty glob | same |
| `doctor` at step 4 differs from step 2 only on the `statusline` row | that row carries the tree's dirty-file count, which every live session moves | compare doctor's rows without `statusline`; the count is nobody's finding |
| **every** harness you baseline is red, and the failing lines share one cause outside your footprint | a layout or path migration landed between spec-writing and dispatch; the harness set is measuring the migration, not your unit | record the shared cause once instead of per-harness, verify your own contract items by hand on a fixture, and report the sweep that repairs the set as its own PRD — do not repair a subset, a half-swept harness set is worse evidence than a uniformly red one |
| a failing line the brief names as inherited is **absent** when you take your own baseline, and harness rows it was reddening are green | a sibling closed it between the brief being composed and your first command; the brief's baseline is older than the tree | take your own baseline as the measurement and say in the report that the brief's line is gone and who closed it — `git status` in both roots names the file. Every harness row that line was reddening is that sibling's flip, not yours: the same rule as a count that went up |
| `command not found: timeout` from a harness wrapper on **darwin** | `timeout` is GNU coreutils and is not on the base system | drop the wrapper, or `gtimeout` where coreutils is installed — and read the exit code of the wrapper, not only the harness's last line |
| every board harness computes its own `ROOT` by walking up from `$0`, and the `repo:` root is a lane | the harness set is nailed to the orchestrator's checkout and can never read a lane; a worker's build is invisible to all of it until `collect` merges | build the merged tree in scratch — `git clone --shared <checkout> <scratch>` (a `git archive` or `git init` copy loses the history a pinned-sha harness reads), `git apply` the checkout's uncommitted diff, overlay the lane's files — then symlink `<scratch>/.pearde` to the live board and run each harness **through that path**, so its own `cd …/../../../..` resolves to the merged tree. The symlink alone is not enough: `grep -l "pwd -P" $(find <board>/prds -name verify.sh)` first, and for every harness it names — and for every harness that honours it — export `PEARDE_ROOT=<scratch>` on the run, because `pwd -P` resolves the symlink back to the live board and the harness then measures the orchestrator's checkout while printing a count that looks like yours. Say in the report that the counts are the merged tree's, not the lane's, and name any harness that could be pointed at neither |
| a harness scores worse on a merged tree built by `git archive`/`git clone` than on the live checkout, and the extra failures name a board path | the board directory is gitignored, so it is in the checkout and not in the archive — the difference is the missing board, not the build | never compare an archive tree to the checkout. Build **both** sides the same way — `git archive main` into one scratch dir and the merged tree into another — and compare those. Do not symlink the live board into the scratch tree to close the gap: `pwd -P` resolves it straight back to the live board and the score gets *worse*, measured here at 35 pass against 36 |
| the earlier build is uncommitted in a **lane**, and that pass published no counts | the pre-edit tree is the lane's own `HEAD`, and it is a whole tree, not a file to restore | `git clone --shared <lane> <scratch>/pre` and run the set with `PEARDE_ROOT=<scratch>/pre`. It is a real pre-edit baseline, taken without a window in which the live tree is half-reverted and without touching a neighbour's hunks in a file of yours. Compare the failing **sets**, not only the counts: a subset proves no harness went green-to-red even when the count is noisy |
| a repo-wide reference gate (`index.py check`) is red in the lane on a line naming an `@pearde/…` or `@.pearde/…` target, and green in the checkout | `lanes.create` cuts the lane deliberately without the board, so every reference from a tracked file into the board dangles there by construction — this never closes on a merge and is not a defect in the file | baseline the gate in both roots and quote both. A line whose target is under the board is the lane's missing board and nothing else; count only the lines whose target exists in the checkout. Do not add the board to the lane to silence it — a second board under a lane is a board the scan will find |
| the harness sweep is baselined with a board symlinked into the lane, and re-run without it | the symlink is inside the tree the sweep measures: a harness asserting about `<root>/pearde/…` sees the real board where it expects a lane's stub, and a harness reading the git store sees the lane's | measured here: `a-lane-s-wiki-is-a-stub-…` exits 1 with the symlink and 0 without, and `list-the-collects-the-repo-bug-orphaned` names the lane's `worktrees/-pearde`. Take both baseline and re-run with the scaffolding in the same state, name the state beside every count, and take the deciding count at the root `collect` will use |
