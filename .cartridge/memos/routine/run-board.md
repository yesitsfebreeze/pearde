---
kind: routine
description: Continuously work one central PRD board using its dependency plan and host sub-agents
uses:
  - usage: "[[run-usage]]"
    when: [work the PRD board, run PRDs continuously, finish all PRDs, orchestrate the planning board]
---

# Run the board

## Inputs

An explicitly selected PRD board and authorization to implement it, the PRD tool,
available host collaboration tools, and a coordinator identity. Default board is
`root`, whose member aliases map to central records and separate code repositories.
Use this routine when asked to work PRDs continuously. The board is the only
work record: analysts follow [[spec-a-prd]], implementers [[implement-a-prd]]
and collection [[land-a-prd]].

## Do

1. Call PRD `scan`, `plan` and `next`. Read the selected PRDs and revision-bound
   review/specification context. PRD performs memory recall where configured;
   recalled facts are evidence, not authority to change a claim or dependency.
2. Reconcile existing claims, worker state, integration receipts and the current
   pass checkpoint before dispatch. Retain foreign ownership. Unknown side effects
   require inspection before retry. Run the root plan so cross-member prerequisites
   remain visible; do not dispatch from an isolated member scan that omits them.
3. Choose the ready dependency frontier and reserve only disjoint footprints.
   Respect host capacity and reserve a coordinator slot. Use the PRD engine's
   claim/brief operations; an explicit source repository must resolve successfully.
   PRD owns planning state; workers edit only assigned code worktrees or spec drafts.
4. Sequence analyst, implementer and an independent verifier for each leaf.
   Briefs name canonical board/PRD, source revision, allowed paths, acceptance checks,
   report location, actor and finite deadline. The analyst probes and prepares specs
   or proposes sub-PRDs through the existing refine/specification engine. Plans need
   an attributed agent review of at least90/100, no blockers and at most five rounds.
   Re-review migrated or changed contracts; historical scores do not approve new inputs.
5. The coordinator publishes accepted specs and dispatches implementation in an
   isolated worktree rooted in the mapped code repository. Workers return artifacts
   and observed checks. Use an independent verifier to check the actual resulting
   revision. Worker prose or process exit0 does not establish completion.
6. Collect through PRD's checked integration operation. Require real verification
   and integration evidence before marking done. PRD publishes the observed transition
   and stores verified outcomes through memory; a pending memory acknowledgment is
   reported separately from already-integrated code and is not blindly replayed.
7. Rescan after each collection, specification or split. Pick newly ready work and
   continue, including newly introduced sub-PRDs within the selected scope. Collect
   parent integration gates only after their required children pass. Never stop
   merely because the initial ready batch finished.
8. Keep a bounded checkpoint with selected scope, revisions, claim/worker IDs,
   attempts, deadlines, checked evidence, pending effects and next action. Continue
   across context compaction from these records. Stop when every in-scope PRD is
   verified and integrated, the user stops the run, or all remaining paths depend
   on external input. Report blocked separately from done.

## Check

The root scan and current records agree about completion. Every done transition has
acceptance and integration evidence. All dispatched workers finished or were
confirmed stopped; no unknown mutations are treated as collected. Dependencies,
source ownership and active claims remain intact. Runtime events describe observed
changes, and memory acknowledgments or pending writes are explicit.

## Failure

Use20-minute worker deadlines with at most one10-minute extension for observed
progress. Wait in intervals no longer than60 seconds and communicate progress.
On cancellation or deadline, stop new dispatch, interrupt owned workers and confirm
termination before releasing their claims. Preserve incomplete attempts and checkpoints;
never clear a foreign claim, reuse an unverified lane, or replay an uncertain collect.
An unavailable host collaboration API is a reported limitation. Terminal runs instead
use an explicitly configured external adapter through `prd run`; no MCP process
pretends to spawn this conversation's sub-agents.
