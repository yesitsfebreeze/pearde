# Independent split review: the context path is deleted

Plan: `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-context-path-is-deleted`. Reviewer: `/root/context_split_reviewer`, 2026-09-19. Scope: bounded decomposition and ownership, not approval of executable specs. Presented artifacts: `analyst-1.md`, `prd-body-draft.md`, and `split-draft.md` in this directory. Root HEAD: `0ba925860f88089792bb03dce1cba756b73d9a7e`; planning HEAD: `c1caed6375f20bfe6e1a9871f99965aee066da37`. Dirty inputs are bound below.

## Round 1 — FAIL, 66/100

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 14 | Correctly pursues deletion of the obsolete transport, but requires unauthorized work on deferred records and omits a remaining evidence-contract owner. |
| Ownership and reuse | 12 | Four source owners are recognized; actual owner-board addresses and LSP board establishment are missing. Harness's shared roster collector is omitted. |
| Dependencies and implementable slices | 11 | Memo-first then provider cleanup is workable, but the named completed consumer prerequisite does not migrate the prompt hook. There is a live adjacent memory heat plan and a live LSP envelope plan to reconcile. |
| Observable acceptance and baseline evidence | 15 | Memory hydration and filesystem service preservation are well identified. The manifest census is correct but cannot prove every evidence copy is gone. Consumer delivery is assumed too broadly. |
| Failure, recovery and compatibility | 14 | Durable data and foreign dirt preservation are stated, but deleting memo now silently removes prompt recall, and deleting harness's contract without replacement would break roster rendering. |
| Reviewer total | 66 / 100 | Blocking findings below. |

Inherited rounds: no earlier review for this deletion leaf, its immediate parent, or ASP master was found. Neither canonical work-map nor historical OPEN-WORK-REVIEW contains their identities. This is deletion-scope round 1; used 1, remaining 4. Subsequent children inherit this used count. The memory-provider sibling has two distinct historical rounds, 78 and 88, not merely the 78 reported by the analyst. Those belong to the provider implementation and do not transfer sideways to this deletion plan. Deferred landscape histories remain untouched and do not supply fresh deletion allowances.

## Blocking findings

1. **Do not retire deferred landscape records.** `PROMPT.md` explicitly excludes deferred PRDs. Both named landscape plans are deferred; the parent decision's instruction to close them does not override the current worker rules or the coordinator's explicit brief. Remove retirement from the draft Outcome, Acceptance and integration child. Record their exclusion in this live rollup; do not reopen, close, rename or delete them. Reconcile the live parent's contradictory acceptance in place before publishing a decomposition. No user question is required to follow the exclusion already supplied.

2. **Prompt recall is still an active old consumer.** `cartridge.ctg/src/cli/prompt-recall.sh:20` builds `{op:"context",action:"recall"...}`, line 22 runs memo, and line 25 expects `.block`. The installed `.cartridge/hooks/prompt-recall` has the same implementation. `src/cli/setup.rs:43` embeds that template. The done consumer sibling's spec step 3 explicitly says the hook moves under its own record; its footprint and collection receipt are proxy-only. The current PRD inventory found no separate hook-migration leaf. Add or identify a runtime-owned migration prerequisite, including generated installation and failure behavior, before memo collector deletion. A green proxy receipt is insufficient.

3. **“Every copy” also includes harness.** `harness.ctg/src/evidence.rs` is explicitly a copy of the context-evidence contract, including `cartridge-context/v1`; `src/lib.rs:45` exports it. `src/roster.rs:3,266,356` imports its types, renders `Prepared`, and calls its collector for the authenticated sessions roster. Add a harness-owned slice which replaces this obsolete general protocol with bounded roster-specific collection while preserving scoped credentials, deadline, explicit partial/unavailable status, revision and untrusted rendering. Do not delete the roster feature or merely rename a complete legacy protocol. Its completed `@harness/scoped-roster-context-contributor` is baseline behavior, not a new work duplicate. Ordinary change-record Evidence in fs and sessions is unrelated and survives.

