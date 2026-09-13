---
atomic: verify-behavior
subject: verify behavior
date: 2026-09-13
tags:
  - atomic
---

## Do

Run scoped checks and real-consumer probes, then required composed checks. Record exact command/cwd, output, revisions and explicit skips. Exercise negative and recovery behavior.

## Done when

Every acceptance box has observed proof; failures remain visible.

## Fails when

| seen | means | do |
| --- | --- | --- |
| Gate fails or was skipped | Completion is not established | Stop this step; record the evidence and resolve the named cause before continuing. |
