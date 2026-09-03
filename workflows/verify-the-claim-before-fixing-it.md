---
workflow: verify-the-claim-before-fixing-it
subject: Every id in the ontology digest points at a store nothing reads
date: 2026-09-02
runs: 1
tags:
  - workflow
---

## Use when

- A PRD reports something in the tree as broken, dead, empty or unrecoverable, and the fix it asks for is premised on that report being true.
- NOT when the break is reproduced by the tree's own gate — a failing test is already the measurement, and `reproduce-the-failure` is the route for that.

## Steps

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | `reproduce-the-reported-measurement` | Re-ran the PRD's own probe unchanged and got its answer, so the disagreement that followed was about the method, not the machine | `stop` |
| 2 | `ask-the-tool-what-it-actually-read` | `kern status` named the store it resolved and every other store on the machine — the reported reading was against a store that was not the subject | `stop` |
| 3 | `re-measure-against-the-named-target` | Pinned `KERN_DIR` to the store the artefact names; 21 of 21 ids resolved where 21 had been reported dead | `→ 2` |
| 4 | `prove-the-false-negative-in-a-clean-room` | Reproduced the empty-store auto-create in a fresh temp dir, so the mechanism is a fact about the tool and not a story about this repo | `→ 2` |
| 5 | `write-the-check-that-cannot-lie` | Turned the correct measurement into a command, and made it fail on an injected bogus id and refuse an absent store — it reported 13 false danglers before that | `→ 3` |
| 6 | `record-the-ruling-the-false-reason-supported` | Found the excluded rename resting on the refuted claim, so the ruling is written down rather than left to be flipped on a wrong reason | `stop` |