4. **Make owner placement and integration executable at the planning level.** The draft says “children” but does not distinguish same-board children from cross-owner `needs`. New memo/fs/memory/harness leaves belong on those owner boards. No `lsp/settings.md` exists; establish the accountable LSP owner board through supported planning operations before adding a leaf there, and register its membership in the root composition. Do not silently place LSP cleanup under runtime. The final composed proof is root-owned and must name actual integration fixture paths during specification. The existing runtime deletion identity can remain a short coordinator rollup with qualified needs.

5. **Reconcile adjacent live contracts without duplicating them.** `@memory/heat-is-deposited-on-read-back-not-on-delivery` remains open and explicitly accepts `context.memory read`, with README/help overlap. Coordinate its acceptance and proof against surviving ASP/by-ID reads; the deletion slice must not implement new heat policy. `@root/tool-lsp-answers-must-carry-the-tool-result-envelope` remains specced and explicitly says context.lsp is untouched. Preserve its result-envelope work and remaining MCP proofs; record how cleanup intentionally supersedes that preservation clause instead of making contradictory live acceptance. Neither is a reason to pick up deferred work.

## Concrete corrected split for the next substantive revision

Keep the current runtime identity as a short rollup. Its outcome is that obsolete context discovery and all copies of its wire contract are removed after surviving consumers have working replacements. Deferred plans stay outside scope. Proposed addresses below are new records to check/create through the engine, not claims that they already exist.

1. **`@runtime/prompt-recall-reads-asp-search`** owns the shipped hook template and setup tests in cartridge.ctg. It asks ASP search, renders bounded attributed whole results into the hook envelope, and retains silent optional failure and empty-result behavior. Verify both the template and a newly installed hook. The root integration record owns refreshing/proving this checkout's generated hook if needed. It depends on the delivered ASP provider contracts and composition; memo deletion needs this leaf. Preserve the completed proxy migration as a separate delivered prerequisite.
2. **`@memo/remove-native-context-collector`** owns removal of the memo operation, context injection/settings, sources, evidence workspace member, registration and obsolete tests/docs. Expand beyond the present seven paths to include lib.rs, Cargo.toml/lock and test registrations discovered by the analyst. Acceptance proves explicit rejection without mutation, surviving memo/document operations, and no legacy dependency. Needs hook migration and delivered document/memory/host providers plus proxy consumer migration.
3. **`@fs/remove-context-file-provider`** owns event/listener/export/settings/source/evidence cleanup. Preserve independent fs.context and ASP file/range/read behavior. Needs memo deletion and delivered filesystem ASP. Its spec must resolve actual config/test registration paths.
4. **`@lsp/remove-context-lsp-provider`**, after establishing the owner board, owns event/listener/export/source/evidence cleanup. Preserve tool status and ASP symbol/reference operations. Needs memo deletion; reconcile the existing envelope plan as described above, without duplicating its implementation or resetting its review history.
5. **`@memory/asp-projection-without-context-contract`** owns extracting only surviving hydration/privacy/source/revision logic into ASP responsibilities, then removes the old event/export/protocol and obsolete tests. Preserve exact-ID reads, filtering, failure states and revision stability. Needs delivered memory ASP and memo deletion. Coordinate overlapping heat docs/proof before dispatch; do not claim a new heat behavior.
6. **`@harness/roster-without-context-evidence-contract`** owns harness evidence removal and roster-specific replacement, with roster unit/integration proofs. Preserve authenticated scope, disabled no-call behavior, caps, deadlines, partial/unavailable metadata and escaped untrusted rendering. It can run independently of memo once its exact footprint is clear. Read the existing roster delivery as baseline and retain its history.
7. **`@root/composition-without-legacy-context-path`** owns composed integration proof and generated hook reconciliation. Needs the five owner deletions (memo/fs/lsp/memory/harness) and hook migration. Prove the current manifest/listener census, absence of obsolete wire copies across enabled owners, live document/memory/file/host ASP search/expand and functioning prompt recall. Run affected checks/tests/audits and isolation, and planning validation. Do not include deferred record transitions. Root submodule-pointer landing remains coordinator work, not a blanket worker footprint.

The four original owner deletion slices remain useful after these corrections. Their starting paths are not final executable footprints. Every implementation spec still requires a fresh revision-bound review within the inherited allowance. Future Verify blocks must honor the supplied lane/repo double-pass, repository-relative paths, no absolute checkout cd, and isolated cargo targets. No build or executable-spec approval is implied here.

