---
complexity: medium
footprint:
- src/file_kernel.rs
- src/lib.rs
- src/inventory.rs
- Cargo.toml
- .cartridge/tests/unit/src/inventory/tests.rs
- .cartridge/docs/inventory.md
---

# Frozen bounded inventory, additive library API

Baseline c705d648: actual legacy view of 10,000 Git-tracked paths serializes 260,311 bytes, more=false and cursor=null. Retained baseline files record the exact disposable fixture and consumer command. No path paging exists. Add public inventory module; preserve view, context, memory and graph/search APIs unchanged. No source records or presentation policy migration.

## Capture and ownership

`inventory::capture(raw: Value, deadline: tokio::time::Instant)` returns an immutable Snapshot or a static named structural error. Capture consumes the trusted native host composition snapshot, not model-selected roots. Entries retain exact host owner IDs, state and generation. No tool descriptors, memo bodies, config values or raw backend errors enter the projection. Host allocation/decoding has already happened; limits here bound inspection, retained metadata, subprocess output and response serialization, not prior host allocation.

At most 128 entries; unique nonempty UTF-8 IDs at most 128 bytes and no NUL. Duplicate/malformed owner IDs or excessive owner count reject the whole capture explicitly. Unknown state, bad generation, malformed or missing directory produces a named owner status rather than disappearing. Disabled entries are not inspected. Legitimate dynamic entries without directories report not_applicable. Canonical absolute directory roots may follow the trusted composition's built-in symlink. Roots at most 4096 bytes. Two configured owners may share a physical root: owner/path remains the exact configured identity, with a single cached physical scan per capture. Parent/sibling roots are independently scoped by `git -C root ls-files -z -- .`; returned paths must be relative to that root. No path resolution, document reads or callable capability creation follows inventory paths.

Read Git tracked names only using an argument vector, null stdin/stderr, piped bounded stdout and kill-on-drop child. Sequential scans share the caller's absolute deadline, including async canonicalization and all reads. No subprocess is launched after deadline. Timeout or capacity cancels capture work and names affected owners; cancellation requests termination and does not claim a worker was joined. Remaining owners report timeout when the common deadline expired. Per scan stdout at most 8 MiB plus one sentinel byte; total retained UTF-8 path bytes at most 16 MiB and paths at most 100,000. Enforce caps before append. Individual paths at most 4096 bytes, strict UTF-8, no absolute or parent/current components; preserve newline and other valid filename bytes represented by UTF-8. Invalid output, missing Git, nonzero exit or capacity fails that owner's entire inventory, never claiming a partial set complete. Other successful owners survive. Paths are sorted and deduplicated per exact owner. Git observation is frozen once captured; no claim of cross-repository atomic reads.

Snapshot has a unique capture token (process-instance seed plus monotonic sequence), distinct stable source digest binding retained owner/generation/state/status/paths, and owned immutable rows. Identical recapture still replaces the token. Unavailable owner path count is null; known totals and partial=true distinguish unknown inventory from zero.

## Summary and pages

`Snapshot::summary()` returns version=2, snapshot token, source_revision, status, total owner count, known path count, omitted owner/path counts and bounded owner rows (owner/state/generation/path_count/status). No full tracked arrays or arbitrary host metadata. Exact serialized JSON is at most 16,384 bytes; trim owner rows with explicit omitted_owners until within cap. Summary omits all inventory paths and reports their known count as omitted_paths; unknown counts stay named/null.

`Snapshot::page(owner: Option<&str>, cursor: Option<&str>, limit: usize)` returns exact owner/path rows from this frozen capture. Default limit 100, validated 1..256. Owner filter selects an exact enabled composition ID, unknown owner errors. Cursor binds token, owner filter and next offset; invalid encoding, another token/filter or out-of-range offset errors with static codes. Start without cursor; next cursor only if remaining rows. Greedily include complete rows until row/16-KiB serialized response cap; validate maximum row size so every nonempty page advances. Response includes matched known count, returned/remaining counts, source_revision and partial statuses. Every permitted pair is visited exactly once in sorted owner/path order. No host/Git/filesystem work happens during summary/page; new files become visible only in a replacement capture. Tokens are freshness markers, not authorization secrets.

## Acceptance / failure proof

- [x] Actual 10,000-path Git fixture: summary <=16 KiB, omitted_paths=10,000, every serialized page <=16 KiB, exact reconstruction and deterministic order.
- [x] Generation replacement and identical recapture invalidate old cursors; malformed/changed-filter/out-of-range cursor refuses; byte-limited pages advance and newline names round-trip.
- [x] Disabled/dynamic, shared-root and nested-root identity, missing Git/nonrepo, bad UTF-8, malformed owner/duplicate ID, oversized output/paths/count, deadline and partial contributor fixtures prove named outcomes and bounds.
- [x] File hashes and Git status remain unchanged across capture/paging; no command source or history reads/writes. Legacy and context/memory tests still pass.

## Verify and proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test landscape
just check landscape
just test memo
```

Proof records exact source SHA and public commands. Native deployed summary/cache behavior belongs to the dependent memo child. Changes to library registration may require coordinator refresh of context/memory receipts. No shared composition edits.
