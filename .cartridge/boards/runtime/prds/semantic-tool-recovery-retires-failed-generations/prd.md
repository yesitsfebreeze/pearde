---
repo: /Users/feb/dev/cartridge/cartridge.ctg
state: deferred
deferred-from: open
deferred-on: "2026-09-15"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: runtime
work-kind: leaf
review-round: 3
review-status: needs-decision
canonical-scope: semantic-tool-recovery-retires-failed-generations
---

# semantic-tool-recovery-retires-failed-generations

Rehome editor/LSP provider lifecycle to the actual host tooling owner; current memory scope excludes that automation. First identify a concrete maintained provider and teardown API before implementation. Preserve generation-safe cancellation and the positive-control distinction between unavailable/indexing and a genuine empty result.

## Acceptance

- [ ] A failed initialization is retired before another query can select it; retry creates one new owned generation.
- [ ] A stale callback cannot invalidate its healthy successor and cancellation waits for owned teardown without touching another session's editor.
- [ ] If no current maintained provider can be identified, this remains a named ownership question rather than invented memory work.

## Proof and recovery

Start at [runtime.rs](../../../../../../cartridge.ctg/src/runtime.rs), [service.rs](../../../../../../cartridge.ctg/src/service.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test runtime` from the composed root with the acceptance fixtures. These gates have not run for this plan.
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `semantic-tool-recovery-retires-failed-generations`; maximum five rounds.

## From the retired work memo

Folded 2026-09-15 from `@prd/work/memory--semantic-tool-recovery-retires-failed-generations.md` (status open, estimate 4h). The PRD state above is authoritative.

> Failed editor or language-server generations cannot poison later queries or leave owned analyzer processes behind

### Do

A failed or interrupted semantic-service initialization does not leave later
queries waiting on a permanently rejected or pending generation. Recovery waits
for owned teardown, preserves cancellation, and prevents stale callbacks from
invalidating a healthy replacement. Service retirement affects only processes
whose ownership is established, never another session's editor or unsaved work.

The existing harness already has failed-readiness eviction and teardown barriers;
the shared editor should obtain the same lifecycle guarantees without a duplicate
provider framework. [the-warm-lsp-times-out](../../../memory/prds/the-warm-lsp-times-out/prd.md) completed an investigation, not a
lifecycle repair. [the-lsp-answer-asks-a-positive-control](../../../memory/prds/the-lsp-answer-asks-a-positive-control/prd.md) already protects empty
answers and must remain intact: unavailable or indexing is not no references.

This work requires evidence of the affected ownership boundary before any repair.
It does not authorize machine-wide process cleanup or weaken semantic fallback.
