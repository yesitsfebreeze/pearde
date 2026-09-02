# every-worker-runs-in-its-own-worktree — implementer report

Verdict: DONE

All five specs implemented, 33/33 acceptance boxes ticked, 0 open. Every
`## Verify and Proof` block exits 0 the way `collect` runs it
(`bash -e -o pipefail`), and each was proved to exit non-zero with one file
of its own footprint mutated and restored (`cmp` equal). The 37-harness
baseline set is unchanged on the merged tree, bar one red→green that is not
mine.

**The work is on `lane/every-worker-runs-in-its-own-worktree`, uncommitted**
— 11 modified files and `resources/board/lanes.py` untracked. See
`## The merge the orchestrator has to make` before collecting: the checkout
holds an older copy of five of them.

## Per-spec box status

| spec | boxes | verify block, as `collect` runs it | fixture |
|---|---|---|---|
| spec01 the lane library | 8/8 | exit 0 | 19 checks · 19 pass · 0 fail |
| spec02 claim cuts, sweep drops | 7/7 | exit 0 | 23 checks · 23 pass · 0 fail (with spec03) |
| spec03 the brief names the lane | 5/5 | exit 0 | — |
| spec04 collect merges the lane | 7/7 | exit 0 | 30 checks · 30 pass · 0 fail |
| spec05 the clash is an edge | 6/6 | exit 0 | 11 checks · 11 pass · 0 fail |

Fixture scripts, harness outputs and the merged-tree simulations are under
`/private/tmp/claude-501/-Users-feb-dev/1bc5591e-763e-4f0d-b6a1-9df322cffab5/scratchpad/impl-worktree/`
(`t01.py`, `t23.sh`, `t45.sh`, `t05.sh`; `base/`, `after/`, `final/`).

## Where the build ran, and why the tree moved first

The brief named the lane as `<repo>`. `git status --short` in it was
**empty**: `lanes.create` cuts off the code repo's HEAD, so the lane carried
nothing of the probe, and every one of the probe's hunks was uncommitted in
the orchestrator's checkout. Per `probe-then-spec` step 1's `Fails when` row
for exactly this shape, I read `git -C <checkout> diff` for each footprint
path, found five entirely this PRD's, and carried those into the lane:

- `resources/board/lanes.py` (untracked), `brief.py`, `collect.py`,
  `plan.py`, `transitions.py` — carried, continued there.
- `references/files.md` — **not** carried. Its only checkout hunk is a
  neighbour's (`pearde-machine.md` → `pearde-all.md` in the skills table).
  I added this PRD's `lanes.py` row to the lane's copy instead, so the two
  hunks are disjoint and merge cleanly.

Everything else dirty in the checkout (`SKILL.md`, `index.md`,
`references/parts/all.md`, `references/skills/pearde-machine.md` deleted,
`edit.py`, `machine.py`, `ramp.py`) is a neighbour's and was left alone.

## The merge the orchestrator has to make

`collect` will merge `lane/every-worker-runs-in-its-own-worktree` into the
branch the checkout is on. Five files in the checkout hold an older copy of
this PRD's work, and the lane's copy is a strict superset of each. The merge
refuses until those are discarded:

```
git -C /Users/feb/dev/infra/pearde checkout -- \
  resources/board/brief.py resources/board/collect.py \
  resources/board/plan.py resources/board/transitions.py
rm /Users/feb/dev/infra/pearde/resources/board/lanes.py
```

`references/files.md` must be **kept** as it stands in the checkout — its
hunk is a neighbour's and the lane adds a different row to the same file.

I simulated the merged tree twice to measure against it, since a board
harness resolves its `ROOT` from its own path and therefore always reads the
checkout, never a lane (see `## Findings`):

- `scratchpad/…/mg` — `git archive HEAD` + the checkout's whole uncommitted
  diff + the lane's files. `python3 resources/index.py check` prints
  **nothing**, exit 0.
- `scratchpad/…/mg2` — a `--shared` clone, so the repo's own history is
  present for the harnesses that read it.

## The harnesses

The set: every `verify.sh` on the board that greps a footprint path,
enumerates the board, or runs a repo-root `git status`/`git diff` — 37 of
59. Recorded **before the first edit**:

| run | root | green | red |
|---|---|---|---|
| baseline | checkout, as the probe left it | 25 | 12 |
| after | checkout (untouched by me) | 26 | 11 |
| final | merged tree with real history | 26 | 11 |

