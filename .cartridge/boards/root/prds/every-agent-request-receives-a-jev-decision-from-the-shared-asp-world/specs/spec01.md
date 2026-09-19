---
complexity: 3
footprint:
  - .cartridge/hooks/request-assessment.ts
  - .cartridge/tests/integration/jev-request-hook.test.ts
  - .cartridge/tests/integration/jev-workflow.test.ts
  - .cartridge/memos/system/jev-request-assessment.md
  - .cartridge/memos/note/jev-shared-request-workflow.md
  - .cartridge/memos/note/jev-request-workflow-proof.md
  - .claude/settings.json
  - .gitignore
---

# Consult the shared ASP world before agent execution

JEV assesses an actual user request by expanding the composition root, reading
registered peer work, searching relevant entities, selecting evidence and
asking the declared closed-set workflow judgement. It returns proceed, inspect,
coordinate, clarify or fallback with confidence and inspectable evidence.
The caller is excluded from peer work. Missing providers and truncation remain
explicit; partial context cannot produce an unqualified proceed action.

Assessment responses fit within 6000 UTF-8 bytes and aggregate discarded
diagnostic identifiers. Selected identifiers remain whole. The metadata journal
retains the effective action and evidence references without storing prompts.
ASP exposes decision:root and individual decisions, including after reload.

Harness automatically assesses native transcript user turns and proxy injection
requests. Stable session/turn identity shares concurrent assessments and avoids
repeat model calls during tool rounds. Failures produce advisory fallback;
a saturated model context fails explicitly instead of dropping the assessment.
Passthrough failures send an unavailable notice to the external model. Native
agents publish their actual current work before assessment. Sessions publishes
registered checkpoints through agents:root without claiming process liveness.

Claude Code uses a project UserPromptSubmit hook. Sessions owns the durable
external conversation mapping under host-configured principal/workspace/profile.
The hook registers work before assessment and clears it at Stop/SessionEnd.
MCP and repository agents can use tool.jev or the composed instruction. Existing
clients must load the changed settings; unrelated applications are not intercepted.

Local voice performs assessment after transcription and before its brain call.
Hosted voice receives instructions to delegate each substantive question for
assessment and waits for returned guidance; consultation is model-driven because
the current hosted protocol lacks a client-controlled pre-answer turn gate.
The voice layer carries bounded peer and selected evidence identifiers. Delegated
native workers also follow the harness path. None of these decisions authorizes
tools, changes policy, or claims unpublished information exists in ASP.

The implementation preserves other panes' manifest command migrations, runtime,
trace, memory and dashboard edits. Component commits are selective and already integrated independently. Their
Git references were recorded by root source commit 0ba9258. They are not file
footprints of this root wrapper: those directories contain concurrent foreign
edits which this collector neither owns nor can mark clean. The runtime gate
verifies their combined behavior. Shared config
and README integration hunks are committed separately without collecting unrelated
concurrent work.

## Acceptance

- [x] Independent JEV and consumer review scores meet 90/100 with no blockers.
- [x] Real-model native context, proxy injection and Claude hook see peer work and retain decisions across reload.
- [x] Tool rounds reuse a decision; inactive external work is no longer reported running.
- [x] Voice assessment precedes local replies and hosted delegation, with the hosted enforcement limit documented.
- [x] Owner tests, checks, audits and isolation pass; the running composition exposes JEV and ASP.

## Verify and Proof

```sh
bun test ./.cartridge/tests/integration/jev-request-hook.test.ts
CARTRIDGE_LIVE_SYSTEM=1 bun test ./.cartridge/tests/integration/jev-workflow.test.ts
./task isolation
```

Independent reports and the observed production decision identifiers are retained
in the adjacent review record and the shared proof memo. This gate deliberately
uses the configured JEV API and makes real model calls. Gate tuning and model
training remain separate PRDs.
