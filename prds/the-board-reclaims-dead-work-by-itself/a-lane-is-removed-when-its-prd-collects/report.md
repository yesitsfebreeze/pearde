Verdict: DONE

Second pass of `probe-then-spec` — the analyst's pass built both units and
wrote the specs; this pass ran every box against the build, found and fixed
one real defect in it, and closed the two shapes `write-the-specs` refuses.

- specs: `spec01` 5/5 boxes ticked, `spec02` 4/4 — each with the check that
  closed it quoted in the box.
- probe: `spent_test.py` **30 checks, 0 failures** (was 21 — this pass added
  9), `verify.sh` **33 checks · 33 pass · 0 fail**.
- repo gate: `index.py check` byte-identical to the baseline (3 problems,
  all pre-existing); `doctor.sh` no row flipped state.
- neighbours: 16 board harnesses besides this PRD's name
  `resources/board/lanes.py` or `collect.py`; all 16 run against the built
  lane, 3 red and **all three red in a pre-edit control worktree at the
  lane's own HEAD** — pre-existing, none this footprint's.

## What this pass changed

1. **`lanes.dirty` read the wrong shape of `git status`.** Box 2 of `spec01`
   had no check at all in the probe. Writing one found the defect on its
   first run:

       FAIL dirty only inside feet is spent (exact foot): (False, '1 uncommitted: src/')

   Plain `--porcelain` collapses an untracked directory to one entry ending
   `/`, so a lane whose only standing bytes are new files **inside** a
   footprint directory reads as a path outside it, and the lane is kept for
   work that is entirely its own — box 2's exact case, and the same read
   `collect.py`'s `inside(p, feet)` makes at line 2046. The human form also
   quotes any path holding a space, handing the quotes to the caller as part
   of the name. `dirty()` now reads `--porcelain -z -uall` and skips a
   rename's second (old-name) record. Six probe checks back it, each of
   which was red or wrong before the fix.

2. **Both `## Verify and Proof` blocks were unrunnable.** They opened
   `LANE="<the lane or checkout holding this unit's build>"` — a literal
   placeholder. `collect` runs these blocks under `bash -e -o pipefail`, so
   both specs would have died at collect time with every box ticked. They now
   open `LANE="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute
   --git-common-dir)")}"`: the env override a worker in a lane sets, and
   otherwise the code repo absolutely, from a linked worktree as well as from
   the checkout. Both blocks run green end to end (`rc=0`).

3. **Each block now names a path under its own footprint.** `pearde specced
   --dry` warned `the verify block names no path under the footprint — the
   whole-workspace smell` on both; one `grep -qF` per block on the code the
   unit contracts closed it. `specced --dry` now warns only about the ticked
   boxes, which is this pass's own doing.

Nothing in `resources/board/collect.py` needed changing: `spec02`'s build
stood as written and its four sections were green on the first run.

## The PRD's question — how many stale lanes, and whose job

Measured read-only against the live board this pass, with the built command:

    python3 <lane>/resources/pearde.py lanes --board /Users/feb/dev/infra/pearde/.pearde
    lanes: 33          25 spent · 8 kept

Cross-read against `plan.scan`, by the state of the PRD each slug belongs to:

| verdict | PRD state | lanes |
|---------|-----------|-------|
| spent | `claimed` | 24 |
| spent | `analyzing` | 1 |
| kept | `claimed` | 2 |
| kept | no PRD holds the slug | 6 |

**Zero** of the 33 belong to a `done` PRD. The PRD's 26 stale `done` lanes are
gone — collected or swept since it was written — so the answer to "how many
of the 26 would this clean" is, today, none: there is no `done` backlog left
to clean. `collect` dropping its own lane is what keeps it at zero from here.

**Cleaning the backlog is a one-off command, not this PRD's job, and it must
not be run on a busy board.** All 25 lanes `spent` calls droppable right now
belong to PRDs still `claimed` or `analyzing` — workers dispatched in this
same round whose lane simply has nothing in it yet. `spent` is two checks and
nothing else by contract, so an empty freshly-cut lane is indistinguishable
from a finished one, and `pearde lanes --apply` would remove all 25 out from
under live workers. I did not run it. See finding 3 below.

## Findings

