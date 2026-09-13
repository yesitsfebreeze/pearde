# Native TypeScript parity: independent final review

2026-09-13. Reviewer: `/root/prd_real_host_fixture`, independent of production
implementation; this reviewer authored the real-host and event fixtures.
**85/100 — FAIL: two reproduced blockers remain in this source snapshot.**
This evaluates the native rewrite contract, not the product backlog. Passing
regressions do not override the additional failures below.

Authority: [11-invariant handoff](native-rewrite-review-handoff.md),
[earlier five-case snapshot](native-typescript-review-snapshot.md), and
[review method](../workflows/review-plan.md). This is the next substantive native
source review after the linked snapshot; preserve the canonical round history
and five-round allowance. No source, live board, claim, personal state or index
was changed. Reproductions used Bun and disposable repositories.

## Blocking findings

### B1: Committed worker changes bypass the source footprint

`src/lifecycle.ts`, collection's status check and fast-forward boundary.
Declare `footprint: [allowed.txt]`, publish a checked acceptance contract verifying
that file, and claim an isolated lane. In the lane, change both `allowed.txt` and
`outside.txt`, then commit both before calling `execute('collect', board, ['one'])`.
Collection checks only uncommitted status, merges the whole candidate commit,
and records valid-looking completion:

```json
{"exit_code":0,"error":"","state":"done","outside":"UNAUTHORIZED\n","proof":null}
```

Here `proof: null` is `completionProblem(...)` reporting no problem. The source
repository's out-of-footprint file was actually changed. This violates the
integration boundary, even though the declared verification passes.

Fix: before changing the source HEAD, validate all changes from source baseline
to candidate against declared paths, including already committed changes,
renames and deletions. Retain a regression where the worker commits its own
changes. Reversible disposable reproduction: `bun /private/tmp/prd-final-review-probe.ts`.
The temporary helper creates and removes its fixture repositories itself.

### B2: Error responses bypass the configured serialized byte limit

`src/service.ts`, dispatch exception returns and final ToolResult boundary.
Construct `Service({root: temporaryRecords, max_output_bytes: 1024})`; call read
with a valid host context and arguments `['one', '--' + '界'.repeat(2000)]`.
The unsupported-flag diagnostic is returned directly by the catch branch:

```json
{"bytes":6085,"cap":1024,"error":true}
```

The 6,085 bytes measure `Buffer.byteLength(JSON.stringify(answer))`, not character
count. Normal response checks also measure the inner value, while the outer
`content` string adds JSON escaping. A single final ToolResult budget must cover
success, status, cancellation and errors, with byte-safe fallback and durable
retention of omitted evidence. Reproduction:
`bun /private/tmp/prd-final-review-bounds.ts`.

## Contract coverage

| Handoff boundary | Observed result |
| --- | --- |
| 1. One native engine and owner | CLI/service share native domain operations; real MCP calls pass. No second engine was executed in this review. |
| 2. Record/code separation | Separate-repository collection and invalid-mapping refusal pass; B1 leaves the footprint incomplete. |
| 3. Master/member dependency context | Cross-member unresolved dependencies refuse; plan addresses round-trip. |
| 4. Atomic mutation/claims | Concurrent same-PRD claims through aliases have one winner; mutation SQLite locks are separate from run locks. |
| 5. Member sub-PRD identity | Member child creation retains owner mapping and full identity. |
| 6. Evidence before done | Executable proof, committed contracts/receipts and stale-contract rejection pass; B1 remains blocking. |
| 7. Recursive parent proof | Cross-repository children and changed-child contract invalidation pass. |
| 8. Accountable dispatch | Owned claims collect independently; foreign claims remain; pre-existing forged done fails; member wave limits pass. |
| 9. Cancellation/process ownership | TERM-ignoring descendants stop after normal leader exit and cancellation; stale journals never supply signal targets. |
| 10. Events and memory | Actual runtime/memory/MCP fixture passes; committed and deduplicated acknowledgments differ; event framing, caps, attribution and delivery loss pass. |
| 11. Bounded service boundary | Input authority checks, session jobs and bounded public summaries pass; B2 remains blocking. |

The earlier snapshot's five concrete failures are covered by passing regressions:
owned-descendant cleanup, forged pre-existing done refusal, authorized returning
worker collection, root plan-address resolution, and member child creation.

## Executed evidence

