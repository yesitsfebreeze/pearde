# Independent plan review A — round 1

Reviewer: `/root/memory_plan_review_a`. Date: 2026-09-19. Review-only; no production, PRD or claim edits. Scores concern plan quality, not measured product quality. Threshold is 90/100 with no blocking finding. Dimensions in order are user value/scope, ownership/reuse, dependencies/slices, observable acceptance/baseline, failure/recovery/compatibility.

I read the investigation, inventory, eight-probe execution log, relevant implementation, canonical work map and existing read-back/frozen/retention plans. ASP search succeeded with all eight reported providers available. The parent's JEV assessment is retained evidence; I did not reload or mutate runtime services. No new runtime test was run by this reviewer. Existing characterization tests demonstrate structural failures, not semantic model quality.

| Plan | Dimensions | Total | Result | SHA256 of prd.md |
| --- | --- | --- | --- | --- |
| parent | 19/19/18/19/19 | 94 | PASS as roll-up | a49174461b73de4cb894b9e3d87c46ac30ab5f4bd1008c38f6a482ac6d974a88 |
| writer | 19/19/18/19/19 | 94 | PASS | 85a05276ceaba0cde2499d911fd8bb4df888c106108bc9b6bea1e09c62fd4f44 |
| evidence | 19/19/17/18/18 | 91 | PASS | 6a5d3798a9e13eedb93361aea616ac46d1b903efe7d82772ec5004118b44e9be |
| merge | 19/19/18/18/18 | 92 | PASS | 19fa9b09157a90c823d38f1ac98346805205537e88a1c8be920dc1b7c53972d7 |
| signals | 19/18/15/18/17 | 87 | FAIL | 5fc8dcdfdf10ead00a33589a15dd94272d7d6f2af140b05864131d392863bb28 |
| retention | 19/16/16/18/17 | 86 | FAIL | 93527918db3ee1f26ad4063a66a41ef1ad470774ec7d57cbd7c2b0d26a7314d7 |

## Parent

No blocker in its roll-up role. It preserves existing implementation authority and active claims, correctly puts cross-owner delivery and Scope leaves in their own boards, and gates integration on all acceptance and recovery checks. Links to cross-board leaves resolve correctly relative to its location. Ordering is coherent without creating artificial dependencies just for shared files. Its acceptance is conditional on fixing failed children; this score does not approve those children or authorize implementation before their reviews pass. Material limit: the live stale writer remains unidentified, real retrieval usefulness remains unmeasured, and exact replay is explicitly out of scope.

## Writer

No blocker. `bootstrap::save_graph_guarded` snapshots under a read lock, flushes outside it, and later updates flushed_epoch under a write lock; `Server::commit_experiences` holds the graph write lock across its epoch-checked partial commit. Those are credible interleaving boundaries for the proposed barrier fixture. Registry owns the ordinary save closure, so the listed ownership is appropriate. Existing stale refusal is deliberately preserved. The proposed test commands name real packages and the RPC experience suite. Material limits: a guard-refusal fixture does not by itself establish the live cause, and crash testing must distinguish process exit after durable commit from an injected precommit error. Before implementing, pin barriers at both disk flush and in-memory epoch publication, and verify the coordinator does not hold a graph lock during model work. Existing read-back/crystallization scopes are not duplicated.

## Evidence

No blocker at PRD level. `input::decode_observation` falls back to response/request/envelope as reason, `observe` stores it as Provenance, and `reason_cluster` averages provenance/question/ratification/rephrase vectors. Thus the stated distinction is justified and belongs to memory. RPC and tick-loop command/package names are valid. Conservative migration and retaining original text/vectors are good recovery constraints. Material limits to resolve in specs: choose the persisted classification representation and define contradiction/removal visibility without manufacturing a causal inference subsystem. Evidence references need bounded count/size and stable interpretation across source revisions. If classification adds fields to base::Reason, declare that schema footprint and its compatibility fixture before coding; the current metadata-based implementation route is still possible without doing so.

## Merge

