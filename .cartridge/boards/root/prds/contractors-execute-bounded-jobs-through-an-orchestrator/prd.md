---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
capability-owner: contractors
work-kind: parent
workflow: develop-one-cartridge
needs: ["@runtime/contractor-workers-receive-immutable-job-capabilities", "@agent/contractor-agents-run-with-a-sealed-event-and-context-set", "@prd/prd-collects-contractor-workflow-requirements-directly"]
---

# Contractors execute planner-produced event workflows

`contractors.ctg` validates and executes bounded workflows composed by planning sub-agents from the current declared event surface. A workflow contains events with parameters, requirements and agent assignments; it is the executable specification. Memo supplies reusable procedures, JEV advises from ASP evidence, PRD owns task dependencies and verified collection, and the host enforces immutable job capabilities.

## Delivery slices

- admission: `@root/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-workflows-validate-declared-events-requirements-and-agent-assignments`.
- host: `@runtime/contractor-workers-receive-immutable-job-capabilities`.
- agent: `@agent/contractor-agents-run-with-a-sealed-event-and-context-set`.
- runner: `@root/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-workflows-dispatch-and-recover-bounded-event-runs`.
- planner: `@root/contractors-execute-bounded-jobs-through-an-orchestrator/planning-agents-produce-executable-contractor-workflows`.
- collect: `@prd/prd-collects-contractor-workflow-requirements-directly`.
- proof: `@root/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-event-workflows-pass-the-composed-dispatch-proof`.

## Integration gate

- [ ] Every delivery leaf is collected with its observed checks.
- [ ] One planner-produced event workflow completes the two-file dependency proof, including denied cross-scope access, stale-result refusal and crash reconciliation.
- [ ] End-to-end token and latency measurements include planning and verification; no speed claim rests on smaller worker prompts alone.

## Authority and evidence

[Workflow contract](workflow.md) defines the proposed version-one representation and boundaries. [Example workflow](workflow.example.json) is a design fixture, not currently dispatchable. Each delivery leaf has its own acceptance and review; this parent is only the integration index. No implementation has been started.

The older `@agent/the-agent-spawns-wakes-and-owns-sub-agents` is deferred to `@root/a-worker-launches-in-tmux-through-the-proxy`; preserve that separate external-worker workflow and its claims. Current agent start has no per-run capability contract. Host confinement exists but includes its root in readable paths. JEV assessment timed out and ASP PRD search was partial; local source and native PRD plan were used as evidence.

The explicit planning request does not reorder or claim higher-ranked agent/harness work. Contractors is not enabled and has no maturity ranking yet. The first bounded work is admission and host capability investigation; overlapping claimed footprints remain held.
