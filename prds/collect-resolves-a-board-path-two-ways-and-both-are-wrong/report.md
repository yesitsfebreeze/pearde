# collect-resolves-a-board-path-two-ways-and-both-are-wrong — implementer report

Verdict: DONE

3 specs · 22 of 22 boxes ticked · spec01 8/8, spec02 7/7, spec03 7/7.
Every `## Verify and Proof` block exits 0 the way `collect` runs it
(`bash -e -o pipefail`) and non-zero on the tree that does not hold the build.

This is the route's second pass. Pass one (the analyst) probed, built spec01's
code and wrote the three specs; its findings stand below under
`## Findings carried forward`. This pass landed spec02 and spec03, which pass
one left entirely unwritten, ticked all three sets against commands it ran, and
repaired one verify block that could never have passed.

## Where the work is

| file | root | state |
|---|---|---|
| `resources/board/collect.py` | lane | pass one's build, unchanged by me |
| `resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh` | lane | spec02, written this pass |
| `references/parts/commits.md` | lane | spec03, written this pass |
| `memos/a-board-s-own-file-commits-in-the-board-repo.md` | board | spec03, written this pass |

The lane is `/Users/feb/dev/infra/pearde/pearde/.lanes/collect-resolves-a-board-path-two-ways-and-both-are-wrong`,
cut at `64ed54a`, which is the checkout's HEAD — nothing landed under it while
I ran. The memo is not in the lane and could not be: `pearde/` is the board,
a linked worktree on branch `pearde`, and the lane is a worktree of `main`
cut without it. It was written in the board directly, which is what
`foot_root` now resolves `pearde/memos/<file>` to.

`git status --short` at the end names, in the lane, exactly the three files
above and nothing else. In the board it names my memo edit and the PRD folder.
In the orchestrator's checkout it names nothing of mine.

## What this pass built

**spec02 — two new sections in the invariant, 12 assertions to 20.**

`board-spelled` (4 rows) builds the nested layout with the footprint spelled
the board's own way, `prds/p1/probe/verify.sh`, and asserts the board repo's
new commit holds it and the code repo's does not. `under` (4 rows) builds the
board as its own repo with the CODE repo checked out inside it at `work/`,
the board ignoring `work/` exactly as it ignores `.lanes/`, and asserts the
code file lands in the CODE repo's commit and that the board's commit carries
it under **no** spelling — the old behaviour committed nothing and said
nothing, so an exit code could not catch it.

Both sections use `code_work`, a lane-cutting helper without `work`'s board
edit: appending a line no footprint names would leave foreign dirt on the
board and the run would be measuring the park rather than the routing.

**It can fail, measured, not asserted.** Run against `git show
HEAD:resources/board/collect.py` — the pre-build module, which has no
`foot_places` — through the file's own `COLLECT=` hook:

```
FAIL  board-spelled: collect exits 0 (got 1) — collect: p1: fatal: pathspec
      'prds/p1/probe/verify.sh' did not match any files — nothing written
FAIL  board-spelled: a NEW commit in the BOARD repo holds prds/p1/probe/verify.sh
FAIL  under: the CODE repo commits resources/board/session.py
3 check(s) failed — the invariant is broken.
```

The twelve rows that existed before stay green under that same mutant, which
is the point of the two new sections: the guard was blind to both defects.

Note which row does *not* fire on the mutant: `under: the BOARD repo commits
the code path under no spelling` stays PASS, because the old code routed the
path to the board, git refused the ignored pathspec, and **nothing was
committed anywhere**. That is the silent failure the memo describes, and the
row that catches it is its partner, `under: the CODE repo commits …`.

**spec03 — the prose and the memo.** `references/parts/commits.md`'s "Which
repo a footprint path lands in" now opens on the checkout's answer
(`git rev-parse --show-toplevel`) rather than the board's path as a prefix,
says both spellings resolve and which to prefer, and carries a paragraph of
its own saying a code checkout nested under the board is its own repo. The
memo's `## Decision` carries the same three sentences, its `## Consequences`
no longer calls `pearde/<file>` "the one way there is", and its `prds:` names
this PRD. `memos/README.md` is generated from `subject:`, which did not move,
so no index row is owed — and regenerating it would have clobbered a sibling's
uncommitted prose pass over that file.

