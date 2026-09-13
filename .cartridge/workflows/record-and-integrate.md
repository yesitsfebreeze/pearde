---
atomic: record-and-integrate
subject: record and integrate
date: 2026-09-13
tags:
  - atomic
---

## Do

Update local evidence and decisions, review the combined change, commit owner work coherently and update root pointers after owner commits exist. Use PRD's checked transitions; collect re-runs verification.

## Done when

Evidence and landed code match the recorded state and root references resolve.

## Fails when

| seen | means | do |
| --- | --- | --- |
| Evidence is stale or owner commits are absent | Integration is incomplete | Stop this step; record the evidence and resolve the named cause before continuing. |