## Validation and limits

Read `./task prompt` first, then PROMPT.md, PROMPT_START.md, workflow and template; all reads finished. `./task task` exited 0 (its manual discovery component was unavailable). ASP was queried before source lookup and returned available providers; source reads supplied the decisive evidence. Targeted manifest/source census, all-PRD live-state scan, canonical inventory inspection and current git identity/status reads completed. A few guessed source-path searches reported absent files; corrected targeted source reads established the cited paths. No build/product gate was run for this decomposition-only review. No processes remain running from this review.

Only this report was written. No source, PRD body/frontmatter, review history, board state or commit was modified. User rating is not required and none is invented. Next action: analyst makes one coherent revision addressing all five blockers, then independent round 2 review. Do not publish or dispatch this split as currently drafted.

## SHA-256 input binding

| Input | SHA-256 |
| --- | --- |
| `PROMPT.md` | `5bbffdd7a4d2f16d0275570440e8d3c09e304a1bfb8576968be57a65263cf733` |
| `PROMPT_START.md` | `921db210253b821129a8dbc2f361bde88898b8864190e11d1b063b5280504b73` |
| `prd.ctg/.cartridge/workflows/review-plan.md` | `1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9` |
| `prd.ctg/.cartridge/templates/review.md` | `d103780f7df7f1c1ceed03480ba168a82c045fdb13ce239be41400f15925b52f` |
| `prd.ctg/.cartridge/boards/root/work-map.json` | `185d98e5dfd62c4daccfcb5c5c56c593088e70a76740c2e7afe3b7676b971b3e` |
| `prd.ctg/.cartridge/boards/root/OPEN-WORK-REVIEW.json` | `df537e321109b44977e1f9732395d4f89bc82c25c572ffaaa4a9922c6f667835` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/prd.md` | `afc6e13c6c36e5d2ce3417d784f8733f8244d7288e0d228ece53f0d6b1cde892` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/prd.md` | `b90ff52e697ae4f58376a7c14289e05c71cf97206fe05e3991ce0f542931f281` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-context-path-is-deleted/prd.md` | `50a89c32cd53087eda836952558005fc1584d00dc8908f394ad9d7d82f56f0f6` |
| `prd.ctg/.cartridge/boards/runtime/.state/loop/the-context-path-is-deleted/prd-body-draft.md` | `39c51fc32c7bdf7d834e3ccdfb3cb2c6515b0d1b40b0cd948a4e64f0da7abab3` |
| `prd.ctg/.cartridge/boards/runtime/.state/loop/the-context-path-is-deleted/split-draft.md` | `7b8809fcdffc425d60106ca63d2b5e90a319f35ee305373f28c05015900d05e3` |
| `prd.ctg/.cartridge/boards/runtime/.state/loop/the-context-path-is-deleted/analyst-1.md` | `2b72b7638a512f145e61ce20e570acf5b00b0cde96def2a9d155d554f91dfcc3` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memory-contributes-its-entities-to-asp/review.md` | `374f4fc0df59fa43b7c8fce00140df4ac151c4992871afd27c01807c9fba0952` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-prompt-recall-and-the-proxy-read-asp-search/specs/spec01.md` | `85dcadc4ad1d191ecaf6f040283e35cf2aba71b302de17b6d69ee57afa64b55f` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-prompt-recall-and-the-proxy-read-asp-search/collection.md` | `8f0c6c5594459ee40de71ae197bf8b38c6b2b8585c56f8468a532cc2e56c1f0e` |
| `cartridge.ctg/src/cli/prompt-recall.sh` | `c8ac828aee7aa8a8cef3c49c6838feccb681da9594c7fb875474204223dfcd02` |
| `cartridge.ctg/src/cli/setup.rs` | `ed23f083daca7fd1d84626e41647c0f34b1a257c1e056fbb551d0abbedff6aaf` |
| `.cartridge/hooks/prompt-recall` | `c8ac828aee7aa8a8cef3c49c6838feccb681da9594c7fb875474204223dfcd02` |
| `harness.ctg/src/evidence.rs` | `8606caf9a4cff4bef137978a6194844d8c5e9a191513a8c673673b1ba84f2079` |
| `harness.ctg/src/roster.rs` | `273e87072ace0a16a1ae0d58a16e6aefa73b00521897b66d0df0ec76c90cc2f6` |
| `memory.ctg/src/cartridge/src/asp/search.rs` | `b58f4cbf3f78df6413316c0e96079fa7703cf54ca8612a514ba95ed8a5152d01` |
| `memory.ctg/src/cartridge/src/asp/expand.rs` | `82921d690c667e2d0afd077d63b0d46512b66cf93b493f9099e66627f195309c` |
| `memory.ctg/src/cartridge/src/asp/node.rs` | `0b01acd86830198725104056d69cf6141bf64f4a2d189bc6dc142eada49a6346` |
| `memo.ctg/Cargo.toml` | `12baed7ec92306eaba380293d78f4792df689d2659195bc2a15c91dd05f17e89` |
| `fs.ctg/src/source.rs` | `a2700efe9952719ed7d2e3a558ccb6e9576a6622017c529dac3e4dd7e10e81fb` |
| `lsp.ctg/src/source.rs` | `45c40386495f74c314f81804c4cd462578019e3b0f4a51cfc4498afa8063a2ef` |
| `prd.ctg/.cartridge/boards/memory/prds/heat-is-deposited-on-read-back-not-on-delivery/prd.md` | `f564fe087c43d63425f3c85717de43b02e822f86b0f754afb51517bf1a86995c` |
| `prd.ctg/.cartridge/boards/root/prds/tool-lsp-answers-must-carry-the-tool-result-envelope/prd.md` | `0434ae8f7ded7d1a6f01a6b8f021fbc46fcf58873ace61e4f76b0aefbe8c2a2a` |
| `prd.ctg/.cartridge/boards/landscape/prds/landscape-composes-system-context/prd.md` | `206c7ba833107ee3f88b7d3fa4852e524050141d90a716453e4518b6ee8aa4f1` |
| `prd.ctg/.cartridge/boards/landscape/prds/one-search-covers-the-record-and-memory/prd.md` | `6e26b148625b83de5d5aa9ac257234ec2fbe9c679160dd28d65d58cb73c18938` |


