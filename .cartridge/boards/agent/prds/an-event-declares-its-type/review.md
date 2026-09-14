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
