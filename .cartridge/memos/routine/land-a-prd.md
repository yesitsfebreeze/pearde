---
kind: routine
description: Collect one worked PRD with independent verification and serial integration before it is marked done
uses:
  - usage: "[[run-usage]]"
    when: [a worker reports DONE and the coordinator collects it, integrating a verified code attempt, running prd collect]
    tags: [landing, prd]
---

## Inputs

One PRD reference and revision with its specs and Acceptance; the implementer's
report and artifact revisions; the exact footprint; current review and
prerequisite evidence; the coordinator checkpoint; and the owning `repo` target.
Only the coordinator integrates code or runs `prd collect`.

## Do

1. Re-read the live PRD, its review, `needs`, claim and the target revision.
   Inspect the report and the actual diff; reject unrelated paths, unexplained
   changes, stale inputs and failed Acceptance. Worker DONE is an input, not
   `state: done`. Reconcile an earlier collection attempt before mutating anything.
2. Assign a separate verifier with the PRD, revision, artifacts, footprint,
   cwd and commands, finite deadline and report path. The verifier reruns the
   observable checks and distinguishes executed results from walkthroughs.
3. Inspect the target's current HEAD and status and the attempt's base. Preserve
   unrelated dirty work. Prepare the combined result in an isolated integration
   worktree at the target revision: cherry-pick only the assigned commits in
   order, resolve in-scope conflicts, rerun Acceptance and the owner gates on the
   combined revision, and have the verifier check that same result. Recheck HEAD
   before advancing it; if it moved, rebuild and reverify. Advance a clean,
   approved target with explicit Git commands such as
   `git -C <target-worktree> merge --ff-only <integration-branch>`. If dirtiness
   or authority prevents this, keep the verified candidate and report collection
   pending. Never force-update or land into an unrelated dirty checkout.
4. Run `prd collect <ref>` with the verification evidence. It ticks nothing on
   trust: it refuses without published specs, executable verification and a
   clean claim, and it records the commit it observed. Retain attempt artifacts
   until collection is verified; remove only a confirmed merged worktree when
   authorized. End this pass without dispatching unrelated work.

## Check

The target contains exactly the assigned result. Independent checks passed on
the combined revision, destination-dependent checks passed, and `prd read`
shows `done` with the observed commit. Every child worker finished or was
confirmed stopped before return. The report separates retained drafts,
published specs and landed code.

## Failure

Failed verification keeps the PRD claimed or returns it through `release` with
the failure recorded; it never becomes done. Stop integration on cancellation,
deadline, stale revision or uncertain effects. Preserve unknown effects and
live worker IDs; never report them stopped without evidence. Record partial
integration by exact target revision. Investigate before retry and roll back
only this pass's changes. A named external prerequisite justifies `blocked`;
otherwise the attempt is preserved and the claim released.
