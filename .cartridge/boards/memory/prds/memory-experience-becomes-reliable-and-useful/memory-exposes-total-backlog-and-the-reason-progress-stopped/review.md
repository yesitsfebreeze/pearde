# @memory/memory-experience-becomes-reliable-and-useful/memory-exposes-total-backlog-and-the-reason-progress-stopped review history

Canonical plan: @memory/memory-experience-becomes-reliable-and-useful/memory-exposes-total-backlog-and-the-reason-progress-stopped. Threshold: 90/100 with no blocking findings. Round limit: five. Inherited rounds: none. This record rates plans, not product behavior.

## Round 1 — 2026-09-19

Reviewer: `/root/memory_plan_review_b`. Plan SHA256: `c3cfdc3c047f2b069a43c7154ca576427cafa14a866fa40dfb6be84a862d9bca`. Specs: not yet published. Source evidence: [pinned source digests](../evidence/source-digests.json).

| Dimension | Score / 20 |
| --- | ---: |
| User value and scope | 20 |
| Ownership and reuse | 19 |
| Dependencies and implementable slices | 18 |
| Acceptance and baseline evidence | 18 |
| Failure, recovery and compatibility | 17 |

Total: **92/100 — PASS**. No blocking finding; retain the bounded specification recommendations in the full review.

[Full independent findings](../evidence/review-b-round-1.md), SHA256 `3dd48baee70698073396f5128480ef808d3915faf4e9dd5e82ef424bfc8c5b49`. Validation: targeted source, PRD and dependency reads; no behavioral tests run by the reviewer. Coordinator test evidence is separately attributed in the investigation. User rating: not requested under delegated policy. Rounds used: 1; remaining: 4.

## Round 2 — 2026-09-19 — implementation specification

Independent reviewer: `/root/lifecycle_prerequisite`. This review evaluates the
published plan against current source; it does not certify implementation or
claim that proposed tests already exist or have passed. No source, specification
or claim was changed by the reviewer.

- PRD SHA-256: `f554dce83b4edd29362a231e67f92eb7ed1bad31c8e1431be5742143888a4331`.
- Specification SHA-256: `929a845e3faafb297075c69eac8ef292c5fab785324591a2c3e5e6187d1b7398`.
- Source baseline inspected: memory `d9161cd2f3a363915c7a7d642a4955e7a3836065`, with preserved live dirty owner work identified by the specification.

| Dimension | Score / 20 |
| --- | ---: |
| User value and scope | 20 |
| Ownership and reuse | 19 |
| Dependencies and implementable boundaries | 16 |
| Observable acceptance and evidence | 15 |
| Failure, recovery and compatibility | 17 |

Total: **87/100 — FAIL**. Two blocking findings. Rounds used: 2; remaining: 3.
Round 1 remains historical plan evidence.

### S1 — Blocking: the performance gate measures the wrong layer/profile

The only proposed polling benchmark runs inside `cargo test -p store_core
experience --lib`, without `--release`. It can establish metadata-read cost, but
cannot establish the declared canonical status serialization, complete RPC
projection cost or 8 KiB response bound. Store-only timing does not substantiate
the status consumer's gate. Debug timings also do not provide an appropriate
optimized operating baseline.

Add a small focused release-mode test/probe that exercises the actual canonical
status projection and serialization on both 1,000 and 100,000 pending-row
fixtures, with the published sample count and numeric gates. Name that test in
an executable pass gate. Preserve the current behavioral suites; label any
storage-only measurements separately. Record build profile, fixture/setup and
migration times, byte sizes and p50/p95/max. Isolate target directories and ensure
fixture setup/compilation is not silently included in the polling samples or
allowed to turn the existing collection block limit into a false pass. No broad
benchmark framework or unrelated retrieval gate is required.

### S2 — Blocking: the 100 ms contention promise exceeds the selected path

The acceptance currently says status calls under a held graph writer finish
within 100 milliseconds with graph_busy. The local canonical projection can
satisfy that using try_read. However, attached native probes call
`src/transport/src/owner.rs::read_observed`, which first executes
`client.health()`. `src/rpc/src/lib.rs::MemoryService::health` calls
`health_stats`, which takes a graph read lock. Thus an attached probe can wait
until its configured deadline before reaching the new nonblocking trace status
projection; the existing default probe deadline is 2,000 milliseconds. The
proposed 22-file footprint does not modify that transport handshake.

Scope the 100 millisecond graph_busy guarantee to the actual canonical local
RPC/ASP projection. Separately require a native/attached probe to respect its
single existing configured total deadline, including owner identity, ready and
trace requests, and test timeout/generation behavior. Retain the existing
transport semantics rather than expanding this status leaf into a transport
repair. Ensure every graph reacquisition in the writer-status helper is also
nonblocking: merely changing its caller's first read to try_read leaves a race
before the helper's current subsequent graph.read calls.

### Additional concrete clarifications

- Preserve the exact existing trace shape `pending: {rows, bytes}`. The prose's
  `pending_rows/pending_bytes` names are not existing wire fields.
- A manual attempt must neither invent nor erase a background retry deadline
  that the scheduler has actually selected. Define the separation between last
  attempt origin and independently scheduled worker state.
