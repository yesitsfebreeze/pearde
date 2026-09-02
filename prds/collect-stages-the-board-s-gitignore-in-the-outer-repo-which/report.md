# collect stages the board's gitignore in the outer repo which ignores it

Verdict: DONE

Pass two of `probe-then-spec`, as the implementer. The specs and spec01's
build came from pass one; spec02 and spec03 were unbuilt and are built here.
All 13 acceptance boxes across the three specs are closed, each against a
command that was run and, for every spec, a `## Verify and Proof` block that
was watched exiting non-zero with a footprint file mutated.

## Where the contract was read from

`prd.md`'s body is the unedited angle-bracketed template — the PRD was filed
from a finding, not written. The contract is `specs/spec01.md`,
`specs/spec02.md`, `specs/spec03.md` and pass one's `report.md`, all of which
this pass read. No fork was asked back on that account.

## Per-spec box status

| spec | boxes | closed | how |
|---|---|---|---|
| spec01 — a footprint path is filed under the repo that holds it | 4 | 4 | pass one's build in the lane, re-measured here |
| spec02 — the routing gets a committed guard | 5 | 5 | built here: invariant, memo, manifest row |
| spec03 — the reference says which repo a footprint path commits in | 4 | 4 | built here: the paragraph in `commits.md` |

### spec01 — nothing rebuilt, everything re-measured

Per the route's own `Fails when` row for a second pass, step 3 authored no new
code for this spec and claims no red-to-green flip: the flip was earned by the
pass that built it. What stands, uncommitted in the lane, is one file —
`resources/board/collect.py` — with `foot_root` and its three call sites.

```
$ grep -c 'foot_root(' resources/board/collect.py
4
```

One definition at line 476 and exactly three calls — `owned_by` at 540,
`sort_paths` at 1518, `land_lane` at 1759. No fourth spelling.

```
$ python3 probe/fixture.py --check
PASS both layouts: the board's own file is committed in the board repo, the flat layout is unchanged
$ python3 probe/fixture.py --mutant
PASS mutant: the check goes red when foot_root routes nothing
```

Both run against the lane (`PEARDE_SRC=<lane>`) and again on the merged tree
described below. `--check` covers boxes 2 and 4 (nested exits 0, the board repo
carries a commit holding `.gitignore`, the board's tree is clean after; flat
unchanged) and `--mutant` covers box 3 — the check is watched failing on the
original error text, not assumed able to.

### spec02 — the invariant, the memo, the manifest row

`resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh` is new,
ported from `probe/fixture.py` into the shape of
`a-master-need-is-the-union-of-its-members.sh`: a `no()` counter, one `PASS` or
`FAIL` line per assertion, exit 1 on any. Twelve assertions, all green:

```
PASS  the lane does not hold the board own file — it is cut without the board
PASS  nested: collect exits 0 (got 0)
PASS  nested: no run hits `fatal: pathspec … did not match any files`
PASS  nested: a NEW commit in the BOARD repo holds .gitignore
PASS  nested: the board working tree is clean after (got '')
PASS  nested: the code repo commits the code file
PASS  nested: the code repo never stages the board own path
PASS  nested: collect names the board-owned path it dropped from the lane add
PASS  flat: collect exits 0 (got 0)
PASS  flat: the code file lands in the one repo there is
PASS  flat: nothing is rerouted — the two roots are one
PASS  every fixture is under one mktemp -d, removed on exit
```

Pointed at a `collect.py` whose `foot_root` routes nothing — the behaviour
before this PRD — six rows go red and the flat rows stay green, which is the
shape of the real regression:

```
FAIL  nested: collect exits 0 (got 1) — collect: p1: fatal: pathspec 'pearde/.gitignore' did not match any files
FAIL  nested: no run hits `fatal: pathspec … did not match any files`
FAIL  nested: a NEW commit in the BOARD repo holds .gitignore
FAIL  nested: the board working tree is clean after (got ' M .gitignore')
FAIL  nested: the code repo commits the code file
FAIL  nested: collect names the board-owned path it dropped from the lane add
6 check(s) failed — the invariant is broken.
```

`COLLECT=<path>` copies `resources/` to scratch and swaps the file in, because
`collect.py` does `sys.path.insert(0, dirname(__file__))` and imports plan,
edit, transitions, specs and lanes from beside itself — a lone copy of the file
cannot run.

**Two rows in the first draft could not fail, and were repaired before the box
was ticked.** `git log --name-only -3` over the whole history matched the
fixture's *own* base commit, so "a commit in the BOARD repo holds .gitignore"
and "the code repo commits the code file" stayed green under the mutant. Both
now read `"$HEAD0"..HEAD`, recording each repo's HEAD before the run, and both
go red under the mutant. The mutant run above is the proof.

