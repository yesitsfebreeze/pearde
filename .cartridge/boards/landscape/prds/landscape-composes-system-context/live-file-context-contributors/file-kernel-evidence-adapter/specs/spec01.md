---
complexity: medium
footprint: ["src/lib.rs","src/file_kernel.rs",".cartridge/tests/unit/file_kernel.rs",".cartridge/docs/file-kernel-context.md","src/census.rs",".cartridge/tests/unit/census.rs","src/source_search.rs",".cartridge/tests/unit/source_search.rs"]
---

# Exact file and kernel adapters reuse the canonical collector

Baseline at Landscape3b9f728/memo45d5a54 proves tracked-name inventory revisions ignore body edits and native context lacks file/kernel options. Preserve inventory summary/page semantics. Existing Prepared has no cursor API; freshness is exact source references/readback plus the new Prepared revision. Per coordinator direction, do not add speculative paging.

Expose typed adapter functions returning existing context::Contribution/Evidence and exact read helpers. `FileSource {owner,path}` comes only from a trusted bounded public allowlist; at most128 entries, context owner grammar<=64bytes, normal relative path and combined `@owner/path` ID<=512bytes, unique pairs, no NUL. Exclude `.cartridge/memos` and `.cartridge/documents` and case aliases at config validation; native FS also enforces exclusion against actual reserved-directory identities before reading. Their privacy/hydration belongs to existing typed adapters. The allowlist is an explicit declaration to surface those file bodies; do not infer that every tracked file is public. Query1..1024bytes nominates matching owner/path strings deterministically, case-insensitive literal matching, at most limits.max_rows slots; no replacement scans after invalid slots. Canonical collect remains the only final selection/deduplication/budget stage.

File contributor calls a supplied exact readonly callback once per nominated source. Callback transports only owner/path plus optional expected revision; no tool search, guessed query or alternate source selection. Validate native FS available shape, returned exact path, bytes<=8192 and full SHA256 of UTF-8 text, revision_kind source_bytes; malformed/unknown errors are static partial/unavailable. Evidence.reference is owner/kind=file/id=@owner/path/full source SHA; source is canonical owner/path JSON; text is the exact file bytes; selection_reason is fixed bounded data. Missing/inaccessible/changed sources preserve other rows with Partial; no indexed/nominated sources is Empty. Disabled/absent are explicit caller Task states, never polled. Exact file read validates every Reference field, exact current logical owner/allowlist membership and expected digest; it never renominates or substitutes another logical file. The reference does not bind a historical physical root or generation: a currently permitted same owner/path with identical full bytes retains the same source-byte reference, even after physical replacement. Only kernel references explicitly bind generation.

Kernel contributor accepts the one trusted raw host composition snapshot, bounding entries128 before inspection. Parse exact unique owner IDs<=128 bytes, state and generation plus at most64 safe capability keys per entry. Every capability key is nonempty, at most128 UTF-8 bytes and contains no NUL; check count and byte length before cloning. Oversized/malformed selected entries produce Partial rather than a truncated digest projection. Project only id/generation/state/provide; exclude raw config, paths, errors, source bodies, descriptors, connections and arbitrary metadata. Disabled/private entries are excluded before candidate creation. Malformed selected entry makes Partial; unsupported state/shape is named unavailable rather than claimed empty. Query matches only owner/capability strings; bounded nominations preserve deterministic order and no provider calls occur. Kernel reference owner=runtime, kind=kernel, id=@runtime/kernel/<exact host owner>; revision_kind observed_projection, digest of canonical projected metadata. Text and source use that same bounded projection. A generation/capability/state change invalidates exact readback; unchanged entries retain exact reference. Native read selects exact ID from one new host snapshot and compares every field/revision, with no semantic search.

Both adapters run inside caller canonical context Tasks under the one shared deadline. They do no blocking transport or detached retry; callbacks inherit that deadline. Shared source4096/id512/text8192 limits and serialized Prepared budget remain authoritative. Producer caps count before append, malformed/private inputs cannot leak arbitrary payload via errors, and missing sources stay distinguishable from successful zero matches.

## Acceptance

- [x] Actual filesystem fixture conforming to the separately proved native FS snapshot contract and shared collector returns separate exact file and kernel capability evidence with stable unchanged references.
- [x] File edit/removal, generation/capability change and changed allowlist invalidate affected exact readback/Prepared revision without changing unrelated row identity; inventory cursors stay frozen.
- [x] Disabled/private, same leaf name across owners, typed-record case aliases, identical-byte physical replacement, malformed/oversized data, failed callback and hanging source preserve bounds and usable contributors, with no provider activation or second query.

## Verify and proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test landscape
just check landscape
just test memo
```

Actual native multi-owner wiring is proved by the memo child; library fixtures include real file bytes and deterministic callback behavior. Root collects FS first, then Landscape, then releases memo integration. No source changes until independent review and explicit owner release.
