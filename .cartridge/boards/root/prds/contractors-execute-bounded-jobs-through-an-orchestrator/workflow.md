# Contractors: the workflow is the specification

This is the proposed cartridge contract, dated 2026-09-19. The example JSON is a design fixture, not a currently implemented API. Contractor jobs have one authoritative artifact: the validated event workflow. This document explains the cartridge that consumes it; it is not a second job specification.

## User flow

The user talks to the main agent. JEV assesses the request against selected ASP evidence. The orchestrator gives bounded planning sub-agents the outcome, permitted capabilities, relevant memo procedures and current event declarations. The planners return workflows containing events, parameters, requirements and agent assignments. An independent planning check tests coverage and boundaries. Validation returns a revision-bound receipt. The orchestrator dispatches that exact workflow through contractors.

Deterministic steps call existing events directly. Only steps needing reasoning start an agent. Agent assignments identify execution contexts, not a demand for a fresh model call on every event. A planner may use the existing agent start/status lifecycle, but its result must satisfy the structured workflow contract before any proposed effect runs.

## One capability and its owners

| Owner | Responsibility |
| --- | --- |
| Contractors | Validate workflows, execute their ready nodes and retain bounded attempts, dependency requests and result receipts. |
| PRD | Own task dependencies, claims, integration order and collection against workflow requirements. |
| Memo | Own reusable authoring procedures, planner instructions and requirement patterns. |
| ASP | Discover declared events and retrieve revision-bound evidence. |
| JEV | Return advisory judgment and evidence; never grant runtime authority. |
| Agent, harness and router | Supply the existing inference loop, bounded context and model transport. |
| Host | Enforce process confinement, immutable grants and private broker identity. |

PRD owns the canonical workflow reference and digest. Memo procedures are referenced with their revisions; they do not become a parallel task-state store. Contractors retains execution state and evidence, not a second board. Workflow revisions are immutable after admission.

## Proposed public surface

The cartridge declares `contractors`, `tool.contractors`, `contractors.request`, `contractors.event` and `asp.contractors`. Names are proposed and must be checked for collisions during admission implementation. The service offers `validate`, `run`, `status`, `cancel` and `resolve`. `validate` has no effects. `run` requires the exact validation receipt plus existing authority. `resolve` is orchestrator-only and binds a request to a verified child artifact or a denial. Worker-facing `contractors.request` can only submit a bounded requirement request for its authenticated attempt. `status` exposes observations, never credentials or private context bodies.

Declared needs include only the selected execution and lifecycle interfaces. ASP `act` is not a dispatch escape hatch: the existing protocol refuses it to cartridge/agent callers. A dynamically selected event must still be declared in the composition and admitted by both the cartridge's needs and the job's grants. Do not grant `tool.*` as ambient worker authority. Discovery of an event does not make it callable.

## Workflow representation

Version one is JSON; human interfaces may render it differently without maintaining another source of truth. The workflow contains:

- Identity, task reference, format version and a host-computed digest over canonical content.
- Inputs naming entities or staged files and exact revisions, with explicit unavailable or partial evidence.
- Agent assignments naming role, selected context, model policy, read/write sets, event-operation/resource grants and finite budgets. Credentials and caller identity are never model-supplied parameters.
- Steps naming an ID, predecessor IDs, assigned execution context, declared event, parameters, completion rule and expected output shape.
- Requirements naming deterministic checks against observed outputs or the candidate artifact. Every requirement identifies its verifier and evidence source.
- Aggregate limits for tokens, elapsed time, concurrency, output bytes, child count and nesting depth.

Parameters are JSON literals or explicit references to predecessor outputs by step ID and JSON Pointer. References cannot address future, unrelated or failed steps. The schema reserves the reference wrapper so ordinary literal objects remain distinguishable. There is no shell interpolation, general expression evaluator, loop or unrestricted script node in version one. Tool payloads use the actual declared envelope, such as `{"op":"call","input":{...}}`; trusted context is injected by the broker.

Event schemas currently describe inputs. Workflow output schemas and deterministic result normalization are new contracts, validated after completion. A normalizer for each admitted service converts its real envelope into a bounded typed result without treating text as control. A transport success or schema-valid tool envelope with an error is not semantic success: normalize its error flag and refuse dependent dispatch. File-content requirements use a trusted candidate-file reader; never strip line numbers or ignore truncation to infer exact content from a display-oriented tool.read response. Agent start returns a session/run acknowledgment; completion must poll or observe that exact run and obtain a validated result. Text saying “done” cannot satisfy a requirement.

