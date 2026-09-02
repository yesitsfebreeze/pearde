# a-cross-board-need-that-names-no-board-in-the-scan-is-ignore — implementer pass

Verdict: DONE

`specs/spec01.md` — 7 of 7 acceptance boxes ticked, each against output quoted
below. The build was already standing in the lane from the analyst pass; this
pass measured it, proved the boxes can fail, proved the block exits the way
`collect` needs it to, and measured the predicted merge collision instead of
predicting it again.

Nothing was written outside `.pearde/prds/<this prd>/`. The lane is exactly as
the analyst left it — `git -C <lane> diff --stat` still reads four files,
`56 insertions(+), 6 deletions(-)`. **The merge is not done and is not mine:**
`lanes.commit_all`'s own docstring is *"The worker never commits; this is the
ORCHESTRATOR closing the lane before it merges."* The spec said the implementer
merges; that sentence was wrong and is corrected in the spec.

## Boxes

| # | box | evidence |
|---|-----|----------|
| 1 | `crossboard` dispatchable, `typo` still held | `verify: 9/9` |
| 2 | `membertypo` held, `absent` dispatchable | `verify: 9/9` |
| 3 | `ownname` held | `verify: 9/9` |
| 4 | the two stderr messages differ | quoted below |
| 5 | the boxes can fail | `verify --vs-head: 2 of 9 rows FAIL against HEAD — crossboard, absent` |
| 6 | no-op over all 104 PRDs | two diffs, both empty |
| 7 | `index.py` introduces nothing | one line, inherited, `edit.py` not in the diff |

## Verify output

`## Verify and Proof` run the way `collect` runs it, `bash -e -o pipefail` over
the awk-extracted fence — **exit 0**.

```
verify: 9/9 — every needs shape lands where the contract says
verify --vs-head: 2 of 9 rows FAIL against HEAD — crossboard, absent
1830:def unscanned_need(prds, d, board=None)
3
282:            if planlib.unscanned_need(prds, d, board):
references/parts/master.md:1
references/parts/contract.md:1
resources/board/edit.py references @questions.py — not on disk
```

Box 4, the two messages the change separates, from the probe's own stderr:

```
plan: absent needs '@elsewhere/thing' — that board is not in this scan, ignored
plan: membertypo needs '@member/nope' — that board is in this scan and holds no such PRD
plan: ownname needs '@masterboard/nope' — that board is in this scan and holds no such PRD
```

Against `git show HEAD:` copies of the two readers, all three read *"that board
is not in this scan, ignored"* — the message that made a member sitting right
there look absent.

### The block can fail, behaviourally

Not only "the counter is wired". A copy of `plan.py` outside the repo had the
new branch's `continue` turned into `pass` — the behaviour, not a string a
`grep` reads. The block went **exit 1**, `verify: 7/9 — off contract:
crossboard, absent`: exactly the two rows the contract moves. The lane was
never mutated; the mutation lived in a scratch tree, and `git -C <lane> diff
--stat` after it still reads the same four files and `+56/-6`.

### Box 6, twice

- lane build vs a HEAD-copy tree of the two readers, `dispatchable` over all
  104 PRDs: **byte-identical**. The HEAD copy provably lacks the helper —
  `grep -c unscanned_need` is `0` there and `3` in the lane.
- main's working tree (the sibling's in-flight work, without this lane) vs the
  same tree with this lane merged in: **byte-identical**, 104 lines each. So
  the change is a no-op on top of the sibling's too, not only on top of `HEAD`.

## The merge, measured

The analyst predicted a collision with the claimed PRD
`the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-dispatched-in-parallel`,
which holds uncommitted hunks in both `resources/board/plan.py` and
`resources/board/transitions.py` in the main checkout. It is now measured, with
`git merge-file --diff3` over the common base — nothing written, nothing staged:

- `transitions.py` — **exit 0, clean.** Its hunks are at lines 390, 461, 935,
  963; mine is at 282. Disjoint.
- `plan.py` — **exit 1, exactly one conflict**, and it is four lines of
  docstring, not code. Both code edits land clean: my `continue` into the
  `needs` loop, and their removal of the footprint-clash block.

The conflict is the workflow's own "adjacent changes merge into one hunk" row:
my edit rewrites the `- needs —` docstring line, theirs deletes the
`- footprint —` line directly beneath it. The resolution is to keep this lane's
four lines and drop the `- footprint —` row, and it is now written into the
spec's `## What is left` verbatim, so whoever merges pastes rather than judges.

