# report — collect commits only the PRD's own edits, not the footprint's

verdict: **DONE** · specs 2/2 · boxes 7/7 · workflow `probe-then-spec`

## Box status

| spec | box | evidence |
|------|-----|----------|
| spec01 | 1 — `run.sh 1` refuses, dry and real, HEAD unmoved, `prd.md` untouched | `1a 1b 1c 1e 1f 1g 1h 1d` all PASS |
| spec01 | 2 — the message names the sibling and `--widen <path>` | `1i-widen-offered`, `5c-widen-offered` PASS |
| spec01 | 3 — `run.sh 1 5` refuses an untracked sibling file, not added whole | `5a 5b 5c 5e 5d` PASS |
| spec01 | 4 — `run.sh 3` control still lands this PRD's own edits | `3a 3b 3c 3d` PASS |
| spec02 | 1 — `run.sh 2` widen finishes, `widened shared.py`, commit whole | `2a 2b 2d 2e` PASS |
| spec02 | 2 — `run.sh 4` analyzing sibling not refused, the gap stands | `4a-gap-persists` PASS |
| spec02 | 3 — `index.py check` and `memos.py check` both exit 0 | both `exit: 0` |

## Verify output

spec01's block, run verbatim under `bash -e -o pipefail`:

```
PASS 1a-dry-refuses      PASS 1i-widen-offered   PASS 1b-dry-exit
PASS 1c-no-commit        PASS 1e-real-refuses    PASS 1f-real-exit
PASS 1g-nothing-written  PASS 1h-state-held      PASS 1d-snapshot-exists
PASS 3a-dry-ok           PASS 3b-dry-adds        PASS 3c-real-ok
PASS 3d-committed        PASS 5a-untracked-refused
PASS 5c-widen-offered    PASS 5b-dry-exit        PASS 5e-real-exit
PASS 5d-not-swept
---- 18 passed, 0 failed · run.sh exit 0 · probe exit: 0 · BLOCK EXIT: 0
```

spec02's block:

```
PASS 2a-widen-collect  PASS 2b-widen-in-message  PASS 2d-committed
PASS 2e-commit-whole   PASS 4a-gap-persists
---- 5 passed, 0 failed · run.sh exit 0 · probe exit: 0 · BLOCK EXIT: 0
```

Whole fixture: **21 passed, 0 failed**.

Harnesses: `python3 resources/index.py check` exit 0, `python3
resources/memos.py check` exit 0.

## What this pass changed

Pass one left the guard built and unproven. Three defects the fixture run
exposed, all fixed:

1. **`probe/run.sh` could never fail.** Its last two lines were
   `[ "$FAIL" -eq 0 ]; echo "run.sh exit $?"` — `echo` is the last command, so
   the script exited 0 with any number of failures, and both specs' verify
   blocks were green by construction. Replaced with an explicit `exit 0` /
   `exit 1`. Proven: the mutation run below returns 1.
2. **Eleven assertions were invisible.** `[ cond ] || report no …` counted a
   failure but never a pass, so `1b 1c 1f 1g 1h 3a 3c 5b` and the widen and
   not-swept checks never appeared. A new `is <name> <got> <want>` helper
   counts both ways; `2a` gained its `report ok`. Pass count went 10 → 21.
3. **Two boxes had no check behind them.** spec01 box 2 (the `--widen <path>`
   half of the message) and spec01 box 3 (`not added whole`) were asserted by
   no line. Added `1i-widen-offered`, `5c-widen-offered`, `5e-real-exit` and
   `5d-not-swept` — the last needing a real collect in scenario 5, which the
   fixture ran only dry, where nothing is staged either way and the check
   could not discriminate.

Plus the shadow the round flagged: `sort_paths`'s `others` loop bound a local
`feet` over the parameter `feet`. Harmless where it stood — the parameter's
last read is the `groups` loop, above the rebind — but a future read below it
would take the wrong list silently. The local is now `claimed`, and the
comprehension variable in the refusal with it. Behaviour unchanged; the
fixture is green either way.

`COLLECT` in the fixture is now `${COLLECT:-<abs path>}`, so the same
scenarios can be aimed at a mutated copy.

## Mutation proof — the guard is what makes the fixture green