## Verify and Proof — run as `collect` runs it

`bash -e -o pipefail -c "$(awk ... <spec>)"`, from a merged tree built the way
`capture-the-harness-baseline` prescribes: `git clone --shared` off the
checkout at `64ed54a`, the checkout's uncommitted diff applied, the lane's
three files overlaid, `pearde` and `.pearde` symlinked to the live board.

| spec | merged tree (holds the build) | checkout (does not) |
|---|---|---|
| spec01 | exit **0** | exit **1**, dies on `grep -n "def holder"` |
| spec02 | exit **0** — `PASS`=20, `under:`=4, `board-spelled`=4 | exit **1** — `PASS`=12, `under:`=0 |
| spec03 | exit **0** — `the claim is gone` | exit **1** — the `show-toplevel` needle counts 0 |

Verbatim red before the merge and green after, with the whole gate running on
the old file — the evidence `write-the-specs` asks for and stronger than
`git show HEAD:`.

**spec03's block detects a regression, not only a wired counter.** Two
mutations of the memo, each restored by `cp` from a scratch dir outside the
repo and the restore proved by `cmp`:

| mutation | block exit |
|---|---|
| `the one way there is` put back into `## Consequences` | **1** |
| a stray frontmatter key `author: nobody` | **1** — `memos.py check rc=1`, naming the memo |
| restored | **0** |

The second also proves `python3 resources/memos.py check` run bare from the
repo root is not vacuous: it finds the board and names the file.

## The block I repaired, and why

`spec03`'s `## Verify and Proof` as pass one wrote it ran two board-wide gates
bare: `python3 resources/memos.py check` and `python3 resources/index.py
check`, each on its own line.

`index.py check` is red in the orchestrator's checkout on a line this unit does
not own — `references/language.md references @references/personas/writer.md —
not on disk`, pass one's own second finding. Under `-e` that line is the
block's exit, so the spec could never have passed `collect` however green the
work was. Repaired per `write-the-specs`' own row: both gates are captured
(`out=$(… 2>&1) && rc=0 || rc=$?`), their output printed, a crashed producer
refused by `[ "$rc" -le 1 ]`, and the block gated only on output lines naming
a path in its own `footprint:`. Two content needles were added so the box
about the nested-checkout paragraph is read by a check rather than by a
reader. Nothing was weakened: the block still exits 1 on either mutation
above.

`spec01`'s and `spec02`'s blocks were left as written.

## Harnesses

Baseline taken in the lane with `PEARDE_ROOT=<lane>`, before the first edit;
re-run identically at the end. Full output of every run is under this run's own
scratch subdirectory.

| harness | baseline | after | note |
|---|---|---|---|
| this PRD's `probe/verify.sh` | 7 · 7 · 0 | 7 · 7 · 0 | |
| `a-board-s-own-file-commits-in-the-board-repo.sh` | 12 PASS | **20 PASS** | +8 rows, this pass added them (spec02) |
| `collect-keeps-its-word` | 101 · 101 · 0 | 101 · 101 · 0 | |
| `collect-is-a-command` | 133 · 133 · 0 | 133 · 133 · 0 | |
| `hunks-land-where-they-came-from` | 47 · 47 · 0 | 47 · 47 · 0 | |
| `filing-refuses-a-file-it-does-not-hold` | 52 · 52 · 0 | 52 · 52 · 0 | |
| `collect-must-not-reset-the-checkout-it-did-not-write` | 31 · 31 · 0 | 31 · 31 · 0 | |
| `post-report-crashes-a-collect-…` | 75 · 75 · 0 | 75 · 75 · 0 | |
| `a-verify-block-must-not-destroy-the-checkout-it-runs-in` | 24 · 0 fail | 24 · 0 fail | |
| `the-verify-guard-parses-git-s-own-output-…` | 46 · 0 fail | 46 · 0 fail | |
| `collect-stages-a-shared-file-whole` | exit 0 | exit 0 | |
| `nothing-left-open/the-line-tells-the-truth` | 85 · 44 · **41 fail** | 85 · 44 · 41 fail | red before the first edit |
| `the-brief-names-the-verdict-line-collect-requires` | 13 ok · **2 FAIL** | 13 ok · 2 FAIL | red before the first edit |
| `every-module-finds-its-siblings-by-one-rule` | 3 pass · **20 fail** | 3 · 20 | red before the first edit |
| `workflows-on-the-board/workflow-improve` | **62/71** | 62/71 | red before the first edit |

