---
memo: an-analyst-that-picks-its-own-route-leaves-its-run-uncounted
kind: decision
status: decided
tags:
  - memo
  - kind/decision
  - status/decided
subject: a workflow run named only in `## Scores` is left uncounted, not reconstructed
date: 2026-09-02
---

# an-analyst-that-picks-its-own-route-leaves-its-run-uncounted — the orchestrator counts rows, never intentions

## Decision

A report that names a workflow in `## Scores` but writes no `## Workflow
<slug>` section is **uncounted**. The orchestrator does not bump `runs`, does
not touch an atomic, and does not reconstruct the rows from the report's prose.
It records the gap in the pass file and moves on.

This is what @references/parts/workers.md already says — absent means nothing
to collect. This memo exists because the rule keeps costing real runs, and the
next session that meets it should know the loss is deliberate rather than an
oversight to be corrected by hand.

## Why

The gap is structural, not careless. The analyst brief demands the `## Workflow
<slug>` section **only inside the workflow block**, and a PRD carrying no
`workflow:` key gets no block. So an analyst that *picks* a route off
`workflows.py list` — which is the encouraged behaviour, and which produces a
`workflow:` key on the PRD for everyone downstream — is never told to write the
section it will be judged by. It does the right thing and is silently not
credited for it.

Counting it anyway would be worse. The whole value of `runs` is that it is a
count of routes actually followed, step by step, with the outcome of each step
recorded — that is what makes a high-`runs` atomic trustworthy and what makes a
`## Fails when` row earned rather than imagined. An orchestrator that infers
rows from a report's prose is inventing the evidence the number is supposed to
summarise. A route with an honestly low `runs` is a route someone can still
improve; a route with an inflated one is a route nobody will question.

Two runs were lost to this on 2026-09-02 alone —
`the-machine-frontier-is-dispatched-in-parallel`'s analyst and
`a-cross-board-need-that-names-no-board-in-the-scan-is-ignore`'s, both
`probe-then-spec`, both naming the route in `## Scores`, neither writing a
section. Both are uncounted and stay uncounted.

## Alternatives considered

**Reconstruct the rows from the report's prose.** Both reports describe what
they did in enough detail that a plausible five-row table could be written.
Lost on the only count that matters: the orchestrator would be authoring the
worker's evidence. @references/parts/loop.md already forbids the milder version
of this — *"the worker wrote the text: paste it or refuse it, never rewrite
it"* — and inventing a table wholesale is the same error with less excuse.

**Send the analyst back for the section.** Correct in principle and affordable
for one run, but it treats a defect in the brief as a defect in the worker. The
worker followed the brief it was given. Sending it back trains nothing and pays
the round trip every time until the brief changes.

**Refuse the verdict outright** — no `## Workflow` section, no SPECCED. Lost on
proportion: the specs are good, the build was real, and the board would stall
on a bookkeeping formality. The verdict is about the work, not about the
paperwork attached to it.

**File a derived PRD to fix the brief.** This is where it ends up if it keeps
happening, but @references/parts/derived.md's test sends it here first: fixing
the brief changes how loudly the board notices its own routes, not what ships.
That is the definition of a memo rather than a PRD.

## Consequences

- `probe-then-spec`'s `runs` under-counts analyst passes, and will keep
  under-counting until the analyst brief demands the section outside the
  workflow block. Read the number as a floor, not a census.
- The fix, when someone takes it: the brief should ask for `## Workflow <slug>`
  whenever the report's `## Scores` names a slug, not only when the PRD arrived
  carrying a `workflow:` key. That is one condition, in one place.
- This does **not** excuse a worker that was handed a workflow block and
  ignored it. That is a defect in the run, and it is collected as one.
- Implementer runs are unaffected — an implementer's brief carries the block
  whenever the PRD carries the key, which by then it always does, because the
  analyst put it there.
