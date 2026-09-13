---
complexity: high
footprint:
- Cargo.toml
- src/main.rs
- src/service.rs
- src/store.rs
- src/provenance.rs
- .cartridge/tests/unit/provenance.rs
- .cartridge/tests/unit/snapshot.rs
- .cartridge/tests/unit/store/tests.rs
- .cartridge/tests/integration/change-provenance.test.ts
- .cartridge/docs/change-provenance.md
---

# Capture mutation receipts and forward reported attribution

Reuse the Sessions library DTO and existing optional host-service pattern. At
apply, read the actual `host.injections` once with a 2-second bound. An exact `sessions`
grant enables the recorder; a known absent grant keeps standalone operations
working, with explicit unavailable attribution on mutation replies. A failed
discovery is not absence: fail initialization explicitly after the bounded
discovery attempt. No required `.inject([sessions])` declaration,
wildcard grant, fabricated Sessions provider or implicit provider activation.
When enabled, call only that injected Sessions owner. Runtime shipped profiles
opt in separately. Model tool input schemas gain no identity or recorder controls.

Capture provider gitfs and reported context session/run/call; session/cwd remain
required, and missing legacy run/call stay null. Validate present identifiers and
bound all retained fields before mutation. Canonical actual repository root and
normalized repository-relative path determine the absolute target. Keep logical
overlay coordinates and actual overlay reference, rather than silently merging
filesystem aliases. `attribution:provider_reported_not_authorization` applies.

Add an internal structured publication receipt to the Store mutation boundary.
`write_blob` retains its existing outward Option<commit> behavior for callers;
the producer variant also returns the actual previous blob/parent/tip and new
blob/commit under the same session lock. Do not reread an unfrozen branch later
and label that result as this call's write. Empty/unchanged writes emit no new
publication evidence. Generate a fresh shared-helper publication_id per path's
actual publication under that lock; entropy failure refuses before mutation.
Never derive identity solely from equal content, run/call, or an old/new hash pair.
Write/edit and snapshot use `git_object` revisions and
`gitfs_overlay` storage. Snapshot reports only selected, already-owned paths that
actually produced a new commit; it never imports an unowned path for attribution.
The accepted record IDs and old/new commit references make the existing diff
read API the current divergence inspection boundary.

Materialize retains repository/session locks and existing guard/selection rules.
Capture direct before/after content hashes for each positively applied path;
reserve a distinct publication_id before that path's publication;
deletion records absent only after successful removal or observed absence. A
failed removal cannot count as applied. Do not infer publication from the current
`applied` string list if an IO result was ignored. Preserve actual applied receipts
when a later file or ledger step fails; report errors without rollback. If a
preimage cannot be read safely for bounded attribution, retain explicit unknown
attribution for that path rather than invent a revision or silently change its
existing mutation policy. No unbounded extra file reads: at most 8 MiB attribution
preimage per path, metadata checked before bounded read. Versions known from
already-present mutation bytes are hashed without duplicate retention.

Receipts are metadata only. Retain at most 64 records and 256 KiB per operation;
additional known applied paths increment an explicit omitted counter. Preserve
existing bulk mutation behavior, but report attribution partial rather than
claiming all paths were recorded. Send one `record_changes` batch after returning
from the blocking mutation worker, with a 2-second recording budget. Never hold the GitFS
mutation lock across a host callback. Validate returned record IDs against exact
evidence. Preserve existing JSON tool content and add an attribution result:
recorded IDs, unavailable, or partial/unknown with counts and reason. Known
mutations followed by recorder refusal, malformed response, capacity or timeout
return tool error/partial_success and preserve saved commit/applied/error fields.
Do not retry the original operation, append automatically, undo refs, or roll back
disk. A lost mutation/recording reply may remain unknown; no false confirmed log.

Read/list/diff, ship previews/local commit/push/reconcile and no-op mutations emit
no file-change record. Shipping has its existing receipts and does not rewrite
working-tree file content. No new GitFS ownership derives from Sessions files or
records. Existing partial-cancellation limitations remain honest.

## Acceptance

- [x] Write/edit/snapshot capture exact locked blob/commit receipts and distinct publication IDs; no-op/refused/unselected paths invent no publication or ownership.
- [x] Materialization records known applied content/deletion, preserves mixed actual effects and identifies unrecorded/uncertain paths under the metadata caps.
- [x] Real injected Sessions persists records; absent grant preserves standalone behavior; failed/malformed/hung recording reports partial/unknown without rollback or retry.
- [x] Existing inspection, selection, policy, reviewed local commit and recorded-push compatibility and public owner gates pass.

## Verify and Proof

Unit tests verify receipts under the existing lock, concurrent same-session write
attribution, no-op/refused operations, selected snapshot, exact materialization
and failed deletion, and capped mixed batches preserving known effects. Actual
native GitFS→Sessions fixtures use a real Sessions instance/session and prove
restart, all operation tags/targets, actor metadata, malformed/hung/failed recorder,
and an absent-grant standalone profile. Existing diff compares direct/overlay
SHA256 and conflict without callback or mutation; no journal-based inference.
Public `just test gitfs`, `just check gitfs`, `just build gitfs`; native maintained
tool-result/reviewed-ship/recorded-push suites plus change-provenance integration.
Wrappers disabled; coordinator owns workspace lock resolution and stale receipts.

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test gitfs
just check gitfs
just build gitfs
just build sessions
just build mcp
cargo build --manifest-path Cargo.toml --bin cartridge
GITFS_BINARY="$CARGO_TARGET_DIR/debug/gitfs" SESSIONS_BINARY="$CARGO_TARGET_DIR/debug/sessions" bun test ../gitfs.ctg/.cartridge/tests/integration/change-provenance.test.ts ../gitfs.ctg/.cartridge/tests/integration/tool-result.test.ts ../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts ../gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts
```
