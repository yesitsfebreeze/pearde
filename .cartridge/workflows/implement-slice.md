---
atomic: implement-slice
subject: implement slice
date: 2026-09-13
tags:
  - atomic
---

## Do

Check that the current plan/spec revision has the completed review gate: reviewer
agent score is at least 90, no blocking finding remains,
and at most five rounds were used, or that the PRD meets every review-plan
fast-path condition. Pending or stale ratings do not authorize this
step. Follow the owner repository workflow and implement the smallest complete
accepted contract. Keep domain state with its owner; preserve existing stores and
unrelated changes.

Follow the [cartridge layout rule](../boards/root/README.md#keep-cartridge-roots-small).
Place all new tests, fixtures, scripts, validation, workflows, and development
artifacts in the owner's `.cartridge/`, or the root `.cartridge/` for shared
support. Wire discovery and commands to those paths and keep any required root
entry point minimal. Reuse existing files to keep cartridge roots small.

## Done when

The change satisfies the spec and can be inspected as a coherent diff.

## Fails when

| seen | means | do |
| --- | --- | --- |
| Scope expands beyond the spec | Re-analysis or refinement is required | Stop this step; record the evidence and resolve the named cause before continuing. |
| Review is missing, failed, pending, exhausted or stale | The current plan is not accepted | Preserve work and resolve the review before dependent implementation. |
