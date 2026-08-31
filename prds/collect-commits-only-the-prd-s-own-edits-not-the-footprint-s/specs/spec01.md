---
complexity: 6
footprint:
  - resources/board/collect.py
  - .pearde/prds/collect-commits-only-the-prd-s-own-edits-not-the-footprint-s
---

# spec01 — refuse a dirty path a held sibling's footprint also holds

`sort_paths` in `resources/board/collect.py` builds an `others` map — every
other held PRD (`analyzing`, `claimed`, `blocked`) whose code lives in this
run's `repo`, its footprint union (prd frontmatter plus specs', member sigil
stripped) — and, inside the loop over dirty union paths, refuses a path whose
dirt is not entirely explained by this PRD's claim baseline (`predates()` is
false) while a held sibling's footprint also holds it: Stop, exit 1,
nothing written, the message naming the sibling and `--widen <path>`. This
stands, built, in the working tree — what is left is proving it on the
fixture and the boxes below, then no more.

The fixture is `probe/run.sh` under this PRD's folder; it builds a throwaway
code repo with a nested board repo in a runtime temp dir, never under
`prds/`, and needs no network and no daemon.

## Acceptance

- [x] `probe/run.sh 1` passes: a claimed sibling's edit to `shared.py` — a tracked path both footprints hold, dirtier than `prds-a`'s claim — is refused by `collect --dry` and by a real collect, exit 1, HEAD of the throwaway code repo unmoved, `prd.md` untouched
- [x] the refusal message names the sibling (`is in prds-b's footprint too`) and the `--widen <path>` answer
- [x] `probe/run.sh 1 5` passes: an untracked file a held sibling's footprint covers is refused the same way, not added whole
- [x] `probe/run.sh 3` passes: with no footprint overlap, this PRD's own edits still land in the dry plan (`would add: own.py, shared.py`) and the real commit

## Verify and Proof

```sh
python3 -m py_compile resources/board/collect.py
bash .pearde/prds/collect-commits-only-the-prd-s-own-edits-not-the-footprint-s/probe/run.sh 1 3 5
rc=$?
echo "probe exit: $rc"
```