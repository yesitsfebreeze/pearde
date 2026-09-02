# one copy per machine of what every lane regenerates — implementer report

Verdict: DONE

Worker: impl-shared-copy · persona engineer · workflow `probe-then-spec`
(second pass — the analyst's SPECCED report is carried forward below under
`## Findings carried from the analyst pass`)
Lane: `/Users/feb/dev/infra/pearde/pearde/.lanes/one-copy-per-machine-of-what-every-lane-regenerates`
Lane HEAD at claim: `7d65ef2`. The orchestrator's checkout moved `318fbda` →
`344d09d` during the run, siblings committing; its tree is clean.

## Boxes

| spec | boxes | block exit | what landed |
|---|---|---|---|
| spec01 | 4/4 | 0 | `main_worktree`, `find_checkout`, `offers`, `root_of`; `trees()` filtered |
| spec02 | 5/5 | 0 | `refusal()`, `reachable()`, the `refused` state, the `WORDS` summary |
| spec03 | 4/4 | 0 | `Share.key`, `CACHE_KEY`, `RETIRED`, `retire()`, the `stale` state |
| spec04 | 4/4 | 0 | the `@@share` row in `index.md` |
| spec05 | 5/5 | 0 | the invariant script and its `references/files.md` row |

22 of 22 acceptance boxes ticked, each against a command that was run.

## Numbers

Before the first edit, in the lane, `PEARDE_ROOT=<lane>`:

```
python3 resources/index.py check            5 lines, exit 1
  references/skills/pearde-machine.md is on disk with no row in references/files.md
  @@share names @pearde/memos/lanes-share-one-copy-of-what-they-regenerate.md — not on disk
  index.md references @pearde/memos/lanes-share-one-copy-of-what-they-regenerate.md — not on disk
  references/language.md references @references/personas/writer.md — not on disk
  resources/board/edit.py references @questions.py — not on disk
pearde share                                278 rows, 31 trees
  Counter({'linked': 241, 'store-only': 37})
  checkout in the survey: False   ·   label `checkout` on the board worktree
  232 shared · 0 not yet · 0 refused (git tracks them) · 0 someone else's link
store                                       45 MB
  pearde/graphify/cache   24 MB, 614 entries
  .pearde/graphify/cache  2.6 MB, 157 entries, 3 of them unique to it
```

After:

```
python3 resources/index.py check            3 lines, exit 1
  (the two @@share lines are gone. The other three were red before the first
   edit and belong to no spec here — two of them a sibling has since closed in
   the checkout at ac73576)
pearde share                                269 rows, 33 trees
  243 shared · 0 not yet · 25 refused (git would show the link) ·
  0 refused (git tracks them) · 0 linked to a retired store path ·
  0 someone else's link · 1 in the store only · 0 not here
  = 269 of 269 row(s) surveyed
  checkout in the survey: True    ·   label `checkout` on the code checkout
  board worktree surveyed: False
store                                       44 MB, one graphify cache, 640 entries
sh resources/invariants/one-copy-…-regenerates.sh    4 PASS, 0 failed, exit 0
```

The row count fell from 278 to 269 while the tree count rose from 31 to 33 —
two lanes landed mid-run, the board worktree left the set, and `targets()` now
drops the second board spelling wherever both resolve to one store copy, which
is nine rows.

## What each spec changed

**spec01 — the checkout is a tree `share` visits.** `cmd_share` resolved the
repo with `find_repo`, which answers the worktree the path is IN; the board is
a linked worktree of this same repo on its own branch, so from the board and
from every lane it answered the board — a tree holding no `resources/board/` at
all. `find_checkout` reads the main worktree off `git worktree list
--porcelain` instead, and `offers()` drops any tree that holds none of the
patterns. Proved from all three cwds:

```
cwd=<checkout>  checkout in trees: True | label: checkout | board surveyed: False | trees: 32
cwd=<board>     checkout in trees: True | label: checkout | board surveyed: False | trees: 32
cwd=<lane>      checkout in trees: True | label: checkout | board surveyed: False | trees: 32
--repo <checkout> run from the board:    label checkout | trees: 32
--repo <board>    run from the checkout: the board is dropped, 31 lanes still surveyed
```

`offers()` keys on `resources/board/plan.py`, not on `shared.py`: 21 of the 31
lanes were cut before this module landed and still regenerate a `node_modules`
and a graphify cache worth sharing. `shared.py` stays what the label `checkout`
means, in `is_checkout`.