The `final` set is **identical to the baseline** except one row:

- `the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list`
  went red → green on `FAIL it moved nothing in this repo`. **Not mine.** It
  made the same jump in the `after` run against the checkout, whose
  `git status --short` is byte-identical to my baseline's 13 lines. Its
  check reads a repo-root git status, which every live session moves.

Twelve harnesses were red **before my first edit** and stayed exactly as
red. Six of those reds are this PRD's contract moving, and the contract is
what the specs implement:

- `the-board-runs-itself/transitions-are-commands` — `FAIL claim with a
  footprint clash names both`, `…and the clashing PRD`. spec05 removed that
  refusal; the matcher is honest and the file is in no footprint here.
- `workflows-on-the-board/workflow-attach` — `FAIL claim refuses a footprint
  a claimed PRD holds`. Same cause.
- `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` — two `E`
  rows are the cascade of those two.

Left red and quoted, per `re-run-the-harnesses`: a committed harness outside
your footprint that goes red on a count the contract itself moves is left
red. The repair is one matcher line in each and is owed to those PRDs. The
remaining reds (`an-unknown-flag-refuses`, `collect-stages-a-shared-file-whole`,
`the-next-line-runs`, `too-big-splits-itself`, `readme-in-three-rings`,
`the-gate-runs-the-harnesses`, `brief-does-not-refuse-the-claim-it-was-just-handed`,
`workflow-skill`) were red at the baseline for reasons outside this PRD.

### Two reds I caused, and closed

- `the-loop-is-commands` (`FAIL loop.md is 173 lines`) and
  `the-round-runs-in-a-window-that-ends` (`FAIL D10 loop.md is still one
  page`). My spec05 edit to `references/parts/loop.md` pushed it past the
  170-line ceiling both harnesses assert. Rewritten to three lines; the file
  is now **170** and both are green (60/60 and 26/26). **loop.md is now at
  the ceiling** — the next edit to it must cut a line.

### Two merged-tree reds that were the simulation, not the tree

- `nothing-left-open/the-line-tells-the-truth` — `FAIL E14 no scratch index
  is left behind`. That row globs `/tmp/pearde-index-*` machine-wide; a
  sibling harness running `collect` at the same instant owns one. Run
  serially against the same tree: **85 checks · 85 pass · 0 fail**.
- `the-tool-keeps-its-word/collect-keeps-its-word` — 8 `the old collect …`
  rows. It builds a pinned copy with `git show e8b262d:…`, and my first
  simulation was a fresh `git init` where that sha does not resolve, so the
  old copy was empty. Re-run in `mg2` (a `--shared` clone with the history):
  **101 checks · 101 pass · 0 fail.**

## The repo's own gate

| gate | baseline (checkout, before the first edit) | merged tree |
|---|---|---|
| `python3 resources/index.py check` | exit 1 · `resources/board/lanes.py is on disk with no row in references/files.md` | **exit 0, prints nothing** |
| `bash resources/doctor.sh` | `index broken 1 problem` · `origin broken` · `knowledge broken` · harnesses/jstests `off` | `index` **ok**; `origin` and `knowledge` unchanged |

`origin` (27 derived, 1 with no `from:`) and `knowledge` (graph.json behind
six notes) were **broken before the first edit**. `origin` is untouched.
`knowledge` is now behind **seven**: the brief requires a fact learned
outside this repo to be written back with `knowledge.py remember`, and
`[[260902-69f0]]` is that note. `knowledge.py relink` closes it and is
outside this footprint. Every
other doctor row is identical; the rows that differ in the simulation
(`statusline`, `guard`, `board`, `vault`, `vision`, `harnesses`, `jstests`)
differ only because the scratch root is not the checkout.

In the **lane** the gate prints two lines the checkout does not:
`references/skills/pearde-all.md is on disk with no row in
references/files.md` and `resources/board/edit.py references @questions.py —
not on disk`. Both are at the lane's `HEAD` (proved with `git ls-tree HEAD`
and `git show HEAD:references/files.md`) and both close on the merge,
because the checkout's uncommitted neighbour hunks fix them. This is
`re-run-the-harnesses`'s row for a repo-wide gate red in the lane on lines
the checkout does not print — baselined in both roots, and nothing added in
the lane to silence them.

## What each spec's blocks were changed to, and why

