---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: landscape
work-kind: rollup
review-round: 2
review-status: stale-after-migration
canonical-scope: landscape-composes-system-context/live-file-context-contributors
needs:
- "@memo/landscape-file-kernel-context-facade"
- "@memo/landscape-live-owner-context-facade"

---

# File and live context retain owner and freshness

Adapt existing file/kernel/live sources to the shared row contract without starting inactive providers.

## Acceptance

- [ ] A fixture returns separately attributable file and kernel hits.
- [ ] Source edits invalidate affected cursors while unchanged rows retain identity.
- [ ] Removed or inaccessible sources return explicit availability within the shared budget.

## Proof and recovery

Start at [lib.rs](../../../../../../../landscape.ctg/src/lib.rs), [surface.rs](../../../../../../../landscape.ctg/src/surface.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test landscape` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `landscape-composes-system-context`; maximum five rounds.

## Owner split and freshness interpretation

The original three acceptance checks above remain preserved. Current shared context uses exact references/readback and Prepared revision, not cursors. Per coordinator review, source edits must invalidate affected exact readback/prepared revisions; frozen inventory cursors retain their separate observed-name snapshot contract. No speculative paging is introduced.

FS owns exact readonly file snapshots; Landscape owns shared file/kernel adapters; memo owns native integration. Historical session and terminal metadata become explicit owner prerequisites, and existing @router/improve-router-route-explanation supplies the router capability boundary. Separate Landscape and memo follow-ups integrate those sources; this parent remains open until those live-source outcomes also pass. See work-map-proposal.json. No duplicate router work item is added.
