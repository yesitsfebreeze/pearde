# Memory engine investigation — 2026-09-19

The engine already has useful structural guarantees: separate occurrence and access counts, explicit outcome compatibility, reason-vector matching, atomic intake/graph/receipt commits, restart deduplication and observational ASP reads. The immediate problem is dependable progress and evidence fidelity. More semantic sophistication is not the first priority.

This assessment separates executed reproductions, live observations, source findings and proposed gates. It is a planning result, not a claim that the defects are fixed or that a model-quality benchmark passed.

## Access and test run

The required preflight initially failed: `jev` was unavailable because its manifest changed since trust. ASP search worked. After reviewing the JEV and Harness manifest changes, refreshing trust and restarting those services, JEV recorded decision `368c40b6-6494-4e21-b656-01bd43e9ad89`. Its action was inspect, with partial coverage and a caution verdict. ASP then located and expanded the real crystallization function and memory evidence. The assessment is retained in [evidence](evidence/jev-preflight.json).

The composition remained unstable during concurrent work: memo, memory, Harness, proxy and later PRD were intermittently unavailable or reported missing declarations. One descriptor reconciliation restored all 21 services at a checkpoint. Later PRD creation used the functioning native PRD CLI, not a fabricated successful runtime call. The user was notified before investigation and again when access changed. No permissions were bypassed and no private live observations were inserted.

`just prompt` no longer exists here; `./task prompt` supplied the composed instructions. Discovery, existing PRD inventories, the canonical work map, ASP search and source reads informed this review. Source digests in [source-digests.json](evidence/source-digests.json) identify dirty source precisely; memory HEAD was `55863b356c7c75032b6a525dbe8addc5b29b924f` and host HEAD was `8da102215640bedf9b11d4f3325abec34bf639a2`.

## Findings

| Concern | Evidence and conclusion | Planning response |
| --- | --- | --- |
| Durable progress | Live cycle 22 failed with `activity graph commit refused stale snapshot; reload required, inputs retained`, after 21 successful cycles processing 1,344 records in that generation. The existing stale-write test confirms rollback. The precise writer that advanced the live epoch is not yet established. | Reproduce writer interleavings and coordinate commit ownership. Never remove the stale guard or reload over dirty RAM blindly. |
| Reason versus evidence | An executed normalization probe shows a response becomes the reason when no explicit reason exists. The graph labels it Provenance; reason clustering averages several kinds. This is evidence of a response, not proof of its cause. | Add evidence role, attribution and uncertainty to the existing reasons, and define which roles can organize reason-space groups. |
| Outcome and context boundaries | Identical vectors with explicit opposite outcomes stay separate, a passing control. However `response.error:true` remains answered; outer context and correlation are not retained in Observation; expired active entities still match exactly. | Normalize supported outcome envelopes, retain semantic scope and occurrence correlation, and apply validity checks before exact and semantic matching. |
| Semantic merge quality | Six distinct synthetic contexts with identical candidate vectors merge. Only one provenance reason remains. This demonstrates missing hard scope checks; it does not estimate how often a real embedding model makes that mistake. | Test structural exclusions independently from a held-out embedding evaluation. Preserve same-scope semantic merging. |
| Frequency and use | Separate counts already exist, so my earlier general concern was too broad. The concrete probe shows recurrence updates heat_updated_at and suppresses an access increment even when the last access was 120 seconds ago. Access count itself is throttled reinforcement, not every retrieval. | Separate clocks and label signals accurately. Reuse the existing read-back attribution work rather than duplicating it. |
| Fidelity and replay | A full first representative and at most three 512-character examples survive a merge; other input rows are deleted on commit. Alternative provenance wording is not retained as another provenance reason by this path. | State representative/sample/unavailable fidelity explicitly. Do not promise exact per-occurrence output or introduce a parallel ledger. |
| Backlog and health | The executed historical-row probe has one pending item while pending statistics report zero. Cycles are bounded, process-local diagnostics. Recent successful retrieval can coexist with failed crystallization. | Expose live and historical backlog, oldest age, last progress, error, generation and loaded build identity through ASP. |
| Batch progress and cost | Source: one decode error aborts the batch; missing embeddings go through one batch call; live inbox is always scanned before history. Count bounds alone do not prove token bounds or historical fairness. | Add invalid-row isolation, byte/token-aware work bounds and measurable fairness with deterministic failure fixtures. These failure rates were not measured live. |
| Producer delivery | Source: the host retries any delivery error indefinitely before the next record. Memory has permanent size and age refusals. A bounded 1,024-entry queue can then overflow; dropped_before is not carried into the current normalized observation. | Give generic delivery explicit accepted/retryable/rejected states and observable loss accounting. Leave semantic policy in memory. |
| Scope and actual usefulness | Scope now exposes resident recent entries, but mixes stored heat origins and does not explain total backlog or stalled processing. The repository already has labelled replay, noise, mature and retention evaluations. None of this pass's tests measures improvement in a real agent decision. | Extend existing evaluation and existing ASP/Scope interfaces. Distinguish nominated, read-back and injected evidence; do not equate a returned candidate with useful application. |

Source starting points are the corresponding leaves' footprints. The critical flow is host activity delivery → RPC normalization → durable intake → embeddings → graph matching and reason-space routing → atomic commit → query/readback → ASP/Scope. A generic transport belongs in the base; evidence semantics, matching, retention, storage and ranking belong in independent memory.

## Executed verification

