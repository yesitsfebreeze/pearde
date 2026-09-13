---
kind: work
level: 9
status: open
description: Close the availability, diagnostic, retrieval-quality, and agent-interface gaps found in the 2026-09-07 Memory integration assessment.
read_when: planning the remaining work from the September 7 live Memory integration assessment
---

# memory-integration-assessment

## Do

Complete the children below in order, prioritizing availability and truthful diagnostics before retrieval quality and interface improvements. This continues [[@prd/work/memory--the-agent-surface-is-usable.md]] without reopening its completed fixes.

The 2026-09-07 assessment observed text queries returning `no tokio runtime`, vector query and report returning `daemon rpc: rpc adapter: eof`, question answering returning an endpoint-up hint, and a later CLI health request exceeding 20 seconds. Meanwhile 142 targeted Rust tests passed at `15761c01`, and the typed-work-field checks passed. The deployed binary's source revision was not established. Reproduce each finding against the current revision before changing code; these observations do not prove that every failure has the same cause.

subwork:
- [[@prd/work/memory--memory-integration-runtime-refusals.md]]
- [[@prd/work/memory--memory-integration-fast-readiness.md]]
- [[@prd/work/memory--memory-integration-embedding-status.md]]
- [[@prd/work/memory--memory-integration-provider-errors.md]]
- [[@prd/work/memory--memory-integration-lifecycle-canary.md]]
- [[@prd/work/memory--memory-integration-template-hygiene.md]]
- [[@prd/work/memory--memory-integration-semantic-evaluation.md]]
- [[@prd/work/memory--memory-integration-bounded-history.md]]
- [[@prd/work/memory--memory-integration-setup-contract.md]]
- [[@prd/work/memory--memory-integration-cloud-disclosure.md]]

The implementation belongs in each child's lane. This parent does not authorize stopping the shared daemon, repairing the production store, deleting existing facts, sending private corpus material to a new provider, or performing a deployment without the relevant approval.

## Check

Every child is `status: done` with its acceptance evidence recorded. Repeat the live integration probe against an identified deployed generation and record query, answer, report, readiness, and direct-ID results separately from isolated test results. Record unavailable dependencies and any checks not run; passing unit tests alone does not complete this parent.
