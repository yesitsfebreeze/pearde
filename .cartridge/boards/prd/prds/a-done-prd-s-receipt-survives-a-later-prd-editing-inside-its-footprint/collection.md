---
commit: "7a44c88fba2322e6c4fa990da24407b3f02b6123"
verification-target: "committed"
original-commit: "7a44c88fba2322e6c4fa990da24407b3f02b6123"
spec-digests: {"spec01.md":"baea317b1d74ce6ae3b3acc241ccced14cf6b85aa0c2e942d8422fe5309d6707"}
child-contracts: {}
workspace-verified: false
workspace-drift: [{"path":".cartridge/help.md","sha256":"0daa476954291c65c1d3d4ff3f874b525bf6586f5660a6a36f89509af044d89e"},{"path":"README.md","sha256":"620e39d59b7dea9f3de1543bcfe11828a5565fd9440765bafe6d4e0ac4568d9c"}]
---

# Collection

Verified committed snapshot 7a44c88fba2322e6c4fa990da24407b3f02b6123 in /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/prd-commit-HHitUA/source.

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/prd/prds/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint/specs/spec01.md: exit 0

Command SHA-256: 205f0f95eb4a3674076e25bba7c07332529f41cefddf51ef3daf1bfa8e3878ed

```text
bun install v1.3.14 (0d9b296a)

+ @types/bun@1.3.10
+ typescript@5.9.3
+ yaml@2.9.1

6 packages installed [19.00ms]

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/prd/prds/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint/specs/spec01.md: exit 0

Command SHA-256: aa3fe7e894bb1b83dcf5a2afc41e37bb508ac9c193bf991f62f15312037d3b08

```text
passed: explicit reverify refreshes committed drift and preserves prior receipt, reverify refuses changed contract missing proof and active ownership, reverify refuses unresolved dependencies and failing proof, committed collection preserves dirty tails and reports workspace drift, legacy receipts remain strict and later committed drift needs reverify, reverification refreshes child rollups without automatic vouchers, verification races cancellation and history tampering fail closed, committed verification tests committed bytes rather than dirty workspace
bun test v1.3.14 (0d9b296a)

.cartridge/tests/collection-proof.test.ts:
(pass) explicit reverify refreshes committed drift and preserves prior receipt [1980.81ms]
(pass) reverify refuses changed contract missing proof and active ownership [813.53ms]
(pass) reverify refuses unresolved dependencies and failing proof [1540.24ms]
(pass) committed collection preserves dirty tails and reports workspace drift [1088.71ms]
(pass) legacy receipts remain strict and later committed drift needs reverify [2483.46ms]
(pass) reverification refreshes child rollups without automatic vouchers [6590.52ms]
(pass) verification races cancellation and history tampering fail closed [4496.35ms]
(pass) committed verification tests committed bytes rather than dirty workspace [796.48ms]

 8 pass
 0 fail
 87 expect() calls
Ran 8 tests across 1 file. [19.82s]

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/prd/prds/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint/specs/spec01.md: exit 0

Command SHA-256: 9e1316cd419bc36f2c03f0cdf4d1935f04c10aba038e0f8751fe8989c5b97c16

```text
bun test v1.3.14 (0d9b296a)

.cartridge/tests/engine.test.ts:
(pass) scan preserves prose, counts members once and resolves cross-owner prerequisites [489.64ms]
(pass) isolated member cannot claim an unscanned prerequisite [315.68ms]
(pass) dependency cycles and held footprints are not dispatchable [728.10ms]
(pass) pagination and planning do not mutate source records [740.82ms]
(pass) claim is serialized across processes and board aliases [1167.32ms]
(pass) edits preserve unrelated fields, comments and body and reject stale revisions [458.05ms]
(pass) PRD symlinks and oversized reads are refused [310.20ms]
(pass) invalid source mapping and missing specs cannot create a lane [363.05ms]
(pass) real collect verifies an isolated lane and commits integration evidence [3141.83ms]
(pass) failed proof preserves source HEAD and never marks done [920.86ms]
(pass) a test block collects only when the runner reports every named test as passed [1300.06ms]
(pass) a lane checks out submodules at their pinned commits and collect removes them [1545.58ms]
(pass) forged done state and old commit cannot substitute for collection evidence [246.45ms]
(pass) run dry needs no adapter and failed workers are not treated as completion [519.07ms]
(pass) deadline kills owned worker groups and leaves a stopped checkpoint [425.39ms]
(pass) process timeout remains enforced after stdout closes [341.81ms]
(pass) process output has a hard byte limit [307.33ms]
(pass) rolling coordinator rescans analysis, dependencies and parent collection [12253.44ms]
(pass) hand edits to state or claim are reported and refused until adopted [3877.54ms]
(pass) a hand-written commit is reported [627.60ms]
(pass) an adopted claim that changed hands warns until it is released [855.87ms]
(pass) a PRD re-added at a removed path inherits no recorded values [1122.68ms]
(pass) dropping the values of a removed or rehomed record is logged and warned once [1158.85ms]
(pass) check reports an unwritable field store instead of a raw errno [333.83ms]
(pass) body edits, untracked records and engine transitions raise no field problem [657.96ms]

 25 pass
 0 fail
 128 expect() calls
Ran 25 tests across 1 file. [34.28s]

```

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/prd/prds/a-done-prd-s-receipt-survives-a-later-prd-editing-inside-its-footprint/specs/spec01.md: exit 0

Command SHA-256: 310c3273b56d4ebff6f5d330300de4d98bf6c6eccc53378b65b7e0f5f206fb98

```text
bun test v1.3.14 (0d9b296a)

.cartridge/tests/records.test.ts:
(pass) the accepted-states check fails an unknown state and passes deferred, on a fixture board [6.95ms]
(pass) migration preserves original PRD fields, native states and historical review inputs [2134.01ms]

 2 pass
 1 filtered out
 0 fail
 4276 expect() calls
Ran 2 tests across 1 file. [2.21s]
$ tsc --noEmit

```
