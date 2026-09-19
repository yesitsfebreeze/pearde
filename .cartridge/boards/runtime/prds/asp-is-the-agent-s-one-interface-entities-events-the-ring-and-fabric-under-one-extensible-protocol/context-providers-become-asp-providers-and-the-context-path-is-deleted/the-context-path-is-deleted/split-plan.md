# Revision 2: seven owner-addressed slices

These are proposed addresses, not records already created. The coordinator creates new top-level owner records with the engine's `add` operation after checking for existing equivalents. Do not use `--parent` pointing at runtime for another owner: lifecycle.ts resolves the parent board as the new record's owner. Keep the existing runtime identity as a coordination record with qualified `needs`. Source starts below are bounded discovery footprints, not approval to dispatch without exact reviewed specs.

## Publication and owner setup

First reconcile the live parent Outcome/Decision/Acceptance to exclude deferred landscape retirement. Leave every deferred file unchanged. Preserve review round 1 (66/100), with four rounds remaining for this decomposition and inherited use count on splits.

The LSP board is currently absent. `prd.ctg/src/cli.ts:23` discovers boards by `settings.md`; `records.ts:155-179` resolves settings and member locations; `engine.ts:41` makes `members` read-only. No board-create, settings-write or member-add engine command exists. The coordinator authors `prd.ctg/.cartridge/boards/lsp/settings.md` using the existing fs owner-board shape: `name: lsp`, `language: English`, `memos: memos/note`, `workflows: ../../workflows`, `grammar: ../../grammar.md`, `repo` and `source-repository` both `/Users/feb/dev/cartridge/lsp.ctg`, and `require-repo: true`. It adds exactly `{"lsp":"../lsp"}` to root/settings.md's members list while preserving every existing entry. This is authored board configuration, not a direct state/claim/commit edit. Then inspect `./task prd boards` and `./task prd members --board root`, create the leaf with `./task prd add "remove context lsp provider" --board lsp --priority 100`, and run `./task prd check --board root`. The analogous supported `add` command creates the other owner leaves using their exact title/address below. Needs and footprints are authored metadata by the coordinator; the engine remains the only writer of state/claim/commit. Analyst workers author none of this.

The shared root/settings.md edit and all submodule-pointer integration are serialized coordinator work. Preserve unrelated dirty settings and records. No new board or leaf was created by this analysis.

## Exact delivered dependency references

The following labels expand to these full addresses; publication must store the full qualified reference, not the label.

- DOCUMENTS: `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memo-contributes-documents-to-asp`.
- MEMORY: `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memory-contributes-its-entities-to-asp`.
- HOST: `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-host-s-cartridge-entities-carry-state-and-generation`.
- PROXY: `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-prompt-recall-and-the-proxy-read-asp-search`.
- FILES: `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/fs-contributes-files-ranges-and-search-to-asp`.
- WORLD: `@root/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on`.

Verify current provider/consumer receipts before using their delivered status. In particular, PROXY's scope is proxy-only; it is not proof that the installed prompt hook migrated. Historical memory-provider review scores 78 and 88 belong to that sibling's history and do not replace deletion-scope review or current receipts.

## 1. @runtime/prompt-recall-reads-asp-search

Title: prompt recall reads asp search. Source repo: `/Users/feb/dev/cartridge/cartridge.ctg`. Hard needs: DOCUMENTS, MEMORY, HOST, FILES and WORLD.

Outcome: the shipped UserPromptSubmit hook queries ASP search and renders bounded whole attributed results as untrusted additional context. Template and a newly installed copy behave identically. No memo context call or `.block` result dependency remains.

Acceptance: disposable executable probes show nonempty ASP hits produce the expected hookSpecificOutput envelope, preserve provenance and result boundaries, and cannot escape the untrusted framing. Empty input/results, absent binary/jq, failed/late/malformed ASP response emit no stdout and exit zero; the prompt is untouched. Apply an explicit total deadline and byte/row cap. Test a newly installed hook, not only template text. Setup preserves unrelated user hooks/settings and installation behavior. The root integration slice refreshes/proves the already installed checkout hook before memo deletion is activated there.

Footprint starts: `src/cli/prompt-recall.sh`, `src/cli/setup.rs`, `.cartridge/tests/unit/src/cli/setup.rs`, a new focused hook test `.cartridge/tests/integration/prompt-recall.test.ts`, `README.md`, `.cartridge/help.md`. Confirm the repository's integration registration before finalizing the spec. Scope excludes root generated files.

## 2. @memo/remove-native-context-collector

Title: remove native context collector. Source repo: `/Users/feb/dev/cartridge/memo.ctg`. Hard needs: `@runtime/prompt-recall-reads-asp-search`, DOCUMENTS, MEMORY, HOST, PROXY and WORLD.

