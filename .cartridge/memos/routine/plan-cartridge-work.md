---
kind: routine
description: Turn an assessment into bounded work with evidence, dependencies, runnable checks, and a verified handoff
uses:
  - usage: "[[run-usage]]"
    when: [planning cartridge improvements, turning an assessment into executable work, preparing an implementation handoff, reviewing all open work items, rating and improving a plan]
  - usage: "[[compose-usage]]"
    when: [writing a work plan, splitting an assessment into work items]
---

# Plan cartridge work from evidence

> "User rating from 0 to 100. Everything below 90 will fail and you can do up to 5 turns per plan"
> Scope: "All the open work items." Follow-up: "Record this method of improvement and integrate it into the workflow."

Superseding user instruction, 2026-09-13: "i dont rate, you do". Agents now
perform the ratings. An attributed agent score of at least 90 with no blocking
findings passes the review gate; no numeric user rating is requested or invented.
Preserve actual user feedback, historical scores and the five-round limit.

Recorded user method, updated 2026-09-13. Apply the shared
[plan review method](../../workflows/review-plan.md) and
[review history template](../../templates/review.md).

## Inputs

The user request, dated assessment, current source and manifests, applicable AGENTS.md,
existing work and ownership, and the current profile. Read the
[PRD template](../../templates/prd.md) and type/question.md before authoring. Planning is complete when another
worker can select a ready item, implement it, and prove its outcome without this
conversation and the current revision has passed the recorded plan review.
Implementation remains open until its acceptance evidence exists.

## Do

1. Resolve relevant work before creating anything. Read status and owner. Reuse a
   matching open item; extend completed work only for a demonstrable new gap. Link
   historical evidence without treating old paths, scores, or test counts as current.
   Do not change another worker's claim or silently supersede their scope.
2. Separate live observations, source findings, reported evidence, and proposals.
   Reproduce a suspected defect first. A suggested improvement is not proof that
   its underlying behavior is absent.
3. Name one observable outcome per executable work item. Add a concrete trigger
   and expected response, current behavior, exact starting files, excluded scope,
   failure cases, migration/compatibility effects, and a rollback boundary.
4. Split independent outcomes into child work. Set needs only for hard prerequisites;
   prose links indicate context. Keep the graph acyclic. A parent is a roll-up,
   never an additional implementation task. Identify shared source footprints:
   independent outcomes touching the same file still need coordinated landing.
5. Give each leaf a first verification/reproduction step, implementation sequence,
   unchecked observable acceptance criteria, and actual repository gate commands
   with cwd. If a fixture does not exist, explicitly require creating it in the
   existing test entry point; never claim a future command already runs.
6. Resolve technical choices through bounded investigation with a recommended default
   and a stop condition. Use a question memo only when a material unanswered choice
   truly prevents progress. Do not invent user approval or calendar estimates.
   Sizes S/M/L describe scope, not elapsed time; split L after the first probe.
7. State risks and mitigations, dependency failure behavior, cancellation and retry
   behavior where relevant, and whether a live model or private store is needed.
   Prefer isolated fixtures and offline gates. Define measurable quality criteria
   before a model evaluation; distinguish fixture correctness from model quality.
8. Write through memo write, with expected_revision when revising a read memo.
   Create prerequisites before dependents. Set new implementation work to open,
   without an owner. Claim active work only when implementation starts.
9. Read the saved record back. Check every new link, DAG, source pointer, coverage
   of the request, and root-to-leaf reachability. Identify the first ready items
   and the next integration gate. Record validation separately from product tests.
10. Before implementation, review and improve each plan independently using the shared
    method. Record an attributed agent review against the presented plan/spec
    revision. Its score must reach 90/100 with no blocking findings; missing agent
    review stays pending. Ratings are delegated to the agent, not requested from the user. Allow at most five substantive review rounds
    per plan across sessions, retaining the count when scope is moved or split.
    Revise failures within authorization, validate changed contracts, and obtain
    the next agent review against the concrete revision. Stop automatic revisions after
    a failed fifth round; never reset counts or fabricate acceptance. Existing
    OPEN-WORK-REVIEW entries retain their historical round-1 evidence and counts;
    their old pending-user fields do not impose the superseded rating gate.
11. During execution, capture revision, exact command, exit status, and concise
    observed outcome. Mark done only after checks and prerequisites pass; update
    Result. A passed older suite, a commit, or a planning document is not completion.

## Check

- A canonical centrally stored review history records the current input digests, findings,
  substantive revisions, rounds used and actual user feedback. The attributed
  agent score is at least 90, all blocking findings are resolved, and at most five
  rounds were used. A green structural validator alone does not prove this gate.

- The saved record passes validated memo writes and can be read through
  `{"op":"read","path":"work/<name>.md"}`.
- Every requested improvement and downside maps to a child outcome or an explicit,
  reasoned limitation; no requirement disappears between assessment and plan.
- A dependency walk over `needs` and child PRDs has no missing targets or cycles.
- Every leaf has unchecked checks and scoped commands such as `./task test memo`
  and `./task check memo`, executed from /Users/feb/dev/cartridge when appropriate.
- The handoff names ready work, shared footprints, success measures, and what was
  actually verified in this planning pass.

## Failure

A failed, pending or stale plan review keeps dependent implementation pending. A
failed fifth round records exhaustion and remaining gaps; other plans can proceed
independently. Substantive changes invalidate the previous revision's acceptance.
Preserve review history separately from PRD implementation state.

On stale revision, re-read and reconcile; never overwrite concurrent changes.
On validation failure, correct the declaration and retry through the same service.
If a source or test command is missing, fix the plan before handing it off.
If an observed blocker is policy or another live store owner, preserve that boundary
and plan an isolated reproduction; do not relax policy or stop someone else's process.
Use isolated branches/worktrees for memory implementation as memory.ctg/AGENTS.md requires.