Every one of the five standing blocks ended on `python3 resources/index.py
check` — a **board-wide gate** whose exit, under `collect`'s `-o pipefail`,
becomes the block's. Measured biting: in the lane, spec01's block exited 1
on the two inherited lines above, neither of which names a path in any
footprint. `write-the-specs`'s `Fails when` row prescribes the repair, and
this pass is the route's second, where applying that table to the blocks
that already stand is the work. Each block now reads:

```
out=$(python3 resources/index.py check 2>&1) && rc=0 || rc=$?
printf '%s\n' "$out"
if printf '%s\n' "$out" | grep -E '(^|@)<this spec own paths>([ ,:]|$)'; then exit 1; fi
```

The rows stay visible; only lines naming this spec's own footprint decide
the exit. The needle is anchored at line start or `@` because index.py's
message names `references/files.md` in *every* line, so an unanchored needle
matched a neighbour's row.

spec05 carried a second one: `python3 resources/memos.py check`, also
board-wide, now captured and printed and never the exit.

### A standing check that could not fail

spec05's block held `! grep -n 'footprint:' resources/board/plan.py | grep -q
'is claimed and holds'`. **A leading `!` exempts a command from `set -e`**
(POSIX XCU 2.11), so that line could print its failure and the block still
exited 0 — proved: the mutation that reintroduced the gate's string left the
block at exit 0. Rewritten `if … ; then exit 1; fi`, which now reddens on
the same mutation. Recorded outside this report as `[[260902-69f0]]`.

### Mutation proof, per block

Each mutation was `cp`'d to a scratch dir outside the repo, applied, run,
restored, and the restore proved with `cmp`:

| spec | mutation in its own footprint | mutated | restored |
|---|---|---|---|
| spec01 | `lanes.py`: `return "lane/"` → `"LANE_X/"` | exit 1 | `cmp` equal, exit 0 |
| spec02 | `transitions.py`: `def drop_lane` renamed | exit 1 | `cmp` equal, exit 0 |
| spec03 | `brief.py`: the `laneslib` import renamed | exit 1 | `cmp` equal, exit 0 |
| spec04 | `collect.py`: `def land_lane` renamed | exit 1 | `cmp` equal, exit 0 |
| spec05 | `plan.py`: the gate's string put back | exit 1 | `cmp` equal, exit 0 |

spec01's and spec05's are **behavioural** — the branch-name computation and
the gate's own predicate. The other three are counter-wired proofs: they
show the check runs and its failure reaches the exit, not that the block
detects a regression in what the tool computes. The fixtures above carry the
behavioural evidence for those three.

## What was built, per spec

**spec01 — `resources/board/lanes.py`.** Two behaviours the probe proved
were needed and did not do, plus the manifest row:

- `create` now adds the worktree `--no-checkout`, excludes the board's path
  with `sparse-checkout set --no-cone '/*' '!/<board-rel>'`, then checks
  out. New helper `board_rel(board, repo)` returns None when the board is
  not under the repo. Measured on a repo that **tracks** its board: the lane
  holds no `.pearde/`, `git add -A` inside it stages no board deletion, and
  `plan.py scan` run with the lane as cwd resolves to the live board
  (`8 PRDs`), not to a phantom.
- `merge` now rebases the lane onto the branch the checkout is on — in the
  lane's own worktree, found by new `worktree_of(repo, branch)`, because git
  refuses to move a branch another worktree holds — then `merge --ff-only`.
  Measured on a checkout that moved after the lane was cut: **one** commit,
  `rev-list --merges` empty, `git branch --merged` lists the lane. A rebase
  conflict aborts, resets the lane branch to where it was, and raises
  `LaneError` naming `src/a.py`, with the checkout on its own commit and
  clean.
- `references/files.md` carries a row for `resources/board/lanes.py`.

**spec02 — `resources/board/transitions.py`.**

- `--dry` now names the lane dir under `would write:` and cuts nothing —
  `cut_lane` stays past the dry return, confirmed.
- The `## Failure` a sweep writes names the branch: partial code stands on
  branch `lane/<slug>`, whose worktree the sweep removed, the branch kept.
  `sweep_rows`'s own `why` line was carrying the same false sentence
  ("may stand in the tree") and now names the branch too.
- `drop_lane`'s docstring states that `sweep` is the only edge that drops a
  lane, and that `retry`, `release`, `question`, `refine` and `park` leave
  it — with the reason, so the next reader does not add a cleanup.

**spec03 — `resources/board/brief.py`.**

