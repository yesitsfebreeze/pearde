---
kind: work
level: 10
status: open
description: Audit mine and the remaining LiteLLM integration against Memory's existing infrastructure and specify a native consolidation plan
read_when: deciding how mine should reuse Memory transport, configuration, lifecycle, LLM clients, observability, and utilities
---

# audit-mine-for-native-memory-integration

## Do

**Mission and scope**

[[memory-alone-owns-model-access]] is the user's final acceptance contract:
launch only Memory, with no LLM command, LiteLLM installation, hidden Python
router, old configuration dependency, or separate service startup step.
This supersedes the older `memory llm` command-preservation bullet below.
Explicitly design the native login operation and agent communication SDK,
and prove the end state with the obsolete installation absent. See
[[native-routing-still-reads-litellm-state]] for verified starting evidence.

Produce an evidence-backed architecture audit and an executable consolidation
plan that makes mine a native Memory subsystem. The user's concern is that the
LiteLLM replacement was implemented largely as a separate router and then
placed inside Memory, while Memory already had transport, lifecycle, configuration,
LLM clients, process management, and utilities that should have been examined
and reused.

Treat “everything inside Memory and native” as a requirement for ownership,
configuration, operation, and implementation—not merely a single executable
name. The end state must not depend on a separately installed LiteLLM Python
service, a Codex HTTP shim, the old Python `llm` launcher, or a second router's
configuration tree to run Memory's model routing. External agent applications,
provider endpoints, and the providers' credential authorities remain external
boundaries; do not confuse those with duplicate infrastructure inside Memory.

This work item is the focused investigation and design pass. Its deliverable
is a source-grounded target design, migration plan, and appropriately scoped
follow-up work. Do not use it as authorization for an unbounded rewrite,
credential relocation, index rebuild, service shutdown, or removal of working
user configuration. Read-only inspection and isolated experiments are enough
to establish the design. Capture unresolved architectural questions explicitly
instead of concealing them in speculative implementation tasks.

**1. Establish the current tree and contract**

Read `AGENTS.md`, [[memo-layout]], [[code-laws]], [[system-commands]],
[[terminal]], [[@prd/routine/run-board.md]], and [[lanes-not-a-shared-tree]]. Read the memo-writing
rules before changing the record. Use the warm editor/LSP for semantic
navigation and the repository's normal lane workflow for code experiments.
Preserve other people's uncommitted changes. Do not start a project daemon in
an experimental lane just to inspect CLI argument handling.

Read these decisions and incident records before proposing replacements:

- [[mine-is-managed-through-memory-llm]]
- [[memory-launch-uses-mine]]
- [[mine-routes-through-task-frontiers]]
- [[local-models-are-configurable-last-resort-routes]]
- [[mine-request-routing-is-bounded]]
- [[responses-history-must-preserve-assistant-output-types]]
- [[memory-launch-keeps-background-models-and-processes-under-control]]
- [[proxy-plugins-can-route-parts-of-a-request]]

Inspect the actual checked-out source. The following is a starting map, not
an assertion that every module is the correct destination for moved code:

| Current surface | What to inspect |
|---|---|
| `src/mine/src/catalog.rs` | Models, provider routes, capability filtering, paths, inventory initialization, duplicated routing defaults |
| `src/mine/src/frontier.rs` | Task detection, benchmark provenance, ranking and refresh |
| `src/mine/src/protocol.rs` | Anthropic, Chat Completions and Responses conversion; streaming and tool-call semantics |
| `src/mine/src/proxy.rs` | HTTP service, provider clients, authentication boundaries, concurrency, deadlines, fallback and healing |
| `src/mine/src/auth.rs` | Provider credential adapters, refresh coordination and atomic JSON writes |
| `src/mine/src/health.rs` | Incidents, request versus route failures, recovery and persistence |
| `src/mine/src/launch.rs` | Agent registry, generated profiles, endpoint/key injection and native agent paths |
| `src/mine/src/cli.rs` | Management commands, path overrides, reload, connection reporting and native Claude discovery |
| `src/commands/src/commands_launch.rs` | Agent orchestration, daemon detection, detached startup and session proxy lifetime |
| `src/commands/src/commands_proxy.rs` | Harness HTTP forwarding, request/response recording and resource ownership |
| `src/commands/src/commands_admin.rs` | Existing detached-process and daemon management helpers |
| `src/config/src/config.rs` | Config merge, validation, secret redirection, private files, log paths, and `MineConfig` |
| `src/transport/src/typed.rs` | Typed channels, local/in-process adapters, framing, peer verification and endpoints |
| `src/transport/src/memory_rpc.rs`, `hub_rpc.rs` | Existing command/service contracts and connection lifecycle |
| `src/llm/src/llm.rs` | Memory's existing inference and embedding client, error taxonomy, retries, admission and shutdown behavior |
| `src/util/src/lifecycle.rs`, `util.rs` | Shutdown, in-flight work, time, IDs, throttled logs and other reusable primitives |
| `src/identity`, `src/hub`, `src/health`, `src/rpc`, `src/test_support` | Build/config identity, service ownership, health reporting, RPC exposure and test infrastructure |

