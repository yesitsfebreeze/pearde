# Attributed independent integration reviews

# Independent JEV assessment review

Reviewer: /root/asp_graft. Reviewed clean revision ab3ada395312faadd813b1e5be6569416e1eca14 in .worktrees/jev-assess.

Verdict: approved bounded candidate, 9/10, no remaining blockers in the reviewed assessment implementation. Production consumer integration is a separate gate.

Independent evidence: integration suite passed 43 tests and 524 assertions; TypeScript checking passed. Both `python3 /tmp/jev-assess-realhost.py` and `JEV_PROBE_INVALID=1 python3 /tmp/jev-assess-realhost.py` passed against the exact revision. The isolated real host admitted JEV and the new native sessions provider, discovered a different registered running agent, returned coordinate for valid probabilities and fallback for malformed probabilities, persisted decisions in the default directory sandbox, preserved them across helper reload, traversed decision:root through ASP, and accepted the trusted tool envelope. Both modes reported two decision nodes, one other active agent, persistence, reload preservation, and tool transport success.

Resolved finding: the earlier revision accepted probability mass assigned to an unknown action and could return proceed. I reproduced this through the actual host with unknown=.99 and proceed=.01. The final revision requires exactly four workflow keys with finite probabilities in [0,1] summing to one within tolerance; the same real-host probe now returns fallback. Caller exclusion, empty-peer coordination downgrade, search-source partiality, and corrupt-journal unavailability are covered by the reviewed changes and regressions.

Evidence boundaries: the isolated host used a deterministic auth fixture matching the actual auth response shape, not a paid model API. Production API and root consumer activation belong to the coordinator's integration gate. ASP evidence is deliberately bounded and marks partial coverage; unregistered external agents cannot be inferred. The persistent journal probe checked absence of a private request sentinel. No production trust, reload, or JEV source mutations were performed by this review.

Final compact-response review: assess output is capped at 6,000 UTF-8 bytes with whole-identifier omission counts and numeric two-pass metadata. Diagnostic withholding is aggregated, while lost selected/peer evidence marks partial coverage and downgrades actions where needed. Losing all peer identifiers cannot leave coordinate. The journal records the effective consumer action and retains original selected entity facts. Both isolated real-host modes were rerun successfully at this final exact revision; the broad-response and Unicode-identity regressions passed independently.


# Independent automatic consumer review

Reviewer: /root/asp_graft. Score: 93/100. Verdict: approve reviewed source; no remaining consumer blockers. Production real-model integration is the coordinator's separate live gate.

Scope: main harness, proxy, agent producer and root Claude hooks, including coordinator's saturated-budget and passthrough-notice fixes. Candidate lineage: harness667877e, proxy1e33d1d, agente6b2ee1, selectively applied over main migration edits. Reviewed JEV response projection ab3ada395312faadd813b1e5be6569416e1eca14.

The default native context and both proxy request paths supply the actual latest user request to shared harness assessment. A bounded shared cache coalesces concurrent identical user turns, caches failure, and distinguishes new textual turns from tool continuations. Native agent start checkpoints actual bounded work before the driver runs; resumed runs preserve that work. The Claude hook registers separate durable hook-namespaced session identities, writes current work before assessment, and marks the mapped agent complete on Stop/SessionEnd. Shell arguments are passed as argument arrays, not interpolated code. Missing durable identity fails explicitly instead of collapsing agents into a shared identity. The host-owned client_context is configured with the workspace principal, canonical workspace and default profile.

Guidance is marked advisory and untrusted; it does not grant permissions. Timeouts, unavailable services and invalid/oversized responses produce fallback guidance. A filled model-context budget now returns context_over_budget before mutating output, rather than keeping a hidden structured assessment while silently omitting all model guidance. Passthrough proxy enrichment failures append an explicit unavailable assessment notice on recognized valid wire formats. Malformed unsupported request shapes retain the existing passthrough behavior.

Independent validation:
- Harness assessment unit tests: 4 passed, covering concurrent/turn dedup, unavailable/slow/oversized responses, model visibility and saturated budget without mutation.
- Actual host harness integration: 1 passed with explicit CARTRIDGE_BIN, proving native and proxy injection transport, guidance in system context, same-turn dedup and reassessment on new turn.
- Proxy textual-turn identity test: 1 passed, including tool continuation and repeated identical new question.
- Agent actual_work_is_checkpointed_before_the_model_driver_starts: 1 passed.
- Root hook suite: 4 passed / 16 assertions, including distinct durable identity, phase transitions, literal request arguments and honest failure.
- Updated JEV integration suite independently passed 43 tests / 524 assertions; TypeScript checking passed.

Resolved cross-boundary findings: the original 8 KiB consumer cap rejected broad valid JEV output; the updated assess-only 6,000-byte projection preserves compact decision/evidence and numeric pass metadata, with omission counts. Whole identifiers are omitted rather than fabricated by truncation. Evidence loss downgrades proceed to inspect; losing every named peer downgrades coordinate to inspect. The journal records the effective returned action while retaining original selected identities. Direct decide retains its existing diagnostics.

