---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
capability-owner: root
work-kind: leaf
workflow: develop-one-cartridge
footprint: ["/Users/feb/dev/cartridge/.cartridge/init.lua", "/Users/feb/dev/cartridge/.cartridge/config.lua", "/Users/feb/dev/cartridge/.cartridge/tests/integration/contractors-workflow.test.ts", "/Users/feb/dev/cartridge/.cartridge/bench/contractors", "/Users/feb/dev/cartridge/.cartridge/README.md"]
needs: ["@root/contractors-execute-bounded-jobs-through-an-orchestrator/planning-agents-produce-executable-contractor-workflows", "@prd/prd-collects-contractor-workflow-requirements-directly"]
---

# Contractor event workflows pass the composed dispatch proof

Register the new cartridge and prove the planner-to-workflow-to-contractor path against a disposable project. File A belongs to the first contractor; an unanticipated need for file B becomes a mediated request and a separate contractor assignment. The workflow is the sole execution contract throughout.

## Acceptance

- [ ] Planning sub-agents produce a validated workflow whose exact admitted revision runs through the real composed host and ordinary event boundaries.
- [ ] Direct and service-mediated access from A's worker to B is denied; the orchestrator dispatches B's worker and returns only its declared artifact.
- [ ] Independent verification rejects a stale input, forged receipt and extra changed path, then PRD collects the correct candidate.
- [ ] Crash ambiguity and cancellation preserve receipts without duplicate mutation; total planning, execution, verification and retry tokens and latency are reported.

## Proof and recovery

Create `.cartridge/tests/integration/contractors-workflow.test.ts` alongside `jev-workflow.test.ts` using temporary repositories and a deterministic fake router. Run `bun test .cartridge/tests/integration/contractors-workflow.test.ts`, `./task audit contractors`, `./task audit prd` and `./task isolation` from root. These proposed tests do not exist yet. Add a paired optional real-model benchmark using identical tasks, model and success gates; report median and tail latency plus total tokens, and make no speedup claim until measured. Runtime networking remains broker-only. Disabling the profile entry stops new admission while bounded active jobs drain or cancel; receipts survive. Do not replace or retire the existing tmux/proxy worker workflow.

## Delivery boundary

This PRD tracks delivery of the cartridge feature. A contractor job is specified only by its event workflow, never by a separately maintained prose spec. Read the parent [workflow contract](../workflow.md) and this leaf's review.md before implementation. Existing claimed work retains ownership; reconcile overlapping source revisions before starting. Requirements remain unchecked until observed.
