---
state: open
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/prd.ctg"
capability-owner: prd
work-kind: leaf
workflow: develop-one-cartridge
footprint: ["/Users/feb/dev/cartridge/prd.ctg/src/lifecycle.ts", "/Users/feb/dev/cartridge/prd.ctg/src/collection-proof.ts", "/Users/feb/dev/cartridge/prd.ctg/src/coordinator.ts", "/Users/feb/dev/cartridge/prd.ctg/.cartridge/tests", "/Users/feb/dev/cartridge/prd.ctg/README.md", "/Users/feb/dev/cartridge/prd.ctg/.cartridge/help.md", "/Users/feb/dev/cartridge/prd.ctg/.cartridge/docs/README.md"]
needs: ["@root/contractors-execute-bounded-jobs-through-an-orchestrator/contractor-workflows-dispatch-and-recover-bounded-event-runs"]
---

# PRD collects contractor workflow requirements directly

PRD accepts an immutable contractor workflow as the task's executable specification and consumes its requirement checks directly. It preserves existing claims, footprint checks, dependency verification and committed collection receipts. Existing Markdown contracts remain supported for unrelated tasks; contractor workflows never gain a separately maintained Markdown spec.

## Acceptance

- [ ] Every requirement maps to an independently observed check bound to workflow, attempt, candidate artifact and input revisions.
- [ ] Agent exit, a passing textual claim or a start acknowledgment cannot mark a task complete; stale evidence and extra changed paths refuse collection.
- [ ] Conflicting writers, replayed receipts and a changed workflow are refused; a permitted child result is integrated only after its own checks pass.
- [ ] Existing Markdown-spec collection and explicit committed re-verification retain their behavior.

## Proof and recovery

Begin at `src/lifecycle.ts` verificationBlocks/specs/collect, `src/collection-proof.ts` and `src/coordinator.ts`; narrow these discovery paths after inspecting the current revisions. Probe workflow-only publication, claim and readiness before collection; none may demand a Markdown spec. Add a structured workflow verification adapter and temporary-repository tests in `.cartridge/tests`. Require independent verifier identity, trusted assertion evaluation and candidate-bound evidence rather than contractor self-certification. Run `bun run check` and `bun run test` with cwd prd.ctg, then root `./task audit prd` and `./task isolation`. Cancellation or a failed requirement leaves the task incomplete and preserves evidence. Register contracts atomically; retry collection only with reconciled source and workflow revisions.

## Delivery boundary

This PRD tracks delivery of the cartridge feature. A contractor job is specified only by its event workflow, never by a separately maintained prose spec. Read the parent [workflow contract](../../../root/prds/contractors-execute-bounded-jobs-through-an-orchestrator/workflow.md) and this leaf's review.md before implementation. Existing claimed work retains ownership; reconcile overlapping source revisions before starting. Requirements remain unchecked until observed.
