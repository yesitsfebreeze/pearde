---
kind: routine
description: Investigate one native work outcome and return a bounded approach, split or question for coordinator publication
uses:
  - usage: "[[run-usage]]"
    when: [a work memo has an Outcome but no Approach, planning how a bounded outcome will be delivered]
    tags: [planning, work]
---

## Inputs

One canonical work path and revision; Outcome and existing Check; relevant type
and context reads; exact footprint; coordinator-assigned attempt/draft directory,
finite deadline and report path. The analyst has no live-record ownership. Read
`type/work.md`; resolve applicable context before probing.

## Do

1. Read the actual memo, dependencies and relevant source. Investigate the outcome
   with the smallest meaningful attempt, reproduction or tool probe allowed by
   the brief. For code, use the coordinator's verified isolated worktree/base and
   required dependency commits; continue a reconciled earlier attempt. For a
   record-only outcome, inspect current MCP contracts and prepare drafts in the
   assigned directory. Never require a lane recipe or create an unassigned checkout.
2. Record what was actually attempted, commands with cwd/exit status, revision,
   observations and remaining uncertainty. Separate source evidence from inferred
   behavior. Do not invent successful probes or an implementation already present.
3. Return one verdict and proposed edits as draft files plus a bounded report:
   - `SPECCED`: Outcome/Approach/Check define one executable leaf, exact files,
     ordered runnable steps, dependency/base requirements and observable checks.
     Name reusable attempt artifacts and the remaining work. Split scope too large
     to hand off safely instead of assigning an unsupported calendar estimate.
   - `SPLIT`: draft independently useful child work with Outcome and Check and
     proposed parent `subwork`. Use `needs` only for hard prerequisites; keep the
     graph acyclic and identify any shared files requiring serialized integration.
     Do not dispatch children or quietly expand the selected outcome.
   - `QUESTION`: describe the material unresolved choice actually reached, the
     evidence, recommended resolution and alternatives. Read `type/question.md`
     before drafting a question and proposed `needs` link. A missing service or
     failed command is failure evidence unless an explicit answer is needed.
4. Send the verdict and report path to the coordinator. It validates draft types,
   unique names, links, readiness and scope, publishes any prerequisites before
   dependent edits with current revision guards, and reads them back. It alone
   updates live status/owner. Implementation requires current review under
   [[@prd/routine/plan-cartridge-work.md]], including explicit user delegation of ratings; a
   worker verdict or successful probe is not a review gate or memo status.

## Check

The report names exactly one analyst verdict, observed evidence, artifacts and
remaining work. On SPECCED, Approach has real files/runnable steps and Check can
detect failure. On SPLIT, proposed children cover the outcome and disclose shared
footprints. On QUESTION, the needed answer and dependent work are explicit.
Draft production is distinct from the coordinator's validated publication.

## Failure

If the attempt cannot start, report the exact failure and what clears it; do not
fabricate an Approach or turn every technical failure into a user question.
Stop on changed inputs, cancellation, deadline or footprint drift; preserve the
attempt and uncertain effects for coordinator reconciliation. Never publish live
memos, tick acceptance boxes, mark done, land code or retry unknown mutations.
