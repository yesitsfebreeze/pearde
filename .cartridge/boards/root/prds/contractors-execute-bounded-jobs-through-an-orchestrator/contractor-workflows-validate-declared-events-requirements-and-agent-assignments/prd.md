---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge"
capability-owner: contractors
work-kind: leaf
workflow: develop-one-cartridge
footprint: ["/Users/feb/dev/cartridge/contractors.ctg"]
---

# Contractor workflows validate declared events, requirements and agent assignments

Create `contractors.ctg` as the owner of validated contractor workflow execution. Its first slice admits a versioned event DAG without dispatching effects. Memo supplies authoring procedures; ASP supplies event declarations; PRD retains task dependencies and ownership. The proposed schema and public surface live in the parent workflow contract.

## Acceptance

- [ ] Validation resolves declared event names, payload schemas and parameter bounds; undeclared or ambiguous callable events are refused before dispatch.
- [ ] Cycles, missing predecessors, output-reference errors, unassigned agents and requirements without deterministic checks fail with the offending node named.
- [ ] Validation binds workflow, event declarations, input files, selected memo bodies, tool configuration and grants to a receipt; validation never authorizes execution.
- [ ] The new cartridge declares its whole surface and documents validate, run, status, cancel and dependency requests in README.md and .cartridge/help.md.

## Proof and recovery

First inspect `cartridge.ctg/docs/asp.txt`, `fs.ctg/cartridge.json` and `prd.ctg/src/planner.ts`; consume them through declared interfaces at runtime. Create schema and admission fixtures under `contractors.ctg/.cartridge/tests`, with one valid workflow and one negative case for each acceptance rule. Add local test/check commands to its manifest. From the composition root, future gates are `./task test contractors`, `./task check contractors`, `./task audit contractors`, and `./task isolation`; they cannot run until the cartridge exists and registration is delivered. Before registration, run its declared local commands directly. Failure writes no run record. No second planner, event catalogue, inference loop or arbitrary expression language is introduced.

## Delivery boundary

This PRD tracks delivery of the cartridge feature. A contractor job is specified only by its event workflow, never by a separately maintained prose spec. Read the parent [workflow contract](../workflow.md) and this leaf's review.md before implementation. Existing claimed work retains ownership; reconcile overlapping source revisions before starting. Requirements remain unchecked until observed.
