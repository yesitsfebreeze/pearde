---
complexity: medium
footprint:
  - src/document.rs
  - src/projection.rs
  - .cartridge/tests/unit/projection.rs
  - .cartridge/tests/fixtures/projections
  - .cartridge/docs/documents.md
---

# spec01 — Bound readable linked prose to an explicit source closure

Docs/human projections hydrate explicit `[[path.md#Heading]]` wiki references
outside inline, fenced and indented code. Paths are exact sibling/owner-relative
.md/.jd paths; `@owner/.cartridge/...` selects another enabled owner explicitly.
Normalize relative links only within the selected owner's .cartridge namespace;
never search by basename, cross an owner implicitly, follow symlinks or fetch URLs.
Named sections match one exact ATX heading outside code and include its subordinate
content. Missing/duplicate sections or targets produce source-located diagnostics.
Ordinary Markdown links and external URLs remain literal.

Preserve `revision` as the primary source's exact-byte digest. Add a distinct
`projection_revision` binding projection type, rendered bytes, sorted public source
identity/revision closure, diagnostics and the fixed limit profile. Cache each
resolved source snapshot once per request; repeated references cannot silently
combine versions. Editing linked prose changes the derived revision without
changing the primary revision. No cross-file atomic filesystem snapshot is claimed.
Commands stay unhydrated, located and unvalidated, with a primary-only closure.

Optional frontmatter `visibility: private` refuses direct projections and hides
that source from the public index. Omitted visibility is public; invalid values
fail. A public link to private content returns a redaction diagnostic/placeholder,
never its body, metadata or digest. This projection rule is not filesystem access
control. Missing, malformed or private dependency diagnostics never quote content.

Bound expansion to depth4, 32 unique source snapshots,128 reference visits,16 MiB
source reads,64 KiB rendered UTF-8 content and64 diagnostics. Detect cycles on the
active identity/section path. Cycle/capacity outcomes set `truncated:true`; unresolved
or redacted references set `complete:false`. Preserve unresolved references or bounded
placeholders and report omissions explicitly. No automatic replay, process launch,
observation writes or executable import resolution occurs. Legacy memo APIs and
frozen identity fixtures remain unchanged.

## Acceptance

- [x] An edited public dependency changes the hydrated projection revision and closure while primary revision stays fixed; repeated references use one frozen source.
- [x] Exact sections, relative and qualified owners resolve; missing/duplicate sections, ambiguous aliases and escaping paths produce located diagnostics.
- [x] Cycles, depth, node, visit, source-byte and output limits remain bounded and explicitly truncated, including repeated fan-out and UTF-8 boundaries.
- [x] Fenced/inline/indented code references stay literal; private bodies/metadata/digests never appear; commands remain unhydrated and no files/processes are created.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test memo
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check memo
```

Freeze projection fixtures separately; retain the prior exact-byte identity corpus.
Use deterministic file-edit hooks to prove snapshot reuse, explicit private sentinels,
source-located errors and all bounds. Reverify the overlapping document-identity receipt.