- The unsupported/corrupt version rule is correctly fail-closed. Preserve the
  explicit unavailable result through the existing higher-level bootstrap
  fallback; never render its missing store as a known zero backlog.

### Findings retained as strengths

The specification assigns one transactional counter authority, handles import
overwrite deltas and unknown historical ages, refuses fabricated historical
progress, reuses the collected writer guard, preserves native cache/ticket
semantics and explicitly reserves ASP status before fact hydration. It honestly
distinguishes embedded deterministic build-input identity from final artifact
SHA-256 and defers actual A-loaded/B-on-disk proof to the parent's controlled
integration. Its precise expanded footprint and required owner-baseline recheck
avoid absorbing unrelated presentation work.

Validation: read the full PRD/specification and earlier review; inspected store
initialization/intake commits, writer/status/drain paths, cycle journal, native
status cache and probe tests, owner read transport, RPC health handshake, ASP
dispatch, scheduler, build script/identity and loader metadata. The local ASP
search was available but returned no relevant code evidence; its PRD contributor
reported a timeout, so source findings rely on direct reads. No new behavioral
tests were run during this plan review.

Next action: one bounded author revision addressing S1 and S2 plus the field and
scheduler clarifications, followed by independent round 3. The reviewer does not
modify the authored specification or perform a lifecycle transition.

## Round 3 — 2026-09-19 — bounded performance/deadline revision

Independent reviewer: `/root/lifecycle_prerequisite`. Reviewed the full revised
specification, unchanged PRD and round 2 source findings. No source or authored
specification was modified, and no proposed implementation tests were run.

- PRD SHA-256: `f554dce83b4edd29362a231e67f92eb7ed1bad31c8e1431be5742143888a4331`.
- Specification SHA-256: `d8cfbc7e1ea33389053bcf6a6250ae41131ee81bf75eb37b2b37df643cc5b96b`.

| Dimension | Score / 20 |
| --- | ---: |
| User value and scope | 20 |
| Ownership and reuse | 19 |
| Dependencies and implementable boundaries | 18 |
| Observable acceptance and evidence | 19 |
| Failure, recovery and compatibility | 18 |

Total: **94/100 — PASS**. No unresolved plan blockers. Rounds used: 3;
remaining: 2. Earlier reviews remain preserved.

S1 is resolved: a named release-mode RPC test now measures canonical status
projection plus JSON serialization at both fixture sizes, with numeric latency,
scale and 8 KiB response limits. Storage-only evidence is explicitly diagnostic.
Foreground compilation/setup is separately identified and does not certify a
latency result or bypass the normal collection timeout.

S2 is resolved: the 100 millisecond graph_busy contract is now limited to the
canonical local RPC/ASP projection. Native/attached probes retain one configured
total deadline covering their existing health handshake and all later reads,
with an explicit named test. The specification forbids blocking graph reacquisition
inside the writer helper. No transport repair or new endpoint was introduced.

The revision also restores the exact legacy pending object, separates scheduler-
owned deadlines from manual attempt outcomes, and requires unavailable/no_store
through the preexisting bootstrap fallback. Atomic migration, durable progress,
honest unknown ages, ASP routing, native freshness/tickets and embedded input
identity versus final artifact SHA remain intact. The owner handoff narrows the
baseline recheck without absorbing unrelated dirty memory-provider changes.

Implementation/verifier watch points, not additional scope:

- The generic native `memory()` trace path in src/cartridge/src/lib.rs lazily
  opens an engine. Forwarding memory:status directly to trace/ASP is therefore
  insufficient for the existing no-engine-open acceptance when uninitialized.
  Enforce an observational guard/projection through the declared status/ASP
  files and exercise the actual native ASP path in its named test. If satisfying
  this requires a new source footprint or different contract, request targeted
  review rather than silently broadening the lane.
- Execute the canonical measurement with --release and retain numeric output;
  the same test name matching a broad debug suite does not replace release proof.
  Build/setup and fixture migration remain outside polling samples.
- The module fingerprint is compiled input evidence, not a final binary hash.
  Parent controlled integration still owes actual artifact SHA and A-loaded/
  B-on-disk verification; unit fixture sensitivity does not establish those facts.

Next action: coordinator rechecks source HEAD/claims, performs checked specced
and implementation claim transitions, then implements the reviewed 22-path
contract. Independent behavioral verification remains required before collection.

## Editorial implementation clarification — 2026-09-19

Coordinator `/root` approved this clarification after round 3 without a new substantive round. The preserved carve-out is tool.memory query deposition; attached-owner reads remain read-only. Native ASP status uses the existing observational status probe, while direct RPC trace/ASP projects the same canonical payload. This prevents lazy engine opening on an uninitialized observational call and retains the separately specified deadlines. No public endpoint, footprint or semantic promise changed. Revised spec SHA256: `6ec3922ab746010766fe49988bcf13dd65e9e564df85e7405a30720148bbbfd2`. Previous reviews remain intact.

## Round 4 — 2026-09-19 — bounded benchmark fixture amendment

