---
state: done
origin: requested
priority: 85
complexity: 32
blast-radius: mid
needs:
  - common-py-gains-a-git-runner-and-a-section-extractor
workflow: probe-then-spec
actual: 0.94h
commit: a55a685 12f6432
---

# the-top-level-resources-modules-delegate-to-common — resources/guard.py`, `health.py`, `knowledge.py`, `questions.py` and `workflows.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`.

resources/guard.py`, `health.py`, `knowledge.py`, `questions.py` and `workflows.py` hold no second definition of a primitive; each keeps its own behaviour on failure through a one-line delegation into `common.py`.

## Report

spec01: exit 0
a55a685
None
None
PASS: health._git, questions.find_board, questions.sections (0/226 prds diverge), workflows.find_board, workflows.section (120 checks), knowledge.parse_frontmatter (1 known/618 wiki notes diverge)

spec02: exit 0
no-work-is-lost-on-the-board/a-lane-rebases-before-collect: `## Answers` with no `## Questions` above it — an answer to a question nobody wrote down
the-board-is-a-real-directory-at-pearde-never-a-symlink/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind: `## Answers` with no `## Questions` above it — an answer to a question nobody wrote down
the-board-reclaims-dead-work-by-itself/a-worker-survives-the-window-that-launched-it: `## Answers` with no `## Questions` above it — an answer to a question nobody wrote down
      13
PASS: health._git, questions.find_board, questions.sections (0/226 prds diverge), workflows.find_board, workflows.section (120 checks), knowledge.parse_frontmatter (1 known/618 wiki notes diverge)

spec03: exit 0
# probe-then-spec — build it first, then write down what it takes

## Use when

- A PRD is `open` and needs specs before anyone can be sent at it.
- A PRD came back `refine` and a child now needs its own specs.
- Not when the specs already exist — that is `implement-a-spec`.
- Also when the specs **do** exist and an implementer is dispatched on this
  same route — the second pass. Steps 3 and 5 are then not build-and-spec
  work: step 3 re-measures and step 5 applies its `Fails when` table to the
  blocks that already stand, without authoring a spec. Step 3's `Fails when`
  table says so; this list should not read as excluding the case that table
  handles.
- Not when the contract is still a title and a hope: nothing here interviews a
  person, and a build against a vague contract produces questions nobody asked
  for.
- The three verdicts, and the rule that a question must be a fork the build
  actually hit, are @references/parts/workers.md. This route orders the steps
  and restates none of that.

### 1 — read-the-contract

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | `read-the-contract` | the answers already on the PRD close forks you would otherwise ask back | `stop` |

#### Do

1. `cat prds/<prd>/prd.md`. Read the body, and `## Answers`, `## Questions`
   and `## Failure` if they are there — an answer already on the file closes
   a fork you would otherwise ask again.
2. `ls prds/<prd>/specs/` and read every file it lists. A spec's own
   `workflow:` and `footprint:` override the PRD's for that unit, and its
   `## Verify and Proof` block is the command set for it.
3. Resolve every `@<path>` and `@@<keyword>` the body cites and open it. `@`
   is a path from the skill root; `@@` is a row in `index.md`, and the first
   anchor in that row is the file that answers the question.
4. `git status --short`. Write down which paths are already modified — that
   list is the only thing that later tells your hunks from someone else's.
5. Write down the `footprint:` paths and, for each, whether it exists yet.

#### Done when

- Every `@` and `@@` in the body resolved to a file that exists, or the
  dangling one is named in the report.
- Every path in `footprint:` has been opened, or is stated as not yet on disk.
- The `git status --short` list is recorded before the first edit, not after.

#### Fails when

| seen | means | do |
|------|-------|----|
| the coordinator reports the PRD body changed while you were building | the contract moved; the build stands on the old text | re-run this step on the new text, keep the build, name both reads in the report |
| `git status --short` lists paths the brief did not | the tree is live; other sessions wrote since the brief | record what you see now — that list, not the brief's, tells your hunks from theirs |
| a `footprint:` path is absent under the `repo:` root | the board is a `.pearde/` inside a code repo, and the footprint spans both | resolve each entry against the board root and the checkout above it, take whichever holds it, and record `git status --short` **in both** — one root's clean tree says nothing about the other's |
| a `footprint:` path does not exist and no sibling is writing it | a layout change moved the file after the specs were written | `find <board> -name '<basename>'`; if exactly one match, take it as the same file, do the contracted work there, and name both spellings in the report — a missing footprint path is a stale spelling far more often than a file to create |
| an edit aimed at `specs/spec01.md` does not find its anchor | every PRD numbers its specs from 01, so a footprint that names another PRD's files puts two identically-named `spec01.md` one directory apart — and this PRD's footprint is entirely inside another PRD's folder | anchor every spec edit on the box's own text and `assert` it before writing; then `git status --short -- prds/<other-prd>/specs/` to prove nothing landed in the neighbour. Never address a spec by number alone |
| the `repo:` root is a worktree under `<board>/.lanes/`, `git status --short` in it is empty, and the brief says the probe's uncommitted code is already there | `lanes.create` cuts the lane off the code repo's **HEAD**, so it carries nothing the orchestrator's checkout has not committed — and with a dirty checkout that is every uncommitted pass before yours, your own included | `git -C <checkout> status --short` and `git -C <checkout> diff -- <each footprint path>`. Read the hunks: where they are entirely this PRD's, copy those files into the lane and continue there, and say in the report that the merge will refuse until the orchestrator runs `git -C <checkout> checkout -- <path>` on each file whose lane copy is a strict superset. Where a hunk is a neighbour's, leave it in the checkout and do not carry it |
| the `repo:` root is a lane, and no `footprint:` path exists under it at any depth | the footprint is board paths, and the board is a repo of its own that the lane is not a worktree of — there is nothing to copy in and nothing to merge out | work in the board repo directly, at the path the spec's `## Verify and Proof` block `cd`s to, and say so in the report. Do not create the missing tree in the lane: a second `prds/` under a lane is a board the scan will find |
| `prd.md`'s body is the unedited template — the angle-bracketed request block, no prose | the PRD was filed from a finding rather than written, and the contract lives elsewhere: in `specs/`, in a previous pass's `report.md`, or in the `report.md` of the PRD this one answers | take those as the contract and name in your report which file you read it from. Do not ask the fork back: a placeholder body is not a missing answer, it is a PRD filed by the board rather than by a person |
| the `repo:` root is a lane and a spec's `## Verify and Proof` block spells `pearde/prds/…`, or runs a command that resolves a board | `lanes.create` gives the lane no board, so the block cannot run there and every board-rooted command in it answers about the checkout | symlink the live board in at `<lane>/pearde` (both `/pearde` and `/.pearde` are gitignored) **and read the next row before you baseline anything** |

