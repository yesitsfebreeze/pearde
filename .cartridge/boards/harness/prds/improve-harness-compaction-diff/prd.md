---
repo: /Users/feb/dev/cartridge/harness.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: harness
work-kind: leaf
review-round: 3
review-status: accepted
canonical-scope: improve-harness-compaction-diff
footprint: ["src/main.rs","src/inspection.rs","src/compaction.rs",".cartridge/tests/unit/compaction.rs",".cartridge/tests/integration/working.rs","Cargo.toml","src/roster.rs",".cartridge/tests/unit/main/tests.rs",".cartridge/tests/unit/inspection_tests.rs",".cartridge/tests/unit/accounting.rs",".cartridge/tests/unit/working_tests.rs",".cartridge/tests/unit/roster_tests.rs",".cartridge/tests/integration/roster.test.ts",".cartridge/docs/roster.md"]
commit: "698a4dc9555a6b3ad8d46dcc5dd3a14463048e70"
---

# Inspect what each compaction retained and removed

The inspector shows original covered messages, resulting summary, retained tail and revision/time/usage evidence for a compaction.

## Acceptance

- [x] After two compactions, inspection maps each summary to its exact covered prefix and shows corrected user constraints in source and result.
- [x] A failed compaction retains the prior summary; requesting its comparison makes no model call and leaks no authorization headers.

- [x] Keep canonical transcripts intact. New metadata/inspection is additive; revert compaction settings without discarding old summaries or their source. Live evaluation requires separately configured models and a bounded budget.

## Proof and recovery

Start at [prompt.rs](../../../prompt.rs), [working.rs](../../../working.rs), [inspection.rs](../../../inspection.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test harness` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-harness-compaction-diff`; maximum five rounds.

## Verified implementation — 2026-09-13

`cargo test --manifest-path ../harness.ctg/Cargo.toml -p harness` passes 33 unit
and 6 real-process integration tests. The rolling-memory test performs two
compactions, compares exact source message arrays and original tails, checks a
corrected constraint in source and summary, timestamp/revision/numeric usage,
reload, and four failure modes with unchanged history and transcript. Inspection
leaves the router call count unchanged and excludes provider authorization data.
Legacy metadata gaps and changed-source comparisons have explicit diagnostics.
Malformed legacy text is retained during regeneration; unknown history versions
are refused. Historical comparisons grow with the number of retained summaries.

## Reverification — 2026-09-13

Token accounting ca7eeabd changes the shared inspector and working-memory
fixture. Reopened for the unchanged compaction-history proof; original receipt
retained in collection-a282c877.md. No acceptance is waived.

## From the retired work memo

Folded 2026-09-15 from `work/improve-harness-compaction-diff.md` (status open). The PRD state above is authoritative.

### Outcome

The inspector shows original covered messages, resulting summary, retained tail and revision/time/usage evidence for a compaction.

### Context

This is a planned improvement, not a claim that every subfeature is absent.
Baseline and limitations: [[cartridge-improvement-evidence]]. Follow
[[@prd/routine/plan-cartridge-work.md]] and read the current source before choosing implementation.
Related existing work (context/coordination, not automatically a hard dependency): [rolling-context-retains-decision-evidence](../../../root/prds/rolling-context-retains-decision-evidence/prd.md), [long-horizon-recall-benchmark](../../../root/prds/long-horizon-recall-benchmark/prd.md).

### Footprint

Harness; one observable outcome. The listed files are starting points and a proposed edit footprint, not permission to make unrelated changes.
All paths below are relative to /Users/feb/dev/cartridge.

- `harness.ctg/prompt.rs`
- `harness.ctg/working.rs`
- `harness.ctg/inspection.rs`
- `harness.ctg/inspection_tests.rs`
- `harness.ctg/eval/eval_compaction.py`

Tests/fixtures and owner-local documentation for this outcome may be added beside
these sources. Recheck active claims before changing shared files. Update cartridge.json
only when public services, schema, configuration or verification commands actually change.

### Check

- [ ] First reproduce or measure the current behavior for the Outcome using a disposable
      fixture; record revision, command, observed result and the remaining gap. If the
      behavior already satisfies the checks, preserve evidence and close the gap without
      rebuilding it.
- [ ] After two compactions, inspection maps each summary to its exact covered prefix and shows corrected user constraints in source and result.
- [ ] A failed compaction retains the prior summary; requesting its comparison makes no model call and leaks no authorization headers.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Build on canonical transcript and prefix hashes. Store bounded summary metadata and provide source drilldown instead of duplicating whole transcripts; distinguish semantic judgments from literal differences.
3. Implement the smallest compatible change, exercise the negative cases above, update
   the owner-local contract/documentation, then run the scoped gates.
4. At integration, test through the real consuming boundary in an isolated profile,
   not only a fake service. Record any retained limitation rather than claiming it solved.

### Verification

Run from `/Users/feb/dev/cartridge` after building the selected fixture prerequisites.
These are future implementation gates; no product-test pass is claimed by this plan.

```sh
just test harness
just check harness
python3 harness.ctg/eval/eval_compaction.py --check
```


### Compatibility and recovery

Keep canonical transcripts intact. New metadata/inspection is additive; revert compaction settings without discarding old summaries or their source. Live evaluation requires separately configured models and a bounded budget.

### Handoff

Priority P1; scope size M (S = one local change; M = a bounded cross-file
contract; L = investigation plus likely smaller slices, not a time promise).
No hard prerequisite inside this programme; ready for an owner after source/claim checks.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
