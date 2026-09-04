Verdict: DONE

Pass two on this route: the specs stood, the build stood, and this pass
measured both. `spec01` — 6/6 boxes, every one now backed by a check that
runs and that fails without the fix. Four of the six were ticked from
reading on pass one; the probe now exercises them.

## Boxes

| box | check | output |
|---|---|---|
| `collect_one` → `done` removes `.claims/<rel>/` | probe `case_done` | `('done', True, 0, False) PASS` |
| `--fail` red gate → `failed` removes it | probe `case_failed` | `('failed', True, 1, False) PASS` |
| `block_conflict` → `blocked` removes it | probe `case_blocked` | `('blocked', True, 1, False) PASS` |
| `close_container` → `done` removes it | probe `case_container` (**added this pass**) | `('container', True, 0, False) PASS` |
| `--dry` removes nothing | probe `case_dry` (**added this pass**) | `('dry', True, 0, True) PASS` |
| `release`/`sweep` never touch it | probe `case_transitions_untouched` (**added this pass**) | `('transitions untouched', True) PASS` |

The block was run the way `collect` runs it — awked out of the spec into
`bash -e -o pipefail -c`, from the code repo root — and exits 0, printing
all six lines and `PASS`.

**The check can fail.** With `resources/board/collect.py` reverted to `HEAD`
in the lane and nothing else changed, the same block exits 1 and every case
flips:

```
('done', True, 0, True) FAIL
('failed', True, 1, True) FAIL
('blocked', True, 1, True) FAIL
('container', True, 0, True) FAIL
FAIL
```

## Findings

