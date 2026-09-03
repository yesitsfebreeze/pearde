# the daemon must not write into a board path it no longer owns — implementer report

Verdict: DONE

Third pass on `probe-then-spec`, and the one that makes the unit landable. The
analyst built and specced; a second pass closed the boxes; **this pass found
that `collect` could not have landed any of it** and repaired the one thing
standing in the way — spec03's `## Verify and Proof` block, which the second
pass reported as a finding and correctly declined to touch under its own
reading of "do not redefine the spec". Step 5 of this route is explicit that a
second-or-later pass applies its `Fails when` table to the blocks that already
stand, so the repair is this pass's work, and it is the whole of it.

Boxes: **17/17** — spec01 6/6, spec02 6/6, spec03 5/5. No code was written or
reverted in either root. The build stands untouched in the lane
`/Users/feb/dev/infra/pearde/pearde/.lanes/the-daemon-must-not-write-into-a-board-path-it-no-longer-own`,
two modified files, exactly as the previous pass left it.

## The blocker, measured

`collect_one` merges the lane **first** (`collect.py:2039`, `land_lane`) and
runs the verify blocks against the merged tree (`collect.py:2047`). spec03's
block was:

    bash …/probe/verify.sh
    git stash push -q -- resources/board/plan.py resources/board/serve.py
    bash …/probe/verify.sh; test $? -ne 0
    git stash pop -q

On the merged tree both files are committed, so the `stash push` saves nothing,
the second probe run is **green**, `test $? -ne 0` is false, `-e` aborts, and
the block exits 1. `collect` then calls `unland` and the PRD comes back red with
the merge reversed — every time, deterministically.

I built the merged tree collect will see (`git clone --shared` of the checkout
at `1880990`, the lane's two files copied in, committed, the live board
symlinked at `pearde/`) and ran the block the way collect runs it
(`bash -e -o pipefail -c "$(awk …)"`):

    BLOCK EXIT=1
    stash list in merged tree: (empty)

That is the finding the previous pass predicted, confirmed on the actual tree
rather than by reading. The stash-pop hazard it also named is real and worse
than a red: `guarded_run` parks a peer's dirt with its own `git stash push -u`
before running the block, so the block's trailing `git stash pop -q` pops
**that** stash. Since `ba69efa` landed, a real `git stash` is refused outright
by `resources/board/refuse.py` for exactly this reason.

## What this pass changed

One file: `pearde/prds/…/specs/spec03.md`. No code, no probe file, nothing in
either root's tracked tree.

