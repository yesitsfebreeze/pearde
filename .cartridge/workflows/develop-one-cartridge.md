---
workflow: develop-one-cartridge
subject: Develop one complete cartridge contract with evidence
date: 2026-09-13
tags:
  - workflow
---

## Use when

- An central owner-scoped or cross-cartridge PRD is selected from the root board.

## Steps

| # | atomic | why | on failure |
| --- | --- | --- | --- |
| 1 | `read-context` | The owner, intended behavior, dependency status and relevant source revisions are recorded. | `stop` |
| 2 | `probe-contract` | The failure or missing capability is demonstrated with a reproducible observation. | `stop` |
| 3 | `write-specs` | Specs describe one implementable contract each and dependencies resolve in the root. | `stop` |
| 4 | `review-plan` | The current plan passes the delegated agent review threshold of 90/100 within at most five rounds. | `stop` |
| 5 | `implement-slice` | The change satisfies the accepted spec and can be inspected as a coherent diff. | `stop` |
| 6 | `verify-behavior` | Every acceptance box has observed proof; failures remain visible. | `stop` |
| 7 | `record-and-integrate` | Evidence and landed code match the recorded state and root references resolve. | `stop` |
