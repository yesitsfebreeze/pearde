---
state: open
origin: requested
priority: 50
repo: "/Users/feb/dev/cartridge/router.ctg"
work-kind: leaf
canonical-scope: measured-model-ledger
---

# Model selection reads a measured cost and latency ledger

`router.ctg` selects a provider and builds a launch command from a catalog: what a model is declared to be. Nothing records what a model turned out to cost or how long it took, so a selection cannot improve from use and a role cannot be matched to the model that actually serves it.

Record an observation per turn — model, cost, latency, outcome — and let selection read it. A declared capability still bounds what a model may be chosen for; the ledger decides among the ones that qualify. Observations age: a ledger entry past its declared freshness is re-probed rather than trusted, so a provider that changed under the composition is noticed instead of being averaged over.

## Acceptance

- [ ] Every completed turn records one observation naming model, measured or estimated cost, latency and outcome, and a failed turn is recorded as failed rather than dropped.
- [ ] A selection among models that all satisfy the declared capability reports which observation led to its choice.
- [ ] An entry older than its declared freshness is re-probed before it is used, and the re-probe replaces it.
- [ ] A model with no observations is selectable and reported as unmeasured, not ranked last by an absent measurement.
- [ ] The ledger is readable as a report naming each model's observation count, cost and latency.
- [ ] Recording, ageing, and selection are tested offline in `just test router` with a scripted provider; no live provider is called.

## Proof and recovery

Mechanism from `/Users/feb/dev/pi/packages/coding-agent/src/core/model-ledger.ts` (288 lines at survey, verified present), which records per-model cost and latency observations, classifies models by role against a registry, and re-probes past a configurable staleness.

Reconcile at implementation with `@router/improve-router-cost-latency` and `@router/improve-router-capability-routing`, which are the existing children on this surface — this may be the implementation of one of them rather than a fourth item; decide that in analysis before claiming.

Gates, cwd `/Users/feb/dev/cartridge`: `just test router`, `just check router`. Not run for this plan.
