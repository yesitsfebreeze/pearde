---
atomic: write-specs
subject: write specs
date: 2026-09-13
tags:
  - atomic
---

## Do

Create a small centrally stored PRD for the source owner for each independent outcome before expanding its
implementation detail. Aim for 150–300 words per leaf, with three to five checks;
split before exceeding 400 words. Keep a parent as a short linked work index.
Use the PRD refinement operation for same-board children and qualified needs for cross-owner
work. Children inherit used review rounds and source history. Narrow and rebase
footprints. Author specs/specNN.md from the probe with observable acceptance and
runnable Verify and Proof gates.

## Done when

Specs describe one implementable contract each and dependencies resolve in the root.

## Fails when

| seen | means | do |
| --- | --- | --- |
| Unknown command or overlapping ownership | The proposed implementation boundary is unproven | Stop this step; record the evidence and resolve the named cause before continuing. |
