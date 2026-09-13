---
repo: /Users/feb/dev/cartridge/memo.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memo
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: landscape-composes-system-context
needs:
- '@landscape/landscape-composes-system-context/context-contributor-contract'
- '@landscape/landscape-composes-system-context/memory-context-contributor'
- '@memo/one-document-serves-every-reader/document-projections'
footprint:
- src/main.rs
- src/service.rs
- src/context.rs
- .cartridge/tests/integration/context.test.ts
- .cartridge/docs/context.md
commit: "3251566e6c92439e4a32c5ce8b734e55726801ee"
---

# The memo facade serves the shared context snapshot

Adapt host-bound document and Memory reads to the Landscape contributor contract
through an opt-in native memo context operation. The library owns composition;
the facade owns capability calls, trusted owner/cwd identity and request validation.
Keep legacy memo and model tool behavior compatible.

## Acceptance

- [x] Actual SDK requests return bounded attributable document and Memory evidence from one shared snapshot, without inference or tool execution.
- [x] Disabled, absent, empty, unavailable and timed-out sources remain distinct under one overall deadline; private content and callable metadata are excluded.
- [x] Exact reference readback returns the selected revision or explicit stale/unavailable status without a replacement semantic query.
- [x] Invalid requests and optional failures preserve existing records and provider state; no hidden retry, provider activation or transcript mutation occurs.

## Proof and recovery

Begin at memo src/service.rs and the shared Landscape context contract. Capture a
real native fixture baseline before specs. Verify SDK integration with synthetic
source providers and temporary documents, plus public memo and Landscape gates.
The library leaf alone cannot claim native integration. Preserve interrupted work;
external reads may complete after timeout but never publish a late snapshot.

## Review lineage

Split from @landscape/landscape-composes-system-context/context-contributor-contract
at its owner boundary, preserving inherited rounds1–2 and maximum5. Source history
and reviews remain linked; no review allowance was reset. Substantive facade plan
requires an independent round3 review before implementation.

Reverification: document identity/projections revalidated at3251566 after executable validation; native context SDK compatibility already passed, shared contributor contract unchanged.
