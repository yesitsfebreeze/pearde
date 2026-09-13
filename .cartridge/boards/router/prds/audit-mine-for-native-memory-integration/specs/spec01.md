---
complexity: small
footprint:
  - .cartridge/docs/routing-handoff.md
  - .cartridge/docs/routing-handoff.json
  - .cartridge/tests/integration/routing-handoff.test.ts
---

# spec01 — Reconcile the retired native-Memory routing proposal

Produce an owner-local handoff and machine-readable disposition ledger covering
all original requirement sections, including routing, login, credentials,
configuration, transport, lifecycle, streaming, recovery, embeddings, plugins,
migration and historical evidence. Retain the original proposal and its commit
claims unchanged. Current Memory authority explicitly excludes model routing;
its pinned source uses configured reason/embed endpoints and has no src/mine.

Each requirement group names current source symbols at pinned revisions and is
classified existing owner boundary, bounded current gap or obsolete ownership
requirement. Existing boundaries are not claims of fully proved live behavior.
Map residual work to canonical root-board leaves or an explicitly bounded
unimplemented contract. Preserve historical test/live/installation claims as
historical, with unavailable imported objects labelled rather than fabricated.

Read Memory through pinned git objects so its concurrent working changes remain
outside this audit. Change router documentation and its audit validator only.
No credential relocation, user configuration inspection, daemon/service restart,
source deletion, live provider calls or revived router inside Memory.

## Acceptance

- [x] Every original section and behavior group maps to a current boundary, explicit gap or obsolete requirement with source references and history intact.
- [x] Pinned Memory startup/ingest/query endpoint path and absent mine dependency are verified; current router/provider source owns routing/login/recovery boundaries.
- [x] Validator checks source digests/symbols and original requirement coverage; documentation distinguishes actual tests, historical claims and unmeasured behavior.

## Verify and Proof

```sh
bun test ./.cartridge/tests/integration/routing-handoff.test.ts
```

No product implementation changes. Existing router35-test/check proof at0a216cb
is retained without inferring that a documentation check proves live deployments.
