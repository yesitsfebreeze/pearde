---
complexity: 3
footprint:
  - resources/board/collect.py
---

# spec02 — the hold-it guard reads history after a deletion lands

`sort_paths` refuses a footprint path "in no repo that holds it" — the
guard against committing `done` over code `collect` never found. Its
answer is disk plus index (`os.path.exists` / `git ls-files`). A lane
whose contract deleted a footprint path lands that deletion as a commit;
after the merge the checkout's index no longer holds the path either —
the index moved with the merge — so the guard refuses the very collect
the fix in spec01 just unblocked, one step later in the same flow. The
comment's own case ("deleted from the working tree but not yet staged")
is the pre-merge shape only.

What already stands: the guard also accepts a path some commit carried —
`git log -1 --format=%H -- <path>` is non-empty for any path history
holds and empty for a path that never existed, so the never-existed
refusal keeps its teeth. Left to finish: nothing in `collect.py`; the
verify below holds the guard both ways on the merged tree.

## Acceptance

- [x] a fixture PRD whose lane deleted a footprint file collects past the
      guard to `state: done` — the PRD record written, the commit shas
      recorded — `verify.py`: `gone shape: 0 ['state: done'] carries: D
      resources/install.sh | M resources/keep.txt`
- [x] a fixture PRD whose footprint names a path that never existed in
      any commit is still refused with `is in no repo that holds it` —
      `verify.py`: `nonexistent shape refused, as it must be: Stop …
      footprint resources/never/was.sh is in no repo that holds it` then
      `PASS`

## Verify and Proof

```sh
python3 .pearde/prds/a-collect-stages-a-deleted-footprint-path-as-a-deletion/probe/verify.py
```