Independent reviewer: `/root/lifecycle_prerequisite`. Read the full current PRD,
specification and preserved prior reviews; inspected the proposed disposable
ledger fixture, production ledger name and store-core dependency pin. This is
a plan review, not acceptance of the still-changing implementation. No tests
were executed for this review and no implementation source was modified.

- PRD SHA-256: `ae0f70634e8383c07168aef3bfd25b86eb443056be15216710ae86aabb9682bd`.
- Specification SHA-256: `81907d5acc8516a13b7bc30b080304abd3972e33028259781dd4ad56dcdd806a`.

| Dimension | Score / 20 |
| --- | ---: |
| User value and scope | 20 |
| Ownership and reuse | 19 |
| Dependencies and implementable boundaries | 18 |
| Observable acceptance and evidence | 19 |
| Failure, recovery and compatibility | 18 |

Total: **94/100 — PASS**. No unresolved plan blockers. Rounds used: 4;
remaining: 1. All earlier reviews remain preserved.

The additional src/rpc/Cargo.toml footprint is limited to a development
dependency on the existing heed 0.20 version. Creating historical ledger rows
in one fixture transaction is appropriate: it models a populated legacy store
without spending the measurement budget on 100,000 separate durable imports.
Closing that environment before production Store::open retains actual migration
coverage. No public bulk-import API, production fast path, new package version
or competing ledger is authorized. The test must prove migrated totals at both
fixture sizes, not merely measure an empty status response.

Canonical RPC dispatch plus JSON serialization, numeric thresholds, 1,000
samples after 20 warmups, release profile and bounded response size remain
unchanged. Fixture construction and production migration are separately timed
and excluded from polling samples. Foreground build setup remains explicit;
normal checked verification timeouts are not weakened. The earlier local
100-millisecond bound and single total native/attached deadline remain intact.

The clarified native ASP path correctly uses the existing observational status
probe before the lazy engine route. The tool.memory query-deposition exception
and attached-owner observational boundary remain separate preserved contracts.
Independent implementation verification must still exercise actual native ASP
when uninitialized and held-graph probes, rather than infer those properties
from mock forwarding tests.

Verifier watch points: confirm the fixture closes all heed handles before
Store::open; validate the lockfile contains only declared dependency changes;
use the canonical RPC-plus-serialization path for all benchmark warmups as well
as samples; retain numeric release output. The current draft fixture's warmup
uses the direct status helper, so align it with canonical dispatch before final
verification. This is implementation compliance with the existing acceptance,
not a contract expansion. Parent artifact and end-to-end retrieval gates remain
mandatory and are not established by this amendment.

Next action: finish and freeze implementation, then obtain independent source
and executable verification before checked collection.

## Round 5 — 2026-09-19 — serving-engine generation contract

Independent reviewer: `/root/lifecycle_prerequisite`. This separate final round
reviews the generation amendment received after the round 4 verdict had been
published. Round 4 and every prior review remain intact; no review was relabelled.
The coordinator requested use of the one remaining ordinary round.

- PRD SHA-256: `bbc058d8db0a1b5bca5aef1e50d7e3d2612088f0d6b057a8bd9e05b07e5589e7`.
- Specification SHA-256: `344f320f91bd395c975878d892675f403012b792cb7bc3dfab32e51414bdcdd0`.

| Dimension | Score / 20 |
| --- | ---: |
| User value and scope | 20 |
| Ownership and reuse | 19 |
| Dependencies and implementable boundaries | 19 |
| Observable acceptance and evidence | 19 |
| Failure, recovery and compatibility | 18 |

Total: **95/100 — PASS**. No unresolved plan blockers. Rounds used: 5;
remaining: 0. This is specification approval, not source verification.

The final 24-path footprint adds src/rpc/src/server.rs solely to expose the
existing engine's Cycles generation through graph-free readiness_stats. Reusing
that same value in experience.owner provides a concrete comparison across the
two observations without inventing an independent identity clock or host API.
An additive field preserves existing readiness consumers. The corrected
uptime_ms spelling matches the existing readiness response.

Native observations are keyed by both serving PID and engine generation. A
same-PID replacement between readiness and progress must yield owner_changed
unavailable. A successful query carrying no generation cannot refresh or erase
a known experience generation. The explicit wire-level same-PID regression
closes the prior draft test's gap: a changed-PID assertion alone does not prove
the amended behavior. Serving-engine generation remains distinct from the
observing module's embedded build-input digest and from final artifact SHA.

The fixture amendment, canonical release benchmark gates, bounded local reads,
one total attached/native deadline, migration/recovery rules and native ASP
no-open path are retained without relaxation. Verification must also handle
missing generation as unknown evidence rather than claim a verified owner
match, and must not introduce blocking graph access into readiness. These are
applications of the existing unknown/unavailable and graph-free contracts.

Validation: checked the final document hashes, full combined specification
against prior rounds, final PRD footprint and existing readiness source. No
implementation source edits or executable acceptance runs occurred in this
review. Source is still being authored. Independent frozen-source verification
and measured results remain required before checked collection. Implementation
bug fixes within this contract do not consume a new plan review; a subsequent
substantive contract change requires coordinator action because no ordinary
review rounds remain.