### 2 — capture-the-harness-baseline

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 2 | `capture-the-harness-baseline` | the probe moves the tree, and nothing afterwards can tell you which edit moved a number | `→ 1` |

#### Do

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

#### Done when

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

#### Fails when

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
| the earlier build is uncommitted in a **lane**, and that pass published no counts | the pre-edit tree is the lane's own `HEAD`, and it is a whole tree, not a file to restore | `git clone --shared <lane> <scratch>/pre` and run the set with `PEARDE_ROOT=<scratch>/pre` — and `ln -s <board> <scratch>/pre/.pearde` before the first run. A lane under `<board>/.lanes/` resolves the live board by walking up and a clone in scratch does not, so every board-reading gate answers about a board that is not there — measured here: `grammar.py check` reddens on ``references/grammar.md: no `---` frontmatter fence`` in the clone and is silent in the lane on identical bytes, and goes silent in the clone the moment the board is linked in. Link it in both trees or neither, and say which in the report. It is a real pre-edit baseline, taken without a window in which the live tree is half-reverted and without touching a neighbour's hunks in a file of yours. Compare the failing **sets**, not only the counts: a subset proves no harness went green-to-red even when the count is noisy |
| the full `--harnesses` sweep does not finish inside the window, or the loop stops after the first red harness | the board has grown past a sweep-per-run (92 here, over 10 minutes), and a `for` loop in `nu` — the shell this repo runs under — takes a non-zero harness exit as the loop's own | baseline the **subset** that names a footprint path: `grep -ln "<path>" $(find <board>/prds -name verify.sh)`, plus every enumerating harness. Say in the report that the sweep was narrowed and to what — a sweep that times out is no baseline at all, and `doctor.sh` without `--harnesses` finishes and still carries every non-harness row. Run the loop as `bash -c "for …; done; exit 0"`, never from `nu` directly |
| a repo-wide reference gate (`index.py check`) is red in the lane on a line naming an `@pearde/…` or `@.pearde/…` target, and green in the checkout | `lanes.create` cuts the lane deliberately without the board, so every reference from a tracked file into the board dangles there by construction — this never closes on a merge and is not a defect in the file | baseline the gate in both roots and quote both. A line whose target is under the board is the lane's missing board and nothing else; count only the lines whose target exists in the checkout. Do not add the board to the lane to silence it — a second board under a lane is a board the scan will find |
| the harness sweep is baselined with a board symlinked into the lane, and re-run without it | the symlink is inside the tree the sweep measures: a harness asserting about `<root>/pearde/…` sees the real board where it expects a lane's stub, and a harness reading the git store sees the lane's | measured here: `a-lane-s-wiki-is-a-stub-…` exits 1 with the symlink and 0 without, and `list-the-collects-the-repo-bug-orphaned` names the lane's `worktrees/-pearde`. Take both baseline and re-run with the scaffolding in the same state, name the state beside every count, and take the deciding count at the root `collect` will use |

### 3 — attempt-the-build

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 3 | `attempt-the-build` | a question asked before the build is a guess, and the board pays for it in a round-trip | `→ 1` |

#### Do

1. Build the thing the contract asks for. Whatever the build passes through
   needs no question; whatever it hits is the finding.
2. Keep NEW code under `prds/<prd>/probe/` — never at the repo root, where it
   would redden the map check for every later PRD — so a file the PRD's
   footprint places under `resources/` is built under `probe/` and moved by
   its spec. A change that is an **edit to an existing footprint file** cannot
   be staged this way: a guard, a rename or a branch has no meaning outside
   the function it lives in, so it is built in place, in the footprint file
   itself, and the spec records what already stands rather than what to move.
   Say which it was in the report.
3. Build every fixture in a directory made at run time — `D=$(mktemp -d)`,
   removed at exit. A fixture `prd.md` left anywhere under `prds/` becomes a
   real PRD the scan picks up.
4. Write `prds/<prd>/probe/verify.sh` as you go: one line per assertion, a
   count at the end. The count is printed, never asserted by a spec.
5. Stop at the first fork the build cannot pick and cannot build around, and
   record what the build was doing when it hit it. Which verdict that becomes
   is @references/parts/workers.md.