Box 3 — reaches no daemon, leaves nothing behind:

- `PEARDE_PORT=1` is exported for every run inside the script.
- `serve.py status` after the runs lists no board on any temp dir this pass
  made. (It does list several from *other* sessions — see Findings.)
- Both temp dirs printed by the green and mutant runs are gone (`ls`: `No such
  file or directory`).
- `git status --porcelain` in the code repo: 0 lines before and after.
  In the board repo: byte-identical before and after, `diff` empty.

Box 4 — the memo is at `pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`,
`kind: invariant`, `verify:` naming the script, and `python3
resources/memos.py check` exits 0. It is written in the board directory, not
the lane, exactly as the spec says: the lane is cut without the board and has
no `pearde/memos/` to write into.

Box 5 — `references/files.md` carries the row. `python3 resources/index.py
check` prints **1 line** on the merged tree, which is the count in the
orchestrator's checkout before this PRD. No new line.

### spec03 — the rule in prose

One paragraph added to `references/parts/commits.md`, under **One commit per
repo the PRD wrote**, headed **Which repo a footprint path lands in.** It
states that a path resolving inside a board holding a `.git` of its own is
committed in the board repo under its board-relative name, that the code repo
never stages it and why (`fatal: pathspec …`, an add that aborts whole), that
the lane never stages it because `claim` cuts the lane without the board, and
what a spec author should therefore expect. It names `foot_root` and wikilinks
the memo.

```
$ python3 resources/prose.py check references/parts/commits.md
(no output, rc=0)
```

Two waste words the checker caught on the first draft (`that is`, `there is`)
were rewritten, not suppressed.

## The blocks were run the way `collect` runs them

`collect` runs a verify block from the orchestrator's checkout **after** the
lane is merged, so a block run against the lane alone is not the block
`collect` will run. A merged tree was built for this: `git clone --shared` of
the checkout, the lane's four files overlaid, `references/files.md`
reconstructed as a real merge (HEAD's row plus mine, not the lane's stale
copy), and `pearde`/`.pearde` symlinked to the live board.

```
$ bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec01.md)"   → exit 0
$ bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec02.md)"   → exit 0
$ bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec03.md)"   → exit 0
```

And each with one footprint file mutated, restored by `cp` from a scratch dir
outside the repo and proved back with `cmp`:

| spec | mutation | kind | exit |
|---|---|---|---|
| spec01 | `foot_root` neutered in `collect.py` | behavioural — what the tool computes | 1 |
| spec02 | the row removed from `references/files.md` | string — proves the counter is wired | 1 |
| spec02 | `kind: invariant` to `kind: decision` in the memo | string | 1 |
| spec03 | the paragraph removed from `commits.md` | string | 1 |

spec02's block also carries a behavioural arm as a first-class line — the
`COLLECT=` mutant — so its tick does not rest on the string mutations alone.
Every `cmp` after restore was silent.

**One repair to a block, under step 5's `Fails when` table.** spec02's block
read `COLLECT="$D/collect.py" bash "$S" && exit 1`. That is the
`<test> && <action>` shape: the script's *passing* case is a non-zero exit, so
the `&&` list returns non-zero and `set -e` aborts the block on exactly the
result it was written to accept. It is now
`if COLLECT="$D/collect.py" bash "$S"; then rm -rf "$D"; exit 1; fi`, and
`rm -rf "$D"` is reached on both arms. The rule the block asserts did not
move; only the shape that could never pass.

## Harnesses

Baseline taken before the first edit, with `PEARDE_ROOT=<lane>` and
`PEARDE_PORT=1`, each run's whole output saved under a subdirectory named for
this run. Re-run after the build with the same command line and the same
roots. **Every one of the 21 holds its baseline exactly** — same exit code,
same FAIL-line count, same final line. Two rows differ only in the random
`mktemp -d` name printed in their last line.

