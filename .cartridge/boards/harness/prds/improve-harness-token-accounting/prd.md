---
repo: /Users/feb/dev/cartridge/harness.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: harness
work-kind: leaf
review-round: 2
review-status: stale-after-migration
canonical-scope: improve-harness-token-accounting
footprint:
- /Users/feb/dev/cartridge/harness.ctg/prompt.rs
- /Users/feb/dev/cartridge/harness.ctg/working.rs
- /Users/feb/dev/cartridge/harness.ctg/inspection.rs
- /Users/feb/dev/cartridge/harness.ctg/inspection_tests.rs
- /Users/feb/dev/cartridge/harness.ctg/eval/eval_compaction.py
---

# Show token estimates alongside serialized bytes

Remove capability-routing as a hard prerequisite. Use existing model metadata when known and explicit unknown/estimate otherwise. Preserve hard byte limits, reserve configured output capacity and keep complete tool exchanges. Later capability routing can enrich counts without blocking basic truthful inspection.

## Acceptance

- [ ] Multilingual, JSON-schema and indivisible-exchange fixtures stay within byte safeguards while estimates identify tokenizer/model and uncertainty.
- [ ] Unknown models produce unknown/estimated token counts, not zero or an inference call.
- [ ] Provider-reported usage remains separately attributed and never silently replaces an estimate for a different assembled request.

## Proof and recovery

Start at [prompt.rs](../../../prompt.rs), [working.rs](../../../working.rs), [inspection.rs](../../../inspection.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test harness` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `improve-harness-token-accounting`; maximum five rounds.