Findings 1, 3, 4 and 5 are carried forward from the analyst's pass by name;
finding 2 of that pass is resolved and recorded as such.

1. **This PRD's claim never cut a lane** (carried forward). The claim line was
   seeded straight into `prd.md` frontmatter, bypassing `pearde claim`, so
   `cut_lane` never ran; the analyst cut the lane by hand with
   `lanes.create`. Every sibling PRD claimed in that batch shows the same
   gap. The lane the brief names exists and holds the build; nothing here
   re-cuts it.

2. **The checkout's `plan.py` merge conflict is resolved** (carried forward,
   now closed). `grep -c '<<<<<<<' /Users/feb/dev/infra/pearde/resources/board/plan.py`
   → `0`. `probe/census.py`, which hardcodes that path, is usable again.

3. **`pearde lanes --apply` is safe by contract and unsafe by timing.** It
   removes exactly what `spent` clears, and `spent` cannot see the difference
   between "this worker finished and merged" and "this worker was dispatched
   ninety seconds ago and has not typed yet". On this board that is 25 live
   lanes. The command is built, probed and read-only by default; running it
   is a decision for a quiet board. A guard — skip a lane whose PRD is
   `claimed`/`analyzing` and whose claim is younger than the reap grace — is
   a follow-up PRD, not a change I may make: `spec01` fixes `spent` at two
   checks and says so.

4. **A stale claim in `transitions.py`** (carried forward, still open).
   `drop_lane`'s docstring at `resources/board/transitions.py:987` says
   "`sweep` is the ONLY edge that drops a lane." `collect` and `pearde lanes
   --apply` are now two more. Outside this PRD's footprint; not fixed.

5. **`probe/backlog.py` disagrees with `pearde lanes` on an orphan slug**
   (carried forward). `backlog.py` always reports a slug no PRD claims as
   `kept — no PRD holds this slug`; `verify.sh` section E and the shipped
   command check it with the same `spent` predicate. Six such slugs are on
   the board today and all six read `kept` for other reasons, so the two
   agree by accident right now. `backlog.py` is read-only and unmodified.

6. **The placeholder verify block is board-wide, not just here.** `grep -rh
   '^LANE=' .pearde/prds` finds `LANE="<the lane or checkout holding this
   unit's build>"` in **5** spec blocks. Two were this PRD's and are fixed;
   the other three are other PRDs' and will die the same way when `collect`
   runs them. Reported, not touched.

7. **Three board harnesses are red and were red before this pass.** All
   three re-run against a control worktree at the lane's own HEAD
   (`git worktree add --detach <scratch>/control 1be5d2b`) with output
   identical to the built lane's, line for line:
   `resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule`
   → `FAIL no launcher spells board/ any more — want '0', got '1'` ·
   `probe: 22 passed, 1 failed`;
   `no-work-is-lost-on-the-board/collect-runs-the-invariants-and-red-refuses`
   → `12 FAIL`; and `nothing-left-open/the-line-tells-the-truth` →
   `85 checks · 81 pass · 4 fail`, the four being `A12 --as engineer lands`,
   `A13 …▸ finished: claimed → done`, `A14 …as engineer last`,
   `A15 state: done`. None is this footprint's.

9. **`nothing-left-open/the-line-tells-the-truth` hangs under a concurrent
   harness sweep.** Run inside a 16-harness loop while other sessions were
   running harnesses on this machine, it stopped dead at
   `ok F3 the sentinel daemon is up on its port` and wrote nothing for over
   three minutes; run alone afterwards it finished in under four. Its
   sentinel port is shared with whatever else is up, which makes its result
   a matter of scheduling — `attempt-the-build`'s row for a neighbour
   harness decided by its own hard-coded port. I did not edit it; it is
   reported here for its owner, and both runs above are the alone ones.

