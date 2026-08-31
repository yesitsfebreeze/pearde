---
complexity: 4
footprint:
  - resources/board/collect.py
  - .pearde/prds/collect-commits-only-the-prd-s-own-edits-not-the-footprint-s
---

# spec02 — the widen escape stands, and the analyzing window is the named gap

Two edges of the same guard, both demonstrated by the fixture: `--widen`
still takes a contested file whole on the worker's word (the refusal exists
only when the worker does not widen), and the analyzing window — a held
sibling with no specs and no footprint frontmatter — is invisible to the
refusal and still sweeps, because there is nothing to read. The gap is a
recorded limit, not work: a PRD declares its footprint at `specced`, and an
`analyzing` sibling with no specs yet cannot be attributed. Closing it needs
footprints to exist earlier — a different contract, reported, not specced
here.

## Acceptance

- [x] `probe/run.sh 2` passes: with `--widen <path>` naming the shared file, collect finishes, the progress line says `widened shared.py`, nothing is left dirty, the commit carries the sibling's lines whole
- [x] `probe/run.sh 4` passes: an `analyzing` sibling with no footprint anywhere is NOT refused — exit 0, the sweep persists, the gap documented rather than fixed here
- [x] the two harnesses stay green with the guard in: `resources/index.py check` and `resources/memos.py check`, both exit 0

## Verify and Proof

```sh
python3 -m py_compile resources/board/collect.py
bash .pearde/prds/collect-commits-only-the-prd-s-own-edits-not-the-footprint-s/probe/run.sh 2 4
rc=$?
echo "probe exit: $rc"
```