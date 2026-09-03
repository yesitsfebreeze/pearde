---
state: done
origin: requested
priority: 21
complexity: 12
blast-radius: low
workflow: probe-then-spec
actual: 0.45h
commit: fd73eff
---

# The promotion rule

*Source: `docs/content/docs/improvements/workflows-promotion.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** workflows · **Axis:** sensibility (7 → 8) · **Pulls the score up
by ~3 points**

## Why now

Two kinds, one line apart: an **atomic** is one unit; a **workflow** is
ordered atomics. An atomic whose body says "then run the other atomic"
already *is* an ordered pair — it reads like a workflow before it is one,
and the reader cannot tell whether they are holding a unit or a route
drawn by hand. The reference gives the promotion no rule, so the promotion
happens by whoever got tired of the pair first, and the library accumulates
both shapes for the same job.

## The change

One promotion rule, checked by the doctor row and written once into the
template's doc: an atomic whose body routes to another atomic **by slug**
is refused — "route it, or inline it". The choice is the author's, stated
in the refusal: *inline* if the second unit is a detail of the first (it
becomes prose, one unit again), *promote* if it is a step on its own (a
workflow file with two atomics). Both outcomes are one file shape, so the
check closes the ambiguity instead of managing it.

## Done when

- An atomic body naming another atomic's slug fails the doctor row with the
  pair named.
- Inlining the second and re-running the check reads `ok` — as does
  promoting both into a workflow with `workflow: <slug>`.
- The library's existing pairs are found and decided once — the check's
  first run names every one.

## Fails when

- The refusal fires on a *prose* mention of another atomic — "compare with
  the reproduce-the-failure atomic" is text, not a route. Guard: the check
  reads the steps table's route column, the structured place routes live,
  never the prose.

## What stays out

No migration script — the first doctor run is the census, and the library
is small enough to decide by hand. The rule is the deliverable; the
cleanup is one session.

## Blocked

**2026-09-03 21:12 — the lane will not rebase**

`lane/the-promotion-rule` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/workflows.py`

Nothing is lost: the worker's commits are on `lane/the-promotion-rule` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-promotion-rule`.

**2026-09-03 21:14 — the lane will not rebase**

`lane/the-promotion-rule` does not land on `session/s27323`; 1 file(s) disagree:

- `resources/workflows.py`

Nothing is lost: the worker's commits are on `lane/the-promotion-rule` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-promotion-rule`.

**2026-09-03 21:19 — the lane will not rebase**

`lane/the-promotion-rule` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-promotion-rule` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-promotion-rule`.

**2026-09-03 21:19 — the lane will not rebase**

`lane/the-promotion-rule` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-promotion-rule` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-promotion-rule`.

**2026-09-03 21:21 — the lane will not rebase**

`lane/the-promotion-rule` does not land on `session/s27323`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/the-promotion-rule` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock the-promotion-rule`.

## Report

the-promotion-rule: session/s27323 moved under the lane — references/templates/atomic.doc.md, references/workflow.md, resources/workflows.py

spec01: exit 0
  ok   a bare `Run `<slug>`.` step is refused
  ok   a route behind a lead-in clause is refused
  ok   a prose comparison to a sibling passes
  ok   `Run `pytest tests/`.` passes — not a slug
  ok   a slug the library does not hold passes
  ok   an atomic naming its own slug passes
  ok   the same sentence outside `## Do` passes
  ok   the refusal names the atomic, the routed-to slug and both choices
  ok   the census on /Users/feb/dev/infra/pearde/.pearde is empty — no existing pair to decide by hand
  ok   references/workflow.md's failure list states the rule once
  ok   references/templates/atomic.doc.md states the rule once
11/11 passed
