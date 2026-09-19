# an-event-declares-its-type — review

Canonical PRD: [@agent/an-event-declares-its-type](prd.md). Reviewer: `/root` (self-review).
Round limit: 5. Agent threshold: 90/100. No user score was supplied or invented.

## Round 1 — inherited, 2026-09-13

- [an-event-declares-its-type](../../../root/reviews/round-1/an-event-declares-its-type.md): reviewer 86/100; Revise. Define who can register projection rules and their authority ceiling; unknown-type reporting is good but cannot allow an untrusted event to become a system instruction.
  Original SHA-256: `74671a402c58dd2fc62d9f799e8965eaca949a20382fc667130d248d47c8b3bc`.

Historical dimension scores were not recorded. The original user-rating field was pending; the current workflow delegates scoring to the agent. Splitting does not reset the allowance.

## Round 2 — 2026-09-13

Revision: the working-tree PRD and the exact input digests in [review-inputs.json](review-inputs.json).
Change: small owner-local contract; broad parents point to leaves, and canonical aliases share one implementation scope.

| Dimension | /20 | Evidence and deduction |
| --- | ---: | --- |
| Value and scope | 19 | The PRD states its bounded outcome; inherited broader requirements are retained in source history and linked children. |
| Ownership and reuse | 19 | Named cartridge and existing starting files; historical duplicate IDs are mapped to this canonical scope. |
| Dependencies and slices | 19 | Qualified hard dependencies resolve; the complete parent/child graph is acyclic. |
| Acceptance and baseline | 18 | Unchecked behavioral acceptance and a real repository gate; fixture details and measured baselines must be captured before specs. |
| Failure and compatibility | 19 | Negative outcomes and a recovery boundary are retained; implementation must supply the specified failure proof. |

Agent score: **94/100 — PASS**.
Finding: One bounded outcome with explicit positive/negative checks. Fixture-specific specs and baseline measurements remain analysis work; proposed tests are not reported as passed.
Blocking review findings: none; implementation prerequisites remain in the PRD.
Validation: complete work-map coverage, content digests, local links, short-leaf bounds and dependency-cycle checks; see [validation record](../../../root/reviews/validation.md). Product gates were not run.
Rounds used: 2/5; remaining: 3. User feedback: create small defined PRDs and split broad work.
Next: select a dependency-ready leaf, probe its contract and write specs before implementation.

## Round 3 — 2026-09-14 (reconciliation and rebase)

Reconciliation verdict: **REBASE**. "Host-owned declarations" now exist: a manifest declares `events` with JSON Schema, the host refuses undeclared or schema-rejected sends and unknown manifest fields (cartridge.ctg `ee7e295`, `c9ef10b`, `docs/creating-cartridges.txt`). Journal record kinds are still untyped (`agent.ctg/src/lib.rs:198`) and harness still drops every non-`message` kind silently (`harness.ctg/src/main.rs:407`). Under decision `a-cartridge-brings-its-own-surface` the agent must declare its own kinds and harness must read declarations, not carry an agent catalog. Not delivered.

Presented revision: prd.md SHA-256 `bf95fc10a5ebbc5291178ca99bdb878e21dc71ac05f9d03f0c950f4bf5664777` (rebased from `b9b064fd16847da08d1314e6e39ce264946e1684b4a4209449619873f5fc3dda`). Source revisions: agent.ctg `fad6d3b`, cartridge.ctg `c9ef10b`, sessions.ctg `e9725e8`, harness.ctg `336f2d1`, prd.ctg `077e57a2` (dirty tree).

| Dimension | /20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 17 | Declaring kinds and enforcing the frame ceiling at write time is bounded. −3: rescoped to agent-side only; the user-visible part (projection by declaration, skipped types in `/context`) now waits on a harness PRD that does not exist. |
| Ownership and reuse | 17 | Agent declares its own kinds in its manifest; reuses host schema validation and the existing role check (`agent.ctg/src/model_loop.rs:186-194`). −3: the projector is harness-owned (`harness.ctg/src/main.rs:407`, `working.rs`, `inspection.rs`) and has no leaf. |
| Dependencies and slices | 16 | No hard needs; downstream post/listener leaves depend on it. −4: harness counterpart PRD missing; events-port precondition has no PRD. |
| Observable acceptance and baseline | 18 | Four checks: declaration coverage via `cartridge help agent`, write-time refusal, frame ceiling, v1 compatibility. −2: whether a JSON Schema annotation can carry the frame is unprobed. |
| Failure, recovery and compatibility | 18 | Start refuses naming the kind; no record rewritten; v1 transcripts stay. −2: behaviour of old harness against new declarations during staggered landing unstated. |
| Reviewer total | **86 / 100** | |

