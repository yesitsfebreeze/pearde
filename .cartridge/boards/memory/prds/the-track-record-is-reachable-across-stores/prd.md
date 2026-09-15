---
repo: /Users/feb/dev/cartridge/memory.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: the-track-record-is-reachable-across-stores
---

# Cross-project recall asks only the stores a caller names, within a bound

`memory query --all` already fans out through the machine hub (`search` in `src/hub/src/lib.rs`; `SearchReq {text,k,live_only,root}` in `src/transport/src/hub_rpc.rs`). Each hit is labelled with its root, and failed roots are named in `skipped` while the answer stays ok. It queries every registered root, though, with no allowlist, no contributor bound and no store-qualified entity IDs. Cross-project reach through the local hub is in scope; cross-machine federation is void (memory decision `the-federation-tier-is-void-not-closed`). Outcome, owned by memory: `SearchReq.roots` (`memory query --root <path>`, repeatable) limits the fan-out to named registered roots, `hub.search_max_roots` bounds it, and hits carry a qualified `root:id`.

## Acceptance

- [ ] Two fixture stores holding the same claim text return two hits with distinct `root:id` values and sources, and each ID reads back exactly from its own store.
- [ ] A root not named in `roots` is never opened or asked, as the hub's per-root call record shows. An unregistered named root is refused. An unavailable named root appears in `skipped` within the query deadline while the other hits return.
- [ ] `--all` without `roots`, and single-store `query`, keep their current results. The fan-out performs no writes and makes no model calls beyond each root's normal query embedding.

## Proof and recovery

First probe: extend `.cartridge/tests/unit/src/hub/src/tests/hub_search_test.rs` with two temporary roots at `c25af4d` and record the current IDs and skip behaviour. Cartridge configuration disables hub auto-start (`src/cartridge.rs`), so this remains a CLI/hub outcome. Gates, run from /Users/feb/dev/cartridge/memory.ctg: `just check`, `just test` (not run). Rollback: ignore `roots`; the registry is unchanged.

## Dependencies and review

No hard needs. [Review history](review.md): rounds 1–2 inherited, round 3 rebased; maximum five.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--the-track-record-is-reachable-across-stores.md` (status open, estimate 2d). The PRD state above is authoritative.

> dated decisions, measurements and verdicts remain recallable across known local stores with provenance and explicit partial results

### Do

An agent opening a second local store can recall its dated decisions,
measurements and verdicts alongside the first store through the existing hub
and tool surface. Every result identifies its source store and claim origin;
an unavailable store produces an explicit partial-result condition without
losing the available results. Default per-cwd isolation remains intact until
the caller explicitly requests cross-store recall.

The record remains dated claims rather than raw transcripts. This reuses the
existing fold and local hub, not cross-machine gossip, replication or another
ledger format. No desktop shell is needed to prove engine-level federation.