**spec02 — status says what apply would refuse.** `state()` now answers
`refused` without writing a link. `refusal()` asks `git check-ignore -v` twice,
because `check-ignore` answers about the path as it finds it on disk: a real
directory is answered as one, so a match is read for the trailing slash that
makes a pattern directory-only; a path that is not there is answered as a file,
which is what a link is, so a miss is put again with the slash written on.

I widened box 1 beyond its letter and say so plainly. The box names the
trailing-slash case; `refusal()` also refuses a path that **no** `.gitignore`
row ignores at all, because `apply` refuses that one too — measured: four
`pearde/graphify/cache` rows in old lanes that `state()` still called
`store-only` after the slash-only fix, while `apply` printed `refused` for them.
The spec's own title, "a tree that cannot be shared says so before apply is
run", is the reason. Both refusals carry the pattern, or its absence, into the
hint:

```
refused  resources/board/node_modules
         `resources/board/node_modules/` ignores a directory and a symlink is not
         one — git would show the link — add `resources/board/node_modules` to
         .gitignore, with no trailing slash, and run `pearde share apply` again
refused  pearde/graphify/cache
         no .gitignore row here ignores it — git would show the link — …
```

The summary is built from the `WORDS` tuple and nothing else, so it cannot omit
a state: it prints `= 269 of 269 row(s) surveyed`, and a state added without a
word in that tuple makes the two numbers differ and prints `unaccounted state`.
A tree already `linked` returns before any of this is asked — in the first tree
that reports a refusal, its other seven rows are still `linked`.

**spec03 — one store path per shared object.** `Share` grew a `key`; both board
spellings carry `key=CACHE_KEY`. `RETIRED` names the store path that is retired
and `retire()` folds it into the survivor at the head of every `apply`. A tree
still linked at the old key is `stale`, not `foreign`, and is re-linked in the
same pass — without that, 30 trees would have been left pointing at a path the
fold had just removed. Measured:

```
retired   store/.pearde/graphify/cache — folded into pearde/graphify/cache — 3 entry(ies) kept
store 45 MB → 43 MB, one cache, 614 + 3 = 617 entries, none lost
```

Then a behavioural mutation rather than a string one: I planted a second store
cache holding one entry the survivor did not have and ran `apply` again —
`folded into pearde/graphify/cache — 1 entry(ies) kept`, 617 → 618 entries, the
planted entry present at the surviving key. Removed afterwards.

Box 4 needed a fixture, since every tree on this machine holds both spellings.
Two git repos built at run time, one with only `pearde/` and one with only
`.pearde/`: each seeds, each link resolves to `<store>/pearde/graphify/cache`,
the entry survives, `git status` stays clean of it, and **neither invents the
other spelling** — which it did before I extended `link_one`'s "no such tree
here" guard from the `absent` branch to every state, in `reachable()`. Without
that, `only-pearde` grew a `.pearde/` directory to hang a link in.

**spec04 — the handle.** `@@share`'s third file is now
`@resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh`.
The memo is untouched: `git status --porcelain` in the board names it not at
all. The two `@@share` lines are gone from `index.py check` in the lane; the
checkout never had them, because the board sits beside it there.

**spec05 — the check.**
`resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh`,
four claims, read off `share --json`:

```
PASS  33 tree(s) point at one store: /Users/feb/dev/infra/pearde/.git/pearde-shared
PASS  0 path(s) hold a real copy, none in two trees at once
PASS  243 link(s), none of them visible to git status
PASS  6 shared row(s) reach 5 store path(s), none of them retired
0 claim(s) failed
```

`SHARE_JSON` replaces the survey with a file, which is how each claim is proved
able to fail rather than asserted to be. All four fire, each naming the tree and
the path:

```
FAIL  x is a real copy in 2 trees at once: <D>/a, <D>/b
FAIL  <D>/r: git shows the link at y — `?? y`
FAIL  <D>/r points at <D>/r/.git/pearde-shared, not at <D>/r/store
FAIL  the store holds .pearde/graphify/cache beside pearde/graphify/cache — one object, two copies
```

## Two spec blocks were repaired, and neither rule moved

