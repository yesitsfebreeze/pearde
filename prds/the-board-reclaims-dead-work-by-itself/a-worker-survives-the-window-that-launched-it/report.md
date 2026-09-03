# report — a worker survives the window that launched it

worker: impl-worker-survives · persona: engineer · 2026-09-03
board: /Users/feb/dev/infra/pearde/.pearde
repo: .pearde/.lanes/the-board-reclaims-dead-work-by-itself-a-worker-survives-the-window-that-launched-it

Verdict: DONE

Both specs implemented in the lane, every box closed and run. The PRD's own
probe is **48 checks · 48 pass · 0 fail** (baseline 34 · 15 pass · 19 fail),
green four ways in parallel. One committed harness outside the footprint
goes red on the tenth verb this contract adds — quoted below with the exact
one-line replacement, not edited: it is another PRD's file.

The build is committed on `lane/…-a-worker-survives-the-window-that-launched-it`
at `7432e4a8119f`, by the command this PRD built:

    checkpoint: …a-worker-survives-the-window-that-launched-it 2 path(s)
    committed as 7432e4a8119f on lane/…

## The build was gone again

The specs say "built and probed in this pass, uncommitted in the lane". It
was not there. `git status --short` in the lane was empty, and the two
footprint files in the orchestrator's checkout hold **neighbours'**
uncommitted hunks, not this PRD's: `transitions.py` carries `claim_liveness`
and `tick_sweep` (the unattended-reclaim sibling, whose own comment says
"`drop_lane` gains the same commit … in `a-worker-survives-the-window-that-
launched-it` spec01"), and `dispatch.py` carries `LIMIT_PAT` and the
limit-halts-the-run branch. Neither was carried into the lane.

So this is the **third** pass to build this contract and the second to lose
the previous one — to the exact failure the contract is about. It was rebuilt
from the specs' own "What already stands" prose, in the lane, and committed
there before this report was written.

## What stands now

`resources/board/transitions.py`

- `drop_lane` checkpoints before `lanes.remove`, only when `lanes.dirty` is
  non-empty, with the PRD rel in the message; the line now reads
  `· N path(s) committed as <sha>`, and `uncommitted path(s) dropped` only
  survives for the `LaneError` path, which also prints `checkpoint failed`
  and still removes the worktree.
- `cmd_checkpoint` — `pearde checkpoint <prd>`: resolves the PRD, refuses one
  with no lane (`holds no lane — nothing to checkpoint at <dir>`), answers
  `--dry` **before** the clean-lane branch, prints `N path(s) committed as
  <sha>` / `lane clean, nothing standing` / `would commit N path(s)`, is in
  `FLAGS` and `COMMANDS`, and needs a persona (not in `DEFAULTS_FOR`).
- The module docstring gains the usage row and the paragraph naming both
  edges; "all nine do" → "all ten do".

`resources/board/dispatch.py`

- `CHECKPOINT_S = float(os.environ.get("PEARDE_CHECKPOINT_S", "120"))`.
- `Job.ckpt_t`, seeded at `t0`.
- `Job.checkpoint(log)` — `lanes.commit_all` on the job's own board and rel;
  silent with no lane and with a clean lane, `ckpt <addr> · committed as
  <sha>` on a commit, `ckpt <addr> · skipped — <git>` on a `LaneError`,
  never raising: the likeliest refusal is the worker's own git holding the
  index, and the next interval retries.
- The reap loop checkpoints every live job whose `ckpt_t` is older than
  `CHECKPOINT_S`, resetting it after each call; `CHECKPOINT_S > 0` guards it.

`probe/verify.sh` grew from 34 checks to 48 — the boxes the prior pass's
probe left uncovered (A3 the refused checkpoint, B7 `--dry` on a *dirty*
lane, B8 a refusal writing nothing, C3–C5 the timer's interval and its off
switch, C6 the skipped git) — and its section D was repaired; see Findings.

## Verify and Proof

- `probe/verify.sh`, `PEARDE_ROOT=<lane>`: **48 checks · 48 pass · 0 fail**,
  rc 0. Run four times concurrently as `( … ) &`, the shape
  `doctor.sh --harnesses` uses: 48/48 every time.
- spec01 block, `LANE=<lane>`: `sweep-checkpoint: ok` / `checkpoint-command:
  ok`, rc 0.
- spec02 block, `LANE=<lane>`: `dispatcher-checkpoint: ok`, rc 0.
- The command run on this PRD's own live lane: `would commit 2 path(s)`
  under `--dry`, then `2 path(s) committed as 7432e4a8119f`, lane worktree
  still on disk and `git status --short` in it now empty.
- `doctor.sh <board>` with `PEARDE_ROOT=<lane>`, diffed against the
  pre-edit baseline: **no row changed status**. Every difference is the
  live board moving under the run — 223 → 226 PRDs, index 189 → 191 files
  and 39 → 40 keywords, health 188 → 189 files, a second stale graph id,
  the statusline. None of those paths is mine; I added no file to the map.
- `index.py check`: lane rc 1 on four lines — `resources/common.py` on disk
  with no `references/files.md` row, `files.md` and `@@view` naming
  `hotreload-test.js` which is not on disk, `commits.md` naming a memo that
  is not on disk. The checkout's own `index.py check` is **rc 0** on all
  four. The lane is cut from `7a162c2`, behind `main` at `77665a3`; every
  one of these closes on the merge. None names a footprint file.

## Harnesses

Baseline taken before the first edit, `PEARDE_ROOT=<lane>`, over the 29
harnesses that name `transitions.py`/`dispatch.py` or enumerate the board.
Three counts moved; 26 are byte-identical.

| harness | baseline | now |
|---|---|---|
| this PRD's own probe | 34 · 15 pass · 19 fail | **48 · 48 pass · 0 fail** |
| `the-board-runs-itself/transitions-are-commands` | 74 · 67 pass · 7 fail | 74 · 66 pass · **8 fail** |
| `nothing-left-open/the-line-tells-the-truth` | 85 · 80 pass · 5 fail | 85 · 81 pass · 4 fail |

The whole-board sweep was not the baseline: `doctor.sh --harnesses` over
this board's **92** harnesses was killed twice past ten minutes without ever
reaching the harness rows. The subset above is what the atomic's step 2
actually asks for; the atomic's own command is not runnable here (Edits).

**`transitions-are-commands` is the one honest red, and it is not mine to
close.** Its line 170 pins the verb set shut:

    assert sorted(t.COMMANDS)==['add','answer','claim','defer','release','retry','set','sweep','unblock'], sorted(t.COMMANDS)

`checkpoint` is the tenth verb this contract asks for, so the matcher is
honest and the file is another PRD's. The exact replacement, for whoever
owns that transition — one line, one file,
`.pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh`:

    assert sorted(t.COMMANDS)==['add','answer','checkpoint','claim','defer','release','retry','set','sweep','unblock'], sorted(t.COMMANDS)

and the label above it, `"COMMANDS exposes the nine names"` → `"COMMANDS
exposes the ten names"`. `references/parts/workers.md` is explicit that a
change to another PRD's file is the orchestrator's edit on the transition
and the worker reports the wording, so it is reported, not made.

`the-line-tells-the-truth` **gained** a pass (`F5 …the sentinel is still up
afterwards` went from FAIL to ok). Nothing in my two files can reach a
serve sentinel; it is a neighbour's landing or that harness's own service
contention, and the rise is not mine to claim.

## Findings (report-only)

- **Section D of this PRD's own probe measured the runner, not the
  interrupt.** It was 48/48 standalone and 46/48 whenever it ran as
  `( … ) &` — the shape `doctor.sh --harnesses` uses — with `D0 the
  window's interrupt was delivered` and `D1 an attached child died with the
  window` red every time, consistently, not by race. A non-interactive
  shell sets SIGINT to `SIG_IGN` for a background job and every child
  inherits it, so `killpg` raised nothing. Repaired inside this PRD's own
  probe: `signal.signal(signal.SIGINT, signal.default_int_handler)` in the
  fixture and `preexec_fn` restoring `SIG_DFL` in both children; the fixed
  sleeps were also replaced with waits for evidence. Written to the KB as
  `260903-656a`.
- **Carried forward from the previous pass's report, still true:**
  - An analyst's own uncommitted build is as exposed as a worker's lane —
    proven twice now, once more by this pass finding nothing in the lane.
    The analyst-side equivalent of `checkpoint` is not in this footprint.
  - `260903-44fa` in the KB: `commit_all` existed with zero callers.
  - The prior pass reported a stale `lane/…-a-worker-survives-…` branch
    carrying an unrelated `pearde_path` removal. That branch is this PRD's
    lane now and the build sits on it; nothing to clean.
- The board's `questions` doctor row names this PRD:
  `` `## Answers` with no `## Questions` above it ``. The previous analyst
  answered Q1 without writing the fork down. `prd.md` frontmatter and body
  are the orchestrator's; not edited here. Two other PRDs carry the same
  shape, so the row stays red either way.
- The orchestrator's checkout holds neighbours' uncommitted hunks in **both**
  of this PRD's footprint files (named above). The merge of this lane will
  need `git -C <checkout> checkout -- resources/board/transitions.py
  resources/board/dispatch.py` first, or the two will conflict: my lane copy
  is not a superset — the neighbours' `tick_sweep`, `claim_liveness`,
  `LIMIT_PAT` hunks are **not** in it and must not be lost. They are separate
  regions of both files, so a three-way merge should carry both; it has not
  been proven here because the checkout is not mine to clone mid-run.

## Health

The brief's floor list was empty — no footprint file under the health floor.
Nothing refactored.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | pass — PRD, both specs, `## Answers`; the lane-is-empty row fired and sent me to the checkout's diffs, which were neighbours' |
| 2 | capture-the-harness-baseline | pass, narrowed — the whole-board sweep is not runnable here; 29 harnesses selected by footprint and by enumeration, counts recorded before the first edit |
| 3 | attempt-the-build | pass — both units built in place in the footprint files; no back-edge |
| 4 | re-run-the-harnesses | pass — 26 identical, one mine and green, one honest red reported, one rise disclaimed |
| 5 | write-the-specs | pass — second pass, no spec authored; the `Fails when` table applied to the standing blocks, all twelve boxes ticked as closed |

### Edits

**`read-the-contract` — the row on a lane with no build does not cover the
build being gone from everywhere.** Its last-but-three row assumes the
checkout holds the hunks. Here nothing anywhere held them. Add after that
row:

| `git status --short` is empty in the lane, and `git -C <checkout> diff` on every footprint path shows only hunks that are plainly a neighbour's | the build the specs describe is gone — a lane was swept, or a session's checkout was reverted, between the pass that built it and yours | build it again from the specs' own `## Acceptance` and their "what already stands" prose, which is the surviving record of it, and say in the report that this is a rebuild rather than a continuation. Do not report BLOCKED: a spec that describes the build is a contract you can meet |

**`capture-the-harness-baseline` — step 1's own command is not runnable on a
board of this size.** `bash resources/doctor.sh --harnesses <board>` over 92
harnesses was killed twice past ten minutes here without printing the
harness rows. Replace the sentence "Most board harnesses take their root
from `PEARDE_ROOT` …" with:

> Most board harnesses take their root from `PEARDE_ROOT` and fall back to
> the board's own repo. Count them first — `find <board>/prds -name
> verify.sh | wc -l`. Past about thirty, the whole sweep is not a baseline
> you can take: it costs tens of minutes and dies before it prints. Select
> the set instead — every harness naming a footprint path, every one whose
> PRD is in `needs:`, every one that runs a repo-root `git status`/`git
> diff`, and every one that enumerates the board — and run those with
> `PEARDE_ROOT=<lane>`, four at a time, saving each output. Say in the
> report that the baseline is the selected set and name how it was selected.

**`attempt-the-build` — the "probe passes standalone, fails under its own
runner" row names a variable; the disposition is the other half.** Add:

| the probe passes standalone and fails only under the harness sweep, with the same checks red every time and no timing jitter | not a race: a non-interactive shell sets SIGINT/SIGQUIT to `SIG_IGN` for a background job (`( … ) &`, the shape the sweep uses) and every child inherits it, so a probe that replays an interrupt measures the runner's job control | restore the disposition explicitly — `signal.signal(signal.SIGINT, signal.default_int_handler)` in the fixture and `preexec_fn` setting `SIG_DFL` in every `Popen` — then run the probe four ways in parallel before quoting a count |

**`re-run-the-harnesses` — its committed-harness row tells the worker to take
another PRD's file into the footprint; `references/parts/workers.md` says the
worker reports the wording instead.** Replace the `do` cell of "a committed
harness outside your footprint goes red on a count the contract itself
moves" with:

> leave it red and quote it beside its baseline. Do **not** edit it and do
> not take it into the footprint: `references/parts/workers.md` holds one
> writer per file, and a change to another PRD's file is the orchestrator's
> edit on the transition. Put the exact replacement line in the report —
> the file path, the line as it stands, the line as it should read — so the
> orchestrator can make it without reopening the question.