Findings and concrete revisions: (1) starting-file links resolved to nonexistent `boards/model_loop.rs`/`boards/run_state.rs`; run state now lives in `agent.ctg/src/lib.rs` and `run_state.rs` is a test module under `.cartridge/tests/unit/` — replaced with real paths and a footprint. (2) Rebased from a new registry onto manifest `events` declarations. (3) Split the harness projection half out of this leaf's acceptance, because the decision forbids a sibling catalog and harness owns projection.
Program finding (non-blocking for this plan, blocks implementation): agent.ctg `fad6d3b` still calls `transport::cartridge::run`, `ctx.call` and `ctx.provide` (`agent.ctg/src/main.rs:14,33,42`) and declares `provide` in `cartridge.json`; cartridge.ctg `ee7e295` removed that API and manifests now refuse unknown fields (`cartridge.ctg/docs/creating-cartridges.txt`). No agent gate builds until the agent is ported to declared events; no PRD owns that port. Coordinator action.
Blocking findings: (a) no `@harness` PRD owns "context projection honours declared frames and lists undeclared kinds as skipped"; coordinator must create it in the harness board (outside this reviewer's authority), then this leaf adds it as a downstream link. (b) Frame carrier feasibility (schema annotation vs other) must be probed; if the host refuses annotations, record a question.
Disposition: revise (cross-owner split pending).
Validation: `ls`/`rg`/`grep` existence checks of every cited path and line, needs resolution under `boards/<owner>/prds/<slug>/prd.md`, root `.cartridge/justfile` recipes (`test`, `check`, `verify`, `smoke`) and the `agent` case in `.cartridge/memos/routine/cartridge-development.md`, `git log` of agent.ctg and cartridge.ctg, decision memo reads. No product gates were run.
Reviewer identity: agent (independent reviewer, plan refresh pass). User rating: not required under delegation; none supplied. User feedback: none supplied for this revision.
Result: **FAIL** (86/100).
Unresolved blocking findings: (a) harness counterpart PRD missing.
Rounds used / remaining: 3 / 2.
Next action: coordinator creates the harness projection leaf; then a round-4 revision links it and records the annotation probe.


# Independent round 4 review: @agent/an-event-declares-its-type

Reviewer: `/root/event_reviewer`. Date: 2026-09-19. This is the independent delegated agent rating, not a user score or an implementation verification.

Result: **PASS, 96/100.** No unresolved blocking findings. Four of five rounds are used after the coordinator records this result; one remains. This review does not reset the three inherited rounds and does not score the downstream harness implementation plan.

## Reviewed revision

Agent HEAD is `2ed4743b075976ebc255905b85688151d6ba8787`; host HEAD and collected prerequisite are `8da102215640bedf9b11d4f3325abec34bf639a2`; PRD repository HEAD is `c1caed6375f20bfe6e1a9871f99965aee066da37`. The reviewed PRD and spec are dirty planning inputs, bound below by content. Existing agent manifest, README and help edits are foreign command-migration work and remain untouched. The coordinator published the twelve-path footprint during this review; I reread it before binding. It now agrees with the spec.

| Dimension | Score / 20 | Evidence and deductions |
| --- | ---: | --- |
| Current user value and scope | 19 | The leaf covers declaration discovery, startup authority, atomic refusal and v1 compatibility. The historical user-visible projection and skipped-kind work now has an actual harness-owned dependent leaf with inherited rounds. One point remains for the staged outcome: shipping this leaf alone intentionally retains current message-only projection. |
| Ownership and reuse | 20 | The manifest owns namespaced journal declarations; host readback is caller-scoped; a mechanical prefix preserves persisted short kinds without a sibling catalog. The native accessor and focused journal validator stay in agent. All twelve implementation and documentation paths are now declared. |
| Dependencies and implementable slices | 19 | The host prerequisite is done and its current code supplies both the closed frame enum and declaration readback. One coherent implementation installs validators before recovery and then enforces them at the checkpoint boundary. One point reflects coordination risk from foreign edits in three shared manifest/documentation paths; the spec explicitly requires preservation and ownership reconciliation. |
| Observable acceptance and baseline evidence | 19 | Named executable tests cover all seven real writer kinds, first/middle/last invalid batch positions, checkpoint call counts and state snapshots, authority refusal, fixed v1 bytes and mutable real-host declarations. The baseline logs show 26 unit tests, 13 integration tests and check/isolation success. One point remains because the host integration fixture uses fake session/buffer services; composition gates and diff reading remain necessary to connect that evidence to the production persistence boundary. Missing new implementation tests are expected and are not treated as a blocker. |
| Failure, recovery and compatibility | 19 | Startup cannot fall back to an embedded manifest; invalid batches cannot call checkpoint; old reads are not schema-revalidated; recovery preserves the original byte prefix, closes pending calls once and does not replay tools. A subsequent valid batch must work. One point reflects the constrained evidence from a fixed historical fixture rather than a broad historical corpus; the plan also preserves extension fields and current role checks. |
| Total | **96 / 100** | **PASS.** |

## Findings and implementation requirements

1. **Resolved historical blocker: frame carrier and host authority.** `Event.frame` is an optional closed Message/Data/None enum, and malformed event parsing names the event. The socket route accepts declarations only from a cartridge caller and supplies that caller's `plan.events`. The existing host test `a_cartridge_reads_its_own_declared_events_and_no_one_elses` exercises separate callers and ASP frame exposure. The agent spec adds the stricter journal-specific message-versus-data/none rule and rejects missing frames. Production reads the host on the entered base thread before `recover` and before the Lua listener is installed. A changed disposable manifest must override the unchanged compiled module's embedded document in integration tests. This is executable using the existing fixture profile, which writes the manifest separately from the module binary.
2. **Resolved historical blocker: downstream ownership.** The actual harness record exists, depends on this exact agent ID, covers declaration-driven data/none projection and skipped historical kinds, and explicitly inherits three used rounds. The agent PRD's current boundary links it. This is sufficient to clear the missing-owner blocker; it is not evidence the harness feature has shipped or passed its own review.
3. **Corrected write boundary.** `record()` returns only v/kind/run; writers add payloads afterward, and model_loop constructs one tool-finished envelope inline. `Run::save` is the common checkpoint path for start, ordinary model/tool records and recovery. Validation before its checkpoint call is the correct location. Tests must inspect the entire rejected batch, zero checkpoint calls, transcript bytes, durable/local revisions, sequence and live snapshot; preserve the stated first/middle/last invalid-position matrix and successful follow-up batch. Do not substitute envelope-only checks or event publication as validation.
4. **Recovery and failure proof must remain literal.** The old v1 fixture must include an unknown kind and an unresolved tool call. Recovery must preserve the exact old prefix, validate only appended records, avoid tool replay and be idempotent on a second call. Preserve ordinary runtime failure handling: a later valid terminal failure checkpoint is allowed, while a rejected batch itself remains unapplied. A terminal checkpoint failure must still populate checkpoint_error rather than emit a fabricated done event.
5. **Expanded footprint accepted.** The manifest and dependency/lockfile, base accessor, startup module, focused journal validator, shared checkpoint state, model-loop compatibility, unit/integration tests and both documentation files are necessary for the one outcome. The coordinator corrected the PRD's old four-path footprint to the spec's twelve paths before this binding. Preserve the foreign command-migration edits when implementing and collecting; do not claim them as feature changes.
6. **Nonblocking editorial cleanup.** The spec still describes itself as a draft requiring a footprint update and says that the downstream counterpart must be linked. Both conditions are now satisfied by the current PRD. The historical PRD sections still contain the former record()-guard instruction and frame questions, but its explicitly current boundary supersedes them. Coordinator may make strictly editorial status/link corrections with a recorded semantic-no-change diff, per the review workflow. Any substantive contract change consumes the remaining review round.

## Verify-block assessment

The `test` fences pin the new behavior test names and existing recovery/model-loop/role-context checks using the documented collector format. They run relative to the lane or repository root and avoid sibling-relative checkout assumptions through CARTRIDGE_BIN. Each cargo command receives an isolated CARGO_TARGET_DIR; the nested integration module build inherits it. The lint shell block exports it before fmt and clippy. CARTRIDGE_YOLO is removed from behavior gates. Composition-root test, check, audit and isolation are explicitly additional coordinator gates, not mislabeled lane commands. A host executable implementing 8da1022 is a stated prerequisite and must be retained in the worker environment.

The new tests are planned deliverables and have not been run or claimed green. Diff reading is the backstop for named-test bodies. No additional adversarial-gate design round was spent, and no cryptographic or unforgeable test guarantee is claimed.

## Validation performed and limits

All commands ran from `/Users/feb/dev/cartridge`. `./task prompt` was the first command and exited zero. `./task task` discovery exited zero. ASP search was requested before targeted code lookup, returned Run::save and module entities, and completed with exit zero; its PRD contributor reported a timeout, so the actual on-disk records were inspected directly. Read-only source, manifest, template, history, dependency and git inspections completed. The baseline logs `/tmp/cartridge-event-analyst-tests.log`, `/tmp/cartridge-event-analyst-loop.log` and `/tmp/cartridge-event-analyst-check.log` were read and support the analyst's reported passing results; I did not rerun those tests or the host suite. No implementation diff exists for this feature yet.

JEV assessment returned fallback with timeout and no validated basis, decision `b9fff666-bf8b-450d-b641-0aec265030f2`; the review therefore uses inspected local evidence. Rust router and type-driven design skills were read. No command started by this reviewer remains running. No source, PRD, spec or review history was edited, and no commit or board transition was made. This report is the only reviewer-owned file written.

Disposition: keep and implement the reviewed spec after the coordinator records round 4. User rating is not required under delegation and none was supplied. Unresolved blocking findings: none. The coordinator owns publication, dispatch and later independent implementation verification.

## Exact input binding

Paths are relative to `/Users/feb/dev/cartridge`. SHA-256 values cover the exact bytes inspected at report creation. The review-history digest binds the pre-append three-round history; appending this review is the expected bookkeeping operation.

| Input | SHA-256 |
| --- | --- |
| `prd.ctg/.cartridge/boards/agent/prds/an-event-declares-its-type/prd.md` | `e54a8be4d14ffa6e5f563e6802103a1a45912573bc0a81aca754fba1665f8e34` |
| `prd.ctg/.cartridge/boards/agent/prds/an-event-declares-its-type/specs/spec01.md` | `dc2aafafec9a04d857b9a7316a613d2e90bfe426252bcfe640013b691bdb2f3d` |
| `prd.ctg/.cartridge/boards/agent/prds/an-event-declares-its-type/review.md` | `52c13b7cb8af24507d5a0db46dcbca202253a6032f60b5d7a06ed2c15100a5a6` |
| `prd.ctg/.cartridge/boards/harness/prds/context-projection-honors-declared-frames-and-names-skipped-journal-kinds/prd.md` | `5d5f4075649a78e680a83449a2c2176148d60cf0b98e4c30dc51a969642764cb` |
| `prd.ctg/.cartridge/boards/harness/prds/context-projection-honors-declared-frames-and-names-skipped-journal-kinds/review.md` | `28ca2e1f51f9e352a16192a0d9a025f800f4ea05289a1c9723434f6e7781d8fe` |
| `prd.ctg/.cartridge/boards/runtime/prds/asp-is-the-agent-s-one-interface-entities-events-the-ring-and-fabric-under-one-extensible-protocol/an-event-declaration-carries-a-host-validated-frame-and-a-cartridge-can-read-its-own-declared-events/prd.md` | `f62873f9b5b6a05dfb6058fbb5db986e217d0c51ee501b0563b176933449c7f1` |
| `prd.ctg/.cartridge/workflows/review-plan.md` | `1e577fe0fe5e4e99eb89e545d83cb8f24510b07585b9accba7a6e8d5be4715e9` |
| `prd.ctg/.cartridge/templates/review.md` | `d103780f7df7f1c1ceed03480ba168a82c045fdb13ce239be41400f15925b52f` |
| `prd.ctg/.cartridge/templates/spec.md` | `0350746f33dde5398bf620c7982e5fe3c8163ff2e0c4879436631393704020ad` |
| `prd.ctg/.cartridge/boards/agent/.state/loop/an-event-declares-its-type/analyst-codex-1.md` | `26d0659f66a8445919da6c08f5fb0263d200002dd733ee1a84b234f5e9ac4312` |
| `agent.ctg/cartridge.json` | `f3492a0c3e0eea7d07bed51896a77acced0468609d05b6bc0a270426e841a441` |
| `agent.ctg/Cargo.toml` | `606a4576e9b8af08a54b14b88d4237ebbf9223d6407d1508a7a3eb8ff9bf500b` |
| `agent.ctg/Cargo.lock` | `ab250bb78ee694d6d62d31d6e1ac175d3d9ab7450b9f9626c3e0f2e5fb619821` |
| `agent.ctg/src/lib.rs` | `7e36d3610f1acd4ebf40d35c071e80c0b91f8544aa7f16389615273bcc5590e1` |
| `agent.ctg/src/base.rs` | `b571c267b7c676be56f6f3e72400f55543bb432bcdc537482c04c81434036f99` |
| `agent.ctg/src/module.rs` | `9e04f3b9f729c1bb57e6e55696727bdcedded6a0c666a297059a5b5e14680783` |
| `agent.ctg/src/model_loop.rs` | `560fcc62b2769a593394a368558c52ca5feb49186a6494ec73d9e6024e9cbd55` |
| `agent.ctg/src/context.rs` | `9a1e5b133ea0df165ba2d656f471f118d2960cfd310c11dfbd1587a56e43adc6` |
| `agent.ctg/src/stream.rs` | `be7401b88e84bfb55c2a93dd1a0811f6b6bb6b49c3f718307c9839a77fe5d202` |
| `agent.ctg/init.lua` | `094a3de2fe89bdae9472d14323d62d624d24b7a294320d63c2c007fd6bc079c3` |
| `agent.ctg/.cartridge/tests/unit/run_state.rs` | `01ae01b25d97a43136fe6e7040c2164af6c3ea3052c5efcf41e232906c8d312a` |
| `agent.ctg/.cartridge/tests/integration/loop.rs` | `20636928a91b457a880bb96452ffa8ab3ad75087f794f1d3efa2ec7be7bd3a00` |
| `cartridge.ctg/src/loader/document.rs` | `5835d898cb39ae9a5254c2cc4f7a106ea617170d4760ed0abd07fc38f0be967f` |
| `cartridge.ctg/src/host/mod.rs` | `7b8e7a7328969ab3d01f89e8860ae6a0d5692fc0398ec607f14d9a216da0e300` |
| `cartridge.ctg/src/host/socket.rs` | `1c1a2c541e3ee1ee6bb1629385fed14ef1286620c7dbfe2732badacea6bee480` |
| `cartridge.ctg/Cargo.toml` | `4508a9b67ec1332782746ac225a9e9c9e86bf45c1b7bfa6a5fc8070d1aecc600` |
| `cartridge.ctg/.cartridge/tests/unit/src/tests/declarations.rs` | `50af78831372d591e6b2faf2eb59b49a89e8f7fe10e8d2b5ae7d258eecdd646f` |


## Editorial owner mapping — 2026-09-19

Round 4 explicitly permits editorial status/link cleanup without another round.
The PRD metadata and Review paragraph now reflect the recorded PASS 96. Historical
checkboxes from the retired combined memo became labelled historical criteria,
with their current owners stated; none was marked complete or removed. The four
active agent acceptance checks and the executable specification are unchanged.
The already-created downstream Harness leaf now explicitly carries the retired
per-record kind/disposition inspection criterion alongside its projection checks.
That leaf still awaits its own executable review within its inherited allowance.
The exact agent diff is preserved at
../../../.state/loop/an-event-declares-its-type/editorial-owner-map.diff.
This changes no approved agent implementation requirement; four rounds are used
and one remains. No integrated verification or collection is claimed.