- The header line reads `repo <path> · lane lane/<slug>` when there is one,
  and adds nothing when there is not.
- `SKIP`'s dead `footprint → clash` entry dropped, with a comment saying why
  it can never be raised. Both spec03 and spec05 named this edit; it is made
  once, in the file spec03's footprint holds, and spec05's box reads it.
- `brief_consult` now has a docstring saying `<repo>` there is deliberately
  the checkout: a consultant holds no claim and so has no lane.

**spec04 — `resources/board/collect.py`, `references/parts/commits.md`.**

- New `commit_message(prd, prd_rel, opts, plan=None)` — the one builder.
  `land_lane` puts it on the lane's commit; step 4 puts it on its own, so
  the message exists once.
- **The three-commit defect is closed.** Where a lane landed, step 4 takes
  the merged HEAD as its sha and makes no second commit in that repo; what
  the board record staged there rides the `<prd> — record` commit behind it.
  Measured: `rev-list --count HEAD` gains **exactly 2** — `change-a — Change
  a` and `change-a — record` — with no merge commit and a clean checkout.
  `commit:` still names the commit holding the work, including where the
  board is its own repo and the code commit is in no `staged_roots`.
- `--dry` now prints `would merge lane lane/<slug> — N commit(s) … merged
  nothing` and merges nothing: `land_lane` handles `dry` itself, so the dry
  line and the real one come off one read of the lane.
- Step 3's shared-file refusal takes a new `landed` argument and stops
  running against the **code** repo when the work arrived through a lane.
  Kept for the board repo and for every laneless board; the path is not
  deleted, and `sort_paths`'s docstring says which is which.
- `snapshot` records the **lane** as the code side once the lane exists, so
  the `known — every line is in the claim's baseline` softening reads the
  tree the worker actually writes. Measured: `.claims/change-a/repo` holds
  the lane's path.
- `commits.md` gains "Where the commit is made: the lane" and "A merge
  conflict is a red collect, never a silent stage", and says a laneless
  board collects exactly as before.

**spec05 — `resources/board/plan.py` and five `references/parts/` files.**

- `bands`'s `ready` no longer excludes on `after`. `after` is built from
  `overlap(feet[r], feet[s])` and nothing else, and `cmd_plan` labels every
  one of them `(footprint)` — so that clause was the footprint clash
  operating as a dispatch gate one command along from the one spec05 just
  removed it from. `needs` still gates. `plan_frontier` keeps the edge, so
  `pearde plan` still prints `after … (footprint)` and says which goes
  first. Measured: `claim` takes the second PRD, `scan` lists it under
  `ready`, `plan` still orders the pair.
- `states.md`, `loop.md`, `machine.md`, `progress.md` and `order.md` all
  said the clash gates `claim`. All five now say the plan orders the pair
  and the merge resolves it. `machine.md`'s `dispatch`-wave clash and
  `view.md`'s timeline edge are a different, live mechanism and were left.

## Findings

- **spec05's `footprint:` was three files short.** Its box says no file
  under `references/` names the footprint clash as a gate on `claim`, and
  three did: `references/parts/machine.md:106`,
  `references/parts/progress.md:27` and `references/parts/order.md:6` — none
  in any spec's footprint. Per `re-run-the-harnesses`'s row for a file the
  contract moves that the footprint does not hold, I added the three to
  spec05's `footprint:` and made the one-clause correction in each. The
  spec's frontmatter is the only frontmatter this pass touched, and no PRD
  frontmatter was. The next author of a spec whose contract deletes a rule
  should sweep `references/` for the rule's wording before fixing the
  footprint.
- **A board harness can never measure a lane.** Every `verify.sh` computes
  `ROOT="$(cd "$(dirname "$0")/../../../../.." && pwd)"` — from its own path
  on the board, which is always the orchestrator's checkout. A worker
  working in its lane cannot move a single board-harness count until
  `collect` merges. Nothing in this PRD's contract covers it, and the
  workaround this run used (a scratch root whose `.pearde` is a symlink to
  the live board, so `ROOT` resolves to the merged tree) is a measurement
  trick, not a fix. Worth its own PRD: either the harnesses take `ROOT` from
  an environment variable the runner sets, or `collect` runs the set in the
  lane before merging.
