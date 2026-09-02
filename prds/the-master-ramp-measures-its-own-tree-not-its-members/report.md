# the-master-ramp-measures-its-own-tree-not-its-members — implementer pass

Verdict: DONE

17 of 18 spec boxes ticked (spec01 8/8, spec02 8/9) and prd.md 5/5. The one
open box asks for a repo-wide gate that is red on two files this PRD does not
own — quoted below against a baseline taken before the first edit.

Headline: `ramp need` on `/Users/feb/dev/infra/.pearde` now prints
`rust 15245  mitosys 14769, model 353, realm 99, shared 23, infra 1` where it
printed `rust 1  *.rs×1`. The five plain boards on this machine print
byte-identical output to the committed `ramp.py`.

## Where the work landed — read this before merging

The brief named the **lane** `.pearde/.lanes/the-master-ramp-measures-its-own-tree-not-its-members`
as `repo:`. That worktree was cut off `HEAD` (59fb13a) and therefore did
**not** hold the probe's uncommitted code the implementer block promises — it
held the committed `ramp.py`, and `git status --short` in it was empty. Pass
1's build was uncommitted in the orchestrator's checkout
`/Users/feb/dev/infra/pearde`. I carried it into the lane (`git diff --
resources/board/ramp.py` there is entirely this PRD's — `scan_roots`,
`_words_of`, `_measure`, unioning `needs`, nothing else) and continued it
there, which is what "continue it, it is pass one" means once the lane exists.

**The merge will refuse unless the orchestrator clears the duplicate.** The
checkout's working `resources/board/ramp.py` is now a strict subset of the
lane's, and `git merge lane/…` will not overwrite a locally-modified file:

```
git -C /Users/feb/dev/infra/pearde checkout -- resources/board/ramp.py
```

That discards a copy of what the lane already carries and nothing else. The
same shape is possible on `references/files.md`, which the concurrent
`lanes.py` PRD also has modified in the checkout — my hunk there is one added
row far from theirs, so it merges once the local modification is committed or
stashed; it is not a duplicate and must **not** be checked out away.

Board files (outside the lane, in `/Users/feb/dev/infra/pearde/.pearde`):
`memos/a-master-need-is-the-union-of-its-members.md`, `memos/README.md`
(regenerated), `prd.md`, `specs/spec01.md`, `specs/spec02.md`,
`probe/compare.sh`. spec02's footprint spans both roots by construction, so
`git status --short` was recorded in both before the first edit.

## Boxes, and the check behind each

### prd.md — 5 of 5

| box | how it was closed |
|---|---|
| `needs()` unions each member's `tracked` and `manifest_text` | `ramp need` on the master, 15245 = 14769+353+99+23+1; the invariant asserts the same sum on repos built at run time (43 = 30+12+1) |
| `board_words()` unions each member's titles | invariant rows 13–14: a member's PRD title reaches the master's union, and the master's own stays in it |
| `need` / `gap` / `ramp` add up to the union, and a master's row credits members | `ramp need` and `ramp gap` on the master both print the credited rows; the gate's own two print paths are `gap()` and `write_ask()`, and both are measured. I did **not** run `pearde ramp` against the real master: `cmd_gate` writes `ask.md` into that board's `.state/` and calls the scout routes |
| a plain board's numbers are unchanged | `probe/compare.sh` against a `git archive HEAD` export: `same` on mitosys, model, realm, shared and pearde; `MOVED` on `/Users/feb/dev/infra/.pearde` alone |
| the master's `ramp need` reports rust in the thousands | `rust 15245` |

### spec01 — 8 of 8

Two edges were left by pass 1 and both are closed.

**`write_ask` names the member.** `ask_subject(job, why, parts)` is new and is
the whole sentence's subject. Measured on a fixture master built under
`mktemp -d`:

```
master: a 30, b 12, top 1 ask for rust, and no installed skill mentions it.
plain : The tree asks for rust (*.rs×30), and no installed skill mentions it.
```

It caps the subject at the three loudest and appends `and N more members`, so
the real master reads `mitosys 14,769, model 353, realm 99 and 2 more members
ask for rust`. `contributors(board)` was factored out of `needs` (both now
read one `_union(board)`) so the sentence gets the `[(member, hits)]` split
back rather than re-parsing the `why` string to guess where a name ends.

**`board_words`'s docstring** now says it is the public union accessor, that
`_measure` reaches for `_words_of` because `needs` sums one board at a time to
keep the credit, and that deleting it as a leftover takes a contract item with
it. Two invariant rows call it, so it is no longer only prose that protects it.

The other six were carried by pass 1's build and re-measured here, not
inherited on trust: the invariant re-derives the sum, the depth, the cycle and
the floor on repos it builds itself.

### spec02 — 8 of 9

