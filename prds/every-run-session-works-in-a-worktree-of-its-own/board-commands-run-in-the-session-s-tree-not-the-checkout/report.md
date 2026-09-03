# board-commands-run-in-the-session-s-tree-not-the-checkout — implementer report

Verdict: DONE

Second implementer pass. The first pass built and ticked all 36 boxes, and its
`collect` then **failed in the rebase**: `land_lane` commits the lane before it
merges, so the work was left committed on `lane/<slug>` at `89f3e8f`, the
checkout untouched, and the PRD still `claimed` with nothing on the board
saying so. That is exactly the shape step 3's `Fails when` table names. This
pass rebased the lane onto the checkout's branch, resolved three conflicts, and
re-proved every block.

| spec | boxes | block in the lane | block in the checkout | under a mutant |
|---|---|---|---|---|
| spec01 | 15/15 | exit 0 · 53 ok · 0 FAIL | exit 1 · 5 FAIL | exit 1 · 3 FAIL |
| spec02 | 14/14 | exit 0 · 65 ok · 0 FAIL | exit 1 · 9 FAIL | exit 1 · 3 FAIL |
| spec03 | 7/7 | exit 0 | exit 1 | exit 1 |

Harness set, same command and same `PEARDE_ROOT` on both runs: **52 of 76
failed before the rebase, 50 of 76 after.** The failing set is a strict
subset — nothing went green-to-red. The repo's own gate, `python3
resources/index.py check`, prints the same two lines before and after, both
naming files outside this footprint.

**The lane has landed.** It was left one commit ahead of `main`, clean and
fast-forwardable, and `lanes.merge --ff-only` took it during this pass: `main`
is now `31620bb`, the lane's own commit, with `lane/<slug>` pointing at the
same sha. One PRD, one commit, per @references/parts/commits.md. Verified on
`main` rather than in the lane: the `spelling_root` narrowing at
`collect.py:683`, the re-sited place at `collect.py:567`, `session.land`, both
kept rows in `references/files.md` and `references/parts/handles.md`, and the
false sentence gone from `references/parts/loop.md`. The checkout's working
tree carries one modification and it is a sibling's — `references/system.md`.

## What this pass did

Nothing in the contract was rebuilt: all 36 boxes were already ticked by the
first pass against checks that were run, and all 36 still hold on the final
tree. The work here was the merge the first pass could not complete.

### The three conflicts, and how each was resolved

`git merge-tree --write-tree --name-only main lane/<slug>` named three files.
All three are inside this PRD's footprint, which is the condition step 3's
table requires before a worker resolves rather than stops.

**1. `references/files.md` — adjacent lines, both kept.** The first pass
predicted this one exactly, under its own Findings. The checkout had since
committed a new `@resources/board/refuse.py` row immediately after the
`session.py` row, and this unit rewrites the `session.py` row itself. Resolved
by keeping both: this unit's rewritten `session.py` row first, the neighbour's
`refuse.py` row after it. Neither line was altered.

**2. `references/parts/handles.md` — the same shape.** The neighbour added a
`what a destructive git may do here` row directly after the
`a worktree per run session` row that this unit rewrites. Both kept, in that
order, neither altered.

**3. `resources/board/collect.py` — a neighbour replaced the mechanism this
unit patched.** This is the one that needed a decision rather than a paste, and
it is the finding of this pass.

### `spelling_root` outlived the containment test it was written for

Spec02's fix was to `foot_root`, which decided whether a footprint belonged to
the board's repo or the code repo by **joining the path onto the code repo and
testing the absolute result for the board's directory as a string prefix**.
This unit's change was one substitution inside that test: join onto
`spelling_root(board, board_root, repo)` rather than onto `repo`, so a session
worktree at `<board>/.sessions/<id>` does not put every footprint inside the
board by prefix.

Between the two passes, `collect-resolves-a-board-path-two-ways-and-both-are-wrong`
landed on `main` and **deleted that test**. `foot_root` now asks git which
checkout holds each candidate path — `foot_places` builds the candidates,
`holder` answers with `rev-parse --show-toplevel`, and the first place the
filesystem or an index holds wins. That is a strictly better fix to the same
underlying defect, and there is no longer a string prefix for `spelling_root`
to anchor.

The neighbour's body was taken whole. The question was then whether
`spelling_root` is dead. **It is not**, and it was measured rather than
assumed: reverting `foot_places` to `main`'s exact base list and re-running the
blocks turns both red on the same box —

```
FAIL a footprint under the board still routes to the board's repo:
  ('…/units/code/.pearde/.sessions/s92115', '.pearde/.gitignore')
    != ('…/units/code/.pearde', '.gitignore')
