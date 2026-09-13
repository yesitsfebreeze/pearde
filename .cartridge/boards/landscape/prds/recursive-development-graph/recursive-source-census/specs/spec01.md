---
complexity: medium
footprint:
- src/lib.rs
- src/census.rs
- .cartridge/tests/unit/census.rs
- .cartridge/docs/source-census.md
---

# Bounded declared source traversal keeps hierarchical ownership explicit

Measured baseline62185289 shows Landscape surface composes only supplied flat entries; it performs no recursive source discovery. Maintained PRD member parsing already preserves three-level aliases, but its strict scanner aborts on a missing descendant or cycle. Add one census library module, retaining existing graph/inventory/context APIs and strict PRD behavior. New prerequisite @prd/declared-source-edges owns parsing/read-only native normalization of existing settings.md members. No YAML parser, Lua evaluation, Git directory sweep, provider launch, record copier, search selector or runtime mutation belongs here.

Expose an asynchronous `capture(roots, limits, declaration_callback)` returning a typed immutable Census. Each trusted root mount supplies a root alias, source kind (`board`/`cartridge`), absolute allowed scope, exact initial directory, and explicit source-only/installed/loaded metadata. This is host configuration, never query/model input. Canonicalize each permitted scope/directory; source status describes filesystem/declaration availability independently of runtime metadata, and `callable:false` is invariant for census rows. Board callback binds the already granted PRD native operation; cartridge callback supplies explicit trusted normalized declarations, without reading/executing init.lua or inventing a cartridge manifest child field. Pure traversal callbacks receive only source kind and exact canonical directory. They return the reviewed declaration shape/root/revision/children or a static failure. A callback may use the existing parser's exported helper in library fixtures; native integration uses its actual capability. No caller may interpret source documentation as service activation authority.

Validate roots<=32; alias segments use existing ASCII alphanumeric first character then alnum/_.-, <=64bytes. Hierarchical owner is a **structured segment vector**, <=8levels and <=512 aggregate bytes, with root alias retained. Owner paths are separate from source-relative record paths; a canonical `address(owner, kind, relative_path)` helper returns their structured tuple plus domain-separated SHA256 identity, so root/base with `plugin/same` cannot collide with root/base/plugin and `same`. This does not rename existing PRD references or broaden memo document owner grammar. Census identifies source roots; record enumeration, private-metadata filtering, body hydration, root search and exact source-byte reads remain the existing root-search sibling. Prove the same-named real record addresses under all three discovered owners without claiming this census searches/reads their bodies.

Traversal is deterministic depth-first with sorted roots/children. Keep canonical directory identity in visited and ancestor maps (stable Unix directory device/inode plus canonical path); observe a root only once. A backlink produces `cycle`; a later repeated mount produces `alias` pointing to the first canonical hierarchical owner and never duplicates its descendants. Child symlinks may resolve inside the explicitly allowed scope and become aliases; any canonical escape is `escaped` and never queried. Missing, non-directory, unreadable/permission, malformed declaration, callback unavailable/timeout and changed-during-inspection each become named source rows preserving siblings. Require returned declaration root to equal the requested canonical root; exact settings revision is validated and retained as the source owner's provided byte revision. Compare filesystem identity around callback to refuse a changed directory; do not claim a transaction against malicious writers restoring observed identities.

Hard limits: max_depth1..8; max_sources1..256; max_edges1..1024; <=64children per declaration; each absolute path <=4096bytes; callback decoded shape bounded before copying; max_bytes4096..1048576 for the entire serialized Census. Defaults depth8/sources256/edges1024/bytes65536/deadline500ms; deadline1..2000ms. Count every attempted mount/edge, including aliases/failures, before append/recursion. Root/declaration overcapacity is explicit, not silently a successful empty source. Stop when global capacity is exhausted with `truncated:true`, `complete:false` and a bounded omitted indicator; do not retain unbounded omitted names. At maximum depth emit an explicit depth status without polling the child callback. One absolute deadline covers canonicalization, metadata and all callbacks; no detached work/retry, and timeout does not imply remote cancellation acknowledgment. Return completed sibling rows and bounded timeout status where budget permits. No callback is issued for missing/escaped/alias/cycle/depth-refused sources.

Census revision hashes canonical observed rows, owner/declaration revisions and statuses with no wallclock time; unchanged declarations/identities are stable on a fresh capture. A current capture notices a deleted source or changed settings revision and changes affected observed source metadata, while previously returned Census stays immutable. This is an observed declaration/root snapshot, not record-content freshness; recursive-source-refresh remains responsible for derived document invalidation. Exact-byte record revisions, pagination and runtime callable grants are outside this leaf.

## Acceptance

- [x] A real three-level declared board fixture, normalized by the actual PRD owner helper, yields three hierarchical owners and distinct addresses for same-named on-disk PRDs; explicit source-only cartridge mounts are identifiable without provider invocation.
- [x] Backlinks, repeated mounts, internal and escaping symlinks, conflicting aliases, malformed callback/root/revision and depth/count/byte/deadline limits terminate explicitly and preserve usable sibling rows.
- [x] Deleted/unreadable descendants have named status on the next capture; changed declaration revision updates only its observed row/overall census revision; no record bytes or provider state is changed.

## Verify and proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test landscape
just check landscape
just test memo
```

Rust library tests consume a bounded actual PRD-generated three-level declaration fixture under the collected adapter, not a duplicate YAML parser or fabricated descendant topology. Include deterministic permission/metadata failure injection when privileged test users can read mode000 paths, while also exercising actual filesystem deletion and symlinks. Root collects PRD first, then releases this owner source after independent review. No source implementation or shared-map mutation is authorized by this unreviewed spec alone.