#### Done when

- `bash prds/<prd>/probe/verify.sh` prints a count, and the count is
  quoted — **unless the contract's verification is the repo's own gate**
  (a `justfile` recipe, a `scripts/` tripwire, `cargo test`), in which case
  that gate's command line and exit code are quoted instead and the probe
  directory carries only what the build needed to reproduce a finding.
  A probe `verify.sh` that merely re-calls the repo gate is a second copy
  of it that can drift. Or the probe is a set of modules the spec's own `## Verify and Proof` block invokes by name, in which case the block's command line and exit code are quoted and the probe carries no `verify.sh` — a probe harness that merely re-invokes what the block already runs is a second copy of it that can drift.
- `ls <board>/prds` against the pre-run listing shows no `prds/<slug>/` you did not make — a hand-walked sweep over the board is refused by the guard in a wired repo, and the listing answers the same question. The guard reads the *shape* of the command, not only its tool: `find <board>/prds -name prd.md` and `ls -d <board>/prds/*/` are both refused, and only the bare one-level `ls` gets through. Where the board is its own git worktree — the layout on this board — `git -C <board> status --short -- prds` answers it too and names the untracked ones; it is silent only where the board is gitignored inside the code repo.
- the probe is under `<board>/prds/<prd>/probe/` and nothing this run wrote
  is at the repo root — check with `ls`, not `git status`, where the board
  is gitignored.

#### Fails when

