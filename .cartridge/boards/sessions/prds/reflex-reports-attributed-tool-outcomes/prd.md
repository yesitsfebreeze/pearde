---
repo: /Users/feb/dev/cartridge/sessions.ctg
state: "done"
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: sessions
work-kind: rollup
review-round: 3
review-status: passed
canonical-scope: reflex-reports-attributed-tool-outcomes
needs: ["@runtime/native-tool-observation-adapter"]
commit: "191e2b6cb4291bdcce7a894f98bb2d475361d30f"
---

# reflex-reports-attributed-tool-outcomes

Use the existing execution/session observation boundary as the owner of tool-use attribution. Classify actor and activity origin, attempt versus completion, outcome, duration and size; retain unknown historical fields. Landscape can consume the evidence, but memory does not host a second Reflex service.

Runtime collection is owned by [native-tool-observation-adapter](../../../runtime/prds/native-tool-observation-adapter/prd.md); sessions projection by [attributed-outcome-report](attributed-outcome-report/prd.md). Both inherit rounds 1–2. This parent remains incomplete until actual composed mixed-work evidence passes, including adapter receipt validity. Synthetic projector fixtures alone are insufficient. Historical source aliases remain on this parent.

## Acceptance

- [x] A mixed fixture of agent calls, UI reads, polling, discovery and cancelled work produces distinct correctly attributed observations.
- [x] Old rows retain unknown status/time rather than gaining invented success or billing; source/descriptor changes identify stale verdicts.
- [x] Default telemetry excludes sensitive arguments/bodies, has bounded retention and cannot turn observation failure into tool failure.

## Proof and recovery

Start at [main.rs](../../../main.rs).

Probe the current behavior in a disposable fixture; record source revision, exact command and expected/observed results before writing specs. Use `just test sessions` from the composed root with the acceptance fixtures. The actual composed gates and dependency receipts now pass; see [proof](proof.md).
Preserve the last usable implementation and durable data on failure; report partial effects without automatic replay. Narrow the owner-local file footprint before claiming.

## Review

[Round 2 agent review](review.md). Inherits round 1 from `reflex-reports-attributed-tool-outcomes`; maximum five rounds.

Named channel registration revalidation at 423ecd32: source footprint includes registered channels and its shared mailbox codec; acceptance and behavior gates remain unchanged.
