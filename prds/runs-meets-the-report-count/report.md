Verdict: QUESTION

## What the build did

Followed `probe-then-spec` (61 prior runs, `## Use when` fits an open PRD
needing specs before a build). Ran `read-the-contract` on this PRD's body —
no `## Answers` present. `knowledge.py query` on the contract's own sentence
returned 104 strong hits (no gap auto-enqueued — the record already covers
adjacent claims, nothing new to remember here).

The PRD asks for a doctor check: count "report sections" for a workflow
library file and compare that count against its `runs:` frontmatter,
`broken` when they disagree, both numbers named.

I located the actual mechanism the PRD is extending: `@references/workflow.md`
`## The report section` defines a fixed report shape, `## Workflow <slug>`,
that a worker embeds in their own `report.md` when they follow a workflow —
this is the only "report section" shape defined anywhere in the tree, and it
is not stored inside the workflow's own library file (`workflow.md` is
explicit: "No log"). So the count has to come from the corpus of
`.pearde/prds/*/report.md` files currently on disk.

I built the count and ran it against the live board:

```
grep -h "^## Workflow " .pearde/prds/*/report.md | sort | uniq -c
  33 ## Workflow probe-then-spec
   1 ## Workflow correct-a-documented-claim
```

`probe-then-spec`'s own file (`.pearde/workflows/probe-then-spec.md`) reads
`runs: 61`. 33 ≠ 61 — on the board's own most-used workflow, today, with no
bug in flight. The gap is structural: a PRD's `report.md` is overwritten by
its next pass (an implementer's report replaces the analyst's), so a
workflow followed early in a PRD's life stops being counted the moment that
PRD moves on, while `runs:` — bumped once and then left alone — keeps every
count it was ever given.

## The fork I hit

The PRD's own text ("the two disagreeing is `broken`") reads as an equality
check. Built literally, that reads the board's real, non-broken
`probe-then-spec` as broken right now, on data with no failure in it — the
`## Fails when` guard in the PRD only covers an in-flight two-step write
race, not this steady-state gap from normal `report.md` replacement. Which
of the two the doctor should actually implement — an equality check, an
asymmetric one that only fires when reports outnumber `runs:` (matching the
"died before the increment" bug the PRD opens with), or a running tally
counted at use-time instead of read off `report.md` at check-time — changes
both what the doctor will say about this board today and how expensive the
check is to run. I could not pick between them without guessing at intent,
and could not build around it: any of the three is a different, non-trivial
check.

Written to `prd.md` as Q1, per drill.md's pass format, three prepared
answers, answer 1 (the asymmetric snapshot check — cheapest, matches the
actual bug the PRD describes, and does not flag the board's own live data)
marked recommended.

## Scores

No specs written — QUESTION, no spec/split table applies.
