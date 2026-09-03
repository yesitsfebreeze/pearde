# no-destructive-git-runs-in-a-tree-the-session-does-not-own — implementer report

Verdict: DONE

Second pass of `probe-then-spec` on this PRD. The analyst built spec01 and
wrote all three specs; this pass reviewed spec01 against the tree, built
spec02 and spec03, and ran every block the way `collect` runs it. Three specs,
25 of 25 acceptance boxes ticked, each against a check that was seen to fail.

The analyst's own report stood at this path and its `## Findings` are carried
forward by name below, per the route's `Fails when` row for a second pass.

## Per spec

| spec | boxes | block, run as `bash -e -o pipefail` | proved able to fail by |
|---|---|---|---|
| spec01 — the refusal | 12/12 | exit 0 from the checkout | `import plan` into `refuse.py`: `refuse.py imports the board: {'plan'}`, exit 1; restored, `cmp` clean, exit 0 |
| spec02 — the manual | 6/6 | exit 0 from the lane | run against the checkout, which does not hold the build: `FAIL: handles.md carries no row for the refuse handle`, exit 1 |
| spec03 — the invariant | 7/7 | exit 0 from the checkout | `RUNNERS = ()` in the invariant's own reader: the self-test fires, exit 1; restored, `cmp` clean, exit 0 |

spec02's is the strongest of the three: the whole block ran on the tree that
does not hold the build and went red at the box's own line, which is the
red-to-green flip the route asks for rather than a `git show HEAD:` argument
about it.

## What was built this pass

| file | what it now does |
|---|---|
| `references/parts/guard.md` | a row in `## What it refuses` for a destructive git aimed at a tree this session does not own — the four commands, the two ownership rules, the board that decides, the spellings that pass, and the memo. The false sentence calling the `Bash` hook "a reader's check" is gone; the point it was carrying — that a `>` or a `tee` into a skill file through a link still passes — is kept |
| `references/parts/handles.md` | a row for `refuse`, both verbs, the exits, and `pearde refuse <verb>` in the Command column |
| `resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh` (new) | reads every `.py` under `resources/` with `ast`, asks `refuse.py`'s own `SPELLINGS` what discards, and fails naming file and line for a destructive git that is neither gated nor exempt |
| `pearde/memos/no-destructive-git-runs-in-a-tree-the-session-does-not-own.md` (new) | the invariant memo, `verify:` naming that script; rests on `a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work` and restates none of it |
| `pearde/memos/README.md` | one added row — the generated kind index, rewritten by `memo add` |
| `specs/spec01.md`, `specs/spec02.md` | their `## Verify and Proof` blocks repaired; see **Blocks that could not fail** |

`references/files.md` and `index.md` already carried the manifest row and the
`@@own` keyword from pass one; both were checked, neither was touched.

## Measurements

Baseline taken before the first edit of this pass, `PEARDE_ROOT` = the lane,
checkout HEAD `64ed54a`, board HEAD `38d5b86`:

```
probe                 probe: green — 29 checks, A1–A10 B1–B6 C1–C4 D1–D5 E1–E2 F1 G1
index.py check        references/language.md references @references/personas/writer.md — not on disk   (exit 1)
memo check            silent (exit 0)
doctor --harnesses    harnesses   broken  3 of 75 green · 63 unpinned · 117s · 51 failed
doctor rows red       index · origin · knowledge · harnesses
```

After, same root, same command line: `3 of 75 green · 63 unpinned · 115s · 51
failed`, and the 51 failing paths `diff` **identical** to the baseline list.
None reddened, none silently fixed.

Run again with `PEARDE_ROOT` = the checkout — the root `collect` uses — the
sweep is `4 of 75 green · 118s · 49 failed`, and the failing set is a strict
subset of the lane's: the two that drop are
`a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re` and
`collect-commits-the-code-repo-not-the-board-repo-twice/list-the-collects-the-repo-bug-orphaned`,
both of which name the worker's own lane in their FAIL line. Measured
directly on the first: with the lane's board symlink in place it prints
`FAIL a stub wiki stands at <lane>/pearde/wiki` and exits 1; with the symlink
removed, `ok no stub wiki under the tree under test`, exit 0. Neither
difference is this unit's, and the count that answers spec01's last box is
the same-root pair, 51 against 51.

`index.py check` is red before and after on the same one line, which names no
file of this PRD's. `memo check` is silent after adding the memo and running
`memo index`.

## Where the work stands, and what the merge needs

The lane was cut at `9a98fae`, four commits behind `main`, and was empty. It
was fast-forwarded to `64ed54a` — a fast-forward of a clean tree with no
commits of its own, so nothing was discarded and no second commit was put
behind this PRD — and this PRD's six uncommitted files were copied in from
the checkout, per the route's step 1 `Fails when` row.

The checkout therefore holds a copy of every footprint file of this PRD, all
of it this PRD's own work and none of it a neighbour's hunk:

