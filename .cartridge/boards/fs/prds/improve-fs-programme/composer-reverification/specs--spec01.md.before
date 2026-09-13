---
complexity: low
footprint: [".cartridge/docs/change-provenance.md", ".cartridge/docs/revision-guards.md", ".cartridge/docs/search-pages.md", ".cartridge/tests/integration/change-provenance.test.ts", ".cartridge/tests/unit/search/tests.rs", ".cartridge/tests/unit/service/tests.rs", "Cargo.toml", "cartridge.json", "src/context.rs", "src/files.rs", "src/main.rs", "src/search.rs", "src/service.rs"]
---

# Qualify the integrated filesystem improvement programme

This no-code rollup preserves the two original acceptance checks. Qualify the
three direct outcomes together: additive direct/overlay change attribution,
revision-guarded publication, and bounded search pages with explicit stale or
truncated readback. The source is FS3a790233; baseline.json records actual current
receipts and the pending provenance integration rather than claiming it done.

Bind exactly three direct needs and all eleven distinct direct/transitive
contracts to spec hashes, complete dependency closure, current owner commits,
checked acceptance, valid collection receipts and current independent reviews
>=90 within the inherited five-round limit. The programme footprint equals the
union of its three FS-owned direct children: thirteen source paths. Referenced
external ownership remains with Sessions/GitFS/Runtime/Policy; no new APIs,
journal, ownership inference, cross-owner source edits or policy rules arise here.

Run the complete current FS public test/check and the seven pinned native
fixtures shared by the provenance integration. Those fixtures use disposable
actual Host compositions and real FS/GitFS/Sessions, with fault-only fake
recorders in negative cases. Pin the provenance executable checker and binding
files too, so changed executable artifacts cannot hide behind unchanged child
spec text. Print the actual receipt/review hashes, source commits and footprint.
External dependency changes require explicit revalidation; the engine does not
recursively invalidate every external need automatically.

Retain tested stale-write refusal and same-version writer serialization, existing
executable permissions/path validation and direct filesystem semantics, partial
publication failures without retry, search continuation tied to its observed
inputs and honest truncation, legacy touch snapshots without invented revisions,
and distinct overlay ownership even when disk/overlay contents diverge. Metadata
is reported invocation attribution, never authentication. Uncooperative external
writers retain the documented final-check race; publication and Sessions append
are separate effects; cancellation/disconnection can leave recording unknown;
bounded evidence logs can fill. Missing optional grant preserves standalone
GitFS; declared provider startup follows existing runtime lifecycle. No automatic
import, replay, rollback or watcher is introduced.

## Acceptance

- [x] All three direct outcomes and eleven-contract closure have current passing independent reviews, checked observable acceptance and source-bound receipts; exact owner footprint and proof inputs match.
- [x] Current FS public and composed native gates pass together; tested stale/refusal/partial/bounded behavior and remaining limits above are recorded at exact integrated owner revisions.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/prd.ctg
bun - <<'TS'
import fs from "node:fs";
import {createHash} from "node:crypto";
const base=".cartridge/boards/fs/prds/improve-fs-programme/";
for(const [file,digest] of Object.entries({"rollup-check.ts":"33e1325caa5b1d2a00a65aa9d3bae1c567c634eadf98e185b4d9e46cc14e1ecb","rollup-bindings.json":"08b0aa8789753ae01a0c5d71c54b7a1e5292f9cd97eafe1e22699592e899a5cd"}))
 if(createHash("sha256").update(fs.readFileSync(base+file)).digest("hex")!==digest)throw Error("rollup executable input changed: "+file);
TS
bun .cartridge/boards/fs/prds/improve-fs-programme/rollup-check.ts
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_PROFILE_DEV_DEBUG=0 CARGO_PROFILE_TEST_DEBUG=0 CARGO_INCREMENTAL=0 CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test fs
just check fs
just build fs
just build gitfs
just build sessions
cargo build --manifest-path Cargo.toml --bin cartridge
export FS_BINARY="$CARGO_TARGET_DIR/debug/fs" GITFS_BINARY="$CARGO_TARGET_DIR/debug/gitfs" SESSIONS_BINARY="$CARGO_TARGET_DIR/debug/sessions" PROVENANCE_EXPECT_SHIPPED_GRANTS=1
bun test ../fs.ctg/.cartridge/tests/integration/context.test.ts ../fs.ctg/.cartridge/tests/integration/change-provenance.test.ts ../gitfs.ctg/.cartridge/tests/integration/change-provenance.test.ts ../gitfs.ctg/.cartridge/tests/integration/tool-result.test.ts ../gitfs.ctg/.cartridge/tests/integration/reviewed-ship.test.ts ../gitfs.ctg/.cartridge/tests/integration/recorded-push.test.ts ../sessions.ctg/.cartridge/tests/integration/change-records.test.ts
```