| harness | before | after |
|---|---|---|
| `a-verify-block-must-not-destroy-the-checkout-it-runs-in` | 24 passed, 0 failed | same |
| `filing-refuses-a-file-it-does-not-hold` | 52 checks · 52 pass · 0 fail | same |
| `nothing-left-open/the-line-tells-the-truth` | rc=1, 41 FAIL | same |
| `collect-stages-a-shared-file-whole` | verify.sh exit 0 | same |
| `collect-must-not-reset-the-checkout-it-did-not-write` | 31 checks · 31 pass · 0 fail | same |
| `resources-are-organised-by-responsibility` | 18 passed, 2 failed | same |
| `the-round-runs-in-a-window-that-ends` | 26 checks · 25 pass · 1 fail | same |
| `the-brief-names-the-verdict-line-collect-requires` | rc=1, 4 FAIL | same |
| `the-verify-guard-parses-git-s-own-output-before-it-trusts-it` | 46 passed, 0 failed | same |
| `workflows-on-the-board/workflow-improve` | 62/71 checks pass | same |
| `workflows-on-the-board/workflow-skill` | 55 checks · 50 pass · 5 fail | same |
| `the-tool-keeps-its-word/collect-keeps-its-word` | 101 checks · 101 pass · 0 fail | same |
| `the-board-runs-itself/collect-is-a-command` | 133 checks · 133 pass · 0 fail | same |
| `every-module-finds-its-siblings-by-one-rule` | rc=1, 20 FAIL | same |
| `the-largest-module-is-cut-by-responsibility` | rc=1, 25 FAIL | same |
| `the-board-runs-itself/an-example-board` | 37 checks · 29 pass · 8 fail · 1 skipped | same |
| `the-board-runs-itself/hunks-land-where-they-came-from` | 47 checks · 47 pass · 0 fail | same |
| `graph-probe-makes-harness-sweep-unaffordable` | 4 checks · 3 pass · 1 fail | same |
| `seven-closed-probes-drifted-red/the-fixtures-meet-the-tool` | rc=1, 11 FAIL | same |
| `the-gate-runs-the-harnesses` | rc=1, 30 FAIL | same |
| `a-harness-measures-the-tree-its-worker-built-in` | verify: 15 pass, 3 fail | same |

**Thirteen of the twenty-one were already red before the first edit**, and
each is recorded failing *before the first edit*. The failing lines name
fixture paths, a missing `pearde_path` module and a `.pearde/settings.md` that
is not written — causes entirely outside this footprint, and none of them
moved. No flip is claimed on any harness in this set; the only green this pass
created is its own new invariant script, whose predicate this pass wrote.

**A harness appeared mid-run.** The census went 72 to 73:
`prds/post-report-crashes-a-collect-between-the-done-write-and-the/probe/verify.sh`,
a sibling picking up pass one's `post_report` finding. It has no baseline here
and is compared to nothing.

Repo gates:

| gate | before | after |
|---|---|---|
| `index.py check`, orchestrator's checkout | 1 line | 1 line |
| `index.py check`, merged tree | — | 1 line |
| `index.py check`, lane | 3 lines | 4 lines — see below |
| `memos.py check`, checkout | rc=0 | rc=0 |
| `prose.py check references/parts/commits.md` | rc=0 | rc=0 |

`bash resources/doctor.sh` exits 1 on this tree before any edit of this pass,
for the reasons pass one recorded. Unchanged, and no spec here uses it.

**The lane's fourth `index.py check` line is structural, not a regression.**
`references/parts/commits.md` wikilinks
`@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`, and a lane is
cut without the board, so the handle cannot resolve there. Two of the lane's
three baseline lines are the same shape, for another PRD's memo. On the merged
tree — the tree `collect` measures — the count is 1, the checkout's pre-PRD
count. Nothing dangles where it is read.

## Tree state, and what has to happen at merge

The lane holds four paths, all uncommitted:

```
 M references/files.md
 M references/parts/commits.md
 M resources/board/collect.py
?? resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh
```

The board holds one new file — the memo — plus its generated index row (see
Findings). The orchestrator's checkout is clean and was clean throughout; this
pass wrote nothing into it.

**The lane is behind the checkout and both touch `references/files.md`.** The
checkout committed `one-copy-per-machine-of-what-every-lane-regenerates.sh`'s
manifest row into the same invariants block while this lane sat at `58c92e6`.
This pass's row is placed **before**
`a-master-need-is-the-union-of-its-members.sh`, so that untouched line sits
between the two adds and the hunks are disjoint; a `-U0` merge cannot fold
them into one two-author hunk. The merged tree built here holds both rows and
reads green.

The checkout's HEAD moved three times during this run (`58c92e6` to `344d09d`
to `1858a35` to `148e009`) and the board's twice. Nothing of this PRD's was
taken by any of them: the lane's diff is intact and the checkout stayed clean.

## Findings — outside this contract, not fixed here

Pass one's findings, carried forward by name with their state now:

**`post_report` crashes every collect on this machine.** Still true, and now
**owned**: `prds/post-report-crashes-a-collect-between-the-done-write-and-the`
appeared on the board during this run with its own probe. Nothing further owed
from here.

**`git add -- <feet>` still fatals on any footprint path the lane does not
hold.** Still open. This PRD removed only the board-owned class; a footprint
naming a file the worker never created in the lane aborts the same add the
same way. A wider contract, unclaimed.