Outcome: memo's context operation, injection, recall-only settings, source state machine and evidence crate disappear while record and public document behavior remain.

Acceptance: the old native context request fails explicitly without mutations or provider calls; ordinary tool invocation context and document operations work; memo/document ASP search/expand retain owner/revision checks; obsolete tests/docs/settings/workspace dependency and lockfile references are absent. Run the surviving named tests, not only grep.

Footprint starts: `src/context.rs`, `src/sources/`, `src/lib.rs`, `src/service.rs`, `Cargo.toml`, `Cargo.lock`, `cartridge.json`, `evidence/`, `README.md`, `.cartridge/help.md`, `.cartridge/docs/context.md`, `.cartridge/tests/integration/context.test.ts`, `.cartridge/tests/integration/kernel-context.test.ts`, `.cartridge/tests/unit/src/sources/kernel.rs`, and registrations/configuration tests found by the leaf analyst. Existing manifest/docs/context-test dirt must be reconciled before a lane. Do not remove unrelated invocation `context` or resolver evidence fields.

## 3. @fs/remove-context-file-provider

Title: remove context file provider. Source repo: `/Users/feb/dev/cartridge/fs.ctg`. Hard needs: `@memo/remove-native-context-collector` and FILES.

Outcome: remove context.file nomination, provider-only context_files configuration and old evidence transport while retaining independent fs.context and ASP file/range/read behavior.

Acceptance: event/listener/native export, provider-only settings, wire structs and old fixtures are absent. Named tests prove native reads, ASP file/range expansion/search and text read actions still work with existing owner/revision and stale behavior. Unrelated filesystem change-record Evidence remains.

Footprint starts: `src/source.rs`, `src/evidence.rs`, `src/lib.rs`, `init.lua`, `cartridge.json`, `.cartridge/tests/unit/source.rs`, `README.md`, `.cartridge/help.md`, `.cartridge/docs/context.md`; resolve context_files configuration plumbing and source-test registration exactly during specification. `src/context.rs` is preservation evidence, not an automatic deletion target.

## 4. @lsp/remove-context-lsp-provider

Title: remove context lsp provider. Source repo: `/Users/feb/dev/cartridge/lsp.ctg`. Establish the LSP board as above before adding this record. Hard need: `@memo/remove-native-context-collector`.

Outcome: remove only the obsolete catalog evidence transport; keep tool status, diagnostics, envelopes, cancellation and ASP symbol/reference behavior.

Acceptance: no context.lsp event/listener/export or old source/evidence protocol/test remains. Named tests prove tool status and diagnostics retain result envelopes and ASP symbol/reference behavior survives. The existing root envelope PRD still owns its two outstanding MCP-session proofs.

Footprint starts: `src/source.rs`, `src/evidence.rs`, `src/lib.rs`, `init.lua`, `cartridge.json`, `.cartridge/tests/unit/source.rs`, `README.md`, `.cartridge/help.md`, plus actual registration references.

Before dispatch, coordinator reconciles `@root/tool-lsp-answers-must-carry-the-tool-result-envelope` in place: retain all envelope/MCP/cancel requirements and historical checked evidence, but qualify its historical context-provider preservation clause as true for that earlier change and superseded only by this deletion leaf. Do not tick its remaining MCP boxes or reset its review count. Serialize any shared lib/manifest/docs footprint with a live owner; this reconciliation is not a hard requirement to complete unrelated MCP proofs before deletion and adds no dependency cycle.

## 5. @memory/asp-projection-without-context-contract

Title: asp projection without context contract. Source repo: `/Users/feb/dev/cartridge/memory.ctg`. Hard needs: MEMORY and `@memo/remove-native-context-collector`.

Outcome: move only hydration, privacy, source attribution and stable content-projection revision responsibilities that ASP needs into ASP-owned modules; remove context.memory and its old protocol, without changing heat policy.

Acceptance: exact-ID hydration, missing/deleted/private/unavailable behavior and content revisions retain named tests. Search/expand maintain the current no-usage-increment contract; heat changes do not change content revisions. Legacy event/listener/export, general contribution/read contract and obsolete tests are absent. Do not merely rename the full evidence protocol.

Footprint starts: `src/cartridge/src/source.rs`, `src/cartridge/src/evidence.rs`, `src/cartridge/src/lib.rs`, `src/cartridge/src/asp/search.rs`, `expand.rs`, `node.rs`, `mod.rs` in that same asp directory, new narrowly scoped projection/hydration files if justified, `init.lua`, `cartridge.json`, `.cartridge/tests/unit/src/cartridge/source.rs`, existing ASP tests, `README.md`, `.cartridge/help.md`.

