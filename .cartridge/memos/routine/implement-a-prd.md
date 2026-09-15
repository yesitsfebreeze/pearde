---
kind: routine
description: Implement one specced PRD in an assigned worktree and return artifacts and observed checks
uses:
  - usage: "[[run-usage]]"
    when: [a PRD is specced and ready to build, delivering a bounded outcome, acting as the implementer for a PRD]
    tags: [implementation, prd]
---

## Inputs

One PRD reference and revision from `prd brief`, its published specs and
Acceptance; a passed current review and prerequisite evidence; exact footprint;
a coordinator-assigned isolated worktree of the PRD's `repo`; acceptance
commands with cwd; a finite deadline and report path. The coordinator holds the
claim and owns every board transition.

## Do

1. Re-read the assigned PRD and specs and confirm the brief matches their
   revision. Verify the workspace base and required dependencies; reuse a
   reconciled analyst attempt. Work only in the assigned worktree; a missing
   lane recipe is not a prerequisite.
2. Implement the spec within the footprint. Resolve routine detail inside the
   contract; report a substantive mismatch for re-analysis instead of widening
   scope. Preserve unrelated changes. Produce reviewable commits only as assigned.
3. Run the Acceptance and the repository gates the brief names, from the owner's
   worktree. Report a missing required gate rather than skipping it. Record
   revision digests, exact commands, cwd, exit status and concise evidence,
   including first failures and focused retries; never claim a check not run.
4. Return one verdict in the report, with artifact paths and remaining limits:
   - `DONE`: the implementation and every locally observable check succeeded;
     coordinator-only checks are named as pending.
   - `FAILED`: the spec or Acceptance failed; preserve the reproducible failure
     and the attempt for correction or [[spec-a-prd]].
   - `BLOCKED`: name the external prerequisite or missing capability and what
     clears it; preserve partial artifacts.
   These are worker verdicts, never PRD states. Independent verification and
   `prd collect` through [[land-a-prd]] follow DONE.

## Check

The report covers the whole footprint and every Acceptance box, distinguishing
observed passes, failures and coordinator-dependent checks. Artifacts can be
inspected at their recorded revision. The worker has not changed PRD state,
ticked boxes or declared the outcome delivered.

## Failure

Stop at cancellation, deadline, stale input, unknown prior effects or a scope
mismatch; report exact evidence and preserve artifacts. Do not widen scope,
split work, overwrite others or replay uncertain mutations. Report an
out-of-scope defect as a proposed new PRD. Worker failure never rewrites the
board; the coordinator decides between `blocked`, `failed` and release.