# Independent decomposition review, round 2

Plan: `@runtime/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-context-path-is-deleted`.
Reviewer: `/root/context_split_reviewer2`, an independent reviewer, 2026-09-19.
Scope: the revision-2 seven-owner decomposition only. This does not approve any executable implementation spec, implementation, or collection.
Root HEAD: `0ba925860f88089792bb03dce1cba756b73d9a7e`. Planning HEAD: `c1caed6375f20bfe6e1a9871f99965aee066da37`.

## Round 2 — PASS, 94/100

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | Preserves full removal of the obsolete transport and contract copies while explicitly excluding deferred retirement. The live parent's contradictory text is a mandatory publication reconciliation, not authority to touch deferred records. |
| Ownership and reuse | 19 | Exactly seven implementation slices have concrete owner-qualified identities, including the omitted hook and harness. LSP board configuration follows existing authored settings and engine discovery. Source discovery footprints still need exact executable-spec boundaries. |
| Dependencies and implementable slices | 19 | Memo deletion needs hook migration and delivered providers/consumer; provider removal follows memo; root composition needs all six slices. Cross-owner needs are distinguished from actual children. The childless runtime identity has a supported verification-only closure path. |
| Observable acceptance and baseline evidence | 18 | The plan requires named owner tests, installed-hook behavior, actual host composition, scoped roster behavior, explicit failure cases and contract census. Exact named gates and fixtures are deliberately deferred to executable specification, so this is not a product proof. |
| Failure, recovery and compatibility | 19 | Preserves silent optional hook failure, authenticated bounded roster, privacy/hydration, owner/revision behavior and unrelated invocation context. Requires foreign-dirt reconciliation and no obsolete fallback. Activation sequencing must be made concrete in the integration spec. |
| Reviewer total | 94 / 100 | No unresolved blocking findings for decomposition. |

## Resolution of the five prior blockers