`resources/invariants/a-master-need-is-the-union-of-its-members.sh` — 17
assertions, all PASS on the built tree, exit 0. Against a `git archive HEAD`
export (`RAMP=$D/resources/board/ramp.py`) it prints **12 FAIL and exits 1**,
and the three rows that stay green are exactly the plain-board rows, which is
the shape of a real regression rather than a broken check:

```
PASS  a plain board counts its own tree: 30 (got 30)
PASS  a plain board's why is the marker list, not a member credit (got  *.rs×30)
FAIL  the master sums 30+12+its own 1 = 43 (got 1)
FAIL  a master under a master reaches the grandchildren: 43 (got none)
FAIL  a members cycle terminates and counts each repo once: 8 (got 4)
FAIL  board_words unions a member's PRD titles (got - OWN)
FAIL  the fork subject could not be read (exit 1): AttributeError: … 'ask_subject'
12 check(s) failed — the invariant is broken.
```

That is a **behavioural** mutation, not a string one: the whole module is
swapped for the pre-union one and the arithmetic moves.

**One check in it was green for the wrong reason and was repaired before the
box was ticked.** `a master's fork does not say "The tree"` passed against the
old module — because the old module has no `ask_subject`, the producer printed
a traceback, and a traceback contains no such words. The producer is now
guarded on its exit code and on printing the two `SUBJECT ` lines it owes;
when it dies, all three fork rows FAIL and say so. Without that guard the
check would have read green on the exact regression it exists for.

It writes nothing under `.pearde/`: the board's file list is byte-identical
across a run (`comm -13` on `find` before/after, empty), every fixture is a
`mktemp -d` removed by `trap … EXIT` (temp-dir count unchanged across a run),
and every command that could hang goes through `bounded() { perl -e 'alarm
shift; exec @ARGV' "$@"; }` — this machine ships no `timeout(1)` and no
`gtimeout`.

The memo is `kind: invariant` with `verify:` naming the script;
`python3 resources/memos.py check` exits 0. `references/parts/ramp.md` gained
the master section and a third column on the three-lists table, and its `have`
row now says plainly that `have` is one machine and one project directory on a
master as on a plain board — so `gap` on a master is a union `need` against a
single machine's `have`, named as deliberate rather than left to be inferred
as symmetry. `references/files.md` gained one row and nothing else
(`git diff --stat`: 1 insertion), no reflow.

**The open box:** `- [ ] python3 resources/index.py check is silent`. It is
not, and no line names a footprint path. Baseline, taken before the first edit:

| root | before the first edit | after |
|---|---|---|
| checkout `/Users/feb/dev/infra/pearde` | `resources/board/lanes.py is on disk with no row in references/files.md` | identical, byte for byte |
| lane (cut off HEAD) | `references/skills/pearde-all.md is on disk with no row in references/files.md` and `resources/board/edit.py references @questions.py — not on disk` | identical |

All three lines are the concurrent `lanes.py` / `pearde-all` PRD's, two of
them already fixed in the checkout's uncommitted `references/files.md` and
`index.md` — which the lane, cut off HEAD, does not carry. I did not add their
rows: doing so in the lane would duplicate a hunk the checkout already holds.
The box closes on the merged tree once that PRD lands.

**One thing the box's own check does not back.** Removing my new
`references/files.md` row and re-running `index.py check` produces **no new
line** — the directory row `@resources/invariants/` already covers everything
beneath it (per the `a-manifest-row-can-name-a-directory` memo). So the row is
correct and required by the spec's words, but `index.py check` is not the
counter behind it; the evidence for that box is the row itself, not the gate.
The mutation was made and restored, and the restore proved with `cmp`
(identical).

## Harnesses

| harness | baseline (before the first edit) | after | whose |
|---|---|---|---|
| `index.py check` (checkout) | rc 1, 1 line: `lanes.py …` | rc 1, same line, `diff` identical | not mine |
| `memos.py check` (checkout) | rc 0 | rc 0 | mine held it green — see below |
| `resources/invariants/every-artifact-lands-inside-the-board.sh` | rc 0, 7 PASS | rc 0, 7 PASS, `diff` identical | — |
| `doctor.sh` | rc 1 — `index` broken (the same line), `origin` broken (27 derived, 1 with no `from:`), `knowledge` broken (graph.json behind 6 notes) | unchanged in kind | all three inherited, all named "before the first edit" |
| `prds/the-board-runs-itself/an-example-board/probe/verify.sh` | — | rc 0, `37 checks · 37 pass · 0 fail · 1 skipped` | green |
| `prds/the-round-runs-in-a-window-that-ends/probe/verify.sh` | — | rc 0, `26 checks · 26 pass · 0 fail` | green |
| `prds/workflows-on-the-board/workflow-skill/probe/verify.sh` | — | rc 1, `55 checks · 51 pass · 4 fail` | not mine, proved below |
| `prds/upgrade-leaves-the-memo-index-stale/probe/verify.sh` | — | rc 1, `40 checks · 9 pass · 31 fail` | not mine, proved below |