The block now proves the same property on a **copy**, chosen through the
harness's own `PEARDE_ROOT` seam, and never writes to the tree it runs in:

    bash …/probe/verify.sh
    mkdir -p pearde/.state
    M="$PWD/$(mktemp -d pearde/.state/probe-mutant-XXXXXX)"
    mkdir -p "$M/resources/board"
    cp resources/*.py "$M/resources/"
    cp resources/board/*.py "$M/resources/board/"
    python3 - "$M" <<'…'         # removes the two guards this unit added,
    …                            # SystemExit if either anchor has drifted
    PEARDE_ROOT="$M" bash …/probe/verify.sh > "$M/mutant.txt" 2>&1 && rc=0 || rc=$?
    tail -2 "$M/mutant.txt"
    rm -rf "$M"
    [ "$rc" -ne 0 ]

Four properties it was built for:

- **Both layers are copied, not just the files** — `resources/*.py` and
  `resources/board/*.py`. `plan.py:48` and `serve.py:150` put `resources/` on
  `sys.path` and import `memos`, `questions`, `render`, `edit`; a copy of
  `board/` alone dies on `ModuleNotFoundError` and the harness's pinned
  denominator would then read the whole thing as one failure rather than as the
  mutation.
- **Not under `/tmp`.** `serve.EPHEMERAL` covers `/tmp`, `/private/tmp` and
  `/var/folders`, which is where `mktemp -d` lands on darwin, and it turns
  `save_entry` into a no-op — the copy would report the write as absent for the
  wrong reason. The scratch root is `pearde/.state/probe-mutant-XXXXXX`: inside
  the board, gitignored, not under `prds/`, not at the repo root, removed by the
  block.
- **The mutation is behavioural, not textual.** It removes
  `if not is_board_dir(board):` from `state_dir` and
  `if not planlib.is_board_dir(b.path):` from `save_entry` — the two guards this
  unit added. It is not a renamed symbol a `grep` would miss.
- **A drifted anchor is loud.** If either line is not found the Python exits
  non-zero, `-e` aborts, and the block goes red rather than silently proving
  nothing.

Acceptance box 5 was re-worded with it, from "Reverting … to HEAD turns it red"
— a sentence that is false the moment HEAD carries the build — to the
tree-independent claim the block now proves. The rule did not move; its spelling
was tied to a moment. `## What is left` gained the third property.

## Verify output

Every block run the way `collect` runs it (`bash -e -o pipefail`), from the
merged tree:

    spec01 exit=0
    spec02 exit=0
    spec03 exit=0

spec03's two runs inside that exit:

    10 checks · 10 pass · 0 fail
    probe harness complete
    the two guards removed in the copy
    10 checks · 6 pass · 4 fail
    probe harness complete

The same three blocks run **verbatim in the orchestrator's checkout**, which
does not hold the build:

    spec01 in checkout (pre-merge) exit=1
    spec02 in checkout (pre-merge) exit=1
    spec03 in checkout (pre-merge) exit=1

That is the red-to-green flip shown against the tree that does not hold the
build — the whole gate ran on the old files, not a `git show HEAD:` of a
predicate. The probe alone, both roots:

    PEARDE_ROOT=<lane>   10 checks · 10 pass · 0 fail   rc=0
    PEARDE_ROOT unset     10 checks ·  6 pass · 4 fail   rc=1

**The block detects a regression in its own footprint.** With `verify.sh`'s
pinned denominator moved from 10 to 99 — backed up to a scratch dir outside
`prds/`, restored by `cp`, proved back:

    spec03 with verify.sh mutated: exit=1
    11 checks · 10 pass · 1 fail
    restored: cmp clean

Nothing was left behind by any run: `pearde/.state/probe-mutant-*` and
`.probe-daemon-path` are absent in both roots afterwards.

`specced --check`:

    the-daemon-must-not-write-into-a-board-path-it-no-longer-own: ok ·
    complexity 20 · footprint …/probe/repro.py, …/probe/verify.sh,
    resources/board/plan.py, resources/board/serve.py

The three `warn: N of N boxes already ticked before an implementer ran them`
lines are this route's second pass showing through; the gate is `ok`.

## The merge is clean — proved, not assumed

The previous pass reported the checkout carrying a peer's uncommitted
`serve.py` and warned that `git checkout --` would destroy it. That is now
settled: the peer's work landed as `caa9a21` (49 insertions, `class Handler`,
lines 970–1330), the checkout is clean of `serve.py`, and the lane's hunks are
at 475–690. Simulated the lane commit onto current `main` in a shared clone:

    git merge-tree --write-tree --name-only mainsim <lane-sim>
    6133596c89ea1c59e1242dc2665804ffab0893c7
    rc=0

One tree oid, no conflict names. Nothing needs stashing or reverting for this
unit to land.

## Findings

### Closed by this pass

**spec03's `## Verify and Proof` block would have destroyed the checkout and
could never have passed.** Reported by the previous pass, unfixed there,
confirmed on the merged tree here, repaired above. This was a live instance of
`a-verify-block-must-not-destroy-the-checkout-it-runs-in`, whose guard was
reverted from `collect.py` in `8bbb4c1` — so nothing in the machine stops the
next one. The general repair is still owed to that PRD; this is one block.

### Still open

**The defect is running in production right now and the disk is paying for it.**
`/Users/feb/dev/manola/.pearde/.state/parse-cache.json` was 12.3 MB at the
analyst pass, 16.7 MB at the second, and is **16,391,250 bytes with an mtime of
today 09:03** — minutes before this run. `serve.py status` shows the live daemon
on port 8443 still holding `manola` at `/Users/feb/dev/manola/.pearde`, a path
that project moved off. Every tick writes into a board directory the project
deliberately does not have. The lane's build stops it; it keeps growing until
the lane lands **and the daemon restarts**. The previous pass reported the
machine's disk hitting zero and killing commands outright; this is one
contributor and it is this PRD's own subject.

**`machine.py`'s `board_at()` is still blind to the legacy `.pearde` name** — a
different, smaller defect, untouched here and outside this footprint.

**Two reds are one untreated cause and want their own PRD.**
`the-board-runs-itself/init-asks-nothing/probe` asserts doctor's pre-`92e318c`
wording, and `resources/invariants/every-artifact-lands-inside-the-board.sh`
fails on `.obsidian/` at the project root — an invariant contradicting the
layout it protects.

**One PRD claim is wrong and was never corrected in `prd.md`.** `save_entry()`
has one call site, `register()` (`serve.py:546`); it does not run on every tick.
The re-creation vector is the source-change reload (`watch()` → `os.execv` with
the stale in-memory paths) plus `/register` and `ensure`, and the parse cache on
`scan`. Nothing in the fix depends on the wrong claim.

**`timeout` is not on this machine** (darwin, no GNU coreutils). The route names
this row; it fired again.

### Findings carried forward, already closed by the build

Kept by name because this route overwrites `report.md` whole and this is the
board's only copy:

- **The standing `isdir` guard could not heal a repo it had already touched** —
  closed by spec01: the guard tests `is_board_dir`, not `os.path.isdir`, so the
  husk `.state/`-only directory the defect leaves is refused too.
- **`die()` in `state_dir()` would have stopped the whole daemon** —
  `SystemExit` is not an `Exception` and walks through `serve.py:607`'s
  watch-thread guard. Closed by `NotABoard(NotADirectoryError)`; verified here
  that `migrate_legacy_state`'s `except (OSError, SystemExit)` (`plan.py:333`)
  catches it.
- **`parse_cache_save()` is the bigger writer and is covered**, because the
  guard sits inside `state_dir()` rather than in the daemon's two writers.
- **No machine-wide list of boards was added** — the `serve.py` diff adds zero
  `REGISTRY`/`BOARDS_FILE`/`expanduser` lines and `BOARDS = {}` at
  `serve.py:302` is still the only store. Re-checked this pass.

### The gates, in both roots

`python3 resources/index.py check`:

| root | lines |
|---|---|
| checkout | 1 — `references/language.md` references `@references/personas/writer.md`, not on disk |
| lane | 3 — the same one, plus `references/skills/pearde-machine.md` with no row in `references/files.md` and `resources/board/edit.py` referencing `@questions.py` |

The checkout was at three lines during the previous pass and is at one now:
siblings closed two while this unit sat in a lane. The lane still prints all
three because it is cut from `8bbb4c1` and is behind. None names a footprint
path; all are inherited, and the two extra close on the merge.

`bash resources/doctor.sh` in the checkout (with `PEARDE_GUARD_STATE` redirected
to scratch, so the guard's session cache was not written) exits 1 on three rows,
none naming a footprint path: `index broken` (the one line above), `origin
broken` (33 derived, 1 with no `from:`), `knowledge broken` (`graph.json` behind
on `260902-4f91`, `260902-aae0`). `harnesses` and `jstests` are `off` by
settings. `memos` and `workflows`, which the previous pass recorded broken in
the lane, are `ok` in the checkout — the lane's lag, closing on the merge, as
step 4's row for it says.

### A neighbour moved during this run

`references/system.md` was clean in the checkout at my first `git status` and
carries 5 insertions / 5 deletions at my last. Not mine — this pass wrote one
file, `pearde/prds/…/specs/spec03.md`, and the board is gitignored inside the
code repo, so the checkout's dirty list can never carry my edit.

### Knowledge and grammar

Nothing was learned outside this repo, so nothing was written back. No word in
the contract was undefined; I coined none.

## Workflow probe-then-spec

| step | atomic | outcome |
|---|---|---|
| 1 | `read-the-contract` | done — PRD, three specs, the previous report, both footprint diffs and both roots' `git status` read before the first edit. No `@`/`@@` dangled |
| 2 | `capture-the-harness-baseline` | done — probe in both roots (10/0 lane, 6/4 checkout), `index.py check` in both, `doctor.sh` in the checkout, all before the edit |
| 3 | `attempt-the-build` | **not entered.** Third pass; the build is in the tree and every spec's footprint is accounted for. No flip is claimed for the code |
| 4 | `re-run-the-harnesses` | done — nothing moved by this pass's one edit; all three blocks green on the merged tree, red pre-merge, and spec03 red under a footprint mutation |
| 5 | `write-the-specs` | entered **as the table, not as authoring** — its `Fails when` rows applied to the blocks that stand, which produced the spec03 repair above |

### Edits

None to the workflow files. The row the previous pass proposed for step 5's
`Fails when` is now measured rather than predicted, and should be added with the
measurement in it:

| seen | means | do |
|------|-------|----|
| a spec's block reverts its own footprint with `git stash push` / `git stash pop`, or with `git checkout --` | `collect` merges the lane **first** and runs the block in the orchestrator's **checkout** (`collect.py:2039` then `:2047`), so the revert can never turn the harness red once HEAD carries the build — the block fails for ever — and `guarded_run` has already parked a peer's dirt with its own `stash push -u`, which the block's trailing `pop` then takes. Measured on this board: the block exited 1 on the merged tree with an empty stash list | prove the property on a **copy**. Where the harness chooses its tree (`PEARDE_ROOT` here), copy `resources/*.py` and `resources/board/*.py` into a scratch root — **not** under `/tmp` or `/var/folders` if anything in the unit branches on an ephemeral path — mutate the guard there, point the harness at the copy, `rm -rf` it and end on a bare test of the captured code. Make a drifted mutation anchor exit non-zero, or the proof quietly stops proving anything |

One further row is worth the workflow owner's judgement, from step 5's rule that
a second pass applies this table to the blocks that stand:

| seen | means | do |
|------|-------|----|
| a pass reports a defect in its own spec's verify block as a finding and declines to touch it, citing "do not redefine the spec" | the brief's rule is about the unit's **contract** — its acceptance boxes and footprint — not about the block that proves it. A block that cannot pass is not a finding for someone else; it is the thing that stops the PRD landing, and the next pass pays a whole round-trip to learn it | repair the block, re-word only the box wording the repair makes false, and say in the report which spec text moved and why the rule it asserts did not. Step 5's own "second pass" clause already authorises this; say so where a worker will read it |

## Scores

complexity: 18
blast-radius: high
workflow: probe-then-spec