1. Deferred records are expressly excluded in all revision-2 artifacts. The current live parent still contains retirement language; the split requires its Outcome, Decision and Acceptance to be reconciled before publication and requires deferred bytes to remain unchanged. Both named landscape records currently say `state: deferred`. This resolves the plan defect without performing unauthorized retirement.
2. `@runtime/prompt-recall-reads-asp-search` is an explicit prerequisite of memo deletion. It covers the template, setup and a newly installed hook, bounded attributed untrusted results, total deadlines and optional silent failures. The generated root hook is separately in the root integration footprint. Current template and installed hook still contain the old `op:context` request; the plan correctly treats them as outstanding work and does not mistake the delivered proxy receipt for hook migration.
3. `@harness/roster-without-context-evidence-contract` replaces generic Contribution/Prepared/schema machinery with roster-specific responsibilities while retaining scoped authorization, actor checks, source/composition revisions, caps, deadlines, omission/unavailable metadata and escaped observations. Current roster.rs imports the evidence types and calls their collector; the scoped-roster baseline receipt records integrated proof. This is contract retirement, not removal of the delivered feature.
4. The seven exact new addresses are `@runtime/prompt-recall-reads-asp-search`, `@memo/remove-native-context-collector`, `@fs/remove-context-file-provider`, `@lsp/remove-context-lsp-provider`, `@memory/asp-projection-without-context-contract`, `@harness/roster-without-context-evidence-contract`, and `@root/composition-without-legacy-context-path`. Search of the canonical work map and current PRD bodies found no existing occurrence of these proposed identities. Existing adjacent work is explicitly preserved instead of copied. The delivered dependency labels expand to full real addresses, whose current records are done and have receipts; they must remain qualified when published.

   LSP settings and root membership are authored configuration, not invented mutation commands: cli.ts discovers settings.md, records.ts resolves centralized members, engine.ts exposes members read-only, and the existing fs settings match the proposed shape. lifecycle.ts selects the parent's board when `--parent` is supplied, so cross-owner top-level records plus needs are correct. The runtime identity has no children; ensureSpecs, verify and collect reject treating it as a spec-free container, and refine explicitly requires actual children. The proposed reviewed verification-only closure spec respects those semantics without adding an eighth implementation outcome.
5. The memory heat leaf remains open with the old context.memory read contract; the LSP envelope leaf remains specced with two unchecked MCP proofs and a historical context.lsp preservation clause. The revision requires in-place reconciliation before dispatch, preserves both histories, retains heat's prerequisite and policy ownership, and does not fabricate MCP success. ASP observational search/expand remains a preservation invariant rather than a new heat policy.

## Publication and specification notes

These are execution constraints already expressed in the reviewed plan, not additional decomposition blockers.

- Publish the parent reconciliation and adjacent live-contract mapping before dispatching deletion. Do not leave contradictory live acceptance behind and rely only on a report to explain it.
- After recording this review, the count is two rounds used and three remaining. Children and the verification-only closure inherit both substantive rounds. The revision's references to one used/four remaining describe its pre-review state; they must not become a reset when records are created.
- Root integration depends on completed deletion leaves, but its installed hook must refresh before the deleted memo implementation becomes active in the live composition. The executable integration/landing plan must distinguish landed submodule work from host activation, perform the hook refresh first, and prove that ordering. Merely refreshing after a host reload would violate the reviewed acceptance.
- Final specs must establish exact footprints, named tests and registrations. The root task launcher currently runs only asp-system.test.ts for its system target; the proposed new retirement fixture therefore needs its explicit named bun test gate. Existing opt-in ASP integration is not sufficient evidence by itself.
- The runtime closure spec must validate current root receipt/contract identity and rollup acceptance using the engine's normal lifecycle. It cannot treat receipt existence alone as behavioral proof, modify owner code, or duplicate the root implementation outcome.
- Every eventual Verify block must follow lane/repo execution, repo-relative paths, isolated cargo targets and scratch writes outside the footprint. No executable block was presented or approved in this review.

## Validation and limits

`./task prompt` was the first command and exited 0. Read PROMPT.md, PROMPT_START.md, review-plan.md, review/spec templates, canonical leaf, parent and round-1 review, and all three revision-2 artifacts. Read relevant current settings, PRD engine closure/member/add paths, installed/template hook, harness roster and its receipt, adjacent live contracts, and task registration. Targeted dependency inventory confirmed all six delivered dependency records and the harness baseline are done with receipts; that is planning evidence, not a rerun of their behavioral gates.