Record commit IDs and relevant symbols for findings so a later implementer
can distinguish observed duplication from assumptions.

**2. Trace the real request and management paths**

Draw the current data flow from `memory launch claude` through the agent,
harness proxy, mine and provider. Include streaming responses, tool calls,
background agent requests, cancellation, errors and recovery. Trace Codex
and Pi separately where their APIs or startup contracts differ.

Trace Memory's own `[reason]` and `[embed]` consumers as well. Identify which
calls bypass mine today, what semantics their callers require, and where
routing could be shared without introducing a request back into the same
router. Trace `memory llm status`, `connections`, `frontier`, `models`, `sync`,
and `serve`: show which use live state, which read snapshots, and which own
configuration or credentials.

Show process boundaries and owners explicitly. Include the project daemon,
machine hub, shared router, session proxy, external agent, and any remaining
LiteLLM/shim processes. Measure or inspect the actual listeners and parent
relationships rather than inferring them from names. Do not terminate live
services during this audit.

**3. Build a reuse and duplication matrix**

For every infrastructure responsibility in mine, identify the corresponding
Memory capability or establish that none exists. For each row provide:

- The current mine symbol and its callers.
- The existing Memory symbol and actual guarantees, with source references.
- Whether the implementations overlap completely, partially, or only in name.
- The proposed disposition: reuse directly, adapt an existing interface,
  extract a genuinely shared primitive, retain model-specific behavior, or
  delete unused code.
- The behavioral difference, dependency/layer consequences, migration work,
  and regression evidence needed.

Cover transport and HTTP client ownership, request framing, streaming,
backpressure, cancellation, deadlines, retry budgets, concurrency admission,
service discovery, process startup/shutdown, config loading, path resolution,
credential lookup, atomic persistence, time/ID helpers, logging, metrics,
health state, CLI dispatch, and test fixtures.

Do not turn `util` into a dumping ground. Model ranking, capability checks,
provider-specific authentication, prompt/API translation, and tool semantics
are domain behavior. Keep them with a clear domain owner unless an existing
Memory domain module already owns the same contract. Reuse is justified by
shared semantics and real callers, not by reducing a line count.

**4. Resolve transport and crate ownership deliberately**

Determine what Memory's `transport` actually provides. Its typed local RPC
adapters are not automatically an HTTP/SSE provider client. Identify where
in-process calls or existing local RPC should replace internal HTTP round
trips, and where an external agent or provider genuinely needs HTTP. Evaluate
reuse of connection ownership, cancellation and framing separately from
provider wire-format conversion.

Specify one owner for each service contract. Compare a shared router process,
a service hosted by existing Memory infrastructure, and an in-process routing
core with adapters at external boundaries. Recommend the smallest design
that meets the real ownership and isolation requirements; do not require all
code to live in one process just because it ships in one binary.

Produce a before/after crate dependency diagram. Inspect current layer
headers and gates. In the current design mine declares itself L0, while
configuration, identity and transport occupy other layers; importing them
blindly is not an acceptable consolidation. Also inspect the existing
`config -> llm` relationship before introducing any `llm -> config/mine`
dependency. Show how the proposed interfaces avoid dependency cycles.

Audit direct dependency versions and feature sets against workspace-owned
dependencies. Specify which duplicate dependency declarations disappear and
which distinct requirements are intentional. Do not claim runtime savings
merely because a crate or helper was renamed.

**5. Make Memory the configuration and state authority**

Inventory every remaining dependency on `~/.config/litellm`,
`~/.local/state/litellm`, `~/.local/state/llmine`, `LLMINE_*`,
`LITELLM_MASTER_KEY`, provider/alias/agent JSON registries, generated agent
profiles, and old launch/service files. Inspect the dotfiles source through
`chezmoi source-path`; do not assume a stale chezmoi checkout is authoritative.
Include the Python `llm` entry point, LiteLLM hooks, Codex shim and service
provisioning only to establish what still consumes them and how to retire
those dependencies safely.

