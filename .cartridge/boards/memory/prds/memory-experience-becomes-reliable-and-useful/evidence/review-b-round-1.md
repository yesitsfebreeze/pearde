# Independent memory follow-up plan review B — round 1

Reviewer: `/root/memory_plan_review_b`. Scope: status, intake, evaluation, delivery and Scope leaves only. This is an independent plan assessment, not a user rating or implementation certification. No source, PRD, claim, trust or runtime state was changed. Review used the actual PRDs, investigation, workflow, prerequisite frozen-query PRD and targeted production source. Every listed footprint path exists. No new behavioral test was run by this reviewer; executed-probe claims remain attributed to the coordinator's retained evidence.

Dimension order throughout: user value/scope; ownership/reuse; dependencies/slices; observable acceptance/baseline; failure/recovery/compatibility. Each dimension is out of 20.

## status — PASS 92/100

Canonical reference: `@memory/memory-experience-becomes-reliable-and-useful/memory-exposes-total-backlog-and-the-reason-progress-stopped`.
PRD SHA256: `c3cfdc3c047f2b069a43c7154ca576427cafa14a866fa40dfb6be84a862d9bca`.
Scores: 20, 19, 18, 18, 17.

The observable outcome directly addresses misleading zero pending while historical rows remain. `src/rpc/src/experience/mod.rs::experience_status` currently exposes only the store's three cached numbers; `src/store/core/src/experience.rs::experience_pending` includes historical keys. The plan correctly separates serving queries from progressing a writer and avoids payload scans on polling. Transaction/restart and stale-worker fixtures are appropriate. The package/test commands and source locations are real.

No blocker. Implementation specification should define additive compatibility with `memory.status.v1` and current trace-status fields, distinguish unknown from zero during counter initialization, and give the polling benchmark a numeric gate rather than only measuring two dataset sizes. Loaded build identity must identify the loaded native artifact, not just current source HEAD; dirty source is explicitly relevant here. These are bounded specification details, not reasons to duplicate ownership or add another status service.

## intake — PASS 91/100

Canonical reference: `@memory/memory-experience-becomes-reliable-and-useful/healthy-intake-progresses-past-malformed-or-expensive-observations`.
PRD SHA256: `53e1825a5d329862c551d3bd45e7b8936f7aab812f042a57a754c71225a830c3`.
Scores: 19, 19, 19, 18, 16.

The inspected `drain.rs` early `input::decode(...)?`, aggregate `embed_batch` and store live-first scan support the stated failure risks. The writer dependency is justified. The plan retains retry identities and atomic acknowledgement semantics and explicitly separates permanent invalid data from transient model outage. The tests target distinct, reproducible failure modes rather than measuring only the happy path.

No blocker. The implementation specification must include retained/quarantined bytes in a bounded storage policy and define behavior when that capacity fills; moving a poison row out of the inbox cannot silently evade its capacity cap. Publish a concrete fairness bound such as historical service within N successful batches under continuous arrivals. Record whether a tokenizer is available; a byte cap alone must not be described as an exact token bound. A documented conservative cap is an acceptable initial design. The desired invariant is healthy progress with durable failure evidence, not infinite retry of a permanently invalid row.

## evaluation — PASS 92/100

Canonical reference: `@memory/memory-experience-becomes-reliable-and-useful/experience-retrieval-earns-a-reproducible-quality-and-latency-gate`.
PRD SHA256: `595b9d428cc87bc0ab935b34bf1bf1b8ac36436e5c144aec1c38ee4043ba2c52`.
Scores: 19, 19, 18, 19, 17.

Existing REPLAY.md confirms a reusable labelled corpus, frozen vector cache, fresh indices, alternating query order, hot/cold layouts and scored recall/latency. It also explicitly excludes ingestion, embedding and transport today; this PRD correctly proposes those as extensions, not achieved measurements. The frozen-query dependency is real, and the investigation already records its stale `touch:false` versus implemented `read_only` spelling. The 0.90 recall, zero harmful hard-boundary merges, two-point regression ceiling and 10% latency ceiling are measurable proposed gates. Failure of baseline does not authorize retuning labels or reporting a pass.

