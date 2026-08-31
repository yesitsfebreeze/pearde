---
complexity: 8
footprint:
  - references/parts/workers.md
  - references/parts/workflows.md
  - references/parts/loop.md
  - references/drill.md
---

# spec03 — the analyst brief, the loop and the drill name the route

Already stands:

- `references/parts/workers.md` — the analyst brief now opens with running
  `workflows.py list` and following what fits; the SPECCED bullet drops
  `workflow: none fit` and, on the same block, adds the `## Route` shape
  (workflow body, then one `### atomic <slug>` block per new step, none for a
  step whose atomic already exists) that `pearde specced --route -` reads;
  the "On return" line documents `--workflow <slug> --route -`.
- `references/parts/workflows.md` — *When a file is written* gains the row
  *nothing fits at spec time — the analyst's route, written by `specced`,
  `runs: 0`*.
- `references/parts/loop.md` step 4 documents `specced` reading `## Route`,
  drafting and gating it, and refusing `--workflow none`; step 6's `runs +1`
  note says a route drafted at `runs: 0` is no exception — its first collect
  is `runs: 1` like any other, filling `## Fails when` for the first time.
- `references/drill.md` now credits a new workflow to the analyst at spec
  time, `## Route`, never to the drill.

Nothing left to finish — prose only, cross-checked against `spec02.md`'s
behavior by hand while writing it.

## Acceptance

- [x] `references/parts/workers.md`'s analyst block names `## Route` and
      shows the `### atomic <slug>` shape, and carries no `none fit` text
- [x] `references/parts/workflows.md`'s *When a file is written* table has a
      row for spec-time drafting
- [x] `references/parts/loop.md` step 4 mentions `--route -` and step 6
      mentions a freshly-drafted route's first collect
- [x] `references/drill.md` credits the analyst, not the orchestrator, with
      writing a new workflow

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
grep -q '## Route' references/parts/workers.md
grep -q 'not a verdict this board accepts any more' references/parts/workers.md
if grep -q '| none fit' references/parts/workers.md; then
  echo "FAIL: the old Scores line, workflow: <slug> | none fit, is still there"; exit 1
fi
grep -q 'nothing fits at spec time' references/parts/workflows.md
grep -q -- '--route -' references/parts/loop.md
grep -q 'runs: 0. is no' references/parts/loop.md || grep -q 'no exception' references/parts/loop.md
grep -q "analyst's, at spec time" references/drill.md
echo spec03 ok
```