| seen | means | do |
|------|-------|----|
| the route's steps 3 and 5 have nothing to do because the specs already exist and the build is already in the tree | this is the route's **second** pass on the PRD — the analyst probed and specced, and an implementer has now been dispatched on the same route | run steps 1, 2 and 4, and enter step 3 **only for the specs whose build is not in the tree** — check each spec's own footprint with `git status --short` and `git diff` before deciding, never the PRD's as a whole. A pass that built two specs of three leaves the third's footprint clean, and clean is indistinguishable from done to anything but reading the file. Say in the report which specs were entered and which were not, and claim a flip only for what this pass built |
| a fixture board built under `mktemp -d` shows up in `serve.py status` after the run, on a path that no longer exists | the probe ran a command whose repair registers whatever board it is handed — `doctor --fix` is one — and the live daemon's registry outlives the temp dir | never run a `--fix`-shaped command against a fixture while a real service is up; point it at a dead port (`PEARDE_PORT=1`) so the repair cannot connect, and check `serve.py status` at the end. To remove one already landed, test the **path** first — `[ -d <path> ] || serve.py forget <name>` — because `forget` takes a name and a mistyped one unwatches a live board; if that happens, `serve.py ensure .` from the board's own root restores it under the same name |
| a check stands a machine-wide guard down (`PEARDE_REAP_GRACE_S=0`, a disabled cap, a bypassed lock) to reach the behaviour it is measuring | the guard is the only thing keeping the action off a neighbouring session's processes, and the check has just removed it machine-wide | scope the action to what the check itself started — a `--pid`, a port, a path filter — and make the narrowing flag **refuse** an unreadable value rather than falling back to "everything". Assert the guard both ways: kept inside it, and expiring outside it, or a widened default keeps every box green while the guard never fires |
| the probe passes standalone and fails only when the runner that is its own subject runs it | the probe is itself an instance of the population it measures, and inherits the environment that runner sets — a guard variable, a cwd, a port — so it measures the guard instead of the behaviour | clear it explicitly for every fixture invocation (`env -u <VAR>`), keep one assertion that sets it deliberately, and run the harness both ways before quoting a count |
| every fixture lands on one board, and assertions pass or fail in the wrong sections | the fixture-maker is called as `B=$(mktemp_helper)`, and command substitution runs it in a **subshell** — a counter or path it keeps never reaches the caller, so every call returns the same board | make each fixture with its own `mktemp -d` inside the helper and echo that; never keep state in a helper you call through `$(…)` |
| a patch's anchor text no longer matches a file you read in step 1 | another session moved the file since | re-read it, merge into its current shape, keep your hunk disjoint from theirs, and name the collision in the report |
| the fixture's own git repo shows `?? err` or another scratch file after a refusal | the harness wrote its scratch inside the fixture, so "the diff is empty" cannot pass | keep scratch in a second `mktemp -d` outside the fixture repo |
| `verify.sh` prints a heading and hangs | a line in the harness reads stdin — a bare `cat` or `read` with no file | run it with `</dev/null`, then fix the line |
| a rule reading mtimes fires on a fresh copy of the example | `plan.py example` copies stat too, so the copy carries the example's own timestamps | `find <copy> -type f -exec touch {} +` before the byte-identity check; set them back only in the fixture that tests age |
| a page driver reads a Lit element right after `pearde.apply` and sees the old render | Lit renders on a microtask | `await el.updateComplete` before reading the DOM; and run any `pearde.replace` test last, since it removes the page's own element |
| `touch: out of range or illegal time specification` on **darwin** | `touch -d '<n> minutes ago'` is GNU coreutils; darwin's `touch` takes `-t <YYYYMMDDhhmm.SS>` and `date -v` for arithmetic — a GNU box never sees this row | portable on both: `python3 -c 'import os,time,sys; t=time.time()-120; os.utime(sys.argv[1],(t,t))' <file>`; darwin-only: `touch -t "$(date -v-2M +%Y%m%d%H%M.%S)" <file>` |
| a fixture meant to hold a foreign hunk and a kept one shows a single hunk, and the file goes whole | the two edits touch adjacent lines, and `-U0` merges adjacent changes into one hunk whose body is in neither baseline | leave one untouched line between the foreign edit and the kept one; the merge itself is a finding for the PRD that classifies hunks |
| `?? prds/<slug>/` appears mid-run and its `prd.md` is the untouched template | a harness in another PRD's probe calls a transition with no `--board` from a cwd inside the repo, and your edit turned its refusal into a write on the real board | before the first edit, grep every harness for the command with no `--board`; run those from a cwd with no `prds/` above; remove the untracked template PRD, name the row it left in `.transitions.jsonl`, and hand the harness's owner the `--board` line |
| a `sed -n 's/^\(a\|b\)$/\1/p'` extractor captures nothing, or captures `0`, on **darwin** | BSD sed has no `\|` alternation in a basic regex; GNU sed does | `grep -E '^(a|b)'` then `sed 's/^  //'` — portable on both |
| a fixture board made by `cp -R resources/board/example <d>/prds` shows `prds/prds`, and doctor resolves to a board one level too deep | `example` is a repo root, not a board — it holds `prds/` and a README | copy `resources/board/example/prds` to `<d>/prds`; doctor from `<d>` hides the nesting, a command run from inside the board does not |
| an assertion on a path printed by a Python command fails on **darwin** with `/private/var/…` against `/var/…` | `os.getcwd()` returns the real path; `mktemp -d` and bash's `$PWD` keep the symlink | compare against `$(cd "$D" && pwd -P)` — portable on both. **This is an equality hazard only. A `grep -F` needle is unaffected: `/private/var/X` contains `/var/X` as a substring, so a `mktemp`-spelled needle matches a realpath-spelled hit and "repairing" it adds a false claim to the file. Measure before you widen a needle on this ground.** |
| `ModuleNotFoundError: No module named 'memos'` from a copied `collect.py` or `plan.py` | the board scripts import from `resources/` beside `board/`, and the copy took `resources/board/*.py` alone | copy `resources/*.py` into `<scratch>/resources/` and `resources/board/*.py` into `<scratch>/resources/board/` — the layout, not just the files |
| a `lacks` needle for a PRD name fails on a `scan` band that does not list it | another row's `after <name>` or `needs <name>` bit carries the name | match the row token `· <name> ·`, never the bare name |
| a `--dry` run refuses on a gate the real run passes | the dry branch re-ran a gate that reads the file the real run writes first — `answer`'s gate saw the question still open because the answer is never on disk in a dry run | compute the gate's input on the scan dict in memory (the answer appended to `prd["body"]`, the state moved on `prd["fm"]`) and print the line off that dict; never re-enter `transition()` for a dry run of a two-step write |
| every assertion in a harness passes, or every one fails, regardless of the command's output | the helper is `ok "<label>" "<expr>"` with the expr evaluated inside `ok`, so `$2`/`$3` in the expr name `ok`'s own arguments, not the caller's values | evaluate the test in the caller (`eq() { [ "$2" = "$3" ]; ok "$1" $? "…"; }`) and hand `ok` only a label and an exit code |
| the brief says the probe's code is uncommitted, and `git status --short` is clean | a sibling session committed the whole tree, your hunks with it — or, on a lane, this PRD's **own** `collect`: `land_lane` commits the lane before it merges, so a conflict in the rebase leaves the work committed on `lane/<slug>`, the checkout untouched and the PRD still `claimed`, with nothing on the board saying so | `git log -1 -- <footprint path>` and read the file itself before concluding anything is missing; if the behaviour is present, the work stands — record the commit that took it, and read every spec's "what already stands" against the **file**, never against a diff. On a lane also run `git -C <checkout> merge-base --is-ancestor HEAD lane/<slug>` and `git merge-tree --write-tree --name-only HEAD lane/<slug>`: where it names conflicting files that are all inside your footprint, rebase the lane onto the checkout's branch and resolve them — never `git merge` main into the lane, which puts two commits behind one PRD and breaks the `--ff-only` `lanes.merge` needs. Where a conflicting file is outside the footprint, stop and report it |
| a box asks you to prove a check *can* fail, and the file to mutate is an uncommitted footprint file | the restore cannot be `git checkout` — the committed text is not the text you must return to, and a checkout would silently discard the build | `cp <file> <scratch>/<name>.bak` into a scratch dir **outside** the repo, mutate, run, `cp` back, and prove the restore with `cmp <scratch>/<name>.bak <file>`. Quote the failing count, the restored count, and the `cmp`. Make the mutation unreachable at run time (`if false; then … fi`) when the check reads text rather than behaviour — a reachable one measures the mutation instead of the check |
| a line appended with `>>` to a harness lands concatenated onto its last line | the harness ends on its exit-carrying check with no trailing newline — the shape every harness on this board ends in | `printf '\n%s\n' '<line>' >> <file>`, or check with `[ -n "$(tail -c1 <file>)" ]` first. An anchored matcher (`^…`) will not see a concatenated offender, so a can-it-fail box run this way reads green on a check that did not fire |
| your probe invokes another PRD's harness and its result is decided by that harness's own defect — a hard-coded port, a leaked process, a shared fixture | you are measuring the neighbour's file, and the box it backs is green or red by scheduling | do not edit that file. Make your own probe stand down when the condition holds (`PEARDE_HARNESSES` set, the port already bound) and say in the check's own text why, then report the neighbour's defect as a finding for the orchestrator to route. Demonstrate the box under the racing condition; never assert it |
| the brief names `probe/run.sh` and only `probe/verify.sh` is on disk | a spec in this PRD's own set contracted the rename, and an earlier pass did it | take the file that exists as the same probe, name both spellings in the report, and check the spec's box against the file rather than against the brief |
| a harness builds its own repo, commits a base, runs the tool, then asserts `git log --name-only -N` names a file — and the row stays green under a mutation that stops the tool committing anything | the `-N` window reaches back past the tool's own commits into the fixture's base commit, which names that file by construction. The row measures the fixture, not the tool | record each repo's HEAD **before** the run and range the log against it — `git log --name-only --pretty=format: "$HEAD0"..HEAD` — then watch the row go red under the mutant. A count of commits is never the window; the window is the commit the run started from |
| a fixture that checks the code repo out INSIDE the board refuses with `footprint <p> is in no repo that holds it — looked for <board>/<p>` | `repo_of` resolves a missing `repo:` as the repo *enclosing* the board and never looks below it, so a checkout under the board is invisible and `repo` comes back as the board itself | give the fixture's `prd.md` a `repo: <dir>` key — it is resolved against the board's own root and is how a board says where its code lives. The refusal names the footprint, so the first four reads go to `foot_root`, which is not the function that decided anything |

