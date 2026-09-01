---
complexity: 15
footprint:
  - .pearde/prds/the-round-is-handed-its-step-not-the-manual/collect-reads-the-worker-s-report-and-routes-its-own-verdict/probe
  - resources/board/collect.py
---

# spec02 — collect reads the report and routes its own verdict

`collect --report <path>` stands in the tree from pass one: the verdict word
is read off the report's head only, an unknown or missing word is refused
with nothing written, and each of the six verdicts runs its transition
in-process through that command's own `COMMANDS` entry — so every gate the
transition already checks still runs, and a red verify is still exit 1.
`collect` without `--report` is unchanged. This spec's work is the probe
harness that proves it, left at the PRD's `probe/` as the next worker's pass
one, plus any repair the probe's rerun asks for.

## Acceptance

- [x] `python3 .pearde/prds/the-round-is-handed-its-step-not-the-manual/collect-reads-the-worker-s-report-and-routes-its-own-verdict/probe/probe_route.py` prints `14 passed, 0 failed` — all six verdicts route, missing and unknown refused, red verify still exit 1, bare collect unchanged
- [x] `collect --report` with a `## Scores` workflow the library does not hold routes `--workflow <slug> --route -` and `specced` drafts the workflow file, as the probe's second fixture asserts (probe check "SPECCED with a new slug routes --route - and drafts the workflow" — ok)
- [x] `python3 -m py_compile resources/board/collect.py` exits 0 (COMPILE-OK)

## Verify and Proof

```sh
PYTHONDONTWRITEBYTECODE=1 python3 .pearde/prds/the-round-is-handed-its-step-not-the-manual/collect-reads-the-worker-s-report-and-routes-its-own-verdict/probe/probe_route.py > /dev/null && python3 -m py_compile resources/board/collect.py && echo ROUTE-OK
```