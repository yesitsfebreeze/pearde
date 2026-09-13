---
complexity: medium
footprint:
  - src/main.rs
  - src/inspection.rs
  - src/compaction.rs
  - .cartridge/tests/unit/compaction.rs
  - .cartridge/tests/integration/working.rs
---

# spec01 — Retain compaction comparisons in the existing summary buffer

Use a versioned JSON summary document with ordered snapshots, while reading
legacy endpoint/hash/text summaries. Persist history and latest summary in one
existing buffer set after successful projection and transcript revalidation.
Each snapshot records covered endpoint/hash, source transcript endpoint/hash,
summary, source revision, timestamp, elapsed time and numeric usage counters.
Never persist provider responses or headers. The canonical journal remains the
source of covered messages and the original retained tail; compare hashes before
showing either, reporting unavailable evidence when edited or missing.

The inspector adds compactions and corresponding source items. It only reads
buffers and transcript; comparison never invokes the router. Failed model calls
leave the complete previous summary document untouched. Legacy snapshots label
unrecorded timing/usage/tail evidence honestly.

## Acceptance

- [x] Two real-process compactions retain both summaries and map each to exact raw covered messages and its original retained tail; a corrected constraint appears in source and summary.
- [x] Failed compaction leaves prior history untouched; inspection makes no model calls and includes no provider authorization metadata.
- [x] Legacy summaries remain readable; edited source prefixes produce an explicit unavailable comparison, not a false match; transcripts remain unchanged.

## Verify and Proof

```sh
cargo test --manifest-path Cargo.toml -p harness
```

The existing runtime/RPC integration uses deterministic local sessions, buffers
and router fixtures. No configured model, paid evaluation or user store is used.