Both spec04's and spec05's blocks ended on a bare `python3 resources/index.py
check`. That command reads the whole manifest, so under `bash -e` its exit is
the block's and the unit's pass was conditional on every other PRD on the
board — the shape `references/workflow.md` names. Three of its lines are red for
reasons outside both footprints, so both blocks would have failed for somebody
else's file. Each now captures the output, prints it, refuses a crashed producer
by exit code, and fails only on lines naming its own footprint. No box changed.

spec05's block also gained the two fixture surveys above, because `sh <script>`
alone is a check that cannot fail: it is green whenever the machine happens to
be tidy. Proof they can now fail: with the script deleted the block exits 127;
with a board path put back into `index.md`, spec04's block exits non-zero on its
own assertion. Both footprint files were copied to a scratch directory outside
the repo, mutated, restored, and the restore proved with `cmp`.

## How the blocks were run

`collect` runs a block from the orchestrator's checkout. Every block here begins
`cd "$(git rev-parse --show-toplevel)"` and then calls `resources/pearde.py` —
which, run from the checkout, is the **checkout's** module and not the lane's;
and spec01's block cannot pass from a lane at all, because from a lane the cwd
is a lane and its label is a slug. So each block was run twice:

- verbatim from the checkout, against the pre-merge module. spec01 and spec02
  both fail there, and that failure is the red-to-green flip shown against a
  tree that does not hold the build:
  `AssertionError: checkout /Users/feb/dev/infra/pearde is surveyed by nothing`
  and `AssertionError: no tree reports refused, states seen: {'store-only': 32,
  'linked': 225, 'foreign': 4}`;
- from the checkout with `resources/pearde.py` substituted for the lane's copy,
  under `bash -e -o pipefail -c "$(awk …)"` — the flags at `collect.py:1242`.
  spec01, spec02 and spec03 exit 0. spec04 and spec05 read only files and were
  run the same way from the lane: exit 0.

The blocks are left exactly as `collect` will run them. No block names the lane.

## Harnesses

Twelve board harnesses name `shared.py`, `references/files.md` or `index.py
check`. All twelve were baselined before the first edit with
`PEARDE_ROOT=<lane>` and re-run identically. **No count dropped.** One rose:
`every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense`
went 13 PASS / 1 FAIL to 14 PASS / 0 FAIL. That harness names `PEARDE_ROOT`
nowhere, so both runs measured the orchestrator's checkout, and the flip is the
sibling commit that landed there mid-run — not mine.

`collect-stages-a-shared-file-whole` was red before the first edit at 25 PASS /
7 FAIL and is red on the same count after. It names a fixture file of its own
called `shared.py`, not this module.

`bash resources/doctor.sh` in the lane: `index broken 3`, `origin broken 1`,
`memos broken 38`, `workflows broken 25`, `knowledge broken`. Not one row names
`resources/board/shared.py`, `index.md`, `references/files.md` or the new
invariant script. The `memos` and `workflows` rows are a `tags:` key on every
file, board-wide.

## Findings

- **The board worktree still holds the dirt the old code left there.**
  `<board>/pearde/graphify/cache`, `<board>/.pearde/graphify/cache` and
  `<board>/resources/board/obsidian/plugins/` are links and empty directories
  `share` created while it took the board for the checkout. `git status` in the
  board does not show them — they are ignored — and after spec01 nothing will
  create them again, but nothing removes them either. One line clears it, and it
  is outside this footprint:
  `rm -rf <board>/pearde <board>/.pearde <board>/resources`.
- **21 lanes cannot share `resources/board/node_modules` and 4 cannot share
  `pearde/graphify/cache`.** Their branches carry the old `.gitignore`, so the
  fix is theirs to merge and not mine to write into their trees. `pearde share`
  now names every one of them with the row to add, which is the whole of spec02.
- Carried from the analyst pass, unfixed: `find_board_soft(<an explicit path>)`
  handed a lane's path returns `<lane>/references` as a board. That is
  `find_board`'s handling of an explicit argument, in `plan.py`, outside this
  footprint.
- `python3 resources/index.py check` is red in the lane on three rows that
  predate this PRD. Two are closed in the checkout by the sibling commit
  `ac73576` and will close on the merge; the third,
  `references/language.md references @references/personas/writer.md`, is red in
  the checkout too and belongs to no spec here.

## Findings carried from the analyst pass