Resolved that way the pair parses, the probe is `9/9` on the merged tree, and
box 6's second measurement above is that merged tree.

Note for the orchestrator: `resources/board/collect.py` in the main checkout
contains **no reference to `lanes`** — a grep for `lanes.` in it is empty.
`lanes.py` is untracked and its merge path is not wired into `collect` yet, so
closing this lane is a hand-run of `lanes.commit_all` + `lanes.merge`, or a
plain `git merge lane/<slug>`, until that PRD lands.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | pass. Specs read, footprint resolved in both roots, `git status --short` recorded in both before the first edit |
| 2 | `capture-the-harness-baseline` | pass, scoped — see below |
| 3 | `attempt-the-build` | **not entered.** The `Fails when` row "the route's steps 3 and 5 have nothing to do because the specs already exist and the build is already in the tree" is this pass exactly. Every red-to-green here was earned by the analyst pass; I claim no flip |
| 4 | `re-run-the-harnesses` | pass. `index.py` in both roots, the probe both ways, the block under `-e -o pipefail`, the mutation |
| 5 | `write-the-specs` | **not entered as authoring.** Its `Fails when` table applied to the block that already stood, which is what the row licenses |

### Step 2 was scoped, and why

23 of the board's 60 harnesses name a footprint path, and none of them can move
from this run: **every byte this pass wrote is inside
`.pearde/prds/<this prd>/`, and the build under test is in a lane worktree
those harnesses never read.** A harness in the main checkout measures the main
checkout, which this pass did not touch. Baselining 23 harnesses to prove they
were unmoved by a run that wrote nothing they read would have been ceremony,
and the main checkout is dirty with a sibling's in-flight work, so a baseline
taken there is attributable to nobody. The scoped equivalents were taken
instead and are quoted above: `index.py` in both roots before the first edit,
and `dispatchable` over all 104 PRDs.

Recorded before the first edit:

- main checkout `git status --short` — 12 modified, 1 untracked
  (`resources/board/lanes.py`); HEAD `59fb13a`, unmoved across the run.
- lane `git status --short` — the four footprint files; HEAD `029d5df`.
- All four footprint files are **byte-identical at `029d5df` and `59fb13a`**
  (`shasum` each way), so the lane's diff sits on the same base main is on.
- `python3 resources/index.py` **before the first edit**: lane exit 1, one
  line, `resources/board/edit.py references @questions.py — not on disk`; main
  exit 1, one line, `resources/board/lanes.py is on disk with no row in
  references/files.md`. Both inherited, neither ours.
- No fixture board leaked: `serve.py status` lists the same 10 registered
  boards and no `xboard-head-*` or `mktemp` path, and `ls .pearde/prds` is 62,
  with no slug this run made.

The brief's inherited line is **only in the lane**. In main it is gone and a
different one stands: the sibling has `resources/board/edit.py` modified and
closed it, and added `lanes.py` with no `files.md` row. Per step 2's row for a
brief whose baseline is older than the tree, my own baseline is the
measurement and the flip is the sibling's, not mine.

### Edits

Three, all from failures this route's atomics caused on this run.

**1 — `capture-the-harness-baseline`, step 1, after "Locate the board root
first".** The route has no row for a lane worktree, and a worker who takes
"the repo root" literally will baseline and verify in the checkout the
orchestrator holds — dirty with a sibling's work — instead of the tree its
own build is in. Add:

> Where the brief's `repo:` is a **lane** (`<board>/.lanes/<slug>`, a git
> worktree on `lane/<slug>`), that worktree is the tree under test and the
> only tree this run may write. The board is **not** inside it — `.pearde/`
> is gitignored, so a lane has no `prds/`, and a verify block spelling
> `.pearde/prds/<prd>/probe/…` cannot run from the lane root as written. That
> is not a defect in the block: `collect` runs it from the checkout after the
> merge, where both halves exist. To run it before the merge, build the tree
> `collect` will see — symlink the lane's entries into a scratch dir, add a
> `.pearde` symlink to the real board, and overlay the merged readers — and
> run the block there. Never repoint the block at the lane; that would break
> the runner it is written for.

