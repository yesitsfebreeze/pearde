# report — the sweep runs between passes

worker: impl-sweep-between · persona: engineer · pass two (implementer)
board: /Users/feb/dev/infra/pearde/.pearde · lane: .pearde/.lanes/the-board-reclaims-dead-work-by-itself-the-sweep-runs-between-passes

Verdict: DONE

specs 1/1 · acceptance 6/6 ticked · probe 11 checks, 11 pass, 0 fail, three
runs in a row · regression 74 checks, 67 pass, 7 fail, the same 7 as the
pre-edit tree.

## What this pass did

The build the first pass left standing was correct and is unchanged in
substance. This pass closed the three acceptance boxes it had no standing
check for, and removed a neighbour's work that had been copied into the
lane by mistake.

1. **Stripped a live neighbour's hunks out of the lane.** The lane's
   `resources/board/serve.py` carried `ask_digest()`, `Board.ask_stamp`
   and the watch-loop block that reads them — 23 lines belonging to
   `the-board-reclaims-dead-work-by-itself/a-fork-reaches-the-user-when-it-is-written`,
   whose spec01 footprint is the same file and whose worker
   `impl-fork-reaches` is claimed and building **in the checkout right
   now** (`git status` names `resources/board/serve.py` dirty there, 23
   insertions, all `ask_*`). Pass one's report says how they got in: it
   built in the checkout, then copied *the checkout's whole uncommitted
   `serve.py` diff* into the lane, which swept the neighbour's in-flight
   work along with its own. Left alone, this lane would have carried a
   stale copy of another PRD's unit into `collect`. Removed; the lane's
   diff is now exactly this unit — `SWEEP_S`, `Board.last_sweep`, the
   guarded `tick_sweep` call, and
   `transitions.claim_liveness`/`tick_sweep`. See **Findings**.
2. **Extended `probe/tick.sh` from 7 checks to 11**, closing acceptance
   boxes 4 (second half), 5 and 6, which no check covered.
3. Re-ran everything after both edits.

## Acceptance, box by box

- **box 1 — `claim_liveness` verdicts.** Run directly against the lane's
  module: `dead : ('dead', 'pid 79457 is gone')` · `alive : ('alive',
  'pid 79455 running since Thu Sep  3 17:53:45 2026')` · `name :
  ('unknown', 'claim names no process — mtime is all there is')`, the
  same `unknown` for `''` and `None`. `impl-sweep-between` — the shape
  `pearde claim` writes today — is the `name` case.
- **box 2 — only DEAD is reclaimed.** Probe checks 1–3: `dead holder:
  the claim was reclaimed with no pass open — state failed` · `live
  holder: silent past claim-ttl and left held — mtime alone does not
  reclaim` · `claim naming no process: left held — unknown never
  reclaims`. All three fixtures are stamped `202001010000` against a
  `claim-ttl: 1m`, so every one of them is silent past the ttl and only
  the dead pid moves.
- **box 3 — the lane is committed before it is dropped.** Probe checks
  4–6, and the daemon log names the order:
  `serve: sweep: a-held-prd uncommitted path(s) committed as 8012aa36d2fe`
  then `serve: sweep: a-held-prd lane removed · branch lane/a-held-prd
  kept`. The bytes are recovered after the worktree is gone with
  `git show lane/a-held-prd:src/b.py` and `…:src/a.py`.
- **box 4 — `## Failure` names the kept branch, the log says so.** Probe
  checks 7–9; checks 8 and 9 are new this pass. Check 8 reads the
  `## Failure` section itself for `lane/a-held-prd` rather than only for
  the heading; check 9 asserts the log line
  `pid 53794 is gone — reclaiming without a pass`.
- **box 5 — `SWEEP_S` defaults to 0 and ticks nothing.** Probe check 10,
  new: a fourth fixture, dead pid, silent since 2020, watched by a daemon
  started with `env -u PEARDE_SWEEP_S` — state stays `claimed`, log holds
  no `reclaiming without a pass`. **Negative control** (the check can
  fail): the identical fixture under `PEARDE_SWEEP_S=2` gives
  `state: failed reclaims=1`.
- **box 6 — a raise is logged and the loop survives it.** Probe check 11,
  new: two boards, the bad one registered first, its `prd.md` `chmod 000`
  so `tick_sweep` raises `PermissionError` (verified it does before the
  check was written). The log:

      serve: sweep tick on tmp.MzE8bQhICC raised PermissionError(13, 'Permission denied')
      serve: a-held-prd · claimed · claim s6903 … — reclaiming without a pass
      serve: sweep: a-held-prd uncommitted path(s) committed as 961dbccb0923
      serve: sweep: a-held-prd lane removed · branch lane/a-held-prd kept
      serve: sweep tick on tmp.MzE8bQhICC raised PermissionError(13, 'Permission denied')

  — the second board was swept after the raise, and the bad board raised
  again a tick later, so the loop kept both.

## Verify and Proof

Three runs in a row, from the lane, after the strip and the extension:
`11 passed, 0 failed` · `11 passed, 0 failed` · `11 passed, 0 failed`,
exit 0 each time. Three earlier runs of the unextended probe after the
strip gave `7 passed, 0 failed` each — the strip changed no behaviour.