The analyst's five measurements each became a spec and each is now closed. Its
"What is not a defect" ruling stands and I did not touch it: `pearde/graphify/`
output, `pearde/health/`, `pearde/.state/` and `pearde/wiki/` stay per-tree and
unshared by design, 5.7 MB across the lanes that is not duplication. Its
knowledge-base gap is still enqueued at `.pearde/wiki/pending/260902-b93a.md`.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | read-the-contract | done — `prd.md`'s body is the untouched template, so the contract is the five specs and the analyst's report; footprint resolved in the lane, `git status` recorded in lane and checkout before the first edit |
| 2 | capture-the-harness-baseline | done — 12 harnesses and `index.py check` in both roots, every output under a run-named scratch subdirectory; `doctor.sh` taken after, and no row names a footprint path |
| 3 | attempt-the-build | done — all five units built **in place** in the footprint files, not under `probe/`: each is an edit to an existing function, or a new file the spec's footprint names |
| 4 | re-run-the-harnesses | done — no count dropped, one rose and is a sibling's |
| 5 | write-the-specs | not entered as authoring — the specs stood; its `Fails when` table was applied to the blocks and two were repaired, above |

Back-edges taken: none.

### Edits

Two failures the atomics caused, with the replacement text.

**1. `capture-the-harness-baseline`, step 1.** It says, flatly:

> Every board harness takes its root from `PEARDE_ROOT` and falls back to the
> board's own repo

Measured: of the twelve harnesses in my set, eleven honour `PEARDE_ROOT` and one
— `every-document-is-written-in-the-writer-s-prose/skills-and-scout-docs-are-rewritten-dense/probe/verify.sh`
— names it nowhere. A worker who believes the sentence records that harness's
count as the lane's and reads a sibling's landing as its own flip, which is
exactly what happened here. Replace the sentence with:

> Most board harnesses take their root from `PEARDE_ROOT` and fall back to the
> board's own repo, which is always the orchestrator's checkout — so a worker
> building in a lane runs `PEARDE_ROOT=<lane> bash resources/doctor.sh
> --harnesses <board>`, or exports `PEARDE_ROOT=<lane>` before running one by
> hand. Not all of them do. `grep -L PEARDE_ROOT $(find <board>/prds -name
> verify.sh)` names the ones that do not, and every count from those is the
> checkout's however you invoke them — record them as measuring another tree,
> and never claim a flip on one.

**2. `write-the-specs`, step 4, the paragraph beginning "Run the block from the
root `collect` will run it from".** It tells you to substitute your own root and
leave the block as written, but not what to substitute. On this board the
substitution is not the root: a block that begins `cd "$(git rev-parse
--show-toplevel)"` and then runs `python3 resources/pearde.py …` runs the
**checkout's** module when you run it from the checkout, so it reads green on
code that is not yours and red on code that is. Append to that paragraph:

> Where the block invokes the tool by a path relative to the root — `python3
> resources/<mod>.py` — running it from the checkout runs the checkout's copy,
> not your lane's, and the exit says nothing about your build. Substitute the
> module path, not the root: run from the checkout with
> `s#resources/<mod>.py#<lane>/resources/<mod>.py#`, and run the block verbatim
> as well. Verbatim it must FAIL before the merge — that failure is the
> red-to-green flip shown against the tree that does not hold the build, and it
> is stronger evidence than `git show HEAD:`, because the whole gate ran on the
> old file.

## Files

- `resources/board/shared.py` — modified in the lane (specs 01, 02, 03)
- `index.md` — modified in the lane (spec04)
- `references/files.md` — one row added in the lane (spec05)
- `resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh`
  — new, untracked in the lane (spec05); `collect` stages the footprint, so it
  lands
- `prds/one-copy-per-machine-of-what-every-lane-regenerates/probe/probe_share.py`
  — probe 1 now prints `find_repo` and `find_checkout` side by side. It read
  `MISSES the checkout` against the finished fix because it called the defective
  resolution directly; it now reads `ok`.

`git status --short` in the lane at the end:

```
 M index.md
 M references/files.md
 M resources/board/shared.py
?? resources/invariants/one-copy-per-machine-of-what-every-lane-regenerates.sh
```

The checkout's own tree is clean and holds no hunk of mine.

## Health

The brief listed no footprint file under the health floor. `doctor`'s `health`
row reads `158 files · 6 under 40` and names none of mine.
