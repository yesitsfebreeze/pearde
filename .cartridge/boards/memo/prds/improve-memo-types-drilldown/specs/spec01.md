---
complexity: small
footprint:
  - src/service.rs
  - .cartridge/tests/integration/tests.rs
---

# spec01 — Discover declarations through the existing index and read operations

Current source already exposes compact kind metadata through `index`, including
qualified declaration paths and explicit ambiguity, and full individual memos
through `read`. Reuse these operations instead of adding another selector.
Change the tool's discovery guidance to recommend index followed by read of the
selected declaration. Preserve `types` as the complete legacy response.

## Acceptance

- [x] Discover work and routine through index, read each returned declaration path, and prove the individual response equals that declaration in legacy types without other declaration bodies.
- [x] Unknown declaration reads return an explicit error; validated writes, stale revision refusal and the complete legacy types response remain covered by the owner suite.
- [x] Tool discovery names index/read and the compatibility types operation; reads do not rewrite authored records.

## Verify and Proof

```sh
cargo test --manifest-path Cargo.toml -p memo_cartridge
```

Run `just test memo` from cartridge.ctg as the integrated public gate. This is
response-size guidance: the existing record validation still scans the bounded
record internally. No storage-layout or authored-record migration is claimed.
