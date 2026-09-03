# a-conflicted-lane-is-reported-not-stranded — implementer report

Verdict: DONE

Both specs implemented and verified. spec01: 9 of 9 boxes closed, verify
block exits 0 in the lane. spec02: 7 of 7 boxes closed, verify block exits 0
in the lane. `python3 resources/pearde.py specced <prd> --check --as
impl-conflict-lane` — exit 0. 21 board harnesses re-run before and after the
final tree state: not one count moved.

## What this pass did

Second pass on the route (specs existed; the build already stood uncommitted
in the lane). Steps 1, 2, 4 and 5 were run; step 3 was not entered — every
spec's footprint is already modified in the tree (`git status --short` in the
lane lists exactly the four footprint files, HEAD `f8968fe` unchanged), so
per the route's second-pass row there was nothing to build. What this pass
added:

1. Re-wrapped one sentence in `references/parts/commits.md` — "never a
   stranded lane" had wrapped across a line break, so spec02's line-based
   grep needle could not see it. The rule did not move; only the wrap did.
2. Repaired spec02's `## Verify and Proof` block: two lines read
   `! grep -q …`, which `set -e` does not abort on (POSIX XCU 2.11 —
   measured: `bash -e -c '! true; echo survived'` prints `survived`), so
   those two checks could never fail the block. Rewritten to
   `if grep -q "…"; then exit 1; fi`. Then proved the block can fail both
   ways, restored, `cmp`-proved (see `### Edits`).
3. Ran every box's check and ticked it as it closed: 16 boxes, 16 checks run
   in this session, output quoted below.

## Verify output

spec01 block, run the way collect runs it from the lane root
(`bash -e -o pipefail -c "$(awk …)"`):

```
21 checks · 21 pass · 0 fail   (exit 0)
```

- `python3 -c "import lanes; assert issubclass(lanes.Conflict, lanes.LaneError)"`
  — passed; a direct construction asserts `branch`, `onto`, `files` carry
  what the caller passes, and `resources/board/lanes.py` passes
  `conflicts(repo)`'s list straight in, no re-parsing.
- `raise Conflict` sits on both conflict paths (`lanes.py:277` rebase,
  `:286` `--ff-only` merge); `collect.py:2063` re-raises `Conflict`,
  `:2065` still turns every other `LaneError` into a `Stop`, `:2221`
  catches it in `collect_one` → `block_conflict`.
- Probe sections A1/B1/B2/B3/C1 cover: exit 1 with the conflict and file
  named on stderr; checkout never moved; lane branch holds the worker's
  commit; lane tree clean; PRD `blocked`, no `claim:`, `## Blocked` naming
  `src/util.py` and `lane/finished`; scan line `blocked` + "waiting on
  you"; `unblock` exits 0 and lands `specced`; the no-conflict collect
  reaches `done` with the worker's code landed and no `## Blocked`.

spec02 block, same invocation: `spec02 ok`, exit 0. `mapfile.py check`
silent, exit 0.

Both blocks run verbatim from the orchestrator's checkout exit non-zero —
spec01 at `module 'lanes' has no attribute 'Conflict'`, spec02 at the
banned-phrase grep. That is the red-to-green flip shown against the tree
that does not hold the build.

## Mutations (the checks can fail)

Each mutation: copy to scratch outside the repo, mutate, run block, restore,
`cmp` proved.

| spec | mutation | block exit |
|---|---|---|
| spec01 | `class Conflict(Exception):` (subclass broken) | 1 — AssertionError in the block's own assert |
| spec02 | `a person merges it by hand.` appended to commits.md | 1 — the `if grep …; then exit 1` fires |
| spec02 | "a lane that will not rebase" → "…reb@se" in states.md | 1 — `grep -q` line fails under `set -e` |

spec01's mutation is counter-wiring; the behavioural side is the probe's own
red on a tree without the change (analyst: 12 of 21; this pass: the block
verbatim on the checkout fails before the probe runs).

## Workflow probe-then-spec

| # | atomic | outcome | note |
|---|--------|---------|------|
| 1 | read-the-contract | passed | both `@` cites resolve; git status recorded in lane and checkout before any edit |
| 2 | capture-the-harness-baseline | passed | baseline inherited and confirmed — see below |
| 3 | attempt-the-build | passed | not entered: both specs' builds already stand in the tree (second pass); nothing this run wrote outside the four footprint files and the PRD folder |
| 4 | re-run-the-harnesses | passed | 21 harnesses, same order, same `PEARDE_ROOT`, same symlink state; every count equal to its baseline |
| 5 | write-the-specs | passed | second pass: no spec authored; fails-when applied to the standing blocks — spec02's dead `!` lines repaired and mutation-proven |

