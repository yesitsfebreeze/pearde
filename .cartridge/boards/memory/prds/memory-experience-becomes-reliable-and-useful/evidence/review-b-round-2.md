# Independent memory follow-up plan review B — round 2

Reviewer: `/root/memory_plan_review_b`. Bounded re-review of the revised delivery and Scope plans and the newly split memory contract prerequisite. The contract leaf inherits the delivery plan's used first round; this is round 2, not a reset. No source, PRD, claims or runtime state was changed. Source findings from round 1 remain applicable. These scores assess plans, not implemented behavior.

Dimension order: user value/scope; ownership/reuse; dependencies/implementable slices; acceptance/baseline evidence; failure/recovery/compatibility. Each dimension is out of 20.

## delivery — PASS 93/100

Canonical reference: `@runtime/rejected-activity-cannot-wedge-the-hosts-delivery-queue`.
PRD SHA256: `9e621118eec66361b6d602ef0b764247daf91ac350fc29a53a13e639fb51f545`.
Dimensions: 20, 19, 19, 18, 17.

The round-1 blocker is resolved. The runtime leaf now has a hard prerequisite naming the memory-owned producer contract. It consumes negotiated structured responses without parsing memory errors, deploys producer support first, and treats old/unknown responses as unsupported or retryable rather than acknowledging them. The actual declared `launch` integration target is now named and the new fixture is explicitly required, avoiding a fictional existing test. The contract producer's independent tests and the host's real-endpoint fixture form an appropriate two-sided proof.

No blocking findings. Small implementation-footprint follow-up: include `.cartridge/tests/integration/launch.rs` or its declared child fixture path when adding the explicitly planned test. Preserve dropped accounting when the record carrying `dropped_before` is rejected; the existing acceptance requirement to expose dropped counts includes this case. Keep the fixture test name and filter aligned so a zero-test run cannot be reported as the integration proof.

## contract — PASS 94/100

Canonical reference: `@memory/memory-experience-becomes-reliable-and-useful/memory-classifies-activity-acceptance-and-refusal`.
PRD SHA256: `4a6bb0800ad002c8e19c79ee341692de285491630a236fd8b3eb7b28c771c6c0`.
Dimensions: 20, 20, 19, 18, 17.

This leaf supplies the missing accountable producer ownership while keeping semantic classification in memory. Its footprint includes the append RPC, normalization, store errors, native entry point and declared manifest schema. Accepted and duplicate dispositions are distinguished from temporary capacity/storage refusal and permanent size/age rejection. The plan explicitly retains stable retry behavior, requires durable acceptance, includes storage fault/restart coverage and stages opt-in support before caller migration. It avoids mixing this outcome with graph matching or drain scheduling. Inheriting the prior used round correctly preserves review history.

No blocking findings. The implementation specification should choose the exact version negotiation field and bounded reason-code enum, identify callers with the required inventory, and document unknown-version/error behavior at the public native entry point as well as the RPC helper. Prove that an error after durable enqueue but before response can be retried as duplicate acceptance; that is the consequential fault boundary for this contract. These are details of the already specified contract tests, not additional product scope.

## scope — PASS 94/100

Canonical reference: `@root/scope-distinguishes-memory-use-from-stalled-processing`.
PRD SHA256: `a5c3f2dbc99eb5756ca843ff066f9c8c2262cdbf8a81b86ae01ab3270bbeff48`.
Dimensions: 20, 19, 19, 19, 17.

The revised acceptance now explicitly marks retained values stale on source failure or generation change until refreshed. State and collector fixtures have an accountable footprint, the unittest pattern is shell-safe, and the isolated PTY proof is retained. Dependencies continue to require published status and signal semantics before UI implementation. This closes the main risk of displaying stale graph attributes as current health while preserving the existing observational timeline.

No blocking findings. Use the isolated PTY to prove the loaded Python revision; if the final pane-reopen wording is implemented against a user pane, inspect that pane first and preserve its running program under existing repository instructions. Keep row selection stable when health updates arrive; the plan already requests this.

## Result

All three revised plans pass round 2 with no unresolved blockers. Scores are bound to the hashes above. The previous delivery FAIL remains part of history. No live-health or implementation-completion claim follows from these planning approvals.
