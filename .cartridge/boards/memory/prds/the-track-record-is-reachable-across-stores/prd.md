---
repo: /Users/feb/dev/cartridge/memory.ctg
state: open
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
