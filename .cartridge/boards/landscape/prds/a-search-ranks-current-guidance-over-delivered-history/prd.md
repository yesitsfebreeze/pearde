---
repo: /Users/feb/dev/cartridge/memo.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: a-search-ranks-current-guidance-over-delivered-history
---

# Fabric search ranks current guidance above delivered history unless history is asked for

The memo `fabric` query ranks graph nodes in `memo.ctg/src/fabric_graph.rs` (`search`: name/when 3.0, tags 2.0, description 1.0, times `1 + ln(1 + uses)`) and ignores lifecycle, so done work memos whose names share query words outrank the routine that applies (measured 2026-09-12 in root `.cartridge/memos/work/a-search-ranks-current-guidance-over-delivered-history.md`). The landscape crate no longer exists; memo owns this ranker. Reuse the `status`/`superseded_by` vocabulary `memo.ctg/src/usage.rs` already emits; add no second ranker or store.

## Acceptance

- [ ] In a fixture holding `routine/repository-checks.md` and four `status: done` gate work memos, "run only the gates the change touches" returns the routine in the top five and "which gates do I run before committing" returns it first.
- [ ] With an explicit `intent: "history"`, done and superseded memos rank by match alone and each hit carries `status`; a demoted hit under the default `current` intent says why; an unknown intent is refused without results.
- [ ] Equal scores order by key; journal counts never lift a done memo above current guidance under `current` intent. A node without `status` ranks as current.

## Proof and recovery

Start: `memo.ctg/src/fabric_graph.rs`, `memo.ctg/src/graph.rs` (`memo_node` must carry `status`), `memo.ctg/src/service.rs` (fabric request), tests `memo.ctg/.cartridge/tests/unit/src/fabric_graph.rs`. First add both queries as failing unit cases and record the observed order. Gates from /Users/feb/dev/cartridge: `just test memo`, `just check memo` (not run for this plan). Excluded: `resolve` ordering, memory hits. Rollback: ranking is derived; reverting restores the prior order with record and journal untouched.

## Dependencies and review

No hard prerequisites. Target board after rehoming: memo. [Review history](review.md); rounds inherited, maximum five.
