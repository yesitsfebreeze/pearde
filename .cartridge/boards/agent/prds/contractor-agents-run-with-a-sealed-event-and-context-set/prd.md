---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/agent.ctg"
capability-owner: agent
work-kind: leaf
workflow: develop-one-cartridge
footprint: ["/Users/feb/dev/cartridge/agent.ctg/src", "/Users/feb/dev/cartridge/agent.ctg/.cartridge/tests", "/Users/feb/dev/cartridge/agent.ctg/cartridge.json", "/Users/feb/dev/cartridge/agent.ctg/README.md", "/Users/feb/dev/cartridge/agent.ctg/.cartridge/help.md"]
needs: ["@runtime/contractor-workers-receive-immutable-job-capabilities"]
---

# Contractor agents run with a sealed event and context set

Reuse the existing agent engine in the host's isolated per-contractor composition. Its configured tools, model route, context packet, sessions and budgets are fixed for that instance. The shared conversational agent remains unchanged. This creates no second inference loop and does not interpret current start arguments as per-job isolation.

## Acceptance

- [ ] The worker's advertised and dispatchable tools equal its admitted event set; forged context/session identity and out-of-scope resource parameters fail at the broker.
- [ ] Only selected revision-bound memo and ASP evidence enters the worker context; ambient workspace configuration, recursive JEV calls and whole-ASP recall cannot widen it.
- [ ] Start acknowledgment is distinguished from matching terminal run completion, with a bounded structured result and source revision.
- [ ] Inference and checkpoint traffic use the authenticated broker; cancellation and turn/token/time limits have observable terminal outcomes.

## Proof and recovery

Inspect `agent.ctg/src/lib.rs`, `src/module.rs`, `src/model_loop.rs`, `src/context.rs` and `.cartridge/tests/integration/loop.rs`. First prove existing start accepts only prompt/session/model and tools are instance configuration. Add a sealed worker fixture using the host launch surface and deterministic fake router, then wire the existing loop to that composition. Resolve any harness-specific change as an owner-board prerequisite before touching harness code. Reconcile the currently claimed event-declaration work before sharing files. Gates from root: `env -u CARTRIDGE_YOLO ./task test agent`, `./task check agent`, `./task isolation`. The sealed-worker fixture must prove that an empty event set stays empty rather than falling back to resolved needs. The host cancels unknown workers; no unsandboxed or ambient-context fallback is permitted. Narrow the discovery footprint before implementation.

## Delivery boundary

This PRD tracks delivery of the cartridge feature. A contractor job is specified only by its event workflow, never by a separately maintained prose spec. Read the parent [workflow contract](../../../root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/workflow.md) and this leaf's review.md before implementation. Existing claimed work retains ownership; reconcile overlapping source revisions before starting. Requirements remain unchecked until observed.
