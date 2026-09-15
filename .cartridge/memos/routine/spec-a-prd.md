---
kind: routine
description: Investigate one open PRD and return a bounded specification, split or question for the coordinator to publish
uses:
  - usage: "[[run-usage]]"
    when: [a PRD has an outcome but no published spec, planning how a bounded outcome will be delivered, acting as the analyst for a PRD]
    tags: [planning, prd]
---

## Inputs

One PRD reference (`@board/slug`) and its revision from `prd brief`; its
Acceptance boxes; exact footprint; a coordinator-assigned attempt or draft
directory, finite deadline and report path. The analyst owns no board state:
`prd` transitions belong to the coordinator. Read the
[PRD template](../../templates/prd.md) and [spec template](../../templates/spec.md).

## Do

1. Read the actual PRD, its `needs` and relevant source. Investigate the outcome
   with the smallest meaningful attempt, reproduction or tool probe the brief
   allows, in the coordinator's isolated worktree at the required base. Continue
   a reconciled earlier attempt rather than starting over. Never create an
   unassigned checkout.
2. Record what was attempted: commands with cwd and exit status, revision,
   observations and remaining uncertainty. Separate source evidence from
   inferred behaviour. Do not invent a successful probe or an implementation
   that is already present.
3. Return one verdict, with drafts in the assigned directory and a bounded report:
   - `SPECCED`: a `specs/specNN.md` draft with exact files, ordered runnable
     steps, dependency and base requirements, and Acceptance boxes a command can
     fail. Name reusable attempt artifacts and the remaining work.
   - `SPLIT`: independently useful child PRDs, each with its own outcome and
     Acceptance, to be added with `prd add --parent`. Use `needs` only for hard
     prerequisites; keep the graph acyclic and name shared files that force
     serial integration. Do not dispatch children or widen the selected outcome.
   - `QUESTION`: the material unresolved choice actually reached, the evidence,
     the recommended resolution and alternatives, for the coordinator's
     `question` transition. A missing service or failed command is failure
     evidence, not a question, unless an explicit answer is needed.
4. Send the verdict and report path to the coordinator. It validates the drafts,
   publishes specs (`specced`), adds children (`refine`) or records the question,
   and alone changes PRD state. Implementation still needs the current plan
   review under [[plan-cartridge-work]]; a worker verdict is not a review gate.

## Check

The report names exactly one verdict, observed evidence, artifacts and remaining
work. On SPECCED the spec has real files, runnable steps and boxes that can fail.
On SPLIT the children cover the outcome and disclose shared footprints. On
QUESTION the needed answer and the dependent work are explicit.

## Failure

If the attempt cannot start, report the exact failure and what clears it; do not
fabricate a spec or turn every technical failure into a user question. Stop on
changed inputs, cancellation, deadline or footprint drift and preserve the
attempt for reconciliation. Never run a `prd` transition, tick Acceptance boxes,
land code or retry an unknown mutation.
