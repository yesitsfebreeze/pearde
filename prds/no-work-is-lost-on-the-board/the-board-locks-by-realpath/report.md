# the-board-locks-by-realpath — analyst pass two, as engineer

Verdict: SPECCED

workflow: probe-then-spec, second pass — the specs already stood from the first
analyst pass (report of 2026-09-03 11:54), and the brief's second-pass rule
applies: step 3 re-measures the build, step 5 applies each spec's acceptance
boxes to the blocks that already stand, and no new spec is authored.

## What the build found this pass

The prior analyst's build stood on the lane, committed by the sweep as
`6560ab9` after the first implementer died silent at 11:57. Its probe held
claims A-D green and **E and F red**. This pass re-measured, fixed both, and
found a third bug the first probe had masked:

1. **E — the dead clause.** `BoardLock.acquire` appended
   `— spelled X there, one physical board at Y` only when the holder's
   spelling differed from the caller's, and `os.getcwd()` returns the resolved
   path (`[[260903-4626]]`), so it never differs. The clause is replaced by the
   always-true `— one physical board at <realpath>`, which is the sentence
   that tells a person the symlink and its target are one board. Green.
2. **F — the silent empty set.** `main` returned 1 on `not locks` with nothing
   printed. Fixed by falling through to the read when there was nothing to
   lock. Green — probe claim F prints the empty frontier, rc 0.
3. **NEW, found while re-measuring: the held filter swallowed the refusal.**
   The first fix, applied in the obvious order, still let a fully-held board
   exit 0: `main` filtered the held boards out of `entries` (leaving it
   empty), *then* tested `not locks and entries` — so the second `pearde run`
   printed a 0-board order, `skipped proj — already being dispatched`,
   `dispatched 0`, and **rc 0**. Measured by hand against the lane before the
   fix: second run rc=0 with the refusal only on stderr. The order of the two
   tests is the fix — `not locks and entries` is now tested on the entry set
   *before* the filter. Probe claim C (`rc=1`, no order printed) is the check
   that catches it, and it was red for rc, not just for the order line.

After the fixes the probe is green end to end — A, B, C (four sub-claims), D,
E, F:

```
PASS  A. one watch entry for one realpath (1: ['proj'])
PASS  A. the second spelling is not a new board
PASS  A. both spellings answer to one name
PASS  B. .state/serve.json was written
PASS  B. the marker records the realpath
PASS  C. the second run refuses (rc=1)
PASS  C. the refusal says the board is already being dispatched
PASS  C. the refusal names the first dispatcher's pid
PASS  C. the second run printed no order it was not going to work
PASS  E. the refusal names the physical board the two spellings share
PASS  D. a run after the first exits is taken, not refused
PASS  F. an empty entry set is answered, not exited on in silence
0 claim(s) failed
```

Committed on the lane (`lane/no-work-is-lost-on-the-board-the-board-locks-by-realpath`,
now at `1be0ff5`, on top of the sweep's `6560ab9` and a mid-pass checkpoint
`bbc134d`): spec01's and spec02's code stands complete; **spec03 is
untouched** and is the implementer's remaining work — the tracked invariant
script, the `references/parts/run.md` section and the `references/files.md`
row.

## Specs

| spec | goal | complexity | state |
|---|---|---|---|
| `specs/spec01.md` | one dispatcher per physical board, and the refusal says whose | 9 | code done, boxes green |
| `specs/spec02.md` | the watch set is keyed by realpath, and the marker holds one name | 3 | code done, boxes green |
| `specs/spec03.md` | the lock is written down, and a tracked check fails when it goes | 10 | untouched — the implementer's work |

Sum 22, three units — under the board's `settings.md` limits on both counts.

Footprint union:

```
resources/board/dispatch.py
resources/board/serve.py
resources/invariants/one-dispatcher-per-physical-board.sh
references/parts/run.md
references/files.md
```

## Scores

complexity: 22
blast-radius: mid
workflow: probe-then-spec

Complexity 22 is the PRD's own frontmatter value, unchanged: the lock
mechanism was standing and needed three small repairs, but the spec03 unit
(invariant script that must be shown to fail, plus two reference pages) is
real work the board has not paid for yet. Blast-radius mid: `dispatch.py`
gates every dispatch on the machine and `serve.py` decides watch-set identity,
but both changes are additive around the existing pool and the probe measures
the whole contract end to end.

## Findings — not specced, not fixed

- **Two memo invariants are BROKEN before anything of this PRD touches them**:
  `no-harness-under-the-board-dispatches-it` and
  `a-pass-holds-its-turn-until-its-workers-are-in` name scripts that exist
  nowhere — not in the lane and not on `main` (`git ls-tree main
  resources/invariants/` holds neither). The lane's `memos.py verify` is
  therefore 6 holds / 2 BROKEN, against the first analyst's report of "all six
  hold". Either the scripts were deleted from main or the memos name scripts
  their PRDs never wrote; either way it is outside this footprint and should
  go to `the-board-reclaims-dead-work-by-itself` or the owning PRDs.
- `python3 resources/index.py check` prints the same four pre-existing lines
  the first analyst recorded (`common.py` unmanifested, `hotreload-test.js`
  twice, `commits.md` memo link) — unchanged by this pass, and spec01's box 8
  already excludes them by name.
- The lane branched at `f8968fe`, several commits behind `main`; the merge at
  collect time is the board's own job (`lane rebase`), not a defect here.
- The first analyst's other findings stand: the duplicate-ArgumentParser note,
  the index drift, the KB gap auto-enqueued under `.pearde/wiki/pending/`.