Specify the native Memory config schema, precedence, validation and ownership
for provider connections, model aliases, agent configuration, routing policy,
frontier sources, timeouts, concurrency, credential references, and state
locations. Eliminate duplicated defaults such as `MineConfig` versus mine's
runtime routing defaults. Distinguish desired configuration from discovered
inventory, benchmark snapshots, live health, and durable recovery records.

Resolve machine-wide versus project-specific policy explicitly: one shared
router must not silently keep the first project's settings and apply them
to every later project. Explain how effective policy is identified, passed,
validated, reloaded and reported for each request or service instance.

Provide a one-time migration plan with verification and recovery steps.
Inventory readers before deleting a path or key. Preserve credentials and
health evidence; do not copy OAuth tokens into ordinary TOML or logs. Memory
can own credential references while Codex or Claude remains the authority
for its login. The final runtime must work without the old LiteLLM trees or
processes. Temporary migration mechanics must have an explicit removal point;
do not retain a permanent second configuration system or forwarding binary.

Installation order matters: a new config must not be activated before the
installed binary understands it. Describe atomic binary/config activation,
service version/config identity, graceful replacement, and what a failed
upgrade leaves running. A previous deployment briefly broke `memory launch`
by writing new `[mine]` fields before installing the matching executable.

**6. Preserve the routing and agent contract**

The following behavior is required in the target design:

- `memory launch claude` means `memory launch claude auto:code`; explicit model
  or frontier arguments override the default.
- Administrative operations belong to Memory. Remove LLM-specific startup
  requirements and executable surfaces under [[memory-alone-owns-model-access]];
  specify the native command/API layout rather than preserving `memory llm`
  solely because it exists today.
- Claude background requests inherit the selected model unless explicitly
  configured otherwise; choosing Astra must not silently select a local
  model through `auto:free` for background work.
- Local generation is a configurable last resort. Ollama Cloud is remote
  inference even when accessed through the local Ollama service.
- Structured request fields determine the task without loading a separate
  local classifier. Frontier rankings carry evidence, dates and capability
  constraints; a provider model listing is not proof of usable inference.
- Failure, fallback, timeout and concurrency budgets have a single owner
  across layers. Nested retry loops must not multiply work or elapsed time.
- A provider or plugin pointing back into the routing path cannot create
  an unbounded cycle. Distinguish legitimate composition from recursion.
- Request-specific errors do not globally disable an otherwise healthy route.
  Quota/payment failures are reported honestly, and are not “repaired” by
  ignoring the account limit. Recovery persists verified results and does
  not starve behind incidents it cannot repair.
- Streaming preserves tool-call IDs, event order, cancellation and resource
  release. Once output has been emitted, no fallback replays that request.
- Assistant history uses `output_text` when represented as typed Responses
  assistant messages; user/developer content uses the appropriate input
  type. Preserve the regression that previously caused multi-turn Astra
  requests to fail while fresh prompts passed.
- Router services outlive individual agent sessions when intended. Session
  resources are cleaned up. A slow but bound daemon is not treated as absent
  and repeatedly spawned.

Preserve supported Anthropic Messages, OpenAI Chat Completions and Responses
behavior, including multi-turn history, tools, system/developer messages,
reasoning controls and supported media input. Enumerate unsupported features
and their deliberate errors; do not silently discard input or fabricate
complete responses.

**7. Separate account access, model capabilities and future modalities**

OpenAI/ChatGPT subscription access, native Claude Max logins, API credits,
and Ollama Cloud access are different connection types. Recheck current
availability and represent each accurately. Do not infer that a native agent
login is a working generic HTTP inference route, or that this assistant's
own model access proves Memory's provider route is usable. Any proposed new
subscription integration must use a supported, verified access path.

Design how the existing Memory LLM and embedding clients fit the shared model
catalog and routing core. Embedding frontiers may rank models for creating
or rebuilding an index, but the active index must be pinned to an embedding
space. Equal vector dimensions do not make two models interchangeable.
Specify provenance, dimensions, index compatibility and rebuild behavior;
do not enable silent cross-model embedding fallback or reembed user data
as part of this audit. Dedicated embedding and media-generation endpoints
must not be represented as already implemented merely because text routing
has modality labels.

Use [[proxy-plugins-can-route-parts-of-a-request]] to assess extension seams
for prompt parsers, tool routing and split/join model requests. The current
memo is a design direction, not an implemented feature. Identify contracts
for request identity, provenance, cancellation, budgets, joins and side-effect
idempotency without building a plugin framework during this work item.

**8. Verify that reuse improves the system**

Define and, where practical, run isolated before/after design experiments.
Use deterministic fake upstreams to distinguish router overhead from model
latency. Record startup cost, resident memory, additional processes/listeners,
time to first forwarded event, streaming overhead, request amplification,
file writes, and bounded failure latency where relevant. Account for harness
ledger costs and avoid logging full conversations merely to measure routing.

