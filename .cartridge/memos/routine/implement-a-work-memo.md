---
kind: routine
description: Implement one reviewed native work memo in an assigned workspace and return artifacts and observed checks
uses:
  - usage: "[[run-usage]]"
    when: [a work memo carries an Approach and is ready to build, delivering a bounded outcome]
    tags: [implementation, work]
---

## Inputs

Canonical memo path/revision with Outcome/Approach/Check; passed current review
and prerequisite evidence; exact footprint; coordinator-assigned isolated code
worktree or record draft directory; acceptance commands with cwd; finite deadline
and report path. Coordinator owns live state and publication. Read `type/work.md`
and applicable resolved instructions. Review follows [[@prd/routine/plan-cartridge-work.md]] and
current user instructions, including delegated ratings without invented user scores.

## Do

1. Re-read the assigned contract and confirm the brief matches its substantive
   revision. Verify the assigned workspace/base and required dependencies; reuse
   a reconciled analyst attempt. Code work stays in the isolated owning repository
   worktree; records stay in assigned draft paths. A missing lane command is not
   a prerequisite: use the provided workspace and actual available tools.
2. Implement the Approach within the allowed footprint. Resolve routine details
   within its contract; report a substantive plan mismatch for re-analysis/review.
   Preserve unrelated changes. Create reviewable patches/commits only as assigned;
   record-only workers produce complete replacement Markdown drafts, not live writes.
3. Run the memo's observable checks and applicable current repository gates named
   by the brief. Validate gate paths/commands for this owner and change; an old
   support-routine link cannot force a stale checkout or missing recipe. Report
   a missing required gate rather than silently skipping it. Documentation-only
   outcomes need meaningful document/tool checks, not unrelated broad builds.
   Record revision or draft digests, exact commands, cwd, exit status and concise
   evidence. Include first failures and focused retries; never claim checks not run.
4. Return one verdict in the report, with artifact paths and remaining limitations:
   - `DONE`: assigned implementation and locally observable checks succeeded;
     any coordinator-only publication/collection checks are explicitly pending.
   - `FAILED`: Approach or acceptance failed; preserve the reproducible failure
     and attempt for correction or [[@prd/routine/spec-a-work-memo.md]].
   - `BLOCKED`: name the external prerequisite or missing capability and what
     clears it; preserve partial artifacts and uncertain effects.
   Send only the verdict and report path in the handoff. These are worker report
   verdicts, never native memo status values. Independent verification and
   coordinator collection through [[@prd/routine/land-a-worked-lane.md]] still follow DONE.

## Check

The report covers the full assigned footprint and Check, distinguishing observed
passes, failures and publication-dependent checks. Artifacts can be inspected at
their recorded revision/digests. The worker has not written live status/owner,
ticked the memo's boxes, published drafts or declared the outcome delivered.

## Failure

Stop at cancellation, deadline, stale substantive input, unknown prior effects
or a scope mismatch; report exact evidence and preserve artifacts. Do not widen
scope, split work, overwrite others or replay uncertain mutations. Report an
out-of-scope defect as a proposal for separate work. The coordinator handles
bounded shutdown, review, native open/active/blocked/done/cancelled state and
ownership; worker failure never silently rewrites the live memo.