The last two carry no baseline of mine — a gap in my own step 2, which
baselined the repo gate and the one repo invariant and only then grepped the
59 board harnesses for footprint paths. Both are shown not mine by evidence
rather than by ordering:

- **`workflow-skill`** fails on `the fixture holds seventeen skill files — got
  [18] want [17]`, `doctor counts seventeen well-formed skills`, `after the
  rows: index.py check is silent — got [resources/board/lanes.py …]` and a
  nested `readme-in-three-rings` baseline. An eighteenth skill
  (`pearde-all`) landed at HEAD and `lanes.py` is untracked in the checkout.
  Nothing it reads is in my footprint, and the third row is precisely the
  shape `.pearde/memos/a-harness-that-reads-the-whole-checkout-is-not-a-harness.md`
  describes.
- **`upgrade-leaves-the-memo-index-stale`** builds its fixture from
  `resources/board/example`, not from the live board, so my memo cannot reach
  it — and I proved it rather than argued it: with my memo moved aside and
  `memos/README.md` reverted, it prints the identical `40 checks · 9 pass · 31
  fail · 0 skip`. Both files were restored and the restore proved with `cmp`
  (identical, both). Its failures are structural — `doctor exits 0 on the
  upgraded board — got: 127` is a command not found, and `the copy landed a
  memo — got: 0` is a fixture that copies no memos.

`resources/board/ramp.py` scores 78 on `health.py list`, `references/files.md`
95 — both well over the floor of 40. Nothing in the footprint was under it, as
the brief said.

## Findings — not this PRD's to fix

Carried forward from the analyst pass by name, with what this pass measured.

**`index.py check` is red on another PRD's in-flight file.** Still true and
unchanged: `resources/board/lanes.py is on disk with no row in
references/files.md`. It is the concurrent worker's row to add and their
`references/files.md` modification already exists in the checkout. It is the
sole reason spec02's last box is open.

**`board_words()` is dead code that a box is green on.** *Closed by this
pass.* The docstring now states the contract and says why `needs` calls
`_words_of`, and two invariant assertions call `board_words` directly, so a
pass that deletes it as a leftover reddens a check instead of silently taking
a box.

**`have` has the same wrong-tree fault, on the other axis.** Confirmed and
still open. `skill_dirs()` does `repo_of(board)` and reads only the master's
own project-level `.claude/skills/`, so a master's `gap` is a union `need`
measured against one repo's `have`. Outside this PRD's boxes. I did **not**
leave it implicit: `references/parts/ramp.md` and the memo both now say the
asymmetry is deliberate and name what it costs, so the next reader does not
"tidy" it into a symmetry. Worth its own contract.

**The gate now asks a new question.** Confirmed on this pass's own run:
`ramp gap` on the master prints `GAP go 3 · mitosys 3` and `gap: 1 of 9 jobs
unanswered`, where before the fix it reported `GAP rust`. Eight of nine jobs
are answered by installed skills. Nothing to fix; the user will see a
different fork than the one the PRD was filed over.

**`timeout(1)` is absent on this machine.** Carried forward from the analyst
pass's knowledge note `[[260902-6e16]]` and used: the invariant bounds every
command through `perl -e 'alarm N; exec @ARGV'`. Nothing new was learned
outside this repo on this pass, so `knowledge.py remember` was not called.

New, from this pass:

**A lane worktree does not carry the checkout's uncommitted work, and the
implementer brief promises that it does.** `lanes.create` cuts the branch off
the repo's HEAD. With thirteen paths uncommitted in the orchestrator's
checkout — as there were at dispatch — every lane starts behind them, while
the implementer block says "The tree already holds the probe's uncommitted
code — continue it". A worker that believes the brief concludes the build
vanished. It is a small fix in `lanes.create` (cut off the working tree, or
have `claim` say what the lane does not carry) and it belongs to the
`every-worker-runs-in-its-own-worktree` PRD, not here.

**A spec's `## Verify and Proof` block hard-codes the orchestrator's
checkout.** Both specs open `cd /Users/feb/dev/infra/pearde`, which is correct
for `collect` — it runs the blocks on the merged tree — and wrong for the
worker, whose repo is the lane. I ran both blocks with the lane substituted
for that root and left the blocks as written, because changing them would
break `collect`. Nothing in the spec template tells an author which root the
block runs from, and now there are two.

