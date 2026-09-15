---
kind: work
description: "Deliver the three Workspace tools improvements with explicit risk coverage"
status: open
subwork:
  - "[improve-tools-preflight](../../../runtime/prds/improve-tools-preflight/prd.md)"
  - "[improve-tools-worktree-resume](../../../runtime/prds/improve-tools-worktree-resume/prd.md)"
  - "[improve-tools-bundle-provenance](../../../runtime/prds/improve-tools-bundle-provenance/prd.md)"
uses:
  - usage: "[[read-usage]]"
    when: ["planning tools improvements", "reviewing tools cartridge readiness"]
---

# Workspace tools improvement plan

## Outcome

Deliver the three improvements requested for Workspace tools, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

## Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Preview workspace-tool effects before execution | [improve-tools-preflight](../../../runtime/prds/improve-tools-preflight/prd.md) |
| 2. Recover interrupted worktree creation safely | [improve-tools-worktree-resume](../../../runtime/prds/improve-tools-worktree-resume/prd.md) |
| 3. Ship bundles with source and dependency provenance | [improve-tools-bundle-provenance](../../../runtime/prds/improve-tools-bundle-provenance/prd.md) |

## Downside coverage

1. Layout assumptions reduce portability: validate paths in preflight and name unsupported layouts.
2. Build dependencies still need management: detect missing prerequisites before mutation.
3. Wrappers hide recovery detail: return step-level evidence and resumable state.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

## Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [lane-rm-refuses-after-the-gates-run](../../prds/lane-rm-refuses-after-the-gates-run/prd.md), [lanes-do-not-poison-each-others-builds](../../prds/lanes-do-not-poison-each-others-builds/prd.md). Their current source, status and owner take precedence over a stale assessment.

## Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Workspace tools behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

## Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test tools
just check tools
just links
```

## Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
