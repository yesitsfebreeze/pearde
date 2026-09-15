---
repo: /Users/feb/dev/cartridge/tools.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: runtime
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: improve-tools-programme
needs:
- '@runtime/improve-tools-preflight'
- '@runtime/improve-tools-worktree-resume'
- '@runtime/improve-tools-bundle-provenance'
---

# Workspace tools improvement plan

Coordinate the linked outcomes for the repository tooling that the `tools`
cartridge now owns (decision `tui-and-tools-are-cartridges`). The former
`cartridge.ctg/scripts/workspace.py` and `repositories.json` are gone (no-Python
layout decision); `bundle`, `lane`, `land` and `lane-rm` live in
`tools.ctg/src/service.rs`, tested by `tools.ctg/.cartridge/tests/unit/service/tests.rs`
and `tools.ctg/.cartridge/tests/integration/lane.test.ts`. Claim a leaf for
implementation; this parent records only combined evidence.

## Acceptance

- [ ] Each linked leaf passes its own review and observable acceptance against `tools.ctg/src/service.rs`.
- [ ] At one pinned tools.ctg and cartridge.ctg revision, `just test tools` and `just check tools` (cwd `/Users/feb/dev/cartridge`) pass with every leaf's fixtures included; record tested mitigations and remaining limitations.

## Work items

- [Preview workspace-tool effects before execution](../improve-tools-preflight/prd.md)
- [Recover interrupted worktree creation safely](../improve-tools-worktree-resume/prd.md)
- [Ship bundles with source and dependency provenance](../improve-tools-bundle-provenance/prd.md)

All three leaves share the footprint `tools.ctg/src/service.rs`; land them serially.

## Review

[Review history](review.md): round 3/5. The tools board is the natural home; board rehome is a coordinator decision.

## From the retired work memo

Folded 2026-09-15 from `work/improve-tools-programme.md` (status open). The PRD state above is authoritative.

> Deliver the three Workspace tools improvements with explicit risk coverage

### Outcome

Deliver the three improvements requested for Workspace tools, with observable evidence
and the three assessed downsides explicitly addressed. This item coordinates its
children; it is not a fourth implementation task. Evidence is in
[[cartridge-improvement-evidence]]; execution follows [[@prd/routine/plan-cartridge-work.md]].

### Work and coverage

| Assessment improvement | Implementation owner |
| --- | --- |
| 1. Preview workspace-tool effects before execution | [improve-tools-preflight](../improve-tools-preflight/prd.md) |
| 2. Recover interrupted worktree creation safely | [improve-tools-worktree-resume](../improve-tools-worktree-resume/prd.md) |
| 3. Ship bundles with source and dependency provenance | [improve-tools-bundle-provenance](../improve-tools-bundle-provenance/prd.md) |

### Downside coverage

1. Layout assumptions reduce portability: validate paths in preflight and name unsupported layouts.
2. Build dependencies still need management: detect missing prerequisites before mutation.
3. Wrappers hide recovery detail: return step-level evidence and resumable state.

These mitigations do not claim to eliminate inherent costs or make this component
independent of all other services. Retained limitations must be stated in Result.

### Order and coordination

Start with children whose needs are satisfied. Child dependencies are authoritative;
the table is a coverage view, not a second backlog. Claim one executable child at
a time and coordinate shared files before work begins. Scope sizes are not time estimates.

Existing records to reconcile before implementation: [lane-rm-refuses-after-the-gates-run](../../../root/prds/lane-rm-refuses-after-the-gates-run/prd.md), [lanes-do-not-poison-each-others-builds](../../../root/prds/lanes-do-not-poison-each-others-builds/prd.md). Their current source, status and owner take precedence over a stale assessment.

### Check

- [ ] Each child in subwork is done, with its exact commands and observed outcomes in Result.
- [ ] Each of the three downsides above has a tested mitigation or a clearly documented
      retained limitation tied to the child evidence.
- [ ] The integrated Workspace tools behavior passes the child gates and its real consuming
      boundary in a disposable profile; enabling the component does not silently widen
      a production tool surface or profile grant.
- [ ] Current owner-local contracts and relevant cartridge.json declarations match the
      delivered interface; old profile compatibility and recovery behavior are recorded.

### Verification

Run from `/Users/feb/dev/cartridge`. Reuse child test results where they cover the
same integrated revision; repeat only after changes or unresolved integration risks.

```sh
just test tools
just check tools
just links
```

### Handoff

Implementation is open and unclaimed. This planning pass did not execute these product
gates. Claim children when implementation starts, preserve unrelated work, and close
this parent only when every child and its integration checks are complete.