### Edits

**probe-then-spec** — step 5, `## Verify and Proof` of
`specs/spec02.md` — the two `! grep -q` lines are dead under `set -e`
(the `## Fails when` shape "a block line reads `! <cmd>` … leaves the
block at exit 0", measured, not assumed). Replacement for the block's
opening, paste-ready:

```sh
set -e
if grep -q "a person merges it by hand" references/parts/commits.md; then exit 1; fi
```

(the second `!` line guarded the same file; after the edit the remaining
five `grep -q` lines abort correctly under `-e`, proven by mutation B.)

**probe-then-spec** — step 5 do-4, `references/parts/commits.md` — the
needle "never a stranded lane" fails on a kept sentence re-wrapped across
two lines. Re-wrapped so the sentence reads whole on one line; the rule
did not move:

```
**A merge conflict is a reported PRD, never a silent stage and never a stranded lane.** When the lane disagrees with what landed in the checkout
```

## Harnesses — baseline inherited and confirmed

The pass-one report published counts for the set "every board harness whose
script names `collect.py` or `lanes.py`". The set was re-derived the same
way — 21 harnesses (`grep -l -E 'collect\.py|lanes\.py'` over
`find prds -name verify.sh`) — and run twice this pass, before and after the
edits, both with `PEARDE_ROOT=<lane>` and with the live board symlinked at
`<lane>/.pearde` (created before the first count; the symlink state is
beside every count). Baseline vs re-run, lane tree:

| harness | baseline | re-run |
|---|---|---|
| a-lane-s-wiki-is-a-stub-… | 19 · 18 pass · 1 fail | 19 · 18 pass · 1 fail |
| a-verify-block-must-not-destroy-the-checkout-it-runs-in | 24 passed, 0 failed | same |
| board-rel-is-a-third-wrong-board-path-resolution | 0 check(s) failed | same |
| collect-must-not-reset-the-checkout-it-did-not-write | 31 · 31 · 0 | same |
| collect-resolves-a-board-path-two-ways-and-both-are-wrong | 7 · 7 · 0 | same |
| collect-stages-a-shared-file-whole | 32 passed, 0 failed | same |
| filing-refuses-a-file-it-does-not-hold | 52 · 52 · 0 | same |
| **this PRD's probe** | 21 · 21 · 0 | same |
| collect-runs-the-invariants-and-red-refuses | 12 FAIL | same |
| nothing-left-open/the-line-tells-the-truth | 85 · 81 · 4 | same |
| post-report-crashes-a-collect-… | 75 · 75 · 0 | same |
| every-file-sits-under-what-it-is-responsible-for | 19 passed, 29 failed | same |
| every-module-finds-its-siblings-by-one-rule | 3 passed, 20 failed | same |
| a-lane-is-removed-when-its-prd-collects | 33 · 21 pass · 12 fail | same |
| the-board-runs-itself/collect-is-a-command | 133 · 133 · 0 | same |
| the-board-runs-itself/hunks-land-where-they-came-from | 47 · 47 · 0 | same |
| the-brief-names-the-verdict-line-collect-requires | 15 ok · 0 FAIL | same |
| the-collect-and-brief-harnesses-are-carried-across-the-layou | 7 · 7 · 0 | same |
| the-tool-keeps-its-word/collect-keeps-its-word | 101 · 101 · 0 | same |
| the-verify-guard-parses-git-s-own-output-before-it-trusts-it | 46 passed, 0 failed | same |
| workflows-on-the-board/workflow-improve | 62/71 pass | same |

Every count equals both its baseline and, where published, the pass-one
report's lane column — the inherited baseline is confirmed, and no count
moved across my edits. HEAD of lane and checkout unchanged throughout
(`f8968fe` / `e55a0e7`).

Two of the set were not in pass one's table and carry no published count:
`every-file-sits-under…` (19/29) and `a-lane-is-removed-when-its-prd-collects`
(21 pass / 12 fail). Both were run against the checkout tree too and fail
**identically** there (19/29 and 33 · 21 · 12) — pre-existing, not this
unit's: the first's failing lines name the layout-migration work
(`the cut runs — 7 directories, board/ emptied`, preamble-reach classes),
the second's name lane-removal after a clean collect, a path this PRD does
not touch (its no-conflict collect is green in this PRD's own probe, C1).

Repo gate, both roots, before first edit: `python3 resources/index.py check`
exit 1 with four lines, byte-identical in lane and checkout —
`resources/common.py is on disk with no row in references/files.md`,
`references/files.md lists @resources/board/hotreload-test.js — not on
disk`, `@@view names @resources/board/hotreload-test.js — not on disk`,
`references/parts/commits.md references @pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md — not on disk`.
All four inherited: the memo is absent in the checkout too and the reference
predates this pass (the lane diff does not touch that line).
`bash resources/doctor.sh` in the lane — red rows `index`, `vault`,
`origin`, `health`, `knowledge`, all inherited and none naming a footprint
file; `statusline` excluded (dirty-count row). The memo's own invariant
script `bash resources/invariants/a-board-s-own-file-commits-in-the-board-repo.sh`
— exit 0, all pass, run directly because the memo's `memo verify` cannot
resolve a lane.

## Findings

Carried forward from pass one (analyst report, this same file) — all still
true at close, re-checked where cheap:

- **The sibling holds three of these four files.**
  `collect-runs-the-invariants-and-red-refuses` was `claimed` at pass one;
  its footprint names `collect.py`, `commits.md`, `states.md`. Whichever of
  the two lands second rebases onto the first — this PRD's own mechanism
  will be exercised by that rebase if it conflicts, and the board will now
  say so instead of stranding it.
- **`lane` and `unblock` are not in the board's grammar.** Re-checked this
  pass: `python3 resources/grammar.py show lane` and `… show unblock` both
  still answer "is not defined on this board".
- **The grammar's `blocked` row goes stale when spec01 lands** — a
  conflicted lane is `blocked` with no `needs:` waiting on a person.
  spec02 corrects the same claim in `states.md`; the grammar row itself is
  a board file under another skill's rules, named not edited.
- **`resources/install.sh --check` prints `usage: dirname string [...]`**
  when `CLAUDE_CONFIG_DIR` is unset — predates this PRD, outside footprint.

New this pass:

- **Three PRDs landed on the board mid-run** (`a-harness-never-dispatches-the-live-board`,
  `one-command-works-the-busiest-board-on-the-machine-from-any`,
  `upgrade-says-two-contradictory-things` — untracked at the time of
  writing) and one new harness appeared after the baseline set was taken:
  `the-board-reclaims-dead-work-by-itself/a-worker-survives-the-window-that-launched-it/probe/verify.sh`.
  Run once for the record — it errored inside its own fixture
  (`FileNotFoundError … /tmp.Wh4AFYJggm/detach/heart` from a `python3 -c`
  line writing a file in a directory the script had already removed). Not
  compared to anything; no baseline exists. The defect is that harness's
  own and is reported for its owner.
- **`specced --check` warns "9 of 9 boxes already ticked before an
  implementer ran them".** Expected shape on this route: the brief orders
  ticking as each box closes, so the check — run at the end — always sees
  them ticked. Exit 0, set accepted (complexity 12, footprint union four
  files).
- **spec02's verify block was authored with the `!` shape the workflow's
  own fails-when table calls unfixable-by-set-e** — recorded under
  `### Edits` so the next brief carries the corrected line; the block now
  fails on both mutation classes it guards.

## Housekeeping

- Nothing learned outside this repo; nothing written with
  `knowledge.py remember`. Pass one enqueued nothing to `.pearde/wiki/pending/`;
  this pass enqueues nothing either.
- The scratch tree for this run lives outside the repo at
  `/tmp/pearde-impl-conflict-lane/` (baseline and rerun outputs per
  harness, gate outputs, mutation backups).
- The lane's `.pearde` symlink (board gitignored there) was created to let
  spec01's block resolve `.pearde/prds/…` from the lane; both baseline and
  re-run ran with it in place, so no count above carries the symlink
  difference.
- Nothing was committed. The four footprint files stand uncommitted on
  `lane/no-work-is-lost-on-the-board-a-conflicted-lane-is-reported-not-stranded`
  for `collect`'s `land_lane` to commit and merge — committing is not the
  implementer's act. The checkout has no uncommitted hunks in any footprint
  file, so the merge has no three-way hazard; if the sibling lands first
  with hunks in `commits.md`/`states.md`/`collect.py`, the conflict is
  exactly what this PRD's mechanism now reports.
- Health floor: the brief lists none under the floor; nothing moved.
