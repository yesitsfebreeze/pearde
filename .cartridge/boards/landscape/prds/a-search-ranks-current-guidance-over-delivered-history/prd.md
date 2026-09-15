---
repo: /Users/feb/dev/cartridge/memo.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
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

## From the retired work memo

Folded 2026-09-15 from `work/a-search-ranks-current-guidance-over-delivered-history.md` (status open, estimate 3h). The PRD state above is authoritative.

> The landscape's top five answer with the routine that applies, not with work memos whose names happen to carry the query's words

### Outcome

Asking the landscape how to do something returns the thing to do it with. A
routine that declares the situation outranks a delivered work memo whose name
happens to share words with the query, and a `done` or `cancelled` memo never
outranks current guidance on the same subject.

Scope is ranking. What is indexed is [one-search-covers-the-record-and-memory](../one-search-covers-the-record-and-memory/prd.md);
this is what order it comes back in.

### Check

- [ ] "run only the gates the change touches" returns `routine/repository-checks`
      in the top five; today it returns four delivered work memos and a fifth
      that matched on the word "only".
- [ ] "which gates do I run before committing" still returns that routine first —
      the query that already works does not regress.
- [ ] A memo with `status: done` ranks below a memo of the same match strength
      without one, and the hit says so, so a caller can see why it was demoted.
- [ ] A name matching two query words does not outrank a declared `when:` phrase
      that matches the situation; the ranker's own tests carry both cases.
- [ ] `cargo test -p landscape` passes.

### Approach

Measured 2026-09-12 against the live record, 463 memo nodes, mirroring
`landscape::search` exactly (same tokens, same STOP list, same field weights
name 3.0 / when 3.0 / description 1.0):

```
Q: which gates do I run before committing
    9.0 [routine] routine/repository-checks.md — when: before,committing; description: before,gates,run
    8.0 [work]    work/gates-run-in-a-lane.md — name: gates,run
    8.0 [work]    work/lane-rm-refuses-after-the-gates-run.md — name: gates,run

Q: run only the gates the change touches
    8.0 [work]    work/gates-run-in-a-lane.md — name: gates,run
    8.0 [work]    work/lane-rm-refuses-after-the-gates-run.md — name: gates,run
    7.0 [work]    work/the-run-is-a-stream-of-typed-events.md — name: run
    6.0 [work]    work/fresh-checkouts-can-run-the-gates.md — name: gates,run
    6.0 [work]    work/lua-only-core-boundary.md — name: only; when: only
```

The same question phrased two ways answers correctly once and not at all the
second time. Three defects, each visible in that output:

1. Delivered history ranks as current. Those four work memos are `done`; the
   record already carries `status`, and the resolver already refuses to read a
   done item as current prose — the ranker does not use it at all.
2. A name is scored as a bag of words at the same weight as a declared
   situation, so two coincidental words in a hyphenated name beat a `when:`
   phrase written for exactly this question.
3. The STOP list is short enough that "only" scores. It holds fifteen words
   against a record whose vocabulary is this dense.

The standing multiplier from the observation journal is the right lever for a
fourth effect and already exists — used guidance rising — but it cannot fix
ordering that is wrong before any observation lands.

Worth building on the measurement rather than on taste: the script that produced
the table above is twenty lines and mirrors the Rust, so a change to the weights
can be checked against real queries before it ships.
