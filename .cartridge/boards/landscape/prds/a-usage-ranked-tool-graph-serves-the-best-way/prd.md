---
repo: /Users/feb/dev/cartridge/landscape.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: a-usage-ranked-tool-graph-serves-the-best-way
---

# a-usage-ranked-tool-graph

Reconcile delivered child work against the existing Landscape library and observation journal. Keep a single derived ranker and no new durable ranking service. The remaining outcome is demonstrable consistent tool/routine/memo selection through real consumers.

## Acceptance

- [ ] Each named older child maps to a current symbol/test or a specific residual gap with source revision.
- [ ] A controlled observation changes standing for equally relevant candidates while stale/private sources retain their constraints.
- [ ] Memo resolve, discovery and agent selection use the agreed ranking boundary; completed child implementations are reused rather than ported twice.

## Proof and recovery

Start at [lib.rs](../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `a-usage-ranked-tool-graph-serves-the-best-way`; maximum five rounds.
