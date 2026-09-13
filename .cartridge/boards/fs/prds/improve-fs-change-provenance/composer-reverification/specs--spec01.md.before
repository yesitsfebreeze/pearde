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

Preserve all three original acceptance checks. This parent is an integration
rollup over the four canonical owner-local leaves in rollup-bindings.json;
it adds no product code. Current baseline-native.json binds real native FS de140668,
GitFS b4b95bb and Sessions c2693a7 behavior and binaries. Direct path-only touch and
absent overlay recording are missing; the existing diff already supplies visible
divergence. Reuse that diff and Sessions' new bounded reported-evidence API.

Hard prerequisites: the collected Sessions record schema/storage, direct FS
producer, GitFS producer and exact shipped-profile grants. The inherited mapping, revision-guard, readable-diff, tool-result interoperability
and policy-operation contracts remain transitive prerequisites. Nine exact
contracts, their complete dependency closure, spec hashes, >=90 current review
within five rounds, and current source-bound completion receipts are checked.
The footprint is exactly the union of direct FS producer children (one here);
transitive guard dependencies are verified without expanding this no-code rollup.
Source ownership for Sessions,
GitFS and runtime remains with their own canonical leaves. External changes
require explicit revalidation; the engine does not recursively invalidate every
external dependency automatically.

## Acceptance

- [x] A real Host profile with actual FS/GitFS/Sessions creates one session, edits one path directly and through its overlay, and reads distinct persisted actor/operation/target/revision records. Existing diff shows distinct base/overlay/disk and conflict. The recorded actor is invocation attribution, not an authenticated-client claim.
- [x] External edits and unrelated files add no records or ownership; read/search/fs.context/diff are observational. Legacy touched-file snapshots still read without invented revisions. Explicit selected snapshot/materialize preserve their own records and partial outcomes.
- [x] Guarded writes, no automatic replay, direct filesystem behavior and distinct overlay ownership remain; missing optional grant and recorder failure are honest. Current public owner/native/context suites pass, all prerequisite receipts and exact source-footprint union are checked, and limits are recorded.

## Verify and Proof

The maintained checker fails missing/stale collection receipts, changed dependency
closure/spec/source identity, unchecked acceptance, missing current review or
mismatched direct-owner footprint. It pins seven native fixture files and prints
actual receipt/review/source digests. Runtime must finish its collection before
this proof can pass; no draft or expected receipt is treated as complete.

```sh
set -eu
cd /Users/feb/dev/cartridge/prd.ctg
bun - <<'TS'
import fs from "node:fs";
import {createHash} from "node:crypto";
const base=".cartridge/boards/fs/prds/improve-fs-change-provenance/";
for(const [file,digest] of Object.entries({"rollup-check.ts":"ecaaa4e83b14321a6d4b6c44e2d2b82035c3632d285ab0cf32122379bc54f12f","rollup-bindings.json":"3f64cdb5ae814e57ac6b586902b3bd74b83cd7c3ac99dcbac5f50139fdad5905"}))
 if(createHash("sha256").update(fs.readFileSync(base+file)).digest("hex")!==digest)throw Error("rollup executable input changed: "+file);
TS
bun .cartridge/boards/fs/prds/improve-fs-change-provenance/rollup-check.ts
```

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test fs
just check fs
```

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test gitfs
just check gitfs
```

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test sessions
just check sessions
```

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test runtime
just check runtime
```

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just build fs
just build gitfs
just build sessions
cargo build --manifest-path Cargo.toml --bin cartridge
```

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
export FS_BINARY="$CARGO_TARGET_DIR/debug/fs" GITFS_BINARY="$CARGO_TARGET_DIR/debug/gitfs" SESSIONS_BINARY="$CARGO_TARGET_DIR/debug/sessions" PROVENANCE_EXPECT_SHIPPED_GRANTS=1
bun test ../fs.ctg/.cartridge/tests/integration/context.test.ts ../fs.ctg/.cartridge/tests/integration/change-provenance.test.ts ../gitfs.ctg/.cartridge/tests/integration/change-provenance.test.ts ../gitfs.ctg/.cartridge/tests/integration/tool-result.test.ts ../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts ../gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts ../sessions.ctg/.cartridge/tests/integration/change-records.test.ts
```

Limits: reported invocation identity only; optional recording requires an exact
grant; bounded logs may fill; filesystem/overlay publication and Sessions append
are separate operations; timeout/disconnect may leave recording unknown; no
global watcher/history or implicit ownership, import, rollback or retry. Existing
FS final-check race against uncooperative OS writers and GitFS partial-cancellation
limits remain. This is round3 of the original requirement, inherited by its splits.
