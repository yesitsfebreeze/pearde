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