Reviewed file SHA-256 values:
- harness/src/assessment.rs: 57d747be6f15713187b5c591a1040a2bdc8034095a5715fc5f7887abbf32a4d1
- harness/src/lib.rs: d7cc4335876199bb5872f5dab7c722765d535d48e8ea9eea09ecdd957f256209
- proxy/src/service.rs: 423d6f1b2a1869f1fc4e2b6b27ecfea3a11d7f0bab5524a928fbad921fe9835e
- proxy/src/wire.rs: 961461b8e422078d5434414d40bb7b14c271db1533b1b68bb75c36d6fcf29730
- proxy/src/lib.rs: 4eb8d5808c6a4935abe1d014428d32bc9dcba61ba63c4d5a100089058bdb8bc0
- agent/src/lib.rs: 7e36d3610f1acd4ebf40d35c071e80c0b91f8544aa7f16389615273bcc5590e1
- root .cartridge/hooks/request-assessment.ts: afcfc574c12d1a9777e5f3f44eb5b16f319c7cbf2e4ee938be1fb5aed969014d
- root .claude/settings.json: 0c3fa5436da45185e294d83cbef95eb481f3149ff28fab5fce381406cf501e96

Limitations: cache identity is bounded and process-local; daemon reload or eviction can reassess a turn. Stop hooks are event-derived state, not process liveness discovery; clients that never register cannot appear as active agents. The independent consumer transport test uses deterministic JEV and session fixtures; actual production model and activated module combination remain the root live test's responsibility. No production trust/reload or consumer source mutation was performed in this review.


# Independent live voice assessment review

Reviewer: /root/asp_graft. Final reviewed clean revision: 167505476cc73943274e865d391e30dc82269dc7. Score: 93/100. Verdict: approved bounded voice integration, no remaining blockers.

The local transport assesses each committed transcription before calling its brain endpoint. It emits the structured decision into live context and carries that decision through local delegation without repeating assessment. Remote delegation IDs are deduplicated before spawning dispatch, which awaits assessment before handing work to a watcher, pane or native worker. A cancellation check after assessment prevents already-cancelled queued work being dispatched. Assessment uses host-configured cwd; input cannot override it. The optional JEV need is declared, responses are bounded and validated, and timeout/error/invalid responses are explicit advisory fallback.

Independent initial evidence: all 41 unit tests passed, including the final evidence-summary regression. The isolated actual-host Python probe passed direct live and tool.live admission, configured trusted cwd despite untrusted caller cwd, decision preservation and failure fallback. Local HTTP fixture proves model ordering and remote WebSocket fixture proves deduplication, guidance emission and retained task assessment. These fixtures do not verify microphone hardware or a paid provider.

Review finding: initial guidance omitted all structured peer and selected entity identities, while actual JEV guidance is generic. The initial test hid this by putting a peer name directly into its guidance string. The final revision fixes this with a 500-byte whole-identifier summary that includes action, decision ID, peer IDs, selected IDs, source partiality, summary_partial and omission count. It preserves approval boundaries and states fallback and clarify behavior explicitly. Production-shaped local and remote wire regressions verify peer/decision identities reach the actual model-facing requests. Oversized Unicode identifiers are omitted whole and counted. The reviewed owner follow-up also fixes two unrelated preexisting chunks_exact Clippy warnings without changing audio conversion behavior.

The README accurately distinguishes local enforced pre-brain ordering from remote model-driven delegation. Remote GPT voice can speak before delegation; its prompt instructs delegation before substantive answers, but this is not a transport-level gate. This limitation must remain visible in final integration reporting. Voice itself does not fabricate a sessions agent identity; native workers use their existing agent/session integration.

No source edits or production activation were performed by this reviewer.

Final revision verification: `CARTRIDGE_BIN=/Users/feb/dev/cartridge/cartridge.ctg/target/debug/cartridge python3 .cartridge/tests/integration/assessment.py` passed after the owner rebuilt liblive.dylib, with HEAD 167505476cc73943274e865d391e30dc82269dc7 and clean status. The independently rerun 41-test suite used the final source contents. The owner additionally reports strict Clippy, formatting and diff checks passed; those checks were not independently rerun.

## Production workspace follow-up

Reviewed exact main revision 520888674a8d05ae435ef2f072b4d8e48812e312 against 1675054. The production profile's relative cwd `.` previously reached JEV unnormalized and caused fallback. Service::new now canonicalizes the trusted configured path once, rejects resolution and UTF-8 failures before opening storage, and passes that absolute path consistently to assessment and composition. Caller cwd remains ignored. The prior composition-only silent fallback has been removed. Configuration help and both documentation surfaces explain resolution against the host process workspace.

Independent focused regression `cargo test --lib relative_workspace_is_canonical_before_any_consumer_sees_it` passed at 5208886. The updated isolated actual-host probe uses configured cwd `.` and asserts JEV receives the temporary workspace's exact canonical absolute path, while a forged request cwd cannot override it. That probe passed again for direct live, tool.live and unavailable-JEV fallback. No new blocker found; approval remains 93/100.

The coordinator separately reports the activated production combined gate passed 57 assertions in 23 seconds, including real two-pass decisions for native, proxy, voice and hook paths, peer visibility, deduplication and journal persistence. This production result is coordinator evidence, not an independently repeated paid-model test.