```
 M index.md                    M resources/board/lanes.py
 M references/files.md         M resources/guard.py
 M resources/board/collect.py  ?? resources/board/refuse.py
                               ?? resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh
```

`lanes.merge` will refuse the `--ff-only` while those stand. Before the merge
the orchestrator wants, for each of the five tracked paths,
`git -C /Users/feb/dev/infra/pearde checkout -- <path>`, and the two untracked
files removed — the lane's copies are the same bytes and the lane also holds
`references/parts/guard.md` and `references/parts/handles.md`, which the
checkout does not.

The invariant script is in **both** trees deliberately, byte-identical
(`cmp` clean): `memo verify` runs its command with the cwd set to the board's
parent, and on this board the lane reaches the board through a symlink, so
the parent it computes is the checkout and not the lane. Without the
checkout's copy, `pearde memo verify` on this slug answers `BROKEN (exit 127)
— No such file or directory` in the lane and nothing in the tree is wrong.
See **Findings**.

`pearde/memos/*` are board-repo paths and land in the board's own commit, per
`a-board-s-own-file-commits-in-the-board-repo`.

## Blocks that could not fail

Four defects in the two blocks this pass inherited, all found by running them
the way `collect` does rather than by reading them.

1. **spec01 ended on a board-wide gate inside a pipeline.**
   `bash resources/doctor.sh --harnesses "$PEARDE_ROOT" 2>&1 | grep '^  harnesses'`
   — `doctor.sh` exits 1 while any row is broken, and three are, for reasons
   outside this footprint. Under `pipefail` that exit was the block's, so the
   unit could not pass however green it was. Measured:
   `doctor.sh | grep '^  index'` exits 1. Repaired by capturing the gate,
   printing the row and the failing list, and gating only on this PRD's own
   probe.
2. **A slug is not a path.** The first repair gated on the bare PRD slug, and
   the worker's lane directory is named for the slug too — so two neighbours'
   FAIL lines quoting paths inside the lane matched, and the block read as
   this PRD going red. Two matches on the raw sweep for the bare slug, zero
   for the probe's path. Now anchored on the path.
3. **`grep -q X && echo "ok"` cannot fail a block.** `-e` skips every command
   of an AND-OR list but the last, so a missed needle printed nothing and the
   block carried on at exit 0. Four such lines across spec01 and spec02.
   Found by running spec02's block against the checkout, which does not hold
   the build: it printed `handles has the row` on a file with no such row,
   because `grep -q 'refuse'` matched the word "refused" in unrelated prose.
   Every one is now written so the miss is the last command of its list.
4. **A captured exit inverted a check.**
   `python3 resources/index.py check 2>&1 | grep -i 'refuse|@@own' && { FAIL } || { OK }`
   — `index.py check` exits 1 on a pre-existing problem, so under `pipefail`
   the pipeline was 1 whether or not the grep matched, and a match would have
   printed the good news. Captured to a variable first.

## Findings

### Carried forward from the analyst's pass, unfixed

- **A protective stash refused destroys the work the refusal exists to
  protect.** Still the live disagreement with a settled memo, and still a
  person's to decide: whether
  `a-session-that-writes-a-shared-checkout-can-revert-another-session-s-work`
  gains a sentence saying its fourth command means a stash with no pop. The
  code, the comment above `_park`, and now the invariant's exemption all
  behave as if it does — the exemption is spent only while that comment
  stands, and removing the comment reddens the invariant. Measured this pass.
- **`rm -rf <a peer's tree>` is not a git command** and nothing catches it.
- **`git worktree remove --force`** is likewise not one of the four.
- **The shell half only exists where `guard.py on` has been run.**
- **`doctor`'s `index` row is red before and after** —
  `references/language.md` references `@references/personas/writer.md`, not on
  disk. Untouched.
- **`doctor`'s `origin` row is red before and after** — 33 derived, one with
  no `from:`.
- **The parent PRD's own probe fails at baseline** —
  `prds/every-run-session-works-in-a-worktree-of-its-own/probe/verify.sh`,
  exit 10. Still failing, unchanged, and the parent's.
- **`a-harness-measures-the-tree-its-worker-built-in` fails on a count of its
  own siblings** — now `got: 74 · want: 75`. Red before and after.
- **`own` is not in the grammar.** Re-checked this pass:
  `grammar: 'own' is not defined on this board`. Reported, not added.

### New, this pass

- **`doctor`'s `knowledge` row is red before and after** — `graph.json is
  behind the files: 260902-4f91, 260902-aae0`. `260902-4f91` is this PRD's own
  knowledge note from pass one, so the relink this row asks for is owed partly
  to this work; it is a one-command repair (`knowledge.py relink`) that writes
  a file no spec here names, and it is left rather than done. It reddens no
  harness of this PRD's.
- **A lane cannot run a board-rooted gate.** `memos.py verify` sets its cwd to
  `os.path.dirname(board)`, and `board_link` resolves a board reached through
  a symlink to what the link points at — so from a lane whose board is a
  symlink to the real one, the root is the checkout, never the lane. An
  invariant script built in a lane is therefore unreachable from its own
  memo's `verify:` until it lands. Worked around here by keeping the script in
  both trees. The general repair belongs to whoever owns `lanes.create`: a
  lane wants a board it can be the parent of.
- **Scaffolding a board into a lane changes the harness sweep.** The lane
  holds no `pearde/`, so a block spelling `pearde/prds/…` cannot run there at
  all; the obvious fix is a symlink, and the symlink makes
  `a-lane-s-wiki-is-a-stub-…` fail (measured, exit 1 with, exit 0 without) and
  `list-the-collects-the-repo-bug-orphaned` name the lane's git store instead
  of the checkout's. A worker who baselines with the symlink and re-runs
  without it will read two flips it did not earn. Both counts above name the
  root they were taken at, and the symlink is not left behind.
- **spec03's spec text names a site that does not exist.** It says the check
  must accept "`session.py`'s reaper, which uses `stash create`". `session.py`
  spells no stash at all — its docstring says so and it snapshots through
  `write-tree` and `commit-tree`. The check names nothing in `session.py`, so
  the box is met; the sentence is wrong.
- **The stash-then-pop pair is two call sites, not one.** spec03 names three
  accepted sites; the fourth is the `stash pop` in `guarded_run`'s `finally`,
  the other half of `_park`. The invariant exempts both, under the same
  recorded reason.
- **Adding a memo makes `memos/README.md` stale, and no footprint names it.**
  `memo add` rewrites the index itself, so the row lands with the memo; the
  spec's footprint should have carried `pearde/memos/README.md`. One added
  row in `git diff --stat`. The header line that also moved was a sibling's,
  already in the working tree before this pass began.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | read-the-contract | pass, on the second reading — the first read the lane as empty. Both `Fails when` rows for a lane fired: the checkout held the uncommitted build, and `pearde/memos/…` exists under no lane at any depth |
| 2 | capture-the-harness-baseline | pass. The row about a lane behind the checkout fired on `memo check`, red in the lane and green in the checkout, closed by the fast-forward |
| 3 | attempt-the-build | entered. The route's first `Fails when` row — "steps 3 and 5 have nothing to do" — is true of spec01 only; spec02 and spec03 were built here |
| 4 | re-run-the-harnesses | pass, no back-edge. Identical failing set at the same root |
| 5 | write-the-specs | entered for the blocks only. No spec was authored; two had blocks that could not fail and were repaired |

### Edits

Four rows the atomics do not carry, each measured on this run.

**`read-the-contract` → `Fails when`, a new row:**

| the `repo:` root is a lane and a spec's `## Verify and Proof` block spells `pearde/prds/…`, or runs a command that resolves a board | `lanes.create` gives the lane no board, so the block cannot run there and every board-rooted command in it answers about the checkout | symlink the live board in at `<lane>/pearde` (both `/pearde` and `/.pearde` are gitignored) **and read the next row before you baseline anything** |

**`capture-the-harness-baseline` → `Fails when`, a new row:**

| the harness sweep is baselined with a board symlinked into the lane, and re-run without it | the symlink is inside the tree the sweep measures: a harness asserting about `<root>/pearde/…` sees the real board where it expects a lane's stub, and a harness reading the git store sees the lane's | measured here: `a-lane-s-wiki-is-a-stub-…` exits 1 with the symlink and 0 without, and `list-the-collects-the-repo-bug-orphaned` names the lane's `worktrees/-pearde`. Take both baseline and re-run with the scaffolding in the same state, name the state beside every count, and take the deciding count at the root `collect` will use |

**`re-run-the-harnesses` → `Fails when`, a new row:**

| a block gates on the PRD's slug appearing in a sweep's failing lines, and goes red with the PRD's own probe green | the worker's lane directory is named for the slug, so any neighbour's FAIL line quoting a path inside that lane matches | gate on the **path** of the PRD's own probe — `prds/<prd>/probe/verify.sh` — never on the slug. Measured: two matches for the bare slug against zero for the path, on the same sweep output |

**`write-the-specs` → `Fails when`, a new row:**

| a spec contracts a `resources/invariants/*.sh` script and its memo's `verify:`, and `memo verify` answers `BROKEN (exit 127) — No such file or directory` in the lane | `memos.py verify` runs each command with the cwd set to `os.path.dirname(board)`, and `board_link` resolves a board reached through a symlink to what the link points at — so a lane's root is the checkout, and the script the lane holds is not on it | run the invariant directly (`bash resources/invariants/<name>.sh`, which takes its tree from `$PWD`) to prove the rule, and keep a byte-identical copy in the checkout — proved with `cmp` — so the memo's own command resolves. Say both in the report; the copy is one of the paths the merge needs cleared |

## Scores

complexity: 30
blast-radius: high
workflow: probe-then-spec