```sh
CARTRIDGE_TEST_BIN=$PWD/cartridge.ctg/target/debug/cartridge \
MEMORY_TEST_BIN=$PWD/cartridge.ctg/target/debug/memory_cartridge \
bun test ./prd.ctg/.cartridge/tests/engine.test.ts \
  ./prd.ctg/.cartridge/tests/service.test.ts \
  ./prd.ctg/.cartridge/tests/parity.test.ts \
  ./prd.ctg/.cartridge/tests/native-host.test.ts \
  ./prd.ctg/.cartridge/tests/event-stream.test.ts
# 45 pass, 0 fail; 300 assertions; 11.82 seconds.
```

The two additional probes above were independently executed and reproduced their
failures. Host tests use actual Cartridge, memory and MCP binaries, isolated
stores and repositories, and a local deterministic embedding endpoint. Model
quality, remote adapters, other operating systems, crashes during every Git
write, and full formal legacy parity are outside this bounded pass. Record
migration validation is covered elsewhere and was not rerun here.

## Reviewer score

| Dimension | Score | Reason |
| --- | ---: | --- |
| Current user value and scope | 19/20 | Native ownership and user-visible entry points work; full legacy UI equivalence is not claimed. |
| Ownership and reuse | 19/20 | Shared engine, host-owned context, reusable native record and process boundaries. |
| Dependencies and implementable slices | 18/20 | Explicit mappings, dependency gates, scoped dispatch and member limits have executable coverage. |
| Observable acceptance and baseline evidence | 16/20 | Extensive real integration evidence; B1 disproves the complete footprint contract. |
| Failure, recovery and compatibility | 13/20 | Cancellation and pending-memory behavior are tested; B2 breaks a stated boundary. |
| **Total** | **85/100** | **FAIL; both blockers require correction and a revision-bound recheck.** |

## Reviewed source and input SHA-256

These hashes identify the reproduced failures, not any later corrective edits.

```text
cli.ts         3fd572dee32dc91e9ce08911b768a78f2488c8792a5d7dc5058a274d0a9c8f89
coordinator.ts 4da0954665de007d8bd5c3facffaf3317b26cafdb6f4ea57fb2ee9ca395e773c
engine.ts      ed3ce2e3816c42ecc919da8ad908ecd40cbda8993a04efdee0274f99fd9a5c97
lifecycle.ts   91bd20c8bb53819fd7c771e09b436f0f76eab68eac40350e62275182d73822f8
planner.ts     fd60f4c7603e212279d47bf1bc37a30e7f2b28d2865b9cc3cbb175317807fcfe
process.ts     873577e65b6fc89c6d4cda7d307e10f006dc58b6506ca23ff344f49fcc3e5867
records.ts     7f60038af768a68ee51f7755a232efd1c60e2e6c6c06598b3b43e5c6faf6f4ed
service.ts     d45569542d15efdb8263a1370adcde92adf20f591a9b04d4fcff670852ede912
handoff        695f2770ae98f8ec0d893e4845282b98ae3de13f5721790f406a6102759780d6
snapshot       1ca8f86ff54b69b1f1f3664dd19e919b9da2aeee9d327f2f30667963ced1a8f5
review-plan    51e87e859b68439ed1714063e3e253eea36dfb16ec20183f1c24d86fdedad121
```

## Round 3: corrective revision recheck — 93/100 PASS

This appended assessment supersedes the initial 85/100 verdict for the exact
source hashes below. The original failures and evidence remain intact. Review
sequence: earlier TypeScript snapshot (round 1), the initial assessment above
(round 2), this corrective recheck (round 3). The five-round allowance was not
reset. Corrections observed during this recheck are documented here rather than
silently replacing failed evidence.

**No blocking finding remains in this bounded review of the final revision.**
This is delegated reviewer approval of the native rewrite contract, not approval
of product PRDs or a claim of complete formal equivalence with every legacy
feature. The original scope limitations still apply.

### Corrections and independently repeated reproductions

B1 now validates the complete committed source-baseline-to-candidate diff before
verification and again before integration. Rename detection is disabled so both
old and new paths are checked. The original reproduction now returns:

```json
{"exit_code":2,"error":"committed path is outside the PRD footprint: outside.txt","state":"claimed","outside":"keep\n","proof":"PRD is not done"}
```

An intermediate implementation used the trimming `git()` helper on NUL-delimited
paths. A second probe with an unauthorized file named ` allowed.txt` reproduced
the same bypass because its leading space disappeared. That observation was
reported immediately and corrected by reading raw subprocess stdout. The
leading-space probe now also refuses, leaves the source unchanged and retains
the claim. Maintained regressions cover committed modifications, deletions,
renames and leading-space names. Both path probes remain reproducible from the
previous helper and `/private/tmp/prd-final-review-spaces.ts`.