Eight new disposable Rust probes linked the actual memory crates and included the actual intake normalizer. All eight passed. Most are characterization tests that assert the observed defect; a fix should replace the corresponding assertion with the desired invariant in production regression coverage. They are not green product acceptance tests. The opposite-outcome test is the positive control. Identical synthetic vectors isolate structural checks and do not establish real-model quality.

The harness, pinned dependency lockfile and relocatable runner are in [evidence](evidence/run-probes.py). Run from the composition root: `CARGO_TARGET_DIR="$PWD/memory.ctg/target" python3 prd.ctg/.cartridge/boards/memory/prds/memory-experience-becomes-reliable-and-useful/evidence/run-probes.py`. It creates and removes its own temporary crate and LMDB fixtures. The original run is [structural-probes.log](evidence/structural-probes.log).

From memory.ctg, `cargo test --locked -p graph -p rpc -p store_core experience --lib` passed 14 tests: graph 5, RPC 7 and store core 2. [Output](evidence/existing-tests.log). These cover outcome separation, recurrence, persistence, rollback, receipt deduplication, bounded intake and observational reads; they do not cover all new concerns.

The retained live sample had 21 successful cycles, median duration 3,428 milliseconds and maximum 28,436 milliseconds, followed by a failed 25,200-millisecond cycle. This is a small uncontrolled sample including model work under a concurrently changing host, not a capacity benchmark or a p95 SLO. [Metadata-only cycle snapshot](evidence/live-cycles.json).

## Existing work and ownership

Preserve the original crystallization parent and its five children as the implementation/collection authority for the delivered feature. Their working-tree implementation is evidence, not a completed collection. Do not reclaim the standalone-cleanup child claimed by codex-memory. The new parent addresses demonstrated follow-up gaps, not a second implementation of crystallization.

Reuse `@memory/heat-is-deposited-on-read-back-not-on-delivery` for the credit point and `@memory/a-frozen-query-reads-the-bank-without-touching-it` for evaluation isolation. The latter must reconcile its proposed touch:false spelling with the now-existing read_only implementation before further API work; that discovery is recorded here without silently changing its owner or review history. The ingest-distiller PRD concerns a different external-data boundary and is not replaced.

The new generic delivery leaf belongs to the runtime board. The Scope leaf belongs to the root board because Scope has no registered independent board; its footprint is exclusively Scope. Reuse the existing changed-cartridge trust-request PRD for trust UX. The open root JEV-grounding PRD and ASP provider-migration PRDs are separate ongoing work, not dependencies invented for every memory improvement. A source generation becoming untrusted must remain visible and fail closed.

The older root exchange/calendar PRD and runtime calendar-compacted trace proposal contain superseded language. Their state and claims are preserved. Before either is implemented, reconcile its scope against the canonical memory-crystallization record; do not revive calendar storage or clear their historical review rounds by copying them here.

## Sequence, shared files and release gate

Start writer coordination, progress visibility and generic delivery reliability. Evidence classification and the frozen evaluation prerequisite can be investigated independently. Context-safe matching follows the evidence contract. Intake scheduling follows writer coordination. Separate use signals follow the existing read-back attribution decision. Scope consumes the published progress and signal contracts. Fidelity labelling is independent of exact archive policy.

Graph matching and evidence work share metadata/observe/input files; writer, status and intake work share store/RPC files. Their specifications may proceed independently, but integrate one change at a time and rerun the affected experience suite after each. Do not use artificial needs edges merely to serialize edits; coordinate the common footprint. Signal work must land after the existing read-back scoring change.

The proposed quality gate is zero harmful merges on held-out hard-boundary fixtures, at least 0.90 relevant-evidence recall@5, no more than two percentage points of recall regression against baseline, and no more than 10% p95 latency regression under the same warmed workload. These are proposed acceptance targets, not measured results. Pin corpus labels before tuning; if baseline misses the gate, report it and keep default changes blocked rather than changing labels. Absolute end-to-end timings, sample counts and hardware must accompany relative numbers.

The parent is a roll-up. All implementation leaves remain open and unclaimed. Current plans require independent, digest-bound review; a structural board check alone is not approval or product completion. No memory-engine production code was changed in this investigation.

## Final planning checkpoint

Eleven implementation leaves and one roll-up now have independent plan reviews scoring 91–95 with no remaining blocking findings. The failed first-round reviews are preserved. The memory-owned delivery-contract leaf inherits the runtime plan's first used round rather than resetting it. [Reviewed input digests](evidence/reviewed-inputs.json) bind final plans and existing prerequisites. No implementation acceptance checkbox was checked.

The final native PRD check validated 753 records with no problems or warnings. The portable saved harness reran all eight probes successfully; the earlier 14 existing tests also passed. PRD/memory hard audits and isolation across 21 cartridges passed, with ordinary dirty-tree/soft audit findings retained in the logs.

A follow-up live probe returned three available context candidates in 676 milliseconds and eight recent-memory ASP nodes in 18 milliseconds. This proves live serving at that checkpoint, not relevance quality or reliable continuous crystallization. The second JEV assessment timed out and explicitly returned fallback; it is retained in evidence/jev-followup.json and is not treated as independent approval.

The planning snapshot reports existing codex-memory and runtime claims overlapping the first leaves. Preserve those claims; coordinate handoff before implementation. The signal and evaluation leaves also wait for their canonical read-back/frozen prerequisites. The parent and leaf PRDs remain open. The investigation changed planning records and reproducible diagnostic artifacts, not production memory-engine source.
