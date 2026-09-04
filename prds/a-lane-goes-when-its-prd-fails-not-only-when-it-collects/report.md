Verdict: DONE

Second pass on `probe-then-spec`. The analyst's build stood uncommitted in
the lane; this pass rebased it onto main, closed the two acceptance boxes
that had no check behind them, fixed the verify block so `collect` can run
it at all, and added one guard against data loss the feature would otherwise
have caused. Lane `lane/a-lane-goes-when-its-prd-fails-not-only-when-it-collects`
is at `61963c2`, one commit, fast-forward onto `main` (`7f760c2`) — the
checkout moved twice during the run and the lane was rebased onto each.

## Boxes — spec01, 6/6

All six ticked as they closed, each against a run quoted in
`specs/spec01.md`. The probe is now `probe/verify.sh` and prints
`13 checks · 13 pass · 0 fail`; the spec's `## Verify and Proof` block exits
0 both from the lane and from a merged tree built the way `collect` builds
one.

## What this pass changed on top of the analyst's build

1. **The verify block could never have run.** It read
   `bash prds/<slug>/probe/probe.sh`, and `collect` runs a block with
   `cwd=repo` — from the repo root that path is `.pearde/prds/…`. The block
   now resolves the board (`B=.pearde; [ -d "$B/prds" ] || B=pearde`) and was
   run the way `collect` runs it, `bash -e -o pipefail`, exit 0.
2. **`probe.sh` → `probe/verify.sh`.** The board's sweep is
   `find prds -name verify.sh`; a probe called `probe.sh` is a check nobody
   ever runs. Renamed, and the hard-coded absolute `LANE_ROOT=` — a path
   that stops existing the moment this PRD collects — replaced with the
   house `BOARD`-walk + `PEARDE_ROOT` preamble every other harness here uses.
3. **Two boxes had no check.** `--dry` and the R2 docstring were claimed
   green in the previous report and the probe tested neither. Both are now
   cases in the harness (case 3 also asserts the *state* is untouched), and
   both were shown to redden under a mutation.
4. **`git branch -D` takes the branch's reflog with it**, so the checkpoint
   `drop_lane` had just made became reachable only through `git fsck`.
   `delete_branch` now returns the sha it deleted and `release` prints it.
5. **The guard (see the finding below).** `drop_lane` now returns
   `sha is not None or not left` instead of a bare `True`, so a caller can
   tell a clean drop from one that threw uncommitted work away, and
   `cmd_release` deletes the branch only when the drop kept the work.
   Without it, a `## Failure` marker on a board where the checkpoint fails
   deletes the last copy of the worker's build. No existing caller reads
   `drop_lane`'s return, so `sweep` is byte-identical.
6. `drop_lane`'s checkpoint **commit message** still said `sweep` when
   `release` was the caller; it takes `who` now, like the progress lines.

## Baseline and re-run — no harness moved

Board harnesses naming a footprint path: 15 of 101, all honouring
`PEARDE_ROOT` (`grep -q` in a loop — `grep -l`/`-L` over a `$(find …)` list
answers identically and wrongly under the `ugrep` this machine aliases as
`grep`, see Edits). Baseline taken **before the first edit** on a
`git clone --shared --branch main` of the checkout with the live board
symlinked in, re-run on the lane with the scaffolding in the same state.

- Both trees: **4 pass, 11 fail**, the same eleven, identical output but for
  echoed paths and timestamps. Every red was red before the first edit.
- `the-board-asks-for-itself/a-question-in-plain-words` went green → red
  mid-run. Not mine: it enumerates the live board, and a sibling wrote an
  unanswered question on `the-file-index-is-green-so-a-spec-can-assert-it`
  between the two runs. Re-running it against the pre-edit clone at that
  moment reddens it identically.
- `the-board-runs-itself/the-next-line-runs` reads one FAIL *fewer* in the
  lane (95 pass vs 94). The extra baseline FAIL is `the alias line —
  missing 'alias pearde='python3 /tmp/lanefail-base2/pre/…''`: an artefact
  of measuring a scratch clone, not a flip.
- `transitions-are-commands` is red on both sides on the sibling's new
  `"why": "every question answered"` key in `.transitions.jsonl` — inherited
  from `enforce-pointer-not-verdict`, outside this footprint.
- Repo gate, both trees identical: `index.py check` 28 lines (0 naming this
  footprint), `doctor.sh` broken on `index claims origin memos workflows
  knowledge questions`. All inherited.
- `probe/verify.sh` is **new**, so it has no baseline; 13/13 on the lane and
  on the merged tree.

## Findings

### Carried forward from the analyst's pass

- **R3 — not built, and still the orchestrator's call.** R3 asks that
  `the-board-reclaims-dead-work-by-itself/a-lane-is-removed-when-its-prd-collects`
  and `the-lifecycle-contract-and-purge-reclaims-it` land first or fold into
  this one. Neither is this PRD's footprint. This unit does not conflict with
  either (`collect.py`, `references/files.md`), so R1/R2 landing first blocks
  nothing. Still true: `index.py check` names three dangling
  `@resources/board/purge.py` references on both trees — the purge PRD has
  not landed.