The whole `resources/` tree copied to a temp dir, the `if not predates(…)`
refusal block cut out verbatim, the fixture aimed at it with `COLLECT=`:

```
---- 12 passed, 10 failed · run.sh exit 1
FAIL 1a-dry-refuses       FAIL 1i-widen-offered  FAIL 1b-dry-exit (got 0, want 1)
FAIL 1e-real-refuses      FAIL 1f-real-exit      FAIL 1h-state-held (got 0, want 1)
FAIL 1g-nothing-written   got [42bb648…], want [c1d942f…]
FAIL 5a-untracked-refused FAIL 5c-widen-offered  FAIL 5b-dry-exit
FAIL 5e-real-exit         FAIL 5d-not-swept  the sibling's untracked file was committed
```

Scenarios 2, 3 and 4 stay green without the guard — it changes nothing on a
path no sibling's footprint holds. Without it, `prds-a` commits `prds-b`'s
`shared.py` hunk and `prds-b`'s untracked `shared/new.py`, and writes itself
`done`. That is the bug this PRD names.

## Regression — the collect-touching harnesses

Nineteen `verify.sh` under `.pearde` mention `collect`; each run serially with
the guard in. **16 green, 3 red**, and every red is another PRD's uncommitted
work in the same tree, none naming collect:

| harness | why | owner |
|---------|-----|-------|
| `the-board-runs-itself/the-loop-is-commands` | `loop.md is 173 lines`, `the eight-row table — got '9'` | `references/parts/loop.md`, dirty |
| `the-board-runs-itself/transitions-are-commands` | `pearde claim: refused — asking 4 — drill first` | board state + `questions.py`, `transitions.py`, dirty |
| `the-board-runs-itself/readme-in-three-rings` | doctor not green — the `origin` row | pre-existing, below |

Every collect-specific harness is green: `collect-keeps-its-word`,
`collect-is-a-command`, `hunks-land-where-they-came-from`,
`the-collect-and-brief-harnesses-are-carried-across-the-layou`,
`list-the-collects-the-repo-bug-orphaned`.

`the-line-tells-the-truth` went red once under 19-way parallelism and green
serially — harness cross-talk over shared temp state, not this change.

## Findings — outside this PRD's scope, not fixed

- **`doctor.sh`'s `origin` row is broken and is not this PRD's.** `6 derived
  in flight vs 4 requested`. Standing before this build, unchanged by it. It
  is the only broken row left, and it is what keeps `readme-in-three-rings`
  red.
- **`doctor.sh --harnesses <repo>` prints no `harnesses` row.** Two runs, with
  and without the repo argument, ended at the `plan` row; the `harnesses` and
  `jstests` rows never appeared, and doctor exited without them. The 43
  harnesses fork at `doctor.sh:674` under `wait`. `doctor.sh` is dirty with
  another PRD's work, so this may be theirs mid-edit — reported, not touched.
- **`index.py check` was red on `resources/board/orphans.py` (no row in
  `references/files.md`) for part of this run**, an untracked file another
  agent created at 00:31. It went green on its own when that agent added the
  row. Nothing to do; noted so the sequence is on record.
- The three findings pass one recorded still hold, unchanged and unfixed: the
  claim baseline never covers code on a nested board (`snapshot()` measures
  the board repo), `--widen` with a relative path resolves against the board
  root and not the code repo, and `predates()` with no baseline falls back to
  whole-file mtime.

## The recorded gap

An `analyzing` sibling with no specs and no `footprint:` frontmatter is
invisible to the refusal and still sweeps — scenario 4, green by design. A PRD
declares its footprint at `specced`; before that there is nothing to attribute
against. Closing it needs footprints to exist earlier: a different contract,
not work this PRD may take.

## Knowledge

No fact from outside this repo was learned — every question this pass raised
was answered by running the tree's own code. Nothing to `remember`.

## Footprint touched

- `resources/board/collect.py` — the guard (31 lines, from pass one) plus the
  `feet` → `claimed` rename
- `.pearde/prds/collect-commits-only-the-prd-s-own-edits-not-the-footprint-s/`
  — `probe/run.sh`, both specs' boxes, this report

Nothing else in the tree was written, staged, stashed or reverted.
