---
kind: routine
description: Collect one worked attempt with independent verification and serial publication or code integration before recording completion
uses:
  - usage: "[[run-usage]]"
    when: [a worker reports DONE and the coordinator collects it, publishing work memo drafts, integrating a verified code attempt]
    tags: [landing, work]
---

## Inputs

One canonical work memo/revision and Check; implementer report and artifact
revisions/digests; exact assigned footprint; current review/prerequisite evidence;
coordinator checkpoint; and approved record destination or owning Git target.
The name retains the old lane vocabulary; collection uses existing MCP/Git tools,
not mandatory lane recipes. Only the coordinator publishes state or integrates.

## Do

1. Re-read live memo/review/dependencies, ownership and target revisions. Inspect
   the report and actual diff/drafts; reject unrelated paths, unexplained changes,
   stale substantive inputs and failed acceptance. Worker DONE is an input, not
   `status: done`. Reconcile an earlier collection attempt before any mutation.
2. Assign a separate verifier with canonical contract/revision, actual artifacts,
   exact footprint, cwd/commands, finite deadline and report path. Respect host
   capacity; verify sequentially if necessary. The verifier independently reruns
   observable checks and distinguishes executed results from walkthroughs.
3. For records, coordinator reads each destination immediately before validated
   memo write, retains its body/revision and uses `expected_revision` for existing
   paths. Recheck new-path/leaf absence; reconcile any appearance. Publish linked
   supporting ingredients before the coordinator/dependents, serially. Read back
   each success and record its final revision; no atomic multi-document update or
   cross-session exclusion is promised. Have the independent verifier read the
   actual published memos through MCP, rerun applicable discovery/link checks,
   and confirm the final content against Check. Draft checks alone cannot pass
   publication acceptance. Never treat a stale write as permission to overwrite.
4. For code, inspect the owning target's current HEAD/status and the attempt's
   base/commits. Preserve unrelated dirty work. Prepare the combined result in
   an isolated integration worktree at the actual target revision; cherry-pick
   only assigned commits in order, or use an agreed equivalent Git integration.
   Resolve in-scope conflicts and rerun acceptance plus applicable current owner
   gates on that combined revision. The independent verifier checks that same
   result. Recheck target HEAD before advancing it; if it moved, rebuild/reverify
   the combination. Advance a verified clean, approved target using explicit Git
   commands such as `git -C <target-worktree> merge --ff-only <integration-branch>`.
   If target dirtiness or authority prevents this, retain the verified candidate
   and report collection pending. Never require `main`, missing recipes, a force
   update, or an unrelated dirty checkout to land the assigned result.
5. After actual publication/integration, rerun any acceptance that depends on the
   destination and read its revision back. Coordinator alone ticks observed boxes,
   records Result with evidence and final revisions, marks `done` only if every
   Check and child prerequisite passes, and removes only this pass's ownership.
   Native statuses are open/active/blocked/done/cancelled; reports remain evidence.
   Retain attempt artifacts until collection is verified; remove only a confirmed
   disposable clean/merged worktree when authorized. End this selected pass without
   dispatching unrelated or newly unblocked work.

## Check

The actual destination contains exactly the assigned result. Independent checks
passed on the published records or combined code revision, destination-dependent
checks passed, and MCP readback confirms the work's Result/status/evidence.
All children are finished or confirmed stopped before normal return. The report
explicitly distinguishes retained drafts, published documents and landed code.

## Failure

Failed verification prevents completion and retains the attempt. Stop dispatch
and publication on cancellation, deadline, stale revision or uncertain effects;
use the pass checkpoint's finite interruption/confirmation budget. Preserve
unknown effects and live worker IDs for reconciliation; never claim they stopped
without evidence. Cancelling the pass leaves wanted work open after safe shutdown;
cancelling the outcome uses cancelled with a reason. Preserve other actors' claims.
Record partial publication per file, or the exact target revision if integration
already occurred. Investigate before retry; rollback only this pass's changes with
current revision guards and concurrent-edit checks. A named external blocker may
justify blocked; otherwise failed wanted work returns open after safe ownership
release. No successful draft, commit or partial publication proves completion.
