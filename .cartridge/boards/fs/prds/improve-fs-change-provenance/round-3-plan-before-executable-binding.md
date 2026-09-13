---
complexity: low
footprint:
- Cargo.toml
- src/main.rs
- src/service.rs
- src/files.rs
- .cartridge/tests/unit/service/tests.rs
- .cartridge/tests/integration/change-provenance.test.ts
- .cartridge/docs/change-provenance.md
---

# Qualify attributable direct and overlay changes together

Preserve all three original acceptance checks. This parent becomes an integration
rollup after root creates the owner-local leaves proposed in owner-split-proposal.md;
it adds no product code. Current baseline-native.json binds real native FS de140668,
GitFS b4b95bb and Sessions c2693a7 behavior and binaries. Direct path-only touch and
absent overlay recording are missing; the existing diff already supplies visible
divergence. Reuse that diff and Sessions' new bounded reported-evidence API.

Hard prerequisites: the proposed Sessions record schema/storage, direct FS
producer, GitFS producer and exact shipped-profile grants. Both inherited mapping
and readable-diff contracts remain transitive prerequisites. Root must bind their
canonical IDs, exact spec hashes, current >=90 review within inherited five rounds
and current source-bound completion receipts before this rollup proof can pass.
The footprint is exactly the FS producer footprint; source ownership for Sessions,
GitFS and runtime remains with their own canonical leaves. External changes
require explicit revalidation; the engine does not recursively invalidate every
external dependency automatically.

## Acceptance

- [ ] A real Host profile with actual FS/GitFS/Sessions creates one session, edits one path directly and through its overlay, and reads distinct persisted actor/operation/target/revision records. Existing diff shows distinct base/overlay/disk and conflict. The recorded actor is invocation attribution, not an authenticated-client claim.
- [ ] External edits and unrelated files add no records or ownership; read/search/fs.context/diff are observational. Legacy touched-file snapshots still read without invented revisions. Explicit selected snapshot/materialize preserve their own records and partial outcomes.
- [ ] Guarded writes, no automatic replay, direct filesystem behavior and distinct overlay ownership remain; missing optional grant and recorder failure are honest. Current public owner/native/context suites pass, all prerequisite receipts and exact source-footprint union are checked, and limits are recorded.

## Verify and Proof

After child integration, make an executable receipt checker pinning all direct and
transitive spec SHA256s and their current review/collection evidence, using existing
records scan/completionProblem/feet APIs. Fail missing/stale receipts, review score
below 90, unchecked acceptance, or footprint mismatch; do not treat draft proposals
as completed records. Pin the maintained composed fixture bytes in this spec before
collection. This input binding is deferred until canonical owner leaves exist;
the current parent is not ready to collect.

Parent executable contract binding is deliberately deferred until the canonical
child specs and receipts exist. Root may record the integration plan review now,
but this rollup remains open, not specced or collected, until the executable
checker and exact pinning are written and reviewed against this same scope.

From runtime with `RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER=` and assigned shared target:
run public FS, GitFS, Sessions and runtime test/check gates, build their native
binaries, then maintained FS context/provenance and GitFS provenance/tool-result/
reviewed-ship/recorded-push suites. Record exact native binary hashes, source SHAs,
positive record readback, actual diff and unchanged unrelated HEAD/index/ref/file
bytes. Use only disposable local repositories/profiles; no real remote or secrets.

Limits: reported invocation identity only; optional recording requires an exact
grant; bounded logs may fill; filesystem/overlay publication and Sessions append
are separate operations; timeout/disconnect may leave recording unknown; no
global watcher/history or implicit ownership, import, rollback or retry. Existing
FS final-check race against uncooperative OS writers and GitFS partial-cancellation
limits remain. This is round3 of the original requirement, inherited by its splits.