`./task task` exited 0; its manual discovery was unavailable and its world component hit the discovery deadline. `./task asp search` exited 2 because asp is not a task recipe; the corrected `cartridge call asp` search exited 0 with available provider responses. An initial shortened report-directory read failed and was corrected to the centralized board path. These unsuccessful lookups are not verification evidence. No build, mutation, board transition, or product gate was run. All started processes completed before this report.

Only this report was written. No source, PRD body/frontmatter, state, canonical review history or commit changed. User rating is not required and none is supplied. Disposition: publish the reviewed split with its mandatory reconciliation steps, then independently review each executable specification. Result: PASS. Unresolved blocking findings: none. Rounds used / remaining: 2 / 3.

## SHA-256 input binding

| Input | SHA-256 |
| --- | --- |
| `PROMPT.md` | `5bbffdd7a4d2f16d0275570440e8d3c09e304a1bfb8576968be57a65263cf733` |
| `PROMPT_START.md` | `921db210253b821129a8dbc2f361bde88898b8864190e11d1b063b5280504b73` |
| `prd.ctg/.cartridge/workflows/review-plan.md` | `1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9` |
| `prd.ctg/.cartridge/templates/review.md` | `d103780f7df7f1c1ceed03480ba168a82c045fdb13ce239be41400f15925b52f` |
| `prd.ctg/.cartridge/templates/spec.md` | `0350746f33dde5398bf620c7982e5fe3c8163ff2e0c4879436631393704020ad` |
| `prd.ctg/.cartridge/boards/root/work-map.json` | `185d98e5dfd62c4daccfcb5c5c56c593088e70a76740c2e7afe3b7676b971b3e` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/prd.md` | `b90ff52e697ae4f58376a7c14289e05c71cf97206fe05e3991ce0f542931f281` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-context-path-is-deleted/prd.md` | `50a89c32cd53087eda836952558005fc1584d00dc8908f394ad9d7d82f56f0f6` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-context-path-is-deleted/review.md` | `8b6a328d012d5b9d358fe018a64c9acea3abdd24ab555f306aa192b597c66819` |
| `prd.ctg/.cartridge/boards/runtime/.state/loop/the-context-path-is-deleted/analyst-2.md` | `5c3897bf6fb044742150058f3ab80f29be3413832677579af558bbc810c03317` |
| `prd.ctg/.cartridge/boards/runtime/.state/loop/the-context-path-is-deleted/split-draft-2.md` | `394235e55b7a9828b7a3c07605178b946511c7756ad13601b4bdd838e93e1597` |
| `prd.ctg/.cartridge/boards/runtime/.state/loop/the-context-path-is-deleted/prd-body-draft-2.md` | `65153d4b5c53bcd969b282c7c45109aa71c7d43b4a0be0e3f4f9ddf770256f4f` |
| `prd.ctg/src/lifecycle.ts` | `e5421d97ebdbe4408d79048dc9eaecb26b5e43c82b5a3c044f43668c54beb772` |
| `prd.ctg/src/records.ts` | `e17e8615d3f9b99012a78cc3d500b03820312fd2c4ea1f27923225331a598926` |
| `prd.ctg/src/engine.ts` | `e070b9d40bbbdbb0bb64957c13bf4750c3807e20c72796fc163ee8955f1dc100` |
| `prd.ctg/src/cli.ts` | `e93df71af4aa3c3e4f62c0be16d66cb1b92e91136e3c0c137e44b65ddb076edb` |
| `prd.ctg/.cartridge/boards/fs/settings.md` | `f9d75bbf21c3c225c9ba0c73381f6dded11382b200eff1a0ed55765f97384abc` |
| `prd.ctg/.cartridge/boards/root/settings.md` | `07d2ff324eb67d8f6ee0ccbd0c5b98c755410e9ff765bd705b5b8c19db3dc1f7` |
| `cartridge.ctg/src/cli/prompt-recall.sh` | `c8ac828aee7aa8a8cef3c49c6838feccb681da9594c7fb875474204223dfcd02` |
| `.cartridge/hooks/prompt-recall` | `c8ac828aee7aa8a8cef3c49c6838feccb681da9594c7fb875474204223dfcd02` |
| `harness.ctg/src/roster.rs` | `273e87072ace0a16a1ae0d58a16e6aefa73b00521897b66d0df0ec76c90cc2f6` |
| `harness.ctg/src/evidence.rs` | `8606caf9a4cff4bef137978a6194844d8c5e9a191513a8c673673b1ba84f2079` |
| `.cartridge/memos/routine/workspace-tasks.md` | `958b13ef019718c103bbbee695aa3d89dda23e283e51f552e8e5cee5ecf326a7` |
| `prd.ctg/.cartridge/boards/memory/prds/heat-is-deposited-on-read-back-not-on-delivery/prd.md` | `f564fe087c43d63425f3c85717de43b02e822f86b0f754afb51517bf1a86995c` |
| `prd.ctg/.cartridge/boards/root/prds/tool-lsp-answers-must-carry-the-tool-result-envelope/prd.md` | `0434ae8f7ded7d1a6f01a6b8f021fbc46fcf58873ace61e4f76b0aefbe8c2a2a` |
| `prd.ctg/.cartridge/boards/harness/prds/scoped-roster-context-contributor/collection.md` | `db7286d1a72efab667eb6290d364bf0fabe4895605d4403aa8449b60e22ad753` |
| `prd.ctg/.cartridge/boards/landscape/prds/landscape-composes-system-context/prd.md` | `206c7ba833107ee3f88b7d3fa4852e524050141d90a716453e4518b6ee8aa4f1` |
| `prd.ctg/.cartridge/boards/landscape/prds/one-search-covers-the-record-and-memory/prd.md` | `6e26b148625b83de5d5aa9ac257234ec2fbe9c679160dd28d65d58cb73c18938` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memo-contributes-documents-to-asp/prd.md` | `0aa0c236a3bb257363091bd028374130dfaa85e349ec6193595dfb580eb58144` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memo-contributes-documents-to-asp/collection.md` | `1b45df6535adbb00ae9becbb1ee4288e60728ffa561cc3fadfc6b418b2537981` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memory-contributes-its-entities-to-asp/prd.md` | `47137ebadef61c3428a4ecb798f87eaa6aa477db00cbd5333514443e692ea5b9` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/memory-contributes-its-entities-to-asp/collection.md` | `4c1b93f048008a119622bf2e7de16bd6ebe33ff501590c0d639fff771f08514c` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-host-s-cartridge-entities-carry-state-and-generation/prd.md` | `eba43cfa44bd70530b41c63974c41cf86a0b23f4dd712dc6beec22f3ddcd4bfe` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-host-s-cartridge-entities-carry-state-and-generation/collection.md` | `296a2f5f3b6202fc474f4aeb516829e27debc3b67d01d3e366cf20267bd4bd90` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-prompt-recall-and-the-proxy-read-asp-search/prd.md` | `09b24e173870886db004d885dec7a363851922f8d11e78e02a6d2d6b4a224622` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/context-providers-become-asp-providers-and-the-context-path-is-deleted/the-prompt-recall-and-the-proxy-read-asp-search/collection.md` | `8f0c6c5594459ee40de71ae197bf8b38c6b2b8585c56f8468a532cc2e56c1f0e` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/fs-contributes-files-ranges-and-search-to-asp/prd.md` | `d519efdf24908f778ba3cd3ba134e6529620c7d7116d8af9c290b3b2f19bafad` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/fs-contributes-files-ranges-and-search-to-asp/collection.md` | `36ee96231803ce7654e730d041cfa43bef8949e5475c756bd2052cb493efbe88` |
| `prd.ctg/.cartridge/boards/root/prds/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on/prd.md` | `76bb6801da9f852ea7dcebe89439f06ef8b5c179ecd48e1266bdb8228aa3e35c` |
| `prd.ctg/.cartridge/boards/root/prds/asp-composes-every-provider-s-contributions-into-one-world-an-agent-can-inspect-and-act-on/collection.md` | `2d6d7ac0d6ff7aca2796c5dcdc0d51e9bfc3d884253cda3a8369f103a5ae1375` |
| `prd.ctg/.cartridge/boards/harness/prds/scoped-roster-context-contributor/prd.md` | `84c1012b689a076f2a382ea8c5bafa2ddbaaf7b748a4d0c2a727af24d9facf2f` |
