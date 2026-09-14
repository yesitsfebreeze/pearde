---
complexity: medium
footprint:
- src/base/src/base_types.rs
- src/retrieval/piece/src/id_detail.rs
- src/retrieval/piece/src/lib.rs
- src/retrieval/src/lib.rs
- src/rpc/src/server.rs
- src/cartridge.rs
- src/transport/src/owner.rs
- src/store/core/src/lib.rs
- .cartridge/tests/unit/src/base/src/tests/base_types_test.rs
- .cartridge/tests/unit/src/retrieval/piece/src/tests/id_detail_provenance_test.rs
- .cartridge/tests/unit/src/rpc/src/tests/server_bounded_test.rs
- .cartridge/tests/integration/cartridge.rs
- .cartridge/docs/CARTRIDGE.md
- .cartridge/docs/fact-provenance.md
---

# Consistent provenance on existing fact projections

Measured baseline at Memory 0a7c4a1f729c700f52c650ee0c3efc56a136560f: actual local and attached SDK `query {include_history:true}` already returns new/old identities, source links, active/superseded labels and the indexed Supersedes explanation. Direct get/batch/compact preserves sources but omits lifecycle status; all projections omit stored creation/update times. A legacy undated fact remains readable without an explicit unknown freshness result. Retain these working selection and ownership semantics. Baseline artifacts were recorded before this spec. Preserve inherited rounds 1–2; independent round 3 review is required before implementation.

## One shared metadata projection

Add a bounded `provenance` object to both existing `base_entity_json` and `entity_detail` through one private helper in retrieval-piece's id_detail module. Existing native local, daemon/attached, batch, compact and cold-ID paths already call these projectors; keep those routes and their resolver authority. Existing fields retain their values and types, including numeric kind on get versus labeled kind on ranked rows. Existing four-field `source` objects remain unchanged.

The additive object has schema `memory.provenance.v1`; `status` active|superseded from existing Entity lifecycle; `review` active|pending from existing review state; `superseded_by` exact stored ID or null; `created_at_ms` and `updated_at_ms` from their corresponding persisted fields only; `observed_at_ms:null` because no distinct source-observation clock is stored; and `freshness` recorded|unknown|unrepresentable. `recorded` means at least one creation/update clock is representable, not that a source was recently checked or its claim is true. `unknown` means both clocks are absent; if clocks exist but neither can be represented, use `unrepresentable`. Include `unrepresentable_clocks` as a fixed bounded list of affected clock names.

Also project existing `valid_from_ms`, `valid_to_ms`, `invalidated_at_ms`, and `valid_until_ms` in this object. These clocks keep their existing meanings: world validity, transaction invalidation and retention deadline. Missing fields remain null. Use checked signed Unix milliseconds with floor rounding (including pre-epoch instants); overflow returns null plus its named unrepresentable clock. Never turn an absent or unsupported time into epoch zero, current time, another clock, filesystem mtime, or query-access time. The existing top-level seconds-based fields retain their compatibility behavior; the new object is explicit and consistent. The object has a fixed number of scalar fields and clock-name entries, no query text, backend error, graph traversal or external-source access. The stored successor ID is the same identity already exposed by ranked recall.

## Explain recorded evidence without inventing conflicts

Retain indexed graph reasons, edge orientation, existing get pagination and text budgets. Add a stable lowercase `kind_label` beside every existing numeric edge kind, using one exhaustive ReasonKind method in base (no enum/field/layout change). A Supersedes edge points from newer to older; Deleted names source deletion, Rephrase records a proposed/rephrased statement and must not be presented as a proven competing fact. Other kinds keep descriptive labels. Do not infer a contradiction by comparing text, invent a supersession, or decide which external source is true.

Ranked edges also retain the stored exact edge `id`, as get already does. Eligible ranked evidence remains enriched reasons plus lifecycle reasons Supersedes/Rephrase/Deleted even when explanation text is absent; a label and exact endpoints are still known. Preserve score/ID ordering and QUERY_MAX_EDGES=12. After ordering, deduplicate identical edge IDs contributed by both directions of a self-loop before counting/capping; the new ranked count names distinct eligible evidence. Direct pagination keeps its existing adjacency behavior. Add `edges_total`, `edges_more` and `edges_scope:"enriched_or_lifecycle"` so a bounded ranked sample is distinguishable from no evidence. Get retains its existing all-indexed-edge count/cursor/limit behavior; compact still omits edge text and exposes named kind/endpoints. No unbounded replacement search, new graph scan, recursive hydration, source fetch, model call, new recall selector or endpoint is added.

Keep default ranked exclusion of superseded rows and existing explicit `include_history:true` behavior. The accepted fixture exercises history-enabled query plus exact get of both identities; source/status/explanation survive across local and attached views. A dangling recorded endpoint remains only a reference: exact get returns the existing explicit missing error, rather than fabricating peer metadata. Cold direct reads retain their cold annotation; unavailable graph edges remain absent under current cold behavior. Metadata-only rendering never claims all conflicts are known or that no edge means absence of a real-world conflict.

## Authority and compatibility

No persisted field, bincode variant, store version, import/export representation, Graph identity, runtime profile or transport schema changes. Retain same-client owner identity/read validation and typed failures; no attachment fallback or additional writer. Query's existing owner-controlled access telemetry is unchanged. Projection alone is pure; store fixtures assert rendering does not mutate entities, clocks, lock identity or stored bytes. Reverting these additive projection fields needs no data rewrite. New helper stays private behind existing hot-reload projection entrypoints; ReasonKind's label method adds no shared type layout or dynamic export. Documentation distinguishes recorded clocks, validity, retention, source links and observed-vs-inferred evidence.

## Acceptance

- [x] Actual seeded local and attached native query with include_history and exact get/batch/compact preserve new and old fact IDs, both distinct source links, shared creation/update/validity clocks, lifecycle labels, successor ID and named Supersedes edge. Current default ranked behavior remains unchanged.
- [x] Legacy missing dates remain readable with null clocks/unknown freshness; partial, pre-epoch, submillisecond, unrepresentable, expired and superseded cases preserve their own semantics. No fabricated observation time or fallback clock. Cold get retains truthful metadata and existing missing-edge behavior.
- [x] Bounded ranked and paged/compact edge projections expose kind labels and exact identity, omit text under compact as before, distinguish omitted eligible evidence, and report a missing referenced peer through existing exact-get error. No inferred contradiction or source fetch.
- [x] Pure projection fixture preserves entity/store/lock state. Public Memory just test/check includes native owner/attachment/readiness, Graph, writer, health, legacy and bounded-projection regressions at one revision. Source-only rollback needs no persisted migration.

## Verify

```sh
set -eu
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary cargo test -p memory --test cartridge provenance -- --nocapture
```

```sh
set -eu
provenance_log=$(mktemp /tmp/memory-provenance-full.XXXXXX)
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just test > "$provenance_log" 2>&1 || { tail -80 "$provenance_log"; exit 1; }
tail -25 "$provenance_log"
shasum -a 256 "$provenance_log"
```

```sh
set -eu
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR=/Users/feb/dev/cartridge/memory.ctg/target/prd-writer-boundary just check
```

Source implementation waits for independent review and release after readiness receipt refresh. Use the isolated Memory worktree and existing debug-zero target. Coordinator owns canonical lifecycle/map/collection. Record exact reviewed input, failure and proof digests; do not change historical acceptance to match implementation.
