# Source-bound native facade proof

Clean Memo source `a458148fb21f85cabcd9e1ced85c96c581b8e0b2` passes all approved gates: 83 Memo unit tests, public check/build, 67 Landscape tests, and 10 real native/SDK compatibility tests with 10,415 assertions. `proof-inputs.json` binds exact source, dependency, executable and log bytes.

The real Runtime→Memo→PRD fixture finds five public owners across three board levels and two cartridge document roots, performs owner-exact raw-byte reads, preserves BOM/CRLF and physical `.jd` selection, and verifies source files unchanged. Poisoned inactive init.lua and the Memory trap remain untouched. Actual SDK cases reject request authority overrides, absent grants, private metadata, stale and cross-owner references; existing inventory/context/validation routes remain compatible. Staged native delays preserve completed cartridge evidence under one deadline. The blocking-read test retains all eight slots after request timeout until actual work returns.

Measured YAML merge syntax initially exposed private metadata because the existing parser retains merge keys. The root-approved narrow public-source repair rejects recursive decoded `<<` keys before index/read output. Duplicate visibility, private/public aliases, quoted/nested merges and real SDK exact-read parity are covered. Saved baseline and before/after repair hashes preserve this failure; legacy projection parsing remains outside this leaf.

Runtime proof uses the coordinator-approved immutable binary copy with equal source-before, copy and source-after hashes, recorded in `proof/runtime-copy-inputs.json`. This is execution binding only; test assertions and default executable path are unchanged. Keep the copy until collection completes.

Resource guarantees cover actual explicit blocking document jobs. Tokio metadata jobs may outlive dropped requests internally, and the reused reader does not promise race-proof confinement against hostile concurrent filesystem replacement. No global cache, Memory service, runtime activation or filesystem mutation was added.
