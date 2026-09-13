---
complexity: low
footprint:
- .cartridge/default/init.lua
- .cartridge/live/init.lua
- .cartridge/mcp/init.lua
- .cartridge/workspace/Cargo.lock
---

# Compose the existing producer and recorder explicitly

Change only the existing GitFS entries in default/live/MCP profiles to inject the
exact `sessions` key. Preserve other injected keys when present. These profiles
already declare Sessions; no optional-dependency or failed-startup behavior is
invented. The proxy profile currently contains no GitFS entry and is unchanged.
Resolve only the shared library dependency edges in workspace Cargo.lock, after
the three owner source manifests settle; getrandom0.4 is already resolved in the
workspace and gains a direct Sessions-library edge for publication identities.

Use the FS/GitFS maintained native provenance fixture through a disposable real
Host profile with actual native Sessions, FS and GitFS. Compare effective grants,
recorded producer calls and stored evidence with the injected Session ID. An
otherwise identical standalone GitFS profile omits Sessions and its grant and
retains mutation/diff behavior with explicit unavailable attribution. Do not use
a fake Sessions implementation for positive composed proof. Existing GitFS
standalone reviewed-ship/push tests remain compatibility evidence.

Verify runtime's public test/check and existing shipped-profile declaration tests,
then the maintained FS and GitFS provenance integration fixtures. Record exact
commands and binary hashes at implementation; root identifies the current runtime
public gate from its existing manifest instead of adding a new test runner.
No test file is required for these declarative lines if the real composition
fixture and existing profile gates prove the grant.

Existing user changes in these profile files are preserved, using an isolated
lane if required. Review exact grant-only hunks before integration; no overwrite
of user configuration is part of this leaf. The composed fixture must inspect
effective grants from the real Host and pin the three desired shipped-entry
declarations in the explicit `PROVENANCE_EXPECT_SHIPPED_GRANTS=1` proof mode;
ordinary producer fixtures do not depend on this later profile leaf. It must not
infer success merely from a hand-authored test profile.

## Acceptance

- [ ] Only the existing GitFS entries in default/live/MCP gain the exact Sessions grant; unrelated user profile changes remain byte-identical.
- [ ] Actual Host composition reports effective grants and records direct/overlay changes through the real Sessions owner; no-grant standalone behavior remains available.
- [ ] Runtime public test/check and owner native provenance fixtures pass with exact source/binary and desired-profile-hunk evidence.

## Verify and Proof

```sh
set -eu
cd /Users/feb/dev/cartridge/cartridge.ctg
export RUSTC_WRAPPER= RUSTC_WORKSPACE_WRAPPER= CARGO_TARGET_DIR="$PWD/target/tool-result-contract"
just test runtime
just check runtime
just build fs
just build gitfs
just build sessions
cargo build --manifest-path Cargo.toml --bin cartridge
PROVENANCE_EXPECT_SHIPPED_GRANTS=1 FS_BINARY="$CARGO_TARGET_DIR/debug/fs" GITFS_BINARY="$CARGO_TARGET_DIR/debug/gitfs" SESSIONS_BINARY="$CARGO_TARGET_DIR/debug/sessions" bun test ../fs.ctg/.cartridge/tests/integration/change-provenance.test.ts ../gitfs.ctg/.cartridge/tests/integration/change-provenance.test.ts
```