No blocker. Exact matching currently checks only active status and occurrence metadata, while ANN compatibility adds origin/event/outcome and reason cosine. Neither path checks valid_until or invalidated_at, so the new boundary is concrete. Input currently loses outer context and ignores native response.error:true. Evidence classification is a legitimate prerequisite, and legacy ambiguity is preserved rather than fictitiously reconstructed. Material limits: specs must say how unknown scope compares with known or another unknown scope and distinguish identity fields from occurrence correlation. Bound retention of unmatched lifecycle halves and test started→completed, completed→started, duplicate halves, and expiry. Identical-vector fixtures prove hard exclusions, not a real model's merge error rate. The production test filter names are real.

## Signals — blocking findings

1. The plan requires a frozen replay evaluation but does not declare the existing frozen-query PRD as a hard prerequisite. The read-back prerequisite does not transitively supply it: read-back depends on the retention probe, whose state is done, while frozen-query remains open. Either add `@memory/a-frozen-query-reads-the-bank-without-touching-it` to needs, or narrow this leaf to signal separation and explicitly leave ranking unchanged until the existing frozen/evaluation owner completes. Do not create another frozen API; the investigation already records read_only versus proposed touch:false reconciliation.
2. Independent decay is an acceptance requirement, but `src/graph/src/heat.rs`, the existing canonical decay/deposit implementation used by both observe and retrieval_score, is absent from footprint. Add that file and its meaningful heat/migration regression test location, or specify a concrete reuse design that achieves independent decay through the existing functions without scattering duplicate decay policy. The current footprint gives the worker insufficient authority for the straightforward implementation.

Strengths: it correctly acknowledges existing separate counters, captures the shared cooldown defect, preserves the read-back owner's product decision, and refuses to infer historical split heat. Material limit: the prerequisite read-back plan has a known round-1 FAIL at 85 and an explicit tool.memory delivery carve-out. Its revision must land first; this leaf cannot silently override that carve-out. ASP labels should distinguish reinforcement count from total read count.

## Retention — blocking finding

The exact-ID readback acceptance lacks the actual exact-ID response construction path and its proof. `Server::query_by_id` and `query_by_ids` both call `retrieval::detail_with`, implemented in `src/retrieval/piece/src/id_detail.rs`; they do not pass through `rpc::experience::view` or cartridge ASP expand. The listed changes can label ASP while leaving memory get/context readback unlabeled, yet the specified graph/RPC experience and ASP tests can all pass. Add the canonical detail serializer (and public consumer adaptation if required) to footprint and add a regression that calls the public exact-ID response for both a representative and a truncated sample/legacy group. Include the test's package/filter in proof. Reuse the serializer for single and batch paths instead of introducing an alternate read API.

Strengths: the distinction between representative, samples and unavailable originals is accurate, and it explicitly declines a parallel ledger. Keep that scope. Material limits: schema rollback must mean an actual supported reader compatibility fixture rather than a promise old code understands new fidelity fields; old readers need only retain original content safely. Include long Unicode and more-than-three variants as planned. No need to invent an archive policy to make this leaf pass.

## Review coverage limits

No specs exist for these leaves yet; this is review of their outcome plans, not a final specification or implementation approval. Existing source dirty state is material and requires repinning before implementation. The review does not independently establish aggregate live counts, final model quality, exact per-occurrence replay, or user-visible improvement. Source inspection supports the named defects and narrow plan changes. The passed plans still require their concrete proofs and independent implementation verification.

## Coordinator evidence received after scoring

The coordinator reports PRD structural validation passed 752 records and all 11 new identities resolve. Its planner blocks the first memory leaves on the existing codex-memory standalone-cleanup claim. Preserve that claim and coordinate the shared-footprint handoff; passing this review does not make a blocked row claimable. The coordinator also reports a fresh 8/8 portable probe run, 14/14 existing experience tests, context.memory returning three candidates in 676 milliseconds and ASP recent returning eight nodes in 18 milliseconds, retained in evidence/live-probe.json. These are attributed coordinator results, not reviewer-executed tests or measured real-agent usefulness. Its second JEV call timed out and returned explicit fallback; evidence/jev-followup.json is not independent approval. This additional evidence does not change the two failed plans' findings or any recorded score.