```

A worktree of the code repo does not carry the paths that repo **ignores**, and
the board is one of them: `.pearde/.gitignore` is absent from
`<board>/.sessions/<id>/pearde/` and from the board's own tree, so no candidate
place holds it and the footprint falls through to the session tree, which does
not hold it either. `spelling_root` was therefore re-sited as an extra **place**
in `foot_places` — tried second, after the code repo — rather than as a
substitution inside a test that no longer exists. Where no session holds a
tree, `spelling_root` is `repo` itself and the existing dedupe drops it, so a
board with no session tries exactly the three places it always tried.

### The regression that re-siting caused, and the narrowing that closed it

The first sweep after the rebase showed one harness going green-to-red:
`prds/the-verify-guard-parses-git-s-own-output-before-it-trusts-it/probe/verify.sh`,
`FAIL D probe_roots`. It is a neighbour's harness and it was honest — the extra
place had genuinely changed an answer it asserts:

```
AssertionError: {'<tmp>/.pearde': ['prds/mine'],
                 '/private/<tmp>': ['../../../../../../../var/<tmp>/resources/board/collect.py']}
        want: ["prds/mine", "resources/board/collect.py"] under the board
```

Cause: `under(parent, child)` is true for equality, so a board that **is** its
own code repo is "under itself", `spelling_root` answered the checkout one
level up, and a footprint the board genuinely holds was routed out of it — and
came back spelled `../../../../../../..` because that root is realpath-spelled
and no `known` root matched it.

The narrowing is that `spelling_root` fires only for a repo **strictly** under
the board and equal to neither the board nor the board's own repo:

```python
if not repo or same_dir(repo, board) or same_dir(repo, board_root):
    return repo
return checkout_of(board, board_root) if under(board, repo) else repo
```

That is faithful to the box's own words — a repo that *is* the board does not
"resolve inside the board", it is the board — and the case `spelling_root`
exists for is a tree cut BELOW the board, which is a session's and a lane's
alone. After it: the neighbour's harness reads `46 passed, 0 failed`, and all
three blocks stay at exit 0.

The rebased commit was **amended** with the narrowing rather than committed on
top of it, so the PRD stays one commit.

## Per-spec box status

No box was re-ticked: all 36 were ticked by the first pass against checks that
were run, and all 36 pass on the final tree. The evidence table for each box is
in the first pass's report and is not repeated. What this pass adds is that
every one of them was re-run **after** the rebase, on a tree that now carries
`main`'s four intervening commits:

| spec | final run in the lane |
|---|---|
| spec01 | `exit 0` · 53 ok · 0 FAIL |
| spec02 | `exit 0` · 65 ok · 0 FAIL |
| spec03 | `exit 0` |

Two boxes in spec02 are the ones the merge put at risk, and both were
re-measured directly rather than inherited:

- `a footprint under the board still routes to the board's repo while a session
  holds a tree` — this is the box the reverted-`foot_places` experiment turns
  red, so it is behaviourally backed, not merely wired.
- `a collect of a PRD whose footprint is ordinary code stages that code in the
  lane, not in the board repo, while a session holds a tree` — green through
  `endtoend.py`, and green through the neighbour's new git-holder mechanism.

## The mutation proof

`spelling_root` was made to `return repo` unconditionally — the exact defect
spec02 names — in `resources/board/collect.py`, a footprint file. Both blocks
went red on a **behavioural** difference, not a grep miss:

| spec | under the mutant | first FAIL |
|---|---|---|
| spec01 | exit 1 · 3 FAIL | `spelling_root for a repo the board hosts: False != True` |
| spec02 | exit 1 · 3 FAIL | `a footprint under the board still routes to the board's repo: (…/.sessions/s12033, '.pearde/.gitignore') != (…/.pearde, '.gitignore')` |

Restored by `cp` from a scratch directory outside the repo, and the restore
proved: `cmp` reports the files identical and `git status --short` in the lane
is empty.

All three blocks were also run **verbatim from the orchestrator's checkout**,
which holds none of this build: spec01 exit 1 · 5 FAIL, spec02 exit 1 · 9 FAIL,
spec03 exit 1. The whole gate ran on the tree that does not hold the build.

## The harness set

Same command, same `PEARDE_ROOT=<lane>`, on the lane before and after the
rebase:

| tree | harnesses failed |
|---|---|
| the lane at `89f3e8f`, as the first pass's collect left it | **52 of 76** |
| the lane rebased, before the narrowing | 51 of 76 — one green-to-red, named above |
| the lane rebased and narrowed | **50 of 76** |

Set difference, not just counts: the final failing set is a **strict subset** of
the pre-rebase set. `comm -13` over the two sorted sets is empty — no harness
went green-to-red.

Two harnesses went green, and **neither is this unit's flip**. Both are the two
commits the rebase brought in from `main`:

- `prds/collect-resolves-a-board-path-two-ways-and-both-are-wrong/probe/verify.sh`
  — its own PRD landed at `1880990`.
- `prds/every-run-session-works-in-a-worktree-of-its-own/no-destructive-git-runs-in-a-tree-the-session-does-not-own/probe/verify.sh`
  — landed at `ba69efa`.

Both were red on the pre-rebase lane precisely because the lane lagged the
checkout by those commits, which is the inherited-red shape step 2's table
names. They close on the merge and are claimed by nobody here.

## Findings

Every finding of the first pass is carried forward. Two are now closed.

**CLOSED — `references/files.md` will conflict on the merge.** It did, exactly
as predicted, and on `references/parts/handles.md` as well, which the first pass
did not predict. Both resolved by keeping both lines.

**CLOSED — the first pass's `collect` left the work stranded.** `land_lane`
commits the lane before it merges, so a rebase conflict leaves a finished PRD
committed on `lane/<slug>` with the board still saying `claimed` and no line
anywhere saying why. That silence is the defect, not the conflict: a conflict
is ordinary and a person can resolve it, but nothing on the board named it. It
belongs to `collect`'s own PRD, not to this one — **reported, not fixed.**

**`spelling_root`'s rationale in `specs/spec02.md` is now stale.** The spec's
prose section *A footprint spelled against a tree the board hosts* describes
`foot_root`'s string-prefix containment test and says the fix anchors that test
to the checkout. The test is gone and the fix is now an extra place in
`foot_places`. Every acceptance box in that spec still holds and none was
touched, so the contract is intact — but the rationale a later reader will
trust is describing code that no longer exists. Not rewritten here: redefining
a spec is not the implementer's act. The replacement sentence is: *"`foot_root`
now asks git which checkout holds each candidate place; `spelling_root` is the
second place it tries, and it is a place only while a session holds a tree."*

**`pearde help` cannot print one line per session verb without
`resources/pearde.py`.** `help_lines` gives a `FORWARD` entry one line per verb;
a module found by discovery gets one line built from its `cmd_*` docstring,
truncated at 80 columns. `session.py`'s docstring already carries the five
usage rows, so the whole fix is adding `session` to `FORWARD` with its verb
tuple. Outside this footprint — carried forward, still open.

**The `all` master row on the live daemon has `path: None`.** `serve.py status`
prints `all synced never · None · master of 10`, and `os.path.abspath(None)` is
the `TypeError` that makes every collect on this machine say `daemon answered
in another shape — report not posted`. `collect.post_report` catches it exactly
as its docstring promises, so nothing tears; the defect is the daemon's row.
Carried forward, still open.

**`resources/invariants/no-colour-group-in-the-vault-preset-is-a-path-query.sh`
fails inside any lane** — `BROKEN: no board at pearde/`. Same family as
`two-harnesses-still-name-a-tree-they-do-not-measure`. Carried forward, not
touched.

**`python3 resources/index.py check` reports two unresolved references from
inside the lane** — `references/language.md` naming
`@references/personas/writer.md`, and `references/parts/commits.md` naming
`@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`. The checkout
prints only the first: the second is the lane's missing board, which step 2's
table says never closes on a merge and is not a defect in the file. Both
outside this footprint, both unchanged across this pass. Carried forward.

**Nothing calls `session take` yet.** Carried forward: `loop.md` now says what
a session gets from `take` onward, but taking one is still prose a pass
follows, not code. That belongs to the parent and to the run verb.

**A live sibling is writing the checkout.** `references/system.md` gained an
uncommitted `@` to `@@` hunk at 09:02:10 during this run, and the checkout's
HEAD moved twice mid-pass — `1880990` then `0c8fd02`, adding
`board-rel-is-a-third-wrong-board-path-resolution` and
`the-daemon-must-not-write-into-a-board-path-it-no-longer-own`. Not this unit's:
no module under `probe/` names `references/` at all. The lane was rebased a
second time onto the new `main` — that rebase was conflict-free — so the
fast-forward claim above is against `main` as of the end of this run.