### 4 — re-run-the-harnesses

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 4 | `re-run-the-harnesses` | a probe that reddens a committed harness is a failed run rather than a finding | `→ 3` |

#### Do

1. Before re-running the harnesses, run the repo's formatter and linter over
   **your files only** — `rustfmt <your file>`, not `cargo fmt --all`, which
   would rewrite every file a parallel worker has in flight. A gate that checks
   formatting before it runs tests fails at a different line and a different
   exit code, which is easily misread as a regression in the tests.
2. Re-run every harness whose count you recorded, in the same order, with the
   same command line — and with the same `PEARDE_ROOT`. A worker building in
   a lane names its lane in both runs (`PEARDE_ROOT=<lane>`); a baseline taken
   against the checkout and a re-run against the lane compare two different
   trees, and every difference between them is the two roots, not your build.
3. Compare each count to the recorded one. A count that dropped is yours until
   you have shown otherwise.
4. Before claiming any red-to-green flip, **diff the predicate against HEAD,
   not just the result**. Extract the harness's own matcher and run it over
   `git show HEAD:<file>` for every file it reads. If the pre-build file
   already satisfies it, the flip is not yours and the box it backs cannot
   fail. Name the file whose change actually moved it. A worker who only
   re-runs checks will take credit for a neighbour's landing every time,
   because a passing check looks identical whoever earned it.
   Record HEAD before the first run and again at the flip. If HEAD moved,
   diff against the commit you recorded (`git show <old-head>:<file>`), not
   against `HEAD` — a sibling that committed the tree took your uncommitted
   hunks with it, and `HEAD:<file>` then shows your own change as the baseline
   and reads your flip as somebody else's.
   A count that rose because *this unit added the tests* is not a flip to
   attribute — name the suite and the number of tests you added, and show the
   pre-existing counts are individually unchanged. The `git show HEAD:` check
   applies to a harness whose predicate you did not write.
5. When a harness fails on a line you edited, read what it matches before you
   touch the harness. A matcher written against a markdown table row often
   matched that row's column padding, so re-aligning a table breaks it while
   the rule it asserts is intact — repair the matcher to read the cell's text,
   never the spacing, and say in the report that the rule did not move.
6. Quote the final line of each harness in the report, next to its baseline.

#### Done when

- Every recorded harness prints a count greater than or equal to its baseline.
- Every count that changed has one sentence saying what moved it.
- Every flip claimed as this PRD's has been shown against `git show HEAD:` —
  the predicate failed on the old file and passes on the new one.
- No harness was edited without the report saying which matcher changed and
  why the rule it asserts is unchanged.

#### Fails when