- **The board's own `.gitignore` still has no `.lanes/` row.** The analyst
  named this and left it to the implementer; it is board state under
  `<board>/.gitignore`, which no spec's `footprint:` holds and which my
  brief forbids me writing. Measured now: `git -C .pearde status --short`
  prints `?? .lanes/`, and on a layout where the code repo tracks its board
  a person's `git add -A` gets `warning: adding embedded git repository`.
  `collect` is safe either way — `scratch()` skips board dotfiles and
  `commits.md` forbids `git add -A` — so this is a person's footgun, not the
  tool's. One line, `.lanes/`, beside the `.claims/` row already there.
- **`nothing-left-open`'s `E14` is decided by scheduling.** It asserts no
  `/tmp/pearde-index-*` exists — a machine-wide glob, not one scoped to what
  the harness itself started. Any sibling harness running `collect`
  concurrently reddens it. It went red in a 4-way parallel sweep and green
  serially, on the same tree. A finding for that PRD: scope the glob to the
  fixture's own `TMPDIR`.
- **`collect-keeps-its-word` cannot run outside the real repo.** It rebuilds
  a pinned collect with `git show e8b262d:…`, so it is red in any copy of
  the tree that lacks the history — including a `git archive` fixture. Only
  a `--shared` clone or the checkout itself measures it. Not a defect to
  fix; a constraint worth a line in the harness's own header, because a red
  there reads exactly like a regression.
- **`loop.md` is now at its 170-line ceiling**, asserted by two harnesses.
  There is no headroom left for the next edit.
- **`resources/index.py check` treats a symlinked `.pearde` as a file.** In
  the merged-tree simulation it printed `.pearde is on disk with no row in
  references/files.md` because the repo's `.gitignore` names `.pearde/` with
  a trailing slash. Only ever visible in a scratch root; noted so the next
  worker building one does not read it as a regression.

## Workflow probe-then-spec

| step | atomic | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass — hit the `Fails when` row for a lane cut off HEAD with the probe uncommitted in the checkout; carried five files, left `references/files.md`'s neighbour hunk. No back-edge. |
| 2 | `capture-the-harness-baseline` | pass — 37 harnesses, both gates, in both roots, before the first edit. |
| 3 | `attempt-the-build` | entered. The specs existed and the probe stood, but its build was **in the checkout, not in the lane** — the `Fails when` row for a second pass ("nothing to do because the build is already in the tree") did not hold, because the tree the brief named held nothing. Built in place in the footprint files, as step 3's rule for an edit to an existing file requires; no `probe/` staging. |
| 4 | `re-run-the-harnesses` | pass, twice — once on the checkout to show it did not move, once on a merged-tree simulation to measure the work. No back-edge. |
| 5 | `write-the-specs` | second-pass form: no spec authored, the `Fails when` table applied to the five blocks that stood. Three defects found and repaired in them. |

### Edits

Two rows the atomics are missing, both hit this run.

**`capture-the-harness-baseline` — add to `Fails when`:**

| seen | means | do |
|------|-------|----|
| every board harness computes its own `ROOT` by walking up from `$0`, and the `repo:` root is a lane | the harness set is nailed to the orchestrator's checkout and can never read a lane; a worker's build is invisible to all of it until `collect` merges | build the merged tree in scratch — `git clone --shared <checkout> <scratch>` (a `git archive` or `git init` copy loses the history a pinned-sha harness reads), `git apply` the checkout's uncommitted diff, overlay the lane's files — then symlink `<scratch>/.pearde` to the live board and run each harness **through that path**, so its own `cd …/../../../../..` resolves to the merged tree. Say in the report that the counts are the merged tree's, not the lane's |

**`write-the-specs` — add to `Fails when`:**

| seen | means | do |
|------|-------|----|
| a block line reads `! <cmd>` and a mutation that should redden it leaves the block at exit 0 | `set -e` does not apply to a command whose status is inverted by a leading `!` (POSIX XCU 2.11), so the line prints its failure and the block carries on | write it `if <cmd>; then exit 1; fi`. This is the same class as the `<test> && <action>` shape the section already names, and the `!` form is not covered by it — a block can hold one and read green forever |

**`write-the-specs` — a clarification to the existing board-wide-gate row.**
Its repair says to grep the captured output for "the rows". A needle spelled
as the bare footprint path over-matches: `index.py check` names
`references/files.md` in *every* line it prints, so a spec whose footprint
holds `references/files.md` fails on a line about a neighbour's file.
Anchor it — `grep -E '(^|@)<path>([ ,:]|$)'` — and say so in the row.

## Health

`none under the floor` — nothing in the footprint was under it, and nothing
moved.
