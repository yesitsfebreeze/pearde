---
complexity: 14
footprint:
  - resources/board/brief.py
  - resources/board/transitions.py
  - resources/board/plan.py
  - references/parts/loop.md
---

# spec01 — brief accepts the claim it was just handed, by worker id

`plan.dispatchable(prd, prds, board=None, holder=None)` now takes an optional
`holder`: the `unclaimed` gate fires only when the PRD's `claim:` names
someone other than `holder` (`held["who"] != holder`, `plan.py:1447-1449`).
Every existing caller — `compute_plan`, `cmd_scan`'s ready/gated sections,
`collect.py:1066`, `plan.py:1621/1718/2064/2066` — leaves `holder` at its
default `None`, so `held["who"] != None` is always true and the gate is
exactly as strict as before for all of them. `transitions.gate_claim(board,
prds, prd, holder=None)` threads the same optional argument straight into
`dispatchable` (`transitions.py:159-168`); its own two callers — `brief.py`
and `transition()`'s `claim` branch at `transitions.py:289` — either pass a
holder or don't, and the `claim` branch's call is unaffected either way
because no `claim:` exists yet at that point in a claim.

`brief.py` gained a `--worker <id>` option (`FLAGS` at `brief.py:363-364`)
and reads it into `worker` in `brief_prd` (`brief.py:283`). The pre-check at
`brief.py:284-302` now computes `self_claim = bool(worker) and bool(held) and
held["who"] == worker`, and only refuses `analyzing`/`claimed` outright when
`not self_claim`; a self-claimed `analyzing`/`claimed` PRD instead falls
through to `gate_claim(board, prds, prd, holder=worker)`, so `needs`,
`footprint`, `workflow` and `leaf` still gate it — the self-claim lifts only
the `unclaimed` word. `open`/`specced` still routes straight to `gate_claim`
as before (`held` is `None` there in the normal case, so `holder` is inert).
A `held and state in ("open", "specced")` PRD — held before its state caught
up — still refuses unconditionally, worker or not: the PRD names this as an
already-odd corner and does not ask for it to be loosened. Nothing here
writes `state:` or `claim:` — `brief` still has no `--dry` because it writes
nothing, full stop.

`references/parts/loop.md` step 4's command cell now reads `pearde brief
<prd> --worker <worker>`, and the step 4·5 paragraph says in words that a
self-claim is not itself a refusal and that the routine dispatch needs no
`--force` — `--force` is described as staying the escape hatch for a PRD
genuinely held by someone else.

All of this stands already: reproduced against a throwaway board built by
`probe/verify.sh` (never under `prds/`), all seven cases below pass. The real
board's own `brief-does-not-refuse-the-claim-it-was-just-handed` PRD —
`claim: an-15 …`, `state: analyzing` — is itself live proof of the exemption
being exactly as narrow as the PRD asks: `--worker an-15` no longer says
`held` (the pre-check the PRD is about is cleared), but it is not clean
either, because this PRD's own new footprint (`resources/board/brief.py`,
declared above) genuinely overlaps `resources/board/brief.py` on
`collect-commits-the-code-repo-not-the-board-repo-twice/collect-defaults-to-
the-boards-enclosing-repo`, `claimed` by `impl-5`, boxes 4/4, elsewhere on
this same board right now — a real concurrent claim, not a fixture. So
`--worker an-15` today exits 1 with `clash`, not `held`: exactly what
"a self-claim that also fails a second gate ... still exits 1" means, caught
live rather than only in the probe. `--worker` omitted still refuses `held`
regardless. Once that other PRD collects, the clash clears and `--worker
an-15` goes clean — that box is written to be re-run then, not asserted here
against a moving target.

## Acceptance

- [x] `bash .pearde/prds/brief-does-not-refuse-the-claim-it-was-just-handed/probe/verify.sh`
      exits 0 (all seven cases: self-claim accepted no-force, no-worker still
      held, other-worker still held, an implementer role and self-claim
      together, self-claim still needs-gated, self-claim still footprint-
      clashed, an out-of-range state still state-refused — and the PRD file
      byte-identical across the three case-1/2/3 runs)
- [x] on the real board, `brief.py <this prd> --worker <the worker its own
      `claim:` names>` no longer says `held`. Re-run 2026-08-31 18:45 against
      the live claim, which had moved on from the `an-15` the paragraph above
      was written against: the holder is now `impl-11`, `state: claimed`, the
      `collect-defaults-to-the-boards-enclosing-repo` clash has since
      collected, and the command exits **0** with the implementer brief and
      no `· forced` — the clean case that box predicted. `--worker an-15`,
      now a *different* worker, correctly still exits 1 with `held`
- [x] the same command with no `--worker` exits 1 and prints a `held` skip
      naming `analyzing` and the `claim:` value
- [x] `python3 resources/board/brief.py --check` still exits 0 (the brief
      block table is untouched)
- [x] `grep -n "pearde brief <prd> --worker <worker>" references/parts/loop.md`
      finds the step 4 row

## Verify and Proof

```sh
# `collect` runs this block under `set -e` with the BOARD as cwd, not the repo
# root. Both bite: paths must be anchored, and every command expected to FAIL
# must be guarded with `|| true` or the capture kills the whole block.
# Original wording follows.
# `collect` runs this block with the BOARD as cwd, not the repo root, so every
# relative path below must be anchored first. Without this the python calls
# all fail to find their file and the greps below read as passes.
cd /Users/feb/dev/infra/pearde
bash .pearde/prds/brief-does-not-refuse-the-claim-it-was-just-handed/probe/verify.sh || exit 1
P=brief-does-not-refuse-the-claim-it-was-just-handed
W=$(sed -n 's/^claim: *\([^ ]*\).*/\1/p' .pearde/prds/$P/prd.md | head -1)
test -n "$W" || { echo "FAIL no claim: holder to test against"; exit 1; }

echo "--- the holder is briefed, unforced ---"
out=$(python3 resources/board/brief.py $P --worker "$W" 2>&1) || true; rc=$?
# assert the command actually ran before trusting what it did not print
printf '%s\n' "$out" | grep -q '^# brief ' || { echo "FAIL no brief header — did it run?"; exit 1; }
test $rc -eq 0 || { echo "FAIL holder brief exit $rc"; exit 1; }
printf '%s\n' "$out" | grep -q 'skipped .* held' && { echo "FAIL still says held"; exit 1; }
printf '%s\n' "$out" | grep -q '· forced' && { echo "FAIL brief was forced"; exit 1; }
echo "ok  holder briefed clean, no force"

echo "--- a different worker is still refused ---"
out=$(python3 resources/board/brief.py $P --worker not-the-holder 2>&1) || true
printf '%s\n' "$out" | grep -q 'skipped .* held' || { echo "FAIL other worker not refused"; exit 1; }
echo "ok  other worker still held"

echo "--- no --worker at all is still refused ---"
out=$(python3 resources/board/brief.py $P 2>&1) || true
printf '%s\n' "$out" | grep -q 'skipped .* held' || { echo "FAIL bare brief not refused"; exit 1; }
echo "ok  bare brief still held"

python3 resources/board/brief.py --check || exit 1
grep -q 'pearde brief <prd> --worker <worker>' references/parts/loop.md || {
  echo "FAIL loop.md does not document --worker"; exit 1; }
echo "spec01 checks done"
```
