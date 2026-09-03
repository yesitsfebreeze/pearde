# report — the machine is the run verb · impl-run-verb · 2026-09-03

Verdict: DONE

One spec, `specs/spec01.md`, sixteen acceptance boxes, all sixteen measured
and ticked. The rename stands as one commit on
`lane/every-task-is-a-verb-under-one-skill-the-machine-is-the-run-verb`
(`60d33f1`, parent `0ed24e1` — today's `main`), nine files, two of them
renames git records as renames. The lane's working tree is clean.

`specs/spec01.md`'s `## Verify and Proof` block, run the way `collect` runs it
(`bash -e -o pipefail -c` over the awk'd fence):

| root | exit |
|---|---|
| the lane, `60d33f1` | **0** |
| the orchestrator's checkout, `0ed24e1` | **1** |
| the lane with one `run.py` constant mutated | **1** |
| the lane, constant restored (`cmp` identical) | **0** |

The checkout row is the red-to-green flip shown against the tree that does not
hold the build — the whole gate ran on the old files, not a `git show HEAD:`
of one predicate. The mutation row is behavioural: `RESERVED` widened to
swallow `definitely-not-a-group`, so the unknown-scope refusal stops refusing.

## What this pass did

The build was pass one's, standing **staged and uncommitted** in the lane at
`1880990` — four commits behind `main`. Those four commits rewrote three files
in this footprint: `references/parts/machine.md` (the dense rewrite,
`b17c06a`), `resources/board/plan.py` (`31620bb`) and `references/files.md`.
A `collect` on that lane would have hit `lanes.merge`'s rebase and come back
red, and merging it as it stood would have thrown away the sibling's dense
rewrite of `parts/machine.md`.

So the pass was: commit the standing build, rebase it onto `main`, resolve.
Exactly one file conflicted — `references/parts/run.md`. It was resolved by
taking **main's dense `parts/machine.md` as the base** and re-applying the
rename's own edits to it, rather than by keeping the lane's older prose. The
sibling's rewrite survives whole; every rename edit is on top of it. The other
nine files merged clean, `plan.py` included.

Then the prose gate, which the dense rewrite had left at zero on this file:
the grafted rename sentences reintroduced four unbound waste words
(`that is` twice, `There is`, `it is`) in `parts/run.md`. Rewritten to nought.
Across the whole doc footprint the only violation left is
`references/settings.md: 1 unbound waste word (that)` — byte-identical to the
checkout's own baseline, and pre-existing.

## The boxes, and where the spec's numbers moved

Every number in `spec01.md` was taken on 2026-09-02. The board and the machine
have both moved since, so where a box quotes a count the count was re-measured
rather than trusted. The **shape** each box asserts holds in every case.

| box | measured now |
|---|---|
| the two `git mv`s | `git show --stat -M HEAD` records `parts/{machine.md => run.md}` and `board/{machine.py => run.py}`. The spec's `git status --porcelain` `RM` no longer applies: the spec's own *What is left* said commit it, and it is committed |
| `pearde-run.md` + manifest row | `references/files.md:197`; `doctor`'s `skills` row reads `19 well-formed · … pearde-run …`, no `pearde-machine` |
| `@@run` in `index.md` | line 74, naming `pearde-run.md`, `parts/run.md`, `run.py`. `pearde index` is now **0 problems in the checkout** — both anchors the spec called pre-existing were closed by siblings (`writer.md` by `0ed24e1`) — and **1 in the lane**, `parts/commits.md` pointing into `@pearde/memos/…`, which is the lane's missing board by construction and closes on the merge |
| `run` discoverable | `COMMANDS = {"run": cmd_run}` (run.py:788), `argv[0] == "run"` (:864), `pearde help` lists `pearde run   dispatch a board, a group or every watched…`, and `pearde run --help` prints `takes: --dry --once --workers N --adapter <id> --deadline S` |
| the five `run` lines | all five answer from the checkout's cwd. `run --dry` and `run here --dry` identical (`dispatched 0 · refused 6`); `run all --dry` 13 boards, `dispatched 14 · refused 49`; `run private --dry` 4 boards, `dispatched 0 · refused 12`; `run every-task-is-a-verb-under-one-skill --dry` prints `scope …: 3 PRD(s) in that subtree` and only those rows. The counts differ from the spec's because the board moved, not the code |
| dedupe by realpath | `run.py:484-488` |
| `board_at` walks `BOARD_DIRS` | `run.py:100`, with the comment naming the disagreement it closes |
| bare-word resolution | `RESERVED` (:397), `READ_VERBS` (:393), `resolve_scope` (:504). An unknown scope exits **1** and names the groups that exist. Both-a-group-and-a-PRD is covered by `probe/scope.py` |
| the nine `plan` lines | all nine exit 0. `plan private slots` and `plan slots private` print one identical line |
| `--group` gone | `grep -c -- '--group' dispatch.py` is **0**; `def main(argv, entries=None, only=None)` at :326 |
| `machine dispatch` nowhere | the command-shaped grep returns **0** lines |
| `git grep -in machine` | prose about the physical machine only — `machine-ceiling`, `machine-wide`, `machine-local`, `_machine_proc`. Checked file by file across `SKILL.md`, `index.md`, `README.md`, `references/parts/`, `references/skills/` and the board modules |
| `fixture.py` | **13 PASS · 0 FAIL** under `PEARDE_ROOT=<lane>` |
| `probe/scope.py` | **24 ok · 0 failed** against the lane |
| the handles row | `references/parts/handles.md:31` still ends in an em-dash Command cell. The row's prose was rewritten by `b17c06a`; the empty Command cell — the thing that keeps the adapter's `/pearde run {rel}` from resolving to the dispatcher — is intact |
| no regression on the two red gates | `prose.py check` over the doc footprint: only `settings.md: 1`, identical in both roots. `every-artifact-lands-inside-the-board.sh`: **7 pass · 0 fail, exit 0, in both roots** — the two failing checks the spec recorded were closed by siblings, so this gate is now green rather than merely unregressed |

## Findings

**A second writer is working this lane and this PRD, concurrently with me.**
This is the finding that matters. Mid-run, without any action of mine:

- the lane branch's reflog took two `commit (amend)` entries on my commit
  (`922cee1`, `46485dc`) and a `rebase (finish)` onto `0ed24e1`, all between
  09:19 and 09:31;
- one of those amends rewrote a sentence I had just written in
  `references/parts/run.md` and another rewrote three lines of
  `references/skills/pearde-run.md`. Both edits are *better* than mine — the
  first avoids naming a removed flag at all, which is what the PRD's **No
  legacy** rule asks for — so nothing was reverted;
- all sixteen boxes in `specs/spec01.md` were already `[x]` when I went to
  tick them: my ticking script replaced **0** boxes and the file still held
  sixteen.

Everything in this report was re-measured against the tree as it stands after
those writes, so the verdict is mine and not inherited. But two workers on one
PRD is a double-book the board is supposed to prevent, and
`.state/transitions.jsonl` records exactly one `specced → claimed` for this
PRD. **The likely mechanism is the next finding.**

**One tree is registered as two boards, and the merged frontier still
double-counts it.** `plan boards` prints `pearde` at
`/Users/feb/dev/infra/pearde/.pearde` and `pearde-2` at
`/Users/feb/dev/infra/pearde/pearde` — `.pearde` is a symlink to `pearde`, so
both rows are one directory, and both carry `groups: private`. The dedupe this
build added is local to the cwd board (`here_entry`); `run all` and
`run <group>` walk the watch set and take the tree twice, so every dispatchable
PRD on this board can be handed to two workers in one run. The analyst reported
the double registration; this pass is live evidence of its consequence. The fix
is one `pearde view forget` on either spelling, and it is not in this
footprint. It should be done before the next `run all`.

**Three dead fixture boards are in the watch set.** `plan boards` skips `fx1`,
`fx3` and `fx5` with `gone from disk`, all three under a session scratchpad
path. Some probe registered its `mktemp -d` fixture against the live daemon —
the shape `probe-then-spec` step 3 already names. They are not mine (this
PRD's `probe/scope.py` uses `mkdtemp(prefix="run-scope-")` and registers
nothing) and `forget` takes a name, where a mistyped one unwatches a live
board, so they are reported rather than removed.

**The machine ran out of disk mid-pass.** The root volume reached 138 MiB free
and the harness could not write its own tool output; every command failed with
ENOSPC until I deleted my own scratch clone, which alone bought 665 MiB.
Thirty-one lane worktrees and four session worktrees are checked out under
`pearde/.lanes/` and `pearde/.sessions/`. Nothing here reaps them, and a board
that cannot write is a board that cannot report.

**Two grammar gaps.** `pearde grammar show run` and `… plan` already answer in
this PRD's sense — a sibling landed them. But `plan`'s own row uses the word
**window** and `grammar show window` answers `not defined on this board`; and
`scope`, which this PRD makes a command word, is defined here as *"what a
feature is made of, not a reading list"* under **Addressing** — a different
sense entirely. A term used inside another term's definition should be a term,
and one word carrying two board meanings should say which is which. Neither is
in this footprint.

**`pearde-machine` is still an installed skill on this machine.** The skill
listing this session was handed still offers `pearde-machine`, because the
install symlinks the checkout's `references/skills/`, which still holds
`pearde-machine.md` until this lands. `pearde update` after the merge is what
closes it; nothing in the lane can.

**Carried forward from the analyst's pass, still open and not fixed here:**
`references/skills/pearde-run.md` is still a near-duplicate of
`pearde-all.md` (the sibling `the-skills-fold-into-one-index`'s to collapse);
both `probe/machine.py` harnesses under
`the-whole-machine-is-worked-as-one-board` carry their own copy of the frontier
code and cannot go red, which is
`a-harness-measures-the-tree-its-worker-built-in`'s; and `knowledge.py query`
from a lane still fabricates a board directory the board walk then answers
with — this lane holds both a `pearde/` and a `.pearde/` directory of exactly
that kind, each with a `graphify/` and a `.state/` and no `prds/`.

## What the orchestrator must know before collecting

The work is a **commit on the lane branch**, not dirt in the lane. `land_lane`
finds nothing standing to commit and merges the one commit; `lanes.merge`'s
rebase is a no-op because the lane already sits on `0ed24e1`. If `main` moves
again before `collect` runs, the rebase runs for real — the only file likely
to conflict a second time is `references/parts/run.md`, and the resolution rule
is the one used here: main's text is the base, the rename edits go on top.

`SKILL.md` left this PRD's diff between the two rebases: `0ed24e1` landed the
same one-line change, so the hunk became a no-op. Nine files carry the rename
now, not ten.

## Workflow probe-then-spec

Second pass on this route: the specs existed and the build was in the tree, so
steps 3 and 5 were entered as that case's `Fails when` row directs — step 3
only for what was not standing, step 5 not at all (no spec authored; the boxes
were applied to the blocks that already stood).

| # | atomic | verdict |
|---|--------|---------|
| 1 | `read-the-contract` | ok — `prd.md`, its `## History`, `specs/spec01.md`, the previous `report.md`, every anchor resolved |
| 2 | `capture-the-harness-baseline` | ok — `index`, `doctor`, `prose`, the invariant and both probe harnesses taken in **both** roots before the first edit |
| 3 | `attempt-the-build` | ok — the build stood; this pass rebased it onto `main` and closed the one conflict and the four waste words it introduced |
| 4 | `re-run-the-harnesses` | ok — every recorded count re-taken; two gates the spec recorded red are now green through siblings, and that is said rather than claimed |
| 5 | `write-the-specs` | not entered — the spec exists; its boxes were applied and ticked |

### Edits

Two, both for step 2's `Fails when` table.

**A row for the shape this pass actually met.** The table has a row for a lane
whose build is uncommitted with no counts published, and one for a lane cut off
a dirty checkout. It has none for the commonest shape on this board: *the lane
holds a whole build, staged and uncommitted, on a base several commits behind
`main`, and `main` has since rewritten files in the footprint.* Proposed row:

| seen | means | do |
|---|---|---|
| the lane holds the build staged-but-uncommitted, and `git log --oneline HEAD..main` in it is non-empty on a file in the `footprint:` | the lane is a base behind the checkout, so `lanes.merge`'s rebase will conflict at `collect` time and a straight merge would discard whatever `main` landed in those files since | commit what stands in the lane, `git rebase main`, and resolve **with main's text as the base and the PRD's own edits on top** — never the reverse, which silently reverts a sibling's landed work in a file you happen to share. Prove it first if it is large: `git diff --cached --binary` to scratch, `git clone --shared` the checkout, `git apply --3way` the patch, and read which files come back `UU`. Leave the work as a commit; `land_lane` handles a lane with commits and nothing standing |

**A row for a lane another session is also writing.** Step 4's table covers a
sibling landing on `main` under you. It has no row for a peer writing your own
lane branch and your own PRD's spec file. Proposed row:

| seen | means | do |
|---|---|---|
| the lane branch's reflog shows `commit (amend)` or `rebase (finish)` entries you did not make, or the spec's boxes are already `[x]` when you go to tick them | a second worker holds the same PRD — on this board most often because one tree is registered under two names, so the merged frontier hands the row out twice | do not revert and do not race. Re-measure every box against the tree as it stands, say in the report that the verdict is re-taken rather than inherited, and name the peer's edits you kept. Then report the double registration: `plan boards` and `os.path.realpath` on each row is the proof, and one `view forget` is the fix |