Carried forward from pass one (its `## Build`, no `## Findings` of its own):
the four call sites it names are exhaustive — `grep -n 'transition_row('
resources/board/collect.py` returns exactly four call sites (2178, 2318,
2501, 2635) and `close_claims` follows each. Its `--dry` reasoning also
holds by reading: each site sits behind an `if opts.get("dry"): … return`
(2172 → 2179, 2314's `and not opts.get("dry")`, 2348 → 2502, 2598 → 2636),
so no dry guard was needed — and `case_dry` now checks it rather than
asserting it.

Three defects this pass found and closed, all inside the spec's own scope:

1. **A ticked box with no check.** `probe/verify.py`'s docstring claimed it
   "drives the four call sites", `main()` ran three: `close_container` was
   never exercised, and box 4 was ticked from reading. Added
   `case_container`, which builds a parent whose only child is `done` with
   a claim dir still on disk and drives `collect_one` into
   `close_container`. Docstring corrected to what `main()` runs.
2. **The verify block named a path from the wrong root.** It read `python3
   prds/<prd>/probe/verify.py`, and `collect` runs a verify block with
   `cwd` set to the **code repo** (`repo = repo_of(...)`, `collect.py:2276`,
   passed to `guarded_run`), not the board. From there `prds/` does not
   exist and the block would have died with every box ticked. Now
   `.pearde/prds/…`, the shape the sibling PRD
   `a-collect-stages-a-deleted-footprint-path-as-a-deletion` uses, with a
   comment naming the cwd. Run from that cwd: green.
3. **Boxes 5 and 6 had no runnable check either** — `--dry` and
   `release`/`sweep` were both read, not run. Two small cases now.

Worth knowing, **outside this scope, not fixed**: `close_container` only
ever meets an `open` PRD — `container()` (`collect.py:2552`) requires
`prd["state"] == "open"`, so that fourth site closes a PRD out of `open`,
not out of `claimed` as the contract's sentence reads. The removal there is
a no-op except on the dir a `release` left standing, which is what the
probe's fixture stages. Nothing in the contract's "must not change" list is
crossed by it, so the call stays.

Second, **the probe file is gitignored** (`.gitignore:61`, `prds/**/probe/`)
while every sibling probe on this board is tracked despite that rule
(`git add -f`). So this spec's verify block names a file that lives only on
this machine's disk, and the board's harness census never sees it. Left as
the analyst wrote it, deliberately: a tracked-but-ignored probe file is the
subject of the live PRD
`a-collect-does-not-stage-a-tracked-but-ignored-probe-file`, and staging
this one would walk into it.

## Baseline

The board holds 102 harnesses (103 by the second run — a neighbour landed
one mid-pass), past the count the atomic calls affordable, so the baseline
is a **selected set of 29**, run with `PEARDE_ROOT=<lane>`, selected as the
union of: every harness naming `collect.py`/`board/collect` (20), every one
naming `.claims` (10), and every board enumerator matching
`find.*verify\.sh` (6). One of the 29 —
`the-tree-holds-only-what-a-board-uses/the-documented-board-matches-the-code`
— does not read `PEARDE_ROOT`; its count is the checkout's and no flip on
it would have been claimed.

**13 of the 29 were red before the first edit** — recorded, not mine:

```
a-harness-measures-the-tree-its-worker-built-in · an-unknown-flag-refuses ·
graph-probe-makes-harness-sweep-unaffordable ·
collect-runs-the-invariants-and-red-refuses · the-line-tells-the-truth ·
one-prd-reading-primitive · every-module-finds-its-siblings-by-one-rule ·
the-fixtures-meet-the-tool · a-lane-is-removed-when-its-prd-collects ·
the-loop-is-commands · transitions-are-commands · the-gate-runs-the-harnesses ·
the-documented-board-matches-the-code
```

The pre-edit tree was recoverable — pass one's build is uncommitted and no
neighbour has hunks in `collect.py` (`git diff -U0 -- resources/board/collect.py`
is 16 added lines, one hunk set, all mine) — so this pass took a real
control rather than inheriting: `collect.py` restored from `HEAD` in the
lane, the same 29 re-run, then the build restored (verified with `cmp`).
**Every exit code identical, both runs.** Seven outputs differed textually;
all seven are board churn, none an edit of mine: `mktemp -d` paths (2),
fixture commit shas (1), timings (1), and a neighbour PRD
`doctor-walks-machine-local-lanes` appearing between the runs, which moved
`102 → 103` in the three census harnesses.

Gate, both trees, `PEARDE_ROOT=<lane>`:

- `python3 resources/index.py check` — **exit 1 before the first edit**, 27
  rows, identical with and without the build. 12 rows are the lane's sparse
  checkout (`/*`, `!/.pearde`) having no `docs/`; the rest are
  `purge.py`, `hotreload-test.js`, `zzdead`, `be`.
- `bash resources/doctor.sh` — **exit 1 before the first edit**, same rows
  with and without the build (`install`, four `memo … no such memo`,
  `questions broken`). Two lines differ between the two runs: the
  `statusline` dirty count (`*1` — this build's own uncommitted file) and
  the `questions` row, where a neighbour rewrote
  `the-file-index-is-green-so-a-spec-can-assert-it`'s question 1 mid-pass
  (3 rows → 2, different text). Neither is this footprint.

## Workflow probe-then-spec

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | read-the-contract | passed | contract, spec01 and pass one's report read; the contract's four terminals map to four call sites |
| 2 | capture-the-harness-baseline | passed | 29 of 102 selected, 13 red before the first edit, real control taken rather than inherited |
| 3 | attempt-the-build | passed | pass one's build stood; this pass added three probe cases and fixed the verify block's root |
| 4 | re-run-the-harnesses | passed | every exit code equal to the control's; the seven textual diffs are board churn, named above |
| 5 | write-the-specs | passed | second pass: no spec authored, `## Fails when` applied to the blocks that stood — two of its rows fired, two more are missing and are below |

### Edits

**write-the-specs** — `## Fails when` — add these two rows:

| a `## Verify and Proof` block names a board path from the board's own root — `prds/<prd>/probe/x.py`, `specs/spec01.md` — and passes when a worker runs it from the board | `collect` runs a verify block with `cwd` set to the **code repo**, never the board (`repo = repo_of(prd, board, board_root)` handed to `guarded_run`). On every layout this board ships on, the board is `.pearde/` *inside* that repo, so a board-rooted path does not exist from the cwd the block will actually run in, and the block dies with every box already ticked | spell every board path from the code repo root — `.pearde/prds/<prd>/…` — and run the block from there, the way collect does. A block that passes in the board dir and nowhere else has never been run as collect runs it |
| a box names a call site, function or path that the PRD's own probe never reaches — its `main()` runs fewer cases than its docstring lists | the box was ticked from reading the code, and a second pass on this route inherits the tick as if it were measured. `specced` reads the box, not what stands behind it | before ticking, name the case in the probe that closes each box, one to one. Where a site is expensive to stage, stage it anyway or leave the box open — an unrun box is the one thing a later pass cannot tell from a run one |

## Knowledge

`python3 resources/knowledge.py query "collect closes the claim dir it
measured against"` was already asked on pass one — no strong hit. Nothing
this pass needed came from outside this repo: every answer is in
`collect.py`, `schedule.py` and the board's own harnesses, all read
directly, so no `remember` is owed.

## Scores

complexity: 4
blast-radius: mid
workflow: probe-then-spec