Live smoke tests should be few, explicitly identify the chosen route, and
respect real quota/payment errors. Never spend a long fallback walk probing
hundreds of paid models to demonstrate that the architecture works. Do not
claim quantified performance gains without measurements.

Reuse `test_support` and existing regression suites where they fit. Identify
tests that should move with their owning code and any missing contract tests.
Keep frontend and provider wire-format tests even if transport mechanics
move into shared infrastructure.

**9. Deliver a concrete implementation handoff**

Include a clean-install acceptance gate that excludes all old executables,
Python environments, services and configuration trees, starts only `memory`,
and exercises login, routing and an agent tool exchange. Test the normal
no-subcommand entry point: today `src/main.rs` sends it to `run_server`,
whereas model-router startup is separately reached from `memory launch`.
Specify which Memory owner starts the model runtime before declaring this
single-entry-point requirement satisfied.

Write the audit and target architecture into appropriately scoped memos,
following the record's atomicity rules. Link them from this work item.
Deliver a concise top-level recommendation supported by:

1. Current request, service and configuration ownership diagrams.
2. The symbol-level reuse/duplication matrix, including justified retention.
3. Target module and crate boundaries with a cycle-free dependency graph.
4. Native configuration/state/credential contracts and the migration table.
5. The behavior-preservation and regression matrix.
6. Measurements or explicitly unmeasured performance claims.
7. A sequenced implementation plan with real paths/symbols, dependencies,
   removal targets and executable checks for each change.

Create follow-up work memos only for decisions sufficiently resolved to be
executable. Keep each implementation item focused enough for its stated
level. If a choice remains unresolved, record the question, evidence,
recommended answer and consequences; do not disguise it as a settled task.
This work item is complete when the investigation and handoff are complete,
not when the entire proposed consolidation has been implemented.

## Check

- Every infrastructure responsibility listed above has a source-grounded
  reuse decision or an explicit evidence-backed gap. The audit names real
  callers and differences in guarantees, not only similarly named modules.
- The target design makes Memory the runtime/configuration authority, identifies
  all remaining LiteLLM dependencies, and explains how the final installation
  runs without them. External agents and credential authorities are described
  accurately rather than mislabeled as internal duplication.
- The proposed dependency graph respects or deliberately revises documented
  layers without creating cycles. Transport reuse distinguishes internal RPC
  from external HTTP/SSE requirements.
- The migration plan covers existing users, credentials, inventory, rankings,
  recovery state, multiple projects, service identity and safe activation
  order. It does not require abandoning working routing during migration.
- The acceptance matrix covers defaults and explicit overrides, background
  model selection, local/cloud distinction, request-scoped failures, recovery,
  bounded retries/deadlines/concurrency, cycle rejection, multi-turn history,
  streamed tools, cancellation, daemon presence and lifecycle ownership.
- Embedding model selection is explicitly constrained by index compatibility;
  future plugin/media work is clearly distinguished from current support.
- Follow-up implementation items have concrete `Do` and `Check` sections and
  dependencies; unresolved choices remain questions with recommendations.
  A subsequent agent can execute the plan without reconstructing this chat.
- `just memos-check` passes. Any code experiments use an isolated lane, run
  their relevant checks, and leave no stray services, credentials, generated
  profiles or temporary runtime dependencies behind.
- The final handoff names the audit/decision/work files, summarizes the chosen
  reuse strategy and residual uncertainties, and reports actual measurements
  separately from proposed benefits. Mark this work item `done` only after
  those artifacts and checks exist.

The user's instruction to finish the remaining work authorized implementation.
[[memory-native-model-service]] records the implemented ownership model, storage
migration, recovery boundary and live evidence. Memory commit `2a66abc6` is
installed; dotfiles commit `e12b8c7` removes the obsolete installation surfaces.
All 1,380 tests passed, with 17 skipped; lint and the memo gate passed. Landing
is blocked by existing uncommitted trunk edits in the launcher and routing
files; `just land memory-native-model-runtime` refused to overwrite them. The
committed lane remains available for integration without discarding that work.

Replanned 2026-09-09: `git merge-base --is-ancestor 2a66abc6 main` exits zero;
the landing blocker above is historical. Reconcile the existing handoff
against its checks, not a second architecture audit or runtime implementation.
Ancestry does not prove current acceptance; no box is closed by this replan.
[[@prd/work/memory--provider-recovery-proves-its-authority-boundary.md]] holds the remaining recovery
policy evidence separately.
