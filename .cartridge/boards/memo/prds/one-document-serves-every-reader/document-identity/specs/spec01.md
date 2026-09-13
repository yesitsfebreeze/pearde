---
complexity: medium
footprint: ["src/context.rs","src/inventory.rs","src/main.rs","src/service.rs","src/document.rs",".cartridge/tests/unit/document.rs",".cartridge/tests/fixtures/documents",".cartridge/docs/documents.md","src/source_search.rs",".cartridge/tests/unit/source_search.rs"]
---

# spec01 — One opt-in document snapshot has one owner, path and revision

Add native `memo` operation `document`, retaining all legacy memo operations.
Enabled cartridge IDs/directories supply canonical owners. When the canonical
cwd is inside one enabled root (including the root itself), that owner is the
default; otherwise the cwd gets owner `workspace`. Enabled roots may not overlap.
The synthetic workspace document namespace must not overlap an enabled owner
namespace; refuse ambiguous physical ownership before reading. Model tool input cannot supply roots or invoke this native
operation. Duplicate owner IDs or one directory attributed to different owners
refuse with source locations. No manifest metadata can override trusted ownership.

Only Markdown with frontmatter `schema: cartridge-document/v1`, nonempty `kind`
and `description` participates. Canonical identity is `@owner/<owner-relative
.cartridge path>.md`. A physical `.jd` is an alias of the corresponding `.md`;
both files existing is an explicit collision. Reject absolute/traversal paths,
symlinks, invalid UTF-8, malformed metadata and source files above 1 MiB.

A read resolves one exact file and freezes its bytes once. SHA-256 of those exact
bytes (including frontmatter, newline style and trailing newline) is `revision`
for commands/docs/human projections. Optional `expected_revision` refuses stale
reads. Commands expose located raw fenced `just` blocks labelled unvalidated;
docs/human expose unhydrated Markdown. No process is launched or launch authority
implied. Executable validation and linked prose hydration remain separate leaves.

Index searches one owner's explicit directory (default `.cartridge/documents`)
under `.cartridge`, discovering only versioned files. Match only frontmatter
kind, description and string tags, never body or recipes; preserve legacy resolve
body scoring. Return compact identities/revisions, at most 128 rows and explicit
truncation. Bound directory inspection to 4096 entries/32 levels, read bytes to
16 MiB per operation, and metadata to 16 KiB per document. Capacity errors are
explicit, not silent omission or claims of complete discovery.

## Acceptance

- [x] Frozen .md/.jd fixtures return the same canonical identity and exact-byte revision through all three projections; byte changes update revision and stale expected_revision refuses.
- [x] Nested cwd retains its enabled canonical owner; overlapping owner roots, duplicate owner/directory bindings and .md/.jd collisions refuse with both source locations; unsafe paths, malformed files and exceeded limits are explicit.
- [x] Index matches metadata-only terms and excludes prose/recipe-only terms, reports bounded truncation, and preserves legacy memo APIs.
- [x] Reads/index create no files, observations or processes; raw just fences are labelled unvalidated and ordinary memos stay outside the opt-in dialect.

## Verify and Proof

```sh
cd ../cartridge.ctg
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just test memo
RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract" just check memo
```

Freeze fixtures in the owner before parser implementation. Use native service and
pure owner-boundary tests, byte snapshots, duplicate identities, metadata-only
queries and stale revision checks. Shared service/main changes require receipt
refresh for types-drilldown and initialize-board; engine behavior stays unchanged.
