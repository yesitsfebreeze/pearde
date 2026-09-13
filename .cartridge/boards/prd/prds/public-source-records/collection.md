---
commit: e4fd43461237e8068e63ba1c29f6722434177c6c
spec-digests: {"spec01.md":"9cd1f231fb2ee9c5df523af30c18eae7918c7f1ef0a81f7b3f90132560ce1f05"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/prd/prds/public-source-records/specs/spec01.md: exit 0

Command SHA-256: dafb00afe810c90b4d15c2551d27850627b366c0eeace37f65ccb18fff903d29

```text
bun test v1.3.14 (0d9b296a)

.cartridge/tests/source-records.test.ts:
(pass) each board indexes only local records and exact reads preserve BOM CRLF and selected owner [17.18ms]
(pass) private and invalid visibility disappear without path title text or count; trusted scan retains them [18.27ms]
(pass) malformed UTF8 headers and duplicate visibility never become public exact text [15.77ms]
(pass) selectors source revision and record revision refuse changed or foreign input [3.86ms]
(pass) symlinks special files and late directory changes are explicit without outside reads [8.09ms]
(pass) file header public count aggregate and directory entry caps bound partial output [93.66ms]
(pass) response deadline retains all shared live I/O slots and closes delayed handles [34.65ms]
(pass) actual Host indexes and exactly reads all three source owners without Memory events spill or tool exposure [419.67ms]
(pass) strict public YAML rejects escaped flow alias merge and tagged ambiguity while trusted planning stays compatible [19.61ms]
(pass) failed growing reads debit actual bytes and cannot multiply the aggregate budget [11.33ms]
(pass) directory entry and depth limits are explicit and late opendir closes after timeout [345.80ms]
(pass) board selectors match declarations while hidden record paths remain excluded [4.09ms]
(pass) final exact-read serialization checks the same absolute deadline [63.50ms]

.cartridge/tests/source-declarations.test.ts:
(pass) real grammar retains hierarchical scanner identities and exports exact immutable declaration bytes [5.83ms]
(pass) missing descendants, backlinks and repeated mounts remain declarations without weakening strict scan [4.51ms]
(pass) selectors, exact configured authority and settings inode rules reject escapes and nonregular files [3.75ms]
(pass) malformed grammar and bounded declarations fail explicitly, with no child scan [15.46ms]
(pass) deadline covers filesystem work and static failures do not expose paths [20.19ms]
(pass) YAML alias member lists stop at the edge cap before expanding repeated maps [3.86ms]
(pass) service native method bypasses tool execution, callbacks, journals and spills [8.68ms]
(pass) a FIFO swapped in after metadata inspection cannot strand the settings open [9.42ms]
(pass) timed out native reads retain their capacity slots until actual IO settles [8.79ms]
(pass) actual Host invokes native declarations without Memory or event effects and tool exposure [357.24ms]

 23 pass
 0 fail
 215 expect() calls
Ran 23 tests across 2 files. [1.52s]
bun test v1.3.14 (0d9b296a)

.cartridge/tests/source-declarations.test.ts:
(pass) real grammar retains hierarchical scanner identities and exports exact immutable declaration bytes [9.92ms]
(pass) missing descendants, backlinks and repeated mounts remain declarations without weakening strict scan [5.61ms]
(pass) selectors, exact configured authority and settings inode rules reject escapes and nonregular files [5.25ms]
(pass) malformed grammar and bounded declarations fail explicitly, with no child scan [10.12ms]
(pass) deadline covers filesystem work and static failures do not expose paths [19.97ms]
(pass) YAML alias member lists stop at the edge cap before expanding repeated maps [3.30ms]
(pass) service native method bypasses tool execution, callbacks, journals and spills [3.93ms]
(pass) a FIFO swapped in after metadata inspection cannot strand the settings open [5.25ms]
(pass) timed out native reads retain their capacity slots until actual IO settles [9.20ms]
(skip) actual Host invokes native declarations without Memory or event effects and tool exposure

.cartridge/tests/service.test.ts:
(pass) real service describes and dispatches the native planner [114.70ms]
(pass) context and closed model input cannot override execution [19.28ms]
(pass) argument whitelist refuses injected paths, flags, adapters and excess counts [15.10ms]
(pass) board and PRD symlinks cannot escape central records [27.99ms]
(pass) duplicate invocation does not repeat a mutation and cancellation leaves a tombstone [132.79ms]
(pass) memory is attributed context and successful mutations publish scoped events [188.99ms]
(pass) only verified evidence enters the durable memory outbox with bounded retry [25.00ms]
(pass) memory replay acknowledges once and deduplicates simultaneous deliveries [41.83ms]
(pass) asynchronous jobs enforce session ownership and never signal stale journals [33.25ms]
(pass) host bridge correlates replies and closes pending requests [13.32ms]
(pass) wire hello, apply, describe, native call, reload and dispose [219.56ms]

.cartridge/tests/host.test.ts:
(skip) real runtime supplies memory and routes PRD events

.cartridge/tests/source-records.test.ts:
(pass) each board indexes only local records and exact reads preserve BOM CRLF and selected owner [21.05ms]
(pass) private and invalid visibility disappear without path title text or count; trusted scan retains them [38.22ms]
(pass) malformed UTF8 headers and duplicate visibility never become public exact text [18.46ms]
(pass) selectors source revision and record revision refuse changed or foreign input [4.54ms]
(pass) symlinks special files and late directory changes are explicit without outside reads [9.00ms]
(pass) file header public count aggregate and directory entry caps bound partial output [105.54ms]
(pass) response deadline retains all shared live I/O slots and closes delayed handles [33.35ms]
(skip) actual Host indexes and exactly reads all three source owners without Memory events spill or tool exposure
(pass) strict public YAML rejects escaped flow alias merge and tagged ambiguity while trusted planning stays compatible [32.83ms]
(pass) failed growing reads debit actual bytes and cannot multiply the aggregate budget [13.99ms]
(pass) directory entry and depth limits are explicit and late opendir closes after timeout [379.55ms]
(pass) board selectors match declarations while hidden record paths remain excluded [5.75ms]
(pass) final exact-read serialization checks the same absolute deadline [65.27ms]

.cartridge/tests/engine.test.ts:
(pass) scan preserves prose, counts members once and resolves cross-owner prerequisites [217.68ms]
(pass) isolated member cannot claim an unscanned prerequisite [152.49ms]
(pass) dependency cycles and held footprints are not dispatchable [311.75ms]
(pass) pagination and planning do not mutate source records [161.32ms]
(pass) claim is serialized across processes and board aliases [218.97ms]
(pass) edits preserve unrelated fields, comments and body and reject stale revisions [109.58ms]
(pass) PRD symlinks and oversized reads are refused [113.30ms]
(pass) invalid source mapping and missing specs cannot create a lane [138.48ms]
(pass) real collect verifies an isolated lane and commits integration evidence [794.15ms]
(pass) failed proof preserves source HEAD and never marks done [305.11ms]
(pass) forged done state and old commit cannot substitute for collection evidence [115.06ms]
(pass) run dry needs no adapter and failed workers are not treated as completion [286.79ms]
(pass) deadline kills owned worker groups and leaves a stopped checkpoint [325.72ms]
(pass) process timeout remains enforced after stdout closes [231.37ms]
(pass) process output has a hard byte limit [154.58ms]
(pass) rolling coordinator rescans analysis, dependencies and parent collection [3661.68ms]

.cartridge/tests/parity.test.ts:
(pass) plan addresses round-trip and member children inherit their actual source owner [456.96ms]
(pass) parent proof validates child contracts and current source across repositories [2092.06ms]
(pass) unverified pre-existing done records fail and persist their reason [136.31ms]
(pass) coordinator independently collects a finished owned claim and preserves foreign claims [1049.45ms]
(pass) partly failed runs publish only independently verified successful receipts to memory [1242.40ms]
(pass) owned descendants are confirmed stopped after normal leader exit [353.77ms]
(pass) owned descendants are confirmed stopped after cancellation [346.09ms]
(pass) collection refuses a contract changed by its own verification before committing code [304.21ms]
(pass) collection rejects already committed out-of-footprint modify [378.34ms]
(pass) collection rejects already committed out-of-footprint delete [384.79ms]
(pass) collection rejects already committed out-of-footprint rename [379.23ms]
(pass) collection rejects already committed out-of-footprint leading-space [352.42ms]
(pass) all serialized tool results obey the byte cap and retain omitted diagnostics [115.18ms]
(pass) planned waves honor member capacity with disjoint footprints [220.31ms]

.cartridge/tests/event-stream.test.ts:
(pass) event socket drains complete Unicode frames and the final event before process completion [62.54ms]
(pass) event socket rejects malformed and oversized Unicode frames while retaining later valid events [37.53ms]
(pass) event socket callback failures are reported and do not prevent draining later events [37.64ms]
(pass) event socket count budget is bounded while excess frames are drained [39.65ms]
(pass) event socket bytes budget is bounded while excess frames are drained [39.18ms]
(pass) real service run streams attributed domain events before returning bounded verified completion [1272.98ms]

.cartridge/tests/statusline.test.ts:
(pass) statusline selects mapped code owner and labels recorded weighted progress [657.62ms]
(pass) statusline renders safe first line without a board and tolerates malformed input [496.06ms]
(pass) statusline bounds transcript reading and uses latest assistant model and persona [173.10ms]
(pass) statusline shows local ahead and behind counts without contacting an upstream [356.05ms]

.cartridge/tests/records.test.ts:
(pass) central records retain explicit owners and a resolvable acyclic dependency graph [4813.30ms]
(pass) migration preserves original PRD fields, native states and historical review inputs [491.16ms]

.cartridge/tests/native-host.test.ts:
(skip) actual runtime and memory recall context and commit verified collection evidence
(skip) actual memory deduplication is never mistaken for committed collection ingestion
(skip) shipped MCP profile discovers PRD and routes real read, plan and mutation

6 tests skipped:
(skip) actual Host invokes native declarations without Memory or event effects and tool exposure
(skip) real runtime supplies memory and routes PRD events
(skip) actual Host indexes and exactly reads all three source owners without Memory events spill or tool exposure
(skip) actual runtime and memory recall context and commit verified collection evidence
(skip) actual memory deduplication is never mistaken for committed collection ingestion
(skip) shipped MCP profile discovers PRD and routes real read, plan and mutation

 74 pass
 6 skip
 0 fail
 5482 expect() calls
Ran 80 tests across 10 files. [25.27s]
$ tsc --noEmit

```