| seen | means | do |
|------|-------|----|
| a count went **up** on a harness you did not touch | every row here reads a count that dropped; a count that rose is the same evidence that the tree moved under you, and a worker that only checks for drops will quietly take credit for a neighbour's landing | quote both counts, say the rise is not yours and name the file whose change explains it — a harness whose baseline you recorded red and that is now green is a finding about the other session, not about your unit |
| `find prds -name verify.sh` lists a harness that was not there at step 2 | a parallel session landed a PRD mid-run, with its own probe | run it, record it as new with no baseline, and do not compare it to anything; a harness you never had a baseline for cannot regress |
| a count moved on a harness whose inputs you did not touch | the harness's own text changed between the two runs | quote both counts, say the text moved and whose it is; it is not yours to explain |
| a count moved on a path you never wrote | another live session landed files under `resources/` mid-run | name the paths and say they are not yours; the baseline stands for your own paths |
| a count dropped on a harness whose failing line is a repo-root `git status` or `git diff` | the check measures the workspace, not this PRD's footprint; a parallel worker's untracked file reddens it | quote the line, list the untracked files it saw and whose they are, leave the harness alone — the rule did not move |
| `index.py check` or `doctor` prints a line naming a file you did not touch | another session moved the tree under you | `git diff <file>` proves whose it is; report it with the path, do not fix it |
| a committed harness outside your footprint goes red on a count the contract itself moves | the matcher is honest and the file is not yours | leave it red, quote it beside its baseline, and put the file in the spec's `footprint:` with the one-line matcher change as that spec's work |
| a count dropped, and every failing line names a file outside your footprint that `git status` shows a live sibling modified after your baseline | the neighbour moved, not your unit | quote the failing lines, the file, and its mtime against your baseline time; report it as a finding and do not back-edge — there is nothing in your footprint that closes it |
| a needle fails on a sentence you kept | the sentence was re-wrapped across a line; the needle is one line | re-wrap so the sentence reads whole on one line and say the rule did not move |
| a needle names a sentence the contract deleted | the rule now lives in a command | quote the needle, name the command and its line, propose the harness edit — the count is a finding, not yours to repair |
| a harness has no `cd` and one line runs a transition with no `--board` | it acts on whatever board is above the caller's cwd — the real one, from the repo root | run it from the scratch dir, where `find_board` refuses and the line fails without writing; quote the count and name the line |
| a state file in `resources/board/state/guard/` you were told not to write moves its mtime during the re-run | a harness in the set calls `doctor.sh` with no `PEARDE_GUARD_STATE`, and `doctor.sh`'s own guard probe carries no session | name the harness by `grep -c doctor.sh` and `grep -c PEARDE_GUARD_STATE`, compare the file's mtime to your start, remove it only if it did not exist before you, and report the writer's line |
| doctor's `view` row is `off` after the run and `serve.py status` says not running | a harness in the set runs `serve.py stop` with no port and reaches the live daemon | name the harness line, do not restart it yourself — the coordinator owns the service |
| a check backing an already-ticked box in your own spec goes red on the change the contract asked for | the check was written against the old behaviour in an environment the change makes reachable, not against the box's words | re-read the box's own sentence and re-aim the check at the shape that still meets it — never weaken it, and never special-case the new path to keep the old check green, which puts back the divergence the unit removes. Quote the red, the box's words, and the re-aimed check in the report |
| a count dropped and the failing line is a harness's own `index.py check`, `doctor.sh` or manifest assertion over the live checkout | the harness measures the workspace, not its PRD's footprint; a parallel worker's new file with no manifest row reddens it | quote the line and the file that explains it (`git status --short` names it untracked, its mtime post-dates your baseline), leave the harness alone, and cite `.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md` — the repair is owed to that harness's own PRD, not to you |
| a repo-wide gate is red in the lane on lines the orchestrator's checkout does not print | the lane is behind the checkout's uncommitted work, so a fix that landed there is missing here — the mirror image of an inherited red | baseline the gate in **both** roots before the first edit and quote both in the report. A line present in the lane and absent in the checkout closes on the merge; a line present in both is a live finding. Never add a neighbour's missing row in the lane to silence it — the checkout already holds that hunk and you would duplicate it into the merge |
| a footprint file of yours is also modified, uncommitted, in the orchestrator's checkout, and the two hunks are on **adjacent** lines | both edits are correct and neither is a conflict with the other's meaning, but a three-way merge cannot keep both automatically — the same adjacency `-U0` hides in a diff | prove it before the merge rather than discovering it in `collect`: clone the checkout to scratch, commit the neighbour's working copy there, `git apply --3way` your own diff, and read whether it conflicts. Name the file, both hunks and the resolution in the report. Do not move your hunk to avoid it — a hunk written to dodge a neighbour's uncommitted line is wrong the moment they land |
| a block gates on the PRD's slug appearing in a sweep's failing lines, and goes red with the PRD's own probe green | the worker's lane directory is named for the slug, so any neighbour's FAIL line quoting a path inside that lane matches | gate on the **path** of the PRD's own probe — `prds/<prd>/probe/verify.sh` — never on the slug. Measured: two matches for the bare slug against zero for the path, on the same sweep output |

### 5 — write-the-specs

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 5 | `write-the-specs` | the probe's knowledge is in one worker's head and nowhere else until this step, and the next worker gets the file, not the head | `→ 3` |

#### Do

1. One `prds/<prd>/specs/specNN.md` per implementable unit, from
   @references/templates/spec.md.
2. Frontmatter carries `complexity:` and `footprint:`. The footprints across
   the specs are what the overlap check reads, so a path in two specs is a
   decision, not an accident.
3. Every acceptance box names an output a check can read. Write the box
   spelling inside backticks in any prose about it — the matcher is
   line-based and fence-blind, so a pasted open box becomes a real one.
