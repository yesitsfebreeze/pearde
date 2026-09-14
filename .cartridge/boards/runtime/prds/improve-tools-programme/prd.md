---
repo: /Users/feb/dev/cartridge/tools.ctg
state: open
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
