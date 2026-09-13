---
complexity: small
footprint:
  - .cartridge/tests/integration/tests.rs
  - .cartridge/docs/shadowing.md
---

# spec01 — Verify intentional local precedence with distinct shipped identities

The existing canonical parser validates local leaf uniqueness separately from
qualified shipped identities. Reuse it. Add one merged-record regression fixture
with two shipped owners sharing a basename. Before a local definition exists,
shorthand resolution must diagnose ambiguity. An explicit local write with those
same records loaded must save and become the legacy unqualified read, while both
qualified shipped paths and bytes remain distinct. Update the local memo using
its expected revision and prove its revision changes.

In that same merged view, reject another local kind using the same leaf, a stale
expected revision and writes directly to either shipped path. Assert all three
physical records remain byte-for-byte unchanged after every rejection. Document
that workspace precedence affects local shorthand; it does not merge or overwrite
owner-qualified documents. This is proof of the current parser contract, not a
new permissive duplicate rule.

## Acceptance

- [x] A merged-view local shadow saves and its unqualified read/revision advances; both owner-qualified original records remain readable and unchanged.
- [x] Ambiguous shipped shorthand is diagnosed before the local write; local precedence selects only the local path after it. Distinct owner identities survive listing.
- [x] Duplicate local leaf, stale local revision and both direct shipped writes fail without changing any record; the public memo suite passes.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test memo
```

All source records are disposable fixtures. Existing memo validation and writing
paths own the behavior; no new parser, mutation path or production state is added.