**Adding a memo reddens a check on a file no footprint names.**
`memos.py check` went red the moment my memo landed — `README.md: the kind
index is stale — run memo index` — because the index by kind is generated. I
ran `python3 resources/memos.py index`, which added exactly one row (`git diff
--stat`: 3 insertions, two of them other workers' rows already present) and
returned the check to rc 0. `memos/README.md` is in no spec's `footprint:`,
and it is not optional: a spec that contracts a memo contracts its index row.

**`floor` has a third meaning on this board.** `grammar.py show floor` returns
two — the billed-window floor and `health-floor` — and neither is the ramp's
`FLOOR` table, the per-job signal count under which a need is not raised. I
used the third throughout this PRD's specs, memo and reference.

**Words I needed that the grammar does not define:** `lane`, `master` (as a
board kind — `member` is defined, its counterpart is not) and `invariant`.
`python3 resources/grammar.py show <word>` answers "is not defined on this
board" for each.

## Workflow probe-then-spec

This was the route's **second** pass — the analyst probed and specced, an
implementer was dispatched on the same route — but not the case step 3's first
`Fails when` row describes: the specs existed and the build did **not** already
stand in the tree the brief named, and spec01 carried two edges nobody had
built. So step 3 was entered for real.

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass, with one shape no row covers — the `repo:` root is a lane that does not hold the build. `git status --short` recorded in the lane, the checkout and the board before the first edit. spec02's footprint spans the checkout and the board; resolved per the row for that |
| 2 | `capture-the-harness-baseline` | pass for the repo gate and the repo invariant, taken before the first edit; **partial** for the board's 59 harnesses — I grepped for footprint paths and baselined the gate first, so two harnesses I later ran have no baseline of mine. Both are shown not mine by evidence above, one by an actual mutate-and-restore |
| 3 | `attempt-the-build` | pass. `ask_subject`, `contributors`, `_union` and the docstring are **edits to existing footprint files**, built in place, not staged under `probe/` — a sentence and a docstring have no meaning outside the function they live in. The new invariant script is a footprint file of spec02, so it was written where it lives |
| 4 | `re-run-the-harnesses` | pass. `index.py check` and `every-artifact…` are `diff`-identical to their baselines; `memos.py check` is rc 0 on both sides because the index was regenerated. No back-edge taken |
| 5 | `write-the-specs` | not entered as authoring — the specs exist. Its `Fails when` table was applied to the blocks that stand: the previous report's `## Findings` are carried forward by name, and the can-it-fail proof was run with the file restored by `cp` from a scratch dir outside the repo and proved with `cmp` |

### Edits

Four replacement rows. Never edited the workflow files.

**1 — `read-the-contract`, add to `## Fails when`:**

| seen | means | do |
|------|-------|----|
| the `repo:` root is a worktree under `<board>/.lanes/`, `git status --short` in it is empty, and the brief says the probe's uncommitted code is already there | `lanes.create` cuts the lane off the code repo's **HEAD**, so it carries nothing the orchestrator's checkout has not committed — and with a dirty checkout that is every uncommitted pass before yours, your own included | `git -C <checkout> status --short` and `git -C <checkout> diff -- <each footprint path>`. Read the hunks: where they are entirely this PRD's, copy those files into the lane and continue there, and say in the report that the merge will refuse until the orchestrator runs `git -C <checkout> checkout -- <path>` on each file whose lane copy is a strict superset. Where a hunk is a neighbour's, leave it in the checkout and do not carry it |

**2 — `re-run-the-harnesses`, add to `## Fails when`:**

| seen | means | do |
|------|-------|----|
| a repo-wide gate is red in the lane on lines the orchestrator's checkout does not print | the lane is behind the checkout's uncommitted work, so a fix that landed there is missing here — the mirror image of an inherited red | baseline the gate in **both** roots before the first edit and quote both in the report. A line present in the lane and absent in the checkout closes on the merge; a line present in both is a live finding. Never add a neighbour's missing row in the lane to silence it — the checkout already holds that hunk and you would duplicate it into the merge |

**3 — `write-the-specs`, add to `## Fails when`:**

| seen | means | do |
|------|-------|----|
| a spec contracts a file under `.pearde/memos/` and `memos.py check` goes red the moment it lands | the index by kind is generated, and adding a memo makes `memos/README.md` stale — a file no footprint names and that the spec cannot omit | run `python3 resources/memos.py index <board>` and check `git diff --stat` names one added row; the index is part of adding a memo, not a separate edit. Say so in the report, because the footprint is wrong and the next author of a memo spec should carry the index row in it |

**4 — `write-the-specs`, replace the fourth `Do` item's closing sentence** —
it tells you to run the block `the way collect runs it`, and says nothing about
*where*:

> Run the block from the root `collect` will run it from — the orchestrator's
> checkout, not your lane — and where the block hard-codes that path, run it
> once with your own root substituted and leave the block as written. A block
> rewritten to name the lane passes for you and fails for `collect`.