**2 — `attempt-the-build`, the second-pass `Fails when` row.** It says to run
"steps 1, 2 and 4 only" and never says where the implementer ticks the boxes,
so the one act the second pass exists for has no step. Replace the row's `do`
cell's first clause with:

> run steps 1, 2 and 4 only, **ticking each acceptance box in step 4 as its
> check comes back green rather than in a batch at the end** — those boxes are
> the board's only live view of the run — say in the report which steps were
> not entered and why, and claim no flip.

**3 — `write-the-specs`, step 4, the `pipefail` paragraph.** The paragraph
warns about a board-wide gate inside a *pipeline*; it does not name the shape
that actually bit here, which is a repo gate called **bare** on its own line
whose exit is non-zero on a defect the box itself names as inherited. Append:

> The same applies to a repo gate called bare on its own line. `index.py`,
> `doctor` and `just all` exit non-zero on any pre-existing red anywhere in
> the tree, and under `-e` that becomes the block's exit — so a block whose
> own box says "this line stands at `HEAD` and is not ours" can never exit 0
> while it calls the gate bare. Capture, print, and gate on the footprint:
> `out=$(<gate> 2>&1) && rc=0 || rc=$?`, `[ -n "$out" ] || exit 1`, then
> `if printf '%s\n' "$out" | grep -E '<footprint paths>'; then exit 1; fi`.

## Findings

Carried forward from the analyst pass, all still open and none fixed here:

**A member path written the documented way is silently dropped.** Unchanged.
`references/parts/master.md` and `references/settings.md` show `members:`
entries as `- ../mitosys/prds`; under the `.pearde` layout `plan.members`
treats a basename of `prds` as already-a-board and appends nothing, so the
documented form resolves to a directory that does not exist and the member
contributes zero PRDs with no line saying so. The working form is
`- ../<repo>/.pearde`. Outside this contract.

**`held` is a word this board uses everywhere and defines nowhere.** Confirmed
again this pass, and it is now three words, not one: `grammar.py show` returns
*"is not defined on this board"* for **`held`**, **`ignored`** and **`lane`**.
The first two are the entire distinction this PRD's title turns on; the third
names the unit of work every worker on this board now runs inside. Three rows
owed to `.pearde/grammar.md`, which is outside my footprint.

**The `needs` grammar row is now short of the truth.** Unchanged — it reads
"PRD directory names that must be `done` first", with no `@<board>/<prd>` and
no word on what happens when the board is not there. `references/parts/contract.md`
now carries the rule; the grammar row does not.

**A footprint collision at merge time.** Now measured rather than predicted —
see *The merge, measured* above. One conflict, docstring only, resolution
written into the spec.

**A job that recurs and already has a file.** Unchanged. The `--vs-head` idiom
is reinvented by every `probe-then-spec` run and is a step in no workflow.

New this pass:

**The spec's verify block could not exit 0, and would have failed `collect`
for a reason unrelated to the work.** Its last line called `python3
resources/index.py` bare; the gate exits 1 on the inherited
`edit.py references @questions.py` line, and `collect` runs blocks under
`bash -e -o pipefail`, so `collect` would have refused with `spec01 exit 1 —
nothing written` on a green unit. Repaired in place per step 5's own
prescription — captured, printed whole, gated only on lines naming one of this
spec's four footprint files. The measurement is unchanged; only the exit
plumbing moved. **This is the only edit this pass made to a spec's block, and
no box's wording changed.** Worth a sweep: any block on this board ending in a
bare repo gate has the same hole, and it reads green by hand every time.

**`collect` is not wired to `lanes` yet.** A grep for `lanes.` in
`resources/board/collect.py` is empty in the main checkout while `lanes.py`
exists untracked beside it, so the lane this PRD was built in has no automated
path home. Reported for routing, not fixed — it belongs to
`the-machine-frontier-is-dispatched-in-parallel`.

**The PRD body is still the empty template.** `prds/<this prd>/prd.md` holds
the unedited `<The request, for an analyst who knows the codebase but not this
conversation: …>` placeholder. The whole contract lives in `specs/spec01.md`
and in the title. Nothing was lost — the spec is thorough — but the board's own
route says a build against a contract that is "a title and a hope" produces
questions nobody asked for, and this one got away with it only because the
title happened to be a complete sentence stating the defect. Not mine to write
(frontmatter and body are the analyst's), reported so the pattern is seen.

## Knowledge

Nothing was learned outside this repo. No `remember` or `conclude` written.
