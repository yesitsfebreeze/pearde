---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
capability-owner: contractors
work-kind: leaf
workflow: develop-one-cartridge
footprint: ["/Users/feb/dev/cartridge/contractors.ctg"]
needs: ["@root/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-workflows-validate-declared-events-requirements-and-agent-assignments", "@agent/contractor-agents-run-with-a-sealed-event-and-context-set"]
---

# Contractor workflows dispatch and recover bounded event runs

Execute validated PRD-ready workflows through declared event needs. Persist attempt identity before effects, bind predecessor outputs to parameters, and record attributed terminal results. Workers ask for missing requirements through the orchestrator; they cannot launch peers or widen grants.

## Acceptance

- [ ] Literal and predecessor-reference parameters reach the named event with scoped authority; disconnected ready steps may run within the admitted concurrency limit.
- [ ] A missing requirement suspends the dependent step. A separately admitted child workflow supplies a revision-bound artifact without changing the original worker's grants.
- [ ] Crash after an effect but before acknowledgment records unknown outcome and requires reconciliation; effectful calls are never blindly replayed.
- [ ] Cancellation, depth/count limits, aggregate budgets and writer conflicts prevent further dispatch and retain attributable receipts.

## Proof and recovery

Create a fake event peer and crash-injection fixture in `contractors.ctg/.cartridge/tests`. Implement receipt storage, binding, dispatch and dependency requests in separate modules. Exercise duplicate submission keys, conflicting keys, wrong-owner replies, output truncation, stale declaration revisions, cancellation races and suspended-worker deadlines. Use a finite DAG only: loops, arbitrary shell templates and automatic recursive expansion are excluded. Run the declared local tests before composition registration; afterward run `./task test contractors`, `./task check contractors` and `./task isolation` from root. An uncertain mutation is inspected through its owning service before retry. PRD remains the source of task readiness and write claims; contractors schedules only nodes inside an admitted workflow.

## Delivery boundary

This PRD tracks delivery of the cartridge feature. A contractor job is specified only by its event workflow, never by a separately maintained prose spec. Read the parent [workflow contract](../workflow.md) and this leaf's review.md before implementation. Existing claimed work retains ownership; reconcile overlapping source revisions before starting. Requirements remain unchecked until observed.
