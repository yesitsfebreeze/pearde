---
complexity: medium
footprint:
- src/main.rs
- src/service.rs
- src/source_search.rs
- src/document.rs
- .cartridge/tests/unit/source_search.rs
- .cartridge/tests/integration/source-search.test.ts
- .cartridge/docs/source-search.md
---
# Bind configured sources to the existing native Memo service

Baseline actual SDK rejects board prds paths and hierarchical owners; live landscape still supplies only current memo survey. Add opt-in host Config.source_search with bounded Root mounts and fixed PRD boards scope, and native `{op:landscape,version:3,action:search|read,...}`. Route version3 before existing v2 inventory dispatch; preserve legacy landscape, graph, inventory and tool schemas. Source roots are host configuration validated before cloning, never native/model path overrides. Defaultdisabled performs no source calls. Exact native request schema accepts query/limits for search or structured reference/limits for read, plus existing trusted cwd; rejects roots/scopes/provider/config/transport overrides. The operation remains native-only.

The facade owns transport only: use collected census and source_search libraries. Board declaration and record callbacks invoke the actual already-granted `prd` capability, deriving normal relative board selectors from fixed host PRD scope and exact canonical callback directory. Check grants before calls; missing PRD preserves independently usable cartridge sources and reports unavailable. It never starts/reloads a provider to read docs. Require configured board scopes beneath the fixed PRD scope. Explicit cartridge mounts are source-only unless host runtime metadata says otherwise; their normalized declarations come solely from bounded host children configuration (empty means an explicit leaf), never init.lua evaluation or guessed manifest fields. Hash canonical declared host configuration as configuration revision and distinguish it in documentation from PRD settings-byte revisions.

For cartridge records reuse Memo's actual document index/parser/bytes/privacy path restricted to the exact granted source/.cartridge/documents tree. Add a narrow internal document source index/exact-read adapter reusing existing confinement, Document::parse, byte reader and public visibility decisions. Do not send hierarchical census owners through flat Memo owner parsing. Normalize to the shared source-records DTO with exact canonical source root and census source revision. A temporary internal workspace identity may be used only inside the existing reader; output uses the caller's structured census address. Human/docs projections hydrate links and have separate projection digests, so they cannot be labeled exact source bytes: exact reads return the frozen parsed raw source bytes with their source revision, without link expansion. No duplicate YAML parser or altered existing projection behavior. Plain untyped Markdown remains outside the opted-in typed-document index; board PRDs use the PRD owner adapter.

Limits/config: <=32roots, existing census alias/path/depth/source/edge caps, <=256 explicit cartridge declaration nodes and<=1024totaledges/64children, host configuration <=262144bytes; validate before cloning. The source_search limits apply unchanged. One absolute request deadline covers grant checks, census and record work, using the library's absolute-deadline entry point. Keep at most8 operations in flight; native timeout/cancellation cannot free a slot while an issued local blocking document read is still executing. Use a semaphore guard owned by the actual blocking job and no unbounded task submission; no user-visible timeout implies remote cancellation acknowledgment. Closed service refuses new work. Error strings are static; no source paths, title, body, tokens or OS details leak from excluded records or failed callbacks.

Each request obtains a fresh census and reads fresh owner data. Do not retain record copies/snapshots globally. Read requests rebuild the census and match selected source_revision+record_revision so removed/moved/changed references are explicit. Disabled/missing/timeout source metadata does not fabricate complete empty search. General source-only and runtime-state distinctions remain in output and callable:false cannot be overridden by request data.

## Acceptance proof

- [ ] Real two-owner SDK/runtime fixture (Memo+PRD) with actual three-level board records and public/private typed cartridge docs finds all public body facts; exact same-basename reads select the right owner, and poisoned inactive init.lua never executes.
- [ ] Actual configured invocation rejects request authority overrides, malformed roots, absent grants, private records and stale/cross-owner references; no Memory, event, source mutation, provider-start or tool exposure is observed.
- [ ] Staged delays and blocking-read capacity prove the one deadline and live resource slots; schema/cap failures preserve independently usable evidence and no raw diagnostics.
- [ ] Existing public Memo tests/check and inventory/context/document integration suites pass; no old schema changes.

## Verify

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test memo
just check memo
just build memo
just test landscape
cd /Users/feb/dev/cartridge/memo.ctg
bun test ./.cartridge/tests/integration/source-search.test.ts ./.cartridge/tests/integration/inventory.test.ts ./.cartridge/tests/integration/context.test.ts ./.cartridge/tests/integration/validation.test.ts
```

Record exact built Memo/runtime binaries and owner source revisions plus unchanged fixture source hashes. This is the actual invocation dependency of original recursive-root-search, not a new global search service.
