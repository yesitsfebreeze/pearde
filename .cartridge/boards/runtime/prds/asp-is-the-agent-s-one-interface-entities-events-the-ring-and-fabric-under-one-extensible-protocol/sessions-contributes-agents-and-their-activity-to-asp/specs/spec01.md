---
complexity: small
footprint:
  - src/asp
  - src/changes.rs
  - src/lib.rs
  - cartridge.json
  - init.lua
  - README.md
  - .cartridge/help.md
  - .cartridge/tests/unit/asp.rs
  - .cartridge/tests/integration/asp.py
---

# Sessions contributes workspace activity to ASP

## Acceptance

- [x] Agent expansion returns roster facts with an admitted string revision.
- [x] A real fs write appears as an admitted touched edge with its digest on file expansion.
- [x] Both agent ownership and non-owning file contributions are declared.
- [x] Foreign workspace evidence does not collide with local file identities.
- [x] Fresh agent edges do not become stale against the session revision.
- [x] README and help document the provider and its limits.

## Implementation

Sessions declares the owned agent scheme and non-owned file scheme. The native entry uses the trusted process working directory, matching the file owner. Only evidence whose workspace equals that directory contributes file edges. Existing evidence validation enforces actor attribution.

Agent nodes and outgoing edges carry the session revision as a string. File expansion edges carry the recorded after digest, or omit revision for an absent target. This follows ASP's expanded-subject revision contract. Responses respect change_page_bytes and explicitly refuse overflow.

The integration probe uses supplied built artifacts and an isolated host. It writes through real fs, checks the resulting bytes and digest, and expands both file and agent through host ASP. It imports no sibling source.

## Verify and Proof

```sh
set -eu
d="$(mktemp -d)"
export CARGO_TARGET_DIR="$d"
export CARTRIDGE_BIN="$(command -v cartridge)"
export SESSIONS_MODULE="$d/debug/libsessions.dylib"
: "${FS_CARTRIDGE:?Supply a built fs cartridge artifact for the integration probe}"
cargo build --lib
cargo fmt --all --check
cargo clippy --all-targets
env -u CARTRIDGE_YOLO cargo test --lib asp::
env -u CARTRIDGE_YOLO cargo test --lib context::tests::native_context_metadata_contract
env -u CARTRIDGE_YOLO python3 .cartridge/tests/integration/asp.py
```

## Independent review

The candidate aa766580095db02d902201687b59da0fa5bde6e6 passed independent verification on 2026-09-19: six ASP tests, actual fs publication through host ASP, and the native context integration with the current host. The previous prototype's numeric revision, missing file declaration, workspace collision and false stale edges were corrected before integration. The prior coordinator's analysis is completed by this recovery pass at the user's request.

## Reload

Build the collected cartridge, then trust sessions and reload it. Verify the live ASP declaration and agent expansion before updating the composition pointer.

The broad 98-test suite exceeded the collection runner's fixed 120-second block deadline in an existing large-log stress test. Collection runs the provider and native context contracts plus the actual fs integration; the broad suite is run separately with a longer process allowance.