The harness set is the 13 that name a footprint path of this PRD (`grep -rl`
over all 75 board harnesses), plus this PRD's probe and the invariant. Nothing
moved but the invariant, and that rise is this unit adding its own assertions
— not a flip to attribute, and every pre-existing count is individually
unchanged.

The repo's own gates:

| gate | baseline | after |
|---|---|---|
| `index.py check`, checkout | exit 1 · 1 line (`language.md` → `writer.md`) | identical |
| `index.py check`, merged tree | — | exit 1 · same 1 line |
| `memos.py check` | exit 0 | exit 0 |
| `doctor.sh`, checkout | `index` / `origin` / `knowledge` broken | byte-identical excluding the `statusline` row |

`index.py check` run **inside the lane** prints a second line —
`references/parts/commits.md references @pearde/memos/… — not on disk`. That
is the lane having no board at all (`lanes.create` cuts it without `pearde/`),
not a defect in the file, and it is absent in the checkout and in the merged
tree. It was present in the baseline too. See `### Edits`.

## Findings carried forward from pass one — still open, still not mine

- **`board_rel` is a third resolution of a board path, and it is also wrong.**
  `sort_paths` computes `board_rel = os.path.relpath(board, board_root)`,
  which is `"."` on a board that is its own repo, and `inside(path, ["."])` is
  False for every path. `scratch()` stops recognising the board's machine-local
  dotfiles and the rider sweep never fires; a `--dry` collect lists 523 board
  paths as "inherited, not added". Same shape as spec01, a different resolver
  and a different contract — a PRD of its own. I did not reach it either.
- **`references/language.md` references `@references/personas/writer.md`,
  not on disk.** The one line `index.py check` prints in the checkout. It is
  what forced the spec03 block repair above, so it now costs a real unit's
  time, not only a red row.
- **Harnesses red before anything of mine**: `every-module-finds-its-siblings-
  by-one-rule` 3/23 and `workflows-on-the-board/workflow-improve` 62/71, both
  from pass one. Add, measured this pass and not in pass one's list:
  `nothing-left-open/the-line-tells-the-truth` 44/85 and
  `the-brief-names-the-verdict-line-collect-requires` 13 ok · 2 FAIL. Four red
  harnesses in the set that reads `collect.py`, none of them moved by this PRD.
- **`doctor.sh` reports `origin` (33 derived, 1 with no `from:`) and
  `knowledge` (`graph.json` behind: `260902-4f91`, `260902-aae0`) broken.**
  Unchanged, unrelated.
- **`lanes.py:90` decides the board's place inside the code repo by
  `os.path.relpath(board, repo)`** — the same string reasoning spec01 removed
  from `collect.py`. On the layout where the code repo sits under the board
  that relpath begins `..` and excludes nothing. Not reached.
- **Pass one ran `pearde specced` without `--dry`** and restored the
  frontmatter by hand; one spurious row stands in `.state/transitions.jsonl`.
  Recorded, not touched.

## Findings this pass

