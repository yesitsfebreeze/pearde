---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
capability-owner: contractors
work-kind: leaf
workflow: develop-one-cartridge
footprint: ["/Users/feb/dev/cartridge/contractors.ctg"]
needs: ["@root/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-workflows-validate-declared-events-requirements-and-agent-assignments", "@root/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-workflows-dispatch-and-recover-bounded-event-runs"]
---

# Planning agents produce executable contractor workflows

A bounded planning workflow dispatches planner sub-agents against selected ASP declarations, memo procedures and input revisions. Their result is the workflow object itself: events, parameters, requirements and assigned agents. There is no prose specification to translate into execution later.

## Acceptance

- [ ] A planner result validates against the same schema consumed by the runner, and the admitted digest is the executed digest.
- [ ] A planner proposes only declared event payloads and explicit bindings; invented capabilities and acceptance by self-report fail validation.
- [ ] A bounded independent planning check catches a missing requirement or permission before any effectful event starts; child proposals cannot mint authority.
- [ ] JEV advice retains evidence and uncertainty; unavailable assessment is explicit, and existing authority plus validation still gates dispatch.

## Proof and recovery

Reuse agent run lifecycle, memo resolve/read and ASP event discovery through declared needs. Add deterministic planner-output fixtures to `contractors.ctg/.cartridge/tests`, including malformed, cyclic and oversized output. First verify the event names and envelopes returned by the current composition. A bounded live model evaluation is separate from these protocol tests and reports total tokens, latency and failures without asserting quality from fixture success. Run local declared tests, then root `./task test contractors`, `./task check contractors`, `./task isolation` once registered. Planning failure emits a diagnostic or dependency request; it neither runs a partial plan nor expands permissions. Memo procedures are authored through memo write and read back at their saved revisions.

## Delivery boundary

This PRD tracks delivery of the cartridge feature. A contractor job is specified only by its event workflow, never by a separately maintained prose spec. Read the parent [workflow contract](../workflow.md) and this leaf's review.md before implementation. Existing claimed work retains ownership; reconcile overlapping source revisions before starting. Requirements remain unchecked until observed.