- **The two-line print on a marked failure** (`… branch <b> kept` from
  `drop_lane`, then `… branch <b> deleted`) is still two lines. Sequentially
  correct, reads oddly side by side, and restructuring `drop_lane`'s single
  return-message shape for one caller costs more than it buys. The second
  line now carries the sha and the reason, which is what a reader needs.

### New — a lane's own `.pearde` symlink breaks every checkpoint

`lanes.create` now gives each lane a `.pearde -> ../..` symlink (`3904b7b`).
On a repo whose `.gitignore` does not name the board, `lanes.dirty` reports
that symlink as an uncommitted path, so `drop_lane` always enters its
checkpoint branch and `commit_all`'s `git add -A` refuses:

```
The following paths and/or pathspecs matched paths that exist
outside of your sparse-checkout definition, so will not be
updated in the index:
.pearde
```

`LaneError` → `<who>: <prd> checkpoint failed — …` → `remove --force` takes
the lane with everything uncommitted in it. On a clean lane that is a false
data-loss report; on a dirty one the checkpoint that exists to save the
worker's build does not run and the build is gone. The pearde repo
gitignores `/.pearde`, so this is invisible here — but `init.py init` writes
no `.gitignore`, so it fires on every freshly initialised board and in every
fixture built with it. It is `sweep`'s path as much as `release`'s and
predates this PRD; `init.py` is outside this footprint, so it is reported,
not fixed. What *is* fixed here is that this PRD's own new branch deletion
can no longer run on top of it (change 5 above, case 5 in the harness).
Recorded as `[[260904-5ce8]]`.

### Defects outside scope, not touched

- `init.py init` writes no `.gitignore` naming the board — above.
- The board's own git repo has `prds/a-lane-goes-when-its-prd-fails-not-only-when-it-collects/`
  **untracked**, `probe/verify.sh` with it. Harness fixtures that copy from
  `git ls-files` will not see this probe until the board stages it.

## Workflow probe-then-spec

| # | step | result |
|---|------|--------|
| 1 | read-the-contract | done — `prd.md`, `specs/spec01.md` and the previous `report.md` read; no fork left open, no question asked back |
| 2 | capture-the-harness-baseline | done — 15 footprint-naming harnesses of 101 + the repo gate, taken on a `clone --shared` of the pre-edit tree before the first edit; re-anchored to `main` after the rebase and both sides re-taken |
| 3 | attempt-the-build | **not entered as build-and-spec** — second pass, the one spec's build was already in the tree (`attempt-the-build`'s own first `Fails when` row). Re-entered for repair only: the rebase conflict, and the `kept` guard step 5 turned up |
| 4 | re-run-the-harnesses | done — identical pass/fail sets on both trees, no green→red this build caused; the one flip traced to a sibling's write on the live board |
| 5 | write-the-specs | applied to the standing spec, no new spec authored: verify block made runnable under `collect`, two unbacked boxes given checks, every check mutated to prove it can fail, the previous report's findings carried forward by name |

No back-edge was taken twice. One rebase: the lane was based on `cb959b9`
and `main` had moved to `676ce01` with a sibling hunk two lines above mine
in `cmd_release` (`"question": ("open",)` in `allowed`). Committed the
build, `git rebase main`, resolved the one conflict by keeping both, as
`attempt-the-build`'s anchor row directs. Never `git merge main`.

### Edits

**`capture-the-harness-baseline`, step 1** — the command
`grep -L PEARDE_ROOT $(find <board>/prds -name verify.sh)` does not work on
this machine: `grep` is `ugrep`, which prints
`<path>: File name too long` on the last argument and returns the *same*
list for `-l` and for `-L`, so a worker following it reads "no harness
honours PEARDE_ROOT" and "every harness honours PEARDE_ROOT" from the same
board. Replace the sentence

> `grep -L PEARDE_ROOT $(find <board>/prds -name verify.sh)` names the ones
> that do not

with

> `for f in $(find <board>/prds -name verify.sh); do grep -q PEARDE_ROOT
> "$f" || echo "$f"; done` names the ones that do not — one file per call.
> `grep -l`/`-L` over a `$(find …)` argument list is not portable here:
> `ugrep`, which this machine aliases as `grep`, prints `File name too long`
> on the list's tail and answers `-l` and `-L` identically, so both
> questions read green.

**`attempt-the-build`, `## Fails when`, the second-pass row** — it says to
"run steps 1, 2 and 4, and enter step 3 **only for the specs whose build is
not in the tree**", which reads as forbidding any code edit on a second
pass. Step 5's own `Fails when` table routinely turns up a defect in the
standing build (here: a verify block `collect` cannot run, two boxes with no
check, a branch deletion that could destroy the last copy of a build), and
repairing those is a code edit in step 3's files. Append to that row's `do`
column:

> Re-entering step 3 to repair what step 5's table finds in the standing
> build is not a second build and does not count as a back-edge — say in
> the report which repairs were made and against which `Fails when` row,
> and re-run step 4 after them.

## Scores

complexity: 14
blast-radius: mid
workflow: probe-then-spec
