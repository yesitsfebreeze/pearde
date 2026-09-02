# a-session-ledger-names-who-holds-what-and-reaps-what-is-gone — implementer report

Verdict: DONE

Worker `impl-session-ledger`, as engineer, workflow `probe-then-spec`, third
pass. This report replaces the second pass's at the same path; every
`## Findings` entry it carried is carried forward here by name, and the ones
this pass re-measured are marked.

**The one thing this pass changed, and why it was needed.** The second pass
found the build uncommitted in the lane and reported DONE. A `collect` ran
after it, at 22:49, and committed the lane — `d8be966`, the five footprint
files, `collect`'s own message shape. Its merge into the checkout then failed:
`lanes.merge` is rebase-then-ff-only, and the rebase conflicted on
`references/files.md` and `references/parts/handles.md`, both rewritten dense
in `main` by the prose sweep after the lane was cut. `land_lane` raises `Stop`
on that, aborts, and leaves the PRD `claimed` — which is the state this pass
was dispatched into. `.transitions.jsonl` confirms it: the last row for this
PRD is `specced → claimed` at 20:14 and there is none after.

So the specs were green and unlandable. Both conflicting files are in
spec02's `footprint:`, so resolving them is inside this unit's scope, and the
lane was rebased onto `main` rather than merged — a merge commit would put two
commits behind one PRD and break the `--ff-only` that `plan.lanes` draws its
bar off. Each conflict was one added table row against a row the sweep had
rewritten: `session.py` beside main's new `shared.py` in `references/files.md`,
and `a worktree per run session` beside main's `one copy of what every lane
rebuilds` in `references/parts/handles.md`. Both sides kept, neither reworded.

The lane is now `9a98fae` — one commit, on top of `main` at `1abd630`, working
tree clean, and `git merge-base --is-ancestor` says the ff-only merge lands.

## Boxes

| spec | boxes | verified | how |
|---|---|---|---|
| `specs/spec01.md` | 16 | 16 | the probe, 29 passed 0 failed, plus the routing and parse lines of its own block |
| `specs/spec02.md` | 8 | 8 | the block exits 0 under `bash -e -o pipefail`; each of the four rows read in the rebased tree |
| `specs/spec03.md` | 6 | 6 | the block exits 0 from the checkout; `check-ignore` on a nested path |

30 of 30. Every one was re-run against the rebased lane after the conflicts
were resolved, not carried over from the run before it. None re-ticked, none
unticked.

## Verify and Proof, run

**spec01** — the probe against the lane, `PEARDE_ROOT=<lane>`:

    29 passed, 0 failed
    PROBE GREEN
    exit 0

**The red-to-green flip, shown against the tree that does not hold the
build.** The block was run verbatim from the checkout, where `collect` runs
it and where `resources/board/session.py` does not exist:

    probe: a session ledger names who holds what and reaps what is gone — tree /Users/feb/dev/infra/pearde
      FAIL no /Users/feb/dev/infra/pearde/resources/board/session.py
    PROBE RED — 1 failure(s)
    exit 1

and in the lane, with only the hard-coded board path substituted (the lane
sparse-checks the board out of itself, so `$(git rev-parse
--show-toplevel)/pearde/prds/…` cannot resolve there), **exit 0**. This is the
whole gate run on the old file, not a `git show HEAD:` on a predicate.

The rest of the block, in the lane:

    pearde session               one worktree per run session, its ledger, and…
    pearde session: takes take, list, reap, owns
    rc=2
    ast ok

`resources/board/session.py` is 503 lines. Its imports are `json os re
subprocess sys time` plus `plan`, `lanes` and `transitions` — the board's own
sibling modules, reached through the `sys.path.insert(0, HERE)` that every
module in `resources/board/` uses. The box says "Python 3 stdlib only"; that
is true of everything off this repo, and the three in-repo imports are named
here so the next reader is not surprised by them.

**spec02** — the block, run the way `collect` runs it, from the rebased lane:
**exit 0**. Its one printed row is `  index       broken  2 problems`, printed
and deciding nothing, as the block intends. The box the block asserts is
`grep -c session` over `index.py check` being `0`, and it is.

The four rows were read in the rebased tree, not inferred:

- `references/files.md:159` — the `@resources/board/session.py` manifest row.
- `references/parts/handles.md:68` — `session take/list/reap/owns`, the four
  verbs, the module.
- `index.md:62` — `@resources/board/session.py` in the `@@handles` row.
- `references/parts/loop.md:52-59` — the **Before step 0** block naming
  `pearde session reap --apply` then `pearde session take`, saying a live
  session's tree is never reaped, naming `refs/pearde/reaped/<id>`, and
  stating in as many words that "Board commands do not yet resolve the taken
  tree as the code repo" — box 7's negative claim, kept.

**spec03** — the block, run from the checkout root as `collect` would:

    .gitignore:17:.sessions/	.sessions/
    .gitignore:40:.state/sessions.json	.state/sessions.json
    exit 0

Box 5 says "shows neither path after a `pearde session take`". No `take` has
been run against the live board — `<board>/.sessions` and
`<board>/.state/sessions.json` are both absent. Rather than cut a real session
worktree in a board several sessions are working in, the box was proved on the
predicate `status` itself consults:

    git -C pearde check-ignore -v .sessions/s12345/resources/board/session.py
    .gitignore:17:.sessions/	.sessions/s12345/resources/board/session.py

A directory pattern that ignores an arbitrary nested path ignores every path a
`take` can create, and `status` never lists an ignored path. Box 6 holds:
`git -C pearde diff --numstat -- .gitignore` is `17	0` — seventeen lines
added, none removed, so no row was changed or reordered.

## Findings

**`collect` already ran on this PRD and its merge was left unlanded — now
fixed, and the mechanism is worth writing down.** `land_lane` commits the lane
*before* it merges, so a conflict leaves the work committed on `lane/<slug>`,
the checkout untouched, and the PRD in `claimed`. Nothing on the board says
"committed but unmerged": `.transitions.jsonl` shows only `→ claimed`, and a
worker re-dispatched onto that PRD reads a clean lane and a clean checkout and
has to find `git log` to learn the build exists. The lane is rebased and
ff-only now, so the next `collect` lands it, but a board that runs many lanes
against a moving `main` will hit this repeatedly and the state is silent about
it. Reported for routing, not fixed beyond this PRD.

**`pearde/.gitignore` is on the board branch, and `collect` will not commit
it — measured, and it bites.** Carried forward from both earlier passes and
confirmed again. The file is absent from the lane entirely (the lane
sparse-checks the board out) and present and **uncommitted** in the board's
own worktree. `pearde collect` commits the code repo's footprint out of the
lane; there is no path by which it reaches `pearde/.gitignore`. spec03 is done
on disk and stays uncommitted until someone commits it on the board branch.
The orchestrator has to do that deliberately. Note that the sibling PRD
`collect-stages-the-board-s-gitignore-in-the-outer-repo-which…` landed in
`main` at `3f4afe2` and the memo
`pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md` now exists, so
this is a known and owned defect rather than an open one.

That file additionally holds **hunks that are not this PRD's**: a `.lanes/`
block and a `health/` block, both uncommitted beside spec03's two. Whoever
commits it commits three units' rows at once, or splits by hunk.

**`doctor.sh` fabricates a board in a lane — new, measured this pass, not
mine.** In the lane after the rebase, `doctor.sh .` prints
`board ok ./references/prds · 0 PRDs · language English`, and
`references/prds` **does not exist** on disk in the lane or the checkout. In
the checkout the same command correctly prints `./pearde/prds · 140 PRDs`.
Before the rebase, the lane's older `doctor.sh` printed `board off — no
board`, which was the honest answer. Whatever landed in `main` between
`6affd1b` and `1abd630` — the resolver change under
`the-doctor-walks-to-a-board-not-to-a-name` is the candidate — turned "no
board here" into a green row naming a directory that is not there. The
`members` row is confabulated off the same path. Outside this PRD's footprint;
reported, not fixed.

**Two probe fixtures outlived their runs.** `pearde-session-probe.bj9pPH` and
`pearde-session-probe.dOpKpR` under `$TMPDIR`, left by runs killed before the
`trap` fired. Still two after this pass, so this run's own fixture cleaned up.
Neither registers a worktree in the real repo (`git worktree list | grep -c
folders` is `0`), so they are residue and not a hazard.

**Hand-walking the board is refused, including by `find` and by a glob.** The
guard fires on `find <board>/prds -name prd.md` and on `ls -d <board>/prds/*/`,
not only on a `grep` sweep. Carried forward from the second pass; the route
edit it proposed is still unapplied and is repeated under `### Edits`.

**The machine's disk filled mid-run on the second pass** (`ENOSPC` on
`/System/Volumes/Data`, every tool down for about two minutes). Carried
forward as the first thing to check when a worker on this board reports that
nothing runs. Not seen this pass.

**Carried forward from the analyst pass, unchanged and not re-measured:**
worktrunk owns one of the four parts and neither the ledger nor the reaping
(`[[260902-eb91]]`); the parent PRD cites `references/parts/run.md`, which does
not exist, for the *watch set is the whole configuration* invariant, which is
in `references/skills/pearde-all.md:55`; the knowledge gap enqueued at
`pearde/wiki/pending/260902-13eb.md` with `[[260902-4385]]` and
`[[260902-eb91]]` written back; and the three words this contract needs that
`grammar.md` does not define — `session`, `ledger`, `reap`.

**Pre-existing red, both roots, before this pass's first edit.**
`index.py check` in the lane before the rebase named three problems; in the
checkout, one. Two of the three closed on the rebase, having been fixed in
`main` after the lane was cut — a lane behind the checkout, the mirror-image
case step 4's own table names, and not a flip of this unit's. After the
rebase the lane names two:

    references/language.md references @references/personas/writer.md — not on disk
    references/parts/commits.md references @pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md — not on disk

The first is in both roots and is a live finding belonging to nobody here. The
second is a **lane artefact**: that memo exists on the board and the lane
sparse-checks the board out, so the reference dangles only where the board is
not checked out. It is not a defect and it closes the moment the merge lands.
Neither names a file in this PRD's footprint, and neither is claimed as
anything of this unit's.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | pass — `prd.md`, three specs and the previous report read; `git status --short` recorded in the lane, the checkout and the board before the first command. Two rows fired: the footprint path absent under the `repo:` root (`pearde/.gitignore`, resolved against the board), and "the brief says the probe's code is uncommitted and `git status --short` is clean" — the cause here was not a sibling but this PRD's own `collect`, which is the `### Edits` entry below |
| 2 | `capture-the-harness-baseline` | pass — the gate is `index.py check` + `doctor.sh`, recorded in **both** roots with `PEARDE_ROOT=<lane>` before anything ran, per step 4's row on a lane behind the checkout. Board harnesses were not swept: no code was written, only a rebase resolved inside the footprint |
| 3 | `attempt-the-build` | **not entered** — the second-pass row of its own `Fails when` table: the specs exist and the build is in the tree. No flip is claimed beyond the verbatim-from-the-checkout failure quoted above, which is the build's own, earned by the pass that wrote it |
| 4 | `re-run-the-harnesses` | pass — every block re-run after the rebase, all three exit 0; the two index lines that closed are disclaimed above as `main`'s, not this unit's; the one that appeared is named as a lane artefact |
| 5 | `write-the-specs` | **not entered** for authoring; its row on a report already at the path was applied — both earlier passes' `## Findings` are carried forward by name |

### Edits

**One, new.** In `probe-then-spec` step 3, `#### Fails when`, the row reading:

> | the brief says the probe's code is uncommitted, and `git status --short` is clean | a sibling session committed the whole tree, your hunks with it | `git log -1 -- <footprint path>` and read the file itself before concluding anything is missing; if the behaviour is present, the work stands — record the commit that took it, and read every spec's "what already stands" against the **file**, never against a diff |

Replace with:

> | the brief says the probe's code is uncommitted, and `git status --short` is clean | a sibling session committed the whole tree, your hunks with it — or, on a lane, this PRD's **own** `collect`: `land_lane` commits the lane before it merges, so a conflict in the rebase leaves the work committed on `lane/<slug>`, the checkout untouched and the PRD still `claimed`, with nothing on the board saying so | `git log -1 -- <footprint path>` and read the file itself before concluding anything is missing; if the behaviour is present, the work stands — record the commit that took it, and read every spec's "what already stands" against the **file**, never against a diff. On a lane also run `git -C <checkout> merge-base --is-ancestor HEAD lane/<slug>` and `git merge-tree --write-tree --name-only HEAD lane/<slug>`: where it names conflicting files that are all inside your footprint, rebase the lane onto the checkout's branch and resolve them — never `git merge` main into the lane, which puts two commits behind one PRD and breaks the `--ff-only` `lanes.merge` needs. Where a conflicting file is outside the footprint, stop and report it |

**One, carried forward from the second pass and still unapplied.** In
`probe-then-spec` step 3, `#### Done when`, the third bullet reads:

> - `ls <board>/prds` against the pre-run listing shows no `prds/<slug>/` you did not make — a hand-walked sweep over the board is refused by the guard in a wired repo, and the listing answers the same question. `git status --short` is silent here where the board is gitignored.

Replace with:

> - `ls <board>/prds` against the pre-run listing shows no `prds/<slug>/` you did not make — a hand-walked sweep over the board is refused by the guard in a wired repo, and the listing answers the same question. The guard reads the *shape* of the command, not only its tool: `find <board>/prds -name prd.md` and `ls -d <board>/prds/*/` are both refused, and only the bare one-level `ls` gets through. Where the board is its own git worktree — the layout on this board — `git -C <board> status --short -- prds` answers it too and names the untracked ones; it is silent only where the board is gitignored inside the code repo.

Nothing else in the route misfired. Its step-1 row on a footprint path absent
under the `repo:` root, its step-3 row on the second pass, its step-4 row on a
lane behind the checkout, and its step-5 row on a report already at the path
each named this run's situation exactly, and each was followed as written.

## What is left

Nothing in the three specs. The lane is at `9a98fae`, one commit on top of
`main` at `1abd630`, and the ff-only merge lands — `collect` can run.

Two acts this PRD cannot finish for itself: committing `pearde/.gitignore` on
the board branch, and routing the two findings above that are outside this
footprint (`doctor.sh`'s fabricated board row in a lane, and the silence of a
committed-but-unmerged lane).

The two siblings under the parent are untouched:
`board-commands-run-in-the-session-s-tree-not-the-checkout` makes the board
follow a session into its tree, and
`no-destructive-git-runs-in-a-tree-the-session-does-not-own` is the refusal
that reads `session owns`.