Checks initially support equality, containment and named check success over trusted normalized evidence. File equality reads the candidate from the verifier's scoped view. A requirement cannot use the writer's self-reported success as its sole evidence. The verifier has independent identity and read access to the candidate; it has no source write permission. Human intent coverage remains a planner/reviewer judgment, explicitly distinct from machine verification.

## Admission and confinement

Validate the DAG, event availability and payload schemas, output bindings, requirement coverage, selected input revisions, writer conflicts and resource bounds before effects. Persist a validation receipt binding the workflow and declaration/configuration revisions. At dispatch, check those revisions and the currently granted authority again. Drift returns a diagnostic for revalidation, not silent adjustment.

Use a separate confined composition per contractor with the existing agent engine. Its root contains only staged allowed files, scratch space and explicit runtime dependencies. The current host sandbox grants read access under its root, so using the full checkout would break isolation. Network grants are empty. Inference travels through a private authenticated broker; provider keys, shared host tokens, host sockets and personal environment are absent from the worker.

The broker restricts event, operation, parameter values, resources and session/attempt identity. A privileged sibling service must not become an indirect route to forbidden files. File operations target the staged job view rather than global session branches. Broker endpoints and their implementation may vary by platform; each advertised platform must prove the same boundary or refuse launch. Version one excludes arbitrary shell execution. Build/test execution is a later explicitly confined capability, not a shortcut through `tool.shell`.

## Dependencies, recovery and result collection

A worker that needs another file or decision submits a requirement request with its evidence and desired artifact. The orchestrator answers from existing evidence or runs a separately validated child workflow. It cannot increase the waiting worker's grants. Returned data is bounded, attributed and revision-bound. Cyclic requests, excessive depth, budget exhaustion and denied requests end in explicit blocked or failed outcomes. Any semantic workflow change creates a new admitted revision.

A run records admitted, running, waiting, succeeded, failed, cancelled or unknown status. Receipts bind workflow, step, attempt, input, declaration and candidate revisions. Record intent before an effect. Submission keys deduplicate identical attempts and reject conflicting payloads. After an ambiguous mutation, mark unknown and reconcile with the service owner. Only proven read-only or idempotent operations can retry automatically. Never promise exactly-once effects without downstream support.

PRD claims task write footprints and determines which workflow is ready. Contractors orders nodes only inside that workflow. Changed input hashes and writer conflicts block dispatch or collection. Cancellation revokes the broker and terminates only owned processes; waiting time counts toward the deadline. Restart reconciles durable receipts and live worker identity without replaying unknown effects. PRD verifies every requirement against the candidate and integrates it under its existing revision/footprint checks. A worker's terminal state is not collection.

## First proof and exclusions

The composed proof starts with file A and file B. A's contractor cannot read B through a path, symlink, host socket or brokered service. It requests B's interface; the orchestrator sends B to another contractor. The revision-bound answer unblocks A. An independent verifier rejects stale inputs, forged success and an extra output file, then accepts the intended candidate. Crash injection between mutation and acknowledgment leaves unknown state without replay.

The example JSON demonstrates the small deterministic path using currently declared `tool.read` and `tool.edit` payloads; the planner/dependency proof exercises reasoning through the existing agent lifecycle once sealed worker support exists. Placeholder inputs in the example must be bound to actual hashes before admission. Deterministic nodes need no inference. The result normalizers and file-check evaluator are planned, not claimed as current APIs.

Initial exclusions are arbitrary network access, arbitrary shell commands, unbounded recursion, autonomous permission expansion, general-purpose workflow expressions and replacement of the tmux/proxy worker path. Speed and token savings remain hypotheses. Measure total planner, assessment, worker, retry and verifier usage on paired tasks with identical correctness gates, including median and tail elapsed time. Report routing failures and unavailable JEV separately; do not omit them from totals.

## Evidence used for this plan

Read `cartridge.ctg/docs/asp.txt`, `cartridge.ctg/src/sandbox/mod.rs`, `cartridge.ctg/src/host/process.rs`, `agent.ctg/README.md`, `agent.ctg/src/lib.rs`, `policy.ctg/README.md`, `fs.ctg/cartridge.json`, and `prd.ctg/src/lifecycle.ts`. ASP exposes event schemas; current agent start does not declare per-job scopes; PRD currently collects Markdown verification blocks. These observations explain the owner-aligned delivery leaves. The new workflow and broker have not been implemented or tested.
