---
complexity: medium
footprint:
- src/lib.rs
- src/source_search.rs
- .cartridge/tests/unit/source_search.rs
- .cartridge/docs/source-search.md
---
# Search and read records using the exact census owner

Measured baseline: census33e0418 sees3 owners, but existing surface composition has no census/record join and returns0 descendant fact hits. Add a public async source_search module. Preserve current surface/Graph APIs; reuse Graph lexical ranking and census::address without embedding hierarchical owners in Memo's flat owner grammar. Library receives a trusted immutable Census and a callback `(source_kind, canonical_directory, typed index/read request)`; only owners parse and read files. No parser, transport, provider activation, durable cache or source copying.

`search(census, query, limits, callback)` polls each available canonical census source once, never alias/cycle/unavailable rows. It validates owner responses before cloning: exact schema/action/root/source_revision, <=128items, normal source-relative paths<=4096, metadata/title<=512, bytes<=1MiB, lowercase64hex revisions and explicit visibility:public. Reject duplicates and mismatched roots/revisions; treat partial index as partial search. Sort source owners and paths deterministically. The declared index is not sufficient authority for content: exact-read each selected indexed record with its expected byte revision, require public visibility again, recompute UTF8 bytes/hash and compare root/path/bytes/revision. Changed/private/malformed evidence never reaches ranking. No arbitrary extension fields copied.

Search full exact text within total byte/record limits, rather than treating a title/preview as the whole document. Build temporary source_record nodes with address identity keys, existing lexical ranking, no observed-use weights and no tool grants. Return compact hits with structured owner/kind/path, address identity, source_revision, exact record_revision, revision_kind:source_bytes, public title, score, bounded UTF8 snippet<=2048, snippet_truncated, and callable:false. Source-only/installed/loaded are carried separately from readability. Equal scores tie-break by structured source address. A hit never embeds a complete large body; exact read is separate.

`read(census, reference, limits, callback)` validates address recomputation, owner vector and source/record revisions against exactly one permitted canonical source. It calls only that source with the selected path/revision. No path supplied by the model can become a root/cwd, and no basename fallback exists. Return the complete validated UTF8 source text with the exact same structured reference or an explicit unavailable/changed/malformed/capacity/timeout; no truncated exact text. A reference is a public source selection, not an authentication credential; host census roots define permission.

Hard ranges: sources1–256(default32), records1–128(default64), aggregate input bytes1–8MiB(default4MiB), query<=1024UTF8 and nonempty, max_hits1–128(default20), search wire bytes4096–1048576(default65536), read wire bytes4096–8388608(default8388608), deadline1–2000ms(default500). Count every record attempt including rejected/changed reads and all indexed input bytes; never process an unbounded response before inspecting array/scalar sizes. Callback itself must bound transport decoding. Whole serialized result stays capped; retain whole hits only. Explicit complete/truncated/omitted/status and per-source static status preserve usable evidence without private diagnostics. Metadata/status arrays obey source and wire caps too. A shared absolute deadline for all awaits drops pending futures, spawns no detached work, retries nothing and makes no remote cancellation claim. Provide an absolute-deadline entry point for the facade to share one deadline across census+search/read.

Index/read operations are fresh on every search; returned results are owned snapshots. No cache invalidation mechanism is invented here. The existing recursive-source-refresh sibling can later prove fresh query behavior and stale references at the real facade once all dependencies are collected; it remains incomplete now.

## Acceptance proof

- [ ] Actual collected PRD native/helper indexes+reads produce three distinct same-basename body-fact hits and selected-owner exact text; use source-bound fixture outputs, not a duplicate parser.
- [ ] Private/foreign/root/path/revision/hash/bytes/malformed responses fail before ranking; source-only metadata never grants calls. A genuine public record with adversarial prose remains untrusted data.
- [ ] Exact reference rejects different owner/kind/path/hash, changed source/record, aliases and unavailable source; no fallback reads another record.
- [ ] Oversized fields/arrays/bytes, source/record/hit/wire limits and staged shareddeadline return bounded partial outcomes, preserve completed sources and drop pending callbacks.

## Verify

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test landscape
just check landscape
just test memo
```

Root collects PRD adapter first and reviews any nonsemantic older census fixture pin update separately. This leaf proves the library; original root-search stays incomplete until actual Memo routing passes the composed fixture.