Before dispatch, reconcile `@memory/heat-is-deposited-on-read-back-not-on-delivery` with its owner. Its current context.memory-read acceptance and README/help proof target must be rewritten around surviving explicit by-ID reads. ASP observational search/expand are preservation checks here and are not silently redefined to deposit heat. The heat leaf owns any future deliberate read-use policy and replay/dedup proof; the deletion leaf implements none of it. Preserve the heat leaf's retention-probe prerequisite, source work and review count. Serialize its overlapping README/help edits and record the reviewed caller-contract mapping before dispatch. No hard dependency on finishing the heat feature is introduced.

## 6. @harness/roster-without-context-evidence-contract

Title: roster without context evidence contract. Source repo: `/Users/feb/dev/cartridge/harness.ctg`. Baseline hard need: `@harness/scoped-roster-context-contributor`, already delivered; validate its receipt. It has no dependency on memo deletion and can run independently once its footprint is reconciled.

Outcome: replace the general context evidence collector with bounded roster-specific capture and rendering, preserving the authenticated roster feature and removing the old wire schema/types.

Acceptance: actual sessions+harness composition renders the authorized roster under row/byte/deadline caps; disabled configuration makes no call and no block. Actor mismatch, unavailable/partial sources, malformed responses and deadline expiry produce explicit metadata without credentials or other scopes. Inspection retains source/composition revision meaning, omission/truncation and unavailable state. Prompt-like and closing-frame data remain escaped untrusted observations. Compaction/transcript gates still pass. No cartridge-context/v1 schema or generic Contribution/Prepared protocol is retained under a new name.

Footprint starts: `src/evidence.rs`, `src/lib.rs`, `src/roster.rs`, new roster-specific responsibility modules if needed, `.cartridge/tests/unit/roster_tests.rs`, `.cartridge/tests/integration/roster.test.ts`, `README.md`, `.cartridge/help.md`, `.cartridge/docs/roster.md`; add `src/limits.rs`/`cartridge.json` only if actual retired-protocol names require changes. Preserve current caps rather than inventing settings changes. The old delivered roster PRD is baseline evidence, not a duplicate work item or a new round allowance.

## 7. @root/composition-without-legacy-context-path

Title: composition without legacy context path. Source repo: `/Users/feb/dev/cartridge`. Hard needs: `@runtime/prompt-recall-reads-asp-search`, `@memo/remove-native-context-collector`, `@fs/remove-context-file-provider`, `@lsp/remove-context-lsp-provider`, `@memory/asp-projection-without-context-contract`, and `@harness/roster-without-context-evidence-contract`.

Outcome: the integrated enabled composition has no obsolete discovery transport or wire-contract copies and every retained consumer demonstrably works.

Acceptance: current manifest/listener/need census is empty for context.*; owner source census finds no old schema/state-machine copies, including harness (ordinary fs/sessions change-record Evidence is preserved). Through the actual host, query and expand document, memory, file and cartridge-state entities with known owner/revisions; exercise the installed prompt hook and authenticated roster. Refresh the generated root hook from the reviewed shipped artifact before the integrated memo removal becomes active. Prove optional empty/failure behavior and that proxy still uses ASP. Unit suites alone cannot establish composition.

Exact integration footprint starts: new `.cartridge/tests/integration/context-path-retirement.test.ts`, existing `.cartridge/tests/integration/asp-system.test.ts` only if fixture helpers must be shared, `.cartridge/hooks/prompt-recall`. The task launcher reads `.cartridge/memos/routine/workspace-tasks.md`; its system target runs only asp-system.test.ts. The new spec must invoke `bun test .cartridge/tests/integration/context-path-retirement.test.ts` explicitly in its named test gate, so this slice needs no task-runner or memo registration edit. The new integration fixture must use disposable data and public provider events, not sibling private fixtures. The existing asp-system test is opt-in and exercises durable memory/JEV; it is precedent, not automatically sufficient proof. Do not expand this worker footprint to submodule source trees or root settings; pointer landing and settings registration are separately serialized coordinator actions.

Run affected owner checks/tests/audits, `./task isolation`, and `./task prd check --board root`; prove named behavioral tests and no skipped proof. Record the root/submodule revisions. Deferred landscape records must have unchanged bytes. No retirement or other transition of deferred plans is included.

## Closure and review

The current runtime identity has qualified needs, not actual engine children. `lifecycle.ts:310` requires real children for refine; lines 54/104/180 require a published executable contract and the normal state path for childless collection. Use a reviewed verification-only closure spec on that existing identity, dependent on the root integration receipt, rather than inventing an unsupported container operation. This is no additional implementation outcome and cannot duplicate root testing or bypass acceptance evidence.

Every eventual executable spec uses lane/repo double-pass semantics, repo-relative paths, scratch writes outside its footprint and an isolated CARGO_TARGET_DIR for every cargo command. No executable spec is published by this decomposition. Round 2 review must pass at least 90 with no blockers before creation/dispatch proceeds under coordinator authority. All leaf specs still require their own current review within inherited history.