**`repo_of` looks only upward from the board, so a code repo checked out
under the board is invisible to it.** Building spec02's `under` fixture, the
first run refused with `footprint resources/board/session.py is in no repo
that holds it — looked for <board>/resources/board/session.py`. With no
`repo:` key `repo_of` resolves the code repo as `repo_root(dirname(board_root))`
and nothing else, so with the checkout *below* the board it walks past both
and lands on the board itself. The fixture names `repo: work` in the PRD's
frontmatter, which is the honest way a board says where its code is and makes
the layout reachable. This is not a defect spec01 contracted — `foot_root` is
right, `repo_of` never sees the case — but any PRD whose code repo is not the
directory above its board must carry `repo:` or be refused with a message
that blames the footprint.

**Nothing was learned outside this repo**, so nothing was written back with
`knowledge.py remember`. Every term in the contract is in
`resources/grammar.py show`.

## Workflow probe-then-spec

| # | step | verdict |
|---|------|---------|
| 1 | `read-the-contract` | ok — `prd.md` is the unedited template; the contract was taken from `specs/` and pass one's `report.md`, per the atomic's own row |
| 2 | `capture-the-harness-baseline` | ok — 15 harnesses and 3 gates baselined in the lane under `PEARDE_ROOT`, before the first edit; four red rows recorded as red before the first edit |
| 3 | `attempt-the-build` | entered — spec01's build already stood; spec02 and spec03 were unwritten and were built this pass, in place in their footprint files, not under `probe/` |
| 4 | `re-run-the-harnesses` | ok — every count identical but the invariant, which rose by the rows this unit added |
| 5 | `write-the-specs` | not entered as authoring — the specs existed; its `Fails when` table was applied to the three blocks that stand, and spec03's was repaired under the board-wide-gate row |

### Edits

**`attempt-the-build` — `## Fails when`, a row that is not there.** A fixture
that builds one repo inside another hits a resolver the contract never
mentions, and the refusal names the footprint rather than the layout:

| seen | means | do |
|------|-------|----|
| a fixture that checks the code repo out INSIDE the board refuses with `footprint <p> is in no repo that holds it — looked for <board>/<p>` | `repo_of` resolves a missing `repo:` as the repo *enclosing* the board and never looks below it, so a checkout under the board is invisible and `repo` comes back as the board itself | give the fixture's `prd.md` a `repo: <dir>` key — it is resolved against the board's own root and is how a board says where its code lives. The refusal names the footprint, so the first four reads go to `foot_root`, which is not the function that decided anything |

**`capture-the-harness-baseline` — `## Fails when`, and step 4's lane row
covers only half of this.** Step 4 has "a repo-wide gate is red in the lane on
lines the orchestrator's checkout does not print", and explains it as the lane
being behind the checkout's uncommitted work — a line that closes on the
merge. There is a second, permanent cause with the same symptom:

| seen | means | do |
|------|-------|----|
| a repo-wide reference gate (`index.py check`) is red in the lane on a line naming an `@pearde/…` or `@.pearde/…` target, and green in the checkout | `lanes.create` cuts the lane deliberately without the board, so every reference from a tracked file into the board dangles there by construction — this never closes on a merge and is not a defect in the file | baseline the gate in both roots and quote both. A line whose target is under the board is the lane's missing board and nothing else; count only the lines whose target exists in the checkout. Do not add the board to the lane to silence it — a second board under a lane is a board the scan will find |

**`write-the-specs` — the existing board-wide-gate row is right and its
"means" is one cause short.** The row explains the refusal as `pipefail`
carrying a gate's exit out of a pipeline. The block that failed here had no
pipeline at all: two bare gate calls, and `-e` took the second one's exit
directly, because that gate is red on an inherited line the unit does not own.
Suggested replacement for that row's `means` cell:

> a line in the block is a **board-wide gate** — `doctor`, a full harness
> sweep, a repo-root `git status`/`git diff`, `index.py check` — and it decides
> the block's exit two ways: `-e` takes a bare call's status, and `pipefail`
> takes it out of a pipeline. Either way the unit's pass is conditional on
> every other PRD on the board, and a gate already red on an inherited line
> means the spec can never pass, however green the work is. `141` instead of
> `1` is the same shape sigpiped into a `grep -q`

## Scores

complexity: 32
blast-radius: high
workflow: probe-then-spec
