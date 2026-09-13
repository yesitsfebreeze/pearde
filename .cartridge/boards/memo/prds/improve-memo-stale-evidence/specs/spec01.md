---
complexity: small
footprint:
  - src/usage.rs
  - .cartridge/templates/seeds/type/resource.md
  - .cartridge/tests/integration/resolver.rs
---

# spec01 — Explain resource freshness without rewriting historical evidence

Add an optional `recorded_target_revision` SHA-256 to resource declarations.
Existing declarations remain valid. Resolve compares the declared baseline to
current target bytes and adds freshness metadata: matching, changed, unrecorded,
or unavailable/missing. Missing search hits keep their original descriptor path,
revision and target in the existing problems array. Exact missing resource reads
continue to fail. Preserve the root/items/problems envelope and existing fields;
new metadata is additive. A matching digest proves bytes only, never that advice
is current. No baseline means unrecorded, not unchanged. Invalid declared digests
are rejected by validated writes. Reads do not update baselines or journals.

## Acceptance

- [x] A changed source reports changed against an explicit recorded digest; a renamed source reports missing with its original path, descriptor revision and recorded digest.
- [x] Existing declarations without baselines remain usable and are labelled unrecorded; malformed baseline writes fail; legacy exact missing reads still fail.
- [x] Current routine and completed work remain separately discoverable; resolver outcome attribution stays explicitly caller-reported; authored bytes and journals remain unchanged.

## Verify and Proof

```sh
cargo test --manifest-path Cargo.toml -p memo_cartridge
```

The public integrated gate is `just test memo` from cartridge.ctg. Existing
negative tests retain path, symlink, cancellation, pagination and write guards.
