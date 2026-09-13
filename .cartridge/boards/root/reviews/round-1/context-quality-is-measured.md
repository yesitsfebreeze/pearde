---
state: open
origin: requested
priority: 88
blast-radius: high
workflow: develop-one-cartridge
needs:
  - @landscape/landscape-composes-system-context
footprint:
  - /Users/feb/dev/cartridge/landscape.ctg/tests
  - /Users/feb/dev/cartridge/landscape.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/memory.ctg/tests/bench
  - /Users/feb/dev/cartridge/harness.ctg/eval
  - /Users/feb/dev/cartridge/memo.ctg/tests
---

# Landscape quality and cost are tested against a versioned corpus

Passing mechanics tests does not tell us whether the context contains the right facts, excludes stale ones, and stays small and fast.

## Ownership and scope

Owner: `landscape`. Participating repositories: `landscape.ctg`, `memory.ctg`, `harness.ctg`, `memo.ctg`. Coordinate from the root master board. Footprints are preliminary checkout-absolute paths so Pearde can detect cross-board overlaps; narrow and rebase them during analysis before claiming in another checkout.

## Implementation plan

1. Record an offline corpus of representative tasks: implementation discovery, memory-only fact, corrected decision, superseded memo, conflicting evidence, missing provider, directory-local instructions, and cross-session knowledge.
2. Store expected source IDs, indispensable facts, forbidden claims, and query/view/budget configuration. Capture the current component baselines before replacing them.
3. Measure candidate recall, selected-context relevance, provenance completeness, byte budget, deterministic ordering, contributor calls, and latency on fixed fixture sizes.
4. Use hard deterministic gates for critical facts, scope, provenance, and size; compare performance to measured baselines instead of inventing target milliseconds.
5. Separate optional real embedding/summarizer evaluation from offline fixtures. Record model, prompt, dataset, and source revisions so scores can be compared.

## Acceptance contract

- Every critical source/fact appears in its designated query context and each negative fixture excludes its forbidden item.
- Same snapshot/query yields stable results; deliberate source changes invalidate stale evidence.
- An unavailable contributor is distinguishable from no matches; every selected item has a resolvable source and revision.
- Context stays within configured byte limits with explicit omissions; source-call counts remain bounded as candidates grow.
- A deliberately damaged ranking/summary baseline fails a quality gate, proving the corpus is capable of detecting regression.

## Verification to turn into specs

Run from the composed repository root. These are proposed gates, not results. The analyst must probe commands and write executable `specs/specNN.md` gates with source revisions and expected outcomes before implementation.

```sh
just test landscape
just test memo
python3 harness.ctg/eval/eval_compaction.py --check
just test memory --test cartridge
```

## Failure and recovery

A test scores its own generated expected answer or measures fixture success as model quality. Keep independent facts/rubrics and separate offline/live reports.

Rollback: Keep baseline fixtures/results versioned and restore the previous selection policy if critical quality regresses. Never overwrite the corpus to bless a failure.

## Prior context

Related existing runtime memo leaf names: `rolling-context-retains-decision-evidence`. Resolve them under `cartridge.ctg/.cartridge/memos/` and inspect older `.pearde` work before changing scope; link superseded work explicitly. This PRD is the authoritative state for this new slice, not a copy of an older ticket.

## Evidence

No implementation evidence yet. The assessment provides the baseline. All new PRDs begin `open`; Pearde transition commands govern later states. Do not manufacture specifications, approvals, timings, claims, or passing results.