B2 now budgets the serialized ToolResult, including `content` string escaping,
on all call, cancellation, error and job-status return paths. An omitted full
response is retained in the ignored service response journal with a returned
identifier. The original Unicode error reproduction now produces **246 bytes
against a 1,024-byte cap**. The maintained regression checks error, Unicode and
escaping cases and verifies retained full diagnostics. Proof is processed for
memory before public-response reduction.

### Event transport failure retained and corrected

An intermediate combined run passed 21 tests and failed one real service event
check: only `plan.updated` and `worker.started` arrived, although the job
completed. An isolated retry passed; that retry was not accepted as clearance.
Coordinator stress subsequently captured `EPIPE: broken pipe, write`, with four
native writes unavailable, and failures also appeared in simple descriptor
fixtures. These observations identify a failure of the inherited-fd3 transport;
they do **not** establish an upstream garbage-collection or library root cause.
Adding only an EOF wait did not resolve the failures.

The final revision replaces inherited fd3 with a private per-invocation Unix
socket. The process owns its listener, single accepted connection, NDJSON
limits, final drain and cleanup. The CLI connects, bounds queued writes and
flushes before returning its result. Host attribution and unavailable/loss
accounting remain intact. This reviewer updated only the owned event fixture to
use the new transport, preserving all six behavioral tests and their assertions.

Independent validation of this replacement:

```sh
bun test ./prd.ctg/.cartridge/tests/event-stream.test.ts --rerun-each 10
# 60 pass, 0 fail; 790 assertions; 10.37 seconds.

CARTRIDGE_TEST_BIN=$PWD/cartridge.ctg/target/debug/cartridge \
MEMORY_TEST_BIN=$PWD/cartridge.ctg/target/debug/memory_cartridge \
bun test ./prd.ctg/.cartridge/tests/parity.test.ts \
  ./prd.ctg/.cartridge/tests/native-host.test.ts \
  ./prd.ctg/.cartridge/tests/event-stream.test.ts
# 23 pass, 0 fail; 217 assertions; 8.81 seconds.

bun run --cwd prd.ctg check
# PASS: tsc --noEmit.
```

The successful repeated socket tests are evidence for the replacement, not an
assertion that the superseded descriptor failure vanished without a change.
The coordinator's broader suite is separate evidence and is not counted here
as independently executed by this reviewer.

### Revision-bound reviewer score

| Dimension | Score | Basis |
| --- | ---: | --- |
| Current user value and scope | 19/20 | Native planning, CLI/MCP and real host behavior remain demonstrated. |
| Ownership and reuse | 19/20 | One engine, explicit code owners and trusted host event context. |
| Dependencies and implementable slices | 18/20 | Dependency, alias, claim, member-capacity and owned-collection regressions pass. |
| Observable acceptance and baseline evidence | 19/20 | Both reproduced blockers now fail safely; committed-path edge cases have durable tests. |
| Failure, recovery and compatibility | 18/20 | Serialized limits retain evidence; replacement event transport survives the focused repeated run; broader crash/platform proof remains outside scope. |
| **Total** | **93/100** | **PASS for this reviewed revision, with no remaining observed blocker.** |

Final source SHA-256 after validation:

```text
cli.ts         438cf72a6a6d70f98e9d337e6b1100aab5247bafcfecaf0926f792066b10d9ed
coordinator.ts 8341a5331d76c476e495b3528faff58236aef9c9d299dcac6b1cf64562a0a83c
engine.ts      ed3ce2e3816c42ecc919da8ad908ecd40cbda8993a04efdee0274f99fd9a5c97
lifecycle.ts   8522f11d6c56bbb5b7487931c23594801953cc8a915af0657fa219d55717be16
planner.ts     fd60f4c7603e212279d47bf1bc37a30e7f2b28d2865b9cc3cbb175317807fcfe
process.ts     0be4a5778d856b96eb6603e5aba9c98e462109f21d0a18e84a5d9e9cf697c518
records.ts     7f60038af768a68ee51f7755a232efd1c60e2e6c6c06598b3b43e5c6faf6f4ed
service.ts     1e7ad44209ed7aeb14ea3e43fd346ab2c7662b0500184e5df1348a53e40ec096
```

The handoff, earlier snapshot and review-workflow input hashes are unchanged from
the initial assessment. Later substantive source changes make this approval
stale until checked within the remaining allowance.