8. **The repo gate is red at the baseline and unchanged by this pass.**
   `index.py check` prints the same 3 problems before and after
   (`resources/common.py` has no row in `references/files.md`;
   `references/files.md` and `@@view` both name
   `@resources/board/hotreload-test.js`, not on disk). `doctor.sh`'s `index`
   (3) and `claims` (6) rows are broken at the baseline too. Every number
   that moved between the two doctor runs — 224→226 PRDs, 96→97 harnesses,
   `*13`→`*16` — is other sessions landing work on the live board.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | pass. `prd.md`, both specs, the analyst's `report.md` and the four probe files read. Footprint: `resources/board/lanes.py` and `resources/board/collect.py`, both present in the lane and both already modified — the row in `attempt-the-build`'s table for a route's **second** pass. `git status --short` recorded in the lane (2 modified) and in the checkout (11 modified, 2 untracked) before the first edit |
| 2 | `capture-the-harness-baseline` | pass. `spent_test.py` 21 ok / 0 fail and `verify.sh` 33/33 on the standing build — equal to the counts the analyst published, which is the atomic's own cheaper confirmation. `index.py check` (3 problems) and `doctor.sh` (index broken, claims broken) recorded red before the first edit. 16 neighbour harnesses named the footprint; all 16 run |
| 3 | `attempt-the-build` | entered for **`spec01` only**. Both footprints already carried a build, so the `Fails when` row for a second pass applies; `spec02`'s build stood unchanged and this pass wrote nothing in `collect.py`. In `spec01`, writing box 2's missing check reddened it and `dirty()` was fixed |
| 4 | `re-run-the-harnesses` | pass. `spent_test.py` 30/30, `verify.sh` 33/33 after the fix. Repo gate byte-identical on `index.py check`, no doctor row flipped. Every neighbour that had been run before the `dirty()` fix re-run after it, same counts. Three red neighbours proved pre-existing against a control worktree at the lane's HEAD |
| 5 | `write-the-specs` | pass, applied as the second-pass reading: no spec authored, the `Fails when` table applied to the blocks that stand. Row 121 (`<placeholder>` argument) and the whole-workspace warning both fired and are fixed; row 115 (a previous pass's report at this path) obeyed — its findings are carried forward above by name. Row 118 checked: neither block asserts a literal probe total, so adding 9 checks reddened nothing |

### Edits

Two failures the atomics caused, with replacement text.

**`attempt-the-build`, `## Fails when` — a new row.** The table already
carries darwin rows for `touch` and `sed`; `timeout` is the same class and
cost this run a whole 16-harness sweep, killed at the tool's own deadline
with no result recorded.

| `bash: timeout: command not found` when a sweep wraps each harness | GNU coreutils `timeout` is not on **darwin**; a bare `timeout 300 bash <h>` fails every harness at once and the sweep reads as 16 reds that never ran | drop the wrapper and run the sweep in the background (`run_in_background`), or `gtimeout` where coreutils is installed. Never read a sweep whose first line is `command not found` as a measurement |

**`write-the-specs`, `## Fails when` — replacement text for the
`<placeholder>` row.** As written the row says the block "dies on a syntax
error"; the shape that actually stands in 5 spec blocks on this board is
`LANE="<the lane or checkout holding this unit's build>"`, **quoted**, which
is valid shell, assigns the placeholder as a literal, and fails much later
with a path error naming the placeholder. The row's `do` column should name
the fix, since every block needs the same one.

| a `## Verify and Proof` block reads as instructions to a person — a `<placeholder>` argument, a `# note the dir` comment standing in for a value, a bare `$?` echoed after the command it describes | the block was written to be *read* and never run, and `collect` runs it: unquoted, `<that dir>` is parsed as a redirect and the spec dies on a syntax error with every box already ticked; **quoted — `LANE="<the lane holding this unit's build>"` — it is valid shell that assigns the placeholder as a literal string, and the block dies later on a path error naming it, which reads like a broken build rather than a spec that was never run** | write the value the block needs, resolved: `LANE="${PEARDE_ROOT:-$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")}"` — the env override a worker in a lane sets, else the code repo absolutely, correct from a linked worktree as well as from the checkout. Then run the block as `collect` will: `bash -e -o pipefail <extracted block>` |

## Health

No file in the footprint is under the health floor — `doctor.sh` reports
`6 under 40` at the baseline and `6 under 40` after, and neither
`lanes.py` nor `collect.py` is among them. `lanes.py` grew 154 lines across
this pass and the analyst's; it is one module with one subject and was not
split — a split would be a refactor outside the spec's scope.

## Scores

complexity: 24
blast-radius: mid
workflow: probe-then-spec
