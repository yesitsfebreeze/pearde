---
commit: c344629f00bd9afc4b5f993538600fc52e612ab2
spec-digests: {"spec01.md":"13961e65098fb2bf80ed1f3318127373af37941869272b0942afe9e70f1ec52d"}
child-contracts: {}
---

# Collection

/Users/feb/dev/cartridge/prd.ctg/.cartridge/boards/prd/prds/declared-source-edges/specs/spec01.md: exit 0

Command SHA-256: 6e02af2607baeb9924d37381040f398fdb183e7e9379362e814ab8d3a1a5b9c8

```text
$ bun test ./.cartridge/tests/*.test.ts
bun test v1.3.14 (0d9b296a)

.cartridge/tests/engine.test.ts:
(pass) scan preserves prose, counts members once and resolves cross-owner prerequisites [184.81ms]
(pass) isolated member cannot claim an unscanned prerequisite [143.30ms]
(pass) dependency cycles and held footprints are not dispatchable [262.17ms]
(pass) pagination and planning do not mutate source records [152.67ms]
(pass) claim is serialized across processes and board aliases [181.67ms]
(pass) edits preserve unrelated fields, comments and body and reject stale revisions [114.79ms]
(pass) PRD symlinks and oversized reads are refused [110.00ms]
(pass) invalid source mapping and missing specs cannot create a lane [138.97ms]
(pass) real collect verifies an isolated lane and commits integration evidence [685.08ms]
(pass) failed proof preserves source HEAD and never marks done [266.36ms]
(pass) forged done state and old commit cannot substitute for collection evidence [106.69ms]
(pass) run dry needs no adapter and failed workers are not treated as completion [254.44ms]
(pass) deadline kills owned worker groups and leaves a stopped checkpoint [301.64ms]
(pass) process timeout remains enforced after stdout closes [215.46ms]
(pass) process output has a hard byte limit [131.61ms]
(pass) rolling coordinator rescans analysis, dependencies and parent collection [3093.54ms]

.cartridge/tests/event-stream.test.ts:
(pass) event socket drains complete Unicode frames and the final event before process completion [58.32ms]
(pass) event socket rejects malformed and oversized Unicode frames while retaining later valid events [30.67ms]
(pass) event socket callback failures are reported and do not prevent draining later events [30.38ms]
(pass) event socket count budget is bounded while excess frames are drained [35.20ms]
(pass) event socket bytes budget is bounded while excess frames are drained [38.24ms]
(pass) real service run streams attributed domain events before returning bounded verified completion [1173.50ms]

.cartridge/tests/host.test.ts:
(pass) real runtime supplies memory and routes PRD events [391.40ms]

.cartridge/tests/native-host.test.ts:
(skip) actual runtime and memory recall context and commit verified collection evidence
(skip) actual memory deduplication is never mistaken for committed collection ingestion
(skip) shipped MCP profile discovers PRD and routes real read, plan and mutation

.cartridge/tests/parity.test.ts:
(pass) plan addresses round-trip and member children inherit their actual source owner [435.82ms]
(pass) parent proof validates child contracts and current source across repositories [1749.36ms]
(pass) unverified pre-existing done records fail and persist their reason [103.50ms]
(pass) coordinator independently collects a finished owned claim and preserves foreign claims [844.57ms]
(pass) partly failed runs publish only independently verified successful receipts to memory [1036.38ms]
(pass) owned descendants are confirmed stopped after normal leader exit [284.28ms]
(pass) owned descendants are confirmed stopped after cancellation [305.92ms]
(pass) collection refuses a contract changed by its own verification before committing code [335.21ms]
(pass) collection rejects already committed out-of-footprint modify [459.13ms]
(pass) collection rejects already committed out-of-footprint delete [364.60ms]
(pass) collection rejects already committed out-of-footprint rename [350.64ms]
(pass) collection rejects already committed out-of-footprint leading-space [339.46ms]
(pass) all serialized tool results obey the byte cap and retain omitted diagnostics [124.63ms]
(pass) planned waves honor member capacity with disjoint footprints [176.56ms]

.cartridge/tests/records.test.ts:
(pass) central records retain explicit owners and a resolvable acyclic dependency graph [5310.94ms]
(pass) migration preserves original PRD fields, native states and historical review inputs [531.75ms]

.cartridge/tests/service.test.ts:
(pass) real service describes and dispatches the native planner [93.38ms]
(pass) context and closed model input cannot override execution [14.86ms]
(pass) argument whitelist refuses injected paths, flags, adapters and excess counts [14.04ms]
(pass) board and PRD symlinks cannot escape central records [14.58ms]
(pass) duplicate invocation does not repeat a mutation and cancellation leaves a tombstone [73.73ms]
(pass) memory is attributed context and successful mutations publish scoped events [129.41ms]
(pass) only verified evidence enters the durable memory outbox with bounded retry [17.97ms]
(pass) memory replay acknowledges once and deduplicates simultaneous deliveries [35.86ms]
(pass) asynchronous jobs enforce session ownership and never signal stale journals [29.30ms]
(pass) host bridge correlates replies and closes pending requests [14.55ms]
(pass) wire hello, apply, describe, native call, reload and dispose [137.14ms]

.cartridge/tests/source-declarations.test.ts:
(pass) real grammar retains hierarchical scanner identities and exports exact immutable declaration bytes [6.22ms]
(pass) missing descendants, backlinks and repeated mounts remain declarations without weakening strict scan [5.25ms]
(pass) selectors, exact configured authority and settings inode rules reject escapes and nonregular files [4.30ms]
(pass) malformed grammar and bounded declarations fail explicitly, with no child scan [6.63ms]
(pass) deadline covers filesystem work and static failures do not expose paths [19.10ms]
(pass) YAML alias member lists stop at the edge cap before expanding repeated maps [2.68ms]
(pass) service native method bypasses tool execution, callbacks, journals and spills [3.58ms]
(pass) a FIFO swapped in after metadata inspection cannot strand the settings open [3.74ms]
(pass) timed out native reads retain their capacity slots until actual IO settles [8.02ms]
(pass) actual Host invokes native declarations without Memory or event effects and tool exposure [318.32ms]

.cartridge/tests/statusline.test.ts:
(pass) statusline selects mapped code owner and labels recorded weighted progress [455.98ms]
(pass) statusline renders safe first line without a board and tolerates malformed input [476.44ms]
(pass) statusline bounds transcript reading and uses latest assistant model and persona [179.22ms]
(pass) statusline shows local ahead and behind counts without contacting an upstream [297.28ms]

3 tests skipped:
(skip) actual runtime and memory recall context and commit verified collection evidence
(skip) actual memory deduplication is never mistaken for committed collection ingestion
(skip) shipped MCP profile discovers PRD and routes real read, plan and mutation

 64 pass
 3 skip
 0 fail
 5377 expect() calls
Ran 67 tests across 9 files. [23.24s]
$ tsc --noEmit

```
