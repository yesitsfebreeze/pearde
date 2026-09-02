---
atomic: record-the-ruling-the-false-reason-supported
subject: Found the excluded rename resting on the refuted claim, so the ruling is written down rather than left to be flipped on a wrong reason
date: 2026-09-02
updated: 2026-09-02
runs: 1
---

## Do

1. Find the work that cites the refuted claim. The board is not walked by hand
   — `python3 <pearde>/resources/board/plan.py scan` names every PRD; then read
   the named files directly. A recursive grep over `.pearde/prds/` is refused.
2. Write the ruling as a memo naming the measured fact, what it beat, and that the cited reason is wrong.

## Done when

- Every citation of the refuted claim is either corrected or covered by a memo a reader of it would find.

## Fails when