No blocker. Before implementation, define paired baseline/candidate equivalence and denominator for recall@5, and isolate crystallization ingestion fixtures from the existing replay path that constructs document fixtures directly. A single aggregate p95 cannot attribute embedding, commit and transport; report both end-to-end and component timings. The consumer probe must state what counts as injected evidence and whether it demonstrates decision usefulness or only delivery. Existing frozen-query authority must reconcile its spelling before the new leaf uses it; do not add an independent competing frozen API. New commands are explicitly required after the runner entry exists, so the plan does not pretend an unimplemented test command already works.

## delivery — FAIL 84/100; blocking finding

Canonical reference: `@runtime/rejected-activity-cannot-wedge-the-hosts-delivery-queue`.
PRD SHA256: `1ff4d5d4985081794dda1554e5ff67173143d3beaa8c96dc3d1985f3adb79049`.
Scores: 20, 16, 14, 18, 16.

The host queue is genuinely vulnerable: `src/trace/activity.rs::delivery` accepts `Result<(), String>` and retries every error forever; node installation maps all successful payloads to unit. `src/host/trace.rs` similarly discards successful payloads. Memory currently returns queued/duplicate JSON on acceptance and plain string errors on size/age refusal through `src/rpc/src/experience/{mod,input}.rs`. Thus no structured producer-consumer classification exists to consume.

BLOCKER: this is a wire-contract change requiring a memory-owned producer implementation, but the plan has only a runtime footprint and no prerequisite that owns memory's accepted/retryable/permanent response shape. The adjacent memory intake leaf concerns drain/quarantine scheduling, not append response classification. “Document the wire response and migrate all trace senders” does not assign the missing producer side or establish safe deployment order. Implementing this leaf alone either cannot pass the real endpoint acceptance check or must brittlely parse memory-specific error strings in the generic runtime, violating the intended boundary.

Bounded fix: add a small memory-owned response-contract leaf, or explicitly expand an appropriate memory-owned leaf with that single outcome and link it as a hard prerequisite. Specify version/capability negotiation or an additive response shape and deployment sequence. Old/unknown responses must remain retryable or explicitly unsupported; they must never be silently acknowledged or permanently discarded. The runtime leaf then consumes that contract, preserving loss counters and cancellation without importing memory semantics. Name the integration target or state concretely where a new declared test will be added; `cartridge.ctg` currently declares the `launch` integration target, not a named disposable-memory contract target. Add permanent refusal, temporary refusal, duplicate acceptance and old-endpoint cases.

Nonblocking: keep terminal rejection counters durable enough for the stated visibility contract, or label their process-local retention. Current `dropped_before` swap can be lost with a permanently rejected carrier; aggregate loss evidence must survive that path.

## scope — PASS 91/100

Canonical reference: `@root/scope-distinguishes-memory-use-from-stalled-processing`.
PRD SHA256: `7d039624845aad29c4f73c1ae53a2f4f97f21b2bc432897c79d0a059b5804844`.
Scores: 20, 19, 18, 18, 16.

Actual Sources polls memory:recent observationally and Activity substitutes `memory.usage` counters for observed calls without fabricating timestamps. The new plan accurately targets absent writer health and ambiguous signal labels while preserving that distinction. Dependencies on published status and signal contracts are appropriate. The footprint stays within Scope despite using the root board. Collector/State and isolated terminal proof are materially better than Activity-only tests.

No blocker. Quote the unittest pattern in the proof command: `python3 -m unittest discover -s scope.ctg/src -p 'test_*.py'`; unquoted `test_*.py` fails in the repository's zsh when no root match exists. Add the relevant State/collector test files to the concrete implementation footprint as needed. Explicitly expire or mark old graph attributes on generation change/unavailability: current Activity.graph ignores invalid payloads and retains nodes, so displaying the last value without freshness can look healthy after a source fails. Reopening the pane should use an isolated PTY or inspect the user's active pane first; do not disrupt it merely to prove a revision.

## Review conclusion

Four leaves pass this independent planning gate with bounded specification recommendations. Delivery fails until its missing memory-owned response contract and compatibility sequence have accountable ownership. A substantive revision requires the next review round and a fresh PRD digest. No review score here certifies live runtime health or completed implementation.
