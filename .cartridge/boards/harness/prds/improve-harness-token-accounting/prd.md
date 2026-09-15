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
canonical-scope: improve-harness-token-accounting
footprint: ["src/inspection.rs","src/accounting.rs",".cartridge/tests/unit/accounting.rs",".cartridge/tests/integration/working.rs","Cargo.toml","src/main.rs","src/roster.rs",".cartridge/tests/unit/main/tests.rs",".cartridge/tests/unit/inspection_tests.rs",".cartridge/tests/unit/working_tests.rs",".cartridge/tests/unit/roster_tests.rs",".cartridge/tests/integration/roster.test.ts",".cartridge/docs/roster.md"]
commit: "698a4dc9555a6b3ad8d46dcc5dd3a14463048e70"
needs:
- "@router/improve-router-capability-routing"
---

# Show token estimates alongside serialized bytes

Remove capability-routing as a hard prerequisite. Use existing model metadata when known and explicit unknown/estimate otherwise. Preserve hard byte limits, reserve configured output capacity and keep complete tool exchanges. Later capability routing can enrich counts without blocking basic truthful inspection.

## Acceptance

- [x] Multilingual, JSON-schema and indivisible-exchange fixtures stay within byte safeguards while estimates identify tokenizer/model and uncertainty.
- [x] Unknown models produce unknown/estimated token counts, not zero or an inference call.
- [x] Provider-reported usage remains separately attributed and never silently replaces an estimate for a different assembled request.

## Proof and recovery

Start at [prompt.rs](../../../prompt.rs), [working.rs](../../../working.rs), [inspection.rs](../../../inspection.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test harness` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-harness-token-accounting`; maximum five rounds.

## Verified implementation — 2026-09-13

The harness gate passes 35 unit and 6 real-process integration tests. Fixtures
cover multilingual text, JSON schemas, complete tool calls, hard byte budget
refusal with reserved output headroom, unknown/model hints, changed projection
hashes, and interleaved per-run usage without credential propagation. The actual
inspector exposes a nonzero labelled estimate and still makes no model call.

## From the retired work memo

Folded 2026-09-15 from `work/improve-harness-token-accounting.md` (status open). The PRD state above is authoritative.

### Outcome

Context inspection reports model-specific estimates, observed provider usage and the source/uncertainty of each count while retaining byte safety limits.

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
- [ ] Fixtures include multilingual text, JSON/tool schemas and a large indivisible exchange; reported budgets remain honest and byte caps still apply.
- [ ] Unknown tokenizer/model yields an explicit unknown/estimate; inspection performs no inference or compaction.
- [ ] The scoped gates below pass with the new behavioral fixtures included; record
      exact commands, exit status, and concise results in Result. New fixtures belong
      to these existing test entry points; they are not claimed to exist yet.

### Approach

1. Inspect the footprint and related records; establish the failing fixture or baseline
   before editing. Keep the implementation within this outcome.
2. Use configured tokenizer support where available and labelled estimates otherwise; reserve output capacity and preserve complete tool exchanges. Do not claim an estimate is provider acceptance or send a model request merely to inspect.
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
Ready after [improve-router-capability-routing](../../../router/prds/improve-router-capability-routing/prd.md) are done with evidence.
Leave status open until a worker actually starts; then set owner and active.
Record Result and mark done only after the checks pass.