4. Give each spec a `## Verify and Proof` block in which every path is
   spelled **literally**, not through a variable — the checker in
   `check_spec` (`resources/board/specs.py`, the `any(p in b for b in blocks
   for p in fp)` line) matches the `footprint:` string, and a
   `"references/personas/$f.md"` reads as no footprint path at all. Spelling
   is not the point, though: **no command's exit may be decided by a file
   outside the footprint.** A repo-wide command (`index.py check`, `doctor`, a
   root `git status`) may be captured and printed, and the block may fail only
   on the lines of its output that name a footprint path. A file the block
   must read but does not own — a neighbour's fixture input, a sibling's
   roster — is not copied, it is **stubbed**: the block writes a minimal valid
   stand-in, so a rename or an empty read next door cannot decide the colour.
   Guard every captured output with `[ -n "$out" ]` before greping it: a
   producer that dies before printing looks exactly like a passing grep miss.
   There is no `verify:` frontmatter key — the template's keys are a closed
   set.

   Before the spec is done, run the block **the way `collect` runs it** and
   confirm the exit. The flags are `bash -e -o pipefail` — the pair
   `collect.py` passes to `run` and to `guarded_run` — and both matter, in
   opposite directions:
   `pipefail` makes a board-wide gate's exit inside a pipeline the block's, and
   `-e` aborts the block at the first bare command that fails. A block tested
   under `pipefail` alone is not tested. Awk the fence out and run it:

   ```
   bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"
   ```

   It must exit 0 on a green tree, and must exit **non-zero** with one
   footprint file mutated.

   Two shapes are safe under `pipefail` and abort under `-e`, so they are only
   ever caught by running with both. An assignment from a command substitution
   carries the substitution's status, so `out=$(<gate> 2>&1); rc=$?` kills the
   block on exactly the red output it was written to survive — write
   `out=$(<gate> 2>&1) && rc=0 || rc=$?`, or `|| true` where the code is not
   wanted. And a bare `<test> && <action>` aborts when the test is false, which
   is its passing case whenever the test is looking for something that should
   not be there — write it `if <test>; then <action>; fi`.

   A mutation proves one of two different things, and only the second is what
   the box claims. A mutation aimed at the string a `grep` reads — a renamed
   function, an altered heading, a changed wording — proves the **counter is
   wired**: the check runs and the failure reaches the exit. A mutation aimed
   at what the tool **computes** — a score, a weight, an axis, a fallback,
   a threshold — proves the block **detects a regression**. A block with only
   the first kind behind it should say so in the report rather than let the
   tick imply the second. The cheapest honest behavioural mutation is usually
   one constant in the unit's own footprint file, restored by `cp` from a
   scratch dir outside the repo and proved back with `cmp`.

   Run the block from the root `collect` will run it from — the orchestrator's
   checkout, not your lane — and where the block hard-codes that path, run it
   once with your own root substituted and leave the block as written. A block
   rewritten to name the lane passes for you and fails for `collect`.

   Where the block invokes the tool by a path relative to the root — `python3
   resources/<mod>.py` — running it from the checkout runs the checkout's copy,
   not your lane's, and the exit says nothing about your build. Substitute the
   module path, not the root: run from the checkout with
   `s#resources/<mod>.py#<lane>/resources/<mod>.py#`, and run the block verbatim
   as well. Where instead the block runs a **harness** that resolves the tree
   itself from `PEARDE_ROOT`, there is no module path in the block to
   substitute and rewriting the harness path would name a different harness, not
   a different tree: run the block verbatim under `PEARDE_ROOT=<lane>`, which
   leaves the block untouched, and verbatim with `PEARDE_ROOT` unset as well.
   Verbatim it must FAIL before the merge — that failure is the red-to-green
   flip shown against the tree that does not hold the build, and it is stronger
   evidence than `git show HEAD:`, because the whole gate ran on the old file.
5. Say in each spec what already stands from the build and what is left.
6. `grep -c '^- \[ \]' prds/<prd>/specs/*.md` — every spec has at least one
   box, and none is ticked before an implementer runs it. Then
   `awk '/^```/{f=!f;next} f' prds/<prd>/specs/*.md` and read every command
   back: each must name a path from its own spec's `footprint:`.
7. `pearde specced <prd> --check --as <id>` — the gate that reads the set, writing nothing. It refuses without `--as <id>` or `PEARDE_AS` — the persona is on the line even in check mode — and refuses a file naming line and reason, and a set over `split-above` or `specs-above`.

#### Done when

- Every spec has `complexity:`, `footprint:`, acceptance boxes and a
  `## Verify and Proof` block.
- No box asks for a commit message — committing is not the implementer's act.
- No command in any block runs the whole workspace.
- Each spec states what the probe already left in the tree.

#### Fails when