Pass one reported one 2-pass/5-fail run out of nine under load. It did not
recur in the six runs here (three at 7, three at 11).

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | ok — PRD, spec01, pass one's report; second pass on this route, so step 3 re-measures and step 5 applies `Fails when` to the blocks that stand rather than authoring a spec |
| 2 | capture-the-harness-baseline | ok — see Harnesses |
| 3 | attempt-the-build | ok — no back-edge taken |
| 4 | re-run-the-harnesses | ok — no count moved against its own pre-edit baseline |
| 5 | write-the-specs | ok — spec01 stood; ticked its six boxes and corrected its `Verify` count from 7 to 11 for the checks this pass added |

### Edits

None. No atomic named a wrong command, a stale path, a check that cannot
fail, or a shape its `## Fails when` does not list.

## Harnesses

23 of the board's 97 `verify.sh` name a footprint path; all 23 honour
`PEARDE_ROOT` (`grep -L PEARDE_ROOT` over the set returns nothing), so
every count below is the lane's, not the checkout's.

Baseline taken **before the first edit** of this pass, as a real pre-edit
tree — the earlier build is uncommitted in a lane, so
`git clone --shared <lane> <scratch>/pre` is the lane's own `HEAD`:

| harness | pre-edit (`<scratch>/pre`) | lane before this pass | lane after |
|---|---|---|---|
| `the-board-runs-itself/transitions-are-commands` | 74 · 67 pass · 7 fail | 74 · 67 · 7 | 74 · 67 · 7 |
| `probe/tick.sh` (this unit) | n/a — the unit is the build | 7 pass 0 fail | 11 pass 0 fail |
| `index.py check` (lane) | 4 lines, exit 1 | identical | identical |

The 7 fails are pre-existing **before the first edit**, and the failing
*set* is identical in all three columns, not only the count: `claim with a
footprint clash names both`, `…and the clashing PRD`, `git diff empty
after every refusal`, `.transitions.jsonl not created by a refusal`, `the
template's comments survive`, `.transitions.jsonl has one row per state
move (13)`, `only prd.md files, the two new PRDs, .transitions.jsonl and
.claims/ moved`. None names `sweep` or `tick_sweep`.

`index.py check`: exit 1 in the lane, exit 0 in the checkout, on 4 lines —
`resources/common.py` with no row in `references/files.md`,
`references/files.md` and `@@view` naming
`@resources/board/hotreload-test.js`, and `references/parts/commits.md`
naming a `@pearde/memos/…` target. Byte-identical to the pre-edit clone's
output. The lane is 3 commits behind `main` and `lanes.create` cuts it
without the board, so these are the lane's, not this unit's.

`doctor.sh` in the lane: `vault`, `origin`, `memos`, `knowledge` and
`questions` broken before the first edit and after it, no row added. Rows
that moved during the run — `board 224 → 226 PRDs`, `harnesses 96 → 97`,
`vision 72 → 74 off`, `health … stale`, and `statusline`, which carries
the tree's dirty count — are neighbours landing PRDs while this ran. This
unit writes no board file, so it added none of them.

## Findings (report-only, not fixed)

- **A live footprint clash on `resources/board/serve.py`.**
  `a-fork-reaches-the-user-when-it-is-written` (state `claimed`,
  `impl-fork-reaches`, spec01 footprint `resources/board/serve.py`) is
  building **in the orchestrator's checkout**, not in its own lane — the
  lane `.pearde/.lanes/the-board-reclaims-dead-work-by-itself-a-fork-reaches-the-user-when-it-is-written`
  exists and its `git status` is clean, while the checkout's `serve.py`
  carries all 23 of its lines uncommitted. Two consequences for the
  orchestrator:
  1. `collect` on **this** PRD merges
     `lane/…-the-sweep-runs-between-passes` into a checkout whose
     `serve.py` is dirty with the neighbour's work. A merge touching a
     dirty path is refused. The neighbour has to land or park first;
     this lane no longer duplicates their lines, so once they land there
     is nothing to conflict on — my hunks are at lines 228, 306 and 767,
     theirs at 301, 449 and 812, and none overlap.
  2. This is the second pass in a row on this route where a worker built
     in the checkout instead of the lane the brief named. Pass one's
     report says its lane had been swept out from under its claim before
     it started. That is this PRD's own subject, from the other side.
- **The lane is 3 commits behind `main`** (lane `HEAD` `7a162c2`, `main`
  `77665a3`). Nothing in those commits touches this footprint; noted so
  the merge is expected to be a fast catch-up, not a surprise.
- **`## Failure` on the swept PRD is appended, never replaced.** A PRD
  swept twice accumulates two `## Failure` sections. Outside this spec's
  scope (`edit.append_section`'s own behaviour), reported not fixed.
- **This PRD's `Needs a-claim-names-the-process-that-holds-it` is prose
  in the body only** — the frontmatter carries no `needs:` key, though
  `needs:` is machine-read elsewhere (`gate_claim` reads it). Nothing
  enforced the ordering. Pass one raised this too; it still stands, and
  it is why `claim_liveness` had to be built inert rather than relied on.

## Files

- `resources/board/transitions.py` — `CLAIM_ID_RE`, `claim_liveness`,
  `tick_sweep` (+74 lines). Unchanged from pass one.
- `resources/board/serve.py` — `SWEEP_S`, `Board.last_sweep`, the guarded
  `tick_sweep` call in `watch()` (+18 lines, was +41 before the strip).
- `prds/…/the-sweep-runs-between-passes/probe/tick.sh` — 7 checks → 11.
- `prds/…/the-sweep-runs-between-passes/specs/spec01.md` — six boxes
  ticked, `Verify and Proof` count corrected 7 → 11.

Nothing under the health floor was in the footprint; nothing was
refactored. The lane is left uncommitted, as `collect` expects.
