# Verified client conversation mapping

Source: `181adb20248c6fdb718823919438939de55bdefc`. [Exact inputs and commands](proof-inputs.json).

- Public native tests: 32 passed, including all 25 existing recovery/checkpoint/persistence tests.
- Public check and build: passed.
- Actual SDK process integration: 3 tests, 48 assertions, passed. Reconnect, copied metadata, all three host scope dimensions, missing IDs and concurrent fresh processes are exercised.
- Atomic failure matrix covers write/file-sync/rename/directory-sync boundaries; stale revision and held OS locks create no sessions. Damaged index/target and symlink/traversal targets fail without rewriting preserved bytes.

Host configuration is the authority boundary. This owner API does not add transport
authentication or access control to existing general session methods. An unconfigured
shared service has instance/connection scope only. Mapping locks do not extend the
legacy transcript writer protocol across processes.

Review round 3 scored 96/100 by independent coordinator `/root`; the reviewed
contracts are unchanged. State/checklist/proof metadata was updated after verification.
Coordinator must collect this PRD and refresh the recovery receipt at this source revision.