| seen | means | do |
|------|-------|----|
| `over split-above: N > 40 — REFINE it` | the set is heavier than the board allows | weigh each spec against the siblings' spec files first; if the weight is honest at that scale the verdict is REFINE with a `## Split` table, never a lower number |
| an implementer reports a box whose command prints a different number than the box asserts | the number was written from the build's memory rather than from running the command **as the box spells it** — a `grep -c` counts every matching line, and a word quoted in a comment beside the code counts too | run each box's own command line verbatim, from the repo root, and paste what it prints into the box. A count in a box is quoted output, never a recollection; when a literal appears in both prose and code, aim the box at the content instead of at the count |
| `collect` refuses with `spec<NN> exit <n> — nothing written`, and every command in the block passes when you run it by hand | a line in the block is a **board-wide gate** — `doctor`, a full harness sweep, a repo-root `git status`/`git diff`, `index.py check` — and it decides the block's exit two ways: `-e` takes a bare call's status, and `pipefail` takes it out of a pipeline. Either way the unit's pass is conditional on every other PRD on the board, and a gate already red on an inherited line means the spec can never pass, however green the work is. `141` instead of `1` is the same shape sigpiped into a `grep -q` | capture, then grep: `out=$(<board-wide command> 2>&1 \|\| true)` then `printf '%s\n' "$out" \| grep -E "<rows>"`. The rows stay visible and stop deciding the exit. Gate **only** on commands reading a path from this spec's own `footprint:`. Check it the way collect will, not by hand: `bash -c "set -o pipefail; $(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"` must exit 0 |
| the report path already holds a previous pass's report | this route is run twice on one PRD — the analyst's pass and an implementer's — and both write `prds/<prd>/report.md` whole | read it before writing and carry its `## Findings` forward into yours by name. A finding reported and not fixed is the route's only record of a defect nobody owns; an overwrite that drops it loses the board's sole copy |
| a block exits non-zero on the result that means it passed | a command whose **passing** result is "nothing matched" — `grep -c`, `grep -vc`, `ls <glob>`, `find … \| wc -l` — exits non-zero on exactly that result | guard the *producer*, not the pipeline: `{ <cmd> \|\| true; } \| wc -l` |
| a block exits **0** while a line in it printed a failure | the assertion is written `[ <test> ] && echo "<the good news>"`, or `<probe> && echo BAD \|\| echo OK`. Neither can fail a block: a false test prints nothing and the next command's status becomes the block's, and the `&&…\|\|` pair always exits 0 | put the assertion **last** and write it bare — `[ ! -s "$f" ]` — or accumulate a counter in the loop and end on `[ "$N" = 0 ]`. Then run the block the way collect does (`awk` it out, `set -o pipefail`) **against a tree where the check should fail**, and confirm it does |
| a box or block asserts a literal total of the PRD's **own** probe | the spec has locked its harness shut: a later pass cannot add the check a thin box needs without reddening the spec that names it | assert the tally *parses* and `failed == 0` — never a total, not even the probe's own. A floor (`>= N`) is honest; an equality is a wall |
| `specced` refuses `<spec>:<n>: `## Verify and Proof` holds no fenced `sh` block` and the block is plainly there | a line inside the block begins `## ` — commonly a heredoc writing a markdown fixture. The section reader in `resources/board/specs.py` is line-based and fence-blind, the same way the acceptance-box matcher is | write the fixture's headings with a placeholder prefix and raise them at run time (`sed 's/^@@ /## /'`). Never a literal `## ` at line start inside a verify block, in a heredoc or out of one |
| a spec contracts a file under `.pearde/memos/` and `memos.py check` goes red the moment it lands | the index by kind is generated, and adding a memo makes `memos/README.md` stale — a file no footprint names and that the spec cannot omit | run `python3 resources/memos.py index <board>` and check `git diff --stat` names one added row; the index is part of adding a memo, not a separate edit. Say so in the report, because the footprint is wrong and the next author of a memo spec should carry the index row in it |
| a `## Verify and Proof` block reads as instructions to a person — a `<placeholder>` argument, a `# note the dir` comment standing in for a value, a bare `$?` echoed after the command it describes | the block was written to be *read* and never run, and `collect` runs it: `<that dir>` is parsed as a redirect from a file named `that`, and the spec dies on a syntax error with every box already ticked | run every block, of every spec in the set, exactly as `collect` will — `bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' <spec>)"` — before `specced` is called. `specced --check` reads the block's *presence*, never its exit, so a block that cannot parse passes the gate |
| a block line reads `! <cmd>` and a mutation that should redden it leaves the block at exit 0 | `set -e` does not apply to a command whose status is inverted by a leading `!` (POSIX XCU 2.11), so the line prints its failure and the block carries on | write it `if <cmd>; then exit 1; fi`. This is the same class as the `<test> && <action>` shape the section already names, and the `!` form is not covered by it — a block can hold one and read green forever |
| a block ends on `<board-wide gate> \| grep <own files> && exit 1`, and the gate is red on rows outside the footprint | under `pipefail` the pipeline carries the gate's exit, so the `&& exit 1` never fires and the block's own exit is the gate's — the check cannot fail, and where the line is last the block fails for a reason outside its footprint | capture the gate (`out=$(<gate> 2>&1) && rc=0 \|\| rc=$?`), refuse a crashed producer by exit code, and put the grep in an `if … then exit 1; fi`. The existing row names the capture; it does not name that the `&& exit 1` tail is dead in the same breath |
| a block reading `.pearde/prds/…` passes in the lane and its census counts read 0 or near it | `lanes.create` gives the lane its own `.pearde/`, holding `graphify/` and no `prds/` — the block is sweeping an empty board and passing vacuously | build the merged tree (`git clone --shared <checkout>`, `git apply` the lane's diff, `ln -s <board> <scratch>/.pearde`) and run every block there, rebuilding it after each edit. Quote a census count from the block: a sweep that finds no PRDs is the tell |
| a spec contracts a `resources/invariants/*.sh` script and its memo's `verify:`, and `memo verify` answers `BROKEN (exit 127) — No such file or directory` in the lane | `memos.py verify` runs each command with the cwd set to `os.path.dirname(board)`, and `board_link` resolves a board reached through a symlink to what the link points at — so a lane's root is the checkout, and the script the lane holds is not on it | run the invariant directly (`bash resources/invariants/<name>.sh`, which takes its tree from `$PWD`) to prove the rule, and keep a byte-identical copy in the checkout — proved with `cmp` — so the memo's own command resolves. Say both in the report; the copy is one of the paths the merge needs cleared |
PASS: health._git, questions.find_board, questions.sections (0/226 prds diverge), workflows.find_board, workflows.section (120 checks), knowledge.parse_frontmatter (1 known/618 wiki notes diverge)

spec04: exit 0
PASS: health._git, questions.find_board, questions.sections (0/226 prds diverge), workflows.find_board, workflows.section (120 checks), knowledge.parse_frontmatter (1 known/618 wiki notes diverge)
query: 104 hit(s), 36 strong · 104 notes on record
  @ 12  [[260902-f2fe]] sources   Rebase then ff-only is how a lane lands as one commit; a plain merge w
  @ 10  [[260903-1458]] sources   Claude Code follows a symlinked skill directory, so one link installs
