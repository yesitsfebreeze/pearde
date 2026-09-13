---
commit: 0b39c5c52f8ff8bc024d90b30a0d5f0068ca727b
spec-digests: {"spec01.md":"0c5e9a09925601fec0740267173159cd355142ebb08be789fc5f5d152e2cb528"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/prd/prds/declared-source-edges/specs/spec01.md: exit 0

Command SHA-256: 6e02af2607baeb9924d37381040f398fdb183e7e9379362e814ab8d3a1a5b9c8

```text
$ bun test ./.cartridge/tests/*.test.ts
bun test v1.3.14 (0d9b296a)

.cartridge/tests/engine.test.ts:
(pass) scan preserves prose, counts members once and resolves cross-owner prerequisites [202.15ms]
(pass) isolated member cannot claim an unscanned prerequisite [134.25ms]
(pass) dependency cycles and held footprints are not dispatchable [339.37ms]
(pass) pagination and planning do not mutate source records [168.34ms]
(pass) claim is serialized across processes and board aliases [200.70ms]
(pass) edits preserve unrelated fields, comments and body and reject stale revisions [105.72ms]
(pass) PRD symlinks and oversized reads are refused [120.56ms]
(pass) invalid source mapping and missing specs cannot create a lane [145.38ms]
(pass) real collect verifies an isolated lane and commits integration evidence [681.49ms]
(pass) failed proof preserves source HEAD and never marks done [263.39ms]
(pass) forged done state and old commit cannot substitute for collection evidence [102.26ms]
(pass) run dry needs no adapter and failed workers are not treated as completion [248.71ms]
(pass) deadline kills owned worker groups and leaves a stopped checkpoint [296.26ms]
(pass) process timeout remains enforced after stdout closes [223.24ms]
(pass) process output has a hard byte limit [154.03ms]
(pass) rolling coordinator rescans analysis, dependencies and parent collection [3266.48ms]

.cartridge/tests/event-stream.test.ts:
(pass) event socket drains complete Unicode frames and the final event before process completion [57.16ms]
(pass) event socket rejects malformed and oversized Unicode frames while retaining later valid events [29.79ms]
(pass) event socket callback failures are reported and do not prevent draining later events [30.10ms]
(pass) event socket count budget is bounded while excess frames are drained [32.28ms]
(pass) event socket bytes budget is bounded while excess frames are drained [32.24ms]
(pass) real service run streams attributed domain events before returning bounded verified completion [962.46ms]

.cartridge/tests/host.test.ts:
(pass) real runtime supplies memory and routes PRD events [409.04ms]

.cartridge/tests/native-host.test.ts:
(skip) actual runtime and memory recall context and commit verified collection evidence
(skip) actual memory deduplication is never mistaken for committed collection ingestion
(skip) shipped MCP profile discovers PRD and routes real read, plan and mutation

.cartridge/tests/parity.test.ts:
(pass) plan addresses round-trip and member children inherit their actual source owner [394.73ms]
(pass) parent proof validates child contracts and current source across repositories [1677.56ms]
(pass) unverified pre-existing done records fail and persist their reason [102.01ms]
(pass) coordinator independently collects a finished owned claim and preserves foreign claims [872.38ms]
(pass) partly failed runs publish only independently verified successful receipts to memory [1162.30ms]
(pass) owned descendants are confirmed stopped after normal leader exit [314.70ms]
(pass) owned descendants are confirmed stopped after cancellation [293.54ms]
(pass) collection refuses a contract changed by its own verification before committing code [218.61ms]
(pass) collection rejects already committed out-of-footprint modify [354.21ms]
(pass) collection rejects already committed out-of-footprint delete [349.96ms]
(pass) collection rejects already committed out-of-footprint rename [348.45ms]
(pass) collection rejects already committed out-of-footprint leading-space [326.55ms]
(pass) all serialized tool results obey the byte cap and retain omitted diagnostics [108.26ms]
(pass) planned waves honor member capacity with disjoint footprints [167.25ms]

.cartridge/tests/records.test.ts:
(pass) central records retain explicit owners and a resolvable acyclic dependency graph [4559.65ms]
(pass) migration preserves original PRD fields, native states and historical review inputs [471.84ms]

.cartridge/tests/service.test.ts:
(pass) real service describes and dispatches the native planner [127.45ms]
(pass) context and closed model input cannot override execution [15.86ms]
(pass) argument whitelist refuses injected paths, flags, adapters and excess counts [19.78ms]
(pass) board and PRD symlinks cannot escape central records [14.60ms]
(pass) duplicate invocation does not repeat a mutation and cancellation leaves a tombstone [86.50ms]
(pass) memory is attributed context and successful mutations publish scoped events [153.99ms]
(pass) only verified evidence enters the durable memory outbox with bounded retry [16.43ms]
(pass) memory replay acknowledges once and deduplicates simultaneous deliveries [38.16ms]
(pass) asynchronous jobs enforce session ownership and never signal stale journals [32.31ms]
(pass) host bridge correlates replies and closes pending requests [15.43ms]
(pass) wire hello, apply, describe, native call, reload and dispose [191.50ms]

.cartridge/tests/source-declarations.test.ts:
(pass) real grammar retains hierarchical scanner identities and exports exact immutable declaration bytes [6.37ms]
(pass) missing descendants, backlinks and repeated mounts remain declarations without weakening strict scan [4.29ms]
(pass) selectors, exact configured authority and settings inode rules reject escapes and nonregular files [4.86ms]
(pass) malformed grammar and bounded declarations fail explicitly, with no child scan [8.35ms]
(pass) deadline covers filesystem work and static failures do not expose paths [20.08ms]
(pass) YAML alias member lists stop at the edge cap before expanding repeated maps [2.59ms]
(pass) service native method bypasses tool execution, callbacks, journals and spills [3.44ms]
(pass) a FIFO swapped in after metadata inspection cannot strand the settings open [4.99ms]
(pass) timed out native reads retain their capacity slots until actual IO settles [9.29ms]
(pass) actual Host invokes native declarations without Memory or event effects and tool exposure [354.66ms]

.cartridge/tests/source-records.test.ts:
(pass) each board indexes only local records and exact reads preserve BOM CRLF and selected owner [16.67ms]
(pass) private and invalid visibility disappear without path title text or count; trusted scan retains them [31.13ms]
(pass) malformed UTF8 headers and duplicate visibility never become public exact text [18.48ms]
(pass) selectors source revision and record revision refuse changed or foreign input [5.30ms]
(pass) symlinks special files and late directory changes are explicit without outside reads [6.96ms]
(pass) file header public count aggregate and directory entry caps bound partial output [74.91ms]
(pass) response deadline retains all shared live I/O slots and closes delayed handles [33.30ms]
(pass) actual Host indexes and exactly reads all three source owners without Memory events spill or tool exposure [363.86ms]
(pass) strict public YAML rejects escaped flow alias merge and tagged ambiguity while trusted planning stays compatible [24.59ms]
(pass) failed growing reads debit actual bytes and cannot multiply the aggregate budget [11.51ms]
(pass) directory entry and depth limits are explicit and late opendir closes after timeout [327.29ms]
(pass) board selectors match declarations while hidden record paths remain excluded [4.68ms]
(pass) final exact-read serialization checks the same absolute deadline [65.16ms]

.cartridge/tests/statusline.test.ts:
(pass) statusline selects mapped code owner and labels recorded weighted progress [627.56ms]
(pass) statusline renders safe first line without a board and tolerates malformed input [502.13ms]
(pass) statusline bounds transcript reading and uses latest assistant model and persona [184.73ms]
(pass) statusline shows local ahead and behind counts without contacting an upstream [319.62ms]

3 tests skipped:
(skip) actual runtime and memory recall context and commit verified collection evidence
(skip) actual memory deduplication is never mistaken for committed collection ingestion
(skip) shipped MCP profile discovers PRD and routes real read, plan and mutation

 77 pass
 3 skip
 0 fail
 5508 expect() calls
Ran 80 tests across 10 files. [23.72s]
$ tsc --noEmit

```