**Two guards in `sort_paths` are no-ops on a board that is its own repo.**
Still open, unchanged. `board_rel = os.path.relpath(board, board_root)` is
`"."` there and `inside(path, ["."])` is never true, so `scratch()` filters
nothing and the clause letting the board's own dirt ride the commit never
fires. Both read as active.

**Sibling contention is never checked in the board repo.** Still open,
unchanged. `sort_paths` builds `others` only for paths under `repo`, so two
PRDs sharing a footprint path under the board are not detected as contending.
Recorded again in the memo's Consequences so it is not lost with this report.

**Knowledge gap.** Unchanged: the lane's wiki is a stub, which is
`a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re`'s contract.
Nothing this pass learned came from outside this repo, so nothing was written
back with `knowledge.py remember`.

**Grammar.** No word in the contract needed a lookup `grammar.py show` could
not answer.

New from this pass:

**The footprint of a memo-writing spec is wrong, structurally.**
`pearde/memos/README.md` is a generated kind index, and adding a memo makes it
stale — `memos.py check` printed `README.md: the kind index is stale` the
moment the memo landed. `python3 resources/memos.py index <board>` was run and
`git diff --stat` names exactly one added row (9 to 10 insertions on a file
three sibling sessions had already regenerated). No footprint in this PRD names
that path, and the spec could not omit the index without leaving the gate red.
**The next author of a memo spec should carry `pearde/memos/README.md` in the
footprint.** This is the route's own known row, hit again.

**The daemon's board registry is full of dead fixture boards.** `serve.py
status` lists at least nine entries on `/var/folders/.../tmp.*/pearde` and one
on a scratchpad path, synced 20 to 35 minutes before this run began — other
sessions' probes registering the throwaway board they built. None are this
pass's (every temp dir this pass made is named and gone). Each is a
`--fix`-shaped command run against a fixture while the real daemon was up.
`serve.py forget <name>` removes one; the repair is owed to whichever probe
registers them, not to this PRD.

**A `git log --name-only -N` needle in a fixture-building harness reads the
fixture's own base commit.** Caught in this pass's own draft and fixed here,
but it is a general trap for the shape this repo writes a lot of: a harness
that builds a repo, commits a base, runs the tool and then asks "does a commit
name this file?" cannot fail, because the base commit names it. The needle has
to be `"$HEAD_BEFORE"..HEAD`. Worth a row in the route's step 3 `Fails when`
table — see Edits.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass. `prd.md` is the unedited template; the contract was taken from `specs/` and pass one's `report.md`, per that step's own `Fails when` row. Both roots' `git status --short` recorded before the first edit. Footprint resolved against the checkout **and** the board — `pearde/memos/…` exists in neither the lane nor the code repo's index |
| 2 | `capture-the-harness-baseline` | pass. 21 harnesses run with `PEARDE_ROOT=<lane>`, whole outputs saved under a per-run subdirectory; 13 recorded red **before the first edit**. Repo gates recorded in three roots, because a lane's `index.py check` and the checkout's answer differently by construction |
| 3 | `attempt-the-build` | pass, partially entered. spec01's build already stood from pass one and was re-measured, not rebuilt — the route's second-pass row. spec02 and spec03 were genuinely unbuilt and are built here. The invariant script is a new file at its contracted path, not under `probe/`, because it is a committed harness rather than a probe; `commits.md`, `files.md` and the memo are edits to footprint files, built in place |
| 4 | `re-run-the-harnesses` | pass. All 21 hold their baseline exactly. One new harness appeared mid-run and is compared to nothing. No flip claimed |
| 5 | `write-the-specs` | pass, in its second-pass form: no spec authored. The `Fails when` table was applied to the three blocks that already stood, and one block was repaired — spec02's `&& exit 1` tail, which aborts under `-e` on its passing case. Every block run as `collect` runs it, green on the merged tree and red with a footprint file mutated |

No back-edge was taken.

### Edits

One row is owed to step 3's `Fails when` table. The atomic caused nothing
wrong; the shape is one it does not list, and it produced two boxes that could
not fail in this pass's own first draft.

| seen | means | do |
|------|-------|----|
| a harness builds its own repo, commits a base, runs the tool, then asserts `git log --name-only -N` names a file — and the row stays green under a mutation that stops the tool committing anything | the `-N` window reaches back past the tool's own commits into the fixture's base commit, which names that file by construction. The row measures the fixture, not the tool | record each repo's HEAD **before** the run and range the log against it — `git log --name-only --pretty=format: "$HEAD0"..HEAD` — then watch the row go red under the mutant. A count of commits is never the window; the window is the commit the run started from |

## Scores

complexity: 18
blast-radius: high
workflow: probe-then-spec