## Health

The brief listed no footprint file under the health floor, and none was
refactored. The only edits this pass made were the three conflict resolutions
and the one-condition narrowing of `spelling_root`, each inside the footprint
file it belongs to.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | read-the-contract | pass — the PRD body is the title twice, so the contract was read from `specs/` and the first pass's `report.md`, per the table's last row. `git status --short` recorded in the lane, the checkout and the board repo before the first edit. The lane was **clean and committed**, which is the row this pass turned on |
| 2 | capture-the-harness-baseline | pass — the earlier build was committed on the lane, so the baseline is the lane's own tree at `89f3e8f`, taken with `PEARDE_ROOT=<lane>` before the rebase: 52 of 76 |
| 3 | attempt-the-build | entered for **no spec** — all three were built and all 36 boxes held. The work was the merge, which the route treats as step 3's `Fails when` row rather than as building |
| 4 | re-run-the-harnesses | pass — same command, same `PEARDE_ROOT`, subset comparison. One green-to-red was found, traced to this pass's own edit, and closed by the narrowing rather than explained away |
| 5 | write-the-specs | not entered as spec-writing — the second pass. Its `Fails when` table was applied to the three blocks that already stood: each run under `bash -e -o pipefail`, green in the lane, red verbatim in the checkout, red under a behavioural mutation, restored with `cmp` |

### Edits

**Step 3, `## Fails when`, the stranded-lane row is incomplete.** The row
`the brief says the probe's code is uncommitted, and git status --short is
clean` correctly predicts this pass's situation and correctly says to rebase
when every conflicting file is inside the footprint. What it does not say is
what to do when a **neighbour has replaced the mechanism your hunk patched** —
which is not a textual conflict to resolve but a design question, and pasting
either side is wrong. Append to that row's `do`:

> Where a conflicting hunk of yours patches a function a neighbour has since
> **rewritten**, take the neighbour's body whole and then measure whether your
> unit is still needed, rather than deciding it from reading: revert your own
> addition, run your spec's block, and read which boxes go red. A hunk that
> changes nothing when removed is superseded and should be dropped; a hunk that
> reddens a box is still load-bearing and must be re-sited into the new
> mechanism, never restored into the old one. Say in the report which it was
> and quote the failing box.

**Step 4, `## Fails when`, a green-to-red that IS yours.** Every row in this
section explains a moved count as somebody else's — a neighbour's landing, a
moved harness text, a workspace-wide check. There is no row for the honest
case, which this pass hit: a harness outside the footprint goes red because
your own edit genuinely changed an answer it asserts, and the harness is right.

| seen | means | do |
|------|-------|----|
| a harness outside your footprint goes green-to-red, and its failing assertion names a value your own edit computes | your change is broader than the box that asked for it — commonly a predicate true in a case you never considered, such as `under(a, a)` being true for equality | do not edit the neighbour's harness and do not quote it as inherited. Read its assertion, find the case your edit widened into, and narrow your own condition until both the neighbour's harness and your own blocks are green. Quote the neighbour's failing assertion, the narrowing, and both green results — a narrowing found this way is the box's real boundary, and the box's own words usually already exclude the case |

**Step 2, `## Fails when`, add a row.** The section covers a lane whose earlier
build is uncommitted, and a lane whose pass published counts. It has no row for
the state this pass actually found:

| seen | means | do |
|------|-------|----|
| the lane is **clean**, its HEAD carries the PRD's own commit, and the PRD is still `claimed` | the previous pass's `collect` ran and its rebase conflicted: `land_lane` commits the lane before it merges, so the work landed on `lane/<slug>` and nothing else moved | the lane's own HEAD **is** the baseline tree, and it is already committed — run the set with `PEARDE_ROOT=<lane>` and record it directly, with no clone and no revert. Then `git merge-tree --write-tree --name-only <trunk> lane/<slug>` before the first edit: the conflicting files are the pass's actual work, and whether they are all inside the footprint decides between resolving and stopping |

## The record

Nothing was learned outside this repo this pass — no web source, no library the
tree does not hold — so nothing was written with `knowledge.py remember`. The
notes the first pass recorded (`[[260902-aae0]]`, `[[260902-b1f6]]`,
`[[260902-b6be]]`, `[[260902-f2fe]]`, `[[260902-eb91]]`) still hold.

## Scores

complexity: 26
blast-radius: high
workflow: probe-then-spec
