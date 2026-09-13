---
atomic: probe-contract
subject: probe contract
date: 2026-09-13
tags:
  - atomic
---

## Do

Use a disposable fixture to exercise the actual owner and consumers. Record baseline behavior, failure, command, cwd and source revisions.

## Done when

The failure or missing capability is demonstrated with a reproducible observation.

## Fails when

| seen | means | do |
| --- | --- | --- |
| Fixture uses production state or does not reproduce | Evidence is not safe or relevant | Stop this step; record the evidence and resolve the named cause before continuing. |